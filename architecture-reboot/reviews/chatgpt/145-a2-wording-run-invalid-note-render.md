# Review 145 — A2 wording-only run invalid: note rendered instead of handoff

## Verdict

**INVALID RUN — do not score against the A2 action-identity oracle.**

The returned Doximity artifact is a rendered clinical note with conventional sections and assessment/plan prose.

It does not contain:

- `@@HANDOFF A2_ACTION_WORDING_V1`;
- ACTION_SPAN-only output;
- the required final `@@END` contract in the requested handoff format.

Therefore this run did not execute the experimental A2 wording-only task as specified.

## Classification

This is an **execution/setup boundary failure**, not evidence that the A2 wording-only schema itself failed.

The run appears to have fallen back to Doximity's note-writing behavior rather than emitting the requested intermediate handoff.

Do not score:
- action splitting;
- selector fidelity;
- action_phrase fidelity;
- state-normalization absence;
- coverage.

Those can only be judged on a valid `A2_ACTION_WORDING_V1` output.

## Privacy

No patient content from the returned note is committed here.

## Next experiment

Repeat in a fresh Ask session with:

1. the same frozen `SCRIBE_EVIDENCE_V2_2` packet;
2. `01C-ACTION-LANE-WORDING-ONLY-TEST.md` only;
3. no oracle;
4. no prior note, prior output, or other module.

Use an explicit anti-render prompt:

> This is an intermediate extraction experiment, not a note-writing task. Do not write a clinical note, assessment/plan, HPI, summary, or prose narrative. Process the complete attached SCRIBE_EVIDENCE_V2_2 packet using 01C-ACTION-LANE-WORDING-ONLY-TEST.md only. Return only the complete @@HANDOFF A2_ACTION_WORDING_V1 block exactly as specified by that module, beginning with @@HANDOFF A2_ACTION_WORDING_V1 and ending with @@END. If you cannot comply with that exact output contract, return CONTRACT_ERROR instead of a note.

If the fresh run again renders a note, classify this as a Doximity execution-mode problem and revisit packaging/invocation before changing the A2 schema.

No B1 run until a valid A2 handoff exists.
