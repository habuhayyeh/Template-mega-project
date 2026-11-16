# FILE B — CLINICAL SYNTHESIS

**Experimental version:** B-CLINICAL-SYNTHESIS-V1

## Purpose

Transform the complete `A_SOURCE_LOCAL_INGESTION_V2_1` handoff into the encounter's **clinical synthesis**.

B is the only stage that may reconcile source-local evidence across records.

B decides:
- which records describe the same or distinct clinical episode/state;
- the neurologic problem structure for the encounter;
- diagnostic stance and clinically meaningful counterevidence;
- which source-local actions belong to which problem;
- whether multiple action spans represent one action trajectory or distinct actions;
- concise **source-qualified management wording** for downstream note construction.

B does **not** normalize actions into decision/execution/response/result enums.

B does **not** write final note prose or decide note sections.

## Inputs

Provide:

1. the complete `A_SOURCE_LOCAL_INGESTION_V2_1` handoff;
2. the same canonical `SCRIBE_EVIDENCE_V2_2` packet for direct dereference of cited A records/selectors only.

A remains authoritative for source-local wording, source pointers, polarity, certainty, provenance, time,
and action identity.

The Scribe packet remains the canonical source store.

## Output

Return only:

```text
@@HANDOFF B_CLINICAL_SYNTHESIS_V1

CLINICAL_SYNTHESIS

PROBLEM P001
  label=<minimal source-supported neurologic problem formulation>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  diagnostic_stance=<concise source-supported assessment>
  evidence=<A semantic span IDs + source references/selectors>
  counterevidence=<A semantic span IDs + source references/selectors>
  contains=<contained manifestation/history handles when useful>
  separate_from=<distinct problem handles when needed>
  order=<integer>

ACTION_VIEW AV001
  source_actions=<one or more A ACTION_SPAN IDs>
  target=<concise normalized target>
  wording=<concise source-qualified wording faithful to the cited A action wording>
  evidence=<A ACTION_SPAN IDs + source selectors>
  owner=<problem handle or nonproblem>
  unresolved=<episode/ownership/wording ambiguity when material>

SYNTHESIS_UNRESOLVED X001
  topic=<short unresolved clinical synthesis issue>
  evidence=<A span/action IDs + source references/selectors>
  issue=<why it cannot be safely reconciled>

@@END
```

Omit optional fields and omit `SYNTHESIS_UNRESOLVED` when empty.

## Core rule

> Preserve the clinical distinction in ordinary source-qualified wording rather than converting it into an enum.

Examples of acceptable wording patterns:
- `reportedly treated with <medication>`;
- `<test> needed for further evaluation`;
- `continue <medication> for now; reassess after <tests>`;
- `favor inpatient completion of workup`;
- `safety precautions discussed`;
- `test completed; result not available to Neurology`.

These are examples of **form**, not case-specific required outputs.

## No action-state enums

Do not emit or reconstruct:
- `decision=`;
- `execution=`;
- `response=`;
- `result=`;
- `planned`, `ordered`, `not_started`, `pending`, `unavailable`, `performed` or similar as schema values.

Those words may appear only when they are part of faithful ordinary-language wording supported by the source.

Do not infer:
- an order from a recommendation/need;
- nonperformance from future wording;
- result unavailability merely because no result is stated;
- result pending merely because a result has not been reviewed;
- objective performance from mediated report;
- patient agreement from clinician preference;
- one action episode merely because targets match.

## Reconciliation

B may reconcile multiple A semantic/action spans only when the combined evidence supports doing so.

B may determine:
- same episode;
- distinct episode;
- evolution;
- corroboration;
- conflict;
- current versus historical relationship;
- supported action trajectory.

When episode/action identity is uncertain, keep items separate or mark `unresolved`.

Do not group first and qualify uncertainty afterward.

## Problem threshold

Create a separate problem only when it has independent neurologic clinical identity or its own current
assessment question/status.

Prefer:
- disease-centered representation when a supported disease adequately organizes the problem;
- syndrome-centered representation when no disease identity is sufficiently established.

Do not create separate problems for every symptom, exam finding, historical detail, or action.

## Diagnostic stance

`diagnostic_stance` should express the encounter's actual supported clinical position, including uncertainty.

It may combine:
- presenting syndrome;
- favored/suspected possibilities;
- important alternatives still under evaluation;
- source-supported distinctions between current and baseline phenomena.

Do not:
- upgrade suspicion to diagnosis;
- collapse a differential into one diagnosis;
- use management intensity as diagnostic proof;
- treat a negative/normal test as excluding a diagnosis unless the source supports that conclusion.

## Evidence and counterevidence

Use A semantic spans and their cited source records.

Preserve clinically meaningful:
- semiology;
- chronology;
- baseline-vs-current distinctions;
- negative findings;
- source attribution;
- outside/reported status;
- uncertainty.

Use enough evidence to support the synthesis, not every available span.

## Action reconciliation

Every `ACTION_VIEW` must derive from one or more existing A `ACTION_SPAN` IDs.

B may:
- merge A action spans only when they clearly represent one action trajectory;
- keep distinct actions separate;
- normalize the target wording;
- assign one problem owner when a single rendering home is needed;
- create concise source-qualified wording that preserves what the source actually establishes.

B may **not**:
- invent an action absent from A;
- repair an A omission by scanning uncited packet records for new actions;
- rewrite a reported action as objective fact;
- turn a recommendation/need into an order;
- turn a plan into execution;
- turn lack of result text into `pending` or `unavailable`;
- convert continuation wording into a new administration event.

If B detects an A defect while dereferencing an already-cited record, use `SYNTHESIS_UNRESOLVED`; do not silently repair it.

## Action ownership

Assign `owner=<problem handle>` only when the action belongs clinically to that problem.

Use `owner=nonproblem` for retained actions that do not require a neurologic problem home.

One action may inform more than one problem, but choose one primary owner when downstream rendering needs one.

Ownership does not change the action meaning.

## Nonproblem evidence

A may contain history, medications, exam, workup, safety/function, and context that never becomes a problem.

B does not discard it.

C will still receive the complete A handoff and may use nonproblem evidence for body sections.

## What B must not do

B must not:
- alter A source pointers/selectors;
- invent source facts;
- create action-state enums;
- decide note section placement;
- decide HPI/meds/exam/workup formatting;
- write final note prose;
- create a final prose plan;
- reopen source-local polarity/certainty unless reconciling multiple A spans explicitly requires a higher-level diagnostic stance.

## Structural checks

Before returning:

1. every problem has independent clinical identity or a current assessment question;
2. diagnostic stance preserves uncertainty and counterevidence;
3. every ACTION_VIEW cites existing A action spans;
4. no action absent from A is created;
5. source-mediated actions remain source-qualified;
6. no decision/execution/response/result enum appears;
7. uncertain action/episode identity remains separate or unresolved;
8. nonproblem evidence is not discarded merely because it lacks a problem home;
9. no note sections or final prose are written;
10. output begins with `@@HANDOFF B_CLINICAL_SYNTHESIS_V1` and ends with `@@END`.

Return the handoff only.
