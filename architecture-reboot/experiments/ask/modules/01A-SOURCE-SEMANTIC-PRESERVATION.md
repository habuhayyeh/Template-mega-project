# FILE A1 — SOURCE-SEMANTIC PRESERVATION

**Experimental version:** A1-SOURCE-SEMANTIC-PRESERVATION-V1

## Purpose

Transform one complete canonical `SCRIBE_EVIDENCE_V2_2` packet into a **material source-local ledger**
before any cross-record reconciliation or compression.

A1 exists because the single-pass A experiments showed that source preservation and reconciliation compete:
material content can disappear while the model is simultaneously deciding what to merge, normalize, and compress.

A1 therefore answers only:

> What material assertion does this source span actually make, locally, with what explicit provenance/state?

It does **not** decide how different records relate to one another.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

## Output

Return:

```text
@@HANDOFF A1_SOURCE_SEMANTIC_V1

SOURCE_SEMANTIC_LEDGER

SPAN S001
  source=<record ID>
  selector=<minimal exact clause/field>
  assertion_type=<statement|question|observation|result|diagnosis|action|reasoning>
  material_role=<current_episode|neuro_history|other_history|medication|exam|workup|safety_function|action|reasoning|context>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established in the same source-local context>
  provenance=<explicit nested provenance if stated>
  time=<explicit source/event time if stated>
  polarity=<affirmed|negated|unresolved>
  certainty=<possible|likely|suspected|unlikely|unstated>
  action_state=<decision:considered|decision:planned|decision:recommended|decision:continue|decision:discontinue|decision:hold|decision:not_indicated|decision:deferred|execution:not_started|execution:ordered|execution:reported_performed|execution:performed|execution:held|execution:resumed|execution:stopped|execution:canceled|response:agrees|response:declines|response:undecided|response:prefers_alternative|result:unavailable|result:pending|result:preliminary|result:final>
  unresolved=<source-local ambiguity/garble/limitation>

@@END
```

Use only fields supported by that source-local span.

Unknown fields stay absent.

## Inclusion rule

A1 is a **preservation layer**, so omission must be conservative.

Include a source-local span when it could materially affect:
- the current neurologic episode;
- neurologic history;
- other history relevant to neurologic interpretation/management;
- medication-at-presentation;
- current examination;
- workup/result state;
- safety/function;
- a management action;
- diagnostic/problem-relevant reasoning;
- a material uncertainty or contradiction later reconciliation may need.

If uncertain whether a clinical span could matter, **include it**.

Exclude only:
- greetings;
- empty acknowledgements;
- conversational repair with no usable assertion;
- clearly nonclinical logistics;
- exact duplicate wording within the same source record when no distinction would be lost.

Do not use “importance” or “candidate problem” as the gate.

## One SPAN = one source-local material assertion

A SPAN must be anchored to one source record.

Use:
- one record ID;
- one minimal selector from that record.

Do not:
- combine multiple record IDs into one SPAN;
- summarize adjacent turns into one synthesized assertion;
- copy long narrative;
- invent a cleaner statement than the source supports.

A single record may generate more than one SPAN when it contains multiple materially different assertions.

This is not global atomicization.
Split only when failing to split would lose a material distinction such as:
- different referent;
- different assertion type;
- different polarity;
- different action state;
- different result state.

## Assertion type

Classify only the source-local assertion:

- `statement`
- `question`
- `observation`
- `result`
- `diagnosis`
- `action`
- `reasoning`

A question remains a question.
A diagnosis/formulation is not automatically a fact.
A management action embedded in diagnostic prose gets its own SPAN when clinically meaningful.

## Speaker/source identity

Always preserve the raw source label.

Examples:
- `SPK0`
- `SPK3`
- `P1`

### Local identity only

Populate `local_identity` only when identity is explicitly established in the same local source context.

Do **not** globally map `SPK#` labels across the transcript.

The packet has shown that diarization labels may not be identity-stable.

If identity is not explicitly established locally:
- keep the raw label;
- omit `local_identity`;
- use `unresolved` if identity matters.

Do not infer patient/mother/fiance/clinician/witness from conversational context alone.

## Provenance

Preserve explicit nested provenance exactly when stated, for example:
- ED note via EMS;
- ED note citing cruise paperwork;
- family member reporting what another witness saw.

Do not collapse mediated reports into objective findings.

## Time

Record only source-local time actually established.

Do not reconcile competing times in A1.

If the source says:
- Wednesday;
- 6:55;
- two days ago;
- prior;
- tonight/tomorrow;

preserve that local time expression.

Cross-record chronology belongs to A2.

## Polarity

Use:
- `affirmed`
- `negated`
- `unresolved`

Rules:
- a question is not a negative;
- `not on file` / `not documented` is not negation;
- silence is not negation;
- garbled material stays unresolved.

## Certainty

Use only explicit/source-stated epistemic certainty:

- `possible`
- `likely`
- `suspected`
- `unlikely`
- `unstated`

Do not infer certainty from:
- chart section;
- management intensity;
- repetition;
- clinical plausibility.

## Source-local action state

When the span is an action, preserve only the state explicitly supported by that span.

Allowed states are field-qualified:

### decision
- `decision:considered`
- `decision:planned`
- `decision:recommended`
- `decision:continue`
- `decision:discontinue`
- `decision:hold`
- `decision:not_indicated`
- `decision:deferred`

### execution
- `execution:not_started`
- `execution:ordered`
- `execution:reported_performed`
- `execution:performed`
- `execution:held`
- `execution:resumed`
- `execution:stopped`
- `execution:canceled`

### response
- `response:agrees`
- `response:declines`
- `response:undecided`
- `response:prefers_alternative`

### result
- `result:unavailable`
- `result:pending`
- `result:preliminary`
- `result:final`

Hard rules:
- `Plan: CT` supports `decision:planned`, not `execution:ordered`.
- `started on drip` in a report supports `execution:reported_performed`; do not infer an order.
- `keep on Keppra for now` supports `decision:continue`.
- `discontinued load` supports a local stop/cancel/discontinue state only for that action episode.
- a test not yet started does not automatically have `result:pending`.
- unknown action fields remain absent.
- A1 never invents an intermediate action state.

## Material role

`material_role` is a preservation class, **not final note placement**.

Use the narrowest supported class:
- `current_episode`
- `neuro_history`
- `other_history`
- `medication`
- `exam`
- `workup`
- `safety_function`
- `action`
- `reasoning`
- `context`

This field exists only to prevent material note-relevant spans from disappearing before A2/C.

It does not decide:
- final note section;
- candidate-problem status;
- PRIMARY/BACKGROUND;
- problem containment;
- final inclusion.

## What A1 must not do

A1 must not:
- merge across records;
- assign `same_event`, `same_state`, `evolution`, `conflict`, or `possible_overlap`;
- globally map speaker identities;
- reconcile competing timestamps;
- combine patient history with family history;
- infer intermediate action states;
- create action episodes across records;
- decide current problem adoption;
- decide problems;
- decide causal/contributory relationships;
- decide note sections;
- write note prose.

## Structural checks

Before returning:

1. every SPAN points to exactly one source record;
2. every selector is actually present in that record;
3. questions remain questions;
4. no adjacent-turn synthesis is attached to one record;
5. raw speaker/source labels are preserved;
6. no global SPK identity mapping appears;
7. `not on file` is not negated;
8. action state is source-local and field-qualified;
9. unknown action fields are absent;
10. current exam/workup/medications/safety/history material is preserved when materially note-relevant;
11. no cross-record relationship is asserted;
12. output ends with `@@END`.

Return the handoff only.
