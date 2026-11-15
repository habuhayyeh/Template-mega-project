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
