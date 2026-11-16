# Prompt for the architect — next structural step

Use this prompt with the architect. It is intentionally about broad structure, not prompt wording.

---

You are the project architect. Do not write code, prompt text, or schemas yet. I need a decision on the next
structural step and its gate.

## Where we are

Current runtime, D-053:

```text
Scribe V2.2 packet
  -> A source-local ingestion
       semantic spans
       action spans (source wording only)
  -> B clinical synthesis
       reconciliation
       problem architecture
       diagnostic stance
       action selection/ownership
       source-qualified management wording
  -> C note compiler
       NOTE_BLUEPRINT
  -> render
```

B1 and all normalized action-state enums are retired. They repeatedly caused schema completion:
plan -> ordered, need -> not_started, no result -> unavailable, continue -> not_started.

What is working on the clean packet:

- A pointer integrity is fixed;
- A preserves the current events, baseline spells, exam, outside workup, reasoning, safety and actions;
- B's primary diagnostic stance is clinically close to the target note;
- B action wording is source-qualified and enum-free:
  - EEG/MRI needed;
  - CT completed but result not available to Neurology;
  - reportedly treated with levetiracetam;
  - continue levetiracetam for now; reassess after EEG/MRI;
  - favor inpatient workup;
  - safety/driving counseling;
- no unsupported order/performance/result enums.

C exists as a contract but has not been run.

## Example of the current output shape

Synthetic example, not patient data:

```text
A:

SPAN S001
  source_record=T010
  selector=three falls since June
  assertion_type=statement
  material_role=current_episode
  speaker_source=SPK2
  polarity=affirmed
  certainty=unstated

ACTION_SPAN A001
  source_record=P1.010
  selector=EEG and MRI are needed
  target=EEG/MRI
  operation=needed
  action_phrase=needed

B:

PROBLEM P001
  label=current recurrent events under evaluation
  encounter_role=PRIMARY
  diagnostic_stance=Current events are not clearly epileptic; nonepileptic events are suspected but not established; epileptic seizure remains under evaluation.
  evidence=S001,S002
  counterevidence=S003
  contains=baseline staring spells as comparator evidence
  order=1

PROBLEM P002
  label=chronic baseline staring spells
  encounter_role=BACKGROUND
  diagnostic_stance=Longstanding brief spells, responsive, different from current events.
  evidence=S004
  order=2

ACTION_VIEW AV001
  source_actions=A001
  target=EEG/MRI
  wording=EEG/MRI needed for further evaluation
  owner=P001
```

## Open issue 1 — B problem threshold

B created P002 as a separate BACKGROUND problem for the chronic baseline spells.

The signer's target note does not want a separate A/P block for them. They function as baseline comparator
evidence inside the primary problem. They are not independently diagnosed, independently managed, or
separately evaluated as a disorder.

Candidate rule:

> A phenomenologically distinct chronic/baseline symptom does not become a separate BACKGROUND problem
> solely because it is chronic and different from the primary event. If it lacks independent neurologic
> disease identity or separate current assessment/management, keep it as comparison/background evidence
> inside the primary problem.

## Open issue 2 — A polarity

A still sometimes collapses mixed-polarity text:

```text
Patient alert and oriented. No focal neurologic deficit identified.
```

into one span with `polarity=affirmed`.

Reported-normal outside labs are sometimes `polarity=negated`.

The selector text remains faithful. The question is whether C may treat A polarity as advisory and rely on
the selector, or whether A must be patched before C.

## What I need from you

1. **Next step:** patch B's problem threshold, patch A's polarity, or proceed to C?
2. **If patch B:** state the one rule and the minimum test that proves it without reopening B.
3. **If proceed to C:** give the broad C design:
   - what C owns and must not own;
   - how it should use typed groups/canonical render operators;
   - where the blueprint ends and the renderer begins;
   - how to keep the final writer from reopening clinical decisions.
4. **Sequence and gates:** what must pass before C, and what must pass before render.
5. **What not to build:** stages, validators, enums, micro-prompts, etc.
6. **Biggest risk** in the next step.

## Constraints

- no new runtime stage unless evidence demands it;
- no normalized action-state enums;
- no same-model semantic validator;
- no prompt micro-tuning for cosmetic variance;
- one Ask invocation with logical phases;
- final writer should be a deterministic lexicalizer over already-decided typed content;
- source fidelity and problem identity are more important than prose polish;
- C must not reopen A/B decisions.

## Deliverable

A one-page decision:

- recommended next step;
- exact order of work;
- pass criteria for each gate;
- what to delete or defer;
- the main risk and the smallest mitigation.

Do not redesign the whole architecture. Decide the next structural move.
