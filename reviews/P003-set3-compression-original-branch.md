# Doximity set 3 review — original architecture branch

## Test metadata

Set 3 occurred after the signer explicitly stated that all prior Doximity runs had used **Thinking** and that subsequent runs would use **Instant**.

Record:
- Set 1: Thinking
- Set 2: Thinking
- Set 3: Instant

Therefore set 3 is not directly comparable to set 2 as a single-variable experiment: both the Handoff and model mode changed. It is still a valid within-set reproducibility test because all three set-3 runs used the same package and mode.

## Verdict

**P003 Doximity runtime remains FAIL for reproducibility, but the failure class is now much narrower.**

### What set 3 successfully establishes

Using `handoff_v2.txt`:

- O54 residual aphasia stays absent in all three outputs. D-014 is successfully enforced upstream by absence.
- `Seizure precautions` appears in all three. The standing-item packaging correction works.
- O52 `no further workup` stays out of all three outputs.
- O2 `admitted 11/12` stays out of all three outputs.
- seizure duration, postictal duration, sodium trend, etiologic reasoning placement, and ASM conditionality are stable.

This is meaningful improvement.

## Remaining failure: semantic compression / grouping

The remaining instability is concentrated in decisions that require recognizing that multiple Handoff objects belong to one rendered proposition or one rendered decision.

Examples:

- infarct fact: O7/O8/O53 can become one bullet, two bullets, or be combined with O18;
- CT facts: O17/O44/O19 can be merged/split differently;
- memory concern: O32/O34 render redundantly;
- MRI hedge: O23/O39 are semantically overlapping but lexically different;
- apixaban hold/resume: O12/O25 are one conditional management decision but split in runs 1–2 and merged in run 3.

This is not primarily a formatting problem anymore. It is a **grouping/compression representation problem**.

## Important correction to DeepSeek's checker claim

The current/tightened P005 checker would **not** catch every duplicate shown in set 3.

After the review-required narrowing:

- exact duplicate detection can catch exact/normalized repeats;
- a strict prefix/subset rule may catch the family-concern pair;
- it will **not reliably catch**:
  - `CT head no hemorrhage` vs `CT head no acute abnormality`;
  - O23 `but the MRI will tell us` vs O39 `we'll see what the MRI shows`;
  - `known left MCA infarct` vs `left MCA infarct [prior neurology]` when provenance/timing differ;
  - apixaban hold + resume as one composed conditional decision.

Those require semantic equivalence or composition, which P005 deliberately excludes.

Therefore P005 is useful as a fail-only guard, but **it cannot solve the dominant set-3 instability by itself**.

## Architectural implication

The remaining grouping decisions should move upstream rather than be repeatedly rediscovered by `05`.

Recommended next proposal:

### Explicit render/compression groups

Keep every O# losslessly, but add A/P assembly metadata that says which retained objects are intended to render together.

Conceptually:

- `RENDER_GROUP` — multiple objects express one factual proposition; render once.
- `COMPOSE_GROUP` — multiple objects are distinct pieces of one clinical decision and should render as one line when compatible.
- each group preserves every member O# and provenance;
- one object can remain ungrouped;
- grouping must be source-faithful and decided upstream, not inferred by `05`;
- `05` receives groups and formats them, rather than deciding semantic equivalence from scratch.

Frozen-case examples:
- O7 + O8 + O53 = one chronic infarct fact/timing group;
- O17 + O44 (+ O19 only if the grouping adjudication says it belongs) = one CT/result group;
- O32 + O34 = one memory-concern group;
- O23 + O39 = one reasoning-equivalence group;
- O12 + O25 = one composed apixaban hold/resume decision.

The precise grouping stage should be proposed rather than patched ad hoc. Likely homes are `03_SELECT_ORGANIZE` or a deterministic assembly layer immediately after it; do not make `05` carry more prose rules.

## P005

Proceed with the revised fail-only checker, but describe its purpose accurately:

> P005 catches mechanically detectable contract breaches. It does not resolve semantic compression instability.

Do not use P005 PASS as evidence that the A/P is reproducible.

## Next sequence

1. Record set-3 mode as Instant and prior sets as Thinking.
2. Revise P005 per the prior review and implement only after review/approval.
3. Write a separate proposal for explicit upstream render/compression groups.
4. Do not add more semantic duplicate prose to `05` yet.
5. After grouping is represented upstream, run another canonical three-run Instant set.

No signer-level decision is required at this point.
