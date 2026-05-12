# Scripts

This directory is reserved for parser, audit, manifest, and reproducibility scripts.

Scripts should be documented with their expected inputs, outputs, command syntax, and assumptions. Scripts that analyze Logic Theorist logs should distinguish theorem attempts, proof findings, failed theorem attempts, warnings, proof certificates, and parser limitations.

## Run Capture

`run_logic_theorist_capture.sh` creates a timestamped run bundle for an authorized Logic Theorist run.

Example:

```sh
scripts/run_logic_theorist_capture.sh
```

Useful validation before a run:

```sh
scripts/run_logic_theorist_capture.sh --dry-run
```

The script preserves:

- `metadata.txt`
- `stdout.txt`
- `stderr.txt`
- `exit_status.txt`
- `generated_artifacts/`
- `generated_artifacts_listing.txt`
- `post_run_metadata.txt`
- `manifest.sha256`
- `summary.md`

The script copies generated artifacts into the companion run directory. It does not delete, move, clean, or modify IPL-V source files.

## Run Analysis

`analyze_run.py` analyzes one preserved run bundle and writes companion analysis artifacts.

Example:

```sh
python3 scripts/analyze_run.py runs/20260512_010918
```

The script reads the existing run directory and writes:

- `reports/YYYYMMDD_HHMMSS/run_report.md`
- `reports/YYYYMMDD_HHMMSS/theorem_summary.csv`
- `reports/YYYYMMDD_HHMMSS/analysis_summary.json`
- `reports/YYYYMMDD_HHMMSS/analysis_manifest.sha256`

By default, the script refuses to overwrite existing analysis outputs. Use `--force` only when intentionally regenerating those derived analysis files:

```sh
python3 scripts/analyze_run.py runs/20260512_010918 --force
```

The parser treats preserved `generated_artifacts/ltresults/*.log` files as the primary source for theorem-attempt parsing. It records theorem attempts, proof and no-proof outcomes, effort counts, subproblem counts, substitution counts, notable theorem statuses, warning lines, compiler-warning summaries, and associated `.dot` artifacts.

The script does not run Logic Theorist, modify the IPL-V executable specimen, contact GitHub, open issues, create pull requests, or delete evidence.

## Run Comparison

`compare_runs.py` compares two or more existing run-analysis directories.

Example:

```sh
python3 scripts/compare_runs.py 20260512_010918 20260512_141829
```

The script reads:

- `reports/RUN_ID/theorem_summary.csv`
- `reports/RUN_ID/analysis_summary.json`
- `reports/RUN_ID/analysis_manifest.sha256`
- `runs/RUN_ID/manifest.sha256`

It writes:

- `reports/comparisons/RUN_ID__RUN_ID/comparison_report.md`
- `reports/comparisons/RUN_ID__RUN_ID/comparison_summary.csv`
- `reports/comparisons/RUN_ID__RUN_ID/comparison_summary.json`
- `reports/comparisons/RUN_ID__RUN_ID/comparison_manifest.sha256`

The comparison checks theorem identifiers, expressions, proof/no-proof status, effort counts, subproblem counts, substitution counts, remembered-theorem fields, notable-theorem flags, selected environment metadata, raw run manifests, and analysis manifests.

The script does not run Logic Theorist, modify the IPL-V executable specimen, contact GitHub, open issues, create pull requests, or delete evidence.
