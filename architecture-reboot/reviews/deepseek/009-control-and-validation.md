# DeepSeek response 009 — control mode vs validation mode, and one disagreement

**Agreed:** 1, 2, 4, 5, 6, 7. **Partly disagreed:** 3.

---

## 1. What I concede

- **No S1↔S2 loop.** You are right and my worry was misplaced: problems are grouped by clinical subject, not by object identity, so a duplicated fact cannot by itself split a problem. S2 flags a conflict; that is enough. Withdrawn.
- **I1 and I4 are hybrid.** Classifying a pasted block as a prior note rather than imaging is inference, and whether an annotation is supported by its span is a judgement. Presence and shape are mechanical; support is not.
- **Duplicate identity is not generally mechanical.** "Never mechanical" was too absolute. Exact-normalised pairs and containment pairs are safely rule-resolvable; the rest is judgement.
- **R2 is hybrid.** Join-only is checkable; "semantically unchanged" is not, in general.
- **Do not freeze one fifth.** Agreed — measure the remainder.

## 2. Where I hold, and why

**I3 must keep a mechanical anti-fabrication check, or the system loses its only defence against invented words.**

You are right that literal substring is too strict: normalising "no fever" to "afebrile" is legitimate and would fail it.

But "exact source anchoring" alone is not a check — every object can be anchored to a span and still contain a word the span never said. That is precisely the `postictal confusion resolved` failure: it was anchored, plausible, and invented.

Replace substring with **content-token containment**:

> Every content token of an object — noun, verb, adjective, adverb, number, negation — must appear in its anchor span, after a closed morphology normalisation (plural/singular, verb tense, abbreviation table). Function words are exempt.

This is mechanical, it permits legitimate normalisation, and it fails any invented clinical word, including `resolved`. The morphology list is small and closed, and it is itself testable against fixtures.

If that is too strict for some operator, the exemption should be an explicit same-span synonym pair in the closed table — not a general licence.

## 3. The per-submodule control and validation table

`L` = language model judgment. `P` = program control with a model call inside. `D` = deterministic. Validation: `M` mechanical, `S` semantic audit, `H` human.

| Submodule | Control | Validation | Failure behaviour |
|---|---|---|---|
| I1 Source Map | L | M for coverage, S for family | unknown block stays `UNLABELLED`, never guessed |
| I2 Span Registry | D | M | uncuttable block becomes one span and is flagged |
| I3 Extraction as text | L | **M — token containment** | object rejected and the span falls to `NOT_CLINICAL` review |
| I3 kind assignment | L | S | downstream conflict surfaces in S2 |
| I4 Annotation | P (assemble) + L (support) | M presence, S support | object without anchor is rejected |
| S1 Problem Model | L | S | problem without a claim fails closed |
| S2 Adjudication | L | M for shape, S for identity | unresolved duplicate fails closed |
| S3 Selection | L | M (total accounting) | an orphan object fails the run |
| S4 Blueprint | L | M (typing, completeness, sections) | any typecheck failure fails the run |
| R1 Realization | L | M (line↔unit, token coverage, voice) | `CONTRACT_ERROR`, run fails |
| R2 Composition | L | M for join order, S for meaning | falls back to unit-per-line, and the fallback is recorded |
| R3 Assembly | D | M | output refused |

Two entries deserve comment.

**S4 is `L` with `M` validation, and that is the right shape.** The blueprint is the most decision-dense artifact in the system and it is produced by a model; what makes it safe is that its output is typed and completely checkable. That is the pattern the stress suite validated.

**R2 falling back to unit-per-line** is deliberate: if composition cannot be shown to preserve order, emitting one unit per line is a faithful, if plainer, note. Degrading the prose is better than degrading the content.

## 4. What still needs measuring, not deciding

The share of decisions that are semantic rather than mechanical. I will not put a number in the architecture; the E1 run should report, per submodule, how many decisions were rule-resolved and how many required judgement. Then the claim about reproducibility can be scoped to a measured fraction instead of an asserted one.
