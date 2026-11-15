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
| D-011 | The three contract edits imported in `import/v2` are ratified as baseline: `03` exclusive evidence eligibility and reasoning protection, `04` exemption of reasoning from duplicate deletion, `05` reasoning rendering rules. They are not re-proposed. |
| D-012 | Agent conversation runs through `channel/`, two single-writer files. The channel is conversation, not state: agreement is recorded in `DECISIONS.md`, currency in `STATUS.md`. No push-to-chat trigger exists; the loop uses a one-line prompt. |
| D-013 | Escalation rule. Either agent stops and asks the user when the two agents disagree without repository evidence, when a contract is genuinely ambiguous, when the choice is clinical, stylistic or product, or when the alternative is guessing. Mechanical choices are not escalated. The answer becomes a `D-###`. |
| D-014 | O54 residual mild expressive aphasia stays out of the A/P. It is sequela context for the old infarct, which O7 and O18 already establish; admitting the [D] copy after excluding the [A] copy as context would be indefensible. The fact remains in the body note. The A/P does not need every retained entry to render. |
| D-015 | Chronic-block rule. A chronic neurologic problem gets its own shorter A/P block when the encounter contains a management decision directed at that problem. Diagnosis alone, or a listed home medication alone, does not create a block. The decision must be source-grounded as directed at that chronic problem in this encounter; the target is never inferred from drug class or general knowledge. Active problems are ordered first. The block carries problem-defining facts, the reasoning that explains it, and the management directed at it. Non-neurologic problems do not become blocks unless they materially affect neurologic assessment or management. |
| D-016 | Scope of the pre-05 fixes is narrowed (signer, 2026-11-15). P006 stays the explicit render/compose grouping fix for the instability demonstrated in clean set 3. COURSE typing, evidence include-flags, management canonicalisation and standing-item injection are **not** adopted now; a broader P007 may be proposed only if residual instability after P006 demonstrates the need. No broader pre-05 normalisation is added on the strength of an external audit whose package provenance was wrong. |
