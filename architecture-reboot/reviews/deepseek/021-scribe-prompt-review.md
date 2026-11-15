# DeepSeek review — baseline Scribe prompt and Scribe/Ask boundary

**Scope:** review only. No implementation. This evaluates the candidate Scribe prompt in the
2026-11-15 channel request under D-034.

## Verdict

The **responsibility boundary is directionally right**, but the proposed prompt is **too semantic and
too category-first** for a source-preserving ingestion surface. It will produce a polished summary that
looks organized but loses source identity, chronology and contradiction locality.

Scribe should produce a **source-faithful evidence packet**, not a mini-note. Ask should own problem
identity, adoption, causality, encounter role and note use.

## Q1 — Is this the right responsibility boundary?

At the highest level, yes:

- Scribe: ingest, preserve, segment, label, compress without semantic adjudication;
- Ask: semantic structure, problem identity/containment, current-encounter state, causality, note use,
  final rendering.

But the prompt crosses the boundary in the output headings. Sections such as
`CURRENT ENCOUNTER — CLINICIAN FORMULATIONS`, `PRECHART — NEUROLOGIC HISTORY` and
`CURRENT ENCOUNTER — MANAGEMENT` require Scribe to classify clinical material by semantic role. That is
already a small act of adjudication, and it destroys source locality.

**Recommendation:** source-first, category-second. Scribe preserves source blocks and labels facts; Ask
does the semantic categorization.

## Q2 — Which instructions are too broad, too narrow, redundant, or hidden decisions?

### Too broad / undefined

1. **“Capture all clinically meaningful information.”** “Clinically meaningful” is the exact judgment
   Scribe is told not to make. Replace with “all clinical content; omit only explicitly nonclinical
   administrative boilerplate.”
2. **“Do not omit a fact merely because it appears redundant.”** This conflicts with the 20K limit.
   Preserve source-distinct duplicates and contradictions; allow deduplication only for exact
   boilerplate with an explicit `DUPLICATE_OF` pointer.
3. **“Preserve source whenever identifiable.”** “Whenever identifiable” makes provenance optional.
   Make source ID mandatory for every segment.
4. **“Preserve explicit clinician assessments ... as stated”** is right, but the heading
   `CLINICIAN FORMULATIONS` invites Scribe to decide what counts as a formulation. Better: label the
   speaker/source and preserve the statement; Ask classifies it.

### Too narrow / missing

- no stable source IDs and segment IDs;
- no rule for exact duplicates vs near-duplicates;
- no rule for OCR/illegible text;
- no inline contradiction/uncertainty markers;
- no output budget or truncation policy;
- no instruction to preserve source order and line boundaries;
- no rule for prior notes quoted inside the current encounter;
- no rule for missing/empty sections (do not fabricate headings);
- no explicit “no preamble/no closing summary.”

### Redundant

Several “do not infer” rules are instances of one principle. Keep one source-fidelity rule plus concrete
examples (negation, uncertainty, causality, current status, attribution). Repetition increases prompt
length without adding coverage.

### Hidden semantic decisions

The category headings and “clinically meaningful” language are the main hidden decisions. Scribe can
also silently reconcile chronology by reordering facts under headings. Preserve original order.

## Q3 — Does the output structure preserve provenance?

No. Grouping by semantic category breaks source identity and context:

- a prior note’s statement can be filed under “current clinician formulations”;
- a current patient statement can be filed under “prechart history”;
- contradictions are moved to a separate section, losing which source said what;
- chronology is replaced by category order;
- attribution becomes a heading rather than a per-segment label.

Use source blocks first, with per-segment IDs and source/date/speaker labels. Semantic grouping belongs
downstream.

## Q4 — Should the first experiment preserve source blocks literally?

**Yes.** The first experiment should preserve:

- transcript;
- most recent neurology note;
- prior notes;
- imaging/studies;
- labs;
- medication list;
- other source families.

Structure only within each source: source ID, source type, date/author, ordered segments, speaker,
verbatim/faithful text. No cross-source semantic sections on the first pass.

## Q5 — What is most at risk of being lost?

In order:

1. **Current-vs-historical status** — category headings and summary compression flatten it.
2. **Attribution/source identity** — “whenever identifiable” and cross-source grouping.
3. **Contradictions** — moving them to a summary section loses source locality and can hide one side.
4. **Negation and uncertainty** — any paraphrase is dangerous; preserve exact qualifiers.
5. **Chronology** — reordering by category destroys sequence.
6. **Repeated facts across sources** — deduplication loses independent corroboration/conflict.
7. **Management rationale and clinician reasoning** — easily summarized into a conclusion.
8. **Pertinent negatives** — often dropped as “no finding.”

## Q6 — What to prioritize under the ~20K limit?

Priority order:

1. current encounter, verbatim/faithful, including negatives and uncertainty;
2. current/active medications, management, studies and results;
3. most recent relevant prechart note with dates and attribution;
4. older/background material needed for problem identity or causality;
5. duplicates and boilerplate last.

Compression rules:

- remove administrative/navigation boilerplate first;
- collapse exact duplicate boilerplate to a `DUPLICATE_OF` pointer;
- never drop a contradiction, a qualifier, or a source-distinct statement to save space;
- if truncation is unavoidable, emit an explicit `OMITTED` list with source IDs and reason; do not
  silently summarize.

Do not let Scribe rewrite clinical statements into shorter prose to fit the budget. Compact line format
is safer than paraphrase.

## Q7 — Does Scribe imply collapsing or removing I1–I4?

**No.** Move mechanical extraction/formatting to Scribe; do not remove the responsibilities.

- I1/I2 source capture and provenance: Scribe can produce the source-labeled evidence packet; Ask (or a
  shared validator) still verifies coverage and provenance.
- I3/I4 object/state extraction: Scribe can preserve candidate facts; Ask still owns semantic adoption,
  contradiction resolution, problem identity and current-vs-historical judgment.
- Do not let Scribe resolve contradictions, infer adoption, causality, stability or final problem
  architecture.

Scribe is a **surface**, not a new semantic owner.

## Q8 — Smallest baseline Scribe prompt to test first

```text
Convert the supplied prechart material and encounter transcript into a source-faithful evidence packet
for a downstream clinical reasoner.

Do NOT write a note, problem list, assessment, or plan. Do NOT decide importance, adoption, current
status, causation, stability, treatment intent, or problem identity. Do NOT merge sources.

OUTPUT
For each source, in the order supplied:

## SOURCE <id> | <type> | <date/author if present>
<one faithful segment per line, with a stable segment id>
Format each segment:
[<segment-id>] [<speaker/source label>] <text>

Rules:
- preserve negation, uncertainty, attribution, dates, times, laterality, severity, frequency and
  chronology exactly as stated;
- preserve explicit clinician statements and rationales as statements, not conclusions;
- keep prior/chart text separate from current encounter text;
- do not turn a prior statement into a current one;
- do not resolve contradictions; mark them inline as CONTRADICTS <segment-id> when identifiable, and list
  them again under CROSS-SOURCE FLAGS;
- exact duplicate boilerplate may be replaced by DUPLICATE_OF <segment-id>; do not deduplicate
  source-distinct clinical statements;
- omit only administrative/navigation boilerplate; mark OCR/illegible text as [ILLEGIBLE] or
  [UNCERTAIN OCR];
- no preamble, no closing summary.

## CROSS-SOURCE FLAGS
- CONTRADICTION: <segment-ids> — <short neutral description>
- DUPLICATE: <segment-ids>
- UNRESOLVED CURRENT STATUS: <segment-ids>

If the output approaches the character limit, keep current encounter, active management/medications and
the most recent relevant prechart first; emit an explicit OMITTED list with source/segment ids and
reason. Never silently paraphrase to fit.
```

This is safer because it preserves source blocks, per-segment provenance, chronology and qualifiers; it
tests compression without asking Scribe to make semantic classifications.

## Q9 — Evidence needed before freezing Scribe -> Ask

1. At least three representative synthetic/de-identified input packets with:
   - transcript + recent note + old note + imaging + labs + medication list;
   - duplicate facts, contradictions, OCR noise, missing dates, quoted prior statements;
   - realistic length near/over the 20K boundary.
2. Scribe output for each, with character count and explicit omissions.
3. A coverage matrix comparing source facts to Scribe segments:
   - negation, uncertainty, attribution, chronology, current-vs-historical, contradictions, repeated
     facts, management rationale;
   - false additions / inferred conclusions.
4. Ask run on the Scribe output vs Ask on raw input, using the same final template. Compare:
   - problem identity/containment;
   - adoption/current status;
   - causal relations;
   - note structure and source fidelity.
5. A failure taxonomy: lost fact, distorted qualifier, merged source, hidden contradiction, invented
   semantic decision, truncation loss.
6. Repeated runs to check stability, not a single polished sample.

Freeze the contract only after the failure taxonomy is acceptable and no semantic authority has moved
upstream by accident.

## Recommendation

Adopt the source-first baseline prompt for the first experiment. Keep Ask as the semantic owner. Do not
use the category-first prompt as the baseline; it optimizes presentation and risks exactly the source
fidelity D-034 is meant to preserve.

No Gate-0 acceptance. No Doximity. No Phase 0.
