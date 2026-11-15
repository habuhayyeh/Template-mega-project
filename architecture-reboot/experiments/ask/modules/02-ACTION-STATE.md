# DRAFT — DO NOT RUN YET

File 2 is defined but not active. Run only after File 1 passes the canonical reference/action-fidelity rerun.

# FILE 2 — ACTION STATE

**Experimental version:** F2-ACTION-V1

## Function

Build a compact, source-backed map of **management and diagnostic action states** from:

1. the immutable Scribe V2.2 packet; and
2. the File 1 reconciled-evidence handoff.

File 2 reconciles **what action was discussed or executed, by whom, and in what state**.

It does **not** decide the final encounter plan and does not attach actions to neurologic problems.

Do not write the note.

## Why this is separate

Action-state errors are clinically material and different from ordinary fact reconciliation.

The following are not interchangeable:

- considered;
- recommended;
- planned;
- ordered;
- administered/started;
- performed;
- completed;
- held;
- stopped/discontinued;
- result pending;
- result available.

File 2 exists to prevent these states from silently upgrading one another.

## Canonical evidence

The Scribe V2.2 packet remains the canonical evidence store.

Use File 1 only as a compact index/context layer.

Dereference the original Scribe record IDs whenever the action wording or state is uncertain.

## Output

Return a compact handoff:

```text
@@HANDOFF F2_ACTION_V1

ACTION A001 — <short action target>
  refs: <all material Scribe record ids>
  state_history:
    - <STATE> | actor=<source-supported actor or -> | timing=<source-supported timing or -> | ref=<record id>
    - <STATE> | actor=<...> | timing=<...> | ref=<record id>
  result_state: <state + ref, only when applicable>
  patient_response: <explicit response/preference + ref, only when applicable>
  unresolved: <material action-state uncertainty + refs, only when applicable>

ACTION A002 — ...

@@END
```

Use only fields that carry information.

Do not add a final-plan field.

## One ACTION = one target

Group mentions only when they refer to the same management/test target.

Examples:
- MRI brain;
- EEG;
- levetiracetam/Keppra;
- CT head;
- seizure precautions;
- admission/inpatient workup;
- driving restriction.

Do not combine unrelated actions merely because they occur in the same encounter or problem.

## Allowed source states

Map source wording to the narrowest supported state:

```text
CONSIDERED
RECOMMENDED
PLANNED
ORDERED
STARTED
ADMINISTERED
PERFORMED
COMPLETED
HELD
STOPPED
DISCONTINUED
DEFERRED
NOT_INDICATED
UNKNOWN
```

Use the state only when the source supports it.

If the wording cannot safely map to one state, use:

```text
UNKNOWN | wording="<short source-faithful wording>"
```

Do not guess.

## State-history rule

Preserve meaningful state evolution rather than collapsing it to one "final" state.

Example:

```text
ACTION A010 — Keppra 1500 mg load
  refs: P1.053,P1.054,P1.055
  state_history:
    - RECOMMENDED | actor=Neurology | timing=current ED | ref=P1.054
    - ORDERED | actor=ED | timing=current ED | ref=P1.054
    - DISCONTINUED | actor=ED after neurology discussion | timing=current ED | ref=P1.055
```

Do not infer whether the dose was administered unless a source says it was.

## Test execution vs result state

For diagnostic tests, action state and result state are separate.

Examples:

```text
PERFORMED != RESULT_AVAILABLE
ORDERED != PERFORMED
PLANNED != ORDERED
```

When applicable, use:

```text
result_state:
  PENDING
  PRELIMINARY
  FINAL_AVAILABLE
  REPORTED_SECOND_HAND
  UNAVAILABLE
  UNKNOWN
```

A reported historical/second-hand normal result is not the same as a directly available report.

## Actor / owner

Preserve only explicitly supported actor/owner information.

Possible wording may include:
- Neurology;
- ED;
- ship medical;
- EMS;
- patient;
- family/collateral;
- unknown.

Do not infer ownership from the action itself.

## Timing / setting

Preserve only timing/setting needed to distinguish action states.

Examples:
- ship medical Wednesday;
- ship medical Thursday;
- EMS transfer;
- current ED;
- proposed inpatient;
- outpatient option;
- after EEG/MRI;
- unknown.

Do not create false precision.

## Patient response / preference

Keep explicit patient/family response separate from clinician action state.

Examples:
- agreed;
- declined;
- preferred inpatient workup;
- preferred outpatient testing;
- no response documented.

Patient preference does not become clinician decision.

## Unresolved action state

Use `unresolved:` when sources leave a materially important state unclear.

Examples:
- unclear whether Keppra bolus was actually administered;
- MRI discussed but not documented as ordered;
- test performed but final report unavailable;
- conflicting documentation of stop/continue.

Do not resolve the uncertainty by choosing the more polished note.

## Executed actions already appearing in F1

F1 may include an executed intervention when needed to preserve event chronology.

That does not remove the need for File 2 to reconstruct the action-state history from the original source records.

## Forbidden decisions

Do not decide:
- whether an action belongs to an independent neurologic problem;
- final current encounter plan/adoption;
- PRIMARY/BACKGROUND problem role;
- causal relation between problems;
- note inclusion;
- section placement;
- final wording.

Those belong downstream.

## Compression

One ACTION should normally summarize all material mentions of the same target.

Do not emit one action object per source mention.

Do not copy source prose unless needed to preserve an unresolved state.

## End check

Before returning:

1. every ACTION refers to one action/test target;
2. every state has a source record reference;
3. no source state was upgraded;
4. order/recommendation/performance/result states remain distinct;
5. patient preference remains separate from clinician decision;
6. no final encounter plan was chosen;
7. no problem ownership was assigned;
8. output ends with `@@END`.

Return the handoff only.
