#!/usr/bin/env python3
"""Compare derived analysis records for preserved Logic Theorist runs.

This companion script reads existing `reports/RUN_ID/` analysis outputs and
writes a cross-run comparison under `reports/comparisons/`. It does not run
Logic Theorist, modify the IPL-V executable specimen, contact GitHub, or delete
evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


NOTABLE_THEOREMS = ("2.21", "2.24", "4.13", "4.24", "4.25")
THEOREM_COMPARE_FIELDS = (
    "theorem",
    "expression",
    "status",
    "effort_limit",
    "effort_actual",
    "subproblems_limit",
    "subproblems_actual",
    "substitutions_limit",
    "substitutions_actual",
    "remembered_theorem",
    "remembered_expression",
    "notable",
)


@dataclass(frozen=True)
class ManifestCheck:
    path: str
    exists: bool
    status: str
    entry_count: int
    missing: list[str]
    mismatched: list[str]
    malformed: list[str]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_to(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_run_id(value: str) -> str:
    path = Path(value)
    if path.exists():
        return path.name
    return value


def comparison_id(run_ids: Iterable[str]) -> str:
    return "__".join(run_ids)


def verify_manifest(manifest_path: Path, base_dir: Path) -> ManifestCheck:
    if not manifest_path.exists():
        return ManifestCheck(
            path=relative_to(manifest_path, repo_root()),
            exists=False,
            status="missing",
            entry_count=0,
            missing=[],
            mismatched=[],
            malformed=[],
        )

    missing: list[str] = []
    mismatched: list[str] = []
    malformed: list[str] = []
    entry_count = 0

    with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2 or len(parts[0]) != 64:
                malformed.append(f"line {line_number}: {line}")
                continue
            expected_hash, rel_path = parts[0].lower(), parts[1].strip()
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            target = base_dir / rel_path
            entry_count += 1
            if not target.exists():
                missing.append(rel_path)
                continue
            actual_hash = sha256_file(target)
            if actual_hash != expected_hash:
                mismatched.append(rel_path)

    status = "OK"
    if missing or mismatched or malformed:
        status = "FAILED"

    return ManifestCheck(
        path=relative_to(manifest_path, repo_root()),
        exists=True,
        status=status,
        entry_count=entry_count,
        missing=missing,
        mismatched=mismatched,
        malformed=malformed,
    )


def run_record(root: Path, run_id: str) -> dict[str, object]:
    report_dir = root / "reports" / run_id
    run_dir = root / "runs" / run_id
    analysis_summary_path = report_dir / "analysis_summary.json"
    theorem_csv_path = report_dir / "theorem_summary.csv"

    if not report_dir.is_dir():
        raise SystemExit(f"analysis report directory does not exist: {report_dir}")
    if not run_dir.is_dir():
        raise SystemExit(f"raw run directory does not exist: {run_dir}")
    if not analysis_summary_path.exists():
        raise SystemExit(f"analysis summary not found: {analysis_summary_path}")
    if not theorem_csv_path.exists():
        raise SystemExit(f"theorem summary CSV not found: {theorem_csv_path}")

    analysis_summary = load_json(analysis_summary_path)
    theorem_rows = load_csv_rows(theorem_csv_path)
    raw_manifest = verify_manifest(run_dir / "manifest.sha256", run_dir)
    analysis_manifest = verify_manifest(report_dir / "analysis_manifest.sha256", root)

    return {
        "run_id": run_id,
        "run_dir": relative_to(run_dir, root),
        "report_dir": relative_to(report_dir, root),
        "analysis_summary": analysis_summary,
        "theorem_rows": theorem_rows,
        "raw_manifest": raw_manifest,
        "analysis_manifest": analysis_manifest,
    }


def theorem_keyed_rows(run: dict[str, object]) -> dict[str, dict[str, str]]:
    rows = run["theorem_rows"]
    assert isinstance(rows, list)
    return {str(row["theorem"]): row for row in rows}


def compare_theorems(runs: list[dict[str, object]]) -> list[dict[str, object]]:
    keyed = [theorem_keyed_rows(run) for run in runs]
    theorem_ids = sorted({theorem for rows in keyed for theorem in rows})
    rows: list[dict[str, object]] = []

    for theorem in theorem_ids:
        present = [theorem in rows for rows in keyed]
        baseline = keyed[0].get(theorem, {})
        field_matches: dict[str, bool] = {}
        differences: list[str] = []

        for field in THEOREM_COMPARE_FIELDS:
            values = [rows.get(theorem, {}).get(field, "") for rows in keyed]
            match = all(value == values[0] for value in values)
            field_matches[field] = match
            if not match:
                differences.append(field)

        all_match = all(present) and all(field_matches.values())
        status_values = {
            str(run["run_id"]): keyed[index].get(theorem, {}).get("status", "NOT OBSERVED")
            for index, run in enumerate(runs)
        }
        effort_values = {
            str(run["run_id"]): keyed[index].get(theorem, {}).get("effort_actual", "")
            for index, run in enumerate(runs)
        }

        rows.append(
            {
                "theorem": theorem,
                "notable": baseline.get("notable", ""),
                "expression": baseline.get("expression", ""),
                "all_fields_match": all_match,
                "status_values": status_values,
                "effort_actual_values": effort_values,
                "differences": differences,
            }
        )

    return rows


def compare_run_metadata(runs: list[dict[str, object]]) -> dict[str, object]:
    fields = {
        "iplv_commit": ("command_outputs", "git rev-parse HEAD"),
        "iplv_branch": ("command_outputs", "git branch --show-current"),
        "iplv_latest_commit_line": ("command_outputs", "git log -1 --oneline"),
        "sbcl_version": ("command_outputs", "sbcl --version"),
        "system": ("command_outputs", "uname -a"),
        "theorem_attempt_count": ("theorem_attempt_count",),
        "status_counts": ("status_counts",),
        "logic_theorist_log_finding_counts": ("logic_theorist_log_finding_counts",),
        "compiler_stderr_finding_counts": ("compiler_stderr_finding_counts",),
    }

    comparisons: dict[str, object] = {}
    for name, path in fields.items():
        values: dict[str, object] = {}
        for run in runs:
            summary = run["analysis_summary"]
            assert isinstance(summary, dict)
            value: object = summary
            for part in path:
                if not isinstance(value, dict):
                    value = None
                    break
                value = value.get(part)
            values[str(run["run_id"])] = value
        unique_values = {json.dumps(value, sort_keys=True) for value in values.values()}
        comparisons[name] = {
            "all_match": len(unique_values) == 1,
            "values": values,
        }
    return comparisons


def notable_summary(theorem_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_theorem = {str(row["theorem"]): row for row in theorem_rows}
    return [by_theorem[theorem] for theorem in NOTABLE_THEOREMS if theorem in by_theorem]


def status_counts(theorem_rows: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in theorem_rows:
        if not row.get("all_fields_match"):
            counts["theorem rows with differences"] = counts.get("theorem rows with differences", 0) + 1
        else:
            counts["theorem rows matching"] = counts.get("theorem rows matching", 0) + 1
    return counts


def output_paths(root: Path, comp_id: str) -> dict[str, Path]:
    output_dir = root / "reports" / "comparisons" / comp_id
    return {
        "report": output_dir / "comparison_report.md",
        "csv": output_dir / "comparison_summary.csv",
        "json": output_dir / "comparison_summary.json",
        "manifest": output_dir / "comparison_manifest.sha256",
    }


def ensure_no_overwrite(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        formatted = "\n".join(f"  - {path}" for path in existing)
        raise SystemExit(
            "Refusing to overwrite existing comparison files. "
            "Use --force to regenerate them.\n"
            f"{formatted}"
        )


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def cell(value: object) -> str:
        if value is None:
            text = ""
        elif isinstance(value, (dict, list)):
            text = json.dumps(value, sort_keys=True)
        else:
            text = str(value)
        return text.replace("|", "\\|").replace("\n", " ")

    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(output)


def write_csv(path: Path, runs: list[dict[str, object]], rows: list[dict[str, object]]) -> None:
    run_ids = [str(run["run_id"]) for run in runs]
    fieldnames = [
        "theorem",
        "notable",
        "expression",
        "all_fields_match",
        "differences",
    ]
    for run_id in run_ids:
        fieldnames.append(f"{run_id}_status")
        fieldnames.append(f"{run_id}_effort_actual")

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output = {
                "theorem": row["theorem"],
                "notable": row["notable"],
                "expression": row["expression"],
                "all_fields_match": row["all_fields_match"],
                "differences": ";".join(row["differences"]),
            }
            status_values = row["status_values"]
            effort_values = row["effort_actual_values"]
            assert isinstance(status_values, dict)
            assert isinstance(effort_values, dict)
            for run_id in run_ids:
                output[f"{run_id}_status"] = status_values.get(run_id, "")
                output[f"{run_id}_effort_actual"] = effort_values.get(run_id, "")
            writer.writerow(output)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_manifest(manifest_path: Path, files: Iterable[Path], base: Path) -> None:
    lines = []
    for path in sorted(files):
        lines.append(f"{sha256_file(path)}  {relative_to(path, base)}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    path: Path,
    *,
    comp_id: str,
    runs: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    metadata_comparison: dict[str, object],
    summary: dict[str, object],
    output_files: dict[str, str],
    created_at: str,
) -> None:
    run_ids = [str(run["run_id"]) for run in runs]
    raw_manifest_rows = [
        [
            run["run_id"],
            run["raw_manifest"].status,
            run["raw_manifest"].entry_count,
            run["raw_manifest"].path,
        ]
        for run in runs
    ]
    analysis_manifest_rows = [
        [
            run["run_id"],
            run["analysis_manifest"].status,
            run["analysis_manifest"].entry_count,
            run["analysis_manifest"].path,
        ]
        for run in runs
    ]
    metadata_rows = [
        [name, value["all_match"], value["values"]]
        for name, value in metadata_comparison.items()
    ]
    theorem_table_rows = [
        [
            row["theorem"],
            row["notable"],
            row["expression"],
            row["all_fields_match"],
            row["status_values"],
            row["effort_actual_values"],
            "; ".join(row["differences"]),
        ]
        for row in theorem_rows
    ]
    notable_rows = [
        [
            row["theorem"],
            row["all_fields_match"],
            row["status_values"],
            row["effort_actual_values"],
            "; ".join(row["differences"]),
        ]
        for row in notable_summary(theorem_rows)
    ]

    report = f"""# Logic Theorist Run Comparison: {comp_id}

Generated: `{created_at}`

This report compares derived analysis records for preserved local Logic Theorist runs. It describes local reproducibility evidence only. It is not a historical claim about the original Logic Theorist, the published literature, or any upstream repository.

## Compared Runs

{markdown_table(["Run ID", "Raw run directory", "Analysis directory"], [[run["run_id"], run["run_dir"], run["report_dir"]] for run in runs])}

## Summary

- Compared runs: `{", ".join(run_ids)}`
- Theorem rows compared: `{summary["theorem_count"]}`
- Theorem rows matching across compared fields: `{summary["matching_theorem_rows"]}`
- Theorem rows with differences: `{summary["differing_theorem_rows"]}`
- All theorem rows match: `{summary["all_theorem_rows_match"]}`
- All selected metadata fields match: `{summary["all_selected_metadata_match"]}`
- All raw run manifests verify: `{summary["all_raw_manifests_ok"]}`
- All analysis manifests verify: `{summary["all_analysis_manifests_ok"]}`

## Raw Run Manifests

{markdown_table(["Run ID", "Status", "Entries", "Manifest"], raw_manifest_rows)}

## Analysis Manifests

{markdown_table(["Run ID", "Status", "Entries", "Manifest"], analysis_manifest_rows)}

## Selected Metadata Comparison

{markdown_table(["Field", "All Match", "Values"], metadata_rows)}

## Notable Theorems

{markdown_table(["Theorem", "All Fields Match", "Statuses", "Effort Actuals", "Differences"], notable_rows)}

## Theorem Comparison

{markdown_table(["Theorem", "Notable", "Expression", "All Fields Match", "Statuses", "Effort Actuals", "Differences"], theorem_table_rows)}

## Outputs

- Markdown comparison report: `{output_files["report"]}`
- Comparison CSV: `{output_files["csv"]}`
- Comparison JSON: `{output_files["json"]}`
- Comparison manifest: `{output_files["manifest"]}`

## Methodological Notes

The comparison uses `reports/RUN_ID/theorem_summary.csv` and `reports/RUN_ID/analysis_summary.json` as derived inputs. It also verifies the raw run manifest under `runs/RUN_ID/manifest.sha256` and the analysis manifest under `reports/RUN_ID/analysis_manifest.sha256`.

The theorem comparison checks theorem identifiers, expressions, proof/no-proof status, effort counts, subproblem counts, substitution counts, remembered-theorem fields, and notable-theorem flags. It intentionally omits run-specific fields such as source log filename, line number, and associated artifact filename from the equality test because those may differ by run timestamp while preserving the same theorem-level behavior.
"""
    path.write_text(report, encoding="utf-8")


def compare_runs(run_ids: list[str], force: bool = False) -> dict[str, object]:
    root = repo_root()
    normalized_run_ids = [normalize_run_id(run_id) for run_id in run_ids]
    if len(normalized_run_ids) < 2:
        raise SystemExit("at least two run identifiers are required")
    if len(set(normalized_run_ids)) != len(normalized_run_ids):
        raise SystemExit("run identifiers must be unique")

    comp_id = comparison_id(normalized_run_ids)
    outputs = output_paths(root, comp_id)
    ensure_no_overwrite(outputs.values(), force)
    for output in outputs.values():
        output.parent.mkdir(parents=True, exist_ok=True)

    runs = [run_record(root, run_id) for run_id in normalized_run_ids]
    theorem_rows = compare_theorems(runs)
    metadata_comparison = compare_run_metadata(runs)
    matching_theorem_rows = sum(1 for row in theorem_rows if row["all_fields_match"])
    differing_theorem_rows = len(theorem_rows) - matching_theorem_rows
    all_raw_manifests_ok = all(run["raw_manifest"].status == "OK" for run in runs)
    all_analysis_manifests_ok = all(run["analysis_manifest"].status == "OK" for run in runs)
    all_selected_metadata_match = all(
        bool(value["all_match"]) for value in metadata_comparison.values()
    )
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    output_rel = {name: relative_to(path, root) for name, path in outputs.items()}
    summary: dict[str, object] = {
        "comparison_id": comp_id,
        "created_at": created_at,
        "run_ids": normalized_run_ids,
        "theorem_count": len(theorem_rows),
        "matching_theorem_rows": matching_theorem_rows,
        "differing_theorem_rows": differing_theorem_rows,
        "all_theorem_rows_match": differing_theorem_rows == 0,
        "all_selected_metadata_match": all_selected_metadata_match,
        "all_raw_manifests_ok": all_raw_manifests_ok,
        "all_analysis_manifests_ok": all_analysis_manifests_ok,
        "theorem_row_match_counts": status_counts(theorem_rows),
        "metadata_comparison": metadata_comparison,
        "raw_manifest_checks": {
            str(run["run_id"]): run["raw_manifest"].__dict__ for run in runs
        },
        "analysis_manifest_checks": {
            str(run["run_id"]): run["analysis_manifest"].__dict__ for run in runs
        },
        "notable_theorems": notable_summary(theorem_rows),
        "theorem_comparison": theorem_rows,
        "comparison_script": relative_to(Path(__file__).resolve(), root),
        "comparison_script_sha256": sha256_file(Path(__file__).resolve()),
        "outputs": output_rel,
        "methodological_note": (
            "This comparison describes derived local run-analysis records only "
            "and does not assert historical conclusions about the original Logic Theorist."
        ),
    }

    write_csv(outputs["csv"], runs, theorem_rows)
    write_json(outputs["json"], summary)
    write_report(
        outputs["report"],
        comp_id=comp_id,
        runs=runs,
        theorem_rows=theorem_rows,
        metadata_comparison=metadata_comparison,
        summary=summary,
        output_files=output_rel,
        created_at=created_at,
    )
    write_manifest(outputs["manifest"], [outputs["report"], outputs["csv"], outputs["json"]], root)

    return {
        "comparison_id": comp_id,
        "outputs": output_rel,
        "theorem_count": len(theorem_rows),
        "matching_theorem_rows": matching_theorem_rows,
        "differing_theorem_rows": differing_theorem_rows,
        "all_theorem_rows_match": differing_theorem_rows == 0,
        "all_selected_metadata_match": all_selected_metadata_match,
        "all_raw_manifests_ok": all_raw_manifests_ok,
        "all_analysis_manifests_ok": all_analysis_manifests_ok,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare derived analysis records for preserved Logic Theorist runs."
    )
    parser.add_argument(
        "runs",
        nargs="+",
        help="Run IDs, such as 20260512_010918 20260512_141829.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated comparison outputs.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = compare_runs(args.runs, force=args.force)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
