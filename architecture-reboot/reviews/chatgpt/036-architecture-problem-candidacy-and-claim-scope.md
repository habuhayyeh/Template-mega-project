# ChatGPT review 036 — Architecture: S1 problem-candidacy criterion and claim-representation scope

## Verdict

DeepSeek 029 converges on the refined S2/S3 claim boundary, but the interface-design portion of Review 4 is **not yet fully closed**.

Two architecture issues remain:

1. S1 still lacks its defining inclusion criterion: what makes a neurologic subject a real problem candidate rather than a passing mention or supporting fact?
2. The claim-representation **concept** is correct, but DeepSeek's example prematurely freezes schema/enums and a free-text rationale field that remain downstream.

There is also one failure-behavior correction:
> a problem with no approved claim representation must not "render without a claim" and wait for completeness to catch it.

---

# 1. Problem candidacy is an architecture question, not an experiment-only question

S1's unique question is now supposed to be:

> Which neurologic subjects/candidate problems are part of today's encounter-level reasoning?

Without a candidacy rule, S1 has no stable contract.

The architecture cannot be considered interface-complete while S1's inclusion boundary is undefined.

## The candidacy rule should be clinical-role based

A **problem candidate** is a source-grounded neurologic subject that warrants **independent encounter-level assessment organization** because at least one of the following is true:

1. it is the current neurologic complaint/reason for consult or a distinct current neurologic symptom/event being evaluated;
2. the current encounter contains independent neurologic reasoning, uncertainty, differential, or etiologic assessment about it;
3. the current encounter contains neurologic evaluation/monitoring/management specifically directed at it;
4. it is a known neurologic condition that is explicitly engaged in today's encounter sufficiently to require its own current assessment status.

This is not a mechanical checklist; these are semantic examples of the governing principle.

### Governing principle

> **Create a separate problem candidate only when the subject requires its own current neurologic assessment question/status.**

A subject that only:
- supports;
- refutes;
- contextualizes;
- explains;
- or modifies management of another neurologic problem

remains evidence/context for that problem unless it independently meets the criterion above.

This matches the signer's established note preference:
- neurological claims/problems organize the assessment;
- non-neurologic/contextual facts do not become separate problems merely because they are clinically relevant.

---

# 2. This rule handles the major edge cases

## Current symptom without diagnosis
> episodic unexplained jolts/energy phenomenon

Valid problem candidate:
- it is itself the neurologic question being evaluated.

No diagnosis is required.

## Family concern mentioned but explicitly not today's issue
Not a separate problem candidate unless the encounter independently assesses it.

It may remain HPI/context.

## Historical migraine mentioned once
Not a problem candidate if not independently engaged today.

It may render in history/body without a problem owner.

## Prior stroke used only as seizure substrate
Not automatically a separate A/P problem.

It may be evidence/etiology under the seizure problem.

If stroke secondary prevention is independently assessed/managed today, it may become its own problem candidate.

## Two symptoms belonging to one syndrome
S1 should group them under one problem subject when they serve one independent neurologic assessment question.

Example:
- diplopia + fatigable dysarthria under suspected MG exacerbation.

## Two neurologic issues requiring independent assessment
Separate candidates.

Example:
- seizure evaluation;
- independently addressed progressive cognitive decline.

---

# 3. S1 problem identity must remain claim-neutral

The candidate ID/subject should be stable enough to survive S2 claim adjudication.

Prefer subject/question identities such as:

- convulsive episodes;
- acute facial weakness;
- progressive cognitive decline;
- myasthenic symptom worsening;

rather than prematurely finalized diagnoses when the diagnosis itself is disputed.

A known disease can still be the subject when it is unambiguously established and explicitly engaged.

This is architecture guidance, not a mandated naming syntax.

---

# 4. Problem candidacy must not be inferred from management alone

DeepSeek's earlier K2 exposed this.

A management action can support candidacy only when the source establishes what problem it addresses.

Do not infer:
- stroke from aspirin;
- epilepsy from levetiracetam;
- AF from apixaban;
- migraine from topiramate;

unless source context establishes the linkage.

This remains consistent with the frozen no-drug-class/adoption heuristic rule.

---

# 5. Claim representation concept — accept, schema — keep downstream

DeepSeek is correct that a final assessment claim is not always one object ID.

Architecture should therefore freeze only this concept:

> **A problem claim may be represented by one or more source-grounded objects and their S2-adjudicated semantic relations. S2 produces one or more semantically approved claim representations; S3 selects among them but may not synthesize or re-adjudicate them.**

That is enough at interface level.

Do **not** yet freeze exact fields such as:

- `kind = SINGLE | NESTED | DIFFERENTIAL | UNRESOLVED`;
- `relation = COMPETING`;
- `head`, `qualifier`, `alternatives`;
- mandatory `rationale`.

Those belong to downstream Case-IR/schema/operator design.

Exact semantic-relation vocabulary is still open.

---

# 6. Free-text `rationale` should not become an architecture requirement

DeepSeek's example includes:

```
rationale: "clinician left both open pending EEG"
```

The frozen architecture already prefers:

> structured evidence references over mandatory free-text rationale.

Therefore architecture should require:
- source/adjudication support references sufficient to audit the representation;

not:
- a mandatory prose rationale field.

A prose rationale may exist where useful, but it is not an interface invariant.

---

# 7. Failure behavior: no approved claim representation must fail before rendering

DeepSeek writes:

> no approved representation exists, and the problem renders without a claim, which completeness catches.

That sequence is wrong.

If an A/P problem requires a claim representation and S2 cannot produce any valid representation:

- S2 returns unresolved semantic failure / no approved representation;
- S3 cannot select a claim;
- S4 must not construct a valid A/P problem block pretending the requirement is satisfied.

The system should fail/flag at the first owned seam.

Do not knowingly render an invalid problem and rely on downstream completeness to discover it.

Exact failure label/containment remains downstream.

---

# 8. Repaired STRUCTURE interface — consolidated

## S1 — Problem Candidate Model

Owns:
- neurologic problem subject/candidate identity;
- encounter-level relevance/candidacy;
- stable problem id;
- source anchors supporting candidacy;
- structured salience inputs for later ordering.

Unique question:
> Which neurologic subjects require their own current assessment question/status in this encounter?

Does not own:
- current adoption;
- final claim semantics;
- final A/P inclusion;
- final render order.

---

## S2 — Semantic Adjudication

Owns:
- duplicate/equivalence/conflict relations;
- modifier/condition/reasoning roles;
- temporality/current adoption;
- semantic relations among candidate claim objects/formulations;
- one or more semantically approved claim representations, supported by source/adjudication references.

Unique question:
> What do these candidate objects/formulations mean now, and what claim representation(s) are semantically valid?

Does not own:
- note inclusion;
- final editorial selection among equivalent/allowed representations;
- final order.

---

## S3 — Content Selection & Problem Use

Owns:
- object retention/disposition;
- problem use/reuse;
- whether an S1 candidate becomes a rendered A/P problem;
- selection among S2-approved claim representations.

Unique question:
> What approved content and representation will this note use, and for which problem?

Cannot:
- create a new semantic claim;
- resolve S2 semantic conflict;
- alter adoption/role.

---

## S4 — Blueprint

Owns:
- section assignment;
- render-unit construction;
- member roles;
- operator;
- centralized final problem/unit order;
- reuse/completeness accounting.

Problem ownership:
- A/P units require exactly one owning problem;
- body units require problem association only when their section contract says so.

---

# 9. Interface-design closure condition

I would close the design portion of Review 4 if DeepSeek accepts these four points:

1. S1 candidacy criterion = separate current neurologic assessment question/status, not mere mention/relevance.
2. claim representation is frozen as a concept only; exact enums/fields remain downstream.
3. structured evidence/adjudication references are sufficient; no mandatory free-text rationale.
4. no-approved-representation fails/flags at the S2→S3 seam rather than rendering an invalid problem and waiting for S4 completeness.

After that, the repaired interface can be written as a controlled DESIGN CHANGE.

The empirical architecture program remains open:
- AX-S1S2-D;
- AX-LEAK;
- AX-S4;
- AX-I3;
- AX-T;
- AX-SCALE;
- AX-R2;
- AX-SHARED.
