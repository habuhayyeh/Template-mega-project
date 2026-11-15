# ChatGPT review 022 — architecture-to-Phase-0 blind-spot audit

## Purpose

This review starts from the frozen architecture, not from the current Phase 0 files.

Question:

For every architectural invariant, seam, and known failure mechanism, what Phase 0 control proves that it is owned, testable, versioned, and incapable of being silently bypassed?

## Verdict

Phase 0 is incomplete as an engineering control plane.

Some gaps must be solved before Phase 1. Others do not need implementation yet, but Phase 0 must register their owner, prerequisite, and future acceptance obligation now so they cannot disappear.

## 1. Architecture invariant coverage itself is missing

The architecture contains many frozen invariants: one paste / one call; stable source-linked objects; no destructive routing; source-span accounting; temporality separate from adoption; neurologic problem model; explicit reuse; every render-affecting decision before RENDER; operator selection fixed before R1; weak renderer; downstream cannot compensate upstream failure; fail closed; section-scoped style; centralized ordering; object usage/disposition accounting; source-to-IR semantic audit separate from IR-to-note mechanical check; test-mode ledger; one decision owner.

Phase 0 has no architecture coverage matrix with fields such as:
ARCH_INVARIANT_ID, owner, controlling contract, acceptance assertions, validation mode, fixtures, prerequisites, and status.

Without that matrix, an architectural invariant can be frozen in prose and never become a test obligation.

Required before Phase 1: create a traceability/coverage authority, likely linked to the missing implementation manifest.

## 2. Test mode vs production mode equivalence is ungoverned

Frozen architecture says TEST MODE additionally emits Case IR / execution trace, while production may suppress it.

We already know asking Doximity for extra structure can change behavior. Diagnostic trace runs are therefore not acceptance evidence.

Blind spot: what proves that the same production package and source with IR emission enabled versus suppressed produce the same note-relevant semantic decisions?

Required control: define a TEST/PRODUCTION EQUIVALENCE experiment using paired production-shaped and test-mode conditions with the same package/source/mode. Phase 0 need not run it now, but must register it as a mandatory deployment acceptance obligation.

## 3. Logical module boundaries are behavioral, not real access boundaries

INGEST, STRUCTURE, and RENDER all occur inside one Doximity call.

Inside one LLM context, R1/R2/R3 may still see raw source, upstream instructions, other objects, and neighboring problems. There is no actual memory sandbox preventing downstream repair.

Required control: define forbidden-context-dependence tests. Examples:
- hold fixed Case IR while perturbing irrelevant raw source; RENDER should not change;
- inject tempting raw-source content absent from the IR; RENDER must not recover it;
- hold a downstream artifact fixed while varying upstream wording where the seam should be invariant.

## 4. No failure-propagation / no-repair coverage map

Frozen process invariant: a downstream artifact may not compensate for an upstream failure.

Current Phase 0 has isolated failure behaviors, but no system-level matrix defining:
- exact failure artifact;
- which downstream modules stop;
- which may continue;
- whether partial note output is allowed;
- whether unaffected problems/cases continue;
- what is externally observable;
- who owns the failure.

Required Phase 0 authority: a failure-propagation matrix or equivalent registration requirement.

## 5. Whole-note atomicity vs partial success is undefined

If one unit is malformed, does the system fail the entire note, omit one unit, emit a partial note plus CONTRACT_ERROR, fail one problem block, or fail only one case in a multi-case batch?

Required before implementation: define failure-containment scope at unit, section, problem, case/note, and batch levels. Phase 0 must register the decision and required tests even if the exact failure-state contract lands in Phase 1.

## 6. No one-call resource / package budget control

The architecture requires all planning and rendering inside one Doximity call. This creates finite input context, instruction volume, output volume, and attention/instruction dilution.

Historical evidence already shows schema degradation with larger structured outputs.

Required future control: a deployment budget contract covering compiled package size, source payload size, output budget, batch size, telemetry overhead, and truncation sentinels. Do not invent numeric thresholds now. Phase 0 should register this as a measured deployment property.

## 7. Compiled-package semantic fidelity is not tested

The architecture separates modular GitHub source from compiled deployment artifact.

Compilation can drop, reorder, duplicate, shadow, or alter instructions even when source modules are correct.

Required control:
- source-to-package trace map;
- package version/hash;
- reproducible/canonical build where feasible;
- invariant that every required active source authority appears in the compiled package and every compiled authority traces to one active source.

## 8. Prompt/order sensitivity of the compiled package is ungoverned

Doximity has demonstrated non-local prompt sensitivity.

Semantically equivalent package serializations may not behave equivalently.

Required:
- canonical package ordering;
- package serialization version;
- A/B regression when order changes;
- package-order changes must not be treated automatically as PATCH.

## 9. Doximity environment/model/mode drift is not captured

Reproducibility is conditional on model/mode, package, source, conversation freshness, date/runtime environment.

Required experiment metadata:
- experiment id;
- date/time;
- observable Doximity model/mode label;
- package version/hash;
- source/batch version/hash;
- case order;
- test vs production mode;
- run number;
- material runtime settings.

## 10. Stable object identity across runs lacks a comparison method

Architecture says one source proposition keeps one stable object identity and E1 compares object coverage and identity.

If the same proposition is O17 in one run and O23 in another, what counts as identity stability?

Required future contract:
- ID determinism scope;
- namespace;
- collision rules;
- whether IDs are sequence labels or semantic identities;
- cross-run matching method.

Phase 0 should register ID stability/matching as an explicit prerequisite for E1 scoring.

## 11. Cross-case namespace isolation is missing

The signer wants 8–12 cases in one Doximity batch.

Without a case namespace, local O1/P1/U1 ids can collide across cases and allow cross-case references.

Required: CASE_ID plus local ids or globally unique ids; cross-case references must mechanically fail. This should be a Phase 0 assertion-schema requirement.

## 12. Source/paste layout is an architectural dependency with no control owner

Architecture says source-span design depends on actual Doximity paste layout preserving usable boundaries.

Phase 0 has no authority for source-package version, paste-layout version, delimiter contract, label robustness, source-order perturbation, or unlabeled inputs.

Required: register a PASTE/INGESTION FIXTURE FAMILY with canonical layout and controlled perturbations.

## 13. Source-order bias / authority leakage is not directly tested

Source order is organizational, not authority.

Need fixtures where source families are reordered while semantic expectations remain stable, except where chronology itself is clinically meaningful.

## 14. Contradictory source facts are not a first-class regression class

What happens when source materials genuinely disagree?

Need conflict-preservation/adjudication fixtures ensuring distinct objects, maintained attribution, no false duplicate collapse, and current adoption only when supported.

## 15. Negation, uncertainty, attribution, and speaker preservation lack dedicated coverage

These are central to I3/I4.

Phase 0 should define coverage obligations for negation, hedging, speaker identity, reported vs examined, and current vs historical source.

## 16. The no-silent-source-loss invariant has no explicit coverage chain

Architecture requires no clinically meaningful source content silently disappears.

Need a first-class coverage chain:
SOURCE -> SPAN -> OBJECT -> USE/DISPOSITION -> UNIT -> OUTPUT

and earliest-missing-link localization.

## 17. No architecture-level seam contract coverage

Need a seam matrix for each producer->consumer pair:
- producer guarantees;
- consumer assumptions;
- mechanical compatibility check;
- semantic compatibility audit if needed;
- failure behavior.

The Phase 1.5 vertical slice tests one happy path only; it does not replace seam coverage.

## 18. R2 fallback behavior is not represented in Phase 0

Frozen guidance permits fallback to faithful unit-per-line output if safe prose composition cannot be maintained.

Need future assertions for when fallback is legal, how it is signaled, whether it affects acceptance, and whether repeated fallback indicates R2 design failure.

## 19. Production-shaped acceptance is not defined

Phase 5 requires production-shaped acceptance, but Phase 0 does not define production-shaped.

At minimum it should mean same compiled package, same paste layout, same one-call topology, no diagnostic telemetry, same final-note envelope, and same Doximity mode/settings.

## 20. No control for component-test instrumentation perturbation

Artifact-level tests such as I3-only or S4-only also change the output task.

Required evidence hierarchy:
1. component/artifact acceptance;
2. integrated one-call acceptance;
3. production-shaped final-note acceptance.

Local component success must not be presented as system reliability.

## 21. No corpus coverage ledger

Ten cases can still leave major gaps.

Need a coverage matrix across clinical domains, source types, failure classes, submodules, semantic primitives, section types, operator families, standing items, source contradictions, multi-problem reuse, and long-context stress.

Corpus sufficiency should be judged by coverage, not case count.

## 22. Scorer/auditor calibration is missing

How do we know ChatGPT and DeepSeek scorers are reliable?

Need periodic dual independent scoring, disagreement tracking, blind re-score of selected cases, adjudication, and scorer/model version identity.

## 23. Control-plane controls are not self-tested

Need meta-fixtures for BUILD, AUDIT, and CHANGE_CONTROL:
- known contradiction;
- compatible conditional pair;
- dangling reference;
- known-correct and known-bad audit artifact;
- missing-evidence audit;
- post-hoc discovery case;
- checker-code bugfix versus acceptance-check change;
- clinical baseline change;
- dependency invalidation.

## 24. No governance for changing the control plane itself

After Phase 0 freezes, what governs edits to CHANGE_CONTROL, BUILD_LINT, AUDIT_PROTOCOL, or fixture schema?

Need explicit control-plane-change governance, likely heightened DESIGN CHANGE:
- both LLMs review;
- signer approval for governance semantics;
- affected meta-tests rerun;
- file being changed cannot be sole authority for its own modification.

## 25. Control-plane version compatibility is missing

Acceptance evidence should record which Phase 0/control-plane version governed it.

After control-plane changes, dependent acceptance evidence must be selectively revalidated.

## 26. Raw evidence immutability is a principle without enforcement

GitHub files can be overwritten.

Need append-only raw-path convention and/or content hashes in experiment manifests. Hand-edited outputs must use separate path/status.

## 27. Baseline/reference versioning is missing

Need baseline id/version, source-package version, target-note version, assertion-set version, change reason/class, and no retroactive rescoring.

## 28. Normative absence vs missing data is not explicitly distinguished

Absent because source lacks it, extractor missed it, note intentionally omits it, it is unresolved, or stage failed must not collapse to the same null.

Phase 0 should require typed absence/failure semantics wherever absence changes interpretation.

## 29. Ordering-policy change risk is not separately governed

Ordering changes can be clinical/product, semantic chronology, implementation tie-breaker, or cosmetic.

Ordering assertions should declare which class they are because these changes require different governance.

## 30. No explicit authority hierarchy for source statements

Need to distinguish source actor and stance:
patient/family/prior clinician/current clinician, and whether current clinician adopts/rejects/does not address a prior statement.

This is not a heuristic such as transcript always wins. It is an audit coverage family preventing prior note from becoming current reasoning and reported finding from becoming examined finding.

## 31. No explicit acceptance rule for UNRESOLVED

When is UNRESOLVED acceptable?

Need per-field/per-stage policy for:
- allowed unresolved;
- escalation;
- note-safe representation;
- acceptance consequence.

## 32. No distinction between local artifact freeze and system readiness

Need lifecycle states distinguishing local acceptance, integration acceptance, Doximity replication, production-shaped acceptance, and frozen-for-dependents.

The missing status ledger should prevent frozen from meaning several different things.

## 33. Urgency classification

### Must resolve or register before Phase 1
1. implementation/status ledger;
2. architecture-invariant coverage matrix;
3. decision/authority registry;
4. control-plane self-change governance;
5. control-plane versioning;
6. failure-containment/propagation ownership;
7. seam contract matrix;
8. evidence/baseline/version authority;
9. active vs pending assertion dependencies;
10. minimum BUILD enforcement state;
11. change-history authority.

### Must be explicit Phase 1/1.5 prerequisites
12. ID namespace/stability/matching;
13. source/paste-layout versioning;
14. typed absence/unresolved semantics;
15. package compilation traceability;
16. canonical package order;
17. case namespace isolation;
18. source-coverage chain;
19. operator/normalization/standing-item dependencies;
20. vertical-slice seam tests.

### Must be mandatory later acceptance obligations, registered now
21. test-mode vs production-mode equivalence;
22. component-test vs integrated-one-call transfer;
23. production-shaped acceptance definition;
24. one-call resource/output budget;
25. model/mode/environment fingerprint;
26. source-order bias tests;
27. contradictory-source fixtures;
28. semantic fidelity primitive coverage;
29. corpus coverage ledger;
30. scorer/auditor calibration;
31. control-plane meta-tests;
32. raw-evidence immutability mechanism;
33. R2 fallback testing;
34. ordering-policy regression;
35. unresolved-ambiguity acceptance policy.

## 34. Conceptual Phase 0 authority shape

A mature control plane likely needs authorities for:
1. STATE / MANIFEST;
2. DECISION / CONTRACT AUTHORITY;
3. ACCEPTANCE;
4. FIXTURE / BASELINE;
5. BUILD;
6. AUDIT / CHECK;
7. CHANGE CONTROL;
8. EXPERIMENT;
9. COVERAGE.

This does not mean nine giant files. It means nine kinds of authority that cannot be missing.

## 35. Requested DeepSeek response

Before editing Phase 0, compare this architecture-gap audit against the 021 line-by-line reviews.

For each numbered blind spot classify:
- ALREADY COVERED — cite exact current control;
- PHASE 0 GAP — state proposed authority;
- DOWNSTREAM DEPENDENCY — name owner/phase and how Phase 0 records it now;
- REJECT — cite frozen architecture/evidence.

Do not solve downstream schema questions prematurely merely because Phase 0 needs to remember them.

Phase 0's job is to make missing obligations impossible to forget, not to implement every future contract now.
