# Recommendation 001 — ingestion as an Evidence Ledger

**Status:** architect recommendation. Not a frozen runtime contract.

## Verdict

Ingestion should produce a compact, source-grounded **Evidence Ledger**, not atomic facts and not a
proto-note.

The Scribe V2.2 packet remains canonical. The ledger is an overlay of source-grounded semantic spans with
record IDs and source views.

## Why

Two failed extremes:

1. **Atomic facts** — one record became many objects; output expanded to ~175 items and truncated.
2. **Synthesized facts + validator** — F1 wrote `fact:` prose, F1V checked it with the same model and
   false-passed wrong references, question-as-answer and action-state upgrades.

The ledger avoids both: it groups source material into clinically meaningful spans and preserves the
source views instead of replacing them with a synthesized truth.

## Classes

```text
E = event / clinical course
H = longitudinal history
O = observation / exam
R = result / study
F = source formulation / reasoning
A = action / decision / execution / result state
C = context / exposure / social / family
Q = question / unresolved query
```

These are ingestion roles, not note sections and not a diagnosis ontology.

## Record shape

```text
@@U04
CLASS=E
LABEL=Thursday recurrent episodes
TIME=Thursday evening; SCOPE=current episode
SUBJECT=patient
CORE=one-line non-authoritative orientation
SOURCE_VIEWS=
- FIANCE [T099-T140; selector=event description]: short fragment
- PATIENT [T112-T120; selector=recollection]: short fragment
- PARAMEDIC [T228-T253; selector=witness description]: short fragment
- ED SUMMARY [P1.013-P1.017; selector=derivative summary]: short fragment
UNCERTAINTY=count and duration differ; classification not established
REFS=T089-T140,T227-T253,P1.013-P1.017
@@END
```

## Boundary rule

Create a new record only when one of these changes materially:

1. event/entity identity;
2. fact time or temporal scope;
3. semantic role;
4. attribution that matters;
5. certainty/state;
6. action state;
7. result state.

Do not split because there are multiple sentences or observations. Do not keep together when downstream
would need different handling.

## Corrections from review

### `CORE` is non-authoritative

`CORE` is a one-line orientation. It must not contain a diagnosis, episode count, causal relation,
resolved conflict, current/historical conclusion, or severity conclusion.

If `CORE` conflicts with a source view, the source view wins. Processing uses the views and refs, not
`CORE`, as evidence.

### `SOURCE_VIEWS` are short

Use one or two sentences per view, plus record IDs and selectors. Do not copy transcript blocks. Processing
dereferences the packet for full detail.

### Add `Q`

Questions are not facts and not negatives. `Q` preserves a question or unresolved query until processing
answers it.

## Actions

Actions preserve separate fields:

```text
TARGET, OPERATION, DECISION, EXECUTION, RESPONSE, RESULT, OWNER,
TIME, CONDITION, TRANSITIONS
```

Never infer:

```text
recommended -> ordered -> performed -> resulted
```

Unknown fields stay absent/NA.

## Relations

Allowed at ingestion:

```text
SAME_EVENT_AS
PART_OF
BEFORE
AFTER
SOURCE_VIEW_OF
SUPERSEDES
```

Not allowed at ingestion:

```text
caused_by
manifestation_of
evidence_for
evidence_against
```

Those are processing decisions.

## Ingestion must not decide

- final problems;
- PRIMARY/BACKGROUND;
- disease vs syndrome architecture;
- note sections;
- A/P evidence;
- diagnosis from raw findings;
- source-conflict resolution;
- outside-service adoption;
- causality;
- treatment-to-diagnosis conversion;
- order/recommendation to completion;
- historical-to-current;
- discarding repetitive but potentially relevant evidence.

## Processing boundary

Processing receives the canonical packet and the Evidence Ledger. It owns:

- reconciliation of source views and conflicts;
- episode model;
- problem architecture;
- note blueprint.

## First test

```text
T001 :: SPK2 :: Three falls since June.
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
P1.002 :: SEC=PMH :: Prior left MCA stroke in 2022.
```

Expected:

- one `E` fall-history unit with two source views;
- one `H` historical left MCA stroke unit;
- `SPK2` role unresolved;
- no inferred count;
- no stroke–falls relation;
- no residual deficit;
- no current stroke problem;
- no consult reason;
- no action, test or result.

If ingestion cannot preserve that boundary, processing cannot recover it.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
