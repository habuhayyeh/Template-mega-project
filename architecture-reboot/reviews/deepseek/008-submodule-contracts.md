# DeepSeek response 008 — submodule interface contracts

**Verdict: ACCEPT all eleven, with two additions.** The re-cut resolves three of my six open questions cleanly. Two remain, and both are one sentence each.

---

## 1. Decisions on each submodule

| Submodule | Decision |
|---|---|
| I1 Source Map | ACCEPT |
| I2 Span Registry | ACCEPT |
| I3 Object Extraction | ACCEPT |
| I4 Source Annotation | ACCEPT |
| S1 Problem Model | ACCEPT |
| S2 Semantic Adjudication | ACCEPT |
| S3 Content Selection & Problem Use | ACCEPT |
| S4 Note Blueprint / Unit Compilation | ACCEPT **with addition 2** |
| R1 Unit Realization | ACCEPT |
| R2 Section Composition | ACCEPT **with addition 1** |
| R3 Note Assembly | ACCEPT |

## 2. What the re-cut settles

- **Projection vs compilation (my Q1)** — solved. S3 is the set, S4 is the shape, and the interfaces make it explicit: S3 "does not choose section or operator"; S4's output has section assignment, operator, order.
- **Section list and order (Q2)** — solved. S4 owns the ordered section list, which is where sections are built. Better than my suggestion of putting it in a completeness step.
- **Completeness (Q3)** — solved as `completeness status` on S4's output. I would have made it its own submodule for attributability; folding it in is acceptable, with the cost that a missing unit and a malformed unit are the same submodule's failure. Not worth another submodule.
- **Identifiers and headings (Q6)** — solved implicitly: R3 assembles "exactly according to the STRUCTURE-supplied section blueprint", so the furniture comes from the IR, not from RENDER. That is the right owner.

## 3. Addition 1 — R2 must be bounded, and must not touch the A/P

As written, R2 turns "already-rendered, already-ordered units of one section into coherent section text". That is unbounded enough to become a second renderer, and it does not say the A/P is exempt.

Add:

> R2 may join adjacent units in unit order and may add punctuation and whitespace. It may not delete, reorder, or merge two units into a new sentence, and may not introduce a temporal or causal connective that no unit contains.
>
> R2 applies only to sections whose contract declares prose composition. The A/P is a bullet list; it bypasses R2 entirely.

Without the second sentence, the first thing R2 will do is turn a bullet list into paragraphs, and CHECK will not be able to say whether that was allowed.

## 4. Addition 2 — S4 must admit units with no objects

`Seizure precautions` is a required A/P line with no source object. Every interface in the document assumes a unit references object payload; nothing permits a unit with empty membership.

Add to S4:

> A unit may have zero members only when its operator is a closed-list standing item, and only when that item's trigger is satisfied by the problem's claim. Such a unit is subject to the same completeness accounting as any other.

Without it, either the standing item cannot be represented, or it gets smuggled in as a fabricated object — which is the failure we spent a day removing.

## 5. Result

With those two sentences, the module/submodule/goal/input/output layer is complete and I have no further questions at this level. Schema, operator list and unit ids remain downstream and untouched.
