# B problem-threshold fixtures

**Purpose:** test the counterfactual independence rule in `02-CLINICAL-SYNTHESIS.md`.

These are development fixtures for B problem architecture only. They are not production patient data and are not
an oracle for wording.

## Fixture 1 — baseline comparator should NOT become a separate problem

Input concepts:
- current recurrent episodes of impaired awareness are the reason for neurologic evaluation;
- patient has longstanding brief staring only when relaxed;
- baseline staring is interruptible by voice/touch;
- clinician states baseline staring appears different from the current events and does not clearly sound like seizure;
- no separate diagnostic workup, treatment, or management is directed at the baseline staring.

Expected architecture:
- one current presenting problem for the recurrent events;
- baseline staring retained as comparison/background evidence within that problem;
- **no separate BACKGROUND problem** for the staring spells.

Failure:
- creating a second problem solely because the baseline spells are chronic or phenomenologically distinct.

## Fixture 2 — independent established neurologic disease SHOULD remain separate

Input concepts:
- current transient episodes are being evaluated as the primary problem;
- patient also has an established prior ischemic stroke with persistent residual hemiparesis;
- the stroke is an independently established neurologic disease identity;
- current notes carry the stroke as relevant neurologic history even though it is not the reason for consultation.

Expected architecture:
- primary problem for the current transient episodes;
- separate BACKGROUND problem for established prior ischemic stroke;
- residual hemiparesis remains contained under the stroke unless it has its own independent current assessment question.

Failure:
- collapsing the established stroke into generic context under the transient-event problem.

## Fixture 3 — distinct current assessment question SHOULD become separate

Input concepts:
- current seizure-like events are under evaluation;
- during the same encounter, a new persistent unilateral foot drop is also being independently evaluated with its own
  localization/differential and planned diagnostic workup;
- the foot drop is not adequately explained by the seizure-like events.

Expected architecture:
- one problem for seizure-like events;
- one separate current neurologic problem for the foot drop/localization question.

Failure:
- absorbing the foot drop into the seizure-like-event problem merely because both are neurologic and current.

## Scoring invariant

For each candidate item, apply the counterfactual question:

> If the primary presenting problem were removed, would this item still justify its own neurologic assessment/problem
> block because of independent disease identity, separate current assessment, or separate current management?

The fixture passes only when:
1. Fixture 1 does **not** create a separate problem;
2. Fixture 2 **does** create a separate BACKGROUND problem;
3. Fixture 3 **does** create a separate current problem.

Do not score prose style, labels, or problem numbering.
