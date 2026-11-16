# DeepSeek pre-run review — final A → B1 patch

**Verdict:** READY TO RUN.

No blocker.

## 1. Mixed-polarity A1

The A contract now:

- requires splitting clauses with different polarity/certainty/provenance/type/role;
- forbids one global polarity across mixed clauses;
- adds a safety fallback: if not split, `polarity=unresolved` with the mixed propositions explained.

This closes the silent global-polarity failure. The fallback can over-mark unresolved, but that is safer
than a false affirmed/negated and is reviewable.

## 2. Specialty shorthand in B1

B1 now says:

- bare service label + intervention shorthand is not an order;
- an explicit plan/recommend/order/administer/perform/hold/stop/discontinue verb is required;
- ambiguous state stays absent/unresolved.

This closes the `Neuro: Keppra load 1500` → `ordered` failure without forcing a false state.

## 3. Opposite failure risk

The new rules may produce more `unresolved` output and omit some legitimate state. That is acceptable for
this run: under D-052 the final output is reviewed, and an omitted state is safer than an invented one.
Do not add more rules before seeing the rerun.

## 4. B1 boundaries

B1 still preserves:

- plan vs order vs performance;
- reported vs objective performance;
- decision/execution/response/result separation;
- no repair/no discovery;
- `A_ACTION_GAP` for bundled/omitted A actions.

## 5. Integration controller

`02B` passes the Stage A `ACTION_SPANS` lane directly into B1 in one invocation. It does not pass problem
architecture, section allocation, or prose. Correct.

## 6. Instruction conflicts

No blocking conflict.

One non-blocking wording issue: B1 still says “frozen A2,” which can imply physician-reviewed under the
superseded D-051. Under D-052, replace it with “completed A action lane” when convenient. It does not
change this run.

## 7. Additional patch

None required before the rerun.

Run the frozen seizure packet through `02B`, return both handoffs unchanged, and score against the
existing A/B1 action oracles.

No B2/C/render. No acceptance, production change or Phase 0.
