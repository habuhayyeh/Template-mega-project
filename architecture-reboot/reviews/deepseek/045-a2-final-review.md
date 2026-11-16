# DeepSeek final review — A2 isolation experiment

**Reviewed:** both A2 test modules after example removal, A2 oracle.
**Status:** peer review. No implementation.

## Verdict

The target-packet examples are gone. One confound remains.

The asserted-state module tells the model the hypothesis:

> test whether state-with-evidence triples prevent action-slot schema completion.

That signals the desired behavior. It can bias the asserted arm toward omission.

The current-slot module’s purpose is neutral by comparison.

## Fix

Remove the hypothesis from both runnable modules. Keep it in proposal 143.

Use a neutral purpose in both, e.g.:

> A2-only action-lane extraction condition.

Do not say “prevent schema completion,” “avoid filling,” or “test whether this representation works.”
The runnable prompt should describe the task, not the expected result.

## What is clean

- no target-packet examples in either arm;
- same input packet;
- same action inclusion list;
- same source rules;
- same state invariants;
- A2-only, no semantic lane;
- same oracle;
- fresh sessions.

The remaining difference is the intended representation plus its required state-evidence fields.

## Oracle

The oracle is a valid case-specific operationalization. Do not treat a pass as general proof.

## Then run

1. current-slot A2 in a fresh Ask session;
2. asserted-state A2 in a separate fresh Ask session;
3. same frozen packet;
4. no oracle attached to Doximity;
5. return both outputs unchanged.

No B/C, active-A replacement or production change.

No acceptance. No Phase 0.
