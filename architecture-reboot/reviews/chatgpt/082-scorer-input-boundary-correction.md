# ChatGPT review 082 — scorer-input boundary correction

## Verdict

> **DEEPSEEK IS CORRECT. REVIEW 081'S SCORER-INPUT CLAUSE WAS TOO NARROW. REOPEN THAT CLAUSE ONLY.**
>
> **Adopt: target artifact + read-only dependency context + oracle + frozen predicate/contract rules.**
>
> Do **not** weaken the predicates. Do **not** turn upstream intermediate outputs into oracle truth.

DeepSeek stopped before implementation because the accepted scorer input:

`artifact + oracle + predicate registry/rules`

cannot evaluate several accepted predicates faithfully.

That is a real source-contract contradiction.

The architecture remains closed. The experiment program remains frozen. This is a narrow acceptance/scorer-interface correction.

---

# 1. DeepSeek's four examples are valid

## S3-SEL-01

Predicate:

> every selected representation exists in S2's approved set for that problem.

An S3 artifact contains the selected id, but not the S2 approved set.

Comparing:

`selected_rep == approved_representation`

would weaken the predicate to a proxy.

PASS: contradiction confirmed.

## S4-PROJ-01

Predicate:

> every S4 input field matches its mapped source path and owner.

The S4 artifact contains the projection under test.

It cannot prove its own projection provenance.

The scorer needs the unmutated S1/S2/S3 source outputs from which that projection should have been constructed.

PASS: contradiction confirmed.

## S2-REP-01

The semantic review asks whether the representation's members/relations support the problem's claim.

The S2 output contains a problem id but not the S1 claim-candidate text/partition that defines the assessment subject.

A human can guess from the members, but guessing is not the accepted predicate.

PASS: contradiction confirmed.

## S3-CAND-01

Coverage is:

> exactly one outcome for every S1 problem candidate.

The S3 artifact cannot establish the complete S1 candidate set by itself.

Using oracle expected outcomes as a substitute would turn expected results into upstream execution state.

PASS: contradiction confirmed.

---

# 2. Reject the "put upstream snapshots into the oracle" alternative

Do **not** solve this by extending ORACLE-2.0 with S1/S2/S3 snapshots.

The oracle and upstream execution context have different meanings:

- **oracle** = external/frozen expected or source-grounded truth used by a predicate;
- **dependency context** = the actual read-only upstream outputs that the tested layer consumed.

Putting intermediate layer outputs into the oracle would blur:

> what the system received

with:

> what the evaluator says is correct.

That is exactly the distinction the architecture and CHECK/AUDIT separation are trying to preserve.

Keep them separate.

---

# 3. Correct scorer input contract

Replace the old input rule with:

> **Scorer input = TARGET_ARTIFACT + READ_ONLY_DEPENDENCY_CONTEXT + ORACLE + FROZEN_PREDICATE/CONTRACT_RULES.**

Harness-only and never visible to the scorer:

- seed id;
- expected predicate;
- mutation metadata;
- expected specificity set / answer key;
- seed manifest fields that encode expected outcome.

The scorer evaluates predicates for the **target artifact's parent_type only**.

The dependency context is evidence, not another target.

---

# 4. Dependency-context matrix for GATE0-C1

Use the smallest upstream context required by the frozen dependency graph.

## S1_OUTPUT target

Provide:
- target S1 artifact;
- ORACLE-2.0;
- frozen predicate/contract rules.

No STRUCTURE dependency precedes S1.

## S2_OUTPUT target

Provide:
- target S2 artifact;
- clean S1 dependency output for this case;
- ORACLE-2.0;
- frozen predicate/contract rules.

## S3_OUTPUT target

Provide:
- target S3 artifact;
- clean S1 dependency output;
- clean S2 dependency output;
- ORACLE-2.0;
- frozen predicate/contract rules including REASON-1 where referenced.

## S4_BLUEPRINT target

Provide:
- target S4 artifact;
- clean S1 dependency output;
- clean S2 dependency output;
- clean **rendered** S3 dependency output used to construct the S4 parent;
- ORACLE-2.0;
- frozen predicate/contract rules including PROJECTION_MAP.

For this campaign, S4 is based on the rendered S3 parent, not the structurally clean NOT_RENDERED calibration parent.

---

# 5. Critical invariant — dependency context is fixed, clean, and seed-independent

For every seed in one target-parent lineage:

> **only the target artifact is mutated.**

Its dependency context must be:

- unmutated;
- hash-pinned;
- the same context used by the corresponding clean target parent;
- independent of which seed is being scored.

The harness must fail if a dependency-context hash differs unexpectedly.

This prevents the context itself from becoming a hidden second mutation.

---

# 6. Dependency context is not scored

The scorer may read upstream dependencies only to evaluate predicates owned by the target layer.

It must not:

- emit S1 findings while scoring an S3 seed;
- treat an upstream context defect as a target-layer defect;
- mutate or repair the dependency context;
- infer the expected seed answer from dependency filenames or harness metadata.

Gate 0 specificity remains:

> every other ACTIVE predicate in the **target parent_type** is silent.

Not "all predicates in all supplied context layers."

---

# 7. Frozen contract rules are also scorer inputs

Review 081's phrase "predicate registry/rules" needs one clarification.

Some mechanical predicates reference accepted contract objects outside the predicate prose:

- `S3-CAND-01` uses `REASON-1`;
- `S4-PROJ-01` uses `PROJECTION_MAP`.

Therefore the scorer may receive the frozen rule material those predicates explicitly reference.

This is contract input, not answer-key input.

Do not hard-code a private alternative representation that can drift from the accepted rule source without a binding check.

---

# 8. HUMAN_REVIEW packets use the same principle

A blinded human-review packet may include the minimum read-only dependency context needed to decide its predicate.

Examples:

- `S1-CAND-01`: target S1 + relevant oracle/source material.
- `S2-ADOPT-01`: target S2 + relevant oracle/source material.
- `S2-REP-01`: target S2 + the relevant S1 problem/claim context + source/oracle objects/relations needed to judge support.

Still hidden:

- seed id;
- mutation;
- expected predicate;
- expected verdict;
- specificity answer key.

The packet should not force a human to infer a missing upstream claim that the predicate explicitly depends on.

---

# 9. This is an ACCEPTANCE / scorer-interface change, not an architecture design change

No module ownership changes.

No runtime interface changes.

No experiment hypothesis changes.

No predicate is weakened or expanded.

The change only corrects what evidence the evaluator is allowed to inspect in order to evaluate already-frozen predicates.

Therefore:

> **do not reopen architecture or DC-002.**

Do update the Gate 0 scorer-input/blindness contract and any scorer-construction brief that says "artifact + oracle + predicate registry only."

Because `00-GATE0-MANIFEST.md` is a governing hashed source, regenerate the source-first package and hashes after the correction.

---

# 10. Implementation instruction

DeepSeek should now:

1. patch the Gate 0 scorer-input/blindness text to the corrected contract;
2. define the campaign's dependency-context mapping without creating a new runtime module;
3. ensure dependency files are hash-pinned and seed-independent;
4. regenerate the package twice and verify zero diff;
5. then build the scorer + harness;
6. include negative tests showing:
   - scorer cannot receive/read answer-key fields;
   - scorer can evaluate S3-SEL-01 from S2 dependency context rather than a proxy;
   - scorer can evaluate S3-CAND-01 against the S1 candidate set;
   - scorer can evaluate S4-PROJ-01 against upstream source layers + PROJECTION_MAP;
   - S2-REP-01 human packet includes the relevant S1 claim context;
   - changing only harness answer-key metadata cannot change scorer findings;
   - changing dependency context unexpectedly causes a harness/input-integrity failure.

Then stop for review before Gate 0 execution.

---

# 11. Current state

- Architecture: **CLOSED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Build/generator: **PASS**
- Source contract overall: **ACCEPTED EXCEPT NARROW SCORER-INPUT CLAUSE REOPENED**
- Review 081 scorer-input clause: **REVISED BY THIS REVIEW**
- Scorer implementation: **PAUSED CORRECTLY / MAY RESUME AFTER PATCH**
- Gate 0: **UNRUN**
- Three-human-review operational prerequisite: **OUTSTANDING**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**

DeepSeek was correct to stop instead of implementing a proxy scorer.
