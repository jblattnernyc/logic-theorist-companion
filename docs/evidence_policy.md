# Evidence Policy

## Scope

Evidence for this project includes baseline metadata, command transcripts, generated Logic Theorist artifacts, parser outputs, reports, manifests, and internal review notes.

## Native Generated Files

Faithful Logic Theorist execution may create native generated files under the `IPL-V/` executable specimen, including:

```text
ltresults/*.log
ltresults/*.dotstar
*.fasl
proof-*.pdf
```

These files should not be treated as automatically erroneous. Their interpretation depends on the run context, command, commit, and environment.

## Run Log Policy

General `.log` files are ignored by default to avoid accidental versioning of incidental output. Curated run logs may be preserved under `runs/` or `evidence/` when they are part of an organized evidence bundle with metadata and SHA-256 manifests.

Every authorized Logic Theorist run should preserve curated run logs and generated artifacts by default. Native files created under `IPL-V/` should remain available in their original generated locations, while organized evidence copies should be stored in a timestamped companion run or evidence directory.

## Companion Evidence

Organized evidence copies, summaries, parser outputs, manifests, and review notes belong in this companion repository or in explicitly documented external evidence storage.

Use timestamped directories for run and audit evidence:

```text
runs/YYYYMMDD_HHMMSS/
reports/YYYYMMDD_HHMMSS/
evidence/YYYYMMDD_HHMMSS/
```

An organized Logic Theorist run should normally preserve:

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

The companion script `scripts/run_logic_theorist_capture.sh` implements this default run-bundle structure.

## Manifests

Use SHA-256 manifests for evidence bundles:

```sh
shasum -a 256
```

Manifests should identify the files they cover and should be preserved with the corresponding evidence bundle.

## Safety

Do not delete, overwrite, move, or clean evidence unless the exact target and purpose have been explicitly authorized. Do not use destructive Git commands on evidence or source repositories without explicit confirmation.
