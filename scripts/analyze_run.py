#!/usr/bin/env python3
"""Analyze one preserved Logic Theorist run bundle.

This companion script reads an existing run directory and writes analysis
artifacts under the companion repository. It does not run Logic Theorist,
modify the IPL-V executable specimen, contact GitHub, or delete evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


NOTABLE_THEOREMS = ("2.21", "2.24", "4.13", "4.24", "4.25")

COLON_PREFIX_RE = re.compile(r"^:+\s*")
THEOREM_RE = re.compile(r"^(?P<theorem>\d+\.\d+)\s+(?P<expression>\S.*)$")
METRIC_RE = re.compile(
    r"^(?P<metric>EFFORT|SUBPROBLEMS|SUBSTITUTIONS)\s+"
    r"LIMIT\s+(?P<limit>\d+)\s+ACTUAL\s+(?P<actual>\d+)"
)
MANIFEST_RE = re.compile(r"^(?P<hash>[0-9A-Fa-f]{64})\s+\*?(?P<path>.+)$")
DOT_ARTIFACT_RE = re.compile(r"lt-proof-(?P<compact_theorem>\d+)\.dot$")


@dataclass
class TheoremAttempt:
    run_id: str
    source_log: str
    theorem: str
    expression: str
    attempt_line: int
    status: str = "UNKNOWN"
    status_line: int | None = None
    effort_limit: int | None = None
    effort_actual: int | None = None
    subproblems_limit: int | None = None
    subproblems_actual: int | None = None
    substitutions_limit: int | None = None
    substitutions_actual: int | None = None
    qed_line: int | None = None
    remember_line: int | None = None
    remembered_theorem: str = ""
    remembered_expression: str = ""
    associated_dot_artifacts: str = ""
    notable: bool = False


@dataclass
class LineFinding:
    source: str
    line: int
    category: str
    text: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_lt_line(raw_line: str) -> str:
    return COLON_PREFIX_RE.sub("", raw_line.rstrip("\n")).rstrip()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def relative_to(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def extract_heading_output(text: str, heading: str) -> str:
    lines = text.splitlines()
    heading_line = f"## {heading}"
    try:
        start = lines.index(heading_line) + 1
    except ValueError:
        return ""

    block: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        block.append(line)

    # The capture script records "Working directory:" and "Command:" lines before
    # the command output. The output starts after the blank line following Command.
    command_index = -1
    for index, line in enumerate(block):
        if line.startswith("Command: "):
            command_index = index
            break
    if command_index == -1:
        return "\n".join(block).strip()

    output = block[command_index + 1 :]
    while output and not output[0].strip():
        output.pop(0)
    return "\n".join(output).strip()


def parse_top_level_metadata(metadata_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for raw_line in metadata_text.splitlines():
        if raw_line.startswith("## "):
            break
        if ":" not in raw_line or raw_line.startswith("## "):
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {
            "Run ID",
            "Companion repository",
            "IPL-V specimen",
            "Run directory",
            "Start date",
            "Command",
        }:
            metadata[key] = value
    return metadata


def parse_post_run_metadata(post_run_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for raw_line in post_run_text.splitlines():
        if ":" not in raw_line or raw_line.startswith("## "):
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {"End date", "Exit status"}:
            metadata[key] = value
    return metadata


def theorem_to_compact(theorem: str) -> str:
    return theorem.replace(".", "")


def collect_dot_artifacts(run_dir: Path) -> dict[str, list[str]]:
    artifacts: dict[str, list[str]] = {}
    for path in sorted((run_dir / "generated_artifacts").glob("**/lt-proof-*.dot")):
        match = DOT_ARTIFACT_RE.search(path.name)
        if not match:
            continue
        compact = match.group("compact_theorem")
        artifacts.setdefault(compact, []).append(relative_to(path, run_dir))
    return artifacts


def parse_attempts_from_log(log_path: Path, run_dir: Path, run_id: str) -> list[TheoremAttempt]:
    attempts: list[TheoremAttempt] = []
    current: TheoremAttempt | None = None
    expect_theorem = False
    expect_remembered_theorem = False
    source_log = relative_to(log_path, run_dir)

    with log_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = clean_lt_line(raw_line).strip()

            if line == "TO PROVE":
                if current is not None:
                    attempts.append(current)
                current = None
                expect_theorem = True
                expect_remembered_theorem = False
                continue

            if expect_theorem:
                if not line:
                    continue
                match = THEOREM_RE.match(line)
                if match:
                    current = TheoremAttempt(
                        run_id=run_id,
                        source_log=source_log,
                        theorem=match.group("theorem"),
                        expression=match.group("expression").strip(),
                        attempt_line=line_number,
                    )
                expect_theorem = False
                continue

            if current is None:
                continue

            if "NO PROOF FOUND" in line:
                current.status = "NO PROOF FOUND"
                current.status_line = line_number
                continue

            if "PROOF FOUND" in line:
                current.status = "PROOF FOUND"
                current.status_line = line_number
                continue

            metric_match = METRIC_RE.match(line)
            if metric_match:
                metric = metric_match.group("metric")
                limit = int(metric_match.group("limit"))
                actual = int(metric_match.group("actual"))
                if metric == "EFFORT":
                    current.effort_limit = limit
                    current.effort_actual = actual
                elif metric == "SUBPROBLEMS":
                    current.subproblems_limit = limit
                    current.subproblems_actual = actual
                elif metric == "SUBSTITUTIONS":
                    current.substitutions_limit = limit
                    current.substitutions_actual = actual
                continue

            if "Q.E.D." in line:
                current.qed_line = line_number
                continue

            if "REMEMBER PROVED THEOREM" in line:
                current.remember_line = line_number
                expect_remembered_theorem = True
                continue

            if expect_remembered_theorem:
                if not line:
                    continue
                remembered_match = THEOREM_RE.match(line)
                if remembered_match:
                    current.remembered_theorem = remembered_match.group("theorem")
                    current.remembered_expression = remembered_match.group("expression").strip()
                expect_remembered_theorem = False

    if current is not None:
        attempts.append(current)

    return attempts


def parse_attempts(run_dir: Path, run_id: str) -> tuple[list[TheoremAttempt], list[str]]:
    logs = sorted((run_dir / "generated_artifacts" / "ltresults").glob("*.log"))
    attempts: list[TheoremAttempt] = []
    for log_path in logs:
        attempts.extend(parse_attempts_from_log(log_path, run_dir, run_id))

    dot_artifacts = collect_dot_artifacts(run_dir)
    for attempt in attempts:
        attempt.notable = attempt.theorem in NOTABLE_THEOREMS
        attempt.associated_dot_artifacts = "; ".join(
            dot_artifacts.get(theorem_to_compact(attempt.theorem), [])
        )

    return attempts, [relative_to(path, run_dir) for path in logs]


def categorize_log_line(line: str) -> str:
    upper = line.upper()
    if "BAD EXPRESSION" in upper:
        return "bad expression"
    if "MISSING LOCAL SYMBOL" in upper:
        return "missing local symbol warning"
    if "PQ" in upper and ("AMBUGIOUS" in upper or "AMBIG" in upper):
        return "ambiguous PQ warning"
    if "WARNING" in upper:
        return "warning"
    return "notice"


def collect_log_findings(log_paths: Iterable[Path], run_dir: Path) -> list[LineFinding]:
    findings: list[LineFinding] = []
    for path in log_paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = clean_lt_line(raw_line).strip()
                upper = line.upper()
                if "WARNING" in upper or "BAD EXPRESSION" in upper:
                    findings.append(
                        LineFinding(
                            source=relative_to(path, run_dir),
                            line=line_number,
                            category=categorize_log_line(line),
                            text=line,
                        )
                    )
    return findings


def collect_stderr_findings(run_dir: Path) -> list[LineFinding]:
    path = run_dir / "stderr.txt"
    findings: list[LineFinding] = []
    if not path.exists():
        return findings

    patterns = (
        "WARNING",
        "STYLE-WARNING",
        "UNDEFINED VARIABLE",
        "UNDEFINED FUNCTION",
        "NOTE:",
        "COMPILATION UNIT FINISHED",
    )
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            upper = line.upper()
            if not line:
                continue
            if any(pattern in upper for pattern in patterns):
                category = "compiler warning"
                if "STYLE-WARNING" in upper:
                    category = "compiler style warning"
                elif "NOTE:" in upper:
                    category = "compiler note"
                elif "COMPILATION UNIT FINISHED" in upper:
                    category = "compiler summary"
                findings.append(
                    LineFinding(
                        source="stderr.txt",
                        line=line_number,
                        category=category,
                        text=line,
                    )
                )
    return findings


def verify_run_manifest(run_dir: Path) -> dict[str, object]:
    manifest_path = run_dir / "manifest.sha256"
    result: dict[str, object] = {
        "path": relative_to(manifest_path, run_dir),
        "exists": manifest_path.exists(),
        "entry_count": 0,
        "status": "missing",
        "missing": [],
        "mismatched": [],
        "malformed": [],
    }
    if not manifest_path.exists():
        return result

    missing: list[str] = []
    mismatched: list[str] = []
    malformed: list[str] = []
    entry_count = 0

    with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            match = MANIFEST_RE.match(line)
            if not match:
                malformed.append(f"line {line_number}: {line}")
                continue
            entry_count += 1
            expected_hash = match.group("hash").lower()
            rel_path = match.group("path").strip()
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            target = run_dir / rel_path
            if not target.exists():
                missing.append(rel_path)
                continue
            actual_hash = sha256_file(target)
            if actual_hash != expected_hash:
                mismatched.append(rel_path)

    status = "OK"
    if missing or mismatched or malformed:
        status = "FAILED"

    result.update(
        {
            "entry_count": entry_count,
            "status": status,
            "missing": missing,
            "mismatched": mismatched,
            "malformed": malformed,
        }
    )
    return result


def count_by_category(findings: Iterable[LineFinding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1
    return dict(sorted(counts.items()))


def read_exit_status(run_dir: Path) -> str:
    text = read_text(run_dir / "exit_status.txt").strip()
    return text if text else "unknown"


def status_counts(attempts: Iterable[TheoremAttempt]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for attempt in attempts:
        counts[attempt.status] = counts.get(attempt.status, 0) + 1
    return dict(sorted(counts.items()))


def notable_summary(attempts: Iterable[TheoremAttempt]) -> list[dict[str, object]]:
    attempts_by_theorem = {attempt.theorem: attempt for attempt in attempts}
    rows: list[dict[str, object]] = []
    for theorem in NOTABLE_THEOREMS:
        attempt = attempts_by_theorem.get(theorem)
        if attempt is None:
            rows.append(
                {
                    "theorem": theorem,
                    "status": "NOT OBSERVED",
                    "expression": "",
                    "effort_actual": None,
                    "subproblems_actual": None,
                    "substitutions_actual": None,
                    "source_log": "",
                    "attempt_line": None,
                    "associated_dot_artifacts": "",
                }
            )
        else:
            rows.append(
                {
                    "theorem": theorem,
                    "status": attempt.status,
                    "expression": attempt.expression,
                    "effort_actual": attempt.effort_actual,
                    "subproblems_actual": attempt.subproblems_actual,
                    "substitutions_actual": attempt.substitutions_actual,
                    "source_log": attempt.source_log,
                    "attempt_line": attempt.attempt_line,
                    "associated_dot_artifacts": attempt.associated_dot_artifacts,
                }
            )
    return rows


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def cell(value: object) -> str:
        if value is None:
            text = ""
        else:
            text = str(value)
        text = text.replace("|", "\\|").replace("\n", " ")
        return text

    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(output)


def write_csv(path: Path, attempts: list[TheoremAttempt]) -> None:
    fieldnames = list(asdict(attempts[0]).keys()) if attempts else list(TheoremAttempt.__annotations__)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for attempt in attempts:
            writer.writerow(asdict(attempt))


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(
    path: Path,
    *,
    run_id: str,
    run_dir: Path,
    metadata: dict[str, str],
    command_outputs: dict[str, str],
    post_run_metadata: dict[str, str],
    exit_status: str,
    log_paths: list[str],
    attempts: list[TheoremAttempt],
    log_findings: list[LineFinding],
    stderr_findings: list[LineFinding],
    manifest_result: dict[str, object],
    output_files: dict[str, str],
    created_at: str,
) -> None:
    counts = status_counts(attempts)
    notable_rows = notable_summary(attempts)
    log_counts = count_by_category(log_findings)
    stderr_counts = count_by_category(stderr_findings)

    theorem_rows = [
        [
            attempt.theorem,
            attempt.status,
            attempt.expression,
            attempt.effort_actual,
            attempt.subproblems_actual,
            attempt.substitutions_actual,
            attempt.source_log,
            attempt.attempt_line,
            attempt.associated_dot_artifacts,
        ]
        for attempt in attempts
    ]
    notable_table_rows = [
        [
            row["theorem"],
            row["status"],
            row["expression"],
            row["effort_actual"],
            row["subproblems_actual"],
            row["substitutions_actual"],
            row["source_log"],
            row["attempt_line"],
            row["associated_dot_artifacts"],
        ]
        for row in notable_rows
    ]

    finding_rows = [
        [finding.category, finding.source, finding.line, finding.text]
        for finding in (log_findings + stderr_findings)[:40]
    ]

    report = f"""# Logic Theorist Run Report: {run_id}

Generated: `{created_at}`

This report describes preserved local executable behavior from a companion run bundle. It is not a historical claim about the original Logic Theorist, the published literature, or any upstream repository.

## Source Evidence

- Run directory: `{relative_to(run_dir, repo_root())}`
- Recorded IPL-V specimen path: `{metadata.get("IPL-V specimen", "")}`
- Recorded command: `{metadata.get("Command", "")}`
- Start date: `{metadata.get("Start date", "")}`
- End date: `{post_run_metadata.get("End date", "")}`
- Exit status: `{exit_status}`
- Manifest status: `{manifest_result.get("status")}` over `{manifest_result.get("entry_count")}` entries
- Primary Logic Theorist log files: `{", ".join(log_paths) if log_paths else "none observed"}`

## Version and Environment

- IPL-V commit: `{command_outputs.get("git rev-parse HEAD", "")}`
- IPL-V branch: `{command_outputs.get("git branch --show-current", "")}`
- IPL-V latest commit line: `{command_outputs.get("git log -1 --oneline", "")}`
- SBCL version: `{command_outputs.get("sbcl --version", "")}`
- System: `{command_outputs.get("uname -a", "")}`

## Summary

- Theorem attempts parsed: `{len(attempts)}`
- Proofs found: `{counts.get("PROOF FOUND", 0)}`
- No-proof outcomes: `{counts.get("NO PROOF FOUND", 0)}`
- Unknown outcomes: `{counts.get("UNKNOWN", 0)}`
- Logic Theorist log findings: `{sum(log_counts.values())}`
- Compiler/stderr findings: `{sum(stderr_counts.values())}`

Status counts:

```json
{json.dumps(counts, indent=2, sort_keys=True)}
```

## Notable Theorems

{markdown_table(["Theorem", "Status", "Expression", "Effort", "Subproblems", "Substitutions", "Source", "Line", "Associated dot artifacts"], notable_table_rows)}

## Theorem Outcomes

{markdown_table(["Theorem", "Status", "Expression", "Effort", "Subproblems", "Substitutions", "Source", "Line", "Associated dot artifacts"], theorem_rows)}

## Warnings and Anomalous Lines

Logic Theorist log finding counts:

```json
{json.dumps(log_counts, indent=2, sort_keys=True)}
```

Compiler/stderr finding counts:

```json
{json.dumps(stderr_counts, indent=2, sort_keys=True)}
```

Representative findings, limited to the first 40 lines found:

{markdown_table(["Category", "Source", "Line", "Text"], finding_rows) if finding_rows else "No warning or anomaly lines were identified by this first-version parser."}

## Analysis Outputs

- Markdown report: `{output_files["report"]}`
- Theorem CSV: `{output_files["csv"]}`
- JSON summary: `{output_files["json"]}`
- Analysis manifest: `{output_files["manifest"]}`

## Methodological Notes

The parser treats the preserved `generated_artifacts/ltresults/*.log` files as the primary source for theorem-attempt parsing. `stdout.txt` is preserved as evidence, but it may duplicate the Logic Theorist log content and is not used as the primary theorem table source.

Associated `.dot` artifacts are listed by filename correspondence only. Their presence is not interpreted as an independent proof claim, especially where the parsed theorem status is `NO PROOF FOUND`.

This first-version parser is intentionally conservative. It records local output structure, status markers, metric lines, warning lines, and notable theorem statuses without changing the IPL-V executable specimen.
"""
    path.write_text(report, encoding="utf-8")


def write_analysis_manifest(manifest_path: Path, files: Iterable[Path], base: Path) -> None:
    lines = []
    for path in sorted(files):
        lines.append(f"{sha256_file(path)}  {relative_to(path, base)}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def output_paths(root: Path, run_id: str) -> dict[str, Path]:
    run_report_dir = root / "reports" / run_id
    return {
        "report": run_report_dir / "run_report.md",
        "csv": run_report_dir / "theorem_summary.csv",
        "json": run_report_dir / "analysis_summary.json",
        "manifest": run_report_dir / "analysis_manifest.sha256",
    }


def ensure_no_overwrite(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        formatted = "\n".join(f"  - {path}" for path in existing)
        raise SystemExit(
            "Refusing to overwrite existing analysis files. "
            "Use --force to regenerate them.\n"
            f"{formatted}"
        )


def analyze(run_dir: Path, force: bool = False) -> dict[str, object]:
    root = repo_root()
    run_dir = run_dir.expanduser().resolve()
    if not run_dir.is_dir():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    metadata_text = read_text(run_dir / "metadata.txt")
    post_run_text = read_text(run_dir / "post_run_metadata.txt")
    metadata = parse_top_level_metadata(metadata_text)
    post_run_metadata = parse_post_run_metadata(post_run_text)
    run_id = metadata.get("Run ID") or run_dir.name

    outputs = output_paths(root, run_id)
    ensure_no_overwrite(outputs.values(), force)
    for output in outputs.values():
        output.parent.mkdir(parents=True, exist_ok=True)

    command_outputs = {
        "pwd": extract_heading_output(metadata_text, "pwd"),
        "git rev-parse HEAD": extract_heading_output(metadata_text, "git rev-parse HEAD"),
        "git branch --show-current": extract_heading_output(
            metadata_text, "git branch --show-current"
        ),
        "git remote -v": extract_heading_output(metadata_text, "git remote -v"),
        "git status --short": extract_heading_output(metadata_text, "git status --short"),
        "git diff --stat": extract_heading_output(metadata_text, "git diff --stat"),
        "git log -1 --oneline": extract_heading_output(metadata_text, "git log -1 --oneline"),
        "sbcl --version": extract_heading_output(metadata_text, "sbcl --version"),
        "uname -a": extract_heading_output(metadata_text, "uname -a"),
        "date": extract_heading_output(metadata_text, "date"),
    }

    attempts, log_paths = parse_attempts(run_dir, run_id)
    log_file_paths = [run_dir / log_path for log_path in log_paths]
    log_findings = collect_log_findings(log_file_paths, run_dir)
    stderr_findings = collect_stderr_findings(run_dir)
    manifest_result = verify_run_manifest(run_dir)
    exit_status = read_exit_status(run_dir)
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    script_path = Path(__file__).resolve()

    output_rel = {name: relative_to(path, root) for name, path in outputs.items()}
    summary: dict[str, object] = {
        "run_id": run_id,
        "created_at": created_at,
        "run_directory": relative_to(run_dir, root),
        "metadata": metadata,
        "post_run_metadata": post_run_metadata,
        "command_outputs": command_outputs,
        "exit_status": exit_status,
        "manifest_verification": manifest_result,
        "source_logs": log_paths,
        "theorem_attempt_count": len(attempts),
        "status_counts": status_counts(attempts),
        "notable_theorems": notable_summary(attempts),
        "logic_theorist_log_finding_counts": count_by_category(log_findings),
        "compiler_stderr_finding_counts": count_by_category(stderr_findings),
        "logic_theorist_log_findings": [asdict(finding) for finding in log_findings],
        "compiler_stderr_findings": [asdict(finding) for finding in stderr_findings],
        "theorem_attempts": [asdict(attempt) for attempt in attempts],
        "analysis_script": relative_to(script_path, root),
        "analysis_script_sha256": sha256_file(script_path),
        "outputs": output_rel,
        "methodological_note": (
            "This analysis describes preserved local executable output only and "
            "does not assert historical conclusions about the original Logic Theorist."
        ),
    }

    write_csv(outputs["csv"], attempts)
    write_json(outputs["json"], summary)
    write_report(
        outputs["report"],
        run_id=run_id,
        run_dir=run_dir,
        metadata=metadata,
        command_outputs=command_outputs,
        post_run_metadata=post_run_metadata,
        exit_status=exit_status,
        log_paths=log_paths,
        attempts=attempts,
        log_findings=log_findings,
        stderr_findings=stderr_findings,
        manifest_result=manifest_result,
        output_files=output_rel,
        created_at=created_at,
    )
    write_analysis_manifest(
        outputs["manifest"],
        [outputs["report"], outputs["csv"], outputs["json"]],
        root,
    )

    return {
        "run_id": run_id,
        "outputs": output_rel,
        "theorem_attempt_count": len(attempts),
        "status_counts": status_counts(attempts),
        "manifest_status": manifest_result.get("status"),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a preserved Logic Theorist run directory and create "
            "companion report artifacts."
        )
    )
    parser.add_argument(
        "run_directory",
        help="Path to a preserved run directory, such as runs/20260512_010918.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated analysis outputs for this run.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = analyze(Path(args.run_directory), force=args.force)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
