# DeepSeek review — B problem-threshold patch

**Verdict:** ACCEPT the counterfactual rule, with one fixture/wording correction before the comparator.

## What is right

- Baseline comparator no longer becomes a separate problem.
- Independent established disease and independently evaluated current syndrome remain separate.
- Counterfactual question is the right test.
- Three fixtures cover the main failure modes.

## One correction

The contract still allows a problem on **independent disease identity alone**:

> independent neurologic clinical identity **or** its own current assessment question/status.

That can turn every historical neurologic disease into a BACKGROUND problem. It conflicts with the
encounter-level problem rule and can recreate a diagnosis list.

Add encounter relevance to the identity branch:

> An established neurologic disease may become a BACKGROUND problem only when it is relevant to this
> encounter’s neurologic interpretation or management. If it is only historical context, keep it in
> A/C history, not B.

### Fixture 2

Fixture 2 should say why the prior stroke is encounter-relevant, e.g.:

- residual hemiparesis changes interpretation of the current deficit; or
- current management depends on the prior stroke.

Do not justify a BACKGROUND problem merely because the chart carries the stroke as history.

Fixture 1 and Fixture 3 are fine.

## Comparator

After that correction, build the A→B vs Scribe→B-direct comparator.

B-direct must:

- cite exact Scribe record IDs/selectors itself;
- preserve source-qualified wording;
- preserve action splitting;
- no action-state enums;
- same problem threshold;
- same output shape as B.

Score coverage, provenance, actions, problem architecture, hidden errors, concision. Do not compare prose
style.

No C until B output is decision-complete.

No new stage, enum or validator. No acceptance or production change.
