# DeepSeek review — Evidence Ledger ingestion

**Status:** architecture recommendation. No implementation.

## Verdict

This is the best ingestion model so far. Use it, with three corrections:

1. `CORE` must be non-authoritative orientation, not a synthesized clinical summary.
2. `SOURCE_VIEWS` must be short source-grounded fragments plus record IDs/selectors, not copied
   transcript paragraphs.
3. Add a `Q` class for questions/unresolved queries.

The important move is correct: **ingestion preserves source-grounded semantic spans; processing does
reconciliation.** Do not put reconciliation in ingestion.

## Three-layer map

```text
SCRIBE PACKET
    |
    v
1. INGESTION
   Evidence Ledger:
   E events/course
   H longitudinal history
   O observations/exam
   R results/studies
   F source formulation/reasoning
   A actions
   C context/exposure/social/family
   Q questions/unresolved queries
    |
    v
2. PROCESSING
   reconciliation
   -> episode model
   -> problem architecture
   -> note blueprint
    |
    v
3. OUTPUT
   renderer
    |
    v
FINAL NOTE
```

Ingestion answers: what source-grounded material exists, when, who says it, what state it is in, and
which pieces refer to the same clinical thing.

Processing answers: what it means together, what the problems are, how sources reconcile, what is
evidence/status/manifestation/context, and where it goes.

Output answers: how to express the frozen blueprint.

## What is right

- semantic spans at meaningful boundaries, not atomic facts;
- one coherent event can hold multiple source views;
- source packet remains canonical;
- competing views preserved, not reconciled;
- actions decomposed by state change;
- limited relation vocabulary;
- event time separated from source date;
- no problem/section/role decisions at ingestion;
- 15–25 records, not 150–300;
- handoff contract is clear.

This directly avoids both failed extremes:
- atomic explosion/truncation;
- synthesized-fact loss and impossible validation.

## Corrections

### 1. `CORE` is a claim surface

The example `CORE` is a synthesized paragraph. It says “recurrent episodes of impaired responsiveness
with staring and later variable eye/head movements...” That is already an interpretation of the source
views, even if a mild one.

Keep `CORE` only as a **one-line orientation** that says what the bundle is about. It must not contain:

- a diagnosis;
- an episode count;
- a causal relation;
- a resolved conflict;
- a current/historical conclusion not explicit in the source;
- a severity/status conclusion.

Make it formally non-authoritative:

> `CORE` is navigation only. Processing must use `SOURCE_VIEWS` and `REFS`; if `CORE` conflicts with a
> source view, the source view wins.

Safer alternative: rename it `LABEL` and allow only a short noun phrase. The long orientation paragraph
is optional and easy to drop.

### 2. `SOURCE_VIEWS` will re-inflate if copied

The example source views are long prose paragraphs. At 15–25 records, that can still be large, and it
invites paraphrase drift.

Use:

```text
SOURCE_VIEWS=
- FIANCE [T099-T140; selector=event description]:
  short source-grounded fragment or neutral one-line summary
- PARAMEDIC [T228-T253; selector=witness description]:
  short fragment
- ED SUMMARY [P1.013-P1.017; selector=derivative summary]:
  short fragment
```

Rules:

- one or two sentences per view;
- preserve exact qualifiers where they matter;
- cite record IDs and selectors;
- processing dereferences the packet for full detail;
- no copied transcript blocks;
- no merging views into one sentence.

### 3. Add `Q`

The class list omits questions. Questions are not facts and not negatives.

Add:

```text
Q = question / unresolved query
```

Use it for:

- clinician questions whose answer is missing or ambiguous;
- consult questions;
- differential questions that are not assertions;
- unresolved source queries.

A question must never be promoted into a statement by ingestion.

## Class definitions

| class | owns | must not |
|---|---|---|
| `E` | event/course/episode span | diagnosis, problem identity, section |
| `H` | longitudinal history/prior state | current status, current problem |
| `O` | observation/exam finding | diagnosis, interpretation |
| `R` | result/study | clinical conclusion, treatment decision |
| `F` | source formulation/reasoning | final Neurology adoption, final diagnosis |
| `A` | action/decision/execution/result state | problem ownership, plan |
| `C` | context/exposure/social/family | problem identity, causality |
| `Q` | question/unresolved query | answer, negation, diagnosis |

These are ingestion roles, not note sections and not a diagnosis ontology. `F` is source reasoning, not
final truth.

## Span boundary rule

Create a new record only when one of these changes materially:

1. event/entity identity;
2. fact time or temporal scope;
3. semantic role;
4. attribution that matters;
5. certainty/state;
6. action state;
7. result state.

Do not split because there are multiple sentences or observations. Do not keep together when the
downstream would need different handling.

## Ledger record shape

```text
@@U04
CLASS=E
LABEL=Thursday recurrent episodes
TIME=Thursday evening; SCOPE=current episode
SUBJECT=patient
CORE=Recurrent episodes of impaired responsiveness with staring and variable eye/head movements.
SOURCE_VIEWS=
- FIANCE [T099-T140; selector=event description]: short fragment
- PATIENT [T112-T120; selector=recollection]: short fragment
- PARAMEDIC [T228-T253; selector=witness description]: short fragment
- ED SUMMARY [P1.013-P1.017; selector=derivative summary]: short fragment
UNCERTAINTY=count and duration differ by source; classification not established
REFS=T089-T140,T227-T253,P1.013-P1.017
@@END
```

### Actions

```text
@@A02
CLASS=A
TARGET=levetiracetam 1500 mg load
OPERATION=administration
DECISION=initially requested @P1.054
EXECUTION=not established
LATER_STATE=discontinued before another load @P1.055
OWNER=ED/Neurology
TIME=current ED encounter
REFS=P1.054,P1.055
@@END
```

Keep fields absent when unsupported. Never infer:

```text
recommended -> ordered -> performed -> resulted
```

### Relations

Keep only:

```text
SAME_EVENT_AS
PART_OF
BEFORE
AFTER
SOURCE_VIEW_OF
SUPERSEDES
```

Do not create `caused_by`, `manifestation_of`, `evidence_for` at ingestion. Those are processing
decisions.

## What ingestion must not decide

- final problems;
- PRIMARY/BACKGROUND;
- disease vs syndrome architecture;
- note sections;
- A/P evidence;
- diagnosis from findings;
- source-conflict resolution;
- outside-service adoption;
- causality;
- treatment-to-diagnosis conversion;
- order/recommendation to completion;
- historical-to-current;
- discarding repetitive but potentially relevant evidence.

## Processing boundary

Processing receives:

1. canonical packet;
2. Evidence Ledger.

Processing owns:

- reconciliation of source views;
- episode model;
3. problem architecture;
4. note blueprint.

It must be allowed to say `UNRESOLVED` rather than complete the story.

## Test

Use the three-record packet:

```text
T001 :: SPK2 :: Three falls since June.
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
P1.002 :: SEC=PMH :: Prior left MCA stroke in 2022.
```

Expected ingestion:

- one `E` fall-history unit with two source views;
- one `H` historical left MCA stroke unit;
- `SPK2` role unresolved, not “patient”;
- no count total;
- no stroke–falls relation;
- no residual deficit;
- no current stroke;
- no consult reason;
- no action, test or result.

If ingestion cannot preserve that, processing cannot recover it.

## Recommendation

Adopt this ingestion model with the three corrections. It is a better boundary than our earlier
`A = interpret and reconcile` design: ingestion preserves evidence; processing reconciles and builds
problems.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
