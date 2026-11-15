# P006 v2 scope escalation — original architecture branch

## Status

**HOLD — signer decision required under D-013.**

DeepSeek now recommends superseding P006 v2 with a broader P007 typed render-plan input. The original architecture review recommends keeping P006 narrow, testing it, and only then adding P007 for residual instability.

This is no longer a mechanical correction. It is an architecture/scope choice with tradeoffs, so it belongs to the signer.

## What is agreed

Both reviewers agree on the direction:

- 05 should make fewer semantic decisions.
- Semantic equivalence/composition should be decided upstream and audited.
- 04 remains lossless.
- The six semantic kinds remain unchanged.
- A post-output checker should validate rather than silently repair.
- The existing audit has provenance/package problems and its set-specific claims cannot be trusted without qualification.

## The actual disagreement

### Option A — keep P006 narrow, then test

P006 handles only the instability directly demonstrated in clean set3:

- duplicate evidence identity;
- duplicate reasoning identity;
- management composition such as hold + resume;
- explicit HEAD/MODIFIER/CONDITION/COVERED roles.

Then rerun Doximity. If COURSE typing, standing-item evaluation, or other decisions still drift, propose P007 with evidence from that run.

Advantages:
- smallest change;
- easier to review and falsify;
- preserves the signer's preference against accumulating unnecessary rules;
- avoids redesigning stable behavior preemptively.

Cost:
- may require another proposal/test cycle if residual ambiguity remains.

### Option B — supersede P006 with broader P007 now

Build one typed pre-05 render plan that also fixes:

- evidence canonicalization/grouping;
- COURSE typing (STATUS/MODIFIER/INDEPENDENT/IGNORE);
- reasoning dedup/render decisions;
- management canonicalization and bucket/problem scope;
- standing-item trigger evaluation;
- render/composition roles.

Advantages:
- clearer final stage boundary;
- potentially removes more semantic judgment from 05 at once;
- less overlapping architecture if we already believe those decisions belong upstream.

Cost:
- larger simultaneous change;
- several components are not currently demonstrated failures in clean set3;
- harder to identify which change fixed or broke behavior;
- risks overfitting architecture to an audit whose package description was wrong.

## Evidence assessment

The cleanest runtime evidence is set3 (Instant, complete package, handoff_v2).

Set3 strongly demonstrates grouping/composition instability.

Set3 does **not** strongly demonstrate:
- standing-item evaluation instability (standing items were stable 3/3);
- major COURSE classification instability (durations/trend were stable);
- broad management bucket instability beyond hold/resume composition.

The external Doximity audit is useful as design commentary, but its package provenance is wrong. It should not be treated as equivalent to a clean independent experiment on set3.

DeepSeek's statement that the audit produced the same boundary "twice from two different run sets" is not established by the current repository record. We have one external audit with incorrect package assumptions plus our own runtime analyses.

## Reviewer recommendation

**Option A: keep P006 narrow, finish the v3 corrections, test it, then decide P007 from residual failures.**

This is not because the broader typed render-plan idea is wrong. It may well be the eventual architecture. The issue is sequencing and evidence: solve the demonstrated defect first, then widen only if the next run proves the remaining boundary still unstable.

## Signer decision requested

Choose one:

- **A — P006 narrow first, test, then P007 if needed** (reviewer recommendation)
- **B — supersede P006 now with one broader P007 typed render-plan stage** (DeepSeek recommendation)

No implementation should proceed until this scope choice is resolved.
