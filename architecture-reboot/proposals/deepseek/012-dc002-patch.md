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
- the partition: which claim candidates attach to which problem candidate.
```

**Rationale:** S1 owns candidate identity *and* the partition. The partition was implicit, which is why "are cross-candidate relations missing?" could not be answered.

**Partition authority is exclusive.** Downstream modules may not merge, split, or re-parent problem candidates or their claim candidates. S2 relates claim candidates **within** one problem candidate; it does not compare across problem candidates, because a cross-candidate comparison is a partition change and the partition is not S2's.

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

## D1b — source-evidence salience

### `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, S1 output — salience line

**Before**

```text
- structured salience inputs — declared, inspectable values; the exact schema is downstream;
```

**After**

```text
- structured salience inputs — declared, inspectable values; the exact schema is downstream;
- `management_reference_spans[]`: the source spans containing a management statement that references
  this candidate. The absence of spans is itself a recorded observation, not an inference;
```

This replaces the `managed_today` boolean. A span list is visibly source-grounded, permits several references, and cannot be read as an adoption verdict — there is nothing to read as a verdict, only spans to check.

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
- exactly one outcome for every S1 problem candidate: RENDERED, or NOT_RENDERED with a typed reason;
- retained object-use set;
- explicit dispositions for unused clinical objects;
```

### S3 distinctive boundary — append

> S3 accounts for candidates as well as objects. A problem candidate that renders nothing leaves a record, not a silence.

### Follow-on predicate (experiments, not this patch)

`S3-CAND-01` (mechanical), three parts:
1. **coverage** — every S1 problem-candidate id has an outcome;
2. **exclusivity** — exactly one outcome per candidate;
3. **equality** — the set marked RENDERED equals S3's `rendered[]`.

The reason on a NOT_RENDERED outcome must be a typed value, not free text. Whether a reason is *correct* is a separate semantic audit; `S3-CAND-01` checks only that a typed reason exists.

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

- from S1: rendered-problem identity and structured salience/order inputs, projected for the ids S3 rendered;
- from S3: the rendered set, the selected representation id per problem, retained use, problem-use/reuse;
- from S2: the selected representation's member ids, the semantic relations or reasoning attributes
  those members carry, and the selected representation's own claim relation where it has one — e.g.
  whether the claim is epileptic or functional. Unselected alternatives and adjudication history are
  NOT projected; the selected representation's own relation is.
- from I3/I4: retained object payload, provenance, temporality;
- from the frozen contracts: section, style, operator definitions, and the frozen ordering contract.

Excluded: unselected alternatives and alternatives' relations, adoption verdicts, duplicate groups,
and any adjudication history.

**What is not excluded:** the selected representation's own claim relation, which S4 needs in order to
form a unit whose operator matches the claim's form.
```

### S4 distinctive boundary — append

> The explicit `S4_INPUT_VIEW` does not contain the adjudication record. That is a packaging statement, not a behavioural one: this is one shared model context, and least-privilege packaging is not the same claim as non-leakage at runtime. Behavioural non-leakage is AX-LEAK's and the S1S2-D adversarial arms' question, not this patch's.
>
> S4 still assigns HEAD, MODIFIER, CONDITION and COVERED from the semantic relations in the view. S2 supplies the relations; S4 supplies the roles. Neither may do the other's part.

### Follow-on predicate

`S4-PROJ-01` (mechanical): every field S4 reads is in the `S4_INPUT_VIEW` list. An adjudication field present in S4 input is a packaging violation. It proves packaging only. This proves packaging only; runtime non-leakage remains AX-LEAK's and the S1S2-D adversarial arms' question.

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
- add a lexical bridge only from a closed allowlist that is **empty by default**; the safest initial
  contract adds **no** lexical bridge tokens at all.

Punctuation is a **surface transform**, not a lexical bridge. Commas, semicolons and full stops do not
belong on the bridge allowlist; they are governed by the punctuation rule above.

A lexical bridge is a word. The allowlist admits none initially. A relation-bearing bridge
(`therefore`, `then`, `before`, `despite`, `but`, `however`, `because`) is never admitted, because the
relation must come from the source or from a unit, not from composition.

R2 has two guards:
- **mechanical preservation** — each unit's text appears as a contiguous span, in unit order;
- **semantic no-new-relation audit** — none of the following appears unless a unit contains it:
  causal, temporal, contrastive, conditional, attributive, certainty, negation, or scope relations.
  Recoverability alone cannot detect an added bridge: `A; therefore B` preserves both spans and
  invents the link.
```

---

## What DC-002 does not do

- No new module, stage, or ordering change.
- Does not touch the experiment program. AX-LEAK's semantic-leak extension, the AX-T production-transfer gate, the S4 ordering contract and AX-R2 targets remain separate.
- Does not touch Gate 0, the scorer, or Phase 0.

## Consequence when applied

Adding `S3-CAND-01` and `S4-PROJ-01` makes the current Gate 0 campaign stale: the active predicate set grows, so the seed corpus, the generated artifacts and the campaign identity hashes must be regenerated before any Gate 0 run. That regeneration is work after this patch, not part of it.

## Review

Four edits, each with before/after quoted verbatim. Application would be one commit plus a `CHANGE_LEDGER` entry naming `DC-002`, with the two follow-on predicates added to `predicates.md` in the same commit.
