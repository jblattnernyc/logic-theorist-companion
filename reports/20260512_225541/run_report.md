# Logic Theorist Run Report: 20260512_225541

Generated: `2026-05-13T02:55:58+00:00`

This report describes preserved local executable behavior from a companion run bundle. It is not a historical claim about the original Logic Theorist, the published literature, or any upstream repository.

## Source Evidence

- Run directory: `runs/20260512_225541`
- Recorded IPL-V specimen path: `/Users/john-blattner/Documents/PROGRAMMING/IPL/LOGIC THEORIST/IPL-V`
- Recorded command: `sbcl --dynamic-space-size 4096 --eval \(load\ \(compile-file\ \"lt.lisp\"\)\) --eval \(sb-ext:exit\)`
- Start date: `Tue May 12 22:55:41 EDT 2026`
- End date: `Tue May 12 22:55:46 EDT 2026`
- Exit status: `0`
- Manifest status: `OK` over `35` entries
- Primary Logic Theorist log files: `generated_artifacts/ltresults/202605122255.log`

## Version and Environment

- IPL-V commit: `e35a705d57e99fe91d76d76b224b8af30f2fd632`
- IPL-V branch: `master`
- IPL-V latest commit line: `e35a705 no message`
- SBCL version: `SBCL 2.6.4`
- System: `Darwin Johns-Mac-mini.local 25.4.0 Darwin Kernel Version 25.4.0: Thu Mar 19 19:31:09 PDT 2026; root:xnu-12377.101.15~1/RELEASE_ARM64_T8132 arm64`

## Summary

- Theorem attempts parsed: `23`
- Proofs found: `17`
- No-proof outcomes: `6`
- Unknown outcomes: `0`
- Logic Theorist log findings: `11`
- Compiler/stderr findings: `23`

Status counts:

```json
{
  "NO PROOF FOUND": 6,
  "PROOF FOUND": 17
}
```

## Notable Theorems

| Theorem | Status | Expression | Effort | Subproblems | Substitutions | Source | Line | Associated dot artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.21 | PROOF FOUND | -PI(PIQ) | 5482 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 393 | generated_artifacts/tmp/lt-proof-221.dot |
| 2.24 | NO PROOF FOUND | PI(-PVQ) | 207183 | 18 | 19 | generated_artifacts/ltresults/202605122255.log | 415 | generated_artifacts/tmp/lt-proof-224.dot |
| 4.13 | PROOF FOUND | P=--P | 8122 | 2 | 3 | generated_artifacts/ltresults/202605122255.log | 610 | generated_artifacts/tmp/lt-proof-413.dot |
| 4.24 | PROOF FOUND | P=(P*P) | 43016 | 11 | 12 | generated_artifacts/ltresults/202605122255.log | 657 | generated_artifacts/tmp/lt-proof-424.dot |
| 4.25 | PROOF FOUND | P=(PVP) | 12277 | 3 | 4 | generated_artifacts/ltresults/202605122255.log | 695 | generated_artifacts/tmp/lt-proof-425.dot |

## Theorem Outcomes

| Theorem | Status | Expression | Effort | Subproblems | Substitutions | Source | Line | Associated dot artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.01 | PROOF FOUND | (PI-P)I-P | 5579 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 46 | generated_artifacts/tmp/lt-proof-201.dot |
| 2.02 | PROOF FOUND | QI(PIQ) | 4253 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 68 | generated_artifacts/tmp/lt-proof-202.dot |
| 2.04 | PROOF FOUND | (PI(QIR))I(QI(PIR)) | 22175 | 3 | 4 | generated_artifacts/ltresults/202605122255.log | 90 | generated_artifacts/tmp/lt-proof-204.dot |
| 2.05 | PROOF FOUND | (QIR)I((PIQ)I(PIR)) | 9280 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 114 | generated_artifacts/tmp/lt-proof-205.dot |
| 2.06 | PROOF FOUND | (PIQ)I((QIR)I(PIR)) | 31762 | 5 | 6 | generated_artifacts/ltresults/202605122255.log | 136 | generated_artifacts/tmp/lt-proof-206.dot |
| 2.07 | PROOF FOUND | PI(PVP) | 1765 | 0 | 1 | generated_artifacts/ltresults/202605122255.log | 162 | generated_artifacts/tmp/lt-proof-207.dot |
| 2.08 | PROOF FOUND | PIP | 5853 | 2 | 3 | generated_artifacts/ltresults/202605122255.log | 181 | generated_artifacts/tmp/lt-proof-208.dot |
| 2.10 | PROOF FOUND | -PVP | 3680 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 204 | generated_artifacts/tmp/lt-proof-210.dot |
| 2.11 | PROOF FOUND | PV-P | 4377 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 226 | generated_artifacts/tmp/lt-proof-211.dot |
| 2.12 | PROOF FOUND | PI--P | 5594 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 248 | generated_artifacts/tmp/lt-proof-212.dot |
| 2.13 | PROOF FOUND | PV---P | 11592 | 2 | 3 | generated_artifacts/ltresults/202605122255.log | 270 | generated_artifacts/tmp/lt-proof-213.dot |
| 2.14 | NO PROOF FOUND | --PIP | 233510 | 19 | 20 | generated_artifacts/ltresults/202605122255.log | 293 | generated_artifacts/tmp/lt-proof-214.dot |
| 2.15 | NO PROOF FOUND | (-PIQ)I(-QIP) | 214612 | 25 | 26 | generated_artifacts/ltresults/202605122255.log | 326 | generated_artifacts/tmp/lt-proof-215.dot |
| 2.20 | PROOF FOUND | PI(PVQ) | 23515 | 6 | 7 | generated_artifacts/ltresults/202605122255.log | 366 | generated_artifacts/tmp/lt-proof-220.dot |
| 2.21 | PROOF FOUND | -PI(PIQ) | 5482 | 1 | 2 | generated_artifacts/ltresults/202605122255.log | 393 | generated_artifacts/tmp/lt-proof-221.dot |
| 2.24 | NO PROOF FOUND | PI(-PVQ) | 207183 | 18 | 19 | generated_artifacts/ltresults/202605122255.log | 415 | generated_artifacts/tmp/lt-proof-224.dot |
| 3.13 | NO PROOF FOUND | (-(P*Q))I(-PV-Q) | 239018 | 48 | 49 | generated_artifacts/ltresults/202605122255.log | 453 | generated_artifacts/tmp/lt-proof-313.dot |
| 3.14 | NO PROOF FOUND | (-PV-Q)I(-(P*Q)) | 200411 | 13 | 14 | generated_artifacts/ltresults/202605122255.log | 515 | generated_artifacts/tmp/lt-proof-314.dot |
| 3.24 | NO PROOF FOUND | -(P*-P) | 213818 | 24 | 25 | generated_artifacts/ltresults/202605122255.log | 574 | generated_artifacts/tmp/lt-proof-324.dot |
| 4.13 | PROOF FOUND | P=--P | 8122 | 2 | 3 | generated_artifacts/ltresults/202605122255.log | 610 | generated_artifacts/tmp/lt-proof-413.dot |
| 4.20 | PROOF FOUND | P=P | 7834 | 3 | 4 | generated_artifacts/ltresults/202605122255.log | 633 | generated_artifacts/tmp/lt-proof-420.dot |
| 4.24 | PROOF FOUND | P=(P*P) | 43016 | 11 | 12 | generated_artifacts/ltresults/202605122255.log | 657 | generated_artifacts/tmp/lt-proof-424.dot |
| 4.25 | PROOF FOUND | P=(PVP) | 12277 | 3 | 4 | generated_artifacts/ltresults/202605122255.log | 695 | generated_artifacts/tmp/lt-proof-425.dot |

## Warnings and Anomalous Lines

Logic Theorist log finding counts:

```json
{
  "ambiguous PQ warning": 6,
  "bad expression": 2,
  "missing local symbol warning": 3
}
```

Compiler/stderr finding counts:

```json
{
  "compiler note": 1,
  "compiler style warning": 3,
  "compiler summary": 2,
  "compiler warning": 17
}
```

Representative findings, limited to the first 40 lines found:

| Category | Source | Line | Text |
| --- | --- | --- | --- |
| missing local symbol warning | generated_artifacts/ltresults/202605122255.log | 1 | WARNING: Cell "M14-9-1" is being added for missing local symbol "9-1"! |
| missing local symbol warning | generated_artifacts/ltresults/202605122255.log | 2 | WARNING: Cell "M15-9-1" is being added for missing local symbol "9-1"! |
| missing local symbol warning | generated_artifacts/ltresults/202605122255.log | 3 | WARNING: Cell "M111-9-10" is being added for missing local symbol "9-10"! |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 4 | *** WARNING: PQ "1" (in ("SUBSTITUTION COUNT" "" "K11" "+" "1" "" "    0" "" "K011D000")) is ambugious and intepreted as p=0, q=1 |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 5 | *** WARNING: PQ "1" (in ("SUBSTITUTION COUNT" "" "K11" "+" "1" "" "    0" "" "K011D000")) is ambugious and intepreted as p=0, q=1 |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 6 | *** WARNING: PQ "1" (in ("EFFORT BASE AND TOTAL" "" "K12" "+" "1" "" "0" "" "K012D000")) is ambugious and intepreted as p=0, q=1 |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 7 | *** WARNING: PQ "1" (in ("EFFORT BASE AND TOTAL" "" "K12" "+" "1" "" "0" "" "K012D000")) is ambugious and intepreted as p=0, q=1 |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 8 | *** WARNING: PQ "3" (in ("X19 MINOTOR POINT FORCER." "" "X19" "" "3" "J0" "0" "" "X019R000")) is ambugious and intepreted as p=0, q=3 |
| ambiguous PQ warning | generated_artifacts/ltresults/202605122255.log | 9 | *** WARNING: PQ "3" (in ("X19 MINOTOR POINT FORCER." "" "X19" "" "3" "J0" "0" "" "X019R000")) is ambugious and intepreted as p=0, q=3 |
| bad expression | generated_artifacts/ltresults/202605122255.log | 12 | BAD EXPRESSION   ((P*Q).=.-(-(PV-Q)/UGH/) |
| bad expression | generated_artifacts/ltresults/202605122255.log | 23 | BAD EXPRESSION   (((PI-Q)I(QI-P)/UGH/) |
| compiler warning | stderr.txt | 6 | ; caught WARNING: |
| compiler warning | stderr.txt | 7 | ;   undefined variable: COMMON-LISP-USER::*CARD-CYCLES.IDS-EXECUTED* |
| compiler warning | stderr.txt | 12 | ; caught WARNING: |
| compiler warning | stderr.txt | 13 | ;   undefined variable: COMMON-LISP-USER::*CARD-CYCLES.IDS-EXECUTED* |
| compiler warning | stderr.txt | 18 | ; caught WARNING: |
| compiler warning | stderr.txt | 19 | ;   undefined variable: COMMON-LISP-USER::*CARD-CYCLES.IDS-EXECUTED* |
| compiler warning | stderr.txt | 22 | ; caught WARNING: |
| compiler warning | stderr.txt | 23 | ;   2 more uses of undefined variable *CARD-CYCLES.IDS-EXECUTED* |
| compiler warning | stderr.txt | 32 | ; caught WARNING: |
| compiler warning | stderr.txt | 33 | ;   undefined variable: COMMON-LISP-USER::*J15-MODE* |
| compiler warning | stderr.txt | 45 | ; caught WARNING: |
| compiler warning | stderr.txt | 46 | ;   undefined variable: COMMON-LISP-USER::*TRACE-EXPRS* |
| compiler style warning | stderr.txt | 50 | ; caught STYLE-WARNING: |
| compiler warning | stderr.txt | 51 | ;   undefined function: COMMON-LISP-USER::LOAD-IPL |
| compiler style warning | stderr.txt | 55 | ; caught STYLE-WARNING: |
| compiler warning | stderr.txt | 56 | ;   undefined function: COMMON-LISP-USER::SET-TRACE-MODE |
| compiler summary | stderr.txt | 58 | ; compilation unit finished |
| compiler warning | stderr.txt | 59 | ;   Undefined functions: |
| compiler warning | stderr.txt | 61 | ;   Undefined variables: |
| compiler warning | stderr.txt | 63 | ;   caught 6 WARNING conditions |
| compiler style warning | stderr.txt | 64 | ;   caught 2 STYLE-WARNING conditions |
| compiler note | stderr.txt | 70 | ; note: deleting unreachable code |
| compiler summary | stderr.txt | 72 | ; compilation unit finished |

## Analysis Outputs

- Markdown report: `reports/20260512_225541/run_report.md`
- Theorem CSV: `reports/20260512_225541/theorem_summary.csv`
- JSON summary: `reports/20260512_225541/analysis_summary.json`
- Analysis manifest: `reports/20260512_225541/analysis_manifest.sha256`

## Methodological Notes

The parser treats the preserved `generated_artifacts/ltresults/*.log` files as the primary source for theorem-attempt parsing. `stdout.txt` is preserved as evidence, but it may duplicate the Logic Theorist log content and is not used as the primary theorem table source.

Associated `.dot` artifacts are listed by filename correspondence only. Their presence is not interpreted as an independent proof claim, especially where the parsed theorem status is `NO PROOF FOUND`.

This first-version parser is intentionally conservative. It records local output structure, status markers, metric lines, warning lines, and notable theorem statuses without changing the IPL-V executable specimen.
