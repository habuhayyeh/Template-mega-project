# DeepSeek review — internal B coverage census and A closure

## Internal B coverage follow-up

**READY TO RUN.**

The experiment is clean:

- same clean packet;
- two fresh runs;
- coverage census before synthesis;
- record IDs only;
- no selectors/copied text/polarity/action state;
- census emitted with synthesis;
- both runs must pass all blocking dimensions;
- burden compared with A→B.

The census-to-synthesis contract is the right test: it preserves A’s useful coverage function without
recreating A’s semantic machinery.

## A closure proposal

**DO NOT ACCEPT A CLOSURE YET.**

The proposed pre-B coverage/action validator is a separate runtime stage. The B-internal census is the
smaller test of the same function.

Order:

1. Run COV1/COV2.
2. If both pass, retire old A and do not build a pre-B validator.
3. If the census itself fails repeatedly, build the minimal pre-B coverage/action validator.
4. Do not close A based on the proposal alone.

If the pre-B validator is built later, keep it read-only over record IDs:
- no selectors;
- no copied text;
- no rewriting;
- no reconciliation/problem/section decisions.

## One guardrail

The emitted `SOURCE_COVERAGE` must be the exact census used for synthesis. Do not let the model emit a
post-hoc census that differs from what it used.

## Do not

- add C;
- add selectors;
- restore old A semantics;
- add action-state enums;
- accept A closure before the census result.

No acceptance or production change.
