# Logic Theorist Run Comparison: 20260512_010918__20260512_141829

Generated: `2026-05-12T18:44:30+00:00`

This report compares derived analysis records for preserved local Logic Theorist runs. It describes local reproducibility evidence only. It is not a historical claim about the original Logic Theorist, the published literature, or any upstream repository.

## Compared Runs

| Run ID | Raw run directory | Analysis directory |
| --- | --- | --- |
| 20260512_010918 | runs/20260512_010918 | reports/20260512_010918 |
| 20260512_141829 | runs/20260512_141829 | reports/20260512_141829 |

## Summary

- Compared runs: `20260512_010918, 20260512_141829`
- Theorem rows compared: `23`
- Theorem rows matching across compared fields: `23`
- Theorem rows with differences: `0`
- All theorem rows match: `True`
- All selected metadata fields match: `True`
- All raw run manifests verify: `True`
- All analysis manifests verify: `True`

## Raw Run Manifests

| Run ID | Status | Entries | Manifest |
| --- | --- | --- | --- |
| 20260512_010918 | OK | 36 | runs/20260512_010918/manifest.sha256 |
| 20260512_141829 | OK | 36 | runs/20260512_141829/manifest.sha256 |

## Analysis Manifests

| Run ID | Status | Entries | Manifest |
| --- | --- | --- | --- |
| 20260512_010918 | OK | 3 | reports/20260512_010918/analysis_manifest.sha256 |
| 20260512_141829 | OK | 3 | reports/20260512_141829/analysis_manifest.sha256 |

## Selected Metadata Comparison

| Field | All Match | Values |
| --- | --- | --- |
| iplv_commit | True | {"20260512_010918": "e35a705d57e99fe91d76d76b224b8af30f2fd632", "20260512_141829": "e35a705d57e99fe91d76d76b224b8af30f2fd632"} |
| iplv_branch | True | {"20260512_010918": "master", "20260512_141829": "master"} |
| iplv_latest_commit_line | True | {"20260512_010918": "e35a705 no message", "20260512_141829": "e35a705 no message"} |
| sbcl_version | True | {"20260512_010918": "SBCL 2.6.4", "20260512_141829": "SBCL 2.6.4"} |
| system | True | {"20260512_010918": "Darwin Johns-Mac-mini.local 25.4.0 Darwin Kernel Version 25.4.0: Thu Mar 19 19:31:09 PDT 2026; root:xnu-12377.101.15~1/RELEASE_ARM64_T8132 arm64", "20260512_141829": "Darwin Johns-Mac-mini.local 25.4.0 Darwin Kernel Version 25.4.0: Thu Mar 19 19:31:09 PDT 2026; root:xnu-12377.101.15~1/RELEASE_ARM64_T8132 arm64"} |
| theorem_attempt_count | True | {"20260512_010918": 23, "20260512_141829": 23} |
| status_counts | True | {"20260512_010918": {"NO PROOF FOUND": 6, "PROOF FOUND": 17}, "20260512_141829": {"NO PROOF FOUND": 6, "PROOF FOUND": 17}} |
| logic_theorist_log_finding_counts | True | {"20260512_010918": {"ambiguous PQ warning": 6, "bad expression": 2, "missing local symbol warning": 3}, "20260512_141829": {"ambiguous PQ warning": 6, "bad expression": 2, "missing local symbol warning": 3}} |
| compiler_stderr_finding_counts | True | {"20260512_010918": {"compiler note": 1, "compiler style warning": 3, "compiler summary": 2, "compiler warning": 17}, "20260512_141829": {"compiler note": 1, "compiler style warning": 3, "compiler summary": 2, "compiler warning": 17}} |

## Notable Theorems

| Theorem | All Fields Match | Statuses | Effort Actuals | Differences |
| --- | --- | --- | --- | --- |
| 2.21 | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "5482", "20260512_141829": "5482"} |  |
| 2.24 | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "207183", "20260512_141829": "207183"} |  |
| 4.13 | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "8122", "20260512_141829": "8122"} |  |
| 4.24 | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "43016", "20260512_141829": "43016"} |  |
| 4.25 | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "12277", "20260512_141829": "12277"} |  |

## Theorem Comparison

| Theorem | Notable | Expression | All Fields Match | Statuses | Effort Actuals | Differences |
| --- | --- | --- | --- | --- | --- | --- |
| 2.01 | False | (PI-P)I-P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "5579", "20260512_141829": "5579"} |  |
| 2.02 | False | QI(PIQ) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "4253", "20260512_141829": "4253"} |  |
| 2.04 | False | (PI(QIR))I(QI(PIR)) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "22175", "20260512_141829": "22175"} |  |
| 2.05 | False | (QIR)I((PIQ)I(PIR)) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "9280", "20260512_141829": "9280"} |  |
| 2.06 | False | (PIQ)I((QIR)I(PIR)) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "31762", "20260512_141829": "31762"} |  |
| 2.07 | False | PI(PVP) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "1765", "20260512_141829": "1765"} |  |
| 2.08 | False | PIP | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "5853", "20260512_141829": "5853"} |  |
| 2.10 | False | -PVP | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "3680", "20260512_141829": "3680"} |  |
| 2.11 | False | PV-P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "4377", "20260512_141829": "4377"} |  |
| 2.12 | False | PI--P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "5594", "20260512_141829": "5594"} |  |
| 2.13 | False | PV---P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "11592", "20260512_141829": "11592"} |  |
| 2.14 | False | --PIP | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "233510", "20260512_141829": "233510"} |  |
| 2.15 | False | (-PIQ)I(-QIP) | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "214612", "20260512_141829": "214612"} |  |
| 2.20 | False | PI(PVQ) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "23515", "20260512_141829": "23515"} |  |
| 2.21 | True | -PI(PIQ) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "5482", "20260512_141829": "5482"} |  |
| 2.24 | True | PI(-PVQ) | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "207183", "20260512_141829": "207183"} |  |
| 3.13 | False | (-(P*Q))I(-PV-Q) | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "239018", "20260512_141829": "239018"} |  |
| 3.14 | False | (-PV-Q)I(-(P*Q)) | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "200411", "20260512_141829": "200411"} |  |
| 3.24 | False | -(P*-P) | True | {"20260512_010918": "NO PROOF FOUND", "20260512_141829": "NO PROOF FOUND"} | {"20260512_010918": "213818", "20260512_141829": "213818"} |  |
| 4.13 | True | P=--P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "8122", "20260512_141829": "8122"} |  |
| 4.20 | False | P=P | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "7834", "20260512_141829": "7834"} |  |
| 4.24 | True | P=(P*P) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "43016", "20260512_141829": "43016"} |  |
| 4.25 | True | P=(PVP) | True | {"20260512_010918": "PROOF FOUND", "20260512_141829": "PROOF FOUND"} | {"20260512_010918": "12277", "20260512_141829": "12277"} |  |

## Outputs

- Markdown comparison report: `reports/comparisons/20260512_010918__20260512_141829/comparison_report.md`
- Comparison CSV: `reports/comparisons/20260512_010918__20260512_141829/comparison_summary.csv`
- Comparison JSON: `reports/comparisons/20260512_010918__20260512_141829/comparison_summary.json`
- Comparison manifest: `reports/comparisons/20260512_010918__20260512_141829/comparison_manifest.sha256`

## Methodological Notes

The comparison uses `reports/RUN_ID/theorem_summary.csv` and `reports/RUN_ID/analysis_summary.json` as derived inputs. It also verifies the raw run manifest under `runs/RUN_ID/manifest.sha256` and the analysis manifest under `reports/RUN_ID/analysis_manifest.sha256`.

The theorem comparison checks theorem identifiers, expressions, proof/no-proof status, effort counts, subproblem counts, substitution counts, remembered-theorem fields, and notable-theorem flags. It intentionally omits run-specific fields such as source log filename, line number, and associated artifact filename from the equality test because those may differ by run timestamp while preserving the same theorem-level behavior.
