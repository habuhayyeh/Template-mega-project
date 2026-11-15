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
- for each problem candidate, its claim candidates — the formulations present in the source that
  could become, or contribute to a claim representation;
- the partition: which claim candidate maps to which problem candidate. Each claim candidate maps
  to exactly one problem candidate.
```

**Rationale:** S1 owns candidate identity *and* the partition. The partition was implicit, which is why "are cross-candidate relations missing?" could not be answered.

**Partition authority is exclusive.** Downstream modules may not merge, split, or re-parent problem candidates or claim candidates.

S2 may adjudicate source-grounded cross-problem and cross-object relations — an infarct that explains a seizure is a real relation. What S2 may not do is use such a relation to alter the S1 partition. Claim candidates whose relation forms a single representation stay within one problem candidate.

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
> 28. A **claim candidate** is a source formulation that may become, or contribute to a claim. A claim is a representation that may carry several claim candidates **belonging to that problem candidate**, together with their relation; the kind vocabulary is downstream.

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
  the problem candidate's subject. This is **salience evidence only** — it records that a management
  statement exists, never that the subject is a problem, adopted, or current. Absence of spans is a
  recorded observation, not an inference;
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

The reason on a NOT_RENDERED outcome must be a typed value, not free text. Where the reason family depends on upstream state (adoption, contradiction, no approved representation), the outcome carries basis references to that state. Whether a reason is *correct* is a separate semantic audit; `S3-CAND-01` checks only that a typed reason exists.

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

- from S1: problem-candidate identity and structured salience/order inputs, projected only for the ids S3 marked RENDERED;
- from S3: the rendered set, the selected representation id per problem, retained use, problem-use/reuse;
- from S2: the selected representation's member ids, the semantic relations or reasoning attributes
  those members carry, the selected representation's own claim relation where it has one, and the
  duplicate/equivalence grouping needed to assign COVERED. Unselected alternatives are NOT projected;
  the selected representation's own relations are.
- from I3/I4: retained object payload, provenance, temporality;
- from the frozen contracts: section, style, operator definitions, and the frozen ordering contract.

Excluded: unselected alternatives, their relations, and the adjudication trail.

The exclusion is **relevance-based, not type-based**. Duplicate and equivalence semantics are projected
where S4 must assign COVERED. An adoption verdict may be projected where a frozen S4 function needs it
for selected or retained content; the adjudication trail never is.

**What is not excluded:** the selected representation's own claim relation, which S4 needs to form a unit whose operator matches the claim's form. In a differential case the individual formulations are claim candidates and the projected relation is e.g. COMPETING or UNRESOLVED — the candidates are projected together with that relation, not one alternative in isolation.
```

### S4 distinctive boundary — append

> The explicit `S4_INPUT_VIEW` does not contain the adjudication record. That is a packaging statement, not a behavioural one: this is one shared model context, and least-privilege packaging is not the same claim as non-leakage at runtime. Behavioural non-leakage is AX-LEAK's and the S1S2-D adversarial arms' question, not this patch's.
>
> S4 still assigns HEAD, MODIFIER, CONDITION and COVERED from the semantic relations in the view. S2 supplies the relations; S4 supplies the roles. Neither may do the other's part.

### Follow-on predicate

`S4-PROJ-01` (mechanical): every field S4 reads is in the frozen `S4_INPUT_VIEW` projection for the selected/retained content. Any field or state outside that projection is a packaging violation. It proves packaging only. This proves packaging only; runtime non-leakage remains AX-LEAK's and the S1S2-D adversarial arms' question.

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
- **mechanical preservation** — after frozen normalisation of permitted capitalisation, whitespace
  and punctuation, each unit's text appears as a contiguous span in unit order. The check runs on
  normalised text; otherwise the transforms it permits would fail it;
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

Applying DC-002 **explicitly stales**: the AX test schema, the CASE-01 parent, the active-predicate set, the Gate 0 seed corpus, the generated artifacts and the campaign identity hashes. All must be regenerated before any Gate 0 run. That regeneration is work after this patch, not part of it.

## Review

Four edits, each with before/after quoted verbatim. Application would be one commit plus a `CHANGE_LEDGER` entry naming `DC-002`, with the two follow-on predicates added to `predicates.md` in the same commit.
