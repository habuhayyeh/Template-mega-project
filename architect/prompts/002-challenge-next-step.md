# Prompt for the note expert — challenge the next-step decision

Use this with the senior neurology note writer who knows your preferred note structure. Attach the
current B output, your target note/example, and the architect decision. Do not attach identifiers.

---

You are a senior neurology note writer. I need you to challenge an architecture decision, not write
prompt text.

## Context

The runtime is:

```text
Scribe packet
  -> A source-local ingestion
       semantic spans
       action spans (source wording only)
  -> B clinical synthesis
       reconciliation
       problem architecture
       diagnostic stance
       action selection/ownership
       source-qualified management wording
  -> C note compiler (blueprint)
  -> render
```

B is now clinically close. Actions are source-qualified and enum-free. C has not been run.

## The concrete problem

The current packet has current recurrent events plus longstanding baseline staring spells. The target
note wants the baseline spells as **comparator evidence inside the primary problem**, not a separate A/P
block.

B currently creates a second BACKGROUND problem for the baseline spells.

A also sometimes collapses mixed polarity:

```text
Patient alert and oriented. No focal neurologic deficit identified.
```

into one span with `polarity=affirmed`. The selector text is faithful.

## The architect decision

1. Patch B’s problem threshold first.
2. Defer A polarity; treat it as advisory; patch A only if C produces a polarity inversion.
3. Then run C, then render.

The proposed B rule:

> A chronic or baseline phenomenon becomes a separate BACKGROUND problem only if it has independent
> neurologic disease identity or its own current assessment/management. If it is only comparator/context
> for the primary problem, it stays inside that problem as comparator evidence.

Minimum B test:

- current events + baseline staring spells, no independent diagnosis/management -> one PRIMARY problem,
  baseline as comparator, no separate block;
- known chronic epilepsy with independent management -> BACKGROUND problem remains.

## Your task

Challenge the decision from the note-writer’s point of view.

### 1. B threshold

- Is the rule clinically correct?
- When does a chronic/baseline phenomenon genuinely deserve its own BACKGROUND block?
- Is “independent disease identity or independent management” the right test?
- Would you ever keep baseline spells separate because the reader needs them as a standalone problem?
- What note-level harm occurs if they are contained vs separated?
- What is the smallest test that proves the rule without reopening B?

### 2. A polarity

- Is deferring A polarity safe?
- Where would a mixed-polarity span actually damage the final note?
- Can C rely on B’s stance plus the exact selector, or must A split now?
- If A is deferred, what must C never do with A polarity?
- What single output would prove A needs patching?

### 3. C design

The proposed C:

- owns section allocation, HPI chronology, history/meds/exam/workup placement, A/P evidence and
  counterevidence, action placement/ownership, order;
- must not decide problems, roles, diagnosis, causality, currentness, action state or prose;
- maps B’s typed groups to a closed set of canonical render operators;
- outputs a blueprint ending at section + problem + operator + members + order + source refs;
- renderer only lexicalizes.

Challenge it:

- Is that division clinically realistic?
- Where does C unavoidably need clinical judgment?
- Is a closed operator set workable for the note style you expect?
- What operators/groups are missing for HPI chronology, contained baseline, diagnostic uncertainty,
  counterevidence, shared actions, medication-at-presentation, exam, workup?
- Where does blueprint end and prose begin in practice?
- What would make the renderer reopen decisions despite instructions?

### 4. Gates

- Are the proposed gates sufficient?
- What must pass before C, and what must pass before render?
- What test would catch C becoming a second problem architect?
- What test would catch a wrong B threshold that still looks clinically plausible?
- What would you refuse to accept as “good enough”?

### 5. What would you change?

- Would you patch B, patch A, or go to C?
- What would you delete, defer or merge?
- What is the biggest risk in the next step?
- What is the smallest mitigation?

## Constraints

- No new runtime stage unless evidence demands it.
- No normalized action-state enums.
- No same-model semantic validator.
- No prompt micro-tuning for cosmetic variance.
- One Ask invocation with logical phases.
- Final writer should be a constrained lexicalizer over decided content.
- Source fidelity and problem identity matter more than prose polish.
- C must not reopen A/B decisions.

## Deliverable

A one-page decision:

1. agree or disagree with the architect;
2. exact order of work;
3. pass criteria for each gate;
4. what to delete or defer;
5. the biggest risk and the smallest mitigation.

Use your knowledge of how I want the final note to read. Challenge the architecture where it would produce
the wrong note, not where the wording is merely different.
