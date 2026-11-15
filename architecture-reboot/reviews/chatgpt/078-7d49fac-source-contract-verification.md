# ChatGPT review 078 — 7d49fac source-contract verification

## Verdict

> **PARTIAL PASS. SOURCE OWNERSHIP IMPROVED, BUT THE PROJECTION IS STILL NOT MECHANICALLY CONSTRUCTED. SCORER REMAINS BLOCKED.**

Commit `7d49fac` fixes several review-077 items:

- active semantic `S2-REP-01` now has an execution-mode entry;
- `ORACLE-2.0` is in the Gate 0 identity header;
- S2 parent now owns `relations`, `claim_relations`, `duplicate_groups`;
- S3 parent now owns `use` and `reuse`;
- S4 parent uses plural `claim_relations`.

Those are real improvements and should be preserved.

However, DeepSeek's claim that the Gate 0 body/pass criteria now use full within-layer silence is false in the live file, and the projection still has no mechanical construction path.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. PASS — source ownership fields now exist upstream

The previous projection-authoring defect is narrowed substantially.

Live S2 parent now contains:

- `relations`;
- `claim_relations`;
- `duplicate_groups`.

Live S3 parent now contains:

- `rendered`;
- `retained`;
- `use`;
- `reuse`.

Therefore those semantic values no longer first appear only in the S4 parent.

PASS as a source-ownership correction.

---

# 2. HARD BLOCKER — S4_INPUT_VIEW is still hand-authored, not mechanically projected

The architecture invariant is:

> `S4_INPUT_VIEW` is a mechanical projection assembled at the seam; the projection decides nothing.

The current generator does not assemble it.

`make_seeds.py`:

1. loads `S1_PARENT.json`, `S2_PARENT.json`, `S3_PARENT.json`, `S4_PARENT.json`;
2. copies each parent into generated output;
3. never constructs `s4_input_view` from S1/S2/S3/oracle/contract sources.

Therefore the current S4 input view can still drift independently from the upstream source parents even though the same values now happen to exist there.

This is the central distinction:

> **upstream availability is necessary, but not sufficient; projection provenance must be executable.**

### Required action

Move S4 input-view construction into deterministic generation.

Conceptually:

```text
S1 source parent
S2 source parent
S3 source parent
INGEST/oracle source
contract constants
        ↓
mechanical projection function
        ↓
S4_INPUT_VIEW
        +
S4 blueprint source
        ↓
generated S4 calibration parent
```

The exact file layout is implementation detail.

But no hand-authored semantic value may remain inside the generated projection.

---

# 3. HARD BLOCKER — exact nested source map is still missing

The schema's current group-level table is useful but insufficient for a mechanical scorer.

Example:

```text
from_s2.members -> S2 output
```

does not specify which exact S2 representation is selected or how the path is derived.

The map must freeze, for each projected destination:

- destination path/pattern;
- source owner;
- source path/pattern;
- selection/filter rule if conditional;
- required / optional / conditional;
- permitted mechanical transform.

This is especially necessary for:

- selected representation members;
- S2 relations relevant to those members;
- selected claim relation;
- duplicate/equivalence grouping;
- S3 selected representation;
- S3 rendered set;
- S3 use/reuse;
- retained ingest payload/provenance/temporality.

The source-path map should drive both projection generation and `S4-PROJ-01` scoring. Do not create a third manually duplicated mapping.

---

# 4. HARD BLOCKER — ingest projection is still only asserted

The S4 parent contains `from_ingest` payload/provenance/temporality.

The oracle contains the corresponding object text/provenance/temporality/status, which can serve as the experiment-local upstream substrate.

But the generator does not copy from the oracle; those values remain hand-authored in `S4_PARENT.json`.

Therefore source-first projection is still incomplete even after S2/S3 parent enrichment.

### Required action

For Gate 0, project `from_ingest` mechanically from the frozen oracle/substrate artifact.

---

# 5. BLOCKER — Gate 0 specificity text still contradicts FULL_SILENCE-WITHIN-LAYER

DeepSeek claimed:

> the body and pass criteria use the full within-layer silence set rather than "unrelated family".

The live manifest still says:

### Seed requirement 3
> it must not trigger predicates from unrelated families

### Procedure step 4
> expect no unrelated family to fire

### Pass criterion
> no seed trips an unrelated family

These are not equivalent to:

> every other ACTIVE predicate in the seed's calibration layer remains silent.

A scorer may over-fire another predicate in the same family/layer and still satisfy the old wording.

### Required action

Replace all three old clauses with one exact rule keyed by `parent_type` / layer.

---

# 6. BLOCKER — G0-S4-11 is stale after claim_relations pluralization

SCHEMA-2 and the S2/S4 parents now use:

`claim_relations`

plural.

But `make_seeds.py` still defines:

```python
def s4_11(a):
    a['s4_input_view']['from_s2']['claim_relation'] = 'COMPETING'
```

and the generated manifest records:

`/s4_input_view/from_s2/claim_relation`

singular.

This no longer tests a wrong semantic value in the valid S2-owned field. It injects a non-schema key.

That overlaps the schema/injected-field branch already represented by `G0-S4-07`.

Meanwhile `G0-SEEDS.md` still claims five distinct S4-PROJ branches:

- schema;
- invented member;
- wrong value;
- fabricated payload;
- wrong-owner relation.

The current fifth seed does not provide an independent wrong-value branch.

### Required action

Rebuild S4-11 against the valid plural `claim_relations` field using a structurally valid but source-inconsistent value, so it calibrates value fidelity rather than key membership.

Keep S4-09 as the true wrong-owner-group branch.

---

# 7. STILL BLOCKING — S3 reason/basis registry

DeepSeek correctly left this unresolved.

For mechanical `S3-CAND-01`, freeze the smallest experiment-local registry sufficient for Gate 0:

- allowed typed reason(s);
- which reason(s) require basis;
- valid basis reference target type(s);
- non-empty requirement;
- reference-existence rule.

Do not design the full production taxonomy.

The current mismatch remains:

- schema example: `NO_APPROVED_REPRESENTATION`;
- generator seeds: `NO_PROPOSAL`.

One authority must define the pilot vocabulary.

---

# 8. STILL BLOCKING — clean NOT_RENDERED calibration parent/reference

DeepSeek correctly left this unresolved.

The equality/reason/basis branches still overlap because all are derived from the rendered parent.

Add a clean NOT_RENDERED S3 calibration parent/reference that is valid under the reason registry and its required upstream references.

Important consequence:

> adding this artifact means the campaign may have **more than four clean parents while still having four parent types**.

Therefore update wording/count logic that currently assumes exactly "four layer-specific parents".

The manifest should distinguish:

- number of parent types;
- number of clean calibration parents;
- parent identity.

Do not overload `parent_type` to identify distinct S3 parent variants.

---

# 9. BLOCKER — HUMAN_REVIEW repetition rule is internally weak

The new text correctly rejects:

> one judge × three repeated passes

as sufficient calibration evidence.

But it then allows:

> three independent judges, **or one judge plus a mechanical pre-filter**.

A mechanical pre-filter cannot substitute for independent semantic judgment when the predicate itself is classified SEMANTIC.

If the mechanical pre-filter fully decides the seeded defect, then that branch is mechanical and should be separated/reclassified.

If semantic judgment remains necessary, Gate 0 needs an independent semantic-review rule.

### Required action

Choose one coherent policy.

For example:

- semantic Gate 0 = three independent blinded judgments, with a defined adjudication rule; or
- redesign the predicate into mechanical gate + one semantic adjudication where the mechanical portion truly captures the calibrated defect.

Do not count a deterministic pre-filter as two missing human judgments.

---

# 10. BLOCKER — S2-REP-01 HUMAN_REVIEW description is too weak for its predicate

Predicate:

> every approved representation is supported by source objects, including representations assembled from relations rather than quoted claims.

Current execution description:

> reviewer checks each representation's members trace to source objects and its support refs exist.

Existence/traceability is necessary but not sufficient.

A representation can cite real objects and real spans while asserting an unsupported relation among them.

### Required action

The HUMAN_REVIEW instruction must explicitly assess **semantic support of the representation by its members/relations**, not merely reference existence.

Mechanical reference-existence may be a pre-filter, but it is not the semantic decision.

---

# 11. Current next pass

The source-contract completion should now do:

1. freeze the experiment-local S3 reason/basis registry;
2. add the clean NOT_RENDERED S3 parent/reference;
3. isolate equality/reason/basis seeds;
4. freeze the exact S4 source-path map;
5. implement deterministic S4_INPUT_VIEW construction from S1/S2/S3/oracle/contracts;
6. remove hand-authored projection values from the source S4 blueprint path;
7. fix S4-11 to mutate valid plural `claim_relations`;
8. make Gate 0 specificity language uniformly FULL_SILENCE-WITHIN-LAYER;
9. resolve semantic HUMAN_REVIEW calibration policy;
10. strengthen S2-REP-01 human instruction to test semantic support;
11. update clean-parent counts/identities for the additional S3 parent;
12. regenerate twice and prove zero diff.

Then return for independent source-contract review.

Do not build the scorer in the same pass.

---

# 12. Current canonical state

- Architecture: **CLOSED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Build-system path: **PASS**
- Upstream S2/S3 projection source ownership: **PASS**
- Mechanical S4 projection construction: **FAIL / NOT IMPLEMENTED**
- S3 branch calibration isolation: **FAIL / PENDING**
- Gate 0 control contract: **NOT YET INTERNALLY CONSISTENT**
- Scorer: **NOT AUTHORIZED**
- Gate 0: **UNRUN**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**
