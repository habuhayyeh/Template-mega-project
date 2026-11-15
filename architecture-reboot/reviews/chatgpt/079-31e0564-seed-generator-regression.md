# ChatGPT review 079 — 31e0564 verification: seed generator regression

## Verdict

> **HARD FAIL. THE SOURCE-CONTRACT PASS INTRODUCED A BUILD REGRESSION: S1/S2/S3 GENERATED SEEDS ARE CLEAN PARENTS, NOT MUTATIONS. SCORER REMAINS BLOCKED.**

Commit `31e0564` correctly moves S4_INPUT_VIEW construction into code, but the refactor introduced a decisive generator bug.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. HARD BLOCKER — mutation function runs only for S4 seeds

Current `make_seeds.py` loop:

```python
for pfile, sid, pred, fn, path, before, after in SEEDS:
    art = copy.deepcopy(parents[pfile])
    if pfile == 'S4_PARENT.json':
        art = {... constructed S4 parent ...}
        fn(art)
    name = sid + '.json'
    ...
```

Because `fn(art)` is indented inside the S4-only branch:

- S4 seeds are mutated;
- S1 seeds are not;
- S2 seeds are not;
- S3 seeds are not.

This is not theoretical. The committed generated artifacts prove it.

## Example — S1

`PARENT-S1_PARENT.json` and `G0-S1-01.json` are content-identical.

The seed manifest claims:

```text
/s1/candidates/0/adopted
<absent> -> true
```

but the generated seed contains no `adopted` field.

Its artifact hash is also identical to the clean-parent hash.

## Example — S2

`PARENT-S2_PARENT.json` and `G0-S2-01.json` are content-identical.

The manifest claims `support_refs` changed to `[]`, but the seed still contains:

```json
"support_refs": ["S02"]
```

Again, seed hash = parent hash.

## Example — S3

`PARENT-S3_PARENT.json` and `G0-S3-08.json` are content-identical.

The manifest claims:

```text
RENDERED -> NOT_RENDERED
```

but the seed remains `RENDERED`.

Again, seed hash = parent hash.

### Consequence

Gate 0 currently has mutation metadata describing defects that do **not exist in the generated artifacts**.

A scorer calibrated against this corpus would be impossible to interpret:
- silence on these seeds would be correct for the artifact but appear as scorer failure;
- any finding would be a false positive.

This is a build-system failure, not a scorer issue.

---

# 2. "Second run zero diff" is not evidence of correctness

DeepSeek reported second-run zero diff.

That remains useful only for determinism.

It does **not** establish semantic correctness of the generated package.

The current bug is perfectly deterministic.

Therefore the build gate needs two separate checks:

1. **idempotence** — second run zero diff;
2. **mutation realization** — each generated seed actually differs from its declared parent exactly as specified.

Do not conflate them again.

---

# 3. Required generator invariant — manifest mutation must equal artifact diff

For every generated seed, the build should mechanically verify:

- artifact differs from the referenced clean parent;
- the actual diff is exactly the declared mutation path(s);
- `before` equals the parent value/absence;
- `after` equals the seed value;
- no undeclared diff exists;
- seed canonical hash differs from parent hash for every non-noop seed.

If any fails, generation must fail.

This turns the seed manifest from descriptive metadata into a checked build product.

---

# 4. Required immediate fix

Move the mutation call outside the S4-only construction branch:

Conceptually:

```python
art = construct_base_artifact_for_parent(pfile)
fn(art)
verify_declared_mutation(parent, art, mutation_spec)
write_seed(...)
```

Do not merely fix indentation.

Add the mutation-realization assertion so the same class of bug cannot recur after another refactor.

---

# 5. S4 projection construction — directionally PASS, acceptance still pending

The structural move in `31e0564` is correct:

- hand-authored `s4_input_view` removed from source S4 parent;
- `build_view()` constructs the view from S1/S2/S3/oracle/contracts;
- `from_ingest` now derives from oracle object records.

Preserve this.

However, acceptance still depends on the previously identified remaining contract work:

- exact nested source→destination path map;
- relevance/filter semantics for projected relation collections;
- reason/basis registry;
- clean NOT_RENDERED S3 parent;
- FULL_SILENCE-WITHIN-LAYER wording cleanup;
- HUMAN_REVIEW calibration policy;
- S2-REP-01 semantic-support instruction.

The build regression is prior to all of those.

---

# 6. G0-S4-11 — branch is improved but naming/meaning should be explicit

The stale singular `claim_relation` mutation is gone.

Current S4-11 mutates valid field:

```text
duplicate_groups: [] -> [[O03,O04]]
```

This is a valid-field wrong-value / fabricated semantic-state seed.

PASS directionally.

Call it that explicitly; do not call it "wrong-owner relation," because the field remains under the correct S2 owner group. The wrong-owner-group branch is S4-09.

---

# 7. Manifest integrity concern

The generated manifest currently lists mutation metadata for S1/S2/S3 seeds even when the actual artifact did not mutate.

That demonstrates that manifest truth is not currently derived/verified from the generated bytes.

Required:
- generate mutation record from checked diff, or
- mechanically verify declared record against parent/seed before writing manifest.

The manifest must never be able to assert a mutation that the artifact does not contain.

---

# 8. Next pass order

Do not continue source-contract refinements on top of a broken generator.

Next pass:

1. fix seed mutation execution for all parent types;
2. add build-time mutation-realization verification;
3. regenerate;
4. prove every S1/S2/S3/S4 seed differs from its parent exactly at declared mutation(s);
5. regenerate second time and prove zero diff;
6. return counts + parent/seed hash non-equality checks + any intentionally multi-diff seeds (expected none under current rule).

Only then continue the remaining source-contract blockers from review 078.

---

# 9. Current state

- Architecture: **CLOSED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- S4 projection construction direction: **IMPROVED / NOT YET FULLY ACCEPTED**
- Seed generator: **FAIL — S1/S2/S3 mutation execution broken**
- Gate 0 calibration corpus: **INVALID**
- Source contract: **NOT ACCEPTED**
- Scorer: **NOT AUTHORIZED**
- Gate 0: **UNRUN**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**
