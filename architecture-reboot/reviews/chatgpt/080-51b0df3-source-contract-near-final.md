# ChatGPT review 080 — 51b0df3 source-contract near-final verification

## Verdict

> **BUILD INTEGRITY RESTORED. SOURCE CONTRACT VERY CLOSE, BUT THREE SCORER-CONTRACT BLOCKERS REMAIN. SCORER NOT YET AUTHORIZED.**

Commit `51b0df3` fixes the hard generator regression from review 079 and materially resolves the structural blockers from review 078.

This is the strongest execution package so far.

The remaining issues are narrow, but they matter because they determine what the scorer is actually allowed to trust.

No scorer yet.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. PASS — generator integrity is restored

The review-079 control-flow regression is fixed.

Verified directly:

- `G0-S1-01` contains the planted `adopted: true`;
- `G0-S2-01` contains `support_refs: []`;
- `G0-S3-08` differs from the clean NOT_RENDERED parent only by `rendered[]`;
- `G0-S3-09` differs only by reason;
- `G0-S3-10` differs only by basis.

The generator now:

- applies the mutation after clean-base construction for every layer;
- rejects no-op seeds;
- computes structural parent→seed diff;
- rejects more than one changed path;
- records the checked path/before/after in the manifest;
- produces non-parent hashes for non-noop seeds.

This is the correct direction.

Important retained lesson:

> second-run zero diff proves determinism; checked parent→seed diff proves mutation realization.

Both are required.

---

# 2. PASS — S3 branch isolation is now structurally clean

The new:

`S3_CASE01_NOT_RENDERED_CLEAN`

gives a valid structural reference for the S3-CAND branches.

The three formerly overlapping seeds now isolate:

- rendered-set equality;
- missing reason;
- missing basis.

The explicit caveat is also correct:

> the NOT_RENDERED parent is structurally clean for S3-CAND-01, not a clinical assertion that C1 should actually be suppressed.

PASS.

---

# 3. PASS — REASON-1 is sufficient for Gate 0 structural calibration

The experiment-local registry now freezes:

- allowed outcome values;
- allowed reason values;
- reason→basis requirement;
- basis target type;
- minimum count;
- uniqueness;
- target existence;
- missing-reason behavior.

It explicitly does **not** claim to be a production taxonomy.

That is the correct scope.

PASS for Gate 0.

---

# 4. PASS — parent identity is now distinct from parent type

Five clean parents across four parent types is now represented honestly.

Each parent has:

- unique `parent_id`;
- separate `parent_type`.

The S3 rendered and NOT_RENDERED parents can therefore coexist without overloading layer identity.

PASS.

---

# 5. PASS — Gate 0 specificity language is now coherent

The live Gate 0 source now consistently uses:

> `FULL_SILENCE-WITHIN-LAYER`

The old "unrelated family" wording is gone from:

- seed requirement;
- procedure;
- pass criteria.

PASS.

---

# 6. PASS — S4 view is now constructed rather than hand-authored

The hand-authored `s4_input_view` is removed from the S4 source parent.

The generator constructs the view from:

- S1 parent;
- S2 parent;
- S3 parent;
- oracle/ingest source;
- contract constants.

This resolves the earlier "source values happen to exist upstream but projection still authors them" defect.

PASS in architecture direction.

---

# 7. BLOCKER — PROJECTION_MAP is not yet the executable authority it claims to be

SCHEMA-2 says:

> The map is executable: `make_seeds.py` reads this block, applies one `op` per destination...

The generator does read the map, but it does **not execute or verify most of the map's semantic metadata**.

For each rule it checks only that these strings are non-empty:

- `owner`;
- `source`;
- `source_path`;
- `condition`;
- `required`;
- `transform`.

The actual projection logic comes from hard-coded Python functions in `OPS`.

Example:

```text
PROJECTION_MAP says:
source = S2_PARENT.json
source_path = /s2/relations[i]
condition = from in M and to in M
transform = filter and copy

Generator actually does:
OPS["s2_relations"] -> hard-coded Python filtering
```

If someone changes the declared `source_path`, `owner`, `condition`, or `transform` while leaving `op: s2_relations`, the build can still pass and generate the old behavior.

Therefore there are currently **two authorities**:

1. the written projection map;
2. the hard-coded semantics of `OPS`.

They can drift.

That violates the purpose of freezing an exact source→destination map.

### Required correction

Choose one source of truth.

Two acceptable designs:

### A. Map-driven execution
Implement a generic projection interpreter sufficient for these 14 rules.

or

### B. Frozen op registry with exact metadata binding
For each op, define the only valid:

- owner;
- source;
- source_path;
- condition;
- required;
- transform;
- destination.

At build time, compare the map rule **exactly** against that registered op contract and fail on any mismatch.

Option B is likely smaller for Gate 0.

The current "field exists and is non-empty" check is insufficient.

---

# 8. BLOCKER — HUMAN_REVIEW calibration policy remains unresolved

Review 078 challenged this:

> three independent judges, **or one judge plus a mechanical pre-filter**

The live predicate file still contains exactly that rule.

A mechanical pre-filter cannot substitute for missing independent semantic judgments if the predicate itself is classified `SEMANTIC / HUMAN_REVIEW`.

If the pre-filter completely determines the seeded defect, then that tested branch is mechanical and should be represented as such.

If semantic judgment remains necessary, the calibration evidence must contain an actual semantic judgment.

### Why this matters

Gate 0 manifest still says semantic modes require 3/3.

But predicates.md defines "three runs" in a way that can mean:

> one human judgment + deterministic preprocessing

which is not 3 independent semantic judgments.

The two documents therefore still do not define one coherent acceptance rule.

### Required correction

Freeze one policy.

My preference for this pilot:

> **SEMANTIC / HUMAN_REVIEW Gate 0 requires three independent blinded human judgments, all three detecting the seeded defect and all three satisfying within-layer specificity.**

If that is impractical, explicitly change the Gate 0 requirement rather than calling a mechanical pre-filter a semantic repetition.

---

# 9. BLOCKER — S2-REP-01 execution instruction still does not test its stated semantic predicate

Predicate definition:

> every approved representation is supported by source objects, including representations assembled from relations rather than quoted claims.

That is a semantic claim.

Current HUMAN_REVIEW instruction:

> reviewer checks each representation's members trace to source objects and its support refs exist.

That checks **reference existence/traceability**, not whether the representation is semantically supported.

A representation can contain:

- real object ids;
- real support refs;

and still combine them into an unsupported claim/relationship.

### Gate 0 seed problem

Current `G0-S2-01` simply empties `support_refs`.

That is an obvious structural defect.

It does not calibrate the reviewer's ability to detect:

> all references exist, but the approved representation is semantically unsupported by those objects/relations.

Therefore Gate 0 currently calibrates only the easy mechanical edge of a predicate labeled semantic.

### Required correction

At minimum:

1. rewrite the HUMAN_REVIEW instruction to require semantic support, not only reference existence;
2. add a semantic-support seed for `S2-REP-01` where:
   - members exist;
   - support refs exist;
   - schema is valid;
   - but the representation's claimed/member relation is not supported by the source/oracle.

If SCHEMA-2 cannot express such a seeded semantic misrepresentation observably, then the predicate is not currently calibratable and must be:
- narrowed to the mechanically observable property; or
- held pending a representation schema that exposes the semantic claim.

Do not call the broader semantic predicate calibrated by an empty-list seed.

---

# 10. One naming correction

`G0-SEEDS.md` still summarizes the S4-PROJ branches as including:

> wrong-owner relation

But current `G0-S4-11` mutates:

```text
duplicate_groups: [] -> [[O03,O04]]
```

under the correct `from_s2` owner group.

That is a **valid-field fabricated/wrong value**, not wrong-owner.

The true wrong-owner-group seed is `G0-S4-09`:

> S3-owned selected_rep under from_s2.

Update the human summary so the branch descriptions match the executable corpus.

This is not independently scorer-blocking, but it should be corrected in the same pass.

---

# 11. Source-contract acceptance target

I would accept the execution source contract for scorer construction after exactly these items are resolved:

1. bind PROJECTION_MAP metadata to executable op semantics so map and code cannot drift;
2. freeze one coherent HUMAN_REVIEW Gate 0 repetition policy;
3. make S2-REP-01 calibration genuinely test semantic support, or narrow/pending the predicate honestly;
4. correct the S4-PROJ branch summary wording;
5. regenerate twice;
6. rerun generator integrity checks.

No architecture change is required for items 1, 2, or 4.

Item 3 may require only a better seed/instruction; if the current representation schema cannot expose the semantic property, stop and classify that prerequisite honestly rather than inventing a scorer.

---

# 12. Current state

- Architecture: **CLOSED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Seed generator integrity: **PASS**
- S3 branch isolation: **PASS**
- S3 reason registry: **PASS**
- Gate 0 specificity policy: **PASS**
- S4 projection construction: **PASS DIRECTIONALLY**
- Projection-map/code single-authority guarantee: **FAIL**
- HUMAN_REVIEW calibration contract: **UNRESOLVED**
- S2-REP-01 semantic calibration: **INADEQUATE**
- Execution source contract: **NOT YET ACCEPTED**
- Scorer: **NOT AUTHORIZED**
- Gate 0: **UNRUN**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**
