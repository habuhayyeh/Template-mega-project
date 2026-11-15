# ChatGPT review 052 — fourth execution-layer correction verification

## Verdict

**EXECUTION SPEC IS NEAR-CLOSED, BUT THE PILOT IS NOT YET RUNNABLE.**

The fourth correction pass resolves the major logical inconsistencies from reviews 049–051. The remaining issues are now narrow and mostly execution-harness/calibration readiness.

Nothing here reopens:
- DC-001;
- the eight architecture experiment specifications;
- Phase 0.

---

# 1. Gate 0 still has no actual clean parent artifacts or scorer implementation

The repository currently contains only:

- `experiments/gate0/00-GATE0-MANIFEST.md`
- `experiments/gate0/seeds/G0-SEEDS.md`

There are no durable:
- S1 clean parent artifact;
- S2 clean parent artifact;
- S3 clean parent artifact;
- S4 clean parent artifact;
- scorer implementation/prompt/package;
- seeded mutated artifacts;
- Gate 0 run records.

The seed file defines **mutations**, not the artifacts those mutations are applied to.

Therefore Gate 0 remains:

> **SPECIFIED / UNRUN / NOT YET EXECUTABLE**

This is not a design defect. It is simply the next required build step.

## Required next artifact

Create reviewed, experiment-local clean parent artifacts conforming to `AX-S1S2-D/schema.md`, then materialize the active seeds from those parents.

A seed cannot calibrate a scorer until the parent and mutated artifact both exist.

---

# 2. The ACTIVE_PREDICATE → seed count is wrong

The map contains 15 active predicates.

The actual seed references in the map are:

- S1: 4 seeds
- S2: 4 seeds
- S3: 3 seeds
- S4: 5 seeds

Total:

> **16 active Gate 0 seeds**, not 18.

The current text says:

> 18 seeds calibrate the 15 active predicates.

The extra runnable seeds belong to inactive predicates such as:
- `S1-BODY-01`;
- `S2-CONF-01`;
- `S3-SEL-02`.

## Required repair

Change the active-map statement to the actual count, or derive it mechanically.

The global 19 RUNNABLE / 1 PENDING_SCHEMA / 1 PENDING_DEPENDENCY count is separate and can remain if correct.

---

# 3. S2-REP-02 is active but the three pilot cases do not exercise its nontrivial condition

`S2-REP-02` now asserts:

> at most one approved representation per problem, unless every approved representation is selection-safe.

That predicate matters only when a problem has **multiple approved representations**.

CASE-01/02/09 are the adoption discriminator trio and do not currently specify a multi-approved-representation state.

Therefore in these three cases the predicate is likely to pass vacuously.

Calibration of the scorer with G0-S2-02 does not make the **experiment case** exercise the architecture property.

## Required repair

For this 3-case pilot, choose one:

### Preferred
Remove `S2-REP-02` from the active pilot set and leave it for CASE-05/06, where multiple representations are actually part of the fixture.

### Alternative
Add a deliberate multi-approved-representation condition to one pilot case, but that would broaden the adoption pilot and is not recommended.

Do not call a predicate "exercised by the pilot" when its discriminating state never occurs.

---

# 4. G0-S1-05 is too easy to calibrate the real S1 candidacy boundary

Current seed:

> append a candidate for a PMHx item with no assessment question ("hypothyroidism")

This certainly should fail, but it does not calibrate the difficult rule the architecture actually depends on:

> a **neurologic**, source-grounded subject may be relevant/contextual and still not warrant its own current assessment question/problem candidate.

A scorer could simply reject non-neurologic PMHx and pass Gate 0 while still failing the actual stroke-context case.

## Required repair

Use a neurologic context-only seed, for example:

> append a source-grounded prior left MCA infarct as its own S1 candidate when the encounter uses it only as background/etiologic context and poses no independent current assessment question for the infarct.

That directly calibrates `S1-CAND-01`.

A non-neurologic PMHx seed can remain as an additional easy control, but it should not be the sole calibration seed for the candidacy rule.

---

# 5. Gate 0 specificity checking is still weaker than the manifest's requirement

The seed table gives one or two `must not fire` predicate ids per seed.

But the Gate 0 manifest's principle is broader:

> a seed must not trigger unrelated predicate families.

A scorer that fires:
- the expected predicate;
- stays silent on the one listed neighbor;
- but fires three other unrelated active predicates

would currently satisfy the row-level silence check.

## Required repair

For the active pilot, define specificity as:

> expected predicate(s) may fire; **no other ACTIVE predicate may fire unless explicitly whitelisted for that seed**.

This is stronger and easier to audit than hand-picking one neighbor per row.

The current `must_not_fire` column can remain as a highlighted sentinel, but it cannot be the whole specificity oracle.

---

# 6. schema.md contains stale text contradicting the fourth-pass activation

The final paragraph still says:

> Predicates marked `PENDING_SCHEMA` ... the schema does not yet expose `selection_safe` and `representation id` well enough...

But the same file now explicitly exposes:

- `representations[].id`;
- `representations[].selection_safe`;
- S3 `selected_rep`;
- S4 `unit.representation`.

And the predicate file correctly activates:
- `S2-REP-02`;
- `S4-REP-01`.

## Required repair

Delete or rewrite that stale paragraph.

The only remaining schema-pending predicate is:

> `S2-ADOPT-02`

because the missing dependency is **explicit-link semantics**, not a missing representation id/selection-safe field.

---

# 7. Corpus F-1 is logically corrected, but the file still overstates what is known

The file still begins:

> The current Case IR has no way to express this. Its only options are to omit or invent.

That is precisely what has **not** yet been established.

The corrected paragraph below says:
- decide product behavior first;
- test whether current representation can produce it;
- add schema only if it cannot.

Those two statements conflict.

## Required repair

Replace the unsupported claim with:

> It is not yet established whether the current representation can preserve the required unknown-state behavior without an explicit slot.

Also keep:
- unsupported invention = fidelity failure;
- omission vs marker = pending product decision.

---

# 8. Corpus "what is still blocked" section remains stale

Section 5 now correctly distinguishes:

- realistic signer corpus: blocked on source packages;
- derived synthetic architecture fixtures: may proceed.

But section 6 still says broadly:

> Fixtures need source packages.  
> Gate 0 parents stay DERIVED_PARENT until at least one case has a source package.  
> Scorer predicates cannot be calibrated without seeds built on real parents.

That contradicts the synthetic-pilot policy immediately above.

## Required repair

Scope those statements to the realistic signer-corpus campaign.

For the synthetic pilot:
- derived synthetic fixtures are allowed;
- reviewed derived clean parents are allowed;
- resulting evidence is limited to interface conformance under synthetic conditions.

---

# 9. manifest.md still contains the duplicate historical paragraph

The architecture-escalation section still has two consecutive paragraphs beginning:

> This separation exists because...

DeepSeek reported this was removed, but it remains in the exact file.

Delete the duplicate.

Nonblocking logically, but it is an exact-file mismatch.

---

# 10. S1 forbidden-field calibration is only partially covered

The local schema lists forbidden fields:

- `adopted`
- `adoption`
- `selected_claim`
- `current`
- `resolved`

Gate 0 currently calibrates:
- `adopted` via G0-S1-01;
- `selected_claim` via G0-S1-02.

It does not directly seed:
- `adoption`;
- `current`;
- `resolved`.

This does not necessarily require three more seeds if the mechanical checker is field-name-set based.

## Required repair

Make the checker contract explicit:

> `S1-AUTH-01` checks the complete forbidden decision-field set mechanically.

Then one representative seed may calibrate the checker implementation only if the scorer's logic is transparently set-based and independently inspected.

Otherwise add seed coverage for each distinct forbidden-field branch.

Do not imply that one `adopted` mutation proves all forbidden-field branches are detected.

---

# 11. What is now accepted

The following are clean:

- active set now includes `S1-CAND-01` and removes `S1-BODY-01` / `S2-CONF-01`;
- every currently declared active predicate has at least a named seed;
- `S2-REP-02` and `S4-REP-01` have the fields required for mechanical scoring;
- 2/3 semantic experiment disagreement is now `NONCONFORMANT` + reproducibility disagreement;
- architecture escalation is case-local and adjudicative;
- omission-vs-marker is no longer scored before product decision;
- realistic vs synthetic evidence classes are explicitly distinguished;
- local S1 schema permits canonical optional relationships;
- NT-* note-level calibration remains outside this pilot;
- fixture provenance/date/CASE-01 wording remain corrected.

---

# 12. Readiness

## Architecture
**CLOSED / CONVERGED**

## Experiment specification layer
**CLOSED / CONVERGED**

## AX-S1S2-D execution specification
**NEAR-CLOSED**

## Gate 0
**NOT YET EXECUTABLE**
because clean parent artifacts, instantiated seed artifacts, and a scorer do not yet exist.

## Three-case pilot
**DO NOT RUN YET**
until:
1. active-set/vacuous S2-REP-02 issue is resolved;
2. candidacy seed is strengthened;
3. Gate 0 specificity rule is closed;
4. stale schema/corpus/manifest contradictions are removed;
5. parent/scorer artifacts are actually built and independently reviewed.

## Phase 0
Do not touch.
