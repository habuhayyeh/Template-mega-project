# P006 v5 — explicit render, reasoning and compose groups

**Status:** v5, revised after `reviews/P006-v4-original-branch.md` and the signer’s voice decision (D-017). Scope fixed by D-016. Awaiting implementation approval.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`, `oracles/` (groups file, append-only), `tests/`, `runs/`.
**Does not affect:** substrate, `01`, `02`, `06`, `07`, the six kinds.

---

## 1. Why

Set 3 narrowed the remaining instability to grouping: the same Handoff produced the infarct as one bullet or two, the CT as one or two, the memory concern once or twice, apixaban hold and resume together or apart. `05` can see the overlap but decides sameness afresh each run.

## 2. Three group kinds, one per rhetorical class

Grouping never moves an object between the fact, reasoning and plan classes. Each group declares its class by its type.

```text
PROBLEM 1
FACT_GROUP:    G1 | HEAD=O7  | MODIFIER=O8  | COVERED=O53 | chronic infarct with timing
COMPOSE_GROUP: G2 | HEAD=O12 | CONDITION=O25              | apixaban held, resume on MRI
FACT_GROUP:    G3 | HEAD=O17 | COVERED=O44                | CT result
REASON_GROUP:  G4 | HEAD=O39 | COVERED=O23                | MRI adjudication
PROBLEM 2
FACT_GROUP:    G5 | HEAD=O34 | COVERED=O32                | family memory concern
```

| Role | Meaning | Rendered |
|---|---|---|
| `HEAD` | the member whose wording is rendered | yes, verbatim |
| `MODIFIER` | adds timing, quantity, tempo or trend to the head's fact | folded into the head |
| `CONDITION` | the conditional part of one decision | attached to the head |
| `COVERED` | another source of the same proposition | not as a line |

Rules: exactly one `HEAD` per group; every member keeps its `O#` and provenance; an object is in at most one group; a group never spans problems or rhetorical classes; `HEAD` is chosen in `03`, never in `05`.

## 3. What each kind does

- **`FACT_GROUP`** — one bullet: head, plus modifier if any. Sits in the facts block.
- **`REASON_GROUP`** — one bullet: head verbatim. Sits in the reasoning block, in its existing position.
- **`COMPOSE_GROUP`** — one plan line: `HEAD` plus `CONDITION`. Sits in its plan bucket. Compatibility is adjudicated in `03` before the group is emitted; a non-composable candidate is never emitted as a `COMPOSE_GROUP`, and validation fails it there. `05` neither judges compatibility nor splits a valid group.

`05` does not choose a head, decide equivalence, judge compatibility, or compose. It renders the head and folds what the group marks as foldable.

## 4. Ungrouped objects

**An ungrouped object remains subject to the existing `05` eligibility rules.** P006 fixes equivalence and composition for explicitly grouped objects only; it does not make every retained object mandatory prose.

Moving eligibility upstream is a separate proposal and is not authorized under D-016.

## 5. Payload accounting

- `HEAD`, `MODIFIER` and `CONDITION` must render.
- `COVERED` has **no independent output-line trace**; it is accounted for through its group. Word overlap with the head is expected and permitted — the check is that it has no line of its own, not that its words are absent.
- Every `O#` appears exactly once in the trace: as a head, modifier, condition, covered member, ungrouped rendered line, or ungrouped omission with its reason.
- A group whose head does not render is a breach.

## 6. Ordering

Grouping creates no new ordering system:

- `FACT_GROUP`s sit where their heads sit in the facts order;
- `REASON_GROUP`s sit where their heads sit in the reasoning order;
- `COMPOSE_GROUP`s sit in their plan bucket, in handoff order among that bucket's entries.

## 7. Frozen-case groups

| Group | Kind | Roles | Rendered |
|---|---|---|---|
| G1 | FACT | HEAD O7 `known left MCA infarct`; MODIFIER O8 `two years ago`; COVERED O53 | `Known left MCA infarct two years prior to presentation (also documented by prior neurology, 2024-02).` |
| G2 | COMPOSE | HEAD O12 `apixaban held since admission`; CONDITION O25 | `Apixaban held since admission, to resume once MRI excludes hemorrhage.` |
| G3 | FACT | HEAD O17 `CT head no hemorrhage`; COVERED O44 | `CT head no hemorrhage.` |
| G4 | REASON | HEAD O39 `we'll see what the MRI shows`; COVERED O23 | `MRI to show.` |
| G5 | FACT | HEAD O34 `family's concern … is not today's issue`; COVERED O32 | `Family's concern about her memory is not today's issue.` |

Deliberate choices:

- **G1 carries documentation provenance, not event timing.** The signer chose the explicit form: clinical timing from O8, and O53's `2024-02` shown as a documentation date. The parenthesis says `also documented by`, so it cannot be read as the infarct's date.
- **G4 is impounded by D-017.** Neither source phrasing survives verbatim: `we'll see what the MRI shows` and `but the MRI will tell us` are conversational, and the A/P voice is impersonal. A new bounded transformation 11 removes first-person framing and keeps the proposition: `we'll see what the MRI shows` becomes `MRI to show.` The longer `MRI to show whether there is a new lesion` is rejected here because it repeats the comparator already on the problem line.
- **G5 renders the head verbatim.** Deleting `is` and rewriting the clause would be a syntax change no transformation permits.
- **G3 renders one head only.** Joining `no hemorrhage` and `no acute abnormality` needs a word neither contains.

`O18` encephalomalacia and `O19` no new focal lesion stay ungrouped and remain subject to eligibility.

## 8. The trace artifact

Ungrouped omission happens inside `05`, so one artifact cannot know everything. Ownership is split:

**`04` emits the skeleton**, beside the Handoff, one row per retained `O#`:

```text
O7   | GROUP=G1 | ROLE=HEAD
O8   | GROUP=G1 | ROLE=MODIFIER
O53  | GROUP=G1 | ROLE=COVERED
O18  | UNGROUPED | ROLE=NONE
```

**The validator reconciles it against the output** (P005, or a check step), one row per `O#` with its final disposition:

```text
O7   | GROUP=G1 | ROLE=HEAD      | RENDERED
O53  | GROUP=G1 | ROLE=COVERED   | TRACED_ONLY
O18  | UNGROUPED | ROLE=NONE     | RENDERED
O2   | UNGROUPED | ROLE=NONE     | OMITTED: not material to this claim
```

- `04` owns `GROUP` and `ROLE`; it never guesses a disposition.
- The reconciliation step owns `RENDERED | TRACED_ONLY | OMITTED: reason`, and it is mechanical: it looks for the head's words in the output, and for every `O#` exactly once.
- `05` never writes either file. It receives the Handoff and the group lines, and emits prose only.

That is what makes "every O# accounted for" checkable instead of aspirational: one skeleton, one reconciliation, two writers, no overlap.

## 9. Validation

1. every grouped `O#` is retained; no object in two groups; no group spans problems or classes;
2. exactly one `HEAD` per group;
3. every `HEAD`, `MODIFIER`, `CONDITION` renders;
4. every `COVERED` has no line of its own;
5. every retained `O#` appears once in the trace with its disposition;
6. group order does not contradict the class order in §6.

P005 checks conformance to these groups; it does not search prose for semantic duplicates.

## 10. Not fixed here

- Whether a group is clinically right — `03` decides, review audits it.
- Wording drift below the group level.
- `COURSE` classification, standing-item evaluation, evidence include-flags, management canonicalisation — all **out of scope under D-016**.
- Transformation 11 (impersonal voice) is in scope because D-017 requires it and the frozen case cannot be rendered without it. It is bounded to first-person removal, not paraphrase.

## Out of scope

Substrate, `01`, `02`, `06`, `07`, and any change to the accepted rendering rules.
