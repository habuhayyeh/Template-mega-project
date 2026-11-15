# Proposal 014 — blinded semantic packets

**Status:** ACCEPTED under D-029 and implemented in `REVIEW-POLICY-F-2`. Review 089 found the leak; the
correction is in the harness, predicate wording and tests.

## Problem

`gate0_harness.build_packet()` exposes semantic expected answers:

- `S1-CAND-01` includes `oracle.expected.candidate_concepts_must_exclude`;
- `S2-ADOPT-01` includes `oracle.expected.adoption` and tells the judge to compare against it.

That makes the signer reference and LLM evaluators partly copy an answer key. A wrong oracle can
calibrate perfectly against itself. Packet 7 already exposed this risk.

## Smallest governed correction

### 1. Packet payload

For every semantic packet, `oracle.expected` is omitted entirely. Keep only:

- `oracle.objects` — source text, provenance, temporal/status;
- `oracle.spans` — source text and attribution;
- `oracle.matching` — concept-identity rule;
- target artifact;
- minimum allowed dependency context;
- predicate assertion and plain-language instructions.

The full oracle remains internal to mechanical scoring and build validation. It is never in a
signer/evaluator packet.

### 2. Predicate wording

`S2-ADOPT-01` becomes:

> every S2 adoption verdict is supported by the supplied source/context for the current encounter;
> historical or medication-only material does not establish current adoption.

The signer reference is the accepted semantic truth for calibration. The evaluator compares to that
reference, not to a visible oracle label.

`S1-CAND-01` keeps its current assertion:

> every candidate names a neurologic subject for which the encounter poses its own assessment question.

No `candidate_concepts_must_exclude` list is shown; the judge derives invalid candidacy from the source
and rule.

### 3. Harness and tests

- `build_packet`: use `_subset_oracle(oracle, [])` for all three semantic predicates;
- rewrite the two instructions that mention oracle expected answers;
- replace leakage-asserting tests with absence tests:
  - packet has no `expected` key;
  - no `candidate_concepts_must_exclude`;
  - no `expected.adoption`;
- all semantic packet IDs change; existing references are invalid.

### 4. Policy version

Bump `REVIEW-POLICY-F-1` to `REVIEW-POLICY-F-2` so old references cannot be accepted after the packet
change.

## Files

- `architecture-reboot/tools/gate0_harness.py`
- `architecture-reboot/experiments/architecture/AX-S1S2-D/predicates.md`
- `architecture-reboot/tests/test_scorer_more.py`
- `architecture-reboot/scorer/README.md` and `HANDOFF.md` wording
- regenerated `runs/gate0-packets-c2/` packets and index

## Approval needed

This is a contract/interface correction, not an implementation-only patch. After approval, DeepSeek
will implement, regenerate all packets, rerun preflight and packets mode, and restart signer reference
collection from zero.

No acceptance. No Doximity. No Phase 0.
