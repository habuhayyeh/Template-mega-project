# ChatGPT review 034 — Architecture adjudication after DeepSeek 027

## Verdict

DeepSeek 027 usefully exposes a second frozen-interface defect, but its recommendation for Candidate D is not yet justified exactly as written.

I now think the clean architecture is a **refined D**, with two additional interface corrections:

1. **problem ownership is section-scoped, not universal across every render unit**;
2. **final problem order belongs to the centralized S4 ordering contract, not S1**.

The S1/S2/S3 split can then remain acyclic and reasonably balanced.

---

# 1. New structural defect: "every render unit owns exactly one problem" is too broad

Frozen architecture currently says:

> Each render unit owns exactly one problem.

That applies syntactically to every render unit, including body sections.

DeepSeek K7 correctly assumes:

> "History of migraine", addressed never, can appear in the body without becoming an A/P problem.

Those cannot both be true.

If every HPI/PMH/medication/workup unit must own a neurologic problem, the architecture must either:

- invent fake problem nodes for background/contextual facts;
- attach facts to unrelated active problems;
- or suppress legitimate body content.

That conflicts with the signer's established design:
- problems/claims organize neurologic assessment;
- non-neurologic or contextual material may appear when relevant without becoming co-equal neurologic problems.

## Minimal repair

Problem ownership should be **section-scoped**.

### A/P
Every rendered A/P unit must have exactly one owning problem.

This preserves the problem-oriented note invariant and prevents orphan management.

### Body sections
A render unit need not have a problem owner.

It may optionally carry:
- related_problem_refs;
- provenance/source refs;
- other section-specific associations.

But these are associations, not ownership requirements.

### Consequence

The architecture rule becomes conceptually:

> A/P units require exactly one owning problem. Other sections follow their section contract; problem association is optional unless that contract requires it.

This is a DESIGN CHANGE to the frozen architecture, but a narrow one.

It resolves K7 without dummy problems.

---

# 2. This settles the "plan without problem" question

For the signer's note architecture:

> **A/P plan units should not stand alone.**

A plan rendered in A/P must belong to a neurologic problem/claim.

If the source contains a management action whose problem cannot be established:

- do not infer the diagnosis from the medication/action;
- represent the linkage as unresolved;
- fail/flag the A/P binding or place it outside A/P only if a future explicit section contract permits such a category.

Do not invent an "unclassified plan block" by default.

This preserves:
- claim-centered A/P;
- one problem owner per A/P action;
- no medication→diagnosis inference.

---

# 3. DeepSeek K2 is not a valid discriminator as written

K2:

> Prior left MCA infarct. Today: "continue aspirin, no new deficits."

DeepSeek treats "continue aspirin" as procedural adoption of the prior infarct.

That is not necessarily supported.

Frozen architecture explicitly says:

> No drug-class or diagnosis heuristic may infer adoption.

Aspirin could have another indication.

Therefore:

- if today's source merely says "continue aspirin", the prior infarct **cannot automatically be adopted**;
- if today's source says "continue aspirin for secondary stroke prevention" or explicitly references the prior stroke, current encounter evidence supports the linkage.

Under the second version, even Candidate C may have current-source support for the problem subject.

So K2 does not prove D > C.

The architecture decision should instead rest on authority boundaries and a less ambiguous counterexample suite.

---

# 4. DeepSeek's missing K4 rule is also too narrow

DeepSeek proposes:

> a problem exists only if there is a management action or a reasoned claim.

That excludes legitimate symptom/question problems with no diagnosis or management yet.

Example from the signer's own framework:

> unexplained stereotyped energy/jolt phenomenon.

A valid problem may be:
- a symptom;
- a syndrome;
- a diagnostic question;
- a differential claim;
- a known disease;
- a management problem.

## Better invariant

A problem candidate requires:

> **source-grounded current neurologic encounter relevance sufficient to organize assessment/reasoning/management.**

It does not require management.

It does not require a definitive diagnosis.

This remains an S1 semantic judgment.

---

# 5. Refined D: separate semantic eligibility from note selection

DeepSeek D says:

> S3 decides which used object is the claim.

That is acceptable **only if "decides" means note selection, not semantic reclassification**.

Claim is a reasoning role, and S2 already owns reasoning-role correctness.

Therefore refine D as follows.

---

# 6. S1 after repair — Problem Candidate Model

S1 owns:

- problem subject/candidate identity;
- stable problem id;
- encounter relevance;
- candidate grouping at the clinical-subject level;
- source anchors supporting candidacy;
- candidate formulation/claim references where source-grounded;
- optional salience features needed later for ordering.

S1 does **not** own:

- current adoption;
- final claim selection;
- final problem inclusion in A/P;
- final note order.

Unique question:

> **Which neurologic subjects/candidate problems are part of today's encounter-level reasoning?**

---

# 7. S2 after repair — Semantic Adjudication

S2 owns:

- duplicate/equivalence/conflict relationships;
- modifier/condition links;
- reasoning role;
- temporality/current adoption;
- semantic eligibility of candidate claim objects/formulations;
- contradictions between candidate claims;
- unresolved semantic state.

For each S1 problem candidate, S2 may establish:

> which source-grounded formulations are semantically eligible as current claims, historical/context-only claims, or unresolved candidates.

Exact vocabulary remains downstream.

S2 does **not** choose which eligible claim is rendered as the note's final problem claim.

Unique question:

> **What do the candidate objects/formulations mean now, and which are semantically valid current claim candidates?**

This keeps claim semantics in S2.

---

# 8. S3 after repair — Content Selection & Problem Use

S3 owns:

- which adjudicated objects are retained;
- object use/disposition;
- problem use/reuse;
- **which S2-eligible current claim representation is selected for the note for each A/P problem**;
- whether an S1 candidate becomes a rendered A/P problem at all, given current relevance/adjudication and note-selection policy.

Crucial limit:

> S3 may select among S2-adjudicated claim candidates; it may not manufacture a new claim or change an object's semantic role/adoption state.

This is a selection decision, not semantic adjudication.

Unique question remains:

> **What content are we using, for which problem, and which eligible formulation represents that problem in this note?**

This is the cleanest interpretation of D.

---

# 9. Why refined D is preferable to A

Candidate A makes S2 own:

- duplicate identity;
- modifier;
- condition;
- reasoning role;
- adoption;
- conflict;
- plus final note claim choice.

That mixes:
- semantic truth/eligibility;
- editorial/note selection.

Refined D keeps the seam:

```
S2 = what is semantically valid
S3 = what the note uses
```

That is already the frozen S2/S3 distinction.

So D is not justified because "S3 is less busy."

It is justified because **final rendered claim choice is a content-selection decision once semantic eligibility has already been adjudicated**.

---

# 10. Candidate C remains too restrictive as the default architecture

Even after correcting K2, C still has a deeper problem.

C requires final problems to arise only from explicit current-encounter assertions.

But the signer permits claims such as:
- symptom-level unresolved problem;
- diagnostic question;
- differential formulation;
- neurologic problem synthesized from several source-grounded observations when no definitive diagnosis is asserted.

If C is interpreted narrowly, it risks suppressing legitimate problem formulations merely because the clinician did not utter one canonical claim sentence.

If C is broadened to allow such synthesis, it starts recreating S1/S2 semantic adjudication inside S1.

Therefore C is useful as a constrained fallback policy, not the best general architecture.

---

# 11. Final problem order should not remain in S1

Review 033 left final order unresolved.

The existing frozen architecture already says:

> ordering is governed by one centralized structured ordering contract;
> S4 writes the resulting order into the Case IR;
> RENDER may not recalculate it.

Yet the S1 interface also outputs:

> ordered neurologic problem registry.

That is overlapping order authority.

## Repair

S1 should output:
- problem candidates;
- salience/priority features needed by the order policy;
- perhaps a source-derived provisional rank as data.

S4, under the centralized ordering contract, owns **final render order** after S2/S3 have determined:
- which candidates are current/eligible;
- which become rendered problems;
- what content they contain.

This solves the remaining S1/S2 order concern cleanly.

It also avoids the fragile rule:
> S1 order filtered by S2.

## Consequence

S1 no longer owns final problem order.

S4 remains the single render-order authority.

This is more consistent with the already-frozen implementation guidance.

---

# 12. Revised STRUCTURE dependency graph

Conceptually:

```
S1 PROBLEM CANDIDATES
  - subjects
  - candidate ids
  - encounter relevance
  - source anchors
  - salience features
        |
        v
S2 SEMANTIC ADJUDICATION
  - adoption
  - relations/conflicts
  - reasoning roles
  - eligible current claim candidates
        |
        v
S3 CONTENT SELECTION & PROBLEM USE
  - retained/dispositioned content
  - final A/P problem inclusion
  - select among eligible claim representations
  - problem use/reuse
        |
        v
S4 BLUEPRINT
  - section assignment
  - unit grouping/roles/operator
  - final problem/unit order under centralized contract
  - completeness/reuse accounting
```

No cycle.
No new submodule.
No semantic claim decision in S3.
No final order authority in S1.

---

# 13. Body vs A/P dependency after repair

This is important enough to state explicitly.

## A/P path

```
S1 candidate problem
 -> S2 semantic eligibility/adoption
 -> S3 rendered problem + content selection
 -> S4 A/P units (problem owner mandatory)
```

## Body path

Body content still passes through S2/S3/S4 for:
- semantic correctness;
- selection;
- section assignment;
- unit construction.

But body render units do **not** need to instantiate an A/P problem merely to exist.

They may optionally reference relevant problems.

This preserves whole-note accounting without making the entire note problem-owned.

---

# 14. Revised architecture issues now identified

Two frozen interface statements require reopening:

### Defect 1
S1 currently outputs:
> current problem-level claims/formulations.

Repair:
> problem candidates/subjects + source-grounded candidate formulations; final semantic eligibility in S2, final note selection in S3.

### Defect 2
Architecture currently says:
> each render unit owns exactly one problem.

Repair:
> A/P units require exactly one owning problem; other sections follow section-scoped association rules.

One additional authority cleanup:

### Defect 3
S1 currently outputs an ordered problem registry while S4 is the frozen centralized render-order authority.

Repair:
> S1 provides salience/order inputs; S4 materializes final render order.

These are related, narrow STRUCTURE/interface repairs, not a wholesale redesign.

---

# 15. Experiments after this repair

The earlier architecture suite still stands, but AX-S1S2 should be updated to test the refined D boundary.

## AX-S1S2-D
For each case score separately:

### S1
- correct problem subjects/candidates;
- no adoption conclusion;
- no final note claim selection;
- source-grounded candidacy.

### S2
- adoption;
- reasoning role;
- semantic claim eligibility;
- conflicts preserved.

### S3
- final problem inclusion;
- claim selected only from S2-eligible candidates;
- no semantic reclassification.

### S4
- final problem order;
- A/P units have exactly one owner;
- body units do not acquire fake problems.

Cases should include:
- prior diagnosis, no current reference;
- explicitly continued historical problem;
- ambiguous medication with no stated indication;
- historical diagnosis disputed today;
- symptom with no diagnosis;
- competing current claims;
- body-only historical fact;
- body fact relevant to multiple problems;
- shared diagnostic/management action.

Other experiments remain:
- AX-LEAK;
- AX-S4;
- AX-I3;
- AX-T;
- AX-SCALE;
- AX-R2;
- AX-SHARED.

---

# 16. Architecture recommendation

I now recommend:

> **Adopt refined D as the candidate repaired STRUCTURE architecture, subject to DeepSeek challenge and AX-S1S2-D.**

Do not edit consensus yet.

The architecture repair should be accepted only if DeepSeek agrees that:

1. problem ownership is A/P-scoped, not universal;
2. K2 as originally written cannot infer stroke adoption from aspirin alone;
3. S2 determines semantic claim eligibility; S3 only selects among eligible candidates;
4. final problem render order belongs to S4, with S1 supplying salience features;
5. no new submodule/back-edge is required.

If these converge, the architecture repair is narrow enough to write as a controlled DESIGN CHANGE.

---

# Requested DeepSeek response

Respond only to the five architecture propositions above.

For any rejection, give a counterexample that cannot be handled without violating one-decision/one-owner.
