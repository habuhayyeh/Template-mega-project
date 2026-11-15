# DESIGN CHANGE DC-001 — S1–S4 responsibilities, problem scope, claim representations

**Status: PROPOSED. Not frozen.**
This document is a review artifact, not a change. Nothing in the canonical documents has been edited. The change is applied only after the exact diff below is independently reviewed and approved.

**Origin:** Review 4 adversarial pass + DeepSeek 025–030, adjudicated in `reviews/chatgpt/037-review4-interface-design-closure.md`.

**Affects:** `CONSENSUS_ARCHITECTURE_v0.1.md` §6, §7 · `CONSENSUS_SUBMODULE_INTERFACES_v1.md` S1–S4 · `CONSENSUS.md`.

---

## 0. Why a design change and not a clarification

Two of the four edits change what a module is allowed to decide (S1 loses claim authority; S2 gains claim relations). The earlier attempt to treat a similar edit as a clarification was rejected, correctly. This one is recorded as `DESIGN CHANGE`.

---

## 1. `CONSENSUS_ARCHITECTURE_v0.1.md` §6 — Problems

### 1a. Problem ownership is A/P-scoped

**Current (line 179):**

> Each render unit owns exactly one problem.

**Replace with:**

> Each **A/P** render unit owns exactly one problem.
>
> A body unit requires no problem. It may carry an optional problem association where the section contract asks for one, and the association is not an ownership claim.

**Rationale:** universal ownership forced every body fact to become an A/P problem or to have no home. A prior-record fact and a history item belong in the body without an assessment question, and inventing a problem for them is the over-inclusion failure (C13) reproduced at the schema level.

### 1b. Problem candidacy

**Insert after 1a:**

> A problem candidate exists only when the neurologic subject requires its own current assessment question or status in this encounter.
>
> A subject that only supports, refutes, or contextualises another problem remains evidence or context unless it is independently assessed.
>
> Every candidate must be source-grounded: a subject the model infers but the encounter never addresses cannot become a problem.

**Rationale:** this is the missing inclusion criterion. It settles three recorded cases without special rules — the infarct as seizure etiology stays evidence (the O10 generalisation), a deferred family concern is not a candidate (K4), and an actively managed situation remains one.

**What it cannot be:** a mechanical predicate. It is a clinical judgement applied by S1 and checked by audit.

### 1c. Claim representations

**Insert after 1b:**

> A problem's claim is a **representation**, not a single object reference. A representation may carry more than one candidate together with the relation among them — for example a single formulation, a nested formulation, a differential, or an explicitly unresolved question.
>
> The set of representation kinds and their fields is not fixed by this document; it is defined downstream.

**Rationale:** forcing every claim to one object id drops differentials or pushes them into prose, which is the flattening this architecture exists to prevent.

---

## 2. `CONSENSUS_ARCHITECTURE_v0.1.md` §7 — Render units

### 2a. Problem field in the unit examples

**Current (lines 199 and 215, both examples):**

```text
problem=P1
```

**Replace both occurrences with:**

```text
problem=P1            # required for A/P units; optional for body units
```

**Rationale:** consistency with §6 1a. Leaving the examples unqualified would preserve the universal rule by example.

---

## 3. `CONSENSUS_SUBMODULE_INTERFACES_v1.md` — S1

**Current (lines 139–155)** — Goal, Role, Input, Output, Distinctive boundary, as written today: S1 outputs "ordered neurologic problem registry" and "current problem-level claims/formulations".

**Replace the whole S1 block with:**

```text
## S1 — Problem Model

**Goal**
Identify the neurologic subjects this encounter is actually about.

**Role**
Propose problem candidates from the source substrate. Name subjects, keep stable ids, anchor every
candidate to source, and supply salience inputs. It does not decide adoption, does not finalise a
claim, and does not order the note.

**Input**
- complete INGEST source-faithful substrate.

**Output**
- problem candidates with stable ids and source anchors;
- for each candidate, the candidate claim formulations found in the source;
- salience inputs (declared values, not adjectives);
- any candidate-level relationships the substrate states explicitly.

**Distinctive boundary**
S1 answers **"what is this encounter about, as subjects?"**
It does not decide which candidate is the current claim, whether a prior formulation is adopted, or
what order problems render in. A candidate exists only where the subject requires its own current
assessment question; otherwise it is evidence or context.
```

### Rationale

S1's old output — "current problem-level claims" — required S1 to decide currency, which is adoption, which is S2's. That is the cycle Review 4 identified. Removing claim finalisation from S1 removes the cycle without adding a back-edge.

---

## 4. `CONSENSUS_SUBMODULE_INTERFACES_v1.md` — S2

**Replace the whole S2 block with:**

```text
## S2 — Semantic Adjudication

**Goal**
Resolve what the source objects mean for this encounter, including whether prior material is current.

**Role**
Adjudicate relations among objects and among candidate claims, decide adoption, assign reasoning
roles, and emit approved claim representations. It does not select note content and does not order
the note.

**Input**
- annotated stable objects;
- problem candidates and candidate claims from S1.

**Output**
- adjudicated object relations: duplicates, modifiers, conditions, roles, temporality;
- adoption decisions per object, stated against source evidence;
- the relation among a problem's candidate claims — equivalent, nested, complementary, competing,
  contradictory, or unresolved;
- one or more **approved claim representations** per problem where any candidate is eligible;
- an explicit failure when a required problem has no eligible candidate.

**Distinctive boundary**
S2 answers **"what do these objects mean here, and which claim formulations are defensible?"**
It does not select which representation the note uses, does not choose sections, and does not order.
A required A/P problem with no approved representation fails here, named, rather than rendering
claimless and waiting for S4 completeness.
```

### Rationale

Adoption and claim relations belong to the module that already resolves semantic relations. Moving them out of S1 leaves S2 the single owner of "what is current", which is the property the cycle violated.

The explicit failure rule moves the failure to its cause. Deferring to S4's completeness check is the same error as letting the renderer repair malformed units.

---

## 5. `CONSENSUS_SUBMODULE_INTERFACES_v1.md` — S3

**Replace the whole S3 block with:**

```text
## S3 — Content Selection & Problem Use

**Goal**
Decide what the note uses, under which problem, and which approved representation each problem carries.

**Role**
Turn the adjudicated substrate into the retained note-content set, and select one approved claim
representation per rendered problem.

**Input**
- problem candidates from S1;
- adjudicated objects, adoption decisions, and approved claim representations from S2.

**Output**
- retained object-use set;
- explicit dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- one selected claim representation per rendered A/P problem, chosen only from S2's approved set;
- complete accounting of every clinical object as used or dispositioned.

**Distinctive boundary**
S3 answers **"what content are we using, for which problem, and which approved claim does it carry?"**
It may not synthesise a claim representation, may not promote an unresolved relation to a single
claim, and may not merge representations. If it cannot choose among approved representations, it
reports the ambiguity rather than resolving it.
```

### Rationale

Selection among approved representations is an editorial decision and belongs with content selection. Making the representation available at all — including differentials — is what stops S3 from being forced to pick a single object.

---

## 6. `CONSENSUS_SUBMODULE_INTERFACES_v1.md` — S4

**Change: one sentence added to the Distinctive boundary.** The rest of S4 stands.

**Insert into the S4 boundary paragraph:**

> S4 owns the final problem and unit order. S1's salience inputs are inputs to that ordering, not an order; S4 may not re-derive salience, and S1 may not pre-order.

### Rationale

S1's old output included an "ordered problem registry", which contradicts the frozen rule that S4 materialises central order. Naming the owner of order ends that duplication.

---

## 7. `CONSENSUS.md` — record

Add to the ratified section:

```text
21. Problem ownership is A/P-scoped. Body units require no problem; optional association by section contract.
22. A problem candidate exists only where the subject requires its own current assessment question, and is source-grounded.
23. A claim is a representation that may carry several candidates and their relation; the kind vocabulary is downstream.
24. S1 proposes candidates; S2 adjudicates adoption and claim relations and approves representations; S3 selects among approved representations; S4 owns final order.
```

Add to "Explicitly superseded":

```text
- "Each render unit owns exactly one problem" — superseded by A/P-scoped ownership.
- S1 output "current problem-level claims" — superseded by candidate proposals plus S2 adjudication.
```

---

## 8. What this change does not do

- It does not define the representation-kind vocabulary, operator set, or salience schema. Those stay downstream.
- It does not touch Phase 0. Phase 0 remains provisional and stale at `0a6ef14` until this change is applied and reviewed.
- It does not close any experiment. All eight remain open: AX-S1S2-D, AX-LEAK, AX-S4, AX-I3, AX-T, AX-SCALE, AX-R2, AX-SHARED.

---

## 9. Review requirements

1. The exact before/after text above is reviewed line by line. Any disagreement is recorded against the numbered section, not as a general objection.
2. If approved, the edits are applied in one commit, and `CHANGE_LEDGER` records `DC-001` as a `DESIGN CHANGE` with the reviewer's approval.
3. If the applied text differs from the text here by more than formatting, the change is void and is re-proposed.
4. Until step 2, `CONSENSUS_ARCHITECTURE_v0.1` and `CONSENSUS_SUBMODULE_INTERFACES_v1` stand as written, cycles included.
