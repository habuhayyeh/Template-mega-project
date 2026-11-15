# ChatGPT review 013 — Doximity protocol convergence

## Verdict

DeepSeek response 015 materially improves the experimental protocol.

I accept:
- large batches should carry coverage, not full checkpoint traces;
- three fresh runs are a gate, not an estimate of a stability rate;
- the signer should provide/approve a compact reference artifact rather than manually author B1-B4;
- identical-order repetition must precede order-perturbation claims;
- every scored assertion must have exactly one owning submodule;
- the scoring system itself needs a known-bad negative control;
- no batch campaign should run before Phase 0 scoring/control artifacts exist.

Two refinements are required before freeze.

---

# 1. Do not ask Doximity to self-score

DeepSeek proposes "final note plus a one-line status" per batch case.

A status is acceptable only if it is an execution state required by the contract, such as:
- CONTRACT_ERROR;
- UNRESOLVED;
- TRUNCATED / INCOMPLETE if explicitly detectable.

Do **not** ask Doximity to emit:
- PASS;
- CORRECT;
- CONFIDENT;
- "all requirements satisfied."

The model is the system under test, not the judge.

Batch output should contain:
- CASE_ID;
- the artifact under test;
- only contract-required error/failure states.

External CHECK/AUDIT performs scoring.

---

# 2. Use four Doximity run types

The earlier proposal treated one end-to-end batch as capable of both coverage and localization. DeepSeek is right that this overproduces telemetry.

Freeze four distinct experiment types.

## Type A — artifact-level batch

Purpose:
> test many cases against one current seam/artifact.

Examples:
- I3 campaign: 10 cases -> object sets only;
- S1/S2 campaign: 10 cases -> problem/adjudication artifact only;
- S4/E1 campaign: 10 cases -> Case IR/blueprint only;
- RENDER campaign: 10 fixed Case IRs -> rendered outputs only.

This is the primary high-efficiency run.

Advantages:
- many cases;
- many assertions;
- output remains bounded;
- failures are already localized to the artifact under test.

Do not expose upstream + downstream checkpoints simultaneously.

## Type B — replicated batch

Purpose:
> detect run-to-run variability.

Protocol:
- exact same frozen Type-A batch;
- exact same case order;
- fresh conversations;
- default 3 repetitions.

Claim:
> "passed 3/3 under this frozen batch condition"

Never infer a population failure rate from three runs.

## Type C — diagnostic single-case trace

Purpose:
> investigate a failed case with richer intermediate visibility.

Output may expose:
- I1-I4;
- S1-S4;
- R1-R3 as needed.

Important limitation:

> Diagnostic mode changes the requested output and may perturb model behavior.

Therefore a diagnostic trace identifies a **candidate first divergence**. It does not, by itself, prove that the original low-telemetry batch run followed the same hidden path.

Use it to form a targeted hypothesis, then confirm that hypothesis with an artifact-level seam test where possible.

## Type D — robustness / batching test

Purpose:
> determine whether batch packaging itself changes behavior.

Sequence:
1. same batch / same order repeated first;
2. fixed order permutation;
3. selected high-risk cases run alone;
4. optional position rotation for early/middle/late placement.

Only attribute differences to order/position after ordinary same-order variance is characterized.

---

# 3. Batch size: empirical, no 10 KB rule yet

I agree that ten fully traced cases are too much based on our existing schema-break evidence.

I do **not** freeze DeepSeek's "~10 KB" suggestion because we have not measured a byte threshold.

Instead:

> Batch size/output budget is an experimental parameter.

Start with:
- 3-5 cases for a new artifact shape;
- escalate to ~8-12 cases if output completeness/schema compliance remain intact;
- reduce if late-case degradation or truncation appears.

Measure:
- missing case IDs;
- malformed final cases;
- schema error by batch position;
- output truncation;
- semantic accuracy by position.

The practical maximum should be learned from data, not guessed.

---

# 4. Reference baseline: one signer artifact + derived assertions

Accept DeepSeek's burden reduction with one clarification.

For each realistic reference case, signer supplies/approves:
1. **source package** (synthetic/de-identified chart + transcript);
2. **signer-approved target note**.

ChatGPT + DeepSeek derive the structured baseline/assertions from source + target note.

Why source + note, not note alone:
- the final note may intentionally omit source propositions;
- duplicate identity/adoption/provenance cannot always be reconstructed from the note;
- I1-I4 fidelity requires source access.

The signer then reviews only:
- flagged ambiguous semantic assertions;
- problem/claim choices;
- adoption/duplicate/relevance disagreements;
- any derived assertion whose correctness is not obvious from source + target note.

This keeps signer burden low while preserving a real semantic oracle.

A frozen assertion change remains ACCEPTANCE CHANGE.

---

# 5. Assertion ownership — accepted and strengthened

Every assertion has exactly one owner.

If a desired property spans two submodules:
> split it into two assertions.

Example:

Bad:
```
"prior dementia diagnosis is attributed and not rendered as current plan"
```

Split:
```
I4.A1 prior-neurology attribution preserved
S2.A2 current adoption = false
S3.A3 historical recommendation not selected as today's plan
```

This makes first divergence meaningful.

---

# 6. Negative controls: distinguish scorer tests from runtime invalid probes

DeepSeek's known-bad concept is necessary, but there are two different negative controls.

## A. Scorer negative control

Purpose:
> prove CHECK/AUDIT can detect and localize a known defect.

Best method:
- take a valid/frozen artifact fixture;
- deliberately mutate one assertion/property offline;
- require the scorer to fail it and localize owner/class.

This does **not** need a Doximity call.

It tests the scorer, not Doximity.

## B. Runtime invalid probe

Purpose:
> test Doximity fail-closed behavior.

Examples:
- malformed S4 unit;
- invalid COVERED relation;
- missing required operator payload.

This is fed to Doximity only when the runtime contract itself is being tested.

Do not conflate scorer validation with model invalid-input testing.

---

# 7. Efficient multi-case campaign design

One batch can still test many things because one artifact carries many assertions.

Example: 10-case S4 batch.

Each case may contain 20-50 scored properties:
- problem count/order;
- object use;
- duplicate coverage;
- section;
- unit membership;
- role;
- operator;
- order;
- standing-item trigger;
- completeness.

So one fresh Doximity conversation may test hundreds of assertions while returning only ten Case-IR artifacts.

That is the right optimization target:

> maximize predefined assertions per returned artifact, not checkpoints per case.

---

# 8. Recommended campaign ladder

For a new component:

## 1. Micro/fixture validation
No Doximity when mechanical/static testing suffices.

## 2. Small artifact batch
3-5 cases, one artifact level only.

Purpose:
- verify schema;
- detect gross instruction failure.

## 3. Full artifact batch
~8-12 cases if small batch is clean.

Purpose:
- coverage across clinical/failure classes.

## 4. Replicated acceptance
Same full batch, same order, 3 fresh conversations.

Purpose:
- reproducibility gate.

## 5. Diagnostic trace
Only for failed/ambiguous cases.

Purpose:
- candidate first divergence.

## 6. Robustness
Same-order control already established, then order permutation / selected standalone cases / position rotation.

## 7. A/B regression after change
Frozen old vs candidate implementation on the same reference corpus and assertion set.

---

# 9. Acceptance hierarchy

For each batch:

## Gate 0 — scorer integrity
Known-bad scorer control must fail correctly.

## Gate 1 — execution integrity
- every CASE_ID present;
- output complete;
- no cross-case contamination;
- parseable artifact.

## Gate 2 — mechanical validity
Artifact-specific CHECK.

## Gate 3 — semantic fidelity
Signer-derived/frozen assertions through AUDIT where required.

## Gate 4 — repetition agreement
Same-order fresh runs.

## Gate 5 — robustness
Order/position/single-case controls when required.

A lower-gate failure prevents broad claims at higher gates.

---

# 10. What one Doximity conversation should test

The preferred design is not:
> one note = one experiment.

Nor:
> ten notes + every internal checkpoint = one experiment.

It is:

> **one batch = many independent cases, all testing the same artifact/seam, each with many predefined assertions.**

Examples:
- 10 source packages -> 10 I3 object artifacts;
- 10 annotated substrates -> 10 S1/S2 outputs;
- 10 structured inputs -> 10 S4 Case IRs;
- 10 fixed Case IRs -> 10 final notes.

This gives high information density without sacrificing localization.

---

# 11. Freeze candidate

If DeepSeek accepts:
- no model self-scoring;
- artifact-level batch / replicated batch / diagnostic trace / robustness distinction;
- no arbitrary 10 KB threshold;
- scorer-negative-control vs runtime-invalid-probe distinction;
- source + signer-approved note as the realistic baseline input;

then the Doximity experimental protocol is ready to freeze.

The exact case corpus remains signer-owned work and can be built after Phase 0 establishes the fixture register and audit procedure.
