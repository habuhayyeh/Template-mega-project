# DeepSeek proposal 006 — how each function should be performed

Broad performance guidance: how to do it, what to do, what not to do. No prompts, no schemas.

---

## I1 Source Map — work top-down from the paste's own structure

**Do:** use the signer's headings, labels, blank lines and speaker turns as the boundaries; preserve the order they pasted; mark anything unclassifiable as unlabelled.
**Don't:** infer a source family from content plausibility ("this sounds like a prior note"); merge two sources into one; reorder to look tidy.

## I2 Span Registry — cut mechanically, never interpret

**Do:** split at line, utterance or turn boundaries; keep character offsets; leave a block with no separators as one span and flag it.
**Don't:** split mid-sentence because it "contains two ideas"; merge turns; renumber spans after the fact.

## I3 Object Extraction — read each span once, enumerate propositions

**Do:** one proposition per object; keep the source's wording, including hedges, negatives and numbers; over-produce rather than under-produce.
**Don't:** paraphrase into cleaner clinical language; summarise a span; merge propositions from different spans; drop a hedge because it reads awkwardly; decide relevance.

## I4 Source Annotation — copy metadata, never derive it

**Do:** attach the source, its date, the speaker where named, and the span id; leave a field absent when the source is silent.
**Don't:** infer a date from context; infer a speaker from plausibility; turn an implication into provenance.

## S1 Problem Model — group by subject, then name

**Do:** group objects by clinical subject; choose one claim per problem; order by acuity then management weight; declare hierarchy only where the source does.
**Don't:** decide duplicate identity; assign sections; write any prose; create a problem with no claim.

## S2 Semantic Adjudication — resolve relations, not wording

**Do:** canonicalise duplicates; attach modifiers and conditions; assign reasoning roles; decide adoption from explicit statements.
**Don't:** infer adoption from the drug or the action; merge two distinct propositions; alter an object's text.

## S3 Content Selection — account for every object

**Do:** mark each object retained or omitted with a reason; assign problem use; permit explicit cross-problem reuse.
**Don't:** drop anything silently; create a new object; choose a section or operator.

## S4 Note Blueprint — compile decisions into typed units

**Do:** choose sections and their order; assign units, operators, order and bucket; run completeness; admit zero-member units only for standing items with a satisfied trigger.
**Don't:** write prose; invent a unit; leave an object unaccounted; emit a unit that does not typecheck.

## R1 Unit Realization — execute the operator, nothing else

**Do:** one line per unit; the operator's fixed text plus designated folds; section-scoped voice and surface rules.
**Don't:** select, merge, reorder, omit, add a word, or repair a broken unit — emit `CONTRACT_ERROR` instead.

## R2 Section Composition — join, then stop

**Do:** keep unit order; form paragraphs; add punctuation and whitespace.
**Don't:** delete, reorder, rewrite, merge two units into a sentence, add a temporal or causal connective, or apply to the A/P at all.

## R3 Note Assembly — follow the blueprint

**Do:** emit the sections in the IR's order with headings from IR identifiers; apply the final format.
**Don't:** add, omit, reorder or edit a section.

---

## The rule that applies to all eleven

Each function has one job and one failure mode. When it cannot do its job within its contract, it **stops and reports** — it does not widen its remit to make the note work.

That is the failure pattern we paid for repeatedly on `main`: a stage quietly doing the next stage's job because the input was ambiguous. `R1` adding a connective, `S2` choosing a section, `I3` cleaning up the wording — each looked helpful and each destroyed attributability.

Two specific consequences worth stating because they are the ones most likely to be violated:

- **No function fills a gap by inference.** If a span has no clinical content, that is a disposition. If a unit has no members, that is only legal for a standing item. If a problem has no claim, the run fails.
- **No function improves the source.** Extraction keeps the hedge, the redundancy and the patient's phrasing. Improvement happens once, in S2's adjudication, and only as a relation between objects — never as a rewrite.
