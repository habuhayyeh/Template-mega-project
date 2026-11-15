# FILE C — NOTE COMPILER

**Experimental version:** C-NOTE-COMPILER-V1

## Purpose

Compile the supported semantic state from File A and the problem structure from File B into a complete
**NOTE_BLUEPRINT** before any final note prose is written.

File C decides **what belongs where, in what order, and with which qualifiers preserved**.

File C does not reinterpret the source, rebuild problem architecture, or write the final note.

## Inputs

Provide all three:

1. File A handoff:
   - `DECISION_LEDGER`
   - `ACTION_LANE`
   - `UNRESOLVED_REGISTER`

2. File B handoff:
   - `PROBLEM_MAP`
   - `ARCHITECTURE_UNRESOLVED`

3. canonical `SCRIBE_EVIDENCE_V2_2` packet for direct dereference of cited records/selectors.

File A remains authoritative for reconciled source meaning and action state.

File B remains authoritative for problem identity, containment, adoption/currentness, certainty,
encounter role, causal/contributory relations, problem order, and action ownership.

## Output

Return `NOTE_BLUEPRINT` only.

Do not write final note prose.

```text
@@HANDOFF C_NOTE_BLUEPRINT_V1

NOTE_BLUEPRINT

SECTION RFC
  ENTRY R001
    content=<UNIT/ACTION/problem handle + selector>
    function=<why this belongs in RFC>
    preserve=<attribution/time/negation/certainty/conflict qualifiers>

SECTION HPI
  ENTRY H001
    content=<UNIT/ACTION IDs + selectors>
    function=<role in current-episode chronology>
    preserve=<attribution/time/negation/certainty/conflict qualifiers>

SECTION NEURO_HX
  ENTRY N001
    content=<UNIT/ACTION IDs + selectors>
    function=<why this belongs in neurologic history>
    preserve=<qualifiers>

SECTION OTHER_PMH
  ENTRY O001
    content=<UNIT IDs + selectors>
    function=<why this belongs in other history>
    preserve=<qualifiers>

SECTION MEDS
  ENTRY M001
    content=<UNIT/ACTION IDs + selectors>
    function=<presentation/home medication role>
    preserve=<qualifiers>

SECTION EXAM
  ENTRY E001
    content=<UNIT IDs + selectors>
    function=<current examination role>
    preserve=<qualifiers>

SECTION WORKUP
  ENTRY W001
    content=<UNIT/ACTION IDs + selectors>
    function=<test/workup role>
    preserve=<performed/result/pending/ordered qualifiers>

AP P001
  problem=<File B problem handle>
  claim=<File B label + permitted supported status>
  support=<UNIT IDs / record IDs + selectors>
  counter=<UNIT IDs / record IDs + selectors>
  reasoning=<source-supported reasoning handles or none>
  actions=<ACTION IDs>
  primary_action_holder=<ACTION IDs>
  references_only=<shared ACTION IDs rendered elsewhere>

@@END
```

Use only sections and entries supported by the inputs.

Do not create empty filler entries.

## Core ownership

File C owns:

- section allocation;
- reason-for-consult placement;
- HPI chronology;
- neurologic-history grouping;
- other-PMH grouping;
- medication-at-presentation selection;
- current-exam selection;
- workup/result placement;
- minimum-sufficient evidence selection;
- counterevidence placement;
- legitimate cross-section reuse;
- shared-action placement;
- A/P composition from already-resolved File B problems.

File C does **not** own clinical reinterpretation.

## What File C must not do

File C must not:

- change File A polarity, certainty, temporality, attribution, event identity, or action state;
- change File B problem identity;
- change File B adoption/currentness;
- change File B certainty;
- change File B PRIMARY/BACKGROUND/unresolved role;
- change containment;
- create or alter causal/contributory relations;
- create a new problem;
- resolve File B `ARCHITECTURE_UNRESOLVED`;
- convert `encounter_role=unresolved` into PRIMARY or BACKGROUND;
- infer a final diagnosis from placement;
- invent source facts;
- write final prose;
- rewrite or upgrade a management action.

If C detects a missing upstream semantic or architecture decision needed for safe placement, preserve the
gap rather than silently repairing A or B.

## RFC

RFC is the source-supported reason Neurology is involved in the encounter.

Use RFC only when the source or resolved architecture actually establishes the reason for consult/service
involvement.

Do not infer RFC from:
- the first charted symptom;
- the most severe historical diagnosis;
- the first PRIMARY-looking problem;
- ED chief complaint alone unless it actually represents the neurologic consult reason.

If RFC is not established, omit RFC or preserve the unresolved gap. Do not invent one.

## HPI

HPI represents the **current episode or current neurologic presentation** in clinical chronology.

Rules:

- order by event chronology, not source-document order;
- use the smallest sufficient sequence that preserves clinically meaningful evolution;
- preserve attribution when events are patient/collateral/outside-report based;
- preserve uncertainty and conflict;
- do not insert chronic background merely because it appeared during the interview;
- do not convert source reasoning into event fact;
- do not show a planned action as if it occurred.

HPI may legitimately reuse material that also supports A/P when the functions differ.

Cross-section reuse must be purposeful, not duplication by default.

## NEURO_HX

NEURO_HX is disease-centered longitudinal neurologic history.

Use it for established or historically relevant neurologic disease/state not required in the current HPI
chronology.

Preserve:
- historical/current distinction;
- longitudinal status;
- established consequences when source-supported.

Do not create a separate history item for every manifestation already adequately represented under an
established neurologic disease.

## OTHER_PMH

OTHER_PMH carries non-neurologic history that remains relevant to the note but does not belong in
neurologic history.

Do not promote non-neurologic history into neurologic problem structure merely because it may contextualize
the encounter.

## MEDS

MEDS represents the medication regimen **at presentation / home baseline**, plus only those source-supported
qualifiers needed to interpret it.

Do not rewrite the presentation medication list based on encounter changes.

Keep distinct:
- home/presentation medication;
- recommended change;
- ordered change;
- administered treatment;
- discontinued/held treatment.

Encounter actions belong to A/P/workup placement through File A ACTION IDs, not by rewriting the baseline
medication section.

## EXAM

EXAM represents the **current examination** for this encounter.

Rules:

- use current exam findings only;
- preserve source attribution when exam findings come from an outside source;
- do not collage old examinations into the current exam;
- do not convert absence of documentation into a normal finding;
- do not convert patient report into objective examination.

## WORKUP

WORKUP must preserve test state.

Distinguish:

- result available;
- test performed but result pending/unavailable;
- test ordered/planned but not performed;
- outside result reported by source;
- no result available.

Never render:

```text
ordered -> performed
performed -> resulted
```

without File A support.

Workup placement must preserve the action/result distinction from File A.

## Nonproblem evidence must survive

File C must consider File A material that never became a problem, including:

- exam;
- medications;
- history;
- workup;
- functional/safety context;
- clinically relevant non-neurologic context.

Do not drop such content merely because File B did not place it in `PROBLEM_MAP`.

File B determines problem architecture, not total note coverage.

## A/P compilation

Each A/P blueprint entry must be based on an existing File B problem handle.

Use File B exactly for:
- problem label;
- adoption/currentness;
- certainty;
- encounter role;
- status/descriptors;
- containment;
- causal/contributory relations;
- problem order;
- action ownership.

C may select the minimum-sufficient evidence and reasoning needed to support the already-resolved problem,
but may not alter the problem's semantics.

### A/P fields

`claim`
- use the File B label plus only status/descriptors already supported by A/B.

`support`
- cite supporting UNIT/record selectors needed for the note.

`counter`
- retain clinically meaningful counterevidence when it changes interpretation.

`reasoning`
- include only reasoning supported by A/source material and consistent with B.
- do not invent a new mechanism or rationale.

`actions`
- use existing File A ACTION IDs.

`primary_action_holder`
- follow File B action ownership.

`references_only`
- use when an action is relevant to another problem but is rendered under its primary home.

## Unresolved encounter role

If File B has:

```text
encounter_role=unresolved
```

C may not silently place that problem as PRIMARY or BACKGROUND.

C may:

- preserve the problem in an unresolved A/P blueprint area if the note architecture requires retention;
- leave its final A/P placement unresolved;
- carry an explicit upstream architecture gap.

C may not resolve the role itself.

## Shared actions

One shared action may relate to multiple problems.

When a single rendering home is needed:

1. use File B's `primary_action_holder`;
2. render the action once at its primary home;
3. use `references_only` for other relevant problems;
4. do not duplicate the full action plan across multiple problems.

Shared relevance does not create multiple action executions.

## Minimum-sufficient selection

Select enough material to preserve:

- defining features;
- meaningful chronology;
- current/historical distinction;
- attribution;
- certainty;
- counterevidence;
- workup state;
- management state;
- functional/safety information that changes care.

Do not copy the entire chart merely because the evidence is available.

Do not remove a clinically meaningful distinction solely for compression.

## Source order vs clinical order

Source order is not note order.

C may reorder already-supported units for:

- clinical chronology;
- disease-centered history;
- coherent workup presentation;
- problem-oriented A/P structure.

Reordering may not change meaning, attribution, time, or certainty.

## Cross-section reuse

Reuse is allowed only when the same evidence legitimately serves different note functions.

Examples:
- an event detail may appear in HPI and support A/P;
- a historical diagnosis may appear in NEURO_HX and as BACKGROUND A/P when File B supports that problem;
- a workup result may appear in WORKUP and support A/P.

Do not repeat material merely because it is important.

## Blueprint completeness

Before returning, check:

1. HPI follows current-episode chronology, not source order;
2. neurologic history is disease-centered and minimum sufficient;
3. OTHER_PMH contains relevant non-neurologic history without creating neurologic problems;
4. MEDS reflects presentation/home regimen rather than encounter rewrites;
5. EXAM reflects the current exam only;
6. WORKUP preserves ordered/performed/result distinctions;
7. every A/P entry maps to an existing File B problem;
8. File B role/certainty/currentness/containment/causality are unchanged;
9. unresolved problem role remains unresolved;
10. nonproblem evidence needed for the note survives;
11. clinically meaningful counterevidence is retained;
12. shared actions have one primary home;
13. the whole chart is not dumped into sections;
14. no final note prose appears;
15. output begins with `@@HANDOFF C_NOTE_BLUEPRINT_V1` and ends with `@@END`.

Return the blueprint only.
