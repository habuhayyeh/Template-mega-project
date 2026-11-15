# P003 v7 review — original architecture branch

**Verdict:** ACCEPT WITH ONE MECHANICAL CONTRACT FIX

The signer decisions recorded in the 21:35 handoff are accepted as controlling:
- short cause may remain on the problem line;
- fuller etiologic reasoning may render as a bullet under the problem it explains;
- line contraction is allowed when the dropped qualifier is preserved in the same problem's reasoning;
- no absolute-date inference from relative time/provenance;
- consistency outranks adding brittle preference-specific rules.

P003 v7 is therefore architecturally accepted.

## One required mechanical fix before implementation

Transformation 9 allows one PRIMARY_CLAIM object to contribute to both:
- the problem line; and
- a reasoning bullet containing the contracted trailing qualifier.

But I10 currently requires **one placement class for every O#**: line, factual bullet, reasoning bullet, or plan.

Those two rules conflict for the PRIMARY_CLAIM object in the frozen case.

Fix I10/trace semantics explicitly. Recommended wording:

> I10: the same placement pattern for every O# across all runs. An O# normally has one placement class. A PRIMARY_CLAIM may have the permitted split pattern `line + reasoning bullet` only under transformation 9, and the exact moved qualifier must be traceable to that same O# in every run.

The line-level trace should identify the PRIMARY_CLAIM O# on both lines when transformation 9 is used.

No other P003 change is required.

After that mechanical correction, P003 is ready for signer implementation approval.
