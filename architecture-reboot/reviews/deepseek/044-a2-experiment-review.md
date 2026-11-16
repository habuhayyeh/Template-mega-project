# DeepSeek review — A2 asserted-state isolation experiment

**Reviewed:** proposal 143, both A2 test modules, A2 oracle.
**Status:** peer review. No implementation.

## Verdict

The experiment is worth running, but it is **not yet a clean A/B comparison**.

The asserted-state condition contains target-specific examples that the current-slot condition does not.
Those examples map directly to the failure cases the oracle is testing. That biases the result.

Fix the examples before asking for the two runs.

## Confound — unequal examples

Current-slot condition:
- schema only;
- no examples of how to leave fields absent.

Asserted-state condition:
- examples use exact target-packet phrases:
  - `Plan: CT head, basic labs, urinalysis`;
  - `started on a Keppra drip`;
- examples explicitly show no execution/result line.

Those are the exact patterns the oracle scores. The asserted condition is therefore being taught the
answers for the hardest items.

### Fix

Either:

1. give both conditions the same **generic** examples using phrases not in the frozen packet, or
2. remove examples from both and rely on the schema.

If examples remain, both conditions must include:

- one example with a stated state;
- one example with an absent state dimension;
- one example showing that absence is no field/line.

Do not use target-packet phrases in either condition.

## What is controlled correctly

- same input packet;
- same action inclusion list;
- same source rules;
- same state invariants;
- A2-only, no semantic lane;
- fresh sessions;
- same oracle.

Apart from the examples, the intended difference is only the representation.

## Oracle

The oracle is a valid operationalization of existing action invariants. It is case-specific, not a
general semantic policy. Do not use a pass here to claim general A2 correctness.

The mechanical checks are appropriate. Exact substring lint must be run outside the model.

## Interpretation guard

- current FAIL + asserted PASS -> schema completion is supported, but only if examples are equalized.
- both FAIL -> simplify further; do not blame lane interference yet.
- both PASS alone + unified A FAIL -> lane interference becomes the leading explanation.

## Recommendation

1. Equalize examples or remove them.
2. Run the two conditions.
3. Score only against the A2 oracle.
4. Do not change B/C or the active A contract before the result.

No acceptance, production change or Phase 0.
