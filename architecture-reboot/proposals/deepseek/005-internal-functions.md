# DeepSeek proposal 005 — internal functions, first pass

Interfaces frozen in `CONSENSUS_SUBMODULE_INTERFACES_v1.md`. This defines what each submodule *does inside* its contract. No schema, no field names.

---

## INGEST

**I1 Source Map** — identify what was pasted.
1. Segment the paste at the coarsest reliable boundaries (blank lines, headings, labels, speaker turns).
2. Classify each block into a source family: transcript, current note, prior note, imaging/study, lab, other.
3. Assign source ids and an order that preserves what the signer pasted.
4. Record unclassified blocks as `UNLABELLED` rather than guessing a family.

**I2 Span Registry** — make boundaries explicit.
1. Cut each source into spans at line, utterance, or turn boundaries — mechanical, never semantic.
2. Assign span ids and back-pointers to source and character range.
3. Preserve source order across the whole paste.
4. Flag any block that could not be cut (no separators) as one span, so coverage still works.

**I3 Object Extraction** — say what each span contains.
1. Enumerate the clinical propositions in each span.
2. Create one object per proposition, in the source's own words.
3. Assign a kind.
4. Never merge propositions from different spans; never paraphrase.

**I4 Source Annotation** — make every object traceable.
1. Attach provenance (source family, name, date), source temporality, speaker where named, span id.
2. Reject any object without a span id.
3. Record metadata the source does not support as absent, not as unknown-valued.

---

## STRUCTURE

**S1 Problem Model**
1. Group objects into candidate problems by clinical subject.
2. Name each problem and choose its claim object.
3. Order problems by acuity then management weight.
4. Declare hierarchy only where one problem explains another.

**S2 Semantic Adjudication**
1. Resolve duplicates within a problem: which object is canonical, which are covered.
2. Attach modifiers, conditions, and reasoning roles.
3. Decide encounter-level adoption for reasoning and for plan items.
4. Emit the adjudicated set with every relation decided; no section, no operator.

**S3 Content Selection & Problem Use**
1. Decide retained vs omitted per object, with a reason for every omission.
2. Assign each retained object to a problem; allow explicit cross-problem reuse.
3. Produce the use map and a total accounting of every object.

**S4 Note Blueprint / Unit Compilation**
1. Choose the section list and its order; omit empty sections.
2. Build units: membership, roles, class, operator, order, bucket.
3. Admit zero-member units only for closed-list standing items with a satisfied trigger.
4. Run completeness: every problem has a claim unit; every current plan item has a plan unit; every retained reasoning object has a unit.
5. Emit the Case IR; fail closed on any unit that does not typecheck.

---

## RENDER

**R1 Unit Realization**
1. Read the unit and its operator; select member text.
2. Apply the operator's fixed text and designated folds.
3. Apply section-scoped style: capitalisation, punctuation, abbreviations, number/time display, voice.
4. Emit exactly one line; on a malformed unit, emit `CONTRACT_ERROR` and fail the run.

**R2 Section Composition**
1. Take the section's units in IR order.
2. Join into paragraphs per the section contract.
3. Add punctuation and whitespace only; no deletion, reordering, or new connectives.
4. Do nothing for sections that bypass prose composition — the A/P in particular.

**R3 Note Assembly**
1. Read the ordered section list from the IR.
2. Emit headings and fixed furniture from IR-supplied identifiers.
3. Concatenate section texts in order.
4. Apply the final formatting contract; make no content edit.

---

## The one thing to argue about in this pass

`S1` runs before `S2`, but problem grouping needs adjudicated duplicates to avoid splitting one fact into two problems. Either S1 groups provisionally and S2 may return problems to it, or S1 consumes a first-pass duplicate resolution.

I have written the first version (provisional grouping) because it keeps S2's contract intact. The second would move duplicate resolution earlier and give S1 a dependency on part of S2's job.

---

## Checkability, tagged now rather than discovered later

Doximity was unforgiving: every failure we actually shipped was caught late, and only by a validator we wrote after the fact. Each internal function below carries a tag now, so the build knows which are enforceable and which are only reviewable.

**M** — mechanically checkable, no model. **P** — partly mechanical: a subset is checkable, the rest needs an oracle or a human. **H** — reviewable only.

| Function | Tag | What the check would be |
|---|---|---|
| I1 source classification | M | every character of the paste belongs to exactly one source block or is explicitly ignored |
| I2 span cutting | M | spans are contiguous, ordered, non-overlapping, and cover the source completely |
| I3 object extraction — recall | **P** | every span has ≥1 disposition; **object text is a substring of its span** — this is the strongest single check in the system and it catches paraphrase, fabrication, and silent summarisation at the source |
| I3 object extraction — kind | H | kind correctness needs a reader |
| I4 annotation | M | every object has a span id, a well-formed provenance triple, and no metadata the span does not contain |
| S1 problem grouping | H | whether two facts belong to one problem is clinical |
| S1 claim selection | **P** | one claim per problem, claim is a `REASONING` object, claim text present in source |
| S2 duplicate resolution | **P** | every duplicate group has exactly one canonical; no object in two groups; each non-canonical is covered by a unit that names it |
| S2 adoption | **P** | every plan/reasoning object carries an explicit `adopted` value; no adoption inferred from drug class |
| S3 selection accounting | M | every object is used or dispositioned with a reason; no orphan |
| S4 unit typing | M | every unit typechecks against its operator; every member role is permitted |
| S4 completeness | M | every problem has a claim unit; every current plan item a plan unit; every retained reasoning object a unit |
| S4 sections | M | section list ordered, no duplicate section, no empty section |
| S4 zero-member units | M | only closed-list standing items, only with a satisfied trigger |
| R1 realisation | M | one line per unit; every content word present in the unit's members or the operator's fixed text; voice rule by section |
| R2 composition | M | each unit's text appears in the section text, in unit order, and no sentence contains words from two non-adjacent units |
| R3 assembly | M | section order equals the IR list; no extra heading; nothing before the first or after the last section |

## Which of these must exist before the pipeline is trusted

Ordered by the failures they would have caught, not by pipeline order:

1. **I3 substring check** — catches fabrication and paraphrase at ingest. Our worst failure was an invented `resolved`; this check would have failed it at the source.
2. **S4 completeness** — catches a required line that never existed. That was the missing `Seizure precautions`.
3. **S3 accounting** — catches a dropped object. That was the infarct evidence vanishing between runs.
4. **R1 line-to-unit** — catches a line that is not in the IR.
5. **S4 section list** — catches a section that disappears.

The rest can follow. Those five are cheap, mechanical, and each maps to a defect that reached a clinician.

## What cannot be validated

Two functions have no mechanical check and never will: **problem grouping** and **duplicate identity**. They are clinical judgements, and the honest instrument is a reviewed oracle on a fixed case, not a validator.

That is worth stating in the architecture rather than discovering it: roughly a fifth of the system will always be audit-only, and any claim of reproducibility has to be made about the mechanical four-fifths.
