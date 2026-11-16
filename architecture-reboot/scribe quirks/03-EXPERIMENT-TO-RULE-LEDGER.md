# Experiment-to-Rule Ledger

## Purpose

This file records the Doximity execution evidence that produced the current engine rules.

It intentionally distinguishes:

- valid execution evidence;
- invalid/stale tests;
- architecture conclusions;
- rejected patterns.

Patient-specific content is omitted.

---

# A. Scribe experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 105 — source-first prompt review | Category-first organization risks flattening chronology, provenance, and contradictions. | Keep source families separate during ingestion. Scribe formats evidence; downstream owns reconciliation. |
| Review 106 — first Scribe structural audit | Source-first organization was viable; cross-source duplication appeared. | Each supplied source should appear once. Do not create normalized duplicate source sections merely for convenience. |
| Review 107 — raw-to-Scribe fidelity audit | Scribe compressed noisy transcript while retaining high-value neurology semantics; template material and nested provenance could still distort output. | Keep Scribe source-faithful. Fence/remove templates. Preserve nested provenance rather than promoting it to direct provenance. |
| Review 110 — Scribe V2 | Unsupported negative inference, garbled-word repair, cross-speaker merge, and speaker-identity inference remained. | One raw speaker/source unit owns one record. Do not repair clinically plausible wording. SPK label is not stable identity. |
| Review 112 — Scribe V2.1 | Prechart compression worked better than transcript question/answer synthesis. | Treat transcript and prechart as different morphologies. Transcript needs stricter turn preservation; prechart can use coherent source-local compression. |
| Review 114 — Scribe V2.2 same-case | Turn-preserving transcript and no-repair rules removed the material prior failures. | One transcript record derives from one raw turn. Preserve odd wording. Do not synthesize across turns. |
| Review 115 — first held-out V2.2 | Structure generalized to a long noisy clinical case; large irrelevant history remained. | Do not push clinical relevance/problem selection into Scribe just because the packet is noisy. Downstream owns relevance. |
| Review 116 — second held-out V2.2 | No new material Scribe-layer failure; long packet completed. | Freeze ingestion unless a downstream failure localizes back to Scribe. Do not optimize Scribe speculatively. |
| Current hard-gate Scribe runs | Hard read-all gate + atomic functional rules materially improved behavior. | Put no-emission gate first. Use atomic imperative functions. Final emission gate last. |

---

# B. First Ask / reconciliation experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 121 — global atomicization failure | One-or-many rewritten evidence objects per source record created a near-full second copy and cardinality explosion. | Reject global atomicization. Decompose lazily only when a downstream distinction requires it. |
| Review 123 — compact F1 dry run | Compact reference-backed reconciliation was possible without recreating full packet. | Intermediate handoffs should be indexes/reconciliations, not replacement evidence stores. Keep raw packet available for dereference. |
| Review 124 — first Doximity F1 | Cardinality solved, but heterogeneous subjects were overcompressed. | Compress only within one coherent clinical subject/trajectory. Do not bundle unrelated facts merely to reduce item count. |
| Review 125 — second F1 | Clinical handoff improved; exact wrapper drift remained; UNRESOLVED invented downstream next steps. | Freeze behavioral boundary rather than parser-perfect syntax unless mechanical parsing requires it. UNRESOLVED carries issue/evidence, not recommendations. |
| Review 126 — action-state dry run | A state-history concept was cognitively coherent, but only when every transition was source-supported. | Never infer hidden intermediate action states. "Needed" != ordered; completed test != available result. |
| Review 127 — first canonical F1 | Wrong/nonexistent refs, question-as-answer support, and action-state upgrades appeared. | Every referenced record must directly support the represented clause. Question records cannot support answers. Do not infer administration from recommendation/order/discontinuation. |

---

# C. Validator experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 128 — combined vs separate validator | Combined generation+validation reduced observability. Separate validator visibly ran but still false-passed. | Do not assume instruction separation inside one context creates semantic independence. |
| Review 129 — stale validator execution | Old validator version executed after a newer version existed. | Verify the model actually executed the intended contract/version before interpreting a test. Invalid execution produces no engine conclusion. |
| Review 130 — same-context validator V2 | Full item-level verification ledger still false-passed obvious reference/action errors. | Same-context LLM semantic validation is not trustworthy merely because it is exhaustive or observable. |
| Review 131 — escalation | Repeated false PASS despite increasingly explicit validator checks. | Stop adding semantic validator prose. Solve semantic ownership/representation upstream. |
| Review 132 — pointer counterproposal | Claim-generating F1 + same-model validation was the wrong boundary; quote anchors risked recreating copying errors. | Prefer pointer/reference structures over copied semantic claims when the source packet already preserves evidence. Mechanical invariants only where truly mechanical. |

---

# D. Pointer / sparse-A experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 134 — pointer-only F1 | Total routing coverage was achievable and compact; overly broad catch-all routing remained. | Pointer-only routing is viable. Use specific nonassertive categories; do not hide clinically useful records in source-wide catch-alls. |
| Review 135 — three-record A contract | Small sparse interpretation/reconciliation boundary worked. | Small, bounded semantic contracts can work when responsibilities are narrow. |
| Review 136 — field-fix rerun | Correcting certainty/relation semantics produced pass without expanding scope. | Distinguish attribution from certainty. Do not force same-state relation when only possible overlap is supported. |
| Review 137 — small B contract | Problem architecture could preserve historical/current distinctions without overpromotion. | Problem construction should be downstream of source preservation. Do not infer causality or PRIMARY status from mere historical coexistence. |
| Review 139 — full-packet A V1 | Completed at scale but failed attribution/action normalization and mixed assertions. | Packet size was not the main problem. Semantic normalization and action-state ownership were. |
| Review 140 — A V1.1 rerun | Fixing some semantics caused other material evidence to disappear; coverage became unstable. | Coverage selection, normalization, reconciliation, and compression compete when performed together. Separate the coverage-preservation responsibility from synthesis. |
| Review 141 — first A1/A2 split | Split localized corruption but A1/A2 contracts still allowed source drift and semantic editing. | Decomposition helps only when each stage is genuinely narrower. Do not let a later stage reread/repair what the earlier stage omitted. |
| Review 142 — standalone source-local A | Coverage improved, but action state slots were still filled beyond source evidence. | Schema completion can dominate explicit anti-inference instructions. Do not use representations that invite unsupported state completion. |

---

# E. Action-state representation experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 143 — ASSERTED_STATE | Requiring exact source phrase did not prevent unsupported state assignment. | Exact phrase anchoring does not guarantee semantic state fidelity. A real phrase can still be mapped to the wrong state. |
| Review 144 — action-state boundary redesign | Moving normalized state out of ingestion was the coherent response to repeated failure. | Ingestion should preserve source-local action identity/wording; normalized interpretation, if needed, belongs later. |
| Review 145 — wording-only A2 repeated runs | Removing state enums fixed state promotion, but action enumeration/splitting varied materially between runs. | Coverage/action enumeration is a separate function from state interpretation. Compound/distributed action discovery needs its own coverage responsibility. |
| Review 146 — A->B1 integration | One-call execution shape worked; semantic issues remained in mixed polarity, actor identity, ambiguous preference, and episode grouping. | Source labels are not actors. Unresolved episode identity means do not group. Split materially different polarity/certainty/roles before assigning metadata. |
| Review 147 — rerun | Bounded fixes improved output; service-label shorthand still tempted state inference. | Bare specialty/service label + intervention is not enough to establish planned/recommended/ordered/performed. |
| Review 148 — clean packet A->B1 | Action-state enum completion recurred despite cleaner input and moved responsibility. | The enum representation itself is brittle. Retire decision/execution/response/result normalization rather than tuning it again. |
| Review 149 — source-qualified B | Removing normalized state enums produced near-pass and faithful management wording. | Prefer ordinary source-qualified management wording over brittle normalized action-state slots. |

---

# F. Architecture and direct-B experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Review 150 — post-D053 architecture review | A might be redundant; B lacked reconciled clinical units; C was not decision-complete. | Test stage necessity empirically. B must emit the result of decisions it owns. C must not reconstruct B's reconciliation. |
| Review 151 — A vs direct-B, four runs | A did not improve pointer fidelity; direct-B reduced burden but lost body/nonproblem evidence. | Do not preserve a stage merely because it exists. Identify its unique useful function. Direct synthesis needs a stable home for nonproblem/body evidence. |
| Review 152 — direct-B + CLINICAL_UNIT | Clinical-unit home improved coverage, but exact selector copying still drifted across neighboring records. | Do not ask the synthesizer to reproduce exact substrings from a long packet while also reasoning. Prefer record-ID provenance. |
| Review 153 — record-ID-only direct-B | Selector-copy defect was removed, but direct-B still missed/wrongly selected records and omitted actions/body evidence. | The remaining unique ingestion function is a dedicated **coverage census** before synthesis. Coverage enumeration and clinical synthesis should not compete. |

---

# G. Reproducibility / renderer experiments

| Evidence | Observed behavior | Rule derived |
|---|---|---|
| Gradient Arm A | Ordinary prose produced clinically similar but merge/split and wording drift. | Do not rely on prose rules to determine semantic grouping. |
| Gradient Arm B | Structured DSL stabilized clinical structure but not wording. | Explicit roles/grouping remove semantic drift; surface realization remains generative. |
| Gradient Arm C | Fully precomputed output was identical across three fresh runs. | Doximity can reproduce exact output when decisions are fully specified; platform randomness is not the only cause of drift. |
| B+ canonical operators | 24/24 operator executions matched across three fresh conversations. | Small canonical operators can recover reproducibility without prewriting the whole note. |
| B+ incomplete proposition bug | Same malformed reasoning sentence reproduced identically. | Stable bad output = deterministic payload/operator defect. Fix semantic completeness upstream. |
| Operator stress suite | 63/63 valid renders correct; 45/45 malformed rejected; no silent repair. | Typed operator contracts can create a strong fail-closed execution boundary. |
| Operator error-label drift | Some invalid cases received different plausible error labels. | Do not overengineer error taxonomy. Preserve valid/invalid behavior first. |

---

# H. Rules that survived multiple independent experiments

## RULE 1 — Decision completeness beats prose repetition

Repeated across:

- gradient;
- B+;
- action-state failures;
- direct-B tests.

If a later stage repeatedly invents or varies a decision, either:

- provide that decision explicitly upstream;
- or remove the brittle representation.

Do not keep restating the same prose warning.

---

## RULE 2 — Coverage and synthesis are competing functions

Repeated across:

- A V1/V1.1;
- wording-only A2;
- direct-B;
- direct-B + clinical units;
- record-ID-only direct-B.

A model can synthesize a clinically good case while silently omitting records/actions.

Use a dedicated coverage census before synthesis.

---

## RULE 3 — Exact copying during reasoning is brittle

Repeated across:

- quote-anchor concerns;
- A selectors;
- direct-B selectors;
- clinical-unit selectors.

When coherent source records already exist, cite stable record IDs and dereference text mechanically.

---

## RULE 4 — Semantic self-validation is not independence

Repeated across:

- F1V V1;
- F1V V2;
- same-context ledger validation.

Observable execution is not equivalent to accurate adversarial checking.

---

## RULE 5 — Schema completion pressure is real

Repeated across:

- A action slots;
- ASSERTED_STATE;
- B1 state slots.

If a schema presents a conceptual state table, Doximity may fill dimensions that the source never established.

Remove the slots when repeated anti-completion rules fail.

---

## RULE 6 — Source-qualified wording is robust

After action-state enums were retired, source-qualified management wording improved fidelity.

Use the smallest transformation needed to make source wording clinically usable.

---

## RULE 7 — A wrong stable output is easier to fix than stochastic drift

The B+ "MRI to show" bug was deterministic.

When the same bad output repeats:

- inspect payload completeness;
- inspect operator semantics;
- do not blame randomness.

---

## RULE 8 — Fail closed at the render boundary

Malformed semantic structures should not be repaired by the final writer.

---

# I. Invalid tests / evidence limitations

Do not derive new engine rules from:

- stale validator execution that did not run the intended version;
- translated "control" output that was not an independent run;
- held-out Scribe outputs where raw source was unavailable for fidelity adjudication;
- one better run chosen after the fact while a paired run failed materially;
- manually unioned outputs from multiple runs.

These can inform hypotheses, not capability claims.
