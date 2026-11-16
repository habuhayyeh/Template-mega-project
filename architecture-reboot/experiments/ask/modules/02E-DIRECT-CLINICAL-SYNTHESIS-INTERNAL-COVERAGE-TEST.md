# DIRECT-B FOLLOW-UP — INTERNAL SOURCE_COVERAGE CENSUS

## EXECUTION GATE

1. Read this entire instruction file before producing output.
2. Read the complete input packet before starting.
3. Do not draft, stream, or emit output while reading.
4. Silently complete these phases in order:
   - READ
   - CENSUS
   - CHECK CENSUS
   - SYNTHESIZE
   - CHECK SYNTHESIS
   - EMIT
5. Do not start SYNTHESIZE until the complete SOURCE_COVERAGE census exists internally.
6. Do not emit the census while building it.
7. Do not emit reasoning, scratch work, progress text, or partial results.
8. Output schemas define allowed structure.
9. Do not infer values only to fill a schema.
10. Omit optional fields when unsupported.

**Experimental condition:** B-DIRECT-INTERNAL-COVERAGE-V1

## Purpose

Test whether direct clinical synthesis becomes reliable when source coverage is enumerated before synthesis in the same B invocation.

This is not a new runtime stage.

Do not generate Stage A.

Do not reproduce source selectors.

Do not copy source text into citation fields.

Do not decide note sections.

Do not write final note prose.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

==================================================
PHASE 1 — SOURCE_COVERAGE
==================================================

Before clinical synthesis, inspect the complete packet and build one internal record-ID census.

Use only record IDs that exist in the packet.

Use these categories:

CURRENT_EVENT
BASELINE_COMPARATOR
NEURO_HISTORY
MEDICATION_CONTEXT
EXAM
WORKUP
ACTION_BEARING
CONTEXT

A record may appear in more than one category.

Do not force every record into a category.

Do not use selectors.

Do not copy source text into the census.

Do not create semantic claims.

Do not reconcile records.

Do not decide:
- problem identity;
- PRIMARY/BACKGROUND;
- diagnosis;
- evidence versus counterevidence;
- action ownership;
- final plan;
- note section.

### CURRENT_EVENT

Include records needed to recover the presenting neurologic event or event chronology.

### BASELINE_COMPARATOR

Include records describing a baseline, chronic, or prior phenomenon that may need comparison with the presenting event.

Do not decide whether it is a separate problem.

### NEURO_HISTORY

Include neurologic history needed downstream, including prior seizure history and relevant family neurologic history.

### MEDICATION_CONTEXT

Include medication, treatment, supplement, and exposure records needed downstream.

### EXAM

Include current examination records needed downstream.

### WORKUP

Include relevant testing, procedures, results, outside testing, result availability, and review-status records.

### ACTION_BEARING

Include every record containing a clinically meaningful:
- test/procedure action;
- medication/treatment action;
- consultation;
- disposition action;
- precaution;
- safety counseling;
- driving/activity counseling;
- follow-up action;
- other management action.

### CONTEXT

Include clinically relevant non-neurologic context that may change downstream neurologic interpretation or management.

If uncertain whether a record belongs in a category, include it rather than silently drop it.

==================================================
PHASE 1 CHECK — CENSUS COMPLETENESS
==================================================

Before synthesis, check the internal census.

Ask:

1. Is current-event chronology recoverable?
2. Is baseline/prior symptom material recoverable?
3. Is prior seizure/neurologic history recoverable?
4. Is relevant family neurologic history recoverable?
5. Are medications/supplements recoverable?
6. Is the current neurologic examination recoverable?
7. Is relevant workup/result state recoverable?
8. Is every clinically meaningful action-bearing record represented?
9. Is relevant context recoverable?

If a required category is missing because no such source exists, continue.

If a source exists but was omitted, correct the census before synthesis.

Do not begin synthesis until this check is complete.

==================================================
PHASE 2 — CLINICAL SYNTHESIS
==================================================

Now synthesize from:

1. the complete Scribe packet; and
2. the completed internal SOURCE_COVERAGE census.

The census is a required recovery map.

Do not ignore a census category merely because the main problem can be synthesized without it.

Decide:

- neurologic problem structure;
- diagnostic stance;
- same versus distinct episode relationships when supported;
- compact preservation of clinically necessary body evidence;
- clinical action identity;
- action ownership;
- concise source-qualified action wording.

==================================================
SOURCE-REFERENCE RULE
==================================================

Use stable Scribe record IDs only.

Allowed:

```text
source_records=T123
```

or:

```text
source_records=T123,T124
```

Rules:

1. Every cited record ID must exist in the packet.
2. Every cited record must materially support the associated output.
3. Cite every record that materially supports the output.
4. Do not substitute a neighboring question record for an answer record.
5. Do not copy or reconstruct selectors.
6. Do not import state, chronology, provenance, or action meaning from an uncited record.
7. If multiple records are needed, cite all of them.
8. If one record is too broad for a required distinction, mark unresolved rather than inventing a selector.

==================================================
OUTPUT
==================================================

Return only:

```text
@@HANDOFF B_DIRECT_INTERNAL_COVERAGE_V1

SOURCE_COVERAGE
  current_event_records=<record IDs or NONE>
  baseline_comparator_records=<record IDs or NONE>
  neuro_history_records=<record IDs or NONE>
  medication_context_records=<record IDs or NONE>
  exam_records=<record IDs or NONE>
  workup_records=<record IDs or NONE>
  action_bearing_records=<record IDs or NONE>
  context_records=<record IDs or NONE>

CLINICAL_SYNTHESIS

PROBLEM P001
  label=<minimal source-supported neurologic problem formulation>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  diagnostic_stance=<concise source-supported assessment>
  evidence_records=<one or more Scribe record IDs>
  counterevidence_records=<one or more Scribe record IDs>
  contains=<contained manifestations or comparison descriptors when useful>
  separate_from=<distinct problem handles when needed>
  order=<integer>

CLINICAL_UNIT CU001
  unit_type=<current_event|baseline_comparator|neuro_history|medication_context|exam|workup|context>
  source_records=<one or more Scribe record IDs>
  chronology=<only if directly supported by cited records and clinically needed>
  problem_relation=<P001|BACKGROUND problem handle|nonproblem|unresolved>
  unresolved=<only when needed>

ACTION_VIEW AV001
  source_records=<one or more Scribe record IDs>
  target=<concise action target>
  wording=<concise source-qualified wording supported by cited records>
  owner=<problem handle or nonproblem>
  unresolved=<only when needed>

SYNTHESIS_UNRESOLVED X001
  topic=<short unresolved issue>
  source_records=<one or more Scribe record IDs>
  issue=<why it cannot be safely reconciled>

@@END
```

The emitted SOURCE_COVERAGE block must match the internal census used for synthesis.

Do not emit copied source text in SOURCE_COVERAGE.

==================================================
CLINICAL_UNIT RULE
==================================================

A CLINICAL_UNIT preserves clinically necessary evidence for downstream note construction.

It is not an atomic fact ledger.

Use the minimum sufficient set.

Do not emit one unit per source record.

Use:
- current_event;
- baseline_comparator;
- neuro_history;
- medication_context;
- exam;
- workup;
- context.

The SOURCE_COVERAGE census may contain more records than the final CLINICAL_UNIT set.

That is expected.

Coverage census = do not overlook.

CLINICAL_UNIT = compact downstream representation.

==================================================
PROBLEM THRESHOLD
==================================================

Create a separate problem only when it has:

- independent neurologic disease identity relevant to this encounter; or
- its own current assessment question; or
- its own current management.

Use this counterfactual:

> If the primary presenting problem were removed, would this item still justify its own neurologic assessment/problem block?

If no:
- keep it as a CLINICAL_UNIT;
- or use it as evidence/counterevidence;
- do not create a separate problem.

A chronic baseline spell does not become a BACKGROUND problem solely because it differs from the presenting event.

==================================================
DIAGNOSTIC STANCE
==================================================

Preserve:
- uncertainty;
- favored or suspected possibilities;
- important alternatives still under evaluation;
- baseline-versus-current distinctions.

Do not:
- upgrade suspicion to diagnosis;
- collapse a differential to one diagnosis;
- use management intensity as diagnostic proof.

==================================================
ACTIONS
==================================================

Every clinically meaningful action represented in ACTION_BEARING must be considered during action synthesis.

Represent all distinct action concepts needed downstream.

Include:
- tests/procedures;
- medications/treatments;
- consultations;
- admission/disposition;
- precautions;
- safety counseling;
- driving/activity counseling;
- follow-up;
- other neurologic management.

For a compound record:
- split distinct targets when needed;
- reuse the same source record IDs;
- do not create selectors.

Do not silently omit an ACTION_BEARING record because another action has the same target.

==================================================
ACTION WORDING
==================================================

Use ordinary source-qualified wording.

Every state in `wording` must be supported by the cited `source_records`.

Do not infer:
- order from recommendation or need;
- performance from plan;
- nonperformance from future wording;
- pending/unavailable result from silence;
- objective performance from mediated report;
- agreement from clinician preference.

If wording requires another record, cite that record.

==================================================
NO STAGE-A RECREATION
==================================================

Do not emit:
- selectors;
- copied source text;
- polarity fields;
- certainty fields;
- assertion_type fields;
- speaker registry;
- source registry;
- one span per utterance;
- exhaustive semantic objects;
- action-state enums.

==================================================
FINAL CHECK
==================================================

Before emitting:

1. Verify every SOURCE_COVERAGE record ID exists.
2. Verify no question-only record substitutes for a substantive answer when the answer exists separately.
3. Verify every synthesis source ID exists in SOURCE_COVERAGE in at least one appropriate category.
4. Verify every output statement uses only state supported by its cited records.
5. Verify current-event chronology is represented.
6. Verify baseline-comparator material is represented when present.
7. Verify neurologic/seizure history is represented when present.
8. Verify relevant family neurologic history is represented when present.
9. Verify medication/supplement context is represented when present.
10. Verify current neurologic exam is represented when present.
11. Verify relevant workup/results are represented when present.
12. Verify every clinically meaningful ACTION_BEARING record was considered and every required action concept is recoverable.
13. Verify source mediation is preserved.
14. Verify diagnostic uncertainty is preserved.
15. Verify no note-section decision appears.
16. Verify no action-state enum appears.
17. Verify output begins with `@@HANDOFF B_DIRECT_INTERNAL_COVERAGE_V1`.
18. Verify output ends with `@@END`.

Correct any internal violation before emission.

Emit the complete handoff once.

Emit nothing else.

Return the handoff only.
