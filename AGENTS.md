# AGENTS.md

## Project Identity

This project supports Logic Theorist / IPL-V software archaeology, reproducibility, and evidence work.

The project concerns the modern execution, verification, documentation, and interpretation of the IPL-V reanimation of the Logic Theorist. Treat this as a scholarly and technical research environment, not merely as a software sandbox.

Use a formal, professional, and academically careful tone. Prioritize factual accuracy, reproducibility, provenance, and clear distinction between evidence, interpretation, and speculation. Use American English.

## Repository Roles

The recommended local project layout is:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/                         executable specimen; fork of upstream IPL-V
  logic-theorist-companion/       companion repository for research apparatus
```

The IPL-V specimen should preserve direct provenance from:

```text
https://github.com/jeffshrager/IPL-V
```

The companion repository is for:

- Reproducibility workflows
- Audit reports
- Evidence manifests
- Parser scripts
- Run summaries
- Documentation
- Internal review notes
- Publication-support materials
- Methodological notes

Do not collapse the executable specimen and companion apparatus into one mixed repository unless explicitly requested.

## Provenance Principles

Always distinguish among:

1. Original upstream IPL-V source
2. The local executable specimen
3. Generated Logic Theorist run artifacts
4. Companion analysis, reports, scripts, and interpretation

Do not claim that a historical result has changed unless there is strong, externally reviewed evidence. Prefer conservative language such as:

- "The current local executable behavior appears to produce..."
- "The local artifacts show..."
- "The anomalous additional local success is..."
- "Further review is required."

Avoid unsupported claims such as:

- "The paper is wrong."
- "The historical result has changed."
- "The result is definitively improved."

## File Placement Policy

Do not place companion reports, parser outputs, CSV files, manifests, review notes, or scholarly notes inside the IPL-V specimen unless explicitly instructed.

Preferred companion repository structure:

```text
README.md
AGENTS.md
docs/
scripts/
runs/
reports/
manifests/
evidence/
review-notes/
baseline/
```

Use timestamped directories for runs and audits when appropriate:

```text
runs/YYYYMMDD_HHMMSS/
reports/YYYYMMDD_HHMMSS/
evidence/YYYYMMDD_HHMMSS/
```

The executable IPL-V repository may create native generated files during faithful operation, including:

```text
ltresults/*.log
ltresults/*.dotstar
*.fasl
proof-*.pdf
```

When preserving such outputs, copy them into the companion repository or an external evidence directory with metadata and SHA-256 manifests.

## Safety Rules

Do not delete, overwrite, move, or clean evidence unless explicitly requested.

Do not run:

```text
git clean
git reset --hard
rm -rf
```

unless explicit confirmation is given for the exact target and purpose.

Do not open GitHub issues, create pull requests, push commits, or publish artifacts without explicit confirmation.

This project does not publish pull requests, GitHub issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers as part of the normal workflow.

Do not modify tracked source files in the IPL-V specimen unless the task explicitly requires it.

Before any destructive operation, confirm:

- Exact path
- What will be deleted or changed
- Whether a manifest or evidence record already exists
- Whether the operation has been explicitly authorized

## Reproducibility Standards

For every significant run or audit, capture:

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

Use SHA-256 manifests for evidence bundles:

```sh
shasum -a 256
```

Preserve stdout, stderr, exit status, generated logs, generated dotstar files, parser outputs, and reports.

General `.log` files are ignored by default in the companion repository, except curated logs under `runs/` and `evidence/`. Every authorized Logic Theorist run should preserve curated run logs and generated artifacts by default in a timestamped companion run or evidence directory.

Use structured outputs where practical:

- Markdown for narrative reports
- CSV for tabular run summaries
- JSON only when useful for machine-readable structured data
- Plain text for raw metadata captures

## Logic Theorist Run Policy

Do not run Logic Theorist unless explicitly requested.

When running Logic Theorist, prefer commands equivalent to:

```sh
cd "$HOME/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V"

sbcl --dynamic-space-size 4096 \
  --eval '(load (compile-file "lt.lisp"))' \
  --eval '(sb-ext:exit)'
```

After each authorized run, identify newly generated artifacts and copy curated logs and generated artifacts into a timestamped evidence directory in the companion repository or external evidence root by default.

Do not overwrite prior run outputs.

Do not treat generated artifacts in IPL-V as automatically erroneous; they may be part of faithful software-archaeological operation.

## Analysis Standards

When analyzing Logic Theorist logs, distinguish:

- Theorem attempts
- `PROOF FOUND.`
- `NO PROOF FOUND`
- Effort counts
- Subproblem counts
- Substitution counts
- Proof certificates
- Remembered-theorem lines
- Compile warnings
- Missing local-symbol warnings
- Ambiguous PQ warnings
- `BAD EXPRESSION` lines

When comparing runs, report:

- Run ID
- Source path
- Commit hash
- Total theorem attempts
- Proof count
- Failure count
- Failed theorem list
- Status of notable theorems, especially 2.21, 2.24, 4.13, 4.24, and 4.25

## Documentation Standards

Write documentation for a scholarly technical audience. Explain assumptions clearly and avoid casual language.

Prefer precise statements over broad claims. When evidence is local, say so explicitly.

Do not conflate:

- Historical Logic Theorist behavior
- Published claims
- Current local executable behavior
- Results from one particular run
- Results from a clean verification run

## Git and GitHub Policy

The recommended GitHub model is two repositories:

```text
<project-owner>/IPL-V
  fork of jeffshrager/IPL-V

<project-owner>/logic-theorist-companion
  companion repository
```

The IPL-V fork should preserve upstream provenance.

The companion repository should preserve research apparatus and evidence.

Do not push to GitHub without explicit confirmation.

Do not create remote repositories, forks, issues, pull requests, releases, or tags without explicit confirmation.

Do not create pull requests, issues, comments, or other communications directed to `jeffshrager/IPL-V` or its maintainers.

When preparing commits, keep them small and purposeful. Separate:

- Workflow scaffolding
- Parser scripts
- Reports
- Evidence manifests
- Documentation updates

## Preferred Tone

Use a formal, professional, and academic tone.

Be clear, conservative, and evidence-oriented.

When uncertain, state the uncertainty directly.

When proposing an action, explain why it supports provenance, reproducibility, or scholarly clarity.
