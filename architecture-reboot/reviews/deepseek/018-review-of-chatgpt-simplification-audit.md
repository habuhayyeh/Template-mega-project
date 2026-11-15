# DeepSeek review of ChatGPT audit 101

**Reviewed:** `reviews/chatgpt/101-independent-architecture-simplification-audit.md`
**Status:** review only; no contract/code change.

## Verdict

ChatGPT's audit is a strong **long-range architecture** review. It correctly identifies the biggest
conceptual accumulation: problem identity/containment, source-fidelity relations, and S2/S3 ceremony.
It is weaker on the **current operating pain**: Gate-0 validation surface and packet workload. Several
candidates are too broad or ownership-changing to bundle into the containment fix.

## Strong agreement

1. **Problem identity/containment (candidate 1).** This is the right generalization. D-015/D-023/D-030
   should collapse into identity + encounter role + render depth. The open issue is relevance threshold
   for compact background problems; ChatGPT notes it but does not define it.
2. **Source-fidelity relation rule (candidate 3).** Correct. "Most specific source-supported acting
   entity; do not infer a mediator" replaces the rigid D-030 substitution rule. This is the same
   direction as proposal 016.
3. **Projection/hash brittleness (candidate 10).** The pain is real: wording edits churn hashes and
   packets. But the proposed fix — typed owner outputs instead of field paths — risks silent ownership
   drift. A smaller fix is better:
   - hash only normative machine blocks, not prose;
   - keep exact paths for semantic fields;
   - allow additive non-semantic fields without a new campaign;
   - separate shape/policy/packet identities.
4. **Decision-closure/accounting (candidate 8).** Good mechanical consolidation, provided reasons stay
   typed and semantically distinct.

## Disagreements / cautions

1. **Candidate 2 over-generalizes.** The diagnosis is right: "adoption" invites confusion with problem
   creation. But replacing it with a broad assertion-state model now is larger than needed and would
   invalidate S2-ADOPT packets again. Proposal 016's wording-only clarification is the smaller fix:
   adoption is current-source endorsement of a proposition/object, not block identity. Keep the field
   and name for now.
2. **Candidate 4 moves ownership.** "Default one resolved formulation" sounds economical, but it shifts
   a note-use/product choice from S3 to S2. That is an architecture change, not a cleanup. It needs an
   experiment with explicit criteria; it should not ride along with containment.
3. **Candidate 5 is premature.** `management_reference_spans` is a concrete schema smell, but S4
   ordering is still `PENDING_DEPENDENCY`. Replacing salience before the ordering contract is frozen
   creates another moving part. Do it after the ordering oracle exists.
4. **Candidate 6 is high-risk and belongs in RENDER experiments.** "No new semantic relation" is the
   right invariant, but verifying it mechanically is much harder than an empty lexical allowlist. It
   must be tested against hallucination, not assumed.
5. **Candidate 7 risks losing clinical content.** "Clinically meaningful coverage" is correct in
   principle, but the definition is the whole problem. It needs conservative nonclinical categories and
   an audit trail; not a first-wave simplification.
6. **Candidate 9 is architecture reopening.** Separating identity, multi-link relevance and render home
   is plausible, but it changes ownership and needs its own experiment.

## What ChatGPT's audit misses

The current package's dominant cost is not architecture; it is the **calibration surface**:

- 44 semantic packets for five clinical questions;
- 21 active predicates, including shape and meaning both scored for the same field;
- structural-only seeds requiring gate special cases;
- full-silence across every semantic family, so one question pulls the whole family;
- one seed per predicate, producing plumbing seeds;
- clean-parent overloaded with layer-local fixtures;
- identity churn from prose edits.

ChatGPT's candidate 10 touches only one of these. A simplification plan that starts with architecture
will not reduce the signer workload.

## Recommended joint sequence

1. **Now, no schema change:** approve/amend proposal 016 wording (S1 identity, S2 adoption,
   S2 causation/D-030).
2. **Now, validation surface:** one non-scored validator per field; one semantic predicate per field;
   one packet per artifact/layer; specificity per family; seeds only for clinical distinctions;
   separate shape/policy/packet identities.
3. **Next contract simplification:** merge candidate 1 + 3 into one problem-identity/source-fidelity
   rule; retire D-015/D-023 special-case wording.
4. **Then infrastructure:** candidate 8 decision closure; candidate 10 hash/projection cleanup.
5. **Experiments only:** candidates 4, 5, 6, 7, 9. Do not implement them as part of containment.

## Disagreement summary

- ChatGPT sees architecture accumulation as the main problem; I see calibration/validation accumulation
  as the immediate problem and architecture accumulation as the second layer.
- ChatGPT's 1/3/10 are the strongest overlaps.
- ChatGPT's 2/4/9 should not be bundled into the current fix.
- ChatGPT's audit does not quantify the 44-packet/21-predicate cost, which is the clearest evidence
  that the current rules are overbuilt.

No Gate-0 acceptance. No Doximity. No Phase 0.
