# FILE 1 — EVIDENCE OBJECTS

**Experimental version:** F1-EVIDENCE-V1

## Function

Transform a Scribe V2.2 evidence packet into atomic source-aware clinical evidence objects for the next
function.

This file performs **extraction/normalization only**.

Do not write a note.

## Input

One complete `SCRIBE_EVIDENCE_V2_2` packet.

The packet already provides:
- source boundaries;
- ordered source record ids;
- transcript speaker labels;
- prechart section labels;
- nested attribution such as `VIA=`;
- inline `[UNCLEAR]` / `[VERBATIM]` markers.

Treat those as source data. Do not recreate or reinterpret the source hierarchy.

## Output

Output only:

```text
@@HANDOFF F1_EVIDENCE_V1
<evidence objects>
@@END
```

Use exactly one line per evidence object:

```text
E0001 :: SRC=<input record id> :: KIND=<kind> :: TIME=<fact time/scope> :: STANCE=<source stance> :: ATTR=<source attribution> :: TEXT=<one atomic clinical proposition>
```

Use sequential evidence ids in source order.

One input record may produce multiple evidence objects.

Each evidence object must derive from **one input record only**.

## KIND

Use the smallest fitting label:

```text
DISEASE
SYMPTOM
EVENT
EXAM
TEST
MEDICATION
ACTION
REASONING
FUNCTION
SOCIAL
FAMILY
PREFERENCE
QUERY
OTHER_CLINICAL
```

Do not invent a new kind merely because a proposition is unusual.

## TIME

Record the time of the **fact**, not merely the date of the source.

Use:

```text
CURRENT
CURRENT_EPISODE
ONGOING
HISTORICAL
FUTURE_CONDITIONAL
UNKNOWN
```

If the fact time is not supported, use `UNKNOWN`.

Do not convert a fact to CURRENT only because it appears in a current note.

## STANCE

Record only the stance expressed by that source proposition:

```text
ASSERTED
NEGATED
POSSIBLE
LIKELY
UNLIKELY
UNCLEAR
```

This is **source stance**, not the final encounter truth.

Do not strengthen certainty because the same proposition appears more than once.

## ATTR

Preserve attribution mechanically.

Examples:

```text
ATTR=SPK2
ATTR=P1
ATTR=VIA:prior neurology note
ATTR=patient-reported
ATTR=collateral-reported
```

If the packet gives only a raw speaker label, preserve the raw speaker label. Do not infer a stable real
person identity from `SPK#`.

If no additional attribution exists beyond the source record, use `ATTR=-`.

## Atomicity

One object = one clinical proposition.

Split a composite input record when it contains separable propositions with different meaning, time,
stance, type or downstream use.

Example:

```text
Input:
T010 :: SPK2 :: Prior stroke in 2022 with residual right weakness; weakness became worse yesterday.

Output:
E0001 :: SRC=T010 :: KIND=EVENT :: TIME=HISTORICAL :: STANCE=ASSERTED :: ATTR=SPK2 :: TEXT=Left/right-unspecified prior stroke occurred in 2022.
E0002 :: SRC=T010 :: KIND=SYMPTOM :: TIME=ONGOING :: STANCE=ASSERTED :: ATTR=SPK2 :: TEXT=Residual right-sided weakness persisted after the prior stroke.
E0003 :: SRC=T010 :: KIND=SYMPTOM :: TIME=CURRENT_EPISODE :: STANCE=ASSERTED :: ATTR=SPK2 :: TEXT=Right-sided weakness was reported worse yesterday.
```

Do not merge propositions from different input records.

## Clinical questions

A question is not a fact.

Preserve a clinically meaningful question as `KIND=QUERY`.

Never convert a question, silence, or ambiguous response into a denial, normal finding or patient
statement.

Later functions may reconcile a question with an answer.

## Actions

Represent an explicit management/test statement as an atomic `KIND=ACTION` proposition.

Preserve the wording/state actually supplied, for example:
- recommended;
- planned;
- ordered;
- given;
- stopped;
- pending.

Do **not** infer or reconcile action state here. File 3 owns action-state adjudication.

## Reasoning

If a source explicitly states diagnostic, causal, localization or other clinical reasoning, preserve it
as `KIND=REASONING`.

Do not decide whether the reasoning is correct or adopted by the encounter.

Do not invent a causal relationship from coexistence.

## Fidelity rules

Preserve:
- negation;
- uncertainty;
- laterality;
- chronology;
- source attribution;
- patient vs clinician/collateral distinction;
- clinically meaningful negatives;
- explicit absent/unavailable test/result states;
- explicit source reasoning;
- `[UNCLEAR]` and `[VERBATIM]` meaning.

Do not:
- correct medically odd source wording;
- silently normalize a diagnosis;
- resolve contradictions;
- deduplicate across records;
- cluster entities across records;
- decide disease identity across time;
- decide current encounter adoption;
- decide problem identity;
- decide PRIMARY/BACKGROUND;
- decide note relevance;
- assign note sections;
- write summary prose.

## Compression

Remove only wording that carries no clinical proposition after the Scribe packet has already been
processed.

Do not drop a proposition merely because it seems unimportant.

The next function, not File 1, decides cross-source reconciliation and later relevance.

## End condition

Before returning the handoff, check:

1. every evidence object traces to one Scribe record;
2. every line contains one proposition only;
3. no cross-record synthesis occurred;
4. no question became a fact;
5. no source stance or time was strengthened;
6. no problem/note-use decision was made.

Return the handoff only. No explanation before or after it.
