# Changelog

All notable changes to the Logic Theorist companion repository will be documented in this file.

This changelog records changes to the companion research apparatus. It does not record changes to the IPL-V executable specimen except when those changes affect companion metadata, evidence policy, or reproducibility workflow.

## Unreleased

### Added

- Added `scripts/run_logic_theorist_capture.sh` to create timestamped Logic Theorist run bundles with metadata, stdout, stderr, exit status, copied generated artifacts, artifact listings, SHA-256 manifests, post-run metadata, and summaries.
- Added README attribution noting that the companion repository is maintained by John Blattner as part of AI Universe Labs research work.
- Added the first captured Logic Theorist run bundle under `runs/20260512_010918/`, including a recovery note documenting completion of summary and manifest files after a capture-script summary-generation failure.
- Added a standing policy to return the IPL-V specimen to a clean working tree after companion evidence is committed, pushed, and manifest-verified, using only exact native generated file cleanup.
- Added `scripts/analyze_run.py` to parse preserved run bundles and generate formal Markdown, CSV, JSON, and SHA-256 analysis outputs.
- Added first derived analysis outputs for `runs/20260512_010918/`:
  - `reports/20260512_010918/run_report.md`
  - `reports/20260512_010918/theorem_summary.csv`
  - `reports/20260512_010918/analysis_summary.json`
  - `reports/20260512_010918/analysis_manifest.sha256`
- Added a per-run analysis-output directory policy for `reports/YYYYMMDD_HHMMSS/`.
- Added the second captured Logic Theorist confirmation run bundle under `runs/20260512_141829/`, including a recovery note documenting completion of the copied FASL artifact set after a timestamp-boundary capture omission.
- Added derived analysis outputs for `runs/20260512_141829/`:
  - `reports/20260512_141829/run_report.md`
  - `reports/20260512_141829/theorem_summary.csv`
  - `reports/20260512_141829/analysis_summary.json`
  - `reports/20260512_141829/analysis_manifest.sha256`
- Added `scripts/compare_runs.py` to compare derived analysis records across preserved Logic Theorist runs.
- Added the first cross-run comparison for `20260512_010918` and `20260512_141829`:
  - `reports/comparisons/20260512_010918__20260512_141829/comparison_report.md`
  - `reports/comparisons/20260512_010918__20260512_141829/comparison_summary.csv`
  - `reports/comparisons/20260512_010918__20260512_141829/comparison_summary.json`
  - `reports/comparisons/20260512_010918__20260512_141829/comparison_manifest.sha256`

### Fixed

- Corrected `scripts/run_logic_theorist_capture.sh` summary generation so Bash `printf` does not treat Markdown bullet lines beginning with `-` as options.
- Corrected `scripts/run_logic_theorist_capture.sh` root-artifact timestamp handling so same-second generated root artifacts, such as `lt.fasl`, are preserved when their filesystem timestamp matches the run marker timestamp.

- Initialized the local `logic-theorist-companion` repository as a separate Git repository under the `LOGIC THEORIST` umbrella workspace.
- Added companion repository documentation describing the two-repository model, provenance expectations, and separation between executable source and scholarly/reproducibility apparatus.
- Added standing project instruction files copied from the umbrella workspace:
  - `AGENTS.md`
  - `PLANS.md`
- Added documentation files:
  - `docs/provenance.md`
  - `docs/workflow.md`
  - `docs/evidence_policy.md`
- Added directory scaffolding and README files for future research materials:
  - `scripts/`
  - `runs/`
  - `reports/`
  - `manifests/`
  - `evidence/`
  - `review-notes/`
  - `baseline/`
- Added `.gitkeep` placeholders where needed to preserve empty evidence and workflow directories in Git.
- Added a companion `.gitignore` covering local system files, Python cache files, virtual environments, temporary files, incidental logs, and incidental Common Lisp compiled artifacts while preserving Markdown, CSV, JSON, manifest files, and curated run artifacts under `runs/` and `evidence/` by default.
- Added initial baseline notes documenting the pre-scaffold workspace state, GitHub CLI availability, authenticated GitHub account, SBCL version, operating system, date, and pending IPL-V baseline status.
- Created the public GitHub fork `jblattnernyc/IPL-V` from `jeffshrager/IPL-V`.
- Created the public empty GitHub repository `jblattnernyc/logic-theorist-companion`.
- Cloned the IPL-V executable specimen locally into `IPL-V/`.
- Configured local IPL-V remotes:

  ```text
  origin    https://github.com/jblattnernyc/IPL-V.git
  upstream  https://github.com/jeffshrager/IPL-V.git
  ```

- Configured the local companion repository `origin` remote:

  ```text
  https://github.com/jblattnernyc/logic-theorist-companion.git
  ```

- Captured IPL-V baseline metadata under `baseline/` before any Logic Theorist run.
- Added `LICENSE.md` using the MIT License for original companion repository materials.
- Added `review-notes/` to support internal review observations under the no-upstream-contact workflow.
- Set the local IPL-V `upstream` push URL to `DISABLED` while preserving the upstream fetch URL for provenance and comparison.

### Documented

- The original upstream IPL-V repository:

  ```text
  https://github.com/jeffshrager/IPL-V
  ```

- The intended local executable specimen path:

  ```text
  ~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V
  ```

- The intended local companion repository path:

  ```text
  ~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion
  ```

- The policy that native Logic Theorist generated files may be created under `IPL-V/` during faithful execution, while organized evidence copies, reports, parser outputs, manifests, and review notes belong in the companion repository or explicitly documented external evidence storage.
- The policy that every authorized Logic Theorist run should preserve curated run logs and generated artifacts by default in a timestamped companion run or evidence directory.
- The license scope for the companion repository, including the distinction between original companion materials and upstream or historical source materials.
- The no-upstream-contact policy stating that this project does not publish pull requests, GitHub issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers as part of the normal workflow.

### Published

- Committed and pushed the initial companion scaffold to `jblattnernyc/logic-theorist-companion` on branch `main`.

### Pending

- Review parser limitations and decide whether to improve theorem-detail extraction.
- Decide whether to perform a second confirmation run after reviewing the first run report.

### Not Performed

- No additional Logic Theorist run was performed while creating the analysis script.
- No IPL-V source files were created, modified, copied into the companion repository, or deleted during this analysis-script update.
- No GitHub issue, pull request, release, or tag was created.
- No communication was sent to the original IPL-V repository or its maintainers.
