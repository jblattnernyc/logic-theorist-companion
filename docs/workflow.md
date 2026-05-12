# Workflow

## Repository Layout

Use two separate repositories under the umbrella workspace:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/
  logic-theorist-companion/
```

Do not make the umbrella directory itself a Git repository. Do not use a Git submodule unless the project explicitly changes that decision.

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

## Upstream Contact Policy

This project does not publish pull requests, GitHub issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers as part of the normal workflow.

Internal notes may be kept in `review-notes/`, but they are not publication requests or planned upstream communications.

The local IPL-V specimen may keep `upstream` configured for fetch access to `https://github.com/jeffshrager/IPL-V.git`, while setting the `upstream` push URL to `DISABLED` to prevent accidental local pushes to the original repository.

## Publication Preparation

Publication-support materials should use conservative language and cite specific local artifacts, commands, commits, and manifests. Reports should distinguish evidence from interpretation.
