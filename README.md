# Logic Theorist Companion Repository

This repository is the companion research apparatus for the Logic Theorist / IPL-V software archaeology, reproducibility, and evidence project.

It is intentionally separate from the executable IPL-V specimen repository. The companion repository is for reproducibility workflow documentation, baseline metadata, evidence records, parser and audit scripts, reports, manifests, internal review notes, and publication-support materials.

## Repository Model

The intended local workspace is:

```text
~/Documents/PROGRAMMING/IPL/LOGIC THEORIST/
  IPL-V/                         executable specimen; fork of upstream IPL-V
  logic-theorist-companion/       companion research apparatus
```

The parent `LOGIC THEORIST/` directory is a workspace container and should not be treated as a monorepo.

## IPL-V Provenance

The original upstream IPL-V source is:

```text
https://github.com/jeffshrager/IPL-V
```

The local `IPL-V/` repository is expected to be cloned from a project fork of that upstream repository, with `upstream` configured to `https://github.com/jeffshrager/IPL-V.git`.

## Separation of Materials

This repository should contain companion materials only. It should not contain a copied full IPL-V source tree.

The project distinguishes among:

1. Original upstream IPL-V source.
2. The local executable IPL-V specimen.
3. Native generated Logic Theorist run artifacts.
4. Companion analysis, reports, manifests, scripts, and interpretation.

Future Logic Theorist runs may create native generated files under the executable specimen repository when faithful operation requires it. Organized copies, reports, parser outputs, manifests, and review notes belong in this companion repository or in explicitly documented external evidence storage.

## Current Repository Status

The public IPL-V fork is:

```text
https://github.com/jblattnernyc/IPL-V
```

The public companion repository is:

```text
https://github.com/jblattnernyc/logic-theorist-companion
```

The local IPL-V specimen has been cloned from the project fork and configured with `upstream` pointing to the original `jeffshrager/IPL-V` repository.

The local companion repository has `origin` configured, and the initial scaffold has been committed and pushed. Future GitHub issues, pull requests, releases, tags, commits, pushes, and Logic Theorist execution require explicit confirmation.

## Upstream Contact Policy

This project does not publish pull requests, GitHub issues, comments, maintainer-review requests, or other communications to the original IPL-V repository or its maintainers as part of the normal workflow.

## License

This companion repository is licensed under the MIT License. This license applies to the original documentation, scripts, reports, and workflow materials in this repository. It does not change the licensing or provenance of the upstream IPL-V repository or historical source materials.

## Attribution

This companion repository is maintained by John Blattner as part of AI Universe Labs research work.

## Changelog

See `CHANGELOG.md` for the chronological project setup record.
