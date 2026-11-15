# DESIGN CHANGE DC-001 v2 — S1–S4, problem scope, claim representations

**Status: PROPOSED. Not applied.** No canonical file edited. Phase 0 untouched.
**Supersedes:** DC-001 v1 (`007-design-change-s1-s4.md`). v1 was rejected for integration defects; this version addresses all nine, plus the two non-blocking notes.

---

## D1 — `CONSENSUS_ARCHITECTURE_v0.1.md` §6, line 179

**Before**

> Each render unit owns exactly one problem.

**After**

> Each **A/P** render unit owns exactly one problem.
>
> A body unit requires no problem. It may carry an optional problem association where the section contract asks for one, and that association is not an ownership claim.

---

## D2 — §6, insert after D1

> A problem candidate exists only when the neurologic subject requires its own current assessment question or status in this encounter.
>
> A subject that only supports, refutes, or contextualises another problem remains evidence or context unless it is independently assessed. Those three are examples, not an exhaustive list of the ways a subject can fail to be a problem.
>
> Every candidate must be source-grounded: a subject the model infers but the encounter never addresses cannot become a problem.

---

## D3 — §6, insert after D2

> A problem's claim is a **representation**, not a single object reference. A representation may carry more than one candidate together with the relation among them.
>
> The kinds of representation and their fields are not fixed here; they are defined downstream.

---

## D4 — §7, lines 200 and 215 (two occurrences)

**Before**

```text
problem=P1
```

**After**

```text
problem=P1            # required for A/P units; omitted for body units
```

---

## D5 — §10.1, line 331

**Before**

> - within one section + problem, the same object may participate in at most one render unit;

**After**

> - within one section and, for A/P units, one problem, the same object may participate in at most one render unit;
> - body units are keyed by section alone;

---

## D6 — `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, execution chain, lines 357–370

**Before**

```text
S1 PROBLEM MODEL
   -> problem registry
S2 SEMANTIC ADJUDICATION
   -> adjudicated object set
S3 CONTENT SELECTION & PROBLEM USE
   -> retained use map + dispositions
S4 NOTE BLUEPRINT / UNIT COMPILATION
   -> completed Case IR
```

**After**

```text
S1 PROBLEM MODEL
   -> problem candidates + candidate claims + salience inputs
S2 SEMANTIC ADJUDICATION
   -> adjudicated objects + adoption + approved claim representations
S3 CONTENT SELECTION & PROBLEM USE
   -> retained use map + dispositions + one selected representation per rendered problem
S4 NOTE BLUEPRINT / UNIT COMPILATION  (owns final problem and unit order)
   -> completed Case IR
```

---

## D7 — S1 block replacement

```text
## S1 — Problem Model

**Goal**
Identify the neurologic subjects this encounter is actually about.

**Role**
Propose problem candidates. Name subjects, keep stable ids, anchor every candidate to source,
and supply structured, inspectable salience inputs. It does not decide adoption, does not finalise
a claim, and does not order the note.

**Input**
- complete INGEST source-faithful substrate.

**Output**
- problem candidates with stable ids and source anchors;
- for each candidate, the candidate claim formulations present in the source;
- structured salience inputs — declared, inspectable values whose exact schema is downstream;
- candidate-level relationships the substrate states explicitly.

**Distinctive boundary**
S1 answers **"which neurologic subjects need their own assessment question in this encounter?"**
It does not decide which candidate is the current claim, whether a prior formulation is adopted,
or what order problems render in. A candidate exists only where the subject needs its own current
assessment; otherwise the subject is evidence or context.
```

---

## D8 — S2 block replacement

```text
## S2 — Semantic Adjudication

**Goal**
Resolve what the source objects mean for this encounter, including whether prior material is current.

**Role**
Adjudicate relations among objects and among candidate claims, decide encounter-level adoption,
assign reasoning roles, and mark which claim formulations are defensible.

**Input**
- annotated stable objects, including the source temporality recorded during annotation;
- problem candidates and candidate claims from S1.

**Output**
- adjudicated object relations: duplicates, modifiers, conditions, reasoning roles;
- encounter-level adoption decisions per object, stated against source evidence;
- for each problem candidate, the relation among its candidate claims — for example equivalent,
  nested, complementary, competing, contradictory, or unresolved; this vocabulary is illustrative
  and is defined downstream;
- zero or more approved claim representations per problem candidate;
- an explicit `NO_APPROVED_REPRESENTATION` state where no candidate is defensible.

**Distinctive boundary**
S2 answers **"what do these objects mean here, and which claim formulations are defensible?"**
It does not select content, does not choose sections, does not order, and does not decide whether a
problem is rendered. **Source temporality is not S2's**: it is recorded during annotation and only
consumed here.
```

Why the `NO_APPROVED_REPRESENTATION` state replaces "fail on a required A/P problem": S2 cannot know that a problem is required before S3 decides rendered inclusion. S2 reports a semantic state; the S2→S3 seam is where inclusion is blocked.

---

## D9 — S3 block replacement

```text
## S3 — Content Selection & Problem Use

**Goal**
Decide what the note uses, under which problem, and which approved representation each rendered
problem carries.

**Role**
Turn the adjudicated substrate into the retained note-content set, and select one approved claim
representation per rendered A/P problem.

**Input**
- problem candidates from S1;
- adjudicated objects, adoption decisions and approved claim representations from S2.

**Output**
- retained object-use set;
- explicit dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- one selected claim representation per rendered A/P problem, chosen only from S2's approved set;
- complete accounting of every clinical object as used or dispositioned.

**Distinctive boundary**
S3 answers **"what content are we using, for which problem, and which approved claim does it carry?"**
It may not synthesise a representation, promote an unresolved relation to a single claim, or merge
representations. **It may not render an A/P problem that has no approved representation**: inclusion
is blocked at the S2→S3 seam, with the problem named. If several approved representations exist, it
selects one and records the choice; it does not resolve the ambiguity itself.
```

---

## D10 — S4

**Input list, line 215 — before**

```text
- ordered problem model;
```

**After**

```text
- problem candidates and S1's salience inputs (S4 owns final order);
```

**Distinctive boundary — append**

> S4 owns the final problem and unit order. S1's salience inputs feed that ordering; they are not an order. S4 may not re-derive salience, and S1 may not pre-order.

---

## D11 — Distinctiveness table, lines 402–405

**Before**

```text
| S1 | What are the encounter's neurologic problems/claims? |
| S2 | What do the objects mean here and how do they relate? |
| S3 | Which content is used, and for which problem? |
| S4 | Exactly what must render, where, how, and in what order? |
```

**After**

```text
| S1 | Which neurologic subjects need their own assessment question? |
| S2 | What do the objects mean, and which claim formulations are defensible? |
| S3 | Which content is used, for which problem, with which approved claim? |
| S4 | Exactly what must render, where, how, and in what order? |
```

---

## D12 — `CONSENSUS.md` additions

**Numbers 26–29** — 21–25 already exist.

```text
26. Problem ownership is A/P-scoped. Body units require no problem; optional association by section contract.
27. A problem candidate exists only where the subject needs its own current assessment question, and is source-grounded.
28. A claim is a representation that may carry several candidates and their relation; the kind vocabulary is downstream.
29. S1 proposes candidates; S2 adjudicates adoption and claim relations and marks defensible formulations; S3 selects among approved representations and blocks inclusion where none exists; S4 owns final order.
```

**Superseded section — append**

```text
- "Each render unit owns exactly one problem" — superseded by A/P-scoped ownership (D1).
- S1 output "current problem-level claims" — superseded by candidate proposals plus S2 adjudication (D7, D8).
```

---

## Unchanged, deliberately

- No representation-kind vocabulary, operator set, or salience schema is fixed.
- No Phase 0 edit. Phase 0 remains provisional and stale at `0a6ef14`.
- No experiment closed. All eight remain open: AX-S1S2-D, AX-LEAK, AX-S4, AX-I3, AX-T, AX-SCALE, AX-R2, AX-SHARED.

## Review requirements

1. Review by numbered section. Disagreements name the section.
2. If approved, applied in one commit, with `DC-001` recorded in `CHANGE_LEDGER` as a `DESIGN CHANGE`.
3. If the applied text differs from this by more than formatting, the change is void and re-proposed.
4. Until applied, both canonical documents stand as written.
