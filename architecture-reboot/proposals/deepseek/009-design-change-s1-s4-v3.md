# DESIGN CHANGE DC-001 v3 — S1–S4, problem scope, claim representations

**Status: PROPOSED. Not applied.** No canonical file edited. Phase 0 untouched.
**Supersedes:** v1 (`007`) and v2 (`008`). Both stay on record with their defects.

Architecture unchanged from v2. This version fixes the eight patch-integration defects.

---

## D1 — `CONSENSUS_ARCHITECTURE_v0.1.md` §2, Case IR diagram, line 44

**Before**

```text
   |     |-- problem
```

**After**

```text
   |     |-- problem  (required for A/P units; optional for body units)
```

This is the old blocker v2 missed: the diagram is the first thing anyone reads, and it was still showing `problem` as universal.

---

## D2 — §6, line 179

**Before**

> Each render unit owns exactly one problem.

**After**

> Each **A/P** render unit owns exactly one problem.
>
> A body unit requires no problem. It may carry an optional problem association where the section contract asks for one, and that association is not an ownership claim.

---

## D3 — §6, insert after D2

> A problem candidate exists only when the neurologic subject requires its own current assessment question or status in this encounter.
>
> A subject that supports, refutes, or contextualises another problem remains evidence or context unless it is independently assessed. These are examples, not an exhaustive list.
>
> Every candidate must be source-grounded: a subject the model infers but the encounter never addresses cannot become a problem.

---

## D4 — §6, insert after D3

> A problem's claim is a **representation**, not a single object reference. A representation may carry more than one candidate together with the relation among them. The kinds of representation and their fields are defined downstream.

---

## D5 — §7, lines 200 and 215 (two occurrences)

**Before**

```text
problem=P1
```

**After**

```text
problem=P1            # required for A/P units; optional for body units
```

---

## D6 — §10.1, line 331

**Before**

> - within one section + problem, the same object may participate in at most one render unit;

**After**

> - within one section and, for A/P units, one problem, the same object may participate in at most one render unit;
> - uniqueness for body units is governed by the section contract, not by this rule;

v2 wrote "body units are keyed by section alone", which invented a body duplicate policy. The architecture does not have one yet, and inventing it in a checker line is how a policy becomes invisible.

---

## D7 — `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, execution chain, lines 357–370

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
   -> rendered-problem set + retained use map + dispositions + selected representations
S4 NOTE BLUEPRINT / UNIT COMPILATION  (owns final problem and unit order)
   -> completed Case IR
```

---

## D8 — S1 block replacement

```text
## S1 — Problem Model

**Goal**
Identify the neurologic subjects this encounter is actually about.

**Role**
Propose problem candidates. Name subjects, keep stable ids, anchor every candidate to source, and
supply structured, inspectable salience inputs. It does not decide adoption, does not finalise a
claim, and does not order the note.

**Input**
- complete INGEST source-faithful substrate.

**Output**
- problem candidates with stable ids and source anchors;
- for each candidate, the candidate claim formulations present in the source;
- structured salience inputs — declared, inspectable values; the exact schema is downstream;
- candidate-level relationships the substrate states explicitly.

**Distinctive boundary**
S1 answers **"which neurologic subjects need their own assessment question in this encounter?"**
It does not decide which candidate is the current claim, whether a prior formulation is adopted, or
what order problems render in. A candidate exists only where the subject needs its own current
assessment; otherwise the subject is evidence or context.
```

---

## D9 — S2 block replacement

```text
## S2 — Semantic Adjudication

**Goal**
Resolve what the source objects mean for this encounter, including whether prior material is current.

**Role**
Adjudicate relations among objects and among candidate claims, decide encounter-level adoption,
assign reasoning roles, and produce approved claim representations.

**Input**
- annotated stable objects, including the source temporality recorded during annotation;
- problem candidates and candidate claims from S1.

**Output**
- adjudicated object relations: duplicates, modifiers, conditions, reasoning roles;
- encounter-level adoption decisions per object, stated against source evidence;
- for each problem candidate, the relation among its candidate claims — for example equivalent,
  nested, complementary, competing, contradictory, or unresolved; this vocabulary is illustrative
  and is defined downstream;
- zero or more approved claim representations per problem candidate, which may be built from
  source-grounded objects and relations and are not limited to sources already phrased as claims;
- where no candidate is defensible, an explicit state that S3 can act on; its name and form are
  downstream.

**Distinctive boundary**
S2 answers **"what do these objects mean here, and which claim formulations are defensible?"**
It does not select content, choose sections, or order. **Source temporality is not S2's**: it is
recorded during annotation and only consumed here.

**Approval is a safety property.** Where S2 approves more than one representation for a problem,
those representations must be interchangeable — equivalent, or explicitly ordered by S2 with the
basis recorded. S2 may not leave S3 a set that requires semantic judgement to choose from.
```

`NO_APPROVED_REPRESENTATION` is withdrawn as a token; it froze vocabulary that is downstream. What remains is the obligation: S2 must emit a state S3 can act on.

---

## D10 — S3 block replacement

```text
## S3 — Content Selection & Problem Use

**Goal**
Decide what the note uses, under which problem, and which approved representation each rendered
A/P problem carries.

**Role**
Turn the adjudicated substrate into the rendered-problem set and retained content, and attach one
approved claim representation to each rendered A/P problem.

**Input**
- problem candidates from S1;
- adjudicated objects, adoption decisions and approved claim representations from S2.

**Output**
- the set of problems that render;
- retained object-use set;
- explicit dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- for each rendered A/P problem, one representation taken from S2's approved set;
- complete accounting of every clinical object as used or dispositioned.

**Distinctive boundary**
S3 answers **"what content are we using, for which problem, and which approved claim does it carry?"**
It may not synthesise a representation, promote an unresolved relation to a single claim, or merge
representations. **It does not resolve semantic ambiguity**: if S2's approved set for a required
problem is empty, inclusion is blocked at the S2→S3 seam with the problem named; if the set holds
more than one non-equivalent representation, that is an S2 defect, not an S3 choice.
```

---

## D11 — S4

**Input list, line 215 — before**

```text
- ordered problem model;
```

**After**

```text
- problem candidates and S1's salience inputs (S4 owns final order);
- the rendered-problem set and the representation selected for each problem, from S3;
```

**Distinctive boundary — append**

> S4 owns the final problem and unit order. S1's salience inputs feed that ordering; they are not an order. S4 may not re-derive salience, and S1 may not pre-order.

---

## D12 — Distinctiveness table, lines 402–405

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

## D13 — `CONSENSUS.md`, numbers 26–29

21–25 already exist.

```text
26. Problem ownership is A/P-scoped. Body units require no problem; optional association by section contract.
27. A problem candidate exists only where the subject needs its own current assessment question, and is source-grounded.
28. A claim is a representation that may carry several candidates and their relation; the kind vocabulary is downstream.
29. S1 proposes candidates; S2 adjudicates adoption and claim relations and produces approved claim representations; S3 selects the rendered-problem set and one approved representation per problem; S4 owns final order.
```

**Superseded — append**

```text
- "Each render unit owns exactly one problem" — superseded by A/P-scoped ownership (D2).
- S1 output "current problem-level claims" — superseded by candidate proposals plus S2 adjudication (D8, D9).
```

---

## Unchanged, deliberately

No representation vocabulary, operator set, salience schema, or body duplicate policy is fixed. No Phase 0 edit. All eight experiments remain open.

## Review requirements

Review by numbered section; one commit to apply; a `CHANGE_LEDGER` entry naming `DC-001`; applied text differing by more than formatting voids the change.
