# ChatGPT review 058 — ten-question architecture red-team adjudication

## Input reviewed

Independent attachment/report:
> **Architecture review — the ten questions**

I reconciled the ten claims against the current canonical architecture, interfaces, experiment program, current Gate 0 artifacts, and prior production evidence.

## Overall verdict

> **ARCHITECTURE SHAPE RETAINED, BUT INTERFACE CONSENSUS IS NARROWLY REOPENED.**

The report's top-line conclusion — "coherent in shape, not yet justified" — is directionally correct, but it mixes four different categories:

1. genuine interface/observability defects;
2. experiment-spec or validation-order gaps;
3. product decisions that were prematurely treated as invariants;
4. risks already explicitly acknowledged by the current experiment program.

Do **not** discard the INGEST → STRUCTURE → RENDER architecture.

Do **not** continue to describe the interface layer as fully CLOSED / CONVERGED, either.

A controlled design change should be drafted before scorer implementation or architecture experiment execution.

DC-001 remains historically valid; this is new evidence after DC-001.

---

# Q1 — S1↔S2 dependency direction

## Review claim
S2 has a veto over S1 candidacy without owning candidacy; cross-candidate equivalence/nesting has no owner; differential cases expose the gap.

## Adjudication
**PARTIALLY ACCEPTED. TERMINOLOGY/INTERFACE CLARIFICATION REQUIRED; CROSS-PROBLEM RELATION DEFECT NOT YET PROVEN.**

The report reads "candidate" as **problem candidate** in places where the architecture has two distinct concepts:

- S1 problem candidate;
- candidate claim formulations within that problem.

The current interface already gives S1 the problem-identity question:
> which neurologic subjects need their own assessment question?

S2 then adjudicates relations among that problem's candidate claims.

Therefore a differential such as:
> epileptic vs functional seizures

need not become two problem candidates. It can be:
- one problem candidate (events/spells/seizures);
- multiple candidate claims;
- S2 relation = competing/unresolved.

That preserves the intended authority split.

### Real defect
Consensus item 28 says:
> "A claim is a representation that may carry several candidates and their relation"

which is ambiguous enough to support the independent reviewer's interpretation.

The interface should explicitly say:
> a claim representation may carry several **candidate claims within one S1 problem candidate** and their S2-adjudicated relation.

If we actually intend one representation to span several S1 problem candidates, then the reviewer is correct and S2 needs an explicit cross-problem-candidate relation. We should not leave this ambiguous.

### S2 "veto"
This is not inherently an authority duplication.

S1 candidacy is provisional:
- "this subject needs its own assessment question."

S2 approval is a separate safety gate:
- "this claim representation is semantically defensible."

S3 rendering requires both.

That is coherent **if non-rendered candidates are explicitly accounted for**, which leads to Q3.

### `managed_today`
The reviewer correctly identifies an ambiguity.

If S1 salience includes `managed_today`, it must mean only a source-grounded cue such as:
> an explicit current management action is linked to this subject

and **not**:
> this historical diagnosis is currently adopted.

S2 still owns adoption.

If that distinction cannot be made operationally, remove `managed_today` from S1 salience.

### Required action
1. clarify problem candidate vs candidate claim terminology;
2. state explicitly that S1 problem identity is provisional but owned by S1;
3. define `managed_today` as a source-grounded cue or remove it;
4. build CASE-05/06 before claiming the seam works.

No cross-candidate S2 relation should be added unless CASE-05/06 demonstrates that one S1 problem candidate + multiple candidate claims is insufficient.

---

# Q2 — I3 object-boundary stability

## Review claim
"Independently useful proposition" is circular; AX-I3 can pass a stable but wrong granularity; no test asks whether downstream unit construction can consume I3 objects without re-splitting/merging.

## Adjudication
**ACCEPTED AS A REAL CONTRACT + EXPERIMENT GAP. NOT YET A TOPOLOGY DEFECT.**

AX-I3 currently tests:
- coverage;
- merge/split agreement;
- qualifiers;
- anchors;
- cross-run semantic identity.

That is not enough if every run makes the same wrong decomposition.

## Required action

### Operational I3 granularity rule
Freeze a conservative extraction rule, for example:

> one object per clause-level clinical proposition; split coordinated propositions when they can differ independently in truth, temporality, negation, condition, attribution, role, or downstream use; keep qualifiers with the proposition they qualify unless independently meaningful.

This remains a source-semantic rule, not a note-routing rule.

### Add a downstream-constructibility dimension to AX-I3
For the frozen object set:

> can a downstream unit constructor build the required valid units **without mutating, splitting, or merging I3 objects**?

If not, the object boundary is not actually usable even if stable.

This can be scored with a fixed downstream target/constructor and does not require reopening the topology immediately.

### I1/I2
The report says layout is untested. That is only partly current.

The program already has a mandatory paste-layout/I1-I2 characterization prerequisite.

Keep it explicit; do not pretend AX-I3 covers it.

---

# Q3 — one-way S2→S3→S4 flow and silent candidate loss

## Review claim
Objects have dispositions, but problem candidates do not. A clinically important S1 candidate can disappear before S4 with no explicit accounting event.

## Adjudication
**ACCEPTED — GENUINE ARCHITECTURE OBSERVABILITY DEFECT.**

The current interface gives:
- object dispositions;
- rendered problem set;
- S2 no-approved-representation state.

But it does not require every S1 candidate to receive an explicit S3 outcome.

That leaves an auditability/silent-loss hole.

## Required design change

S3 should output **candidate disposition/accounting** for every S1 problem candidate.

Minimum semantics:

- `RENDERED`
- `NOT_RENDERED` with structured reason/state

Example reasons may include:
- no S2-approved representation;
- context/evidence only after adjudication;
- intentionally deferred/not independently assessed;
- duplicate/equivalent candidate collapsed under an explicitly owned rule.

Exact vocabulary is downstream.

### New invariant

> Every S1 problem candidate is either rendered exactly once or carries an explicit non-render disposition.

### New mechanical/hybrid predicate

> S1 candidate set = S3 rendered candidates ∪ S3 candidate dispositions, with no silent remainder.

This does not create backtracking and does not give S4 source access.

---

# Q4 — S4 complexity / decision concentration

## Review claim
S4 owns too many decisions; final ordering has no oracle; known production grouping failure is already an S4-type failure.

## Adjudication
**PARTIALLY ACCEPTED. NO SPLIT YET.**

The known grouping failure is real evidence that S4-type work is high risk.

But AX-S4 was deliberately designed to score each S4 family independently and to split S4 only if distinct recurrent failure supports a separate seam.

The reviewer's statement:
> "all families read the same IR, so they fail together"

is a hypothesis, not yet evidence.

## Required action

1. **Freeze the ordering contract before scoring S4 order.**
   `S4-ORD-01` correctly remains pending until that exists.
2. Prioritize grouping/member-role/operator cases because old production evidence already showed grouping instability.
3. If S4 drifts, analyze per decision family before changing topology.
4. Factorial/ablation arms that remove one S4 decision family are optional localization follow-ups, not a prerequisite to the first S4 experiment.

Do not split S4 merely from complexity count.

---

# Q5 — R2 expressivity

## Review claim
"join adjacent units" versus "do not merge into a new proposition" is not operational; no prose-HPI baseline exists.

## Adjudication
**PARTIALLY ACCEPTED — BOUNDARY NEEDS AN OPERATIONAL TEST AND AX-R2 NEEDS REAL PROSE TARGETS.**

The conceptual boundary is still useful:
- R2 may compose;
- R2 may not invent semantic relations.

But "join" versus "merge" needs a testable criterion.

## Required clarification

Use a reversibility criterion:

> R2 composition is allowed only when the output can be decomposed at clause boundaries back to the same ordered unit meanings without adding, deleting, re-scoping, or changing temporal/causal/contrast/attribution relations.

This is not perfect mechanization, but it is an observable semantic criterion.

## Corpus dependency

AX-R2 already requires 5–10 realistic signer-quality HPI/history targets.

The current four stored baselines are not sufficient for this.

Therefore:
> AX-R2 remains blocked until actual prose-section targets are supplied/frozen.

Do not use A/P notes as the HPI oracle.

---

# Q6 — shared-context / authority-boundary leakage inside one call

## Review claim
Field-level prohibition can be bypassed by encoding a forbidden decision in allowed prose; S4 sees enough S2 relationships to re-decide; all boundaries are logical inside one model context.

## Adjudication
**ACCEPTED AS A MAJOR ARCHITECTURE RISK. PARTLY A DESIGN HARDENING ISSUE, PARTLY A MISSING EXPERIMENT ARM.**

This is the most important new challenge in the report.

AX-LEAK currently tests:
> raw source → RENDER leakage

It does **not** test:
> upstream logical owner → downstream logical owner authority leakage through semantically loaded allowed fields.

Examples:
- S1 subject text smuggles adoption/final-state judgment;
- S4 receives unneeded alternative semantic relations and re-picks what S3 selected.

## Required design hardening — least privilege

S4 should not receive the unrestricted S2 relation universe.

S4 should receive only:
- S3-selected representation for each rendered A/P problem;
- retained objects/problem-use map;
- the subset of adjudicated relations required to compile those retained objects/selected representations into units.

It should not receive unselected alternative claim relations merely because S2 produced them.

Exact projection schema is downstream.

## Required experiment extension

Do **not** add a ninth experiment.

Extend AX-S1S2-D and/or AX-LEAK with semantic leakage probes such as:

1. forbidden adoption/final-state judgment encoded in an otherwise allowed S1 text field;
2. alternative S2 representation/relation visible downstream but not selected by S3;
3. tempting relation on a retained object that S4 must not use to change the selected claim;
4. control where the same allowed field is source-faithful and non-decisional.

The scored question is:
> does the downstream artifact follow the owner's explicit decision fields/refs, or is authority reconstructed from prose/context?

Until this passes, "one decision has one owner" is a logical design rule, not a demonstrated runtime property.

---

# Q7 — IR size and attention cost

## Review claim
One-call IR/accounting adds burden; no budget is named; "derive bookkeeping mechanically" is not available inside the model call.

## Adjudication
**PARTIALLY ACCEPTED. RISK ALREADY OWNED BY AX-SCALE; REPRESENTATION CAN BE SIMPLIFIED NOW.**

AX-SCALE already separates:
- source size;
- span count;
- object count;
- IR/accounting size;
- document count;
- transcript length;
- batch size;
- telemetry burden.

So the architecture is not blind to this risk.

The reviewer is correct about one thing:

> self-reported totals/completeness labels are weak evidence and consume output budget.

## Required simplification

Prefer the Case IR to contain the actual:
- objects;
- uses;
- dispositions;
- units;
- refs;

while external CHECK recomputes:
- counts;
- completeness;
- accounting totals.

Do not require the model to emit redundant self-attested `ACCOUNTING: 60/60`-style totals.

### Budget
Do not invent a token threshold before measuring Doximity.

AX-SCALE should record actual:
- input size;
- output size;
- object/span/unit counts;
- truncation/completeness behavior.

A deployment budget can then be frozen from observed usable limits and realistic case distribution.

---

# Q8 — AX-T observer effect is positioned too late

## Review claim
If requesting Case IR changes behavior, test-mode evidence from all other experiments may not transfer to production. Therefore AX-T is a validity precondition.

## Adjudication
**ACCEPTED — PROGRAM-LEVEL VALIDATION DEFECT.**

AX-T need not physically run before every diagnostic/component experiment.

But:

> **No test-mode experiment may support a production-transfer claim until AX-T passes under the relevant package/artifact condition.**

That needs to be explicit in the program.

## Required program change

Classify AX-T as a **production-transfer gate**.

Allowed before AX-T:
- diagnostic/component evidence about the test-mode system;
- architecture localization.

Not allowed before AX-T:
- claiming the same reliability applies to final-note-only production.

If AX-T fails:
- test-mode artifacts remain useful for diagnosis;
- production acceptance must use final-note-only evidence.

No ninth experiment is needed.

---

# Q9 — one-problem-per-unit / shared-action render policy

## Review claim
AX-SHARED pre-decides that a shared action renders exactly once; that is a product/clinical communication choice, not an architecture invariant.

## Adjudication
**ACCEPTED — PRODUCT DECISION WAS PREMATURELY FROZEN.**

The architecture invariant is:
> one A/P unit has one owner.

That does **not** logically require:
> a shared action's text may appear only once in the note.

Those are separate questions.

The current AX-SHARED spec pre-freezes "shared action renders exactly once."

That should be reopened until the signer/user chooses the preferred note behavior.

## Product choices to present to signer

Possible policies include:

### A. One full action + secondary cross-reference
- full order/action appears once under primary owner;
- secondary problem may contain a terse non-duplicative cross-reference when clinically material.

### B. Duplicate action in both problem plans
- maximizes local completeness;
- risks duplicate orders and inconsistency.

### C. Single shared-plan location
- avoids duplication;
- conflicts with the current one-block-per-problem note style unless explicitly adopted.

A is the strongest default candidate for this note style, but it is **not frozen without signer approval**.

## Operator/schema consequence

Whichever product rule is chosen, the representation/operator vocabulary must be able to preserve:
- primary owner;
- secondary indication(s);
- distinct clinically material rationales;
- optional cross-reference behavior.

Do not treat "exactly once" as an architecture invariant until the user decides.

---

# Q10 — do canonical operators justify the surrounding architecture?

## Review claim
108/108 proves render execution, not upstream selection/grouping. Operators can make a wrong plan reproducible. The currently demonstrated value is auditability more than semantic reproducibility.

## Adjudication
**ACCEPTED AS AN EVIDENCE-FRAMING CORRECTION, NOT AN ARGUMENT TO DISCARD THE ARCHITECTURE.**

The canonical documents already say:
> architecture is not empirically validated.

The operator evidence supports:
- well-formed/invalid render-boundary behavior;
- stable canonical realization under the tested condition.

It does **not** establish:
- object decomposition;
- problem selection;
- claim selection;
- unit grouping;
- operator selection;
- end-to-end reproducibility.

## Correct current evidence statement

> **Demonstrated:** canonical rendering boundary + auditability of explicit decisions.  
> **Hypothesized / unvalidated:** reproducibility of the semantic decisions that populate the IR.

That distinction should appear in architecture status language.

## E1 reconciliation

The architecture still contains the original E1:
> fixed raw paste → Case IR reproducibility, with render-unit/operator agreement primary.

The later eight-experiment program decomposed the failure modes but never clearly retired or positioned E1.

Do not add E1 as a ninth architecture experiment.

Instead make one cheap **program-level integrated preflight** after Gate 0:
- one fixed representative raw paste;
- three fresh runs;
- compare object coverage, problem set, selected representation, unit membership, operator selection, order.

Purpose:
> detect catastrophic whole-chain instability early and localize which component experiment should be prioritized.

It is a screening run, not independent acceptance evidence and not a ninth architecture experiment.

The later integrated end-to-end campaign remains required for whole-system acceptance.

---

# Architecture consequence

The independent review is strong enough that the prior state:

> ARCHITECTURE INTERFACE LAYER — CLOSED / CONVERGED

should no longer be used without qualification.

## New state

> **ARCHITECTURE SHAPE — RETAINED**  
> **INTERFACE CONSENSUS — NARROWLY REOPENED FOR CONTROLLED DESIGN CHANGE**

The controlled change should address:

### Interface changes
1. problem-candidate vs candidate-claim terminology / provisionality clarification;
2. S3 candidate dispositions + candidate completeness invariant;
3. S4 least-privilege semantic input projection;
4. R2 reversible/non-semantic composition criterion.

### Experiment/program changes
5. I3 operational granularity + downstream constructibility dimension;
6. semantic authority-leak probes;
7. AX-T as production-transfer gate;
8. early integrated E1-style preflight, not a ninth experiment;
9. remove redundant self-attested IR totals/completeness fields where external CHECK can derive them.

### Product decision
10. shared-action final-note render/cross-reference policy must be decided by the signer before AX-SHARED freezes required behavior.

### Dependencies
11. freeze S4 ordering contract before scoring order;
12. obtain/freeze actual signer-quality HPI/history targets before AX-R2.

---

# Gate 0 consequence

Recent post-057 work materially improved Gate 0:

- S4-REP-01 reactivated;
- active state now 14 predicates / 16 seeds;
- harmless variation artifact now exists;
- governing source hashes now exist;
- scorer blindness is explicit;
- predicate-level finding schema exists;
- predicate-mode calibration authority is mostly corrected.

Minor stale prose remains, but **do not spend another cycle polishing Gate 0 right now**.

The new architecture review may change:
- predicate definitions;
- active set;
- candidate accounting;
- S4 input contract.

Therefore:

> **PAUSE SCORER IMPLEMENTATION AND GATE 0 EXECUTION UNTIL THE controlled architecture change is resolved.**

Do not throw away the Gate 0 work; it is reusable after the affected predicates/schema are regenerated.

---

# Requested DeepSeek response

Do not edit consensus yet.

Please respond to this review point-by-point, especially:

1. Does "candidate" in consensus item 28 mean S1 problem candidate or candidate claim?
2. Is candidate disposition necessary, or can you prove existing S1/S2/S3 artifacts mechanically account for every non-rendered candidate and reason?
3. What is the minimum S2-derived relation projection S4 actually needs?
4. Can the R2 join/merge boundary be made testable without moving discourse synthesis upstream?
5. Do you agree AX-T must gate production-transfer claims?
6. Do you agree AX-SHARED's "render exactly once" requires signer approval?
7. Is the E1-style integrated preflight redundant with an existing executable arm, or should it remain a program-level screen?

Return a proposed minimal DC-002 only after resolving those disagreements.

No Phase 0.
No scorer implementation yet.
No Doximity architecture run yet.
