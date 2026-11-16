# Review 149 — Clean A -> B clinical synthesis run

## Verdict

**Near-pass. Do not reopen architecture. One B problem-threshold question remains before C.**

The D-053 simplification worked:
- no normalized action-state enums;
- no unsupported `not_started` / `pending` / `unavailable` completion;
- source-qualified management wording is clinically faithful;
- prior A pointer drift is fixed.

## Stage A

### Pass

The prior T005/T006 pointer mismatch is corrected.

A preserves:
- no prior seizure history;
- no known family history;
- two-day event chronology;
- semiology and meaningful negative features;
- baseline interruptible staring;
- current diagnostic reasoning;
- CT completion without result availability;
- supplement history;
- ED exam;
- outside reported labs;
- source-local actions for EEG, MRI, levetiracetam, inpatient workup, safety and driving.

### Residual A issue

A still occasionally collapses mixed-polarity content into one span:
`Patient alert and oriented to person, place, and time. No focal neurologic deficit identified.`
with `polarity=affirmed`.

This is imperfect but the selector itself remains faithful. Whether to patch before C depends on whether downstream
uses polarity mechanically.

Reported-normal outside testing is also represented with `polarity=negated`, exposing that result-polarity semantics
remain somewhat ambiguous.

## Stage B

### Strong pass on diagnostic stance

P001 appropriately represents the current syndrome:
- new recurrent seizure-like events;
- semiology not clearly epileptic;
- PNES/nonepileptic events suspected/considered but not established;
- epileptic seizure remains under evaluation.

### Strong pass on management wording

ACTION_VIEWs preserve distinctions in ordinary source-qualified language:
- EEG needed;
- MRI needed;
- CT completed but result not available to Neurology;
- reportedly treated with levetiracetam on cruise ship;
- continue levetiracetam for now and reassess after EEG/MRI;
- favor inpatient completion of workup;
- safety precautions counseled;
- driving restriction counseled.

No retired action-state enums reappear.

## Remaining B architecture question

B creates:
`P002 = longstanding brief staring episodes when relaxed, responsive to calling/touch, not interrupting active conversation`
as a separate BACKGROUND problem.

This is probably over-problematization for the signer's target note.

Those spells:
- lack an independent neurologic diagnosis;
- are not independently managed;
- are not the reason for consultation;
- are being used mainly as a baseline comparator to distinguish the current events.

The target note handles them inside HPI/A&P reasoning under the primary seizure-like-event problem rather than as a
separate A/P block.

Proposed minimal B rule:

> A phenomenologically distinct chronic/baseline symptom does not become a separate BACKGROUND problem solely
> because it differs from the primary event. If it lacks independent neurologic disease identity or separate current
> assessment/management, preserve it as comparison/background evidence within the primary problem.

## Advancement

Await DeepSeek architecture adjudication on:
- collapse P002 into P001 evidence/contains vs keep separate;
- whether the residual A polarity issue must be patched before C.

Do not run C until this is resolved.

No new architecture or additional state layer is needed.
