# Reports

This directory is reserved for audit reports, run summaries, theorem-status summaries, and publication-support reports.

Per-run derived analysis outputs should be organized by run ID:

```text
reports/YYYYMMDD_HHMMSS/
  run_report.md
  theorem_summary.csv
  analysis_summary.json
  analysis_manifest.sha256
```

Reports should state the evidence basis for each claim and should distinguish local executable behavior from historical claims and scholarly interpretation.

Cross-run comparisons should be organized under `reports/comparisons/`:

```text
reports/comparisons/RUN_ID__RUN_ID/
  comparison_report.md
  comparison_summary.csv
  comparison_summary.json
  comparison_manifest.sha256
```

Comparison reports should identify the compared run IDs, verify the relevant raw and analysis manifests, and state whether theorem-level records match.
