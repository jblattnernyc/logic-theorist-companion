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
