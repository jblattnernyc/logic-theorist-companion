# Logic Theorist Companion User Guide

## Purpose

This guide explains how to use the Logic Theorist companion repository as a reproducibility and evidence apparatus for the local IPL-V executable specimen.

The project uses two separate repositories:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/
  logic-theorist-companion/
```

`IPL-V/` is the executable specimen. It is a fork of the upstream IPL-V repository and should remain focused on source provenance and faithful execution.

`logic-theorist-companion/` is the research apparatus. It stores workflow documentation, baseline metadata, run bundles, generated analysis, comparisons, manifests, and review materials.

Do not collapse these repositories into a monorepo. Do not copy the full IPL-V source tree into the companion repository. Do not create pull requests, issues, comments, or other communications to the original IPL-V repository or maintainers as part of the normal workflow.

## Repository Roles

### IPL-V

The local IPL-V specimen is expected at:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V
```

Its normal remote model is:

```text
origin    https://github.com/jblattnernyc/IPL-V.git
upstream  https://github.com/jeffshrager/IPL-V.git
```

The `upstream` fetch URL preserves provenance. The `upstream` push URL may be set to `DISABLED` to reduce the risk of accidental upstream communication.

Do not modify tracked IPL-V source files unless the task explicitly requires it.

### Companion Repository

The companion repository is expected at:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion
```

It contains the operating workflow:

```text
baseline/       initial repository and environment metadata
docs/           project documentation
runs/           raw preserved Logic Theorist run bundles
reports/        per-run analysis and cross-run comparisons
scripts/        capture, analysis, and comparison scripts
manifests/      project-level or cross-run manifests when needed
evidence/       supplemental evidence bundles when needed
review-notes/   internal review notes
```

## Core Concepts

### Raw Evidence

Raw run evidence belongs under:

```text
runs/YYYYMMDD_HHMMSS/
```

A run bundle normally contains:

```text
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

These files document what the local IPL-V specimen produced during a specific execution.

### Derived Analysis

Per-run analysis belongs under:

```text
reports/YYYYMMDD_HHMMSS/
```

The standard outputs are:

```text
run_report.md
theorem_summary.csv
analysis_summary.json
analysis_manifest.sha256
```

These records are generated from preserved run evidence. They do not replace the raw run bundle.

### Cross-Run Comparison

Cross-run comparisons belong under:

```text
reports/comparisons/RUN_ID__RUN_ID/
```

The standard outputs are:

```text
comparison_report.md
comparison_summary.csv
comparison_summary.json
comparison_manifest.sha256
```

These records compare derived run analyses and help document repeatability across local runs.

## Before Running Logic Theorist

Before any run, confirm that both repositories are clean:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V"
git status --short --branch

cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion"
git status --short --branch
```

The desired state is no uncommitted changes in either repository.

Also confirm that SBCL is available:

```sh
sbcl --version
```

Do not run Logic Theorist until the run is intentional and the companion workflow is ready to preserve the evidence.

## Capturing a Run

From the companion repository:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion"
scripts/run_logic_theorist_capture.sh
```

The script runs Logic Theorist from the IPL-V specimen and creates a timestamped run bundle under `runs/`.

To preview paths and command without running Logic Theorist:

```sh
scripts/run_logic_theorist_capture.sh --dry-run
```

To specify a run ID:

```sh
scripts/run_logic_theorist_capture.sh --run-id YYYYMMDD_HHMMSS
```

To specify a non-default IPL-V path or SBCL executable:

```sh
scripts/run_logic_theorist_capture.sh --iplv-dir /path/to/IPL-V --sbcl /path/to/sbcl
```

The capture script copies generated artifacts into the companion repository. It does not clean or delete native generated files from `IPL-V`.

## Analyzing a Run

After a run bundle exists, analyze it from the companion repository:

```sh
python3 scripts/analyze_run.py runs/YYYYMMDD_HHMMSS
```

Example:

```sh
python3 scripts/analyze_run.py runs/20260512_141829
```

The analyzer writes:

```text
reports/YYYYMMDD_HHMMSS/run_report.md
reports/YYYYMMDD_HHMMSS/theorem_summary.csv
reports/YYYYMMDD_HHMMSS/analysis_summary.json
reports/YYYYMMDD_HHMMSS/analysis_manifest.sha256
```

By default, the analyzer refuses to overwrite existing analysis outputs. To intentionally regenerate outputs:

```sh
python3 scripts/analyze_run.py runs/YYYYMMDD_HHMMSS --force
```

Do not hand-edit generated reports, CSV files, or JSON summaries unless there is a clearly documented correction. Prefer regenerating them from the script.

## Comparing Runs

After two or more runs have been analyzed, compare them with:

```sh
python3 scripts/compare_runs.py RUN_ID RUN_ID
```

Example:

```sh
python3 scripts/compare_runs.py 20260512_010918 20260512_141829
```

The comparison script writes:

```text
reports/comparisons/RUN_ID__RUN_ID/comparison_report.md
reports/comparisons/RUN_ID__RUN_ID/comparison_summary.csv
reports/comparisons/RUN_ID__RUN_ID/comparison_summary.json
reports/comparisons/RUN_ID__RUN_ID/comparison_manifest.sha256
```

By default, the comparison script refuses to overwrite existing comparison outputs. To intentionally regenerate outputs:

```sh
python3 scripts/compare_runs.py RUN_ID RUN_ID --force
```

The comparison checks theorem-level results, selected metadata, raw run manifests, and analysis manifests.

## Verifying Manifests

Run manifests are relative to their run directories. Verify a raw run manifest from inside the run directory:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion/runs/YYYYMMDD_HHMMSS"
shasum -a 256 -c manifest.sha256
```

Analysis manifests and comparison manifests are relative to the companion repository root. Verify them from the companion repository:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion"
shasum -a 256 -c reports/YYYYMMDD_HHMMSS/analysis_manifest.sha256
shasum -a 256 -c reports/comparisons/RUN_ID__RUN_ID/comparison_manifest.sha256
```

A successful verification reports `OK` for every listed file.

## Cleaning Native Generated Files

Logic Theorist may create native generated files under `IPL-V`, including:

```text
*.fasl
ltresults/*.log
ltresults/*.dotstar
proof-*.pdf
```

These are normal generated artifacts, not errors.

Only clean native generated files after all of the following are true:

1. The run bundle has been created under `runs/`.
2. The run bundle manifest verifies.
3. The per-run analysis has been created under `reports/`.
4. The analysis manifest verifies.
5. The companion repository evidence has been committed and pushed.

Then remove only the exact files generated by that run. Do not use broad cleanup commands. Replace the timestamp placeholders in the example below with exact generated filenames from the run being cleaned.

Example:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V"
rm -f iplv.fasl lt.fasl ltresults/YYYYMMDDHHMM.log ltresults/YYYYMMDDHHMM.dotstar
git status --short --branch
```

Never use `git clean`, `git reset --hard`, or broad `rm -rf` commands for evidence cleanup unless the exact target and purpose have been explicitly authorized.

## Existing Checkpoint Records

At the time this guide was added, the companion repository contained:

```text
runs/20260512_010918/
runs/20260512_141829/
reports/20260512_010918/
reports/20260512_141829/
reports/comparisons/20260512_010918__20260512_141829/
```

The cross-run comparison reports that the two preserved local runs match across the selected theorem-level and metadata fields.

The strongest current reproducibility artifact is:

```text
reports/comparisons/20260512_010918__20260512_141829/comparison_report.md
```

## Recommended Routine

For a new run:

1. Confirm both repositories are clean.
2. Run `scripts/run_logic_theorist_capture.sh`.
3. Verify `runs/RUN_ID/manifest.sha256`.
4. Run `python3 scripts/analyze_run.py runs/RUN_ID`.
5. Verify `reports/RUN_ID/analysis_manifest.sha256`.
6. Commit and push the companion evidence when publication of the local evidence update has been reviewed and authorized.
7. Remove only exact native generated files from `IPL-V`.
8. Confirm both repositories are clean.
9. Compare runs when there is a useful reproducibility question.

## Language and Interpretation

Use cautious language when discussing results.

Appropriate wording:

- "The preserved local run shows..."
- "The generated analysis records..."
- "The two local runs match across the compared theorem-level fields..."

Avoid unsupported wording:

- "The historical result has changed."
- "The original paper is wrong."
- "The upstream implementation definitively proves..."

This project documents local executable behavior, preservation, and reproducibility evidence. Broader historical interpretation requires separate scholarly support.

## Actions That Require Explicit Confirmation

Do not perform these actions without explicit confirmation:

- Run Logic Theorist.
- Push commits.
- Create GitHub repositories, releases, tags, issues, or pull requests.
- Contact upstream maintainers.
- Modify tracked IPL-V source files.
- Delete, overwrite, move, or clean evidence files.
- Use destructive Git or filesystem commands.

## Troubleshooting

If a run bundle is missing an artifact that appears in `stdout.txt` or in the post-run IPL-V Git status, do not clean `IPL-V`. Inspect the bundle first, copy the missing artifact into the run bundle if appropriate, update the listing, update the summary or recovery note, and regenerate the run manifest without rerunning Logic Theorist.

If an analysis or comparison output already exists, the scripts will refuse to overwrite it unless `--force` is supplied. Use `--force` only when intentionally regenerating derived outputs.

If a manifest verification fails, do not edit evidence casually. Identify whether the failure is due to an incorrect working directory, a missing file, an actual content mismatch, or an outdated manifest. Record any correction in the relevant run summary, recovery note, changelog, or commit message.
