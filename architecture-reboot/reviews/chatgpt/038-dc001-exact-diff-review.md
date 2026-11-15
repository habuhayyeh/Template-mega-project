# ChatGPT review 038 — DC-001 exact-diff review

## Verdict

**REVISE. Do not apply DC-001 yet.**

The architecture direction is accepted and remains converged. The problems below are exact-diff/integration defects: the proposed edits do not yet fully remove the old authority model from the canonical documents, and two lines introduce new ambiguity.

This is not a reopening of Review 4.

---

# Blocker 1 — S4 still consumes an "ordered problem model"

DC-001 says:

> S4 owns the final problem and unit order. S1's salience inputs are inputs to that ordering, not an order; S1 may not pre-order.

But the current S4 **Input** remains:

> - ordered problem model;

DC-001 §6 proposes changing only the S4 Distinctive boundary.

If applied as written, the canonical interface would simultaneously say:

- S1 may not pre-order;
- S4 owns final order;
- S4 consumes an already **ordered** problem model.

That is an unresolved authority contradiction.

## Required revision

Replace the S4 input so it consumes the post-S3 problem/content state plus S1 salience inputs, not an ordered S1 model.

Conceptually:

- selected/rendered problem set and selected claim representations from S3;
- retained object-use/problem-use map from S3;
- adjudicated semantic relationships from S2;
- structured salience/order inputs originating from S1;
- section/style/operator/ordering contracts.

Exact wording may be shorter, but there must be no upstream final order.

---

# Blocker 2 — the interface chain still encodes the old S1/S2/S3 outputs

The current interface chain says:

```
S1 PROBLEM MODEL
   -> problem registry
S2 SEMANTIC ADJUDICATION
   -> adjudicated object set
S3 CONTENT SELECTION & PROBLEM USE
   -> retained use map + dispositions
```

After DC-001, that is materially incomplete and misleading.

The repaired architecture is:

```
S1
 -> problem candidates + source anchors + salience inputs
S2
 -> adjudicated objects/relations + adoption + approved claim representations
S3
 -> retained use map + rendered problem inclusion + selected approved representations
S4
 -> completed blueprint + final order
```

## Required revision

DC-001 must update the interface-chain output labels.

Otherwise the detailed blocks and the canonical summary diagram will disagree.

---

# Blocker 3 — the Distinctiveness table still gives S1 the old authority

The current table says:

| S1 | What are the encounter's neurologic problems/claims? |
| S2 | What do the objects mean here and how do they relate? |
| S3 | Which content is used, and for which problem? |

That reintroduces claim authority into S1 after the replacement block explicitly removes it.

## Required revision

Update at minimum:

- **S1:** Which neurologic subjects require their own current assessment question/status?
- **S2:** What do the candidate objects/formulations mean now, and which claim representation(s) are semantically defensible?
- **S3:** What approved content/representation will the note use, and for which problem?
- **S4:** may remain the blueprint/order question, preferably naming final order.

The exact prose may differ, but one-decision/one-owner must survive the summary table.

---

# Blocker 4 — CONSENSUS.md numbering collides with existing decisions 21–25

DC-001 §7 says to add:

```
21. Problem ownership is A/P-scoped...
22. A problem candidate exists...
23. A claim is a representation...
24. S1 proposes candidates...
```

But `CONSENSUS.md` already contains ratified decisions **21–25**:

- 21 Mechanical checking...
- 22 Source-to-Case-IR correctness...
- 23 Stable object identity...
- 24 Object accounting...
- 25 Source spans...

Applying DC-001 literally creates duplicate decision numbers.

## Required revision

Append these as **26–29**, or deliberately renumber the entire canonical list in one reviewed change.

Preferred: append **26–29** to preserve historical references.

---

# Blocker 5 — S2 wording risks taking source-temporality authority back from I4

Proposed S2 output:

> adjudicated object relations: duplicates, modifiers, conditions, roles, **temporality**;

I4 already owns source-grounded temporality/metadata.

The frozen architecture deliberately separates:

- **source temporality / source attributes** → I4;
- **current adoption / encounter-level semantic interpretation** → S2.

The bare word `temporality` in S2 can erase that distinction.

## Required revision

Use wording that preserves the boundary, e.g.:

> encounter-level temporal/semantic relations where adjudication is required

while explicitly leaving source-grounded temporality with I4.

Do not make S2 re-annotate source temporality.

---

# Blocker 6 — S2 freezes a relation vocabulary that DC-001 says is downstream

DC-001 §1c correctly says:

> The set of representation kinds and their fields is not fixed by this document; it is defined downstream.

But the proposed S2 output then states:

> the relation among a problem's candidate claims — equivalent, nested, complementary, competing, contradictory, or unresolved;

Read literally, that is a closed architecture-level relation taxonomy.

Review 4 explicitly left the exact relation vocabulary downstream.

## Required revision

Make the list illustrative:

> semantic relation(s) among candidate claim formulations (for example equivalence, nesting, competition, contradiction, or unresolved relation); exact vocabulary downstream.

Or omit the examples entirely.

---

# Blocker 7 — "required problem" is not known by S2

Proposed S2 output:

> an explicit failure when a **required problem** has no eligible candidate.

Proposed S2 boundary:

> A **required A/P problem** with no approved representation fails here...

But S3 owns:

> whether an S1 candidate becomes a rendered A/P problem.

Therefore S2 cannot generally know that a candidate is a "required A/P problem" without taking S3's inclusion authority.

This creates a subtle new cycle/authority leak.

## Required revision

At S2:

> emit approved representation(s), or an explicit no-approved-representation / unresolved semantic state for that candidate.

At the S2→S3 seam:

> S3 may not render/select an A/P problem lacking an S2-approved representation. If governing requirements require that problem to render, the seam fails/flags there.

Architecture invariant:
- S2 owns semantic adequacy;
- S3 owns inclusion;
- absence of an approved representation blocks S3 from selecting/rendering the problem.

Do not require S2 to know S3's final inclusion decision.

---

# Blocker 8 — the mechanical checker still assumes universal problem ownership

`CONSENSUS_ARCHITECTURE_v0.1.md` §10.1 currently includes:

> within one section + problem, the same object may participate in at most one render unit;
> cross-section reuse is allowed;
> explicit cross-problem reuse within the same section is allowed.

After A/P-scoped problem ownership, body units may have no problem.

The checker rule therefore becomes undefined or under-specified for body sections.

## Required revision

Scope the current problem-uniqueness rule explicitly to A/P, and state that body-section duplicate/use constraints are governed by the body section contract / unit-accounting rule.

Do not invent the exact body duplicate policy here if it is downstream.

---

# Blocker 9 — the high-level Case IR diagram still visually makes `problem` mandatory for every unit

The architecture diagram lists render-unit fields as:

```
|-- problem
|-- rhetorical class
...
```

After DC-001, this can be read as universal ownership.

This is weaker than the blockers above but cheap to fix while the canonical design is being changed.

## Required revision

Change conceptually to:

> problem owner / association as required by section contract

or annotate that owner is mandatory for A/P and optional for body units.

---

# Non-blocking wording issue A — candidacy examples should not look exhaustive

DC-001 §1b says:

> A subject that only supports, refutes, or contextualises another problem remains evidence or context unless it is independently assessed.

The governing principle is good.

To avoid a narrow exhaustive reading, prefer:

> supports, refutes, explains, contextualises, or otherwise modifies another problem **without requiring its own assessment status**...

This preserves the actual rule:
> separate problem only when it needs its own current assessment question/status.

Not a blocker if DeepSeek makes the sentence clearly illustrative rather than exhaustive.

---

# Non-blocking wording issue B — S1 salience wording is too implementation-flavored

Proposed:

> salience inputs (declared values, not adjectives)

The architecture agreement was:

> structured, inspectable salience/order inputs; exact schema downstream.

"Declared values, not adjectives" communicates the intent but risks implying an enum/value schema before it exists.

Preferred:

> structured, inspectable salience inputs required by the centralized ordering contract; exact fields and scales remain downstream.

---

# What is accepted in DC-001

These parts are directionally correct:

1. A/P-scoped problem ownership.
2. Source-grounded S1 candidacy criterion.
3. Claim-representation concept without fixing representation-kind schema.
4. S1 loses final claim/adoption/order authority.
5. S2 owns adoption + semantic claim relations/eligibility.
6. S3 selects only among S2-approved representations.
7. S4 owns final order.
8. No new submodule or back-edge.
9. Phase 0 remains untouched/stale.
10. All eight architecture experiments remain open.

So this is a **revision of the canonical patch**, not a redesign.

---

# Required DeepSeek revision

Please issue **DC-001 v2** and change only the items above.

The v2 proposal should include exact before/after text for:

1. Architecture §2 Case IR diagram;
2. Architecture §6 problem scope/candidacy/claim representation;
3. Architecture §7 examples;
4. Architecture §10.1 checker wording affected by optional body ownership;
5. Interface S1;
6. Interface S2;
7. Interface S3;
8. Interface S4 **including its Input block**;
9. Interface chain;
10. Distinctiveness table;
11. CONSENSUS.md additions with non-colliding numbering and supersessions.

Do not apply the canonical change yet.
Do not touch Phase 0.
