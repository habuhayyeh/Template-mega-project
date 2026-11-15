# ChatGPT review 075 — source-first execution rebuild verification

## Verdict

> **BUILD PIPELINE IMPROVED, EXECUTION PACKAGE STILL NOT ACCEPTED. SCORER REMAINS BLOCKED.**

The source-first rebuild at `5cbf573` fixes the largest failure from review 074:

- `make_seeds.py` now actually loads layer-specific parents;
- it emits four clean parents and 27 seeds;
- it carries campaign `GATE0-C1`;
- it clears generated JSON before rebuilding;
- it computes governing hashes during generation;
- it no longer depends on the deleted four-layer source parent;
- it no longer emits the old `PARENT-CLEAN.json` or `VARIATION.json`.

So the **build-system architecture is now directionally correct**.

However, the authoritative source/control package it generates from is still internally inconsistent with DC-002 and with its own calibration claims.

This remains an execution-layer problem, not an architecture or experiment-program reopen.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. Hard blocker — `schema.md` is still not a valid SCHEMA-2

The file now claims:

> Post-DC-002 only; no legacy dual-schema text.

But it still contains multiple errors.

## 1a. Wrong type for management-reference spans

Current schema example:

```yaml
management_reference_spans: true
```

The canonical interface requires:

```yaml
management_reference_spans: [S03]
```

or another list of span ids.

This is not editorial. A boolean cannot support source-grounded salience traceability.

## 1b. Residual self-contradictory addendum

Current text says:

> Each candidate carries `claim_candidates` (not `claim_candidates`)

This is a malformed remnant of the old dual-schema correction and should not exist in a clean source schema.

## 1c. Active field→predicate map is still stale

The schema says the map covers ACTIVE predicates, but it omits active:

- `S3-CAND-01`;
- `S4-PROJ-01`;
- `S4-REP-01`.

It also still says `S4-REP-01` is not scored yet, contradicting:
- `predicates.md`;
- `G0-SEEDS.md`;
- the generated manifest;
- seed `G0-S4-05`.

## 1d. No exact S4 projection schema

The entire former `S4_INPUT_VIEW` example/source rule has effectively been removed rather than replaced with the exact nested projection contract review 074 required.

A mechanical `S4-PROJ-01` scorer still has no authoritative source document defining:
- allowed destination paths;
- source owner;
- source path;
- required/optional/conditional status;
- permitted mechanical transform.

### Required action

Rewrite `schema.md` once more from scratch.

It must be the machine/scorer-facing definition of SCHEMA-2, not a lightly edited historical document.

---

# 2. Hard blocker — S4 projection is still not mechanically derivable from the committed upstream parents

The new `S4_PARENT.json` is cleaner than the old one, but it still contains semantic state absent from its stated sources.

## From S2

`S4_PARENT.json` contains:

- `from_s2.relations = [SUPPORTS O04 -> O03]`;
- `claim_relation = null`;
- `duplicate_groups = []`.

But `S2_PARENT.json` contains only:

- adjudication;
- representations with members/support/selection_safe.

It has no:
- relations;
- claim relation;
- duplicate/equivalence grouping.

Therefore the S4 projection still contains S2-owned values that cannot be copied from the committed S2 reference.

## From S3

`S4_PARENT.json` contains:

- `use` map;
- `reuse` list.

But `S3_PARENT.json` contains no:
- problem-use map;
- reuse map.

Again, those values are not derivable from the committed S3 reference.

## Consequence

The rebuilt projection still violates the core D3 invariant:

> the projection decides nothing.

The values may be clinically reasonable, but they remain authored at the projection layer rather than mechanically copied from source-owned state.

### Required action

Either:

1. extend the clean S2/S3 parents to carry the source-owned fields the S4 view needs; or
2. remove projection fields not needed by this calibration campaign.

Then freeze exact source mapping.

No value may first appear inside `S4_INPUT_VIEW`.

---

# 3. Hard blocker — branch coverage for `S3-CAND-01` is not actually isolated

The seed count is now six, matching six named branches, but several seeds violate more than the branch they claim to calibrate.

## G0-S3-08 — claimed rendered-set equality branch

Mutation:
- C1 outcome: `RENDERED -> NOT_RENDERED`.

But the seed does **not** add the required NOT_RENDERED reason.

So it simultaneously violates:
- rendered-set equality;
- missing typed reason.

It does not isolate equality.

## G0-S3-09 — claimed missing-reason branch

Mutation:
- append a second C1 NOT_RENDERED outcome with no reason.

That simultaneously violates:
- exclusivity;
- missing reason.

It does not isolate reason enforcement.

## G0-S3-10 — claimed missing-basis branch

Mutation:
- replace C1 RENDERED with C1 NOT_RENDERED / NO_PROPOSAL / empty basis.

But S3 `rendered[]` still contains C1.

So it simultaneously violates:
- rendered-set equality;
- potentially basis requirement.

Again, not isolated.

## Required construction

Add a second **clean S3 NOT_RENDERED calibration parent/reference** where:

- C1 has exactly one NOT_RENDERED outcome;
- C1 is absent from `rendered[]`;
- typed reason is valid;
- required basis refs are valid;
- all other S3 invariants hold.

Then derive:
- missing-reason seed from that parent;
- missing-basis seed from that parent.

For rendered-set equality, mutate only equality while retaining a structurally valid NOT_RENDERED outcome.

The objective is not one seed name per clause; it is **one valid parent plus one controlled defect per calibrated branch**.

---

# 4. `S4-PROJ-01` branch labels remain partially wrong

The five seeds improve coverage, but the claimed branch interpretation is not yet exact.

## G0-S4-07
Good:
- injected field outside projection schema.

## G0-S4-08
Good direction:
- adds O05 to S2-selected members although S2 representation members are O03/O04.
- tests nonselected/nonrequired projected state.

## G0-S4-09
Changes:
- `from_s1.salience.acuity MODERATE -> SEVERE`.

This is an **invented/wrong value under the correct owner group**.

It is not a wrong-owner-group seed.

## G0-S4-10
Good direction:
- changes retained ingest payload/provenance.
- tests source trace/value mismatch.

## G0-S4-11
Changes:
- `from_s2.claim_relation null -> COMPETING`.

But claim relation is canonically S2-owned and is placed under `from_s2`.

Therefore this is another **invented S2 value**, not a wrong-owner-group seed.

### Missing branch

There is still no true wrong-owner-group case.

Example:
- put S1 salience under `from_s2`;
- put S2 relation under `from_s1`;
- put S3 use/reuse under `from_ingest`.

The exact seed should use the frozen nested source map.

---

# 5. Hard blocker — `G0-SEEDS.md` claims a harmless variation that the generator does not produce

Current source spec says:

> A harmless variation and a clean parent per layer are produced by the generator.

Current generator produces:
- four parent copies;
- 27 seeds;
- manifest.

It does **not** generate a harmless variation artifact.

So source spec and generator still disagree.

Either:
- implement a harmless variation per intended calibration design; or
- remove the claim/control if it is no longer part of Gate 0.

Do not describe a control that does not exist.

---

# 6. Gate 0 manifest has not been updated to the new campaign model

`00-GATE0-MANIFEST.md` is still the older generic document.

It does not explicitly freeze:

- campaign `GATE0-C1`;
- layer-specific parent model;
- full silence **within layer**;
- source-first generation rule;
- generated-directory immutability;
- second-run zero-diff requirement;
- active-set identity `ACTIVE-PILOT-2`;
- SCHEMA-2 / ORACLE-2.0 identities.

It also still frames specificity as:

> no unrelated family to fire

rather than the now-chosen:

> all other active predicates in the same calibration layer must remain silent.

### Required action

Update the Gate 0 control-plane manifest to match the campaign that actually exists.

This file is a governing control artifact and should itself be included in campaign identity/hash once stabilized.

---

# 7. Manifest seed records still do not carry `parent_type`

The rebuild contract requested each seed record to identify:

- parent artifact;
- parent_type.

Generated artifacts themselves carry `parent_type`, which is good.

But manifest seed records currently carry only:

```json
"parent": "PARENT-S3_PARENT.json"
```

Add:

```json
"parent_type": "S3_OUTPUT"
```

Do not require the harness/scorer reviewer to infer type from filename.

---

# 8. Hash-method metadata remains ambiguous

The generator correctly uses:

- `fsha()` = SHA-256 over file bytes for governing source files;
- `canon()` = SHA-256 over canonical JSON for JSON artifacts.

But the manifest exposes only:

> `hash_method: sha256 over canonical JSON`

That description is false for `governing_hashes`.

### Required metadata

Use distinct fields, e.g.:

- `governing_hash_method: sha256(file bytes)`;
- `json_artifact_hash_method: sha256(canonical JSON ...)`.

The current underlying implementation is mostly correct; the manifest description is not.

---

# 9. Governing-hash set still omits the Gate 0 control-plane manifest

The rebuilt manifest hashes:
- canonical interfaces/architecture;
- frozen program;
- AX-S1S2-D spec;
- schema;
- predicates;
- seed spec;
- generator;
- oracle.

Good.

But `00-GATE0-MANIFEST.md` is itself the governing calibration protocol and is not hashed.

Once updated to the new campaign model, include it in the governing hash set.

Otherwise the calibration protocol can change without campaign identity changing.

---

# 10. Program/scorer semantic-mode language needs one clarification before implementation

The Gate 0 manifest says:

> semantic predicates are model- or human-judged; three runs.

That is acceptable as protocol language.

But the actual scorer is not yet built.

Before scorer implementation, freeze for each active SEMANTIC predicate whether Gate 0 scoring is:
- deterministic code;
- LLM judge;
- human adjudication;
- hybrid.

Do not let "semantic" itself choose an execution mechanism.

This is a scorer-design prerequisite, not a reason to reopen the experiment program.

---

# 11. What now passes and should be preserved

The following review-074 blockers are genuinely fixed:

## Generator architecture
PASS.
- layer-specific source parents;
- deterministic generated directory;
- old four-layer source dependency removed;
- 27 seed definitions implemented;
- campaign id present;
- counts generated programmatically.

## Old generated artifacts
PASS.
- old `PARENT-CLEAN.json` removed;
- old `VARIATION.json` removed.

## Identity drift
Largely PASS.
- registry `PILOT-2`;
- active set `ACTIVE-PILOT-2`;
- schema `SCHEMA-2`;
- oracle `ORACLE-2.0`;
- campaign `GATE0-C1`.

## Governing hashes
Direction PASS.
- hashes are now computed by the generator rather than copied forward.
- exact source hash verification was not independently recomputed in this review, but generation logic is now present and internally plausible.

## Layer specificity
PASS.
- the original cross-layer full-silence impossibility is fixed.

These are substantial improvements.

---

# 12. Required next pass

This should now be a **source-contract completion pass**, not another full rebuild.

### A. Fix source/control artifacts
1. rewrite `schema.md` to a genuinely clean SCHEMA-2;
2. add exact nested S4 projection/source map;
3. make S2/S3 source parents contain every projected value S4 needs;
4. add a valid S3 NOT_RENDERED clean parent/reference for isolated reason/basis seeds;
5. correct `G0-SEEDS.md` harmless-variation claim;
6. update `00-GATE0-MANIFEST.md` to GATE0-C1/layer-specific semantics.

### B. Fix branch seeds
7. rebuild S3 equality/reason/basis seeds from valid parents so each branch is isolated;
8. add a true S4 wrong-owner-group seed;
9. relabel existing S4 seeds by what they actually test.

### C. Fix manifest metadata
10. add `parent_type` per seed;
11. split governing vs JSON hash-method metadata;
12. hash the Gate 0 control-plane manifest.

### D. Regenerate
13. run generator;
14. run generator again;
15. confirm second run zero diff;
16. no manual generated-file edits.

Then return for review.

---

# 13. Current status

## Architecture
**CLOSED / VERIFIED**

## Experiment program
**SPECIFICATION FROZEN**

## Build-system path
**SUBSTANTIALLY FIXED**

## Execution source contract
**NOT YET ACCEPTED**

## Scorer
**NOT AUTHORIZED**

## Gate 0
**UNRUN**

## Doximity
**UNRUN**

## Phase 0
**UNTOUCHED**
