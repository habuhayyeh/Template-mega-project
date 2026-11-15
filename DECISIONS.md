# DECISIONS

Permanent. A decision changes only by a new decision that names the old one.

| ID | Decision |
|---|---|
| D-001 | Six semantic kinds — `DEMOGRAPHIC`, `OBSERVATION`, `COURSE`, `MANAGEMENT`, `DIAGNOSTIC_FORMULATION`, `ETIOLOGY`. No reasoning kind; reasoning is compositional and is carried by formulation and etiology objects. |
| D-002 | The A/P derives from the Handoff only. `05` never reads the sources. |
| D-003 | One frozen substrate feeds both branches. Neither branch consumes the other's intermediate output. |
| D-004 | Explicit current-clinician reasoning outranks downstream inference. Where the clinician stated a formulation, etiology or adjudication, the pipeline organizes it rather than reconstructing a substitute. |
| D-005 | `02` and `05` are prose modules. Their code-spec versions are superseded and live only in history. |
| D-006 | Production `06` is unresolved. The section contract and the reviewed ledger are accepted; Doximity runs of `06` are not reliable enough to run unattended (3 runs: 12, 6, 9 unacceptable differences; schema broken on the third). |
| D-007 | `04` dereferences O# and appends provenance verbatim. Provenance is never added to the `03` ledger. |
| D-008 | `EVIDENCE_MODE` is required on `OBSERVATION` and `COURSE` only; it is routing metadata and never appears in prose. |
| D-009 | One writer per path. The reviewer writes `reviews/` only. |
| D-010 | No real patient data in the repository. Synthetic or de-identified only. |
