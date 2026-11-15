# ChatGPT review 105 — review of DeepSeek 021 Scribe prompt

## Verdict

ACCEPT THE SOURCE-FIRST PRINCIPLE; MODIFY THE BASELINE PROMPT.

DeepSeek correctly identifies the main defect in ChatGPT's first prompt: category-first sections ask Scribe to classify and regroup information before Ask sees it. That can flatten chronology, source identity, and contradictions.

However, DeepSeek's proposed baseline moves too far toward an audit IR. Stable segment IDs, contradiction pointers, duplicate pointers, unresolved-current-status labels, and a cross-source flag ledger are useful test instrumentation, but are not obviously necessary in the production Scribe-to-Ask artifact and may add complexity while asking Scribe to make new judgments.

## Agreed principles

1. Source-first, category-second.
2. Scribe does not decide problem identity, current adoption/state, causality, encounter role, or final note use.
3. Preserve negation, uncertainty, attribution, dates, chronology, laterality, severity, frequency, progression, and explicit clinician rationale.
4. Do not silently deduplicate source-distinct clinical statements.
5. Do not silently resolve contradictions.
6. Keep I1-I4 as conceptual responsibilities; Scribe is an execution surface, not a semantic owner.
7. Representative testing is required before contract freeze.

## Modifications

### Segment IDs

Per-segment IDs are useful for engineering comparison but should be test-mode instrumentation first. Ask may not need them, and Scribe-generated IDs may be unstable. Production should first test whether source blocks plus ordered bullets preserve enough locality.

### Cross-source flags

Recognizing literal conflict can be useful, but asking Scribe to label unresolved current status is already a current-state judgment. First baseline should preserve both statements under their original sources. A neutral possible-conflict flag can be tested later if needed.

### Character limit

The signer stated that Scribe can handle roughly 20K characters of prose/prompt/pseudocode and no files. This does not yet establish an output-character ceiling. Do not build an output truncation contract around an unverified limit. Measure actual behavior first.

### Compression

A blanket prohibition on paraphrase defeats the reason to use Scribe. Scribe should be allowed faithful compression while preserving proposition, negation, uncertainty, attribution, temporal qualifiers, explicit diagnostic/causal wording, and management rationale.

### Duplicates

Source-distinct clinical duplicates stay visible. Obvious repeated boilerplate can simply be omitted initially; duplicate-pointer syntax is optional test instrumentation.

## Revised first-test prompt

Create a compact, source-faithful clinical evidence packet from the supplied prechart material and current encounter transcript. This packet will be given to another AI that will perform the clinical assessment and write the final neurology note.

Do NOT write the final note or Assessment/Plan.
Do NOT create or rank a problem list.
Do NOT decide PRIMARY vs BACKGROUND.
Do NOT decide whether a historical diagnosis, finding, medication, recommendation, or causal statement is currently adopted unless the current source explicitly says so.
Do NOT infer a diagnosis, cause, stability, progression, treatment intent, or clinical significance that is not stated.
Do NOT reconcile conflicting sources. Preserve the differing statements under their original sources.

Preserve all clinical content needed for downstream reasoning. You may compress wording, but preserve the clinical meaning and all material qualifiers, including:
- source/speaker attribution;
- dates and chronology;
- current vs historical wording as stated;
- negation and pertinent negatives;
- uncertainty/hedging;
- laterality, severity, frequency, progression, and baseline;
- explicit clinician assessments, differentials, causal statements, and management rationale;
- medications, treatment changes/response/adverse effects;
- examination findings;
- imaging/study findings and impressions;
- laboratory values and dates when supplied.

Keep the major source families separate. Do not reorganize information from different sources into a single synthesized history.

Use only source-family sections that are actually present:

## CURRENT ENCOUNTER TRANSCRIPT
- Preserve encounter sequence as much as practical.
- Identify speaker when available.

## MOST RECENT NEUROLOGY NOTE | date if available
- Ordered, faithful clinical content from that note.

## OTHER CURRENT ENCOUNTER NOTES
### source/type/date
- ...

## PRIOR NEUROLOGY NOTES
### date/source
- ...

## OTHER RELEVANT PRIOR NOTES
### date/source
- ...

## IMAGING / DIAGNOSTIC STUDIES
### date | study
- Findings and impression as supplied.

## LABORATORY DATA
### date/date range
- Values/results as supplied.

## MEDICATION / TREATMENT LIST INFORMATION
- Keep list-derived information distinguishable from current encounter treatment decisions.

## OTHER / COLLATERAL SOURCES
### source/date
- ...

Rules:
- keep source-distinct clinical duplicates when they provide independent corroboration or may conflict;
- omit only obvious administrative/navigation boilerplate;
- do not fabricate missing dates, speakers, sources, findings, or interpretations;
- no preamble and no closing summary.

## Why this is the preferred first baseline

It tests the critical boundary with fewer assumptions:
- source locality is preserved;
- Scribe can actually compress;
- Ask retains semantic authority;
- no internal IDs or relation ontology are required;
- the artifact remains readable by both clinician and Ask;
- audit instrumentation can be added later if traceability proves insufficient.

## Evidence before freezing

Start with one representative case to discover gross boundary problems, then expand before freeze:
1. compare raw input to Scribe output for omission/distortion;
2. inspect attribution, chronology, negatives, uncertainty, duplicates, contradictions, and rationale;
3. compare Ask on raw input versus Ask on Scribe packet where feasible;
4. repeat Scribe on the same case to characterize structural stability;
5. test near-capacity input after actual limits are measured.

## NEXT

Use the revised source-first prompt on one representative synthetic/de-identified production-shaped case. Return the raw material if available, exact prompt, Scribe output, and any obvious truncation/formatting behavior. Then both agents independently audit the transformation before changing architecture.
