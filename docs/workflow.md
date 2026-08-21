# Workflow

## Repository Layout

Use two separate repositories under the umbrella workspace:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/                         pinned executable specimen
  logic-theorist-companion/       public research project and apparatus
```

Do not make the umbrella directory itself a Git repository. Do not use a Git submodule unless the project explicitly changes that decision.

The original upstream provenance source is `https://github.com/jeffshrager/IPL-V`. The local specimen is pinned at commit `e35a705d57e99fe91d76d76b224b8af30f2fd632`, and existing preserved runs were generated from this commit. Reproducers must use the exact documented commit rather than current upstream `master`.

The local specimen uses this fetch-only remote configuration:

```text
origin  https://github.com/jeffshrager/IPL-V.git (fetch)
origin  DISABLED (push)
```

The public research project is `https://github.com/jblattnernyc/logic-theorist-companion`. The former public fork `https://github.com/jblattnernyc/IPL-V` was part of the historical project configuration and is being retired; historical evidence describing it remains unchanged.

## Baseline Capture

Before running Logic Theorist or modifying the executable specimen, capture baseline metadata from the `IPL-V/` repository and store it under `baseline/` in this companion repository.

Recommended metadata commands include:

```sh
pwd
git rev-parse HEAD
git branch --show-current
git remote -v
git status --short
git diff --stat
git log -1 --oneline
sbcl --version
uname -a
date
```

Do not save companion baseline records inside the IPL-V specimen unless explicitly requested.

## Run Procedure

Logic Theorist should not be run until repository layout, baseline metadata, and evidence policy are in place.

When an organized Logic Theorist run is authorized, curated preservation is the default. Preserve stdout, stderr, exit status, generated logs, generated dotstar files, parser outputs, metadata, and SHA-256 manifests in a timestamped companion run directory.

The recommended run bundle structure is:

```text
runs/YYYYMMDD_HHMMSS/
  metadata.txt
  stdout.txt
  stderr.txt
  exit_status.txt
  generated_artifacts/
  generated_artifacts_listing.txt
  post_run_metadata.txt
  manifest.sha256
  summary.md
```

Native generated artifacts may remain in `IPL-V/ltresults/` or other IPL-V-generated paths. The companion run directory should contain organized evidence copies with sufficient metadata to connect them to the source commit, command, environment, and timestamp.

The companion script `scripts/run_logic_theorist_capture.sh` implements this capture workflow. It should be used for organized Logic Theorist runs unless a run has a documented reason to use a different capture method.

After the companion run bundle has been committed, pushed, and manifest-verified, return the IPL-V specimen to a clean working tree by removing only the exact native generated files from that run. This keeps the executable specimen clean between runs while preserving the permanent evidence record in the companion repository.

## Run Analysis

After a run bundle is preserved, analyze the preserved companion copy rather than rerunning Logic Theorist immediately.

The companion script `scripts/analyze_run.py` analyzes a single run directory:

```sh
python3 scripts/analyze_run.py runs/YYYYMMDD_HHMMSS
```

It writes derived analysis outputs under a per-run directory in `reports/`:

```text
reports/YYYYMMDD_HHMMSS/
  run_report.md
  theorem_summary.csv
  analysis_summary.json
  analysis_manifest.sha256
```

The report and structured summaries are derivative companion records. They do not replace the raw run bundle, stdout, stderr, generated artifacts, or run manifest.

## Run Comparison

After two or more run analyses exist, compare the derived records rather than manually inspecting separate reports.

The companion script `scripts/compare_runs.py` compares run IDs:

```sh
python3 scripts/compare_runs.py YYYYMMDD_HHMMSS YYYYMMDD_HHMMSS
```

It writes comparison outputs under `reports/comparisons/`:

```text
reports/comparisons/RUN_ID__RUN_ID/
  comparison_report.md
  comparison_summary.csv
  comparison_summary.json
  comparison_manifest.sha256
```

Comparison records should verify the raw run manifests and analysis manifests for every compared run. They should report matching or differing local run behavior without making historical claims beyond the preserved local evidence.

## Upstream Contact Policy

This project does not publish pull requests, GitHub issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers as part of the normal workflow.

Internal notes may be kept in `review-notes/`, but they are not publication requests or planned upstream communications.

The local IPL-V specimen uses `origin` for fetch access to `https://github.com/jeffshrager/IPL-V.git`, with the `origin` push URL set to `DISABLED` to prevent accidental local pushes to the original repository.

## Publication Preparation

Publication-support materials should use conservative language and cite specific local artifacts, commands, commits, and manifests. Reports should distinguish evidence from interpretation.
