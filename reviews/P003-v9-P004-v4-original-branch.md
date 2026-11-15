# P003 v9 / P004 v4 review — original architecture branch

## P003 v9
**Verdict: ACCEPT ARCHITECTURE — one mechanical contract fix before implementation**

The provenance/event-date defect is fixed correctly:
- O8 remains the timing source.
- No provenance date is promoted into an infarct event date.
- The signer preference against bare `ago` is respected by anchoring the relative interval to presentation.

One internal contract mismatch remains.

### Anchored relative-time rendering is not yet an allowed transformation

The acceptance target now requires:

`known left MCA infarct two years prior to presentation`

but the Handoff says:

`left MCA infarct two years ago`

and transformations 1–9 do not authorize `ago -> prior to presentation`.

Under I8, the words `prior to presentation` are therefore currently new output content.

This is not a design objection. The signer already established the style rule that relative dates should be absolute or anchored to presentation rather than written as `ago`.

### Required fix

Add one bounded transformation, for relative-time display only:

> A relative interval stated as `X ago` may render as `X prior to presentation` (or the exact approved anchored equivalent) when the source interval is preserved unchanged. This changes only the reference wording; it does not calculate or infer an absolute date.

Then update:
- the permitted-transform count;
- I8;
- PASS wording;
- any trace-table transformation range.

Do **not** permit general synonym replacement or date arithmetic.

After that mechanical edit, P003 is ready for signer implementation approval.

## P004 v4
**Verdict: ACCEPT HOLD STATE**

P004 now correctly recognizes that D-015 cannot be implemented on the present substrate because the management -> problem target is absent from the representation.

Accepted next sequence:

1. implement and validate P003;
2. create a separate representation proposal that exposes the management-to-problem relation source-faithfully;
3. update the frozen substrate/oracle under that proposal;
4. return to P004 for implementation.

The following P004 corrections are accepted:
- O9 remains discarded;
- O10 remains discarded from A/P;
- no hand-written assignment-count claim;
- no medication/class heuristics;
- O54 may later render under the chronic infarct block only after an explicit decision supersedes D-014 for that context.

No signer escalation is needed for either proposal at this point.
