# DIRECT-B FOLLOW-UP — CLINICAL SYNTHESIS WITH CLINICAL UNITS

## EXECUTION GATE

1. Read this entire instruction file before producing output.
2. Read the complete input packet before starting.
3. Do not draft, stream, or emit output while reading.
4. Silently complete:
   - READ
   - EXTRACT
   - DECIDE
   - CHECK
   - EMIT
5. Apply all rules before committing output.
6. Do not emit reasoning, scratch work, progress text, or partial results.
7. Output schemas define allowed structure.
8. Do not infer values only to fill a schema.
9. Omit optional fields when unsupported.

**Experimental condition:** B-DIRECT-WITH-CLINICAL-UNITS-V1

## Purpose

Test whether direct clinical synthesis can preserve the clinically necessary body evidence that Stage A currently carries.

This is a follow-up experiment.

Do not generate Stage A.

Do not decide note sections.

Do not write final note prose.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

## Responsibilities

Perform clinical synthesis directly from the Scribe packet.

Decide only:

- neurologic problem structure;
- diagnostic stance;
- same versus distinct episode relationships when supported;
- action identity and ownership;
- concise source-qualified management wording;
- compact preservation of clinically necessary nonproblem/body evidence.

## Source grounding

Every cited item must use:

- one exact `source_record`;
- one exact contiguous `selector` from that same record.

Hard rules:

1. The selector must occur literally inside the cited record.
2. Do not use text from a neighboring record.
3. Do not combine text from multiple records into one selector.
4. Do not paraphrase inside a selector.
5. Do not repair a source pointer by using nearby context.
6. If a claim needs multiple records, cite each record separately.

## Output

Return only:

```text
@@HANDOFF B_DIRECT_CLINICAL_SYNTHESIS_WITH_UNITS_V1

CLINICAL_SYNTHESIS

PROBLEM P001
  label=<minimal source-supported neurologic problem formulation>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  diagnostic_stance=<concise source-supported assessment>
  evidence=<source_record + exact selector; one or more>
  counterevidence=<source_record + exact selector; one or more>
  contains=<contained manifestations or comparison descriptors when useful>
  separate_from=<distinct problem handles when needed>
  order=<integer>

CLINICAL_UNIT CU001
  unit_type=<current_event|baseline_comparator|neuro_history|medication_context|exam|workup|context>
  source_record=<exact record ID>
  selector=<exact contiguous source substring>
  chronology=<only if source-supported and clinically needed>
  problem_relation=<P001|BACKGROUND problem handle|nonproblem|unresolved>
  unresolved=<only when needed>

ACTION_VIEW AV001
  source_record=<exact record ID>
  selector=<exact contiguous source substring>
  target=<concise action target>
  wording=<concise source-qualified wording faithful to selector>
  owner=<problem handle or nonproblem>
  unresolved=<only when needed>

SYNTHESIS_UNRESOLVED X001
  topic=<short unresolved issue>
  evidence=<source_record + exact selector; one or more>
  issue=<why it cannot be safely reconciled>

@@END
```

Omit optional fields when unsupported.

## CLINICAL_UNIT rule

A CLINICAL_UNIT preserves clinically necessary evidence for downstream note construction.

It is not an atomic fact ledger.

Use the minimum sufficient set.

Do not emit one unit for every source record.

## CLINICAL_UNIT types

### current_event

Use for chronology-defining event evidence needed downstream.

Preserve only the event details needed to reconstruct the clinically important course.

### baseline_comparator

Use for a chronic or baseline phenomenon that helps distinguish the presenting event.

Do not create a separate problem unless the problem threshold is met.

### neuro_history

Use for neurologic history that affects interpretation or management.

### medication_context

Use for medications, supplements, or relevant exposure context needed downstream.

Do not reconcile conflicting lists unless supported.

### exam

Use for current examination findings needed downstream.

### workup

Use for tests, results, outside reported testing, or result-availability state needed downstream.

Preserve reported versus directly reviewed status.

### context

Use only for non-neurologic context that changes neurologic interpretation or management.

## Coverage floor

Before returning, verify that the handoff preserves, when present in the packet:

1. current presenting neurologic event chronology;
2. clinically meaningful baseline comparator;
3. prior neurologic history relevant to the encounter;
4. seizure-history information;
5. family neurologic history when relevant;
6. medication/supplement context relevant to the encounter;
7. current neurologic examination;
8. relevant outside and current workup/results;
9. clinically relevant non-neurologic context.

Do not preserve unrelated material solely for completeness.

## Problem threshold

Create a separate problem only when it has:

- independent neurologic disease identity that is relevant to this encounter; or
- its own current assessment question; or
- its own current management.

Use this counterfactual:

> If the primary presenting problem were removed, would this item still justify its own neurologic assessment/problem block?

If no:

- keep it as a CLINICAL_UNIT;
- or keep it as evidence/counterevidence;
- do not create a separate problem.

A chronic baseline spell does not become a BACKGROUND problem solely because it differs from the presenting event.

## Diagnostic stance

Preserve:

- uncertainty;
- favored or suspected possibilities;
- important alternatives still under evaluation;
- baseline-versus-current distinctions.

Do not:

- upgrade suspicion to diagnosis;
- collapse a differential to one diagnosis;
- use management intensity as diagnostic proof.

## Actions

Enumerate every distinct clinical action relevant to the neurologic encounter.

Include:

- tests/procedures;
- medications/treatments;
- consultations;
- admission/disposition;
- precautions;
- safety counseling;
- driving/activity counseling;
- other neurologic management.

Split distinct targets when combining them would lose downstream meaning.

Do not create action-state enums.

## Action wording

Use ordinary source-qualified wording.

Do not infer:

- order from recommendation or need;
- performance from plan;
- nonperformance from future wording;
- pending/unavailable result from silence;
- objective performance from mediated report;
- agreement from clinician preference.

## Source-qualified outside evidence

Preserve mediation.

Examples of form:

- outside testing reportedly showed ...
- treatment was reportedly given ...
- family reports ...

Do not promote mediated information to directly reviewed fact.

## No Stage-A recreation

Do not emit:

- polarity fields;
- certainty fields;
- assertion_type fields;
- speaker registry;
- source registry;
- one span per utterance;
- exhaustive source ledger;
- action-state enums.

The CLINICAL_UNIT lane is compact preservation only.

## Structural checks

Before returning:

1. every PROBLEM evidence selector is exact and contiguous;
2. every CLINICAL_UNIT selector is exact and contiguous;
3. every ACTION_VIEW selector is exact and contiguous;
4. every selector belongs to its cited record;
5. no neighboring-record drift appears;
6. required body/nonproblem evidence is preserved with CLINICAL_UNITs;
7. all clinically material actions are represented;
8. source mediation is preserved;
9. baseline comparator is not promoted without threshold support;
10. diagnostic uncertainty is preserved;
11. no action-state enum appears;
12. no note-section decision appears;
13. no final note prose appears;
14. output begins with `@@HANDOFF B_DIRECT_CLINICAL_SYNTHESIS_WITH_UNITS_V1`;
15. output ends with `@@END`.

## FINAL OUTPUT GATE

Before emitting:

1. Re-read the output contract.
2. Re-check every cited record-selector pair.
3. Re-check CLINICAL_UNIT coverage.
4. Re-check action coverage.
5. Re-check problem architecture and diagnostic stance.
6. Correct any internal violation.
7. Emit the complete handoff once.
8. Emit nothing else.

Return the handoff only.
