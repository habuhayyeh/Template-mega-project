# P006 — explicit render and compose groups

**Status:** draft, awaiting review. Not implemented.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`, `oracles/` (groups file, append-only), `tests/`, `runs/`.
**Does not affect:** substrate, `01`, `02`, `06`, `07`, the six kinds, the `05` rendering rules already accepted.

---

## 1. Why

Set 3 narrowed the remaining instability to one class. Not formatting, not selection of facts — **grouping**. The same Handoff produced:

- the infarct as one bullet, two bullets, or merged with the encephalomalacia;
- the CT as one bullet or two;
- the memory concern once or twice;
- the MRI hedge once or, in run 3, twice;
- apixaban hold and resume as one conditional or two bullets.

`05` can see that these objects overlap. Deciding whether two objects are the same proposition is a semantic judgement, and it is being made fresh on every run. That is why it moves.

P005 cannot fix this. A checker can catch exact and normalised duplicates; it cannot decide that `CT head no hemorrhage` and `CT head no acute abnormality` are one fact, or that `but the MRI will tell us` and `we'll see what the MRI shows` are one proposition. I claimed it could; that was wrong.

## 2. What is proposed

Keep `04` lossless. Add one thing: an A/P grouping manifest that says which retained objects are meant to render together.

```text
PROBLEM 1
RENDER_GROUP: G1 | O7 O8 O53 | chronic infarct with its timing
COMPOSE_GROUP: G2 | O12 O25 | apixaban held, resume on MRI
RENDER_GROUP: G3 | O17 O44 | CT result
RENDER_GROUP: G4 | O23 O39 | MRI adjudication
...
PROBLEM 2
RENDER_GROUP: G5 | O32 O34 | family memory concern
```

- **`RENDER_GROUP`** — the members express one factual proposition. `05` renders it once, using the member whose wording carries the most, and may fold a `COURSE` modifier from another member.
- **`COMPOSE_GROUP`** — the members are distinct pieces of one decision. `05` renders them as one line when they are compatible — `apixaban held, to resume once MRI excludes hemorrhage` — and as separate lines when they are not.
- Every member keeps its `O#` and its provenance. A group never deletes an object; it decides how many lines it becomes.
- An object may be in at most one group, and a group may not span problems.
- An ungrouped object renders on its own, as today.

## 3. Who decides the groups

`03`. It already decides selection and block ownership; grouping is the same kind of judgement, it needs the whole problem, and it must be auditable. Putting it in `03` also means the decision is visible in an artifact rather than re-derived at render time.

`04` passes the group lines through verbatim, next to the entries, and keeps dereferencing every member. `05` stops deciding equivalence and starts formatting groups.

That is the division the project already uses elsewhere: decide once, mechanically, then render.

## 4. What `05` does with a group

- One bullet per group, not one per member.
- The bullet's content is the union of the members' facts; no member's distinct content may vanish. If two members carry different facts, the group is wrong, not the bullet short.
- Provenance: the group's members keep their markers; the rendered bullet carries the attribution of the member whose wording it uses, plus any other marker that adds clinical attribution.
- A `COMPOSE_GROUP` whose members are incompatible — a hold with no condition, two contradictory states — renders as separate lines and the group is reported as malformed. `05` does not invent compatibility.
- Everything else `05` does today is unchanged.

## 5. Frozen-case groups

| Group | Members | Kind | Rendered |
|---|---|---|---|
| G1 | O7, O8, O53 | RENDER | known left MCA infarct, two years prior to presentation (prior neurology, 2024-02) |
| G2 | O12, O25 | COMPOSE | apixaban held since admission, to resume once MRI excludes hemorrhage |
| G3 | O17, O44 | RENDER | CT head without hemorrhage or acute abnormality |
| G4 | O23, O39 | RENDER | the MRI will tell us |
| G5 | O32, O34 | RENDER | family's concern about her memory, not today's issue |

`O18` encephalomalacia and `O19` no new focal lesion stay ungrouped: they are distinct findings and folding them into G1 or G3 is a judgement this proposal does not make.

## 6. Validation

- Every retained `O#` appears in exactly one group or in none.
- No group spans problems, repeats an object, or contains a discarded object.
- A checker can verify all three mechanically.
- The three-run protocol then measures what remains: wording and ordering, not fact grouping.

## 7. What this does not fix

- Whether a group is clinically right. That is `03`'s judgement, reviewed like any other selection.
- Wording drift between runs. It reduces the surface but does not remove it.
- The `05` prose. Nothing is added to it beyond the group rules in §4.

## Out of scope

Substrate, `01`, `02`, `06`, `07`, the six kinds, P005, and any change to the accepted rendering rules.
