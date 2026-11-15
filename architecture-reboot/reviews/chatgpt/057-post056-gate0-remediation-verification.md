# ChatGPT review 057 — post-056 Gate 0 remediation verification

## Scope

This review verifies the unannounced post-056 corrections now present on branch HEAD after:

- DeepSeek independent review `034-independent-review-gate0.md`
- ChatGPT reconciliation `056-independent-gate0-review-reconciliation.md`

## Verdict

> **MOST SUBSTANTIVE 034/056 BLOCKERS ARE FIXED. GATE 0 IS STILL NOT READY FOR SCORER IMPLEMENTATION UNTIL THE CONTROL-PLANE FILES ARE SYNCHRONIZED.**

This is no longer an architecture problem.

The remaining issues are narrow:
- active-set / seed-inventory inconsistency;
- Gate 0 calibration authority inconsistency;
- missing harmless-variation control;
- incomplete frozen campaign identity;
- one unrelated corpus F-1 contradiction.

No Phase 0.
No Doximity pilot.

---

# 1. Temporal source-of-truth mismatch — FIXED

Current CASE-01 oracle now preserves:

- O01 temporal = `2024-02 documented`
- O02 temporal = `2024-02`
- O03 temporal = `June–November`
- O04 temporal = `now`

and correctly stores O05/O06/O07 as:

> `status: current`

rather than inventing a temporal field.

The clean parent now uses the exact frozen values for the S2 temporal records it emits.

This resolves 034 B1 / 056 item 1.

---

# 2. Adoption oracle overreach — FIXED ENOUGH FOR CASE-01

Current oracle now scores adoption only for:

- O01 = false
- O03 = true

and explicitly states:

> objects not named are not scored.

It also correctly distinguishes:

> O07 is a medication fact and cannot adopt anything; that is not itself an adoption verdict.

This is materially better and resolves the prior all-object answer-key overreach.

For the discriminating historical-diagnosis rule, O01 remains the important target.

Do not expand the adoption oracle to every source object without a defined reason.

---

# 3. G0-S2-06 isolation — FIXED

Current mutation:

> O01 adoption `false -> null`

with evidence unchanged `null`.

This is:
- one field;
- schema-valid;
- wrong against CASE-01's frozen expected value;
- isolated from the separate “true requires evidence” rule.

Accept.

---

# 4. G0-S1-05 semantic shortcut — FIXED

The added infarct candidate is now structurally plausible:

- source anchor S01;
- source-grounded candidate claim;
- valid salience shape;
- no embedded `has_assessment_question` answer field.

Therefore a semantic scorer must actually use case/oracle context to determine that the prior infarct does not deserve an independent current assessment question.

Accept.

---

# 5. S4-REP-01 — correctly reactivated in two places, but control-plane files are inconsistent

Current `predicates.md` ACTIVE set now includes:

> `S4-REP-01`

Current generator and generated manifest now include:

> `G0-S4-05`

and the seed correctly mutates:

> S4 unit representation `R1 -> R-999`

while S3 remains `selected_rep = R1`.

This is the right test.

## But current `predicates.md` contradicts itself

Immediately after the active set, it still says:

> excluded ... `S4-REP-01`

That is now false.

## And `G0-SEEDS.md` is stale

It still says:
- 15 seed artifacts;
- 13 active predicates;
- G0-S4-05 is NOT_IN_PILOT;
- S4-REP-01 is inactive.

But current generated state is:

> **16 active seed artifacts / 14 active predicates**

assuming no other active-set change.

### Required correction

Synchronize all four authorities:

1. `predicates.md` ACTIVE set and exclusion prose;
2. `G0-SEEDS.md` table status;
3. `G0-SEEDS.md` current-state arithmetic + active map;
4. generated `MANIFEST.json`.

Expected:
- S4-REP-01 active;
- G0-S4-05 runnable and active;
- active map includes `S4-REP-01 -> G0-S4-05`;
- 16 active seeds / 14 active predicates.

This is the main current exact-file inconsistency.

---

# 6. Predicate-level finding schema — FIXED

Gate 0 manifest now defines a finding record containing:

- exact `predicate_id`;
- owner;
- artifact;
- artifact path;
- oracle reference;
- expected;
- observed;
- status.

It explicitly rejects a scorer that reports only the layer.

This resolves 034 B7 / 056 finding-schema requirement.

Keep this as the scorer output contract.

---

# 7. Gate 0 run-count authority — STILL BLOCKING

`G0-SEEDS.md` now correctly says:

> calibration policy is derived from each predicate's own mode.

But `00-GATE0-MANIFEST.md` still says:

> Gate 0 is scoped to a predicate family

and contains a table assigning:
- family-level mode;
- family-level run count.

Its procedure still says:

> semantic families repeat three times.

That is exactly the contradictory authority identified by 034.

The active families contain mixed predicate modes, so family-level run counts are not correct.

## Required correction

Make the predicate registry the sole authority:

> For every ACTIVE predicate, read its mode from `predicates.md`.

Then Gate 0 maps:

- `MECHANICAL` -> deterministic calibration procedure;
- `SEMANTIC` -> semantic calibration procedure;
- `HYBRID` -> explicitly defined hybrid calibration procedure when active.

Family is organizational only.

A family-level aggregate pass may still mean:
> every active predicate in that family passed its own calibration policy.

But the family does not determine the run count.

---

# 8. Harmless-variation control — STILL MISSING

Gate 0 requires:

> same content, different valid wording -> zero findings.

No such frozen artifact currently exists.

This was one of the important 034 blockers because it tests whether the scorer is matching exact surface form instead of the predicate.

## Required artifact

Create at least one experiment-local harmless variation of the clean parent.

It should change valid non-contractual surface representation without changing the semantic/structural truth of any active predicate.

Examples must be chosen carefully because most current artifacts are typed JSON rather than prose.

A valid control could vary:
- non-semantic JSON ordering only if scorer sees parsed objects rather than canonicalized text; or preferably
- a source-faithful candidate subject/claim wording variant explicitly accepted by the oracle's semantic-equivalence rule.

The control needs:
- frozen artifact;
- expected zero findings;
- hash;
- inclusion in the campaign manifest.

Do not use a trivial byte-format variation if the scorer parses JSON before judging it; that would calibrate nothing.

---

# 9. Scorer blindness — conceptually fixed, not yet frozen in the Gate 0 manifest

The oracle note states:

> scorer receives artifact + oracle + predicate registry.

The earlier handoff correctly states:
- seed expected answer/mutation metadata belongs to the harness;
- scorer must not see it.

But `00-GATE0-MANIFEST.md` still does not clearly freeze this input separation as an execution rule.

## Required correction

Add an explicit section:

### Scorer input
- artifact under score;
- frozen oracle;
- frozen predicate registry.

### Harness-only input
- seed manifest;
- seed id;
- expected predicate;
- mutation metadata;
- specificity expectation.

The harness compares scorer output to the answer key only **after** the scorer returns findings.

This should be in the executable Gate 0 manifest, not only in an oracle note/channel discussion.

---

# 10. Frozen campaign identity — PARTIALLY FIXED

Current generated manifest now has:
- full canonical-JSON SHA-256 for parent;
- oracle hash;
- seed hashes;
- predicate-registry label/version;
- active-set label;
- specificity-policy label.

Good.

Still missing hashes of controlling source artifacts:

- exact `predicates.md` content;
- exact `G0-SEEDS.md` seed specification;
- exact `make_seeds.py` generator;
- preferably `schema.md`.

The human ids:
- `PILOT-1`;
- `PILOT-ACTIVE-1`;
- `FULL_SILENCE-1`

are useful labels, but they do not prove which file content those labels refer to.

## Required correction

Freeze full content hashes for the governing files in the campaign manifest.

Then changing any governing contract necessarily changes campaign identity.

---

# 11. Seed-spec wording — G0-S1-05 FIXED; inventory prose still stale

The G0-S1-05 row now accurately describes the CASE-01 context-only infarct candidate.

Accept.

The remaining problem is only the stale inventory/current-state prose described in section 5.

---

# 12. Corpus F-1 contradiction — STILL OPEN, but not a Gate 0 scorer blocker

Current corpus says:

> unknown-marker vs omission is blocked on a product decision.

Correct.

But it still says:

> omission fails completeness.

That is still unsupported until the product decision exists.

It also says:
> no schema proposal until a run shows failure.

The correct sequence remains:

1. signer/product defines required behavior;
2. test the requirement;
3. schema only if current representation cannot satisfy it.

## Required correction

Until the product decision:
- unsupported invention = failure;
- omission vs explicit marker = not scoreable.

This should be fixed, but it does not need to block building the Gate 0 scorer once the Gate 0 control-plane issues above are closed.

---

# 13. What the detailed independent review accomplished

DeepSeek 034 was valuable because it caught defects that checklist reconciliation missed:

- false temporal ground truth;
- overlapping predicate domains;
- adoption-seed invalidity;
- seed-inventory drift;
- absence of predicate-level finding records;
- contradictory calibration authorities;
- missing negative-control artifacts.

Most of the substantive data/oracle defects are now repaired.

The remaining work should therefore stay narrow. Do not reopen the architecture or rebuild the experimental program.

---

# 14. Current readiness

## Architecture
**CLOSED / CONVERGED**

## Experiment program
**CLOSED / CONVERGED**

## AX-S1S2-D execution specification
**CONDITIONALLY CLOSED**

## Gate 0 data/oracle/seed build
**SUBSTANTIVELY CORRECTED**

## Gate 0 control plane
**NOT YET CLOSED**

Before scorer implementation:

1. synchronize S4-REP-01 active-set / inventory files;
2. remove family-level calibration-run authority;
3. freeze scorer-vs-harness input separation in Gate 0 manifest;
4. create and freeze a meaningful harmless-variation control;
5. hash the controlling predicate/spec/generator/schema files.

Then the scorer may be implemented and independently reviewed.

## Gate 0
UNRUN.

## Doximity pilot
DO NOT RUN.

## Phase 0
Do not touch.
