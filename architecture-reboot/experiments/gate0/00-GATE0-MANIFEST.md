# Gate 0 — scorer calibration manifest

**Campaign:** `GATE0-C1` · **registry** `PILOT-2` · **active set** `ACTIVE-PILOT-2` · **schema** `SCHEMA-2` · **oracle** `ORACLE-2.0`

**Model:** **five clean calibration parents across four parent types.** `S1_OUTPUT`
(`S1_CASE01_CLEAN`), `S2_OUTPUT` (`S2_CASE01_CLEAN`), `S3_OUTPUT` (`S3_CASE01_RENDERED_CLEAN`,
`S3_CASE01_NOT_RENDERED_CLEAN`), `S4_BLUEPRINT` (`S4_CASE01_CLEAN`). A seed mutates one field of its
own parent. Specificity is `FULL_SILENCE-WITHIN-LAYER`: for every seed, every other ACTIVE predicate
whose `parent_type` equals the seed's `parent_type` must be silent. A four-layer artifact is not a
valid parent.

**Generation:** source-first. `python architecture-reboot/tools/make_seeds.py` clears
`seeds/generated/`, rewrites parents, seeds and the manifest, and recomputes governing hashes. A second
run must produce **zero diff**; a run that does not is a build failure, not a warning. The build also
rejects a seed that is a no-op copy of its parent, or that differs at more than one path. The manifest
mutation record is the checked parent→seed diff, not a hand-written claim.

**Status: AUTHORED / UNRUN.** No scorer exists yet; this defines what one must do to earn the right to
score architecture experiments.

---

## 1. The rule

Before any experiment's result is treated as acceptance evidence, the scorer that will judge it must demonstrate, on a known-bad case, that it fails when it should.

A scorer that passes everything is indistinguishable from a working system. Gate 0 is what separates those two states, and it is a **prerequisite, not an experiment**.

## 2. Scope

Gate 0 calibrates the predicates that the campaigns in scope will use. It is scoped to a **predicate layer**, not to the whole scorer:

Run count is set **solely** by each predicate's `mode` in `AX-S1S2-D/predicates.md`. The table below is organisational; its layer column is descriptive and does not set counts.

| family | layer | used by |
|---|---|---|
| S1 authority (candidacy, adoption leakage, claim leakage) | semantic | AX-S1S2-D |
| S2 representation (source grounding, approval safety) | semantic | AX-S1S2-D, AX-SHARED |
| S3 selection (approved-only, no synthesis, inclusion blocking) | semantic | AX-S1S2-D |
| S4 blueprint (inclusion/claim immutability, order, typing) | mechanical + semantic | AX-S1S2-D, AX-S4 |
| generic fidelity (fabricated content, duplication, omission) | mechanical | all |
| voice / section style | mechanical | all |

A calibration covers only the predicate layers exercised by the campaigns it gates. Running Gate 0 for layers nobody will score is waste.

## 2a. Parent identity

`parent_type` names the layer. It does not identify a parent variant. The campaign counts are:

- **parent types:** 4 — `S1_OUTPUT`, `S2_OUTPUT`, `S3_OUTPUT`, `S4_BLUEPRINT`;
- **clean calibration parents:** 5;
- **S3 identities:** `S3_CASE01_RENDERED_CLEAN` and `S3_CASE01_NOT_RENDERED_CLEAN`.

`seeds/generated/MANIFEST.json` keys `clean_parents` by `parent_id`, not by `parent_type`. Every seed
record carries both `parent_id` and `parent_type`. A second S3 parent is therefore an identity, not a
fifth type.

## 3. Two modes, two procedures

**Mechanical predicates** are deterministic. One run. A failure to fire is a scorer bug, not variance.

**Semantic predicates** are model- or human-judged. Three runs. Calibration passes only if the seeded defect is detected in **all three**; two of three is a calibration failure, because a scorer that detects a planted defect two times in three cannot be trusted to detect a real one once.

## 4. Seed requirements

Every seed is a **mutation of a clean parent**, never a bespoke bad case:

- the clean parent is a real artifact from the historical corpus (or a hand-built case marked as such);
- the mutation changes exactly one thing;
- the seed records what the mutation is, where it is, and which predicate must fire.

A seed that mutates two things cannot tell you which predicate noticed.

Requirements per seed:

1. it must be detected by at least one named predicate;
2. it must be attributed to the **correct owning submodule**;
3. it must leave **every other ACTIVE predicate in its own `parent_type` layer silent** — a scorer that fires another predicate in the same layer is as useless as one that fires nothing;
4. the clean parent must produce **zero** findings.

Predicates of a different layer are not part of this check: a layer-specific artifact contains only
that layer's output, so an S3 seed cannot calibrate an S1 predicate.

## 4a. Finding record

A finding is not prose. Every finding carries:

```yaml
predicate_id: S2-TEMP-01      # exact id, never a layer label
owner: S2
artifact: G0-S2-03.json
path: /s2/adjudication/0/temporal
oracle_ref: objects.O03.temporal
expected: "June–November"
observed: "now"
status: FIRED | SILENT | UNDECIDABLE
```

A scorer that reports only `S1`/`S2` cannot pass Gate 0: attribution is checked against `predicate_id`, not the layer.

## 5. Procedure

```text
For each parent type under test:
  1. run the scorer on every clean parent of that type -> expect zero findings
  2. run the scorer on each seed of that type          -> expect the named predicate to fire
  3. check attribution                                 -> expect the owning submodule
  4. check specificity                                 -> every other ACTIVE predicate in the seed's parent_type is SILENT
  5. semantic modes: repeat 2-4 three times            -> expect detection 3/3
```

Steps 1 and 4 are the ones usually skipped, and they are the ones that make a pass meaningful.

## 6. Pass criteria

Gate 0 passes for a parent type when:

- every seed of that type is detected, 3/3 for semantic modes;
- every seed is attributed to the owning submodule;
- for every seed, **every other ACTIVE predicate in the seed's `parent_type` is silent**;
- every clean parent of that type scores zero.

It fails if any of those is false, including "detected but misattributed" — a finding attached to the wrong module sends the fix to the wrong place, which is worse than no finding. A single extra finding on another active predicate in the same layer is also a failure, not a warning.

## 7. Recalibration triggers

- a predicate definition changes;
- the scorer's model, prompt, or version changes;
- a new predicate layer is added;
- a real defect is discovered that the scorer did not flag — that becomes a new seed, and Gate 0 is re-run for that layer.

The last trigger matters most: every miss in production should become a seed, so the calibration corpus grows from experience.

## 7a. Scorer blindness

The scorer receives **artifact + case oracle + predicate registry only**.

Harness-only, never passed to the scorer: the seed manifest, the seed id, the expected predicate, mutation metadata, and the specificity answer key. Keeping the answer key in the same directory as the artifacts is not a control; it is a convention. The control is that the harness selects the artifact and holds the answer.

## 8. What Gate 0 does not prove

- It does not prove the scorer detects defects nobody seeded.
- It does not calibrate reasoning about clinical correctness, only detection of the seeded categories.
- It does not gate Phase 0, and does not depend on it.

## 9. Artifacts

- `AX-S1S2-D/parents/S1_PARENT.json`, `S2_PARENT.json`, `S3_PARENT.json`,
  `S3_PARENT_NOT_RENDERED.json`, `S4_PARENT.json` — clean source parents.
- `seeds/G0-SEEDS.md` — the seed corpus and expected outcomes.
- `seeds/generated/MANIFEST.json` — the authoritative inventory, keyed by `parent_id`, with counts and
  hashes.
- Per-run records: scorer version, predicate set version, control-plane version, case ids, findings,
  verdict.

Runs are recorded like experiment runs: frozen inputs, immutable outputs, one verdict per parent type.

## 10. Ownership

Authored by the engineer, reviewed by the reviewer, run by whoever operates the scorer. The reviewer's check is that the seeds actually test what the manifest claims — a seed that cannot fail proves nothing.
