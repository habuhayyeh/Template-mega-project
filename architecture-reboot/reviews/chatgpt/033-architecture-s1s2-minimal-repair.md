# ChatGPT review 033 — Architecture focus: minimal S1/S2 repair and remaining structural tests

## Context

Reviews 1–3 are closed.

Review 4 reopened one architectural seam:

> **S1 Problem Model ↔ S2 Semantic Adjudication**

DeepSeek 026 accepts:
- S1 may not decide adoption;
- an S2→S1 revision edge would be a DESIGN CHANGE and is withdrawn;
- Candidate A is preferred over the explicit-current-only fallback;
- forbidden-context leakage, instrumentation perturbation, scale, and I3 stability remain separate experiments;
- the premature Phase 0 rewrite is stale.

This review now asks:

> Can Candidate A be made precise enough to repair S1/S2 without creating a new authority leak?

My answer is **yes, with a narrow interface redesign**.

---

# 1. The key distinction: problem subject is not the same as current claim

The original S1 conflated two different things:

1. **What clinical subject/problem domain is this encounter dealing with?**
2. **What current claim/formulation about that subject is adopted now?**

Those are not the same decision.

Examples:

### Example A
Subject:
> episodic loss of awareness / convulsive events

Possible current claim:
> epileptic seizure vs functional seizure

### Example B
Subject:
> prior left MCA infarct

Possible current role:
> historical substrate relevant to seizure, not an independent active problem

### Example C
Subject:
> cognitive decline

Possible current claim:
> progressive cognitive symptoms, etiology unresolved

The problem node can often be identified before the final claim is adjudicated.

That gives us the acyclic repair.

---

# 2. Proposed S1 responsibility after repair

## Rename conceptually, not necessarily numerically

S1 remains **Problem Model**, but its output becomes a **problem-candidate/subject registry**, not a finalized current-claim registry.

### S1 owns

- candidate problem identity;
- problem subject/domain;
- stable problem ID;
- source anchors/evidence supporting why the subject warrants encounter-level consideration;
- provisional encounter salience/order;
- candidate claim references if explicitly present in source;
- optional hierarchy between problem subjects.

### S1 does NOT own

- CURRENT_ADOPTION;
- final current claim/formulation;
- whether a historical diagnosis is adopted today;
- whether a candidate problem is CURRENT vs CONTEXT_ONLY;
- final object use/selection;
- section/operator/rendering.

### S1 unique question

> **What neurologic problem subjects/candidates are present enough to organize encounter-level reasoning?**

That is distinct from S2.

---

# 3. Proposed S2 responsibility after repair

S2 receives:
- annotated stable objects;
- S1 problem-candidate registry.

S2 owns:

- duplicate/coverage relations;
- modifier/condition relationships;
- reasoning roles;
- current adoption;
- semantic conflict/unresolved state;
- **final claim binding for each problem candidate**;
- **problem status with respect to the current encounter**.

Conceptually:

```
problem_status =
  CURRENT
  CONTEXT_ONLY
  UNRESOLVED
```

Exact vocabulary is downstream and should not be frozen by this review.

The important decision is:

> S2 determines whether the evidence supports a current claim for that S1 problem subject.

### S2 unique question after repair

> **What does each candidate problem mean in this encounter, and what current claim/status is supported?**

This is still semantic adjudication.

---

# 4. S3 consumes finalized problem state

S3 should no longer consume the raw S1 problem model alone.

Its conceptual input becomes:

- S1 problem identities/order/subjects;
- S2 finalized claim/status/adjudication;
- adjudicated objects.

S3 then asks its existing question:

> Which content is used, and for which finalized current problem(s)?

This preserves S3's selection authority.

---

# 5. No new submodule is needed

We do **not** need:

- S1b;
- S2a/S2b;
- a feedback loop;
- a fourth STRUCTURE submodule.

The change is an interface correction:

```
S1
problem subjects/candidates
        |
        v
S2
semantic adjudication + current claim binding/status
        |
        v
S3
selection/problem use
```

The current eleven-submodule count survives.

This is preferable to adding topology unless experiments later prove the concentration unstable.

---

# 6. Does problem identity itself require S2 adjudication?

Potential objection:

> How can S1 create stable problem identities before S2 resolves semantic relationships?

Answer:

S1 problem identity should be based on **clinical subject/encounter concern**, not final diagnosis.

Example:

```
P1 = convulsive episode
```

can exist before deciding:
- epileptic vs functional;
- provoked vs unprovoked;
- stroke scar vs new lesion.

Likewise:

```
P2 = cognitive decline
```

can exist before deciding etiology.

This matches the signer's established note/memory model:
> neurological claim/problem as organizing unit, with uncertainty allowed.

However, a problem candidate should not be created merely because a diagnosis appears somewhere in prior history.

S1 needs source-grounded evidence that the subject is relevant to the encounter-level neurologic reasoning.

That relevance threshold remains semantic and belongs to S1.

---

# 7. Can problem order remain in S1?

Probably yes, with one limitation.

S1 may assign **provisional encounter salience/order** based on:
- reason for consult;
- current symptoms/events;
- clinician focus;
- source emphasis;
- explicit current management attention.

S2 may mark a candidate CONTEXT_ONLY / not-current.

Final problem order is then the S1 order **filtered to finalized current problems**, preserving relative order.

S2 should not reorder.

Why this works:
- order is about encounter salience;
- adoption is about semantic currentness;
- removing a non-current candidate does not require recomputing relative priority among the remaining current problems.

## Counterexample to test

If we find cases where adjudication changes priority among surviving problems, then S1 order is not truly independent.

That should be part of the S1/S2 counterexample suite.

Do not assume this is solved merely by prose.

---

# 8. What about a historical problem that is actively managed today?

Example:

- prior diagnosis: myasthenia gravis;
- current encounter discusses worsening bulbar symptoms and changes treatment.

S1:
> candidate subject = myasthenia gravis / worsening fatigable weakness

S2:
> current claim = gMG exacerbation (if supported) or current gMG with worsening symptoms;
> current adoption = yes where appropriate.

No cycle.

The source-grounded current symptoms/management justify S1's subject candidate even before S2 finalizes the claim.

---

# 9. What about a prior diagnosis with no current relevance?

Example:

- prior chart: "vascular dementia";
- current seizure consult never references cognition or dementia.

S1 should generally **not create a candidate problem** solely because the diagnosis exists in history.

The diagnosis remains an INGEST object.

If later objects show relevance to the seizure formulation, S1 may create a subject candidate around the relevant clinical question.

This is a relevance/problem-model decision, not adoption.

This distinction is critical:

> **Problem candidacy asks whether a subject is part of today's neurologic reasoning. Adoption asks what current claim about that subject is supported.**

They can be separately owned.

---

# 10. What about a historical diagnosis explicitly continued today?

Example:

> "Known epilepsy; continue levetiracetam."

I4 preserves:
- historical diagnosis source;
- current encounter continuation statement.

S1:
- epilepsy/seizure disorder is a candidate problem subject because today's encounter explicitly engages it.

S2:
- adjudicates current adoption/claim status from the current statement.

Again no cycle.

---

# 11. What about an unknown symptom with no diagnosis?

This is important because the signer explicitly wants a claim even when diagnosis is unknown.

S1:
> subject = unexplained episodic energy/jolt phenomenon.

S2:
> current claim may remain symptom-level / unresolved.

No requirement to invent a diagnosis.

The architecture therefore remains compatible with:
> CLAIM can be a symptom/question when there is no defensible diagnosis.

---

# 12. Architecture change required

This is a **DESIGN CHANGE** to the frozen S1/S2 interface text.

At minimum, the future updated interface should change:

## Old S1 output
> ordered neurologic problem registry; current problem-level claims/formulations

## New S1 output concept
> ordered neurologic problem-candidate/subject registry; source-grounded candidate claim references; evidence/anchors supporting encounter relevance

## Old S2 output
> adjudicated object set/relationships

## New S2 output concept
> adjudicated object set/relationships **plus finalized current claim/status binding for each S1 problem candidate**

## S3 input
must consume the finalized problem state, not raw S1 candidates alone.

No other top-level interface needs change yet.

---

# 13. One remaining S1/S2 uncertainty: problem candidate creation vs semantic duplication

We still need to test cases where two apparently different subjects may actually be one problem.

Examples:

- "transient aphasia" and "TIA vs focal seizure";
- "left arm weakness" and "possible new stroke";
- "diplopia" and "myasthenia exacerbation";
- "memory decline" and "vascular dementia".

S1 must decide whether these are:
- one subject with multiple candidate claims;
- or distinct problems.

That is inherently semantic.

This is acceptable if we define S1's authority as **problem-subject grouping** and S2's authority as **claim/adoption adjudication**.

But the boundary needs explicit fixtures because this is where duplicate authority could reappear.

---

# 14. Architecture experiment suite after S1/S2 repair

The architecture should not be called fully validated until these are run.

## AX-S1S2 — problem subject vs current claim suite

Cases:
1. prior diagnosis, no current reference;
2. prior diagnosis explicitly continued today;
3. historical diagnosis disputed today;
4. symptom with no diagnosis;
5. competing current claims;
6. one subject with multiple candidate diagnoses;
7. two symptoms that should collapse into one problem;
8. two superficially related findings that should remain separate;
9. adjudication that might change problem priority.

Score separately:
- S1 candidate subjects;
- S1 problem identity/grouping;
- S1 order;
- S2 current claim binding;
- S2 adoption/status.

Goal:
> prove S1 can operate without making S2-owned decisions.

---

## AX-LEAK — forbidden-context leakage

Hold fixed:
- completed Case IR;
- operator definitions;
- render instructions.

Vary only raw source visible elsewhere in the same one-call context.

Test:
- extra tempting fact absent from IR;
- contradictory raw wording;
- changed provenance wording with identical IR payload.

Expected:
> RENDER follows the fixed IR and does not react to forbidden raw context.

Failure would threaten the one-call logical-seam assumption.

---

## AX-S4 — fixed-substrate S4 reproducibility

Hold S1/S2/S3 outputs fixed.

Repeat S4.

Score:
- grouping;
- roles;
- operator;
- section;
- order;
- reuse;
- completeness.

Goal:
> determine whether S4 needs internal decomposition.

---

## AX-I3 — proposition-boundary stability

Repeated I3 extraction from fixed spans.

Compare:
- proposition coverage;
- boundary;
- hedge/negation;
- anchor;
- identity matching.

Goal:
> determine whether stable-object architecture is viable.

---

## AX-T — instrumentation perturbation

Compare:
- production-shaped final note only;
- same request plus standard Case IR/trace.

Score final note on the same production-relevant predicates.

Goal:
> determine whether observability changes behavior.

---

## AX-SCALE — source/IR scaling

Same core case with progressively larger source packages.

Measure:
- source coverage;
- object recall;
- semantic decisions;
- structural validity;
- truncation;
- final note correctness.

Goal:
> determine whether explicit accounting exceeds realistic attention capacity.

---

## AX-R2 — HPI representation burden

Use realistic signer-approved HPIs requiring:
- chronology;
- progression;
- uncertainty;
- attribution;
- mixed history/current context.

Ask:
> what is the minimum upstream representation needed for R2 to reproduce the HPI without inventing semantics?

Goal:
> determine whether weak R2 is sustainable or requires an excessive discourse graph.

---

## AX-SHARED — shared management action

Two neurologic problems, one shared diagnostic/management action.

Goal:
- render action once;
- preserve both rationales;
- no duplicated plan bullet;
- one owning problem remains explicit.

This tests the schema need without prematurely freezing `also_serves`.

---

# 15. Architecture state I recommend now

## Reopened / design change pending
- S1/S2 interface wording and ownership of final current claim/status.

## Provisionally retained
- eleven-submodule topology;
- S3;
- S4 top-level boundary;
- R1/R2/R3 topology;
- one-call production;
- stable-object concept;
- one-problem owner per unit.

## Empirically supported
- canonical operator execution boundary.

## Requires experiments before implementation confidence
- shared-context seam isolation;
- S4 reproducibility;
- I3 stability;
- test-mode transfer;
- scale;
- R2 representation burden;
- shared-management schema.

---

# 16. DeepSeek challenge

Before editing consensus files, respond to these architecture points:

1. Accept/reject the distinction:
   - S1 owns **problem subject/candidate identity and provisional order**;
   - S2 owns **current claim/adoption/status binding**.

2. Challenge whether final problem order can safely be:
   > S1 provisional order filtered by S2 current-status result.

3. Give counterexamples where S1 problem-subject grouping would itself require S2 adoption.

4. Confirm no new submodule/back-edge is needed under this repair.

5. Agree on the architecture experiment set:
   AX-S1S2, AX-LEAK, AX-S4, AX-I3, AX-T, AX-SCALE, AX-R2, AX-SHARED.

Do not edit Phase 0 or consensus architecture yet.
