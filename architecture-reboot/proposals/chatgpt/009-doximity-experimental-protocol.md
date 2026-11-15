# ChatGPT proposal 009 — Doximity experimental protocol

## Purpose

Define how to use Doximity runs as high-information experiments rather than one-note demos.

Core principle:

> Each fresh Doximity conversation should maximize the number of predefined assertions tested while preserving case isolation, first-divergence localization, and reproducibility validity.

The signer owns the clinical reference baseline.

---

# 1. Three testing units

## Case
One independent synthetic/de-identified clinical source package.

## Batch
A fixed collection of cases submitted in one Doximity conversation.

Recommended engineering target:
- start small;
- then use approximately 8-12 cases per batch if output completeness remains reliable;
- ten cases is a reasonable default target, not a fixed limit.

## Repetition
The same exact frozen batch/package executed in a fresh Doximity conversation.

Important:

> Ten cases in one conversation are ten within-run fixtures, not ten reproducibility repetitions.

Reproducibility requires repeating the same frozen batch in fresh conversations.

Initial default:
- 3 fresh conversations per batch;
- more if a semantic decision remains unstable or failure-rate estimation matters.

---

# 2. Signer-owned reference baseline

Every case needs a frozen reference before testing.

ChatGPT/DeepSeek may prepare a proposed baseline, but the signer owns the clinically meaningful semantic reference.

The baseline should be layered.

## B0 — source truth
Exact input:
- chart material;
- transcript;
- labels;
- ordering.

## B1 — proposition reference
Clinically meaningful propositions that should be discoverable.

Used mainly for I3 recall/fidelity.

## B2 — clinical interpretation reference
Signer-approved:
- neurologic problem(s)/claim(s);
- important duplicate vs distinct decisions;
- modifiers/conditions where material;
- historical attribution vs current adoption;
- must-use / must-not-use decisions where clinically meaningful.

## B3 — note-structure reference
Expected:
- problem use/reuse;
- required/forbidden section use;
- required render-unit relationships;
- standing items;
- clinically meaningful ordering constraints.

## B4 — render reference
Only where exact/bounded wording matters:
- operator;
- required payload;
- exact or bounded realization.

Do not make free-language prose gold unless wording itself is being tested.

Changing a frozen baseline is an ACCEPTANCE CHANGE.

---

# 3. Baseline creation

For each reference case:

1. One LLM drafts the reference packet from the source.
2. The other LLM critiques it independently.
3. The signer adjudicates clinically meaningful disagreements.
4. Freeze the reference.
5. Mechanical fields do not require signer micromanagement.

Signer attention should focus on:
- claim/problem definition;
- duplicate vs distinct;
- adoption;
- clinical relevance;
- note-use decisions;
- clinically meaningful ordering/style choices.

---

# 4. Test mode exposes checkpoints

Do not judge only the final note.

Each test case should expose enough structured output to localize the earliest failure.

Conceptually:

```text
CASE_ID

I1_SOURCE_MAP
I2_SPANS
I3_OBJECTS
I4_ANNOTATIONS

S1_PROBLEMS
S2_ADJUDICATION
S3_USE_MAP
S4_BLUEPRINT

R1_UNITS
R2_SECTIONS
R3_FINAL_NOTE
```

Exact schema remains downstream.

Experimental invariant:

> Every scored decision must be observable at the earliest artifact that owns it.

---

# 5. First-divergence localization

Every failed assertion is assigned to the earliest checkpoint that differs from the frozen reference.

Example: "no prior seizures" missing from final note.

- absent from I3 -> I3 failure;
- present I3, omitted S3 -> S3 failure;
- retained S3, no S4 unit -> S4 failure;
- unit exists, R1 line missing -> R1 failure;
- R1 present, R2 drops -> R2 failure;
- completed section exists, R3 omits -> R3 failure.

This is the primary isolation method.

Do not diagnose from final prose alone.

---

# 6. Batch design: coverage matrix, not random notes

A 10-case engineering batch should intentionally cover distinct failure surfaces.

Illustrative set:

| Case | Primary stressors |
|---|---|
| C01 | simple clean neurologic happy path |
| C02 | duplicate facts across transcript + prior note |
| C03 | historical diagnosis vs current adoption |
| C04 | conditional management / hold-resume / if-unless |
| C05 | multiple neurologic problems with shared evidence |
| C06 | non-neurologic fact supporting a neurologic claim |
| C07 | source-date vs event-date / provenance trap |
| C08 | uncertainty / competing diagnosis / incomplete conversational reasoning |
| C09 | standing-item trigger / zero-member unit |
| C10 | prose-heavy HPI + chronology + negatives + A/P voice |

One case may test many assertions.

Historical regression cases should be represented preferentially.

---

# 7. Assertions are the primary score

A batch is scored by predefined assertions, not by "notes that look good."

Each assertion contains:

- CASE_ID
- ASSERTION_ID
- owner submodule
- expected property
- validation mode:
  - MECHANICAL
  - SEMANTIC_AUDIT
  - HYBRID
- severity:
  - CRITICAL
  - MATERIAL
  - COSMETIC
- result:
  - PASS
  - FAIL
  - UNRESOLVED

Example:

```text
C03.A01 source family = PRIOR_NEUROLOGY
C03.A02 "probable vascular dementia" proposition present
C03.A03 attribution retained
C03.A04 current adoption = FALSE unless current clinician adopts
C03.A05 not rendered as today's plan
```

One Doximity run can therefore test hundreds of properties.

---

# 8. Severity-aware acceptance

Do not collapse everything into one pass percentage.

## CRITICAL
Examples:
- fabricated clinical fact;
- dropped current plan item;
- prior recommendation promoted to current plan;
- cross-case contamination;
- unsafe semantic inversion;
- malformed structure silently repaired.

Any CRITICAL failure fails the batch.

## MATERIAL
Examples:
- wrong problem ownership;
- duplicate bullet;
- wrong section;
- missing relevant evidence;
- wrong operator while meaning mostly preserved.

Tracked separately.

## COSMETIC
Examples:
- allowed punctuation;
- allowed abbreviation variation.

Not allowed to mask material failures.

---

# 9. End-to-end batch, single-owner assertions

A batch may test the whole system in one call.

But every assertion has one earliest owner.

This allows one run to test:
- I1 provenance;
- I3 extraction;
- S1 grouping;
- S2 semantic relations;
- S3 relevance;
- S4 unit compilation;
- R1 rendering;
- R2 prose preservation;
- R3 assembly.

We should not require separate Doximity calls for every submodule if a structured end-to-end batch can expose the intermediate states.

---

# 10. Deliberate invalid probes

When useful, include isolated invalid IR-level probes in the same experimental package, clearly marked as test cases.

Examples:
- missing operator field;
- invalid COVERED relation;
- duplicate ORDER;
- zero-member non-standing unit.

These test fail-closed behavior.

Do not hide invalid probes inside realistic cases.

---

# 11. Fresh-run protocol

For a frozen batch/package:

1. Run 1 in fresh Doximity conversation.
2. Commit raw output unchanged.
3. Run 2 fresh, exact same input/package.
4. Commit raw output.
5. Run 3 fresh, exact same input/package.
6. No prompt/package/baseline changes between repetitions.
7. Diff checkpoint-by-checkpoint.

Interpretation:

### Stable + correct
Candidate for acceptance.

### Stable + wrong
Representation/contract/baseline defect; not stochasticity.

### Semantic disagreement across runs
Reproducibility failure at earliest varying checkpoint.

### Identical S4 but wording drift
Renderer-freedom issue; decide whether wording difference matters.

---

# 12. Cross-case contamination test

Batching introduces a new failure surface: one case may affect another.

After a primary batch passes:

## Order perturbation
Re-run same cases with a predetermined different order:
- reverse;
- rotate;
- fixed permutation.

Case content stays identical.

Compare each CASE_ID against:
- baseline;
- original batch output.

For high-risk cases, also run case alone once.

If results depend materially on neighboring cases/order, batching is causing context leakage.

---

# 13. Position-effect test

Rotate the same case through early, middle, and late positions.

Look for:
- truncation;
- instruction decay;
- late schema failure;
- poorer semantic fidelity later in the batch.

This determines practical batch-size limits.

Do not assume ten cases are safe merely because Doximity accepts the input.

---

# 14. Batch-size escalation

Recommended sequence:

## Bootstrap
2-3 tiny cases.

## Engineering batch
8-12 realistic cases.

## Stress batch
Larger only after completeness and position stability are demonstrated.

Batch size is an experimental variable.

If later cases degrade, reduce batch size or change packaging; do not reinterpret those errors as module failures until position effects are separated.

---

# 15. Paired A/B contract testing

For one implementation change:

## A
old frozen implementation.

## B
new candidate implementation.

Keep constant:
- cases;
- case order;
- baseline;
- Doximity mode;
- scoring.

Run in separate fresh conversations.

Compare assertion-level deltas, including unrelated assertions.

This is how to detect non-local prompt sensitivity.

A targeted fix is rejected if it improves its target but causes unacceptable regression elsewhere.

---

# 16. Minimal-change rule

Where feasible, change one implementation variable per experiment.

Do not simultaneously change:
- fixture;
- baseline;
- schema;
- prompt rule;
- operator;
- scoring rule.

If multiple changes are unavoidable, list them explicitly and avoid narrow causal claims.

---

# 17. Layered metrics

Report separately.

## INGEST
- source recognition;
- span coverage;
- proposition recall;
- fabrication/precision;
- annotation correctness.

## STRUCTURE
- problem-model agreement;
- semantic-relation agreement;
- adoption agreement;
- content-use agreement;
- unit/operator/order agreement;
- completeness.

## RENDER
- unit-to-line conformance;
- payload preservation;
- voice/style;
- section preservation;
- assembly completeness.

## REPRODUCIBILITY
Across fresh runs:
- object-set agreement;
- problem agreement;
- relation agreement;
- use-map agreement;
- unit/operator agreement;
- final structural agreement.

Do not produce one global "accuracy" number.

---

# 18. Semantic disagreement protocol

When Doximity differs from the frozen semantic baseline:

1. Hide Doximity's answer from the re-reviewer where feasible.
2. Re-review source + baseline.
3. Classify:
   - baseline clearly correct;
   - Doximity clearly correct / baseline wrong;
   - genuinely ambiguous.
4. Baseline wrong:
   - ACCEPTANCE CHANGE;
   - document reason;
   - update reference;
   - rerun affected regression set.
5. Ambiguous:
   - mark UNRESOLVED;
   - do not count as proof of pass/fail;
   - clarify contract if material.
6. Baseline correct:
   - localize earliest divergence;
   - file implementation defect.

The baseline is authoritative during a frozen experiment, but not infallible.

---

# 19. Signer reference corpus

The signer should curate a durable corpus rather than continuously inventing isolated cases.

Recommended initial target:
- approximately 10-15 representative neurology cases.

Coverage should include, over time:
- seizure;
- stroke/TIA;
- encephalopathy/AMS;
- weakness/localization;
- neuropathy;
- headache;
- movement disorder;
- cognition;
- inflammatory/demyelinating;
- neuromuscular;
- complex multi-problem consultation.

Each should contain enough transcript/chart history to stress provenance and temporal reasoning.

These become the main semantic regression benchmark.

Micro-fixtures remain useful for isolated structural/operator invariants.

---

# 20. Baseline should not over-specify prose

For realistic cases, freeze primarily:
- propositions;
- claims/problems;
- semantic relationships/adoption;
- use/omission;
- section/problem ownership;
- unit/operator structure;
- mandatory/forbidden content;
- voice/style invariants.

Freeze exact prose only when:
- canonical operator wording is under test;
- wording changes clinical meaning;
- signer wants canonical style.

Do not reward imitation of a gold paragraph instead of clinical fidelity.

---

# 21. Experimental artifact package

Each batch should preserve something conceptually like:

```text
experiment/
  MANIFEST.md
  INPUT_BATCH.txt
  BASELINE/
  PACKAGE/
  RAW/
    run_01.txt
    run_02.txt
    run_03.txt
  SCORES/
    mechanical
    chatgpt_blind
    deepseek_blind
  DIFF/
    first_divergence
    reproducibility
  VERDICT.md
```

Raw outputs are immutable.

Hand-corrected outputs are separate and never labelled generated.

---

# 22. Efficient-test objective

A good Doximity experiment maximizes:

> independent predefined assertions observed per fresh conversation

subject to:

> case isolation + output completeness + first-divergence localization + reproducibility validity.

Therefore:
- one-note-per-run is usually too low-information;
- one huge unconstrained batch is too hard to localize and may introduce context/position effects;
- structured multi-case batches are the preferred middle ground.

---

# 23. Acceptance is hierarchical

A batch can fail at different levels:

1. **Execution integrity**
   - all cases returned;
   - schema parseable;
   - no truncation/cross-case leakage.

2. **Mechanical conformance**
   - IDs/accounting/type/order/completeness.

3. **Semantic fidelity**
   - baseline clinical assertions.

4. **Reproducibility**
   - same frozen input/package across fresh runs.

5. **Robustness**
   - order perturbation / position tests.

Do not evaluate higher layers if a lower layer is invalid enough to contaminate them.

---

# 24. Proposed practical cycle

For each major implementation milestone:

### Development batch
- 8-12 cases;
- many assertions;
- 1 run for debugging only.

### Acceptance batch
- freeze package;
- freeze baseline;
- 3 fresh runs;
- no edits between runs;
- blind scoring where feasible.

### Robustness batch
- one predetermined case-order permutation;
- selected single-case controls;
- only after acceptance batch passes.

### Regression after change
- paired A/B on same frozen corpus;
- then full relevant regression if target improves.

This gives high information per signer-run conversation while preserving causal interpretability.
