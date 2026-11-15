# ChatGPT review 055 — corrected Gate 0 build verification

## Verdict

**GATE 0 BUILD IS SUBSTANTIALLY IMPROVED, BUT SCORER IMPLEMENTATION SHOULD WAIT FOR ONE FINAL LOCAL CONSISTENCY PASS.**

The rebuilt CASE-01 parent is much cleaner:
- S1 candidate claim is now source-faithful;
- S2 support is reduced appropriately;
- S3 retained/disposition accounting now has a render path;
- the oracle provides the missing scorer context;
- G0-S1-05 no longer leaks the semantic answer.

The execution specification remains conditionally closed.
No architecture redesign is indicated.

However, the current build still has several concrete inconsistencies that would contaminate calibration if the scorer were implemented against it now.

---

# 1. Hard blocker — S1-AUTH-01 and S1-AUTH-02 overlap on `selected_claim`

Current predicates:

### S1-AUTH-01
forbids the field set:
`{adopted, adoption, adoption_verdict, selected_claim, resolved, status_current}`

### S1-AUTH-02
asserts:
> S1 emits no single selected claim

Current seed:
> G0-S1-02 adds `selected_claim = "CC1"` and expects only `S1-AUTH-02`.

But that exact mutation necessarily also violates `S1-AUTH-01`.

Gate 0 specificity now requires:
> every active predicate except the expected/whitelisted one stays silent.

Therefore the current calibration corpus is internally impossible unless this overlap is resolved.

## Preferred repair

Restore the conceptual separation:

### S1-AUTH-01 — adoption/final-state authority
Forbidden decision fields:
- `adopted`
- `adoption`
- `adoption_verdict`
- `resolved`
- `status_current`

### S1-AUTH-02 — final-claim-selection authority
Owns:
- `selected_claim`
- equivalent selected/final-claim state.

Then:
- G0-S1-01 / G0-S1-06 calibrate S1-AUTH-01;
- G0-S1-02 calibrates S1-AUTH-02;
- specificity can remain strict.

Do not solve this merely by whitelisting both predicates unless intentional overlap is a frozen design choice. The two predicates exist to test different authority leaks, so non-overlap is cleaner.

---

# 2. G0-S2-06 is still a coupled two-field mutation

The generated seed changes:
- `adoption: false -> true`
- `evidence: null -> [S02]`

The manifest now records it as one record-level mutation, but Gate 0 still states:
> mutation changes exactly one thing.

More importantly, `S02` does not contain an explicit current adoption of the infarct. It is the falls/no-new-deficit sentence.

So the seed combines:
1. wrong adoption;
2. questionable evidence support.

That weakens isolation.

## Preferred repair

Build a small clean CASE-02 S2 parent:
- adoption = true;
- correct evidence = S02 of CASE-02, where the infarct is explicitly re-adopted.

Then mutate only:
> adoption true -> false

for `S2-ADOPT-01`.

This gives a true one-field semantic inversion.

If the team intentionally permits atomic coupled-record mutations instead, change the Gate 0 mutation rule explicitly and use evidence that does not introduce a second semantic defect.

---

# 3. G0-S1-05 written definition still does not match its executable parent

`G0-SEEDS.md` says:

> old infarct used only as evidence for the seizure claim

But the generated seed is based on CASE-01:
- falls encounter;
- no seizure claim;
- infarct is historical/context-only.

The executable seed itself is valid for `S1-CAND-01`, but its written definition is stale.

## Required repair

Describe it as:

> append the source-grounded old left MCA infarct as a separate candidate in CASE-01 even though it is historical/context-only and the encounter poses no independent current assessment question for it.

Spec, generator, artifact, and oracle should tell the same story.

---

# 4. schema.md example still teaches an invalid S1 synthesis

The clean parent was correctly repaired, but the schema example still shows:

> `gait instability from deconditioning`

as a candidate claim.

That wording is not source-present in CASE-01 and is exactly the synthesis error previously removed from the parent.

If `schema.md` is used as implementation/prompt guidance, the example can reintroduce the defect.

## Required repair

Use a source-faithful example such as:

> `three falls since June`

with support `[S02]`.

Examples in a typed test schema must themselves obey the interface contract.

---

# 5. Gate 0 family-level mode table is stale

`00-GATE0-MANIFEST.md` still labels whole families as:
- semantic;
- mechanical;
- mechanical + semantic

and associates run counts with those family labels.

But the current predicate registry correctly defines mode **per predicate**.

Example:
- S1 family contains semantic and mechanical predicates;
- S2 family contains semantic and mechanical predicates;
- S3 family contains mechanical predicates and future semantic ones.

## Required repair

Family names may remain organizational only.

Calibration repetition count must derive from the exact predicate mode in the versioned predicate registry:
- MECHANICAL -> deterministic calibration execution;
- SEMANTIC/HYBRID -> frozen semantic-calibration policy.

Do not infer scorer mode from family membership.

---

# 6. schema.md field map still carries a stale partial S1 forbidden-set copy

The schema correctly says the authority is the versioned set in `predicates.md`.

But the field->predicate row still says S1-AUTH-01 checks only:

> adopted / adoption / selected_claim

That is both incomplete and, after repair #1, conceptually mixed.

## Required repair

Use:

> absence of the versioned S1-AUTH-01 adoption/final-state forbidden-field set defined in `predicates.md`.

No second field-name copy.

---

# 7. Corpus F-1 still contains the exact contradiction previously identified

The file correctly states:
> omission versus marker is a product decision not yet made.

But immediately afterward it still says:

> a run that omits the slot entirely fails completeness.

That conclusion is not available until the product decision exists.

## Required repair

Until product behavior is frozen:

- invented unsupported value -> fidelity failure;
- omission vs explicit unknown marker -> **not scoreable**.

Also change the proposed-next-action rule from:

> no schema proposal until a run shows failure

to:

> decide required product behavior first; test that requirement; propose schema only if the current representation cannot satisfy it.

A system cannot fail an undecided requirement.

---

# 8. Scorer blindness must be explicit

The oracle is appropriately an answer key for the test.

But Gate 0 only means anything if the scorer does **not** receive:
- seed filename/id;
- `must_fire`;
- mutation description;
- before/after values;
- generated MANIFEST expected result.

## Required scorer/harness split

### Scorer input
Only:
- artifact under score;
- frozen case oracle;
- predicate registry/version.

### Harness input
Additionally:
- seed manifest;
- expected predicate(s);
- full-silence policy.

The harness compares scorer findings to the expected seed result **after** scoring.

Make this separation explicit before scorer implementation.

---

# 9. Oracle/registry identity should be frozen in the generated manifest

The manifest now hashes:
- parent;
- each seed.

Good.

It should also freeze:
- oracle version + hash;
- predicate registry version + hash;
- active predicate set;
- specificity policy version.

Otherwise the same seed artifacts could be scored against a changed oracle/predicate definition and still appear to belong to the same Gate 0 campaign.

---

# 10. Hashes should use the full digest or clearly state truncation

Current hashes are:

> `sha256:<16 hex chars>`

The generator computes SHA-256 and truncates to the first 16 hex characters.

For an auditable frozen evidence package, prefer:
> full 64-hex SHA-256

for parent, oracle, registry, and seed artifacts.

If truncation is retained for display, store the full digest separately.

Also document whether the hash is:
- file-byte SHA-256; or
- canonicalized-JSON SHA-256.

The current generator hashes canonicalized JSON objects, not file bytes. That is acceptable if named accurately.

---

# 11. Oracle robustness for semantic candidate matching

`oracle.json` currently stores:

> `candidate_subjects_must_exclude: ["old left MCA infarct", "known left MCA infarct"]`

That works for the exact G0-S1-05 seed, but the eventual Doximity artifact might phrase the same forbidden subject as:
- chronic left MCA stroke;
- prior left MCA infarction;
- old left hemispheric infarct.

The semantic scorer should not reduce S1-CAND-01 to exact string matching.

## Required scorer behavior

Use the oracle's source/object identity and semantic equivalence, or add a canonical subject/object reference, e.g.:

> forbidden independent-candidate objects: O01/O02 or canonical concept `prior_left_MCA_infarct`.

This is scorer implementation guidance, not a need to change the architecture.

---

# 12. What is now accepted

The following build corrections are good:

- CASE-01 S1 claim is source-faithful;
- S2 representation support is narrowed;
- S3 retained/disposition accounting is coherent with an A/P-only parent;
- the generated clean parent matches the source parent;
- the oracle supplies spans, temporality, adoption expectations, and required plan-unit information;
- G0-S1-05 answer leakage was removed;
- generator now records mutation metadata;
- generator is correctly described as implementation rather than authority;
- generated parent/seed hashing exists;
- synthetic-vs-realistic evidence boundary remains clear.

---

# 13. Current readiness

## Architecture
CLOSED / CONVERGED.

## Experiment design
CLOSED / CONVERGED.

## AX-S1S2-D execution specification
CONDITIONALLY CLOSED.

## Gate 0 build
**NEAR-READY / ONE LOCAL CONSISTENCY PASS REQUIRED**

## Scorer
**DO NOT IMPLEMENT AGAINST THE CURRENT BUILD YET** until items 1–8 above are resolved, especially:
- S1 predicate overlap;
- S2 adoption seed isolation;
- scorer blindness.

## Gate 0
UNRUN.

## Doximity pilot
DO NOT RUN.

## Phase 0
Do not touch.
