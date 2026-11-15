# ChatGPT review 050 — execution-layer exact verification after second correction pass

## Verdict

**REVISE LOCALLY. DO NOT RUN YET.**

The second correction pass fixes many of review 049's substantive issues, but the exact files still contain several execution blockers and internal inconsistencies.

Nothing here reopens the architecture or the eight experiment specifications.

---

# 1. Gate 0 exact-predicate mapping is still incomplete

The seed file now maps each seed's **must-fire** field to current AX predicate ids.

That is good.

But the file simultaneously states:

> `expected_fire / must_not_fire` — predicate ids, not family names.

The tables still use family labels in `must not fire`, e.g.:

- `S2, S3`
- `S1`
- `I4`

Those are not exact predicate ids.

## Required repair

Either:

1. instantiate exact `must_not_fire` predicate ids per seed; or
2. explicitly redefine that column as **family-level silence**, and maintain a separate exact-predicate specificity set if needed.

Do not claim exact-id specificity while storing family labels.

---

# 2. Gate 0 runnable-count status is wrong

The current rows contain:

- 18 `RUNNABLE` seeds;
- 3 `PENDING_SCHEMA` seeds;
- 1 `PENDING_DEPENDENCY` seed.

The file says:

> 14 RUNNABLE, 3 PENDING_SCHEMA, 1 PENDING_DEPENDENCY.

That status is stale.

Correct the count or remove aggregate counts and derive them mechanically later.

---

# 3. Gate 0 should calibrate only the active predicate set for this pilot

Several runnable seeds target predicates that do not apply to CASE-01/02/09.

Example:

- `G0-S1-03 -> S1-BODY-01`
- but `S1-BODY-01` applies to CASE-07/08/10, none of which is in the 3-case pilot.

The frozen program already says calibration is scoped to predicates actually used.

## Required repair

The 3-case pilot manifest must declare its **ACTIVE_PREDICATE_SET**.

Gate 0 for this pilot calibrates exactly that active set and its required scorer families.

Do not require unrelated future-case predicates to block the pilot.

---

# 4. Pending predicates must be excluded from the pilot verdict explicitly

Current pending predicates include:

- `S2-ADOPT-02` — PENDING_SCHEMA, applies `all`;
- `S2-REP-02` — PENDING_SCHEMA;
- `S4-REP-01` — PENDING_SCHEMA, applies to CASE-02/09;
- `S4-ORD-01` — PENDING_DEPENDENCY, applies `all`.

The manifest says:

> PASS = all required predicates true 3/3.

As written, CASE-01/02/09 cannot have a clean PASS unless "required" is separately defined to exclude pending predicates.

## Required repair

Freeze for this pilot:

- `ACTIVE` predicates — contribute to verdict;
- `PENDING_SCHEMA`;
- `PENDING_DEPENDENCY`;
- optional `CHARACTERIZATION_ONLY`.

State explicitly:

> only ACTIVE predicates contribute to the pilot verdict.

A pending predicate cannot silently count as pass/fail.

---

# 5. S2-REP-02 remains internally contradictory

Current text says:

> `SEMANTIC · PENDING_SCHEMA`

and:

> not scoreable mechanically until schema exists, **but until then a human judges it against the written rule**.

This still mixes two states.

If a frozen human semantic predicate exists now, it is scoreable as SEMANTIC and should have:
- a defined oracle;
- Gate 0 seed;
- verdict participation.

If it is `PENDING_SCHEMA`, it must not contribute to this pilot verdict.

## Required repair

For the current pilot, simplest:

> `S2-REP-02 = PENDING_SCHEMA / excluded from verdict`.

Later, either define the local schema or define a separate explicit semantic oracle.

---

# 6. Experiment repetition semantics are still inconsistent

At the top of `predicates.md`:

> `MECHANICAL` — deterministic, one run.  
> `SEMANTIC` — judged, three runs, must agree 3/3.

That still reads as if predicate mode determines experiment run count.

But the manifest freezes:
> 3 fresh Doximity repetitions for the experiment.

Every ACTIVE predicate should be scored on every valid experiment repetition.

Then the scoring rules say:

> 2/3 semantic disagreement is "semantic nonconformance recorded as `UNSCORED`."

That conflicts with the manifest, where:
- `NONCONFORMANT` = a required predicate false;
- `UNSCORED` = fewer than 3 valid runs.

## Required repair

Separate these concepts cleanly.

### Predicate mode
- MECHANICAL = deterministic check of one artifact instance;
- SEMANTIC/HYBRID = semantic judgment of one artifact instance.

### Gate 0
- calibration repetition policy lives only in Gate 0.

### Experiment
- all ACTIVE predicates are scored on each of the 3 valid repetitions;
- 3/3 pass = pass under frozen condition;
- any valid-run predicate failure = experiment nonconformance;
- disagreement across repetitions is also a reproducibility finding;
- `UNSCORED` remains reserved for insufficient valid runs / missing prerequisites, not 2/3 disagreement.

Do not call a valid 2/3 outcome UNSCORED.

---

# 7. Architecture-escalation trigger is now too restrictive in the opposite direction

The manifest says a structural predicate must be false in:

> all valid runs of **all cases**

before it even becomes architecture-escalation evidence.

That is not the rule we froze.

A single well-controlled case can contain a logical counterexample to a universal responsibility invariant.

The correct distinction is:

- one execution miss does not prove architecture failure;
- 3/3 reproducible failure on one controlled discriminating case may justify architecture adjudication;
- architecture reopens only if adjudication shows the correct requirement cannot be satisfied without violating the canonical responsibility boundary after alternative causes are excluded.

## Required repair

Replace "all runs of all cases" with case-local evidence language.

For example:

> Reproducible structural nonconformance on a controlled case is evidence that triggers architecture adjudication; it is not itself proof. The adjudication determines whether the canonical boundary is impossible to satisfy for that case after implementation, schema/contract, substrate, scorer, and platform causes are excluded.

Do not require every unrelated fixture to fail before recognizing a logical counterexample.

---

# 8. The experiment-local artifact schema is still too informal for the claimed mechanical predicates

Current artifact summary is:

```
S1 candidates[] id, subject, anchors[], salience, candidate_claims[]
S2 adjudication[] ... representations[]
S3 rendered[] ...
S4 blueprint ...
```

This is not yet an exact emitted schema.

Several mechanical checks require fields/keys whose precise representation is unspecified.

Examples:
- `S1-AUTH-01` checks forbidden adoption fields;
- `S1-AUTH-02` checks absence of selected claim;
- `S3-SEL-01` compares selected representation against S2 approved set;
- `S4-MEM-01` compares unit member ids against retained-use map;
- `S3-INC-01` needs a problem -> approved representation link.

## Required repair before scorer implementation

Define an **experiment-local typed test schema** for the ACTIVE 3-case pilot.

It need not freeze the global production Case IR.

It only needs to expose the fields required by the active predicates unambiguously.

This is the cleanest way to make Gate 0 mutations such as:
- `candidates[0].adopted`
- `rendered[0].selected_rep`

mean something exact.

---

# 9. F-1 corpus inference is still not corrected

The corpus still says:

> only the third outcome — model marks the absence — sustained across cases argues for a schema addition.

That is backwards.

If the current architecture can mark a required absence correctly without a new schema, that argues **against** needing a schema addition.

The correct sequence remains:

1. signer/product defines required behavior for unknown-but-relevant data;
2. construct a source case establishing that unknown state;
3. test current architecture against that requirement;
4. propose schema change only if the required behavior cannot be represented/preserved reliably.

`P-08` is correctly marked `PENDING_PRODUCT_DECISION`; now make F-1 consistent with it.

---

# 10. Manifest fixture provenance remains stale

The fixture file correctly says:

> DERIVED_SYNTHETIC ... not derived from any supplied baseline.

But the manifest still says:

> CASE-01/02/09 are reconstructed from BASELINE-01 and the signer's prior-stroke material.

That is false and contradicts the fixture file.

## Required repair

Use the fixture file's accurate description:

> derived synthetic architecture fixtures based on the prior-stroke/adoption counterexamples developed during architecture review.

Do not cite BASELINE-01 as provenance.

---

# 11. CASE-01 expected-outcome text in predicates remains ambiguous

The fixture file is now clear:

> the infarct must not render as an A/P problem.

But `predicates.md` still says:

> infarct not adopted; **problem renders with historical attribution or not at all**

"problem renders" is ambiguous and can be read as allowing an infarct A/P problem.

## Required repair

State:

> infarct does not render as an A/P problem; infarct information may appear only as attributed body/history context if selected.

---

# 12. Gate 0 note-level local predicates are not defined and are not needed for this pilot

The seed file says `NT-*` ids are "defined here," but it only names them in seed rows.

It does not provide independent predicate definitions/oracles.

Also, AX-S1S2-D outputs STRUCTURE artifacts, not a final note, so note-level calibration is not required to gate this 3-case pilot.

## Required repair

For the pilot:
- exclude NT-* families from required Gate 0 scope.

Later, before a note-level experiment uses them:
- define their exact predicate semantics/oracles;
- then calibrate them.

---

# 13. What is now accepted

The following review-049 corrections are cleanly applied:

- G0-S1-03 now targets candidacy, not source grounding;
- G0-S2-04 now seeds contradiction deletion;
- G0-S1-01 now mutates an adoption field;
- S2-ADOPT-02 is no longer falsely mechanical;
- S3-ACCT-01 no longer invents a mandatory reason;
- S4-REP-01 correctly acknowledges its missing representation-id dependency;
- Gate 0 ordering seed and S4 ordering predicate are both pending;
- fixture sex/pronoun mismatch fixed;
- fixture dates moved before project date;
- CASE-09 AX-SHARED wording removed;
- fixture provenance is corrected in the fixture file itself;
- CASE-01 fixture expectation explicitly forbids infarct A/P rendering.

These should not be reopened unless the next revision regresses them.

---

# 14. Readiness

## Architecture
CLOSED / CONVERGED.

## Gate 0
Still **not executable** for the pilot until:
- active predicate set is frozen;
- exact seed specificity mapping is reconciled;
- local test schema exists;
- pending predicates are excluded;
- Gate 0 scope is limited to the pilot's active predicates.

## AX-S1S2-D 3-case pilot
Still **not runnable as acceptance evidence** until:
- predicate/run semantics are consistent;
- local schema is frozen;
- manifest provenance and escalation wording are corrected.

## Doximity
Do not run yet.

## Phase 0
Do not touch.
