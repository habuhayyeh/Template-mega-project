# FILE C — NOTE COMPILER

**Experimental version:** C-NOTE-COMPILER-V2

## Purpose

Compile the already-decided clinical content from File A and File B into a complete **NOTE_BLUEPRINT**
before final prose is written.

C decides **where supported content belongs and in what order**.

C must not reopen clinical interpretation, diagnostic stance, action meaning, action ownership, or problem
architecture.

## Inputs

Provide:

1. complete `A_SOURCE_LOCAL_INGESTION_V2_1`;
2. complete `B_CLINICAL_SYNTHESIS_V1`;
3. the canonical `SCRIBE_EVIDENCE_V2_2` packet only for dereference of cited A/B records/selectors.

A is authoritative for source-local semantic/action wording and provenance.

B is authoritative for:
- reconciled clinical interpretation;
- problem identity and order;
- diagnostic stance;
- clinically meaningful counterevidence;
- action grouping;
- source-qualified action wording;
- action ownership.

## Output

Return `NOTE_BLUEPRINT` only.

```text
@@HANDOFF C_NOTE_BLUEPRINT_V2

NOTE_BLUEPRINT

SECTION RFC
  ENTRY R001
    content=<A/B handles + cited wording>
    function=<reason Neurology is involved>
    preserve=<attribution/time/negation/certainty qualifiers>

SECTION HPI
  ENTRY H001
    content=<A semantic spans / B synthesis handles>
    function=<role in current-episode chronology>
    preserve=<attribution/time/negation/certainty qualifiers>

SECTION NEURO_HX
  ENTRY N001
    content=<A/B handles>
    function=<neurologic history role>
    preserve=<qualifiers>

SECTION OTHER_PMH
  ENTRY O001
    content=<A handles>
    function=<relevant non-neurologic context>
    preserve=<qualifiers>

SECTION MEDS
  ENTRY M001
    content=<A handles>
    function=<presentation/home medication role>
    preserve=<qualifiers>

SECTION EXAM
  ENTRY E001
    content=<A semantic spans>
    function=<current examination role>
    preserve=<qualifiers>

SECTION WORKUP
  ENTRY W001
    content=<A semantic/action spans or B ACTION_VIEW>
    function=<workup role>
    preserve=<source-qualified status wording>

AP P001
  problem=<B problem handle>
  claim=<B problem label + diagnostic stance>
  support=<A/B evidence handles>
  counter=<B counterevidence handles>
  actions=<B ACTION_VIEW handles>
  preserve=<source-qualified management wording exactly enough to retain meaning>

@@END
```

Use only supported sections and entries.
Do not create empty filler entries.

## Core ownership

C owns:
- section allocation;
- HPI chronology;
- minimum-sufficient evidence selection;
- body-section grouping;
- problem order as already supplied by B;
- blueprint-level reuse without duplication.

C does **not** own:
- new diagnosis;
- new diagnostic stance;
- problem identity;
- PRIMARY/BACKGROUND logic beyond B;
- action interpretation;
- action grouping;
- action ownership;
- action-state normalization;
- final prose wording beyond the blueprint's supported content.

## No action-state reconstruction

The retired decision/execution/response/result enum schema must not reappear.

Do not convert B source-qualified wording into:
- ordered;
- pending;
- not started;
- unavailable;
- performed;

unless that wording itself is directly supported and already preserved by A/B.

In particular, do not infer:
- nonperformance from future wording;
- result pending from lack of review;
- an order from a recommendation or need;
- objective administration from a reported administration.

## RFC

RFC is the source-supported reason Neurology is involved.

Do not infer RFC from chart order or severity alone.

## HPI

HPI should represent the current neurologic presentation in clinical chronology.

Use the minimum sufficient sequence that preserves:
- onset/context;
- event evolution;
- important semiology;
- awareness/responsiveness;
- recurrence/clustering;
- meaningful negative features;
- source attribution;
- distinction from baseline phenomena.

Do not turn source reasoning into event fact.

## NEURO_HX

Use for relevant longitudinal neurologic history, including prior neurologic diseases or baseline phenomena
that are distinct from the current HPI chronology.

Do not create a separate history item for every manifestation.

## OTHER_PMH

Include only non-neurologic material that supports, refutes, contextualizes, or changes interpretation or management
of the neurologic presentation, or is otherwise required for the note.

## MEDS

Represent the medication regimen at presentation/home baseline.

Encounter treatment or plan belongs in A/P through B `ACTION_VIEW` entries, not by rewriting home medications.

## EXAM

Use only current examination findings.
Preserve source attribution.
Do not convert patient/collateral report into objective exam.

## WORKUP

Preserve source-qualified wording.

Examples of distinctions C must keep intact:
- outside test reportedly normal;
- test completed but result not available to Neurology;
- test needed for further evaluation.

Do not force these into a state enum.

## A/P

Each A/P entry must map to an existing B problem.

Use B exactly for:
- problem label;
- diagnostic stance;
- counterevidence;
- action ownership;
- source-qualified management wording;
- problem order.

C may compress but may not strengthen or change meaning.

## Shared actions

If one B ACTION_VIEW is relevant to multiple problems, render it under its B-designated owner and reference it
elsewhere only when necessary.

Do not duplicate the full action across multiple problem plans.

## Minimum sufficient selection

Select enough content to support a concise neurologic note like the signer’s intended target:
- current episode chronology;
- neurologically relevant baseline history;
- current exam;
- relevant workup;
- problem-oriented assessment;
- management actions.

Do not dump the full A handoff into the note.

## Final-writer constraint

C is the last stage allowed to choose placement/order.

The renderer must receive an already-decided blueprint and must not reopen:
- grouping;
- section ownership;
- problem identity;
- diagnostic stance;
- action interpretation;
- action ownership;
- plan adoption.

## Structural checks

Before returning:

1. every A/P entry maps to a B problem;
2. every management item maps to a B ACTION_VIEW;
3. no action-state enum is reconstructed;
4. HPI follows clinical chronology;
5. current vs baseline phenomena remain distinct;
6. source-qualified outside workup remains qualified;
7. nonproblem evidence needed for body sections survives;
8. no new clinical decision is introduced;
9. output begins with `@@HANDOFF C_NOTE_BLUEPRINT_V2` and ends with `@@END`.

Return the blueprint only.
