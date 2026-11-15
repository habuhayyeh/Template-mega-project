# P006 v3 — explicit render and compose groups, with roles

**Status:** v3, scoped by **D-016**. Signer chose the narrow option: this proposal stays the render/compose grouping fix and nothing else. Awaiting implementation approval.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`, `oracles/` (groups file, append-only), `tests/`, `runs/`.
**Does not affect:** substrate, `01`, `02`, `06`, `07`, the six kinds.

---

## 1. Why

Set 3 narrowed the remaining instability to grouping: the same Handoff produced the infarct as one bullet, two bullets, or merged with the encephalomalacia; the CT as one or two; the memory concern once or twice; apixaban hold and resume together or apart.

`05` can see the overlap. Deciding whether two objects state one proposition is a semantic judgement, made fresh on every run. That is why it moves. A checker cannot settle it: `CT head no hemorrhage` and `CT head no acute abnormality` are not string duplicates, and `but the MRI will tell us` and `we'll see what the MRI shows` are not either.

## 2. The group line

`03` emits, per problem, a group for every set of objects meant to become one rendered unit. Every member carries a **role**.

```text
PROBLEM 1
RENDER_GROUP:  G1 | HEAD=O7  | MODIFIER=O8  | COVERED=O53 | chronic infarct with its timing
COMPOSE_GROUP: G2 | HEAD=O12 | CONDITION=O25              | apixaban held, resume on MRI
RENDER_GROUP:  G3 | HEAD=O17 | COVERED=O44                | CT result
RENDER_GROUP:  G4 | HEAD=O23 | COVERED=O39                | MRI adjudication
PROBLEM 2
RENDER_GROUP:  G5 | HEAD=O34 | COVERED=O32                | family memory concern
```

| Role | Meaning | Rendered? |
|---|---|---|
| `HEAD` | the member whose wording is rendered | yes, verbatim |
| `MODIFIER` | adds timing, quantity, tempo or trend to the head's fact | yes, folded into the head |
| `CONDITION` | the conditional part of one decision | yes, attached to the head |
| `COVERED` | another source of the same fact | no — traced only |

Rules: every member keeps its `O#` and provenance; exactly one `HEAD` per group; an object belongs to at most one group; a group never spans problems; an ungrouped object renders alone; `HEAD` is chosen by `03`, never by `05`.

## 3. Roles, not intuition

- **`RENDER_GROUP`** — members express one factual proposition. One bullet: the head, plus a modifier if any.
- **`COMPOSE_GROUP`** — the parts of one decision. One line: head plus condition, when compatible. A `COMPOSE_GROUP` with no condition is malformed.

`05` does not decide equivalence, choose a head, or decide whether a covered member adds a fact. It formats what it is given.

## 4. Payload accounting

- `HEAD`, `MODIFIER`, `CONDITION` **must** render — their content appears in the output.
- `COVERED` is accounted for in the trace, not rendered separately.
- Every `O#`, grouped or not, appears exactly once in the trace table.
- A group whose head does not render is a breach, not a style choice.

That is what makes "no lost reasoning, no duplicated reasoning" auditable instead of aspirational.

## 5. Frozen-case groups

| Group | Roles | Rendered |
|---|---|---|
| G1 | HEAD O7 `known left MCA infarct`; MODIFIER O8 `two years ago`; COVERED O53 | `Known left MCA infarct two years prior to presentation.` |
| G2 | HEAD O12 `apixaban held since admission`; CONDITION O25 `to resume once MRI excludes hemorrhage` | `Apixaban held since admission, to resume once MRI excludes hemorrhage.` |
| G3 | HEAD O17 `CT head no hemorrhage`; COVERED O44 | `CT head no hemorrhage.` |
| G4 | HEAD O23 `but the MRI will tell us`; COVERED O39 | `The MRI will tell us.` |
| G5 | HEAD O34 `family's concern … is not today's issue`; COVERED O32 | `Family's concern about her memory, not today's issue.` |

Deliberate choices:

- **G1 prints no provenance.** O53's `2024-02` is the record's date, not the infarct's, and attaching it to O8's timing is the error we already made once. The marker stays in the trace.
- **G3 prints only the head.** `no hemorrhage` and `no acute abnormality` are both source words; joining them needs a word — `without` — that neither contains. One head, one covered duplicate, no invention.
- **G4's head is O23**, chosen upstream, so `05` never picks between the two hedges.
- **G5's head is O34**, which already carries the full proposition; O32 is the bare concern.

`O18` encephalomalacia and `O19` no new focal lesion stay ungrouped: distinct findings, and folding them is a judgement this proposal does not make.

## 6. Validation

Mechanical, on the group file and the output:

1. every retained `O#` appears in at most one group, and every grouped object is retained;
2. exactly one `HEAD` per group; no group spans problems; no discarded member;
3. every `HEAD`, `MODIFIER` and `CONDITION` renders;
4. every `COVERED` appears in the trace and nowhere in the output text;
5. rendering order follows group order within the facts block.

P005 becomes a conformance check against these groups, not a search for semantic duplicates in prose.

## 7. What this does not fix

- Whether a group is clinically right. `03` decides; review audits it like any other selection.
- Wording drift below the group level.
- `COURSE` classification, which is still prose in `05`. **Explicitly out of scope under D-016.**
- Standing-item evaluation, evidence include-flags and management canonicalisation. **Out of scope under D-016**; each needs its own evidence before it is proposed.

## Out of scope

Substrate, `01`, `02`, `06`, `07`, and any change to the accepted rendering rules.
