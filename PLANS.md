# PLANS.md

## Current Objective

Create a professional, provenance-preserving two-repository workflow for the Logic Theorist / IPL-V software archaeology, reproducibility, and evidence project.

The project should distinguish clearly between the executable IPL-V specimen and the companion scholarly apparatus used to document, verify, interpret, and publish results.

## Recommended Repository Model

Use two separate GitHub-oriented repositories under a local umbrella directory:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/                         fork of jeffshrager/IPL-V; executable specimen
  logic-theorist-companion/       companion repository; research apparatus
```

Do not make the parent `LOGIC THEORIST/` directory itself a Git repository if it contains both child repositories.

## Repository Purposes

### IPL-V

Purpose:

- Preserve the executable Logic Theorist / IPL-V specimen.
- Maintain direct provenance from `https://github.com/jeffshrager/IPL-V`.
- Support faithful local execution of the reconstructed program.
- Keep any source modifications minimal, explicit, and historically interpretable.

Expected remotes:

```text
origin    project fork of IPL-V
upstream  https://github.com/jeffshrager/IPL-V.git
```

### logic-theorist-companion

Purpose:

- Reproducibility workflow documentation
- Baseline metadata
- Evidence policies
- Parser and audit scripts
- Run summaries
- Reports
- SHA-256 manifests
- Internal review notes
- Publication-support materials
- Methodological notes

This repository should not contain a copied full IPL-V source tree unless the project model is explicitly reconsidered.

## Initial Phases

### Phase 1: Establish Local Repository Layout

Create or confirm:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion
```

The `IPL-V` directory should be cloned from the project fork of the original upstream repository, with `upstream` configured to `jeffshrager/IPL-V`.

The `logic-theorist-companion` directory should be initialized as a separate original repository.

### Phase 2: Capture Clean Baseline Metadata

Before running Logic Theorist or modifying any files, capture baseline metadata for the fresh `IPL-V` clone:

```text
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

Save these records under the companion repository, preferably in:

```text
baseline/
```

Do not save companion baseline records inside the IPL-V specimen unless explicitly required.

### Phase 3: Scaffold Companion Repository

Recommended companion structure:

```text
README.md
AGENTS.md
PLANS.md
docs/
  provenance.md
  workflow.md
  evidence_policy.md
scripts/
runs/
reports/
manifests/
evidence/
review-notes/
baseline/
```

The initial documentation should explain:

- The distinction between the executable specimen and companion repository.
- The original upstream IPL-V provenance.
- The role of the project fork.
- The policy for generated Logic Theorist outputs.

### Phase 4: Define Evidence and Run Policy

Future Logic Theorist runs may create native generated files under `IPL-V`, including:

```text
ltresults/*.log
ltresults/*.dotstar
*.fasl
proof-*.pdf
```

This is acceptable when it is part of faithful software-archaeological operation.

After each authorized run, organized evidence should be copied by default into a timestamped companion or external evidence directory with:

- Run metadata
- stdout/stderr capture
- Exit status
- Generated log and dotstar files
- Parser outputs
- SHA-256 manifests
- A concise run summary

General `.log` files should remain ignored by default, except curated logs preserved under `runs/` or `evidence/` as part of organized evidence bundles.

### Phase 5: First Organized Run

Do not run Logic Theorist until the repository layout, baseline metadata, and evidence policy are in place.

The first organized run should be treated as a test of the new workflow rather than as a publication claim.

### Phase 6: Publication Preparation

After the workflow is stable, prepare selected public-facing materials:

- Reproducibility guide
- Run comparison tables
- Evidence manifest
- Conservative theorem-status report
- Internal review notes
- Publication notes

Use conservative language. State only what the local artifacts and verification runs support.

## Non-Goals for Initial Setup

The initial setup should not:

- Run Logic Theorist.
- Modify IPL-V source files.
- Push to GitHub without explicit confirmation.
- Open GitHub issues automatically.
- Create pull requests, issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers.
- Delete evidence.
- Import the complete IPL-V source tree into the companion repository.
- Convert the project into a single monorepo without explicit reconsideration.

## Open Decisions

- Exact GitHub repository name for the companion repository.
- Whether the companion repository should be public from the beginning or private until reviewed.
- Whether selected raw logs and dotstar files should be versioned in Git, attached to releases, or kept in external evidence storage.
- Whether large PDFs and evidence bundles should use Git LFS, GitHub Releases, Zenodo, OSF, or local storage.
- Whether any IPL-V source changes are needed for local reproducibility, and how to document them without contacting upstream.
- Whether theorem-result discrepancies should be recorded as internal review notes, local reports, or publication-support materials.

## Guiding Principle

Preserve provenance first. Separate executable evidence from scholarly interpretation. Make every claim traceable to specific local artifacts, commands, commits, and manifests.
