# DIRECT-B TEST — CLINICAL SYNTHESIS FROM SCRIBE

## EXECUTION GATE

1. Read this entire instruction file before producing output.
2. Read the complete input before starting the transformation.
3. Do not draft, stream, or emit output while still reading or interpreting instructions.
4. Silently complete these phases in order:
   - READ — understand the full contract and input.
   - EXTRACT — identify only supported source material needed by this stage.
   - DECIDE — make only the decisions assigned to this stage.
   - CHECK — apply every rule and structural check in this file.
   - EMIT — output only the required handoff.
5. Apply later rules in this file before committing any earlier output decision.
6. Do not emit reasoning, scratch work, partial results, or intermediate drafts.
7. Output schemas define allowed structure. They do not authorize unsupported field completion.
8. Omit optional fields rather than infer values to fill the schema.

**Experimental condition:** B-DIRECT-CLINICAL-SYNTHESIS-V1

## Purpose

Test whether the clean `SCRIBE_EVIDENCE_V2_2` packet can support File B clinical synthesis directly without a
separate Stage A ingestion handoff.

This is an architecture comparator only. It does not replace active A unless the experiment supports that decision.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

Do not generate an A handoff.

## Responsibilities

Perform the same clinical-synthesis responsibilities as active `02-CLINICAL-SYNTHESIS.md`:

- reconcile same/distinct clinical episodes when supported;
- determine neurologic problem structure;
- preserve diagnostic stance and clinically meaningful counterevidence;
- identify and split distinct clinical actions directly from source records;
- reconcile action trajectories only when supported;
- assign action ownership;
- produce concise source-qualified management wording;
- preserve unresolved ambiguity rather than guessing.

Do not decide note sections or write final note prose.

## Source grounding

Every clinical claim and action must cite exact Scribe source material directly.

For every cited source item provide:
- exact `source_record`;
- exact contiguous `selector` from that record.

Do not:
- merge text from different records into one selector;
- paraphrase inside a selector;
- invent source text;
- use neighboring records as support;
- infer an action absent from the packet.

When multiple records support one synthesis, cite each independently.

## Output

Return only:

```text
@@HANDOFF B_DIRECT_CLINICAL_SYNTHESIS_V1

CLINICAL_SYNTHESIS

PROBLEM P001
  label=<minimal source-supported neurologic problem formulation>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  diagnostic_stance=<concise source-supported assessment>
  evidence=<source_record + exact selector; one or more>
  counterevidence=<source_record + exact selector; one or more>
  contains=<contained manifestation/history descriptors when useful>
  separate_from=<distinct problem handles when needed>
  order=<integer>

ACTION_VIEW AV001
  source_record=<exact record ID>
  selector=<exact contiguous source substring>
  target=<concise normalized target>
  wording=<concise source-qualified wording faithful to the selector>
  owner=<problem handle or nonproblem>
  unresolved=<episode/ownership/wording ambiguity when material>

SYNTHESIS_UNRESOLVED X001
  topic=<short unresolved clinical synthesis issue>
  evidence=<source_record + exact selector; one or more>
  issue=<why it cannot be safely reconciled>

@@END
```

If one action trajectory is supported by multiple distinct source records, keep separate ACTION_VIEW entries unless
the records clearly describe the same action. Do not hide distinct source actions inside one synthesized selector.

## Problem threshold

Create a separate problem only when it has independent neurologic clinical identity or its own current assessment
question/status.

### Counterfactual independence test

Before creating a separate problem, ask:

> If the primary presenting problem were removed from this encounter, would this item still justify its own
> neurologic assessment/problem block because of an independent disease identity, separate current assessment
> question, or separate current management?

- **Yes** -> it may qualify if supported.
- **No** -> preserve it as evidence, counterevidence, a contained manifestation, baseline comparator, history, or
  context under the relevant problem.

An established historical neurologic disease may become a BACKGROUND problem only when it is also relevant to the
current encounter's neurologic interpretation or management. Historical identity alone is insufficient.

A chronic/baseline symptom or phenomenologically distinct spell does not become a BACKGROUND problem merely because
it is longstanding or differs from the presenting event.

## Diagnostic stance

Preserve:
- current syndrome;
- supported suspected/favored possibilities;
- important alternatives still under evaluation;
- meaningful baseline-vs-current distinctions.

Do not:
- upgrade suspicion to diagnosis;
- collapse a differential to one diagnosis;
- use management intensity as diagnostic proof;
- use a normal/negative test to exclude a diagnosis unless the source supports that conclusion.

## Actions

Enumerate every distinct source-local clinical action relevant to the neurologic encounter, including:
- diagnostic tests/procedures;
- medications/treatments;
- consultations;
- admission/disposition;
- precautions/safety/driving counseling;
- other neurologic management.

For compound action wording, split distinct targets when needed to preserve downstream meaning.

Preserve ordinary source-qualified wording rather than action-state enums.

Acceptable form includes wording such as:
- reportedly treated with medication;
- test needed for further evaluation;
- continue medication for now; reassess after tests;
- favor inpatient workup;
- safety counseling discussed.

These are form examples only.

## No action-state enums

Do not emit:
- `decision=`;
- `execution=`;
- `response=`;
- `result=`;
- state-slot values such as `not_started`, `pending`, `unavailable`, or `ordered`.

Do not infer:
- order from recommendation/need;
- nonperformance from future wording;
- pending/unavailable result merely from silence or lack of review;
- objective performance from a mediated report;
- agreement from clinician preference.

## Source-qualified outside evidence

Preserve mediation explicitly.

Examples:
- family was told testing was normal;
- outside testing reportedly showed no significant abnormality;
- treatment was reportedly given on the ship.

Do not promote mediated information to directly reviewed objective fact.

## Structural checks

Before returning:

1. every evidence selector is an exact substring of its cited Scribe record;
2. every ACTION_VIEW selector is an exact substring of its cited Scribe record;
3. all clinically material actions in the packet are represented;
4. source-mediated facts/actions remain qualified;
5. problem threshold uses the counterfactual independence test;
6. baseline comparator symptoms are not promoted to problems without independent identity/assessment/management;
7. no action-state enum appears;
8. no note sections or prose note are written;
9. output begins with `@@HANDOFF B_DIRECT_CLINICAL_SYNTHESIS_V1` and ends with `@@END`.

## FINAL OUTPUT GATE

Before emitting:

1. Re-read the required output contract.
2. Check the completed internal result against every structural check in this file.
3. Correct any internal violation before emission.
4. Verify that no unsupported field was added only to complete a schema.
5. Emit the required handoff once.
6. Emit no commentary or reasoning.


Return the handoff only.
