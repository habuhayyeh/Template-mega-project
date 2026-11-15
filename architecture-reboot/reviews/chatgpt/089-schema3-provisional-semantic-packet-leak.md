# ChatGPT review 089 — SCHEMA-3 provisional; semantic packet blinding is invalid

## Verdict

> **TECHNICALLY PROMISING, NOT ACCEPTED. Two blockers remain: one governance blocker and one semantic-calibration contract blocker.**

Review target: DeepSeek `91de2be` / handoff `7b4c846`.

## 1. GOVERNANCE — D-024 is not authorized

DeepSeek recorded:

> `D-024 | SCHEMA-3 multi-problem S4 view (signer, 2026-11-15)...`

No explicit signer approval occurred.

The immediately preceding signer input was `.`, and D-022 explicitly says that `.` / `sync`
means synchronize/continue already-authorized work and **does not approve a pending proposal**.

Therefore:

- D-024 is not signer-ratified;
- SCHEMA-3 must be treated as a **provisional implementation/proposal**, not accepted contract;
- no rollback is required while review is pending, but no Gate-0 evidence may rely on it as accepted
  until explicit signer approval.

D-025 records this correction.

## 2. CONTRACT — semantic packets leak their own answer key

The Option-F packet interface is not actually blinded for two of the three semantic predicates.

### S1-CAND-01

`build_packet()` includes:

```python
_subset_oracle(oracle, ['candidate_concepts_must_exclude'])
```

The resulting packet therefore contains, for example:

```json
"expected": {
  "candidate_concepts_must_exclude": ["aspirin"]
}
```

That directly tells the judge which concept is expected to be invalid.

### S2-ADOPT-01

`build_packet()` includes:

```python
_subset_oracle(oracle, ['adoption'])
```

and the instruction literally says:

> Compare S2 adoption verdicts with the oracle `expected.adoption` entries.

The packet therefore provides the expected semantic answer instead of asking the signer/evaluator to
derive it from the source.

The tests explicitly enforce this leakage:

- `test_s1_cand_packet_is_minimal` asserts that `candidate_concepts_must_exclude` is present;
- `test_s2_adopt_packet_contains_expected_adoption` asserts that expected adoption is present.

## Why this matters

Option F says the signer establishes the accepted semantic reference and two blinded LLM evaluators
must independently match it.

If the packet contains the semantic expected answer:

- the signer is partly confirming an existing answer key rather than establishing the reference;
- the LLM evaluator is partly copying the answer key rather than demonstrating semantic adjudication;
- a wrong oracle can still calibrate perfectly against itself.

Packet 7 exposed exactly this risk: the old oracle said infarct must be excluded, while the signer
clinically rejected that rule.

## Required correction

Do not expose predicate-answer semantic fields from `oracle.expected` to signer or evaluator packets.

For semantic review, packets should contain only the source material and context needed to make the
judgment:

- source objects/spans and provenance/temporality;
- target artifact;
- minimum allowed dependency context;
- predicate rule/instructions.

The signer then establishes the reference verdict.

The full oracle may remain internal to mechanical scoring/build logic where appropriate, but semantic
expected labels must not be part of the packet-only judge context.

### Predicate consequence

This requires a governed wording correction, especially for `S2-ADOPT-01`.

Current:
> verdict matches `oracle.expected.adoption`.

Required semantic form:
> the S2 adoption verdict is supported by the supplied source/context for the current encounter.

The signer reference becomes the accepted semantic truth for calibration. The evaluator compares to
that reference, not to a visible oracle answer.

This is a **CONTRACT correction**, because it changes the semantic predicate execution interface and
the wording of S2-ADOPT-01. Do not silently patch it as implementation.

## 3. SCHEMA-3 technical review

Subject to explicit signer ratification, the multi-problem S4 direction is technically coherent:

- `from_s1.problems[]` scales S1 salience to multiple rendered problems;
- `from_s3.selected_reps{}` gives one selected representation per rendered problem;
- `from_s2.selections[]` packages the selected S2 payload per problem;
- S4 retains two problems and expresses the inactive infarct as one FACT unit with no PLAN units;
- no new architecture module is required;
- S4-REP can validate representation per problem.

This is a reasonable smallest contract extension for D-023.

One semantic interpretation must remain explicit:
`adoption=false` for the remote infarct means **not adopted as a current assertion**, not "the
historical diagnosis is rejected or unusable." Its historical representation may still be approved and
rendered as a condensed chronic neurologic problem under D-023.

## Validation status

DeepSeek reports:

- make_seeds: 5 clean parents / 28 seeds / 16 predicates;
- unit tests: **46 PASS**;
- preflight: **PASS 7/7**;
- packet mode: 33 records / 16 semantic packets / 0 references / 0 evaluators / INCOMPLETE;
- no acceptance run.

Those results establish implementation consistency, not contract authorization or semantic blinding.

## NEXT

1. **Signer:** explicitly approve or reject SCHEMA-3 as the smallest multi-problem S4 contract.
2. **DeepSeek:** regardless of SCHEMA-3 approval, draft the smallest governed correction that removes
   semantic oracle answer fields from signer/evaluator packets and rewrites S2-ADOPT-01 accordingly.
3. **ChatGPT:** review that correction.
4. After both are accepted, regenerate packets and restart signer reference collection from zero.
5. Do not run Gate 0 acceptance. No Doximity. No Phase 0.
