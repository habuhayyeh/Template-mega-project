# Current architecture map

**Status:** architect recommendation. Not a frozen runtime contract.

## Three layers

```text
SCRIBE V2.2 PACKET
    |
    v
1. INGESTION
   Evidence Ledger
    |
    v
2. PROCESSING
   reconciliation -> episode model -> problem architecture -> note blueprint
    |
    v
3. OUTPUT
   renderer
    |
    v
FINAL NOTE
```

## Ingestion

Input: one canonical Scribe V2.2 packet.

Output: Evidence Ledger, an overlay on the packet. The packet remains the evidence store.

Record classes:

- `E` — event / clinical course
- `H` — longitudinal history
- `O` — observation / exam
- `R` — result / study
- `F` — source formulation / reasoning
- `A` — action / decision / execution / result state
- `C` — context / exposure / social / family
- `Q` — question / unresolved query

Record shape:

```text
@@U04
CLASS=E
LABEL=Thursday recurrent episodes
TIME=Thursday evening; SCOPE=current episode
SUBJECT=patient
CORE=one-line non-authoritative orientation
SOURCE_VIEWS=
- FIANCE [T099-T140; selector=event description]: short fragment
- PARAMEDIC [T228-T253; selector=witness description]: short fragment
- ED SUMMARY [P1.013-P1.017; selector=derivative summary]: short fragment
UNCERTAINTY=count and duration differ; classification not established
REFS=T089-T140,T227-T253,P1.013-P1.017
@@END
```

Rules:

- create a new record only at a material semantic boundary: event/entity, time/scope, semantic role,
  attribution, certainty/state, action state, result state;
- do not atomize every sentence;
- preserve competing source views;
- `CORE` is navigation only; source views and refs win;
- `SOURCE_VIEWS` are short fragments plus IDs/selectors, not copied transcript blocks;
- actions preserve decision / execution / response / result separately;
- relations limited to `SAME_EVENT_AS`, `PART_OF`, `BEFORE`, `AFTER`, `SOURCE_VIEW_OF`, `SUPERSEDES`;
- ingestion does not decide problems, roles, sections, diagnosis, causality or reconciliation.

## Processing

Input: canonical packet + Evidence Ledger.

Sub-steps:

1. **Reconciliation** — reconcile source views, conflicts, evolution, current vs historical, attribution.
2. **Episode model** — build the current episode and relevant longitudinal context.
3. **Problem architecture** — independent problems, containment, PRIMARY/BACKGROUND, relations,
   action ownership.
4. **Note blueprint** — section allocation, chronology, evidence/counterevidence, plan placement.

Output: `NOTE_BLUEPRINT`.

## Output

Input: frozen `NOTE_BLUEPRINT` + packet for exact qualifiers.

Output: final note.

The renderer owns wording only. It may not reopen diagnosis, currentness, causality, containment, role,
action state or section allocation.

## Deleted / rejected

- atomic fact corpus;
- topic index;
- synthesized fact prose;
- same-model validator;
- separate action pass by default;
- separate renderer call by default;
- final audit pass as runtime proof.

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
- no stroke–falls causality;
- no residual deficit;
- no current stroke problem;
- no consult reason;
- no action, test or result.

## Open

- processing contract and handoff schema;
- note blueprint contract;
- renderer contract;
- whether one Ask call or a clean two-call split is needed for packet size.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
