# DESIGN CHANGE DC-002 — candidate authority, accounting, S4 input view, weak-R2 boundary

**Status: PROPOSED. Not applied.** No consensus, interface or architecture file edited.
**Origin:** ten-question red team (058), DeepSeek 035–036, adjudicated in `reviews/chatgpt/060`.
**Scope:** four edits. No module, stage or ordering change.

---

## D1 — terminology and S1 partition authority

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, S1 output

**Before**

```text
- problem candidates with stable ids and source anchors;
- for each candidate, the candidate claim formulations present in the source;
```

**After**

```text
- problem candidates with stable ids and source anchors;
- for each problem candidate, its candidate claims — the formulations present in the source that
  could become, or contribute to, a claim representation;
- the partition: which candidate claims attach to which problem candidate, and why;
```

**Rationale:** S1 owns candidate identity *and* the partition between problem candidates and claim candidates. Previously the partition was implicit and nobody owned it, which is why "are cross-candidate relations missing?" could not be answered. S1 still decides no claim; it decides what belongs to what.

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, S2 input

**Before**

```text
- problem candidates and candidate claims from S1.
```

**After**

```text
- problem candidates, their candidate claims, and the partition between them, from S1.
```

### `CONSENSUS.md`, items 27–28

**Before**

> 27. A problem candidate exists only where the subject needs its own current assessment question, and is source-grounded.
> 28. A claim is a representation that may carry several candidates and their relation; the kind vocabulary is downstream.

**After**

> 27. A **problem candidate** exists only where the subject needs its own current assessment question, and is source-grounded. S1 owns the candidate partition: which claim candidates attach to which problem candidate.
> 28. A **claim candidate** is a source formulation that may become, or contribute to, a claim. A claim is a representation that may carry several claim candidates and their relation; the kind vocabulary is downstream.

---

## D2 — candidate accounting

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, S3 output

**Before**

```text
- the set of problems that render;
- retained object-use set;
- explicit dispositions for unused clinical objects;
```

**After**

```text
- the set of problems that render;
- for every problem candidate from S1, an outcome: RENDERED, or NOT_RENDERED with a reason;
- retained object-use set;
- explicit dispositions for unused clinical objects;
```

### S3 distinctive boundary — append

> S3 accounts for candidates as well as objects. A problem candidate that renders nothing leaves a record, not a silence.

### Follow-on predicate (experiments, not this patch)

`S3-CAND-01` (mechanical): every S1 problem-candidate id appears in S3 `rendered[]` or in candidate outcomes. Added to `predicates.md` when DC-002 is applied.

---

## D3 — S4 input view

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, S4 input

**Before**

```text
- problem candidates and S1's salience inputs (S4 owns final order);
- the rendered-problem set and the representation selected for each problem, from S3;
- retained object-use set and problem-use map from S3;
- adjudicated semantic relationships from S2;
- section/style/operator contracts.
```

**After**

```text
S4 receives `S4_INPUT_VIEW`, a mechanical projection assembled at the seam. Each field keeps its
source owner; the projection decides nothing.

- from S1: rendered problem identity, structured salience and order inputs;
- from S3: the rendered set, the selected representation id per problem, retained use, problem-use/reuse;
- from S2: only the selected representation's member ids, and the semantic relations or reasoning
  attributes those members carry;
- from I3/I4: retained object payload, provenance, temporality;
- from the frozen contracts: section, style and operator definitions.

Excluded: unselected alternatives, candidate relations, adoption verdicts, duplicate groups, and any
adjudication history.
```

### S4 distinctive boundary — append

> S4 has no access to the adjudication record. It may not re-adjudicate, re-select, or consult alternatives — not because it is forbidden, but because they are not delivered.

### Follow-on predicate

`S4-PROJ-01` (mechanical): every field S4 reads is in the `S4_INPUT_VIEW` list. An adjudication field present in S4 input is a packaging violation. This proves packaging only; runtime non-leakage remains AX-LEAK's and the S1S2-D adversarial arms' question.

---

## D4 — weak-R2 bridge boundary

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, R2

**Before**

```text
R2 may:
- join units in order;
- add punctuation and whitespace.
```

**After**

```text
R2 may:
- add whitespace;
- apply capitalisation;
- apply punctuation permitted by the section contract;
- add a lexical bridge only from a closed allowlist that is **empty by default**.

A bridge is admitted to the allowlist only if it is semantically empty — a comma, a semicolon, a full
stop. A relation-bearing bridge (`therefore`, `then`, `because`, `despite`, `but`, `however`) is never
admitted: the relation must come from the source or from a unit, not from composition.

R2 has two guards:
- **mechanical preservation** — each unit's text appears as a contiguous span, in unit order;
- **semantic no-new-relation audit** — no relation, scope or causality appears that no unit contains.
  Recoverability alone cannot detect an added bridge: `A; therefore B` preserves both spans and
  invents the link.
```

---

## What DC-002 does not do

- No new module, stage, or ordering change.
- Does not touch the experiment program. AX-LEAK's semantic-leak extension, the AX-T production-transfer gate, the S4 ordering contract and AX-R2 targets remain separate.
- Does not touch Gate 0, the scorer, or Phase 0.

## Review

Four edits, each with before/after quoted verbatim. Application would be one commit plus a `CHANGE_LEDGER` entry naming `DC-002`, with the two follow-on predicates added to `predicates.md` in the same commit.
