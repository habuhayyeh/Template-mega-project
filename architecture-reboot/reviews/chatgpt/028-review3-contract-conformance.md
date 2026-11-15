# ChatGPT review 028 — Review 3: Contract-Conformance Review

## Status

**Review 1: CLOSED.**  
**Review 2: CLOSED.**

This is **Review 3: Contract-Conformance Review**.

It asks only:

> Does Phase 0 conform to the already-frozen architecture, submodule interfaces, implementation guidance, two-LLM workflow, and Doximity experimental protocol?

This review is intentionally different from Reviews 1–2.

- Review 1 asked whether the right authorities exist.
- Review 2 asked who is canonical when authorities overlap.
- Review 3 asks whether Phase 0 is trying to **change upstream design without reopening it**.

Because the current Phase 0 files are still the pre-rewrite versions, some findings are already expected to disappear during the agreed rewrite. They are still listed because the rewrite must not carry them forward.

---

# Classification

Each finding is one of:

## CONFLICT
Phase 0 contradicts an already-frozen rule.

## UNAUTHORIZED EXTENSION
Phase 0 adds a semantic/runtime rule not frozen upstream.

## PREMATURE FREEZE
Phase 0 treats a downstream-open schema/operator/normalization/failure decision as already settled.

## CONFORMANCE GAP
The frozen upstream rule exists, but Phase 0 lacks enough representation to enforce it safely.

---

# Executive verdict

**Phase 0 is not yet contract-conformant.**

The most serious direct conflicts are:

1. F-11 conflates historical provenance with current plan eligibility, directly violating the frozen temporality/adoption separation.
2. BUILD_LINT still excludes normative prose unless encoded as rule records, conflicting with frozen PROSE_POLICY.
3. registry order scope currently permits RENDER authority over S4-owned ordering.
4. AUDIT overstates mechanical Case-IR→note proof and forbids expected prose even where canonical operator wording is contractual.
5. diagnostic/test-mode acceptance is not protected from the frozen rule that diagnostic trace runs can never satisfy acceptance.
6. CHANGE_CONTROL's DESIGN CHANGE definition is narrower than the frozen workflow.
7. O-21 incorrectly limits reproducibility claims to the mechanical subset, contradicting the semantic-audit protocol.
8. O-06 demands package-order invariance even though the frozen Doximity protocol treats order/position as an empirical robustness variable.
9. several obligations/fixtures freeze exact behavior the architecture explicitly left open: failure containment, literal cross-run IDs, paste-order invariance, operator cardinality, normalization, standing-item triggers.

---

# A. Direct conflicts with frozen architecture

## A1 — F-11b/F-11c violate source-temporality vs current-adoption separation

Current fixture:

> A-11b — a `HISTORICAL` object does not appear in a plan unit.

> A-11c — a plan unit's members are all `CURRENT` or `PROPOSED`.

Frozen architecture:

> Source history and current clinical adoption are separate dimensions.

and:

> A historical diagnosis/recommendation can be historical and currently adopted.

and:

> This rule applies to both REASONING and PLAN.

Therefore the current F-11 assertions are not merely imperfect; they enforce the opposite of the frozen design.

### Correct seam decomposition

The historical failure should be represented approximately as:

- **I4/source metadata:** provenance/source temporality remains historical;
- **S2:** `current_adoption` is false unless current encounter evidence adopts it;
- **S3:** a historical recommendation with current_adoption=false is not selected as today's current plan;
- if current_adoption=true, the same historical-source object **may** legitimately contribute to today's plan.

Do not use source temporality as a plan-exclusion rule.

**Class:** CONFLICT.  
**Rewrite blocker:** YES.

---

## A2 — BUILD_LINT still conflicts with frozen PROSE_POLICY

Current BUILD says:

> A statement not written as a rule record is documentation, and documentation is not compiled.

Frozen implementation guidance explicitly preserves:

- LLM_JUDGMENT;
- PROSE_POLICY;
- TYPED_DSL;
- CANONICAL_OPERATOR;
- MECHANICAL_RULE.

Semantic/contextual rules may intentionally remain authoritative prose.

Review 021 already identified this; Review 2 supplied the authority fix.

### Contract-conformant form

A structured rule record may carry:
- decision id;
- applicability;
- payload_ref;
- assertion refs;

while `payload_ref` resolves to authoritative prose where PROSE_POLICY is the correct control mode.

BUILD validates reference/integrity; it does not erase prose authority.

**Class:** CONFLICT.  
**Rewrite blocker:** YES.

---

## A3 — current order authority leaks into RENDER

Current registry seed:

> AP_ORDER_WITHIN_PROBLEM — owner S4 — allowed scopes: RENDER, STRUCTURE.

Frozen guidance:

> ordering is governed by one centralized structured ordering contract;

> S4 writes the resulting order into the Case IR;

> RENDER may not recalculate it.

Therefore a RENDER rule may be obligated to **preserve** order, but must not be authorized to decide `AP_ORDER_WITHIN_PROBLEM`.

Review 2's `authority_scope` vs `obligated_scopes` distinction is required for conformance.

**Class:** CONFLICT in current representation.  
**Rewrite blocker:** YES.

---

## A4 — `COVERAGE_DISPOSITION -> S3` is too broad for the frozen interfaces

Current registry seed assigns:

> COVERAGE_DISPOSITION → S3.

But frozen interfaces distinguish:

- I2/I3 span coverage/accounting;
- S3 clinical-object use/disposition.

Every source span must be accounted for, while every clinical object must be used or dispositioned.

One global decision called `COVERAGE_DISPOSITION` assigned to S3 collapses these distinct authorities.

### Required

Split at least conceptually:

- span/source-fragment accounting → INGEST seam;
- clinical-object note-use/disposition → S3.

Exact decision IDs can wait for rewrite.

**Class:** CONFLICT / authority collapse.  
**Rewrite blocker:** YES.

---

# B. CHECK/AUDIT conformance

## B1 — AUDIT overstates what mechanical CHECK can prove

Current AUDIT:

> The mechanical checker can prove the note matches the Case IR.

Frozen workflow and interfaces are narrower.

For R2 prose composition:
- mechanical order/coverage checks can prove structural preservation;
- semantic-preservation audit may still be required where meaning equivalence is not mechanically decidable.

Therefore:

> "CHECK proves note matches Case IR"

is too broad.

### Correct framing

CHECK proves the **declared mechanically decidable conformance predicates** at a seam.

AUDIT handles semantic predicates that remain non-mechanical.

**Class:** CONFLICT by overclaim.  
**Rewrite blocker:** YES.

---

## B2 — "never expected prose" conflicts with canonical fixed wording

Current AUDIT Mode A says:

> fixture assertions — properties only, never expected prose.

The architecture makes canonical operators first-class and allows:
- fixed wording elements;
- operator-fixed text;
- section-scoped style rules.

When exact or bounded wording is itself contractual, expected prose/text may be the property under test.

The default should still be property-based, but **never** is wrong.

### Correct rule

Expected exact/bounded wording is excluded by default **except when wording itself is a frozen operator/style property**.

**Class:** CONFLICT by overrestriction.  
**Rewrite blocker:** YES.

---

## B3 — AUDIT escalation to signer is too broad

Current:

> When the reviewer cannot decide, escalate to the signer.

Frozen workflow assigns the signer:
- clinical/product authority;
- unresolved genuine product/clinical choices.

Engineering ambiguity should first be resolved through:
- frozen contract;
- independent review;
- existing evidence.

The signer should not become the universal fallback for technical ambiguity.

**Class:** CONFLICT with role division.  
**Rewrite blocker:** YES.

---

## B4 — diagnostic trace acceptance is not structurally prevented

Frozen Doximity protocol:

> diagnostic single-case trace is diagnostic only and can never satisfy an acceptance criterion.

Current Phase 0:
- packet has only `mode: PRODUCTION | TEST`;
- AUDIT says either mode may sign acceptance if assertions are decidable.

Those concepts are not equivalent.

A TEST artifact could be:
- ordinary artifact-level test output;
- diagnostic trace.

The latter is forbidden as acceptance evidence.

### Required

EXPERIMENT_MANIFEST / packet relation must encode run type distinctly, e.g.:
- artifact batch;
- replicated batch;
- diagnostic trace;
- robustness.

A packet belonging to a diagnostic-trace experiment must be **ineligible for acceptance**, regardless of audit answerability.

This is a frozen protocol gate, not auditor discretion.

**Class:** CONFORMANCE GAP with safety consequence.  
**Rewrite blocker:** YES.

---

# C. Acceptance packet / experiment conformance

## C1 — "packet is the unit of acceptance" is too strong

Current PACKET:

> The unit of acceptance is the packet.

Frozen protocol requires higher-level gates:
- repeated same-order batches;
- scorer integrity;
- robustness where applicable;
- experiment-level relationships.

A single case/run packet can be valid evidence without being sufficient to accept the artifact/system.

### Better statement

> The packet is the atomic unit of **scored run evidence**.

Experiment-level acceptance is determined from the relevant packet set under the frozen experimental protocol.

This is exactly why Review 1 required EXPERIMENT_MANIFEST.

**Class:** CONFLICT with experiment-level acceptance model.  
**Rewrite blocker:** YES.

---

## C2 — production packet example assumes Case IR exists

Current packet example:

```
mode: PRODUCTION
required_evidence: [source_package, case_ir, note]
```

Frozen architecture says production may suppress/hide Case IR.

Therefore a production acceptance packet cannot universally require a visible Case IR.

Evidence requirements must come from:
- predicate prerequisites;
- experiment/run type.

A diagnostic/test artifact may expose IR; production-shaped acceptance may not.

**Class:** PREMATURE/overbroad schema assumption.  
**Rewrite blocker:** YES.

---

## C3 — DISCOVERY should not be a verdict

Current packet allows:

> verdict = ACCEPT | REJECT | BLOCKED | DISCOVERY

but also says:

> DISCOVERY is not scored.

A discovery is a **finding**, not the acceptance verdict of the run.

A run can:
- REJECT and contain a discovery;
- BLOCK and contain a discovery;
- potentially ACCEPT its frozen predicates while also surfacing an unscored discovery that then blocks promotion pending governance, depending on final policy.

Do not collapse finding type and verdict type.

This is not explicitly frozen upstream, but the current representation is incompatible with the frozen "predefined assertions score the run" principle.

**Class:** CONFORMANCE GAP / type conflation.

---

# D. Runtime fixture conformance

## D1 — A-02a silently narrows explicit reuse

Current:

> an object id appears in at most one unit per (section, problem).

Frozen consensus:

> the same object may be reused explicitly by multiple render units/problems.

The frozen architecture does not state a same-section/same-problem uniqueness prohibition.

Therefore A-02a may be a sensible downstream duplicate-control rule, but it is **not authorized yet**.

If desired, prove/ratify it as a new invariant or replace it with:

> repeated use must be explicitly represented in reuse accounting and must not produce an unapproved duplicate proposition.

**Class:** UNAUTHORIZED EXTENSION.  
**Rewrite blocker:** YES unless upstream ratified.

---

## D2 — A-02b is too broad for explicit reuse

Current:

> two objects asserting the same proposition do not both render.

That is too broad across:
- different problems;
- different sections;
- different rhetorical uses.

The historical defect was duplicate rendering within one problem/use-context.

The assertion must be scoped to:
- adjudicated duplicate relation;
- intended use-context;
- explicit reuse policy.

**Class:** UNAUTHORIZED NARROWING.  
**Rewrite blocker:** YES.

---

## D3 — A-01a freezes lexical normalization before its contract exists

Current:

> no object's content token is absent from its span.

The frozen implementation guidance says:
- lexical normalization must be conservative;
- exact normalization/abbreviation/synonym tables remain downstream.

So the predicate may eventually be mechanical, but **not until its normalization dependency exists**.

It must be PENDING_DEPENDENCY rather than ACTIVE/mechanical now.

Also, lexical containment alone does not prove semantic non-fabrication.

**Class:** PREMATURE FREEZE.

---

## D4 — A-01c depends on unfrozen transformation/operator tables

Current R1 assertion permits:

> object payload + operator text + transformation table.

Those authorities are downstream-open.

So this is a future mechanical predicate with prerequisites, not an immediately executable Phase 0 oracle.

**Class:** PREMATURE FREEZE.

---

## D5 — A-06b depends on an unfrozen standing-item contract

Current:

> when the trigger is satisfied, the unit exists.

The architecture freezes only the **shape** of the S4 exception:
- closed-list standing item;
- explicit trigger satisfied.

The actual standing-item catalog/trigger schema remains downstream.

A-06b is valid in principle but must be PENDING_DEPENDENCY until the standing-item contract exists.

**Class:** PREMATURE FREEZE.

---

## D6 — A-07a / C12 role completeness depend on unfrozen operator registry

Current assertions require:
- typechecking unit against operator;
- required semantic roles present.

The exact operator vocabulary/role schemas remain downstream.

These should be registered as future predicates with explicit operator-registry prerequisites.

**Class:** PREMATURE FREEZE.

---

## D7 — F-07b silently chooses whole-run failure containment

Current:

> malformed unit yields CONTRACT_ERROR and the run fails.

Frozen architecture says malformed/underspecified units fail closed, but does **not** yet define:
- unit-level;
- problem-level;
- note-level;
- batch-level containment.

Phase 0 cannot choose "the run fails" unless upstream failure-containment policy is ratified.

**Class:** UNAUTHORIZED EXTENSION.

---

## D8 — F-14a freezes conditional operator cardinality before operator contract

Current:

> a plan unit with CONDITION member produces one line, not two.

The historical apixaban defect motivates this, but the exact canonical operator vocabulary/cardinality is still downstream.

The stronger currently frozen rule is:

> the condition relationship must remain attached to the action and must not be semantically lost/split incorrectly.

Exact one-line realization should be asserted once PLAN_CONDITIONAL/operator cardinality is frozen.

**Class:** PREMATURE FREEZE / unauthorized surface commitment.

---

# E. Failure-containment obligations are currently contradictory

## E1 — O-03 says only the bad line should fail

Current O-03:

> inject one malformed unit; assert only that line fails.

Current F-07b:

> malformed unit ... run fails.

These contradict each other.

More importantly, neither behavior is frozen upstream.

Architecture only says:
> malformed or underspecified render units fail closed.

### Required

COVERAGE_LEDGER should record:

> failure-containment scope is unresolved and must be decided before implementation that depends on it.

Do not put the expected containment answer in the obligation.

**Class:** INTERNAL CONTRADICTION + UNAUTHORIZED EXTENSION.

---

# F. Reproducibility / robustness contract conflicts

## F1 — O-06 incorrectly requires package-order insensitivity

Current:

> reordering files must not change output.

Frozen Doximity protocol explicitly treats:
- order/position as robustness variables;
- same-order repetitions must be characterized before order effects are attributed;
- non-local prompt sensitivity is empirical.

Therefore the correct requirement is **not**:
> arbitrary package reorder produces identical output.

It is:
- production build uses a canonical package order;
- changes in package order are versioned implementation changes;
- when order is experimentally varied, differences are measured under the robustness protocol.

Demanding order-insensitivity is an invented reliability property the LLM may not possess.

**Class:** CONFLICT with frozen experimental framing.

---

## F2 — O-10 overstates paste/source-order invariance

Current:

> output must not depend on where a fact was pasted.

The concrete paste-layout/provenance contract is explicitly still open.

And some ordering may legitimately encode:
- source grouping;
- chronology;
- explicit labels/context.

What we want is not total order independence.

We want:
> semantically equivalent reorderings that preserve contracted source identity/chronology must not create unauthorized authority or semantic changes.

The experiment should characterize position bias, not presuppose exact output invariance.

**Class:** PREMATURE FREEZE / overbroad robustness claim.

---

## F3 — O-01 requires "IR identical except trace block"

Current closing test:

> same case, both modes, IR identical except the trace block.

Production may suppress IR entirely.

The frozen requirement is behavioral:
> test-mode instrumentation must not materially change note-relevant decisions.

Exact IR byte/identity equivalence is not yet a ratified invariant and may not even be observable in production mode.

Use paired semantic/output predicates, not literal hidden-IR identity.

**Class:** PREMATURE FREEZE.

---

## F4 — O-02 seam probe is logically wrong

Current:

> change one module's input, assert no other module's output changes.

The architecture is a dependency graph.

If S2 input changes legitimately, S3/S4 output **should** sometimes change.

The seam invariant is:
- downstream may depend only on the declared upstream artifact;
- downstream must not use forbidden context to repair/reinterpret;
- irrelevant/non-consumed perturbations should not alter behavior.

A correct probe might:
- hold the seam artifact fixed while varying forbidden raw context;
- perturb an irrelevant field and assert downstream invariance;
- perturb a declared input and assert only authorized dependent decisions change.

**Class:** CONFLICT with dependency architecture.

---

## F5 — O-08 freezes literal cross-run ID identity too early

Current:

> same object keeps the same id across runs.

The architecture freezes stable object identity, but exact ID schema/determinism remains downstream.

The E1 experiment must compare object identity, but whether that means:
- identical literal ID;
- deterministic source-derived key;
- semantic matching under a stable mapping;

has not been frozen.

Do not make literal set equality the oracle before the ID contract exists.

**Class:** PREMATURE FREEZE.

---

## F6 — O-21 incorrectly limits reproducibility to the mechanical subset

Current:

> Any reproducibility claim is scoped to the mechanical subset.

This directly conflicts with the frozen experimental protocol.

We intentionally measure semantic decisions across runs:
- problem model;
- adoption;
- duplicate identity;
- operator selection;
- condition attachment;

using SEMANTIC_AUDIT where necessary.

The correct limit is:

> mechanical reproducibility claims may be computed mechanically; semantic reproducibility claims require frozen semantic assertions and audit.

Do not erase semantic reproducibility simply because it is not deterministic checking.

**Class:** DIRECT CONFLICT.  
**Rewrite blocker:** YES.

---

# G. Open vocabularies frozen too early

## G1 — O-21 introduces `ABSENT_BY_CONTRACT`

The architecture explicitly says the exact closed disposition vocabulary remains to be finalized.

Current O-21 requires:

> UNDECIDABLE, DISCOVERY, ABSENT_BY_CONTRACT are distinct.

But these are not even the same conceptual layer:
- UNDECIDABLE = audit/evidence result;
- DISCOVERY = governance finding;
- ABSENT_BY_CONTRACT = proposed runtime/data-state concept.

Do not freeze `ABSENT_BY_CONTRACT` through Phase 0.

The real obligation is:

> missing, intentionally not used, unresolved, and invalid/failure states must not collapse into one indistinguishable absence.

Exact vocabulary belongs downstream.

**Class:** PREMATURE FREEZE + layer conflation.

---

# H. Corpus and experiment conformance

## H1 — "ten-note corpus covers each failure class" overfreezes case count and coverage unit

Current O-15:

> the ten-note corpus covers each failure class.

Frozen protocol says:
- start 3–5;
- escalate ~8–12 if stable;
- batch size is empirical;
- coverage matrix matters more than arbitrary count.

The signer may indeed supply ten reference cases, but Phase 0 should not make **ten** a normative completeness threshold.

Better:
> reference corpus covers the required architecture/failure dimensions; case count remains empirical.

**Class:** UNAUTHORIZED PROCESS NARROWING.

---

## H2 — one fixture per failure class is not sufficient coverage

Relatedly, the frozen protocol optimizes **assertions per artifact**, not merely failure-class presence.

Coverage should include:
- submodules/seams;
- semantic primitives;
- operator families;
- source types;
- high-risk historical regressions;
- long-context/batch position.

Failure class is one axis, not the whole oracle.

**Class:** CONFORMANCE GAP.

---

# I. Change-control conformance

## I1 — current DESIGN CHANGE definition is too narrow

Current:

> any change to architecture, submodule goal/interface, shared contract, or a decision that affects more than one module.

Frozen workflow defines DESIGN CHANGE more broadly:
- responsibility;
- semantic authority;
- function;
- input/output;
- frozen contract.

A semantic-authority change entirely inside one module can still be a DESIGN CHANGE.

Review 2 also established registry rows cannot move authority without upstream design change.

### Required rewrite

Classify by **semantic effect/authority**, not number of affected modules.

**Class:** CONFLICT with frozen workflow.

---

## I2 — signer approval for acceptance changes is too narrow

Current table requires signer approval when an acceptance change alters:

> a clinical baseline expectation.

But the signer is also the product/style authority.

A signer-approved:
- style baseline;
- output format/product preference;
- clinical baseline;

cannot be changed by reviewer-only approval.

### Required

Signer approval when an acceptance change alters a signer-approved **clinical, style, or product** baseline/property.

Pure engineering predicate corrections remain reviewer-controlled under evidence/change rules.

**Class:** CONFORMANCE GAP / role mismatch.

---

## I3 — current "original reviewer approves" is not a frozen role

Current requirement:

> explicit approval from the reviewer who wrote the original expectation.

Frozen workflow defines roles, not permanent identity of one historical session/agent.

Governance must survive agent replacement.

Use:
> current independent acceptance owner/reviewer, with signer where baseline authority requires.

**Class:** UNAUTHORIZED GOVERNANCE RULE.

---

# J. Acceptance-brief conformance

## J1 — F2 example silently defines runtime failure behavior

Current template example:

> F2 duplication → reject unit pair, fail closed.

That behavior is not frozen.

Duplicate identity is owned by S2; selection/use by S3; unit shape by S4.

The correct response to a detected duplicate depends on where the invalidity appears.

A template must not introduce new runtime policy through an example.

**Class:** UNAUTHORIZED EXTENSION.

---

## J2 — "never expected prose" / property-only brief must allow frozen wording properties

Same issue as AUDIT.

If operator-fixed wording or exact style token is contractual, the brief may reference that bounded wording property.

Do not turn anti-gold-prose discipline into a ban on testing canonical wording.

**Class:** CONFLICT by overrestriction.

---

# K. Implementation-manifest conformance

## K1 — current manifest granularity is too coarse for the frozen implementation workflow

Current manifest rows:

- INGEST;
- STRUCTURE;
- RENDER;
- CHECK;
- AUDIT;
- BUILD.

Frozen workflow implements and freezes:

- I1;
- I2;
- I3;
- I4;
- S1–S4;
- R1–R3;

one artifact at a time with independent review.

Therefore the manifest must be capable of representing **submodule-level artifacts**, shared contracts, checker implementations, and build/audit artifacts individually.

Module-level aggregate rows may be derived summaries.

**Class:** CONFORMANCE GAP.

---

## K2 — readiness must distinguish local acceptance from integration/system evidence

Frozen workflow:
- artifact-level acceptance;
- vertical slice;
- replicated Doximity testing;
- production-shaped acceptance.

A single generic `ACCEPTED` state is insufficient unless its evidence level is typed.

Review 022 already identified this.

Possible implementation:
- readiness state + acceptance_level;
- or evidence pointers describing local/integrated/production-shaped scope.

Do not let local I3 acceptance imply system readiness.

**Class:** CONFORMANCE GAP.

---

# L. Source-coverage conformance

## L1 — O-12's coverage wording should preserve both span and object accounting

Current:

> every span reaches a disposition or a line.

Frozen architecture is more precise:

- every span is represented/accounted;
- spans may yield multiple objects;
- every object points to a span;
- every clinical object is used or explicitly dispositioned.

A span need not itself "reach a line."

The contract-conformant chain is:

```
SOURCE
 -> SPAN (accounted)
 -> OBJECT(S) or span disposition
 -> OBJECT USE/DISPOSITION
 -> UNIT
 -> OUTPUT
```

The coverage checker should localize the first broken edge rather than flatten this to "disposition or line."

**Class:** CONFORMANCE NARROWING.

---

# M. Contradictory-source fixture obligation needs less prescriptive output

Current O-11 says conflicting notes should:

> assert both objects survive and adoption is explicit.

Preserving both source propositions may often be right, but the frozen architecture gives S2 authority to adjudicate semantic relationships.

The invariant should be:

- conflict/provenance must not be silently erased;
- attribution survives;
- any collapse/coverage/adjudication is explicit and source-grounded;
- current adoption is explicit where relevant.

Do not pre-decide that two separate renderable objects must always survive all later stages.

**Class:** UNAUTHORIZED EXTENSION.

---

# N. What already conforms and should not be reopened

Review 3 should not create churn where Phase 0 already matches upstream.

The following are directionally conformant:

1. one-call runtime architecture remains untouched;
2. no extra runtime module has been introduced;
3. CHECK/AUDIT/BUILD remain engineering support systems;
4. S2 duplicate/adoption authority, S3 selection/use, S4 blueprint/operator/order boundaries are preserved in the agreed Review 2 target;
5. canonical operator execution remains separate from operator selection;
6. test trace is recognized as observational, not hidden chain-of-thought;
7. historical regressions remain preferred fixtures;
8. derived fixtures are allowed only for uncovered invariants;
9. assertion changes are governed rather than silently edited;
10. raw outputs are intended to remain immutable evidence;
11. batch size remains empirical in the frozen protocol;
12. one-decision/one-owner remains preserved;
13. Review 2's predicate-kind split correctly preserves runtime first-divergence ownership without forcing BUILD/PROCESS into runtime submodules.

Do not reopen these without new evidence.

---

# O. Rewrite requirements from Review 3

The eventual Phase 0 rewrite must not carry forward these current rules:

1. historical object prohibited from current plan;
2. plan members restricted by source temporality rather than current adoption;
3. unreferenced prose automatically non-normative/never compiled;
4. RENDER authorized to make S4 ordering decisions;
5. one global S3 coverage-disposition decision;
6. CHECK claimed to prove all Case-IR→note semantic conformance;
7. expected prose categorically forbidden;
8. every unresolved audit question escalated directly to signer;
9. diagnostic trace potentially acceptable merely because its assertions are decidable;
10. packet treated as sufficient unit of overall acceptance;
11. production packet universally requiring Case IR;
12. DISCOVERY used as a verdict type;
13. same object prohibited from multiple units in one section/problem without upstream ratification;
14. same proposition categorically prohibited from rendering more than once without use-context;
15. lexical/operator/standing-item predicates marked executable before prerequisite contracts;
16. whole-run failure containment assumed for malformed unit;
17. one-line-only containment assumed elsewhere;
18. arbitrary package reorder required to be output-invariant;
19. arbitrary paste reorder required to be output-invariant;
20. test vs production required to have literally identical IR;
21. seam perturbation test requiring all other module outputs stay unchanged;
22. literal cross-run IDs required before ID contract;
23. reproducibility limited to mechanical subset;
24. `ABSENT_BY_CONTRACT` frozen before disposition vocabulary;
25. ten-case corpus treated as normative threshold;
26. DESIGN CHANGE limited partly by number of affected modules;
27. signer acceptance-change authority limited to clinical baseline only;
28. original historical reviewer required forever;
29. template examples defining duplicate failure handling;
30. manifest too coarse to represent I1–R3 artifact lifecycle;
31. local acceptance indistinguishable from integration/production-shaped acceptance;
32. source coverage flattened to span→line;
33. contradictory-source behavior forced to "both objects survive" rather than explicit source-faithful adjudication.

---

# P. Requested DeepSeek response

Do **not** rewrite Phase 0 yet.

For each item A1–M1 above, respond:

```text
ITEM
POSITION: ACCEPT | REJECT | PARTIAL | ALREADY FIXED BY REVIEW-2 TARGET
UPSTREAM CONTRACT:
WHY:
REWRITE CONSEQUENCE:
```

For any rejection:
- cite the exact frozen architecture/workflow/protocol statement that authorizes the current Phase 0 rule.

Important distinction:

> "Review 2 already plans to change this" is not a rejection.

Label it:
> ALREADY FIXED BY REVIEW-2 TARGET.

The purpose of Review 3 is to prove that the **target rewrite**, not just the current prose, will remain subordinate to the frozen upstream contracts.
