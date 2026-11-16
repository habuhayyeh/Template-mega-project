# DeepSeek architecture verdict — retire normalized action states and B1

**Evidence:** review 148, clean-packet A→B1 run.
**Decision:** remove normalized decision/execution/response/result enums. Fold action reconciliation into B2.
Delete B1 as a separate runtime stage.

## Why

The same schema-completion failure survived:

- optional state slots in A2;
- exact-phrase asserted states in A2;
- moving normalization from A2 to B1;
- repeated prohibitions;
- bare-shorthand rules;
- a cleaner Scribe packet.

B1 still invents:

- `result=unavailable` for a reported normal result;
- `result=unavailable` for unspecified additional testing;
- `execution=not_started` for “needed” EEG/MRI;
- `result=pending` for CT completed but not reviewed;
- `execution=not_started` for “continue for now”;
- `execution=not_started` for “favored inpatient workup.”

This is structural. More prompt rules will not fix it.

## New runtime

```text
Scribe V2.2 packet
  -> A source-local ingestion
       semantic spans
       action spans (wording only)
  -> B clinical synthesis
       reconciliation
       problem architecture
       diagnostic stance
       action selection/ownership
  -> C note compiler
       blueprint
  -> Render
       source-qualified prose
```

No B1.

## A action lane

Keep:

- source_record;
- selector;
- target;
- operation;
- action_phrase;
- speaker/source;
- local identity only if explicit;
- setting/time/condition;
- unresolved.

No state enums. No raw state buckets.

## B clinical synthesis

B owns:

- cross-record reconciliation;
- episode grouping;
- problem identity/containment/role;
- diagnostic stance;
- which A action spans belong to each problem/plan;
- action ownership;
- source-qualified plan wording.

B may not invent an action absent from A.

For each selected action, B should preserve the source-qualified wording, e.g.:

- “reportedly treated with levetiracetam”;
- “EEG/MRI needed”;
- “continue levetiracetam for now, reassess after EEG/MRI”;
- “favor inpatient workup”;
- “safety/driving counseling discussed.”

Those distinctions do not need enums. They need the source wording plus problem ownership.

If B needs to group actions into an episode, it may, but it must cite the A spans and keep separate when
unsupported.

## C render

C allocates the selected source-qualified actions to the plan. Renderer lexicalizes only.

No new action state, no enum, no late action interpretation.

## A pointer drift

The T005/T006 drift is a separate A defect. It does not justify keeping B1.

A’s exact-record/selector invariant already forbids it. Run A with exact pointer lint after the B1 removal.
If the drift persists, treat it as an A contract issue, not a reason to restore B1.

## What to retire

- B1 action-state interpretation stage;
- B1 state oracle;
- normalized action-state enums in A/B;
- any test that scores enum normalization.

Keep the A2 wording-only test, adjusted to A runtime.

## Test

1. Run A on the clean packet; lint exact pointers/selectors.
2. Run B2 clinical synthesis on the frozen A.
3. Check:
   - every selected action cites an A span;
   - no action invented;
   - source-qualified wording preserved;
   - problem/plan ownership correct;
   - no normalized state enum.
4. Then C blueprint; only then render.

No new stage. This removes one.

No acceptance, production change or Phase 0.
