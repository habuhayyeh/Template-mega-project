# ChatGPT review 083 — scorer/harness implementation verification

## Verdict

> **PARTIAL PASS. SCORER/HARNESS DESIGN IS SOUND, BUT GATE 0 EXECUTION IS NOT YET AUTHORIZED.**

DeepSeek commit `1aaf4be` implements the review-082 input boundary correctly in broad structure:

- target artifact is separated from read-only dependency context;
- the pure scorer does not read files or the seed manifest;
- answer-key comparison is harness-owned;
- 13 mechanical + 3 HUMAN_REVIEW predicates match the current 16-active-predicate split;
- S3 predicates can inspect S1/S2 dependency context;
- S4 projection checking can inspect upstream context;
- HUMAN_REVIEW packets are blinded to seed id / expected predicate / mutation metadata;
- dependency hashes are checked before context is supplied;
- no Gate 0 acceptance run was performed.

Those are real passes.

However, six implementation defects can still make a future Gate 0 result stale, misclassified, or non-reproducible.

No Gate 0 run yet.
No Doximity.
No Phase 0.

---

# 1. BLOCKER — load_campaign does not verify the current governing sources against MANIFEST.json

`load_campaign()` currently:

1. loads `MANIFEST.json`;
2. loads the current oracle;
3. reads current `REASON_REGISTRY` and `PROJECTION_MAP` from `schema.md`;
4. verifies clean-parent artifact hashes.

It does **not** recompute the manifest's `governing_hashes` against the current source files.

Therefore this state is possible:

- `schema.md`, `predicates.md`, Gate 0 manifest, oracle, or another governing source changes;
- generated `MANIFEST.json` remains stale;
- harness loads the new source content plus the old campaign manifest;
- acceptance proceeds under a mixed campaign identity.

That defeats the source-first hash contract.

### Required correction

Before packet generation or acceptance execution, the harness must:

- recompute every governing-source hash listed in `MANIFEST.json`;
- fail on any mismatch;
- verify the frozen campaign identities:
  - `GATE0-C1`;
  - `PILOT-2`;
  - `ACTIVE-PILOT-2`;
  - `SCHEMA-2`;
  - `ORACLE-2.0`;
  - `FULL_SILENCE-WITHIN-LAYER`;
- verify the runtime scorer registry's active predicate ids match the accepted active set.

Do not merely copy the manifest's governing hashes into EVIDENCE.json.

A stale manifest must be an `InputIntegrityError`.

---

# 2. BLOCKER — scorer/projection.py reintroduces a second projection authority

Review 080 closed a specific defect:

> the written PROJECTION_MAP and executable projection semantics must not drift.

The generator now enforces this with `OP_CONTRACTS`.

But `scorer/projection.py` does not execute or validate the PROJECTION_MAP rule metadata.

It reads the map only for:

`contracts`

and then reconstructs S4_INPUT_VIEW using independently hard-coded Python logic.

It ignores the map's declared:

- `rules`;
- `dst`;
- `source`;
- `source_path`;
- `condition`;
- `required`;
- `transform`;
- `expands`.

So the scorer now has a second projection implementation that can drift from the accepted map even while the seed generator remains correct.

### Required correction

Use one shared projection-contract implementation for generator and scorer, or give the scorer the same exact metadata-binding protection.

Minimal acceptable pattern:

- extract the accepted op contracts + projection executor into a pure shared module;
- generator and scorer both call it;
- no file or answer-key access in the shared projection evaluator;
- negative test: modifying a map source path/condition/transform without matching executable contract must fail before scoring.

Do not merely add a test that today's two outputs happen to match.

---

# 3. BLOCKER — clean-parent FIRED findings are mislabeled INCOMPLETE

Current harness code:

```python
if row['kind'] == 'clean':
    verdict = 'PASS' if all(f['status'] == SILENT for f in result['findings']) else 'INCOMPLETE'
```

This conflates two very different states.

A clean parent with:

- one `FIRED` finding = **FAIL**;
- no FIRED but one or more `UNDECIDABLE` findings = **INCOMPLETE**;
- all SILENT = **PASS**.

Gate 0 explicitly requires every clean parent to produce zero findings.

A false positive on a clean parent is not missing evidence.

### Required correction

Implement exactly:

```text
any FIRED        -> FAIL
else any UNDECIDABLE -> INCOMPLETE
else all SILENT  -> PASS
```

Add tests for all three branches.

---

# 4. BLOCKER — HUMAN_REVIEW judgments are not bound to their predicate

`load_judgments()` requires a `predicate_id`.

But `aggregate_human()` groups judgments by `packet_id` and never checks:

`judgment.predicate_id == finding.predicate_id == packet.predicate.id`

Therefore a judgment record can carry the correct packet id but the wrong predicate id and still count toward 3/3.

That is a judgment-binding defect.

### Required correction

Before aggregation:

- packet id must identify a known packet in this run;
- judgment `predicate_id` must equal the packet's predicate id;
- packet predicate id must equal the finding predicate id;
- judge ids must remain unique for the three accepted judgments;
- unexpected/stale packet judgments should fail input validation rather than silently influence or disappear from acceptance evidence.

Add negative tests for predicate mismatch and unknown/stale packet id.

This does not solve real-world identity verification of a human judge; that remains an operational control. It does ensure the records are internally bound correctly.

---

# 5. BLOCKER — evidence discards the dependency hashes actually used

`dependency_context()` correctly returns:

```python
context, pinned
```

But `run()` discards `pinned`.

The per-artifact evidence record therefore does not state which exact dependency artifacts/hashes were supplied to the scorer.

This weakens the central review-082 invariant:

> target artifact + hash-pinned seed-independent dependency context.

### Required correction

Each evidence record should include the dependency context actually used:

```text
dependency_context:
  - parent_id
  - parent_type
  - artifact hash
```

Also strengthen implementation fingerprinting.

Current EVIDENCE records only:

`scorer/scorer.py` hash.

But scorer behavior also depends materially on:

- `scorer/registry.py`;
- `scorer/projection.py`;
- `tools/gate0_harness.py`.

Record those hashes individually or define a reproducible composite scorer/harness fingerprint.

The evidence must be sufficient to reconstruct exactly what code produced the verdict.

---

# 6. BLOCKER — harness does not produce the Gate 0 verdict defined by the manifest

The Gate 0 contract defines acceptance **per parent type**, then the campaign must know whether all required parent types passed.

Current harness writes:

- one verdict per clean parent / seed artifact;
- no parent-type aggregation;
- no campaign-level verdict.

So even after all human judgments exist, the harness cannot yet produce the acceptance object the Gate 0 protocol describes.

### Required correction

Add deterministic aggregation:

## Per parent_type

`FAIL` if:
- any clean parent FAILS;
- any seed FAILS specificity/detection/attribution.

`INCOMPLETE` if:
- no FAIL exists, but any required artifact is INCOMPLETE / missing required human evidence.

`PASS` only if:
- every clean parent is PASS;
- every seed in that parent type is PASS.

## Campaign

`FAIL` if any required parent_type FAILS.

`INCOMPLETE` if none FAIL but any is INCOMPLETE.

`PASS` only if every required parent_type is PASS.

Write both:

- `parent_type_verdicts`;
- `campaign_verdict`;

into `EVIDENCE.json`.

Add synthetic tests for PASS, FAIL, and INCOMPLETE aggregation.

---

# 7. PASS — scorer blindness is meaningfully implemented

The pure scorer module accepts arguments only and does not perform file I/O.

The test that patches `builtins.open` to raise while calling `score()` is a useful negative control.

The test that adds answer-key-shaped metadata to `rules` and verifies findings do not change is also useful.

Preserve both.

One clarification:

> these prove the pure scorer does not read files or react to an added `expected` key.

They do not replace the harness-level source-integrity checks required above.

---

# 8. PASS — review-082 dependency boundary is implemented correctly in principle

The manifest now defines dependency context by target type.

The harness:

- selects clean upstream parents;
- checks dependency parent type;
- checks dependency canonical hash;
- supplies the context separately from the target artifact.

This is the right model.

Preserve it.

---

# 9. PASS — HUMAN_REVIEW packet structure is directionally correct

The S2-REP-01 packet now includes:

- target S2 artifact;
- clean S1 problem/claim context;
- source/oracle material;
- predicate assertion and instructions;

without seed id / expected predicate / mutation metadata.

That closes the review-082 claim-context defect.

Preserve this structure.

---

# 10. No additional architecture/source-contract work is requested

The six blockers above are implementation/harness defects.

Do **not** reopen:

- S1/S2/S3/S4 ownership;
- DC-002;
- Gate 0 seed design;
- the 28-seed source corpus;
- the HUMAN_REVIEW policy;
- Doximity architecture.

Only patch scorer/harness integrity and aggregation.

---

# 11. Required next pass

DeepSeek should:

1. verify current governing hashes/identities at harness load;
2. remove the second projection authority by sharing/binding projection execution;
3. fix clean-parent PASS/FAIL/INCOMPLETE semantics;
4. bind human judgments to packet + predicate and reject stale/mismatched records;
5. record dependency hashes and full scorer/harness implementation fingerprints in evidence;
6. implement parent-type + campaign aggregation;
7. add focused tests for all six;
8. run the synthetic/unit test suite;
9. **do not run Gate 0 acceptance**;
10. return scorer/harness diff + test results for review.

No need for another source-contract rewrite unless the implementation exposes a new actual contradiction.

---

# 12. Current canonical state

- Architecture: **CLOSED / VERIFIED**
- DC-002: **APPLIED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Execution source contract: **ACCEPTED with review-082 scorer-input correction**
- Seed/generator package: **PASS**
- Scorer core separation/blindness: **PASS DIRECTIONALLY**
- Scorer/harness implementation: **REVISE**
- Gate 0 execution: **NOT AUTHORIZED YET**
- Gate 0: **UNRUN**
- Three-human-review operational prerequisite: **OUTSTANDING**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**
