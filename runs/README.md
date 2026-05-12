# Runs

This directory is reserved for organized Logic Theorist run records.

Every authorized Logic Theorist run should preserve curated logs and generated artifacts by default. Use timestamped subdirectories when preserving run evidence:

```text
runs/YYYYMMDD_HHMMSS/
```

Each run record should identify the source commit, command, environment, stdout, stderr, exit status, generated artifacts, parser outputs, and related manifests.

Recommended structure:

```text
runs/YYYYMMDD_HHMMSS/
  metadata.txt
  stdout.txt
  stderr.txt
  exit_status.txt
  generated_artifacts/
  manifest.sha256
  summary.md
```

General `.log` files are ignored elsewhere by default, but curated `.log` files under `runs/` may be versioned as part of an organized run bundle.
