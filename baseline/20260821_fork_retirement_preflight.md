# IPL-V Public Fork Retirement Preflight

## Record Identity

- Date: 2026-08-21 11:08:51 EDT
- Workspace path: `/Users/john-blattner/Documents/PROGRAMMING/IPL/LOGIC THEORIST`
- Local IPL-V path: `/Users/john-blattner/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V`
- Companion path: `/Users/john-blattner/Documents/PROGRAMMING/IPL/LOGIC THEORIST/logic-theorist-companion`

This record captures the reversible preparation state before retiring the public GitHub fork `jblattnernyc/IPL-V`.

## Local IPL-V Preflight State

- HEAD: `e35a705d57e99fe91d76d76b224b8af30f2fd632`
- Branch: `master`
- Most recent commit: `e35a705 no message`

`git status --short`:

```text
?? .DS_Store
```

Current remotes before migration:

```text
origin    https://github.com/jblattnernyc/IPL-V.git (fetch)
origin    https://github.com/jblattnernyc/IPL-V.git (push)
upstream  https://github.com/jeffshrager/IPL-V.git (fetch)
upstream  DISABLED (push)
```

The former `upstream` configuration is preserved here because the migration will make the original upstream repository the sole `origin` and remove the redundant `upstream` remote.

## Companion Repository Preflight State

- HEAD: `f34c19be2b001763f7fb5ba4e4726ca7cc272f80`
- Branch: `main`
- Most recent commit: `f34c19b Add third Logic Theorist run evidence`

`git status --short`:

```text
?? docs/iplv_fork_retirement_migration_prompt.md
?? review-notes/20260601_deep_technical_analysis.md
?? review-notes/20260601_project_assessment.md
?? review-notes/20260601_theorem_424_discrepancy_analysis.md
```

Companion remote:

```text
origin  https://github.com/jblattnernyc/logic-theorist-companion.git (fetch)
origin  https://github.com/jblattnernyc/logic-theorist-companion.git (push)
```

## Migration Rationale and Intended State

The public fork `jblattnernyc/IPL-V` is being retired because it appears alongside the owner's original public projects on the GitHub profile even though its role is only to preserve an executable specimen derived from the original upstream repository.

The intended post-migration architecture is:

```text
Public research project:
  https://github.com/jblattnernyc/logic-theorist-companion

External provenance source:
  https://github.com/jeffshrager/IPL-V

Local executable specimen:
  /Users/john-blattner/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V
  pinned at e35a705d57e99fe91d76d76b224b8af30f2fd632
```

The intended post-migration local IPL-V remote configuration is:

```text
origin  https://github.com/jeffshrager/IPL-V.git (fetch)
origin  DISABLED (push)
```

Reproduction must use the exact documented commit, `e35a705d57e99fe91d76d76b224b8af30f2fd632`, rather than the current tip of upstream `master`.

## Preservation Statements

- No tracked IPL-V source files were modified while creating this preflight record.
- The local IPL-V branch, HEAD, and working tree were not updated.
- Logic Theorist was not executed.
- The untracked IPL-V `.DS_Store` was not deleted, cleaned, overwritten, or staged.
- The untracked companion migration prompt and review notes were not deleted, cleaned, overwritten, or staged.
- Historical evidence, including prior baseline records, runs, reports, review notes, and changelog entries, remains unchanged.
- No commit was created or pushed, and no GitHub repository was deleted.
