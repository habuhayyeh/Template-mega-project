# Review 147 — A V2.1 -> B1 rerun

## Verdict

**Substantially improved; two hidden semantic blockers remain. One final bounded contract patch, then rerun.**

The second integrated A -> B1 run fixes the prior consult-state upgrade, actor-label misuse, ambiguous preference
conversion, uncertain Keppra grouping, and A019 EEG/MRI bundling.

## Remaining blocker 1 — mixed-polarity A1 selectors still collapse

Examples:

- `Neurological: no focal deficit present; alert and oriented to person, place, and time`
  is emitted as one span with `polarity=affirmed`.
- `no posturing of arms/legs; ... feet twisted inwards`
  is emitted as one span with `polarity=negated`.

These selectors contain materially different propositions with different polarity. The prior split rule was not
reliably followed.

Patch:
- split remains preferred;
- safety fallback: if a mixed-polarity selector is not split, `polarity=unresolved` and an unresolved note are
  mandatory. Never assign a single affirmed/negated polarity across mixed propositions.

## Remaining blocker 2 — bare specialty shorthand still upgraded to order

A007:
`Neuro: Keppra load 1500; will come evaluate`

B1 emits:
`execution=ordered`

The source shorthand contains no explicit order verb/state. This is the same class of hidden state promotion D-049
was intended to prevent.

Patch:
- service-label + intervention shorthand without an explicit state verb does not establish planned/recommended/
  ordered/performed;
- state remains absent/unresolved unless another phrase in the same cited selector explicitly carries state.

## What is now acceptable

Minor imperfections that are transparent/reviewable should not block advancement after the next rerun, including:
- hedged admission wording represented as planned with unresolved;
- conservative unresolved actor fields;
- stylistic target/operation normalization;
- nonessential omission variance that does not silently change care meaning.

## Advancement

Rerun the same A -> B1 integration once after the bounded patch.

If:
1. mixed-polarity spans no longer receive a false single polarity; and
2. bare Keppra shorthand no longer becomes an order;

then advance to B2/problem architecture without further A/B1 tuning.

No architecture change. No new stage. No validator.
