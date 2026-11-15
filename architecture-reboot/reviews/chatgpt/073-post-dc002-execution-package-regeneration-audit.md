# ChatGPT review 073 — post-DC002 execution-package regeneration audit

## Verdict

> **REGENERATION IS NOT ACCEPTED. DO NOT BUILD THE SCORER YET.**

The package at `b96d4cf3` is a real regeneration attempt and correctly adds:
- `S3-CAND-01`;
- `S4-PROJ-01`;
- 18 generated seed artifacts for 16 listed active predicates;
- a DC-002-aware parent/oracle extension.

But the regenerated control plane is internally inconsistent with the verified DC-002 interface and, more importantly, the current Gate 0 seed architecture cannot satisfy its own full-silence calibration rule.

This is an execution-package defect, not an architecture reopen.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. Hard blocker — regenerated files still declare themselves stale

The following current files still say they are stale/pending regeneration:

- `AX-S1S2-D/schema.md`;
- `gate0/seeds/G0-SEEDS.md`;
- `gate0/00-GATE0-MANIFEST.md`;
- `gate0/seeds/generated/STALE.md`.

The generated package was regenerated, but the governing control-plane artifacts still tell an operator not to use it.

## Required correction

Do not merely delete the warnings first.

After the substantive defects below are corrected:
- remove the obsolete stale banners from current artifacts;
- delete/retire `generated/STALE.md`;
- update Gate 0 manifest status to an accurate current state such as:
  > REGENERATED / UNRUN / SCORER NOT BUILT.

Until then, the package remains stale.

---

# 2. Hard blocker — S1 schema/parent still carry pre-DC002 fields

The verified S1 interface says:

- `claim_candidates`;
- `management_reference_spans[]`;
- no adoption/current-status inference.

But current `schema.md` still begins with the old example:

- `candidate_claims`;
- `salience.managed_today: true`;

then appends a separate "DC-002 shape" paragraph saying the field is really `claim_candidates`.

That creates two schema authorities in one file.

The clean parent is also inconsistent:

- candidate 1 uses `claim_candidates`, good;
- salience still contains `managed_today: true`, not `management_reference_spans[]`;
- `s4_input_view.from_s1.salience` contains `management_reference_spans: [S03]`, even though that value does not exist in S1.

So the projection is introducing a value rather than mechanically projecting it.

The generator compounds this:
- `m_s1_05` still adds `candidate_claims`;
- it still adds `managed_today: False`.

That seed therefore contains extra schema defects beyond the intended candidacy mutation.

## Required correction

Rebuild the S1 test schema cleanly rather than appending a DC-002 addendum:

```text
problem candidate
  id
  subject
  anchors[]
  claim_candidates[]
  salience:
    ...
    management_reference_spans[]
```

Remove `managed_today` and `candidate_claims` from the post-DC002 schema, parent and generator.

The S4 projection must mechanically copy the S1 salience value; it may not manufacture it.

---

# 3. Hard blocker — `S4_INPUT_VIEW` is not the canonical projection

The verified S4 interface requires:

## From S1
- rendered problem-candidate identity;
- structured salience/order inputs.

## From S3
- rendered set;
- selected representation per rendered problem;
- retained use;
- problem-use/reuse.

## From S2
- selected representation member ids;
- relations among those members;
- selected claim relation where present;
- duplicate/equivalence grouping required for COVERED.

## From I3/I4
- retained object payload;
- provenance;
- temporality.

## From contracts
- section;
- style;
- operator definitions;
- ordering contract.

The current clean parent's `s4_input_view` is incomplete:

- `from_s3` has only `selected_rep` + `retained`; no rendered set or use/reuse map;
- `from_ingest.payload` is only object → span id, not payload + provenance + temporality;
- `from_contracts` lacks style and contains a claimed `ORDER-1` even though ordering is still `PENDING_DEPENDENCY`;
- the schema freezes only the five top-level groups, not the allowed nested fields/source ownership needed to score `S4-PROJ-01`.

## Required correction

Freeze an exact experiment-local nested `S4_INPUT_VIEW` schema and source-path map.

For every projected field define:
- destination path;
- source owner/interface;
- source path;
- whether optional/conditional;
- dependency if any.

Then build the clean projection mechanically from the parent upstream artifacts.

Do **not** invent `ORDER-1`.

Either:
- freeze a real test ordering contract/oracle, which would change the ordering dependency state; or
- explicitly keep ordering contract/order correctness outside this Gate 0 parent and mark that portion PENDING_DEPENDENCY.

Do not use a fictional contract id to make the shape look complete.

---

# 4. Critical calibration defect — one full parent makes full-silence specificity impossible

The Gate 0 manifest says seeds are layer-specific:
- S1_OUTPUT;
- S2_OUTPUT;
- S3_OUTPUT;
- S4_BLUEPRINT.

But `make_seeds.py` loads one full S1→S4 parent and mutates that whole artifact for every seed.

That creates legitimate downstream secondary findings.

## Concrete example A — G0-S1-05

Mutation:
> append C2 as a new S1 candidate.

Expected:
> only `S1-CAND-01` fires.

But S3 still contains an outcome only for C1.

Therefore a correct scorer must also fire:
> `S3-CAND-01` — C2 has no candidate outcome.

Under the current FULL_SILENCE policy, a correct scorer fails calibration.

## Concrete example B — G0-S3-02

Mutation:
> S3 selected_rep R1 → R-999.

Expected:
> `S3-SEL-01` only.

But S4 unit U1 still carries R1.

Therefore a correct scorer must also fire:
> `S4-REP-01`.

Again, full silence is impossible.

## Required correction

Return to the intended layer-specific calibration model.

Preferred:
- S1 seeds receive an S1_OUTPUT parent only;
- S2 seeds receive S2_OUTPUT + required frozen references only;
- S3 seeds receive S3_OUTPUT + the upstream references needed by that predicate;
- S4 projection/blueprint seeds receive S4 input/output + required frozen references only.

Record `parent_type` in the generated manifest.

An alternative is to define causally expected secondary firings per full-pipeline seed, but that weakens the original one-defect/one-owner calibration design and makes specificity harder to interpret. Do not switch to that model casually.

The layer-specific approach is preferred.

---

# 5. Compound DC-002 predicates are under-calibrated

## S3-CAND-01

The predicate currently asserts all of:

- coverage;
- exactly one outcome per candidate;
- rendered-set equality;
- unknown candidate id rejection;
- typed reason for NOT_RENDERED;
- basis refs when reason family depends on upstream state.

Current Gate 0 has only:

> G0-S3-05 — remove C1 outcome.

That tests only **coverage**.

It does not calibrate the scorer for the other branches.

### Required branch calibration

Add branch seeds, or explicitly split the predicate before scorer construction.

At minimum calibrate:

1. missing outcome / coverage;
2. duplicate outcomes / exclusivity;
3. unknown candidate id;
4. NOT_RENDERED without required typed reason;
5. NOT_RENDERED reason family missing required basis refs;
6. rendered-outcome set mismatch.

A second clean candidate-outcome parent may be needed for a valid NOT_RENDERED baseline. That is acceptable.

## S4-PROJ-01

The predicate asserts:

- frozen projection schema;
- allowed source-interface ownership/traceability;
- no unselected/nonrequired state;
- no newly introduced semantic value.

Current seed:

> add top-level `adoption: true` to `s4_input_view`.

That tests only the easiest top-level schema violation.

### Required branch calibration

At minimum seed:

1. field outside projection schema;
2. field/value under the wrong source-owner group;
3. schema-valid but unselected/nonrequired state projected;
4. schema-valid but invented semantic relation/value not present in source owner;
5. retained payload/provenance/temporality mismatch where applicable.

If one broad predicate remains, Gate 0 must demonstrate that the scorer implements all material branches, not just one.

The existing S1-AUTH multiple-seed logic already follows this principle.

---

# 6. Active-set and campaign identity are inconsistent

Current files use several identities at once:

- `predicates.md`: **PILOT-2** active set wording;
- `parent.json`: `predicate_set: "PILOT-1"`;
- generator: `PREDICATE_SET = "PILOT-2"`;
- generated manifest:
  - predicate registry id `PILOT-2`;
  - active set `PILOT-ACTIVE-1`.

A regenerated campaign must have one frozen identity.

## Required correction

Freeze explicit identifiers for:
- predicate registry;
- active predicate set;
- Gate 0 campaign;
- schema version;
- oracle version.

Use them consistently in:
- parent(s);
- oracle(s);
- seed spec;
- generator;
- generated manifest.

If registry id and version are intentionally separate concepts, document that semantics; do not leave numbers that merely look contradictory.

---

# 7. Governing interface/program identity is missing from the generated manifest

Review 072 explicitly required regenerated artifacts to record the new governing interface/program identities.

The current `MANIFEST.json` hashes:

- predicates;
- schema;
- G0-SEEDS;
- generator.

It does **not** freeze:

- `CONSENSUS_SUBMODULE_INTERFACES_v1.md` / canonical interface identity;
- frozen architecture experiment program;
- relevant AX-S1S2-D spec;
- Gate 0 manifest/control-plane version.

A `dc: DC-002` string inside parent/oracle is not enough to establish which exact canonical text governed the campaign.

## Required correction

Add governing hashes/commit ids for at least:

- canonical submodule interface document;
- frozen architecture experiment program;
- AX-S1S2-D experiment spec;
- predicate registry;
- schema;
- Gate 0 seed specification;
- generator;
- parent/oracle.

This makes campaign identity reproducible and auditable.

---

# 8. Field→predicate map is stale after regeneration

`schema.md` says its map covers active pilot predicates, but the table still omits the newly active:

- `S3-CAND-01`;
- `S4-PROJ-01`;

and it also omits `S4-REP-01` while that predicate is now listed active.

## Required correction

The active field→predicate map must include **all active predicates** or explicitly state a narrower scope.

For the current claimed 16-active-predicate pilot, all 16 must be represented.

---

# 9. G0-SEEDS contains contradictory current-state text

The file now says:

> 18 seed artifacts exist · 16 active predicates.

That count is plausible.

But later it says:

> `S4-REP-01` ... excluded because no active predicate scores it

while `S4-REP-01` is explicitly in the active set and has `G0-S4-05`.

It also lists `S4-REP-01` among:
> Predicates with seeds but not active in this pilot

which contradicts its own active map immediately above.

## Required correction

Reconcile:
- active predicate list;
- seed map;
- NOT_IN_PILOT list;
- pending list;
- artifact counts.

Do not rely on arithmetic written by hand when the generator can derive it.

Prefer generated summary counts in the manifest, then make the prose cite those counts rather than duplicate them independently.

---

# 10. Parent/oracle scope must be explicit

A reduced Gate 0 parent does not need to prove every canonical S4 feature if it is only calibrating a defined predicate subset.

That is acceptable.

But then it must be labeled as a **layer-specific/reduced calibration parent**, not silently treated as evidence that a full canonical S4 blueprint is complete.

If the clean S4 parent intentionally omits:
- member roles;
- rhetorical class;
- reuse accounting;
- completeness status;
- other non-active fields;

state that these are outside this Gate 0 parent's calibration scope.

Gate 0 calibration evidence must not later be cited as validation of those omitted S4 dimensions.

---

# 11. What is correct and should be preserved

Keep:

- 16-predicate post-DC002 pilot concept;
- addition of `S3-CAND-01`;
- addition of `S4-PROJ-01`;
- CASE-01 oracle v2 direction;
- generated canonical-JSON artifact hashes;
- harmless id-renaming variation control;
- full-silence specificity **within a layer-specific parent scope**;
- no scorer yet;
- no Gate 0 run;
- no Doximity;
- Phase 0 untouched.

The regeneration should be repaired, not abandoned.

---

# 12. Required next pass

DeepSeek should perform an **execution-package remediation only**:

1. rebuild `schema.md` as a single post-DC002 schema;
2. create true layer-specific clean calibration parents/references;
3. mechanically derive the S4 input projection from valid upstream state;
4. freeze exact nested S4 projection/source-owner schema;
5. add branch seeds for compound DC-002 predicates;
6. reconcile campaign/registry/active-set identities;
7. add governing interface/program/spec hashes;
8. reconcile seed/current-state counts;
9. regenerate all seed artifacts and manifest from the corrected generator;
10. remove stale markers only after successful regeneration;
11. re-fetch and verify all governing artifacts.

Return:
- exact changed-file list;
- number of clean parents;
- active predicate count;
- seed count by predicate;
- pending predicates;
- governing hashes/ids.

Then ChatGPT will independently review the regenerated package again.

**Do not build the scorer yet.**
