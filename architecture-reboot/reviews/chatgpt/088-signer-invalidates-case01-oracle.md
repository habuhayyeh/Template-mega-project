# ChatGPT review 088 — signer evidence invalidates CASE-01 clinical oracle

## Classification

**CONTRACT / ORACLE**, not architecture.

## Trigger

During blinded Option-F signer review of packet 7, the signer judged:

> prior left MCA infarct is a major primary neurologic problem and should retain its own separate A/P
> problem even when inactive; because it is inactive, its block should be shorter/condensed.

The packet therefore received `S1-CAND-01 = SILENT`: adding the infarct as a separate S1 candidate is
not a candidacy violation.

## Conflict found

The current CASE-01 oracle and predicate notes encode the opposite policy:

- `expected.candidate_concepts_must_exclude = ["infarct"]`;
- CASE-01 expected outcome says infarct is not rendered as an A/P problem;
- the Gate-0 seed `G0-S1-05` expects the added infarct candidate to fire `S1-CAND-01`.

This means the current calibration fixture would classify the signer's accepted clinical behavior as a
defect.

## Governance

D-023 records the corrected product rule and partially supersedes D-015:

- major established primary neurologic diagnoses may retain their own problem block even when inactive
  and without new management;
- inactivity controls compression, not automatic exclusion;
- current adoption and A/P problem retention are separate decisions.

## Architecture check

No architecture impossibility is established.

The frozen interfaces already separate:

- S1 problem candidacy;
- S2 encounter-level adoption;
- S2 approved representations;
- S3 rendered-problem selection.

Therefore the desired state is representable in principle: a remote infarct can remain a problem
candidate and rendered problem while the historical source object is not treated as a newly/currently
adopted assertion.

Do **not** reopen S1/S2/S3 architecture unless implementation of this corrected contract proves that
distinction impossible.

## Required controlled rebuild

1. Rebuild CASE-01 clean truth so the old left MCA infarct is a legitimate separate neurologic problem.
2. Preserve the signer's Packet-2 distinction unless the rebuilt representation proves it internally
   inconsistent: historical infarct may remain not-currently-adopted while still retained as a
   condensed problem.
3. Update clean S1/S2/S3/S4 parents consistently; do not patch only the S1 seed.
4. Replace the current `S1-CAND-01` bad seed with a genuinely invalid candidate under D-023.
5. Ensure the inactive infarct's downstream blueprint can represent a shorter/condensed problem without
   stealing authority from RENDER; if the existing schema cannot express the needed render depth,
   classify that as a CONTRACT issue and propose the smallest addition.
6. Regenerate all generated artifacts through the generator; do not hand-edit generated files.
7. Rerun preflight and packets mode only.
8. Treat current signer references as pre-D-023 evidence. Reuse only if the harness proves packet
   identity is unchanged; otherwise collect new references under Option F.

## Current Gate-0 consequence

Gate 0 must **not** be run against the current CASE-01 package. Packet 7 demonstrates that its answer
key conflicts with signer clinical policy.

## NEXT

DeepSeek performs the controlled CASE-01 source-contract rebuild under D-023, runs preflight, regenerates
the blinded packet index, and hands the exact diff/results back to ChatGPT for review.

No acceptance run. No Doximity. No Phase 0.
