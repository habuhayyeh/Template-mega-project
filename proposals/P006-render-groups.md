# P006 v4 — explicit render, reasoning and compose groups

**Status:** v4, revised after `reviews/P006-v3-original-branch.md` and the signer's G1 decision. Scope fixed by **D-016**. Awaiting implementation approval.
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
- **`COMPOSE_GROUP`** — one plan line: head plus condition when compatible. Sits in its plan bucket. A `COMPOSE_GROUP` with no condition is malformed.

`05` does not choose a head, decide equivalence, or compose. It renders the head and folds what the group marks as foldable.

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
| G4 | REASON | HEAD O39 `we'll see what the MRI shows`; COVERED O23 | `We'll see what the MRI shows.` |
| G5 | FACT | HEAD O34 `family's concern … is not today's issue`; COVERED O32 | `Family's concern about her memory is not today's issue.` |

Deliberate choices:

- **G1 carries documentation provenance, not event timing.** The signer chose the explicit form: clinical timing from O8, and O53's `2024-02` shown as a documentation date. The parenthesis says `also documented by`, so it cannot be read as the infarct's date.
- **G4's head is O39, not O23.** O23 begins with `but`; rendering it verbatim gives `But the MRI will tell us.`, and dropping the conjunction is not among the ten transformations. Choosing the other member upstream avoids an unauthorized edit — `HEAD` selection is `03`'s decision, not a paraphrase licence.
- **G5 renders the head verbatim.** Deleting `is` and rewriting the clause would be a syntax change no transformation permits.
- **G3 renders one head only.** Joining `no hemorrhage` and `no acute abnormality` needs a word neither contains.

`O18` encephalomalacia and `O19` no new focal lesion stay ungrouped and remain subject to eligibility.

## 8. Validation

1. every grouped `O#` is retained; no object in two groups; no group spans problems or classes;
2. exactly one `HEAD` per group;
3. every `HEAD`, `MODIFIER`, `CONDITION` renders;
4. every `COVERED` has no line of its own;
5. every retained `O#` appears once in the trace with its disposition;
6. group order does not contradict the class order in §6.

P005 checks conformance to these groups; it does not search prose for semantic duplicates.

## 9. Not fixed here

- Whether a group is clinically right — `03` decides, review audits it.
- Wording drift below the group level.
- `COURSE` classification, standing-item evaluation, evidence include-flags, management canonicalisation — all **out of scope under D-016**.

## Out of scope

Substrate, `01`, `02`, `06`, `07`, and any change to the accepted rendering rules.
