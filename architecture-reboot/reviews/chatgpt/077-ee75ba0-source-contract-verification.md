# ChatGPT review 077 — ee75ba0 source-contract verification

## Verdict

> **THREE MAJOR DIRECTIONS IMPROVED, BUT SOURCE CONTRACT STILL NOT ACCEPTED. SCORER REMAINS BLOCKED.**

DeepSeek commit `ee75ba0` genuinely improves:
- the broad SCHEMA-2 rewrite;
- the Gate 0 campaign header/source-first identity;
- scorer execution-mode explicitness.

But the live artifacts still contain several concrete source-contract contradictions.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. PASS — the major stale SCHEMA-2 defects from review 076 are fixed

The following are now corrected:

- `management_reference_spans` is a list in the S1 schema example;
- the malformed `claim_candidates (not claim_candidates)` remnant is gone;
- `S3-CAND-01`, `S4-PROJ-01`, and `S4-REP-01` now appear in the field→predicate map;
- the false claim that `S4-REP-01` is inactive is gone;
- `NOT_RENDERED` now requires a typed reason and conditional basis.

Preserve these changes.

---

# 2. BLOCKER — not every active SEMANTIC predicate has a frozen execution mode

DeepSeek said:

> execution mode frozen for every active semantic predicate.

That is not true in the live file.

Active SEMANTIC predicates are:

- `S1-CAND-01`;
- `S2-ADOPT-01`;
- `S2-REP-01`.

The execution-mode table defines:

- `S1-CAND-01` -> HUMAN_REVIEW;
- `S2-ADOPT-01` -> HUMAN_REVIEW;

but **omits `S2-REP-01`**.

The table also includes two mechanical predicates, which is harmless, but does not cure the omission.

### Required action

Freeze an explicit execution mode for `S2-REP-01`.

Do not authorize scorer implementation until every ACTIVE semantic predicate has one.

---

# 3. BLOCKER — Gate 0 specificity policy is still internally inconsistent

The manifest header now correctly says:

> `FULL_SILENCE-WITHIN-LAYER`: every active predicate of that layer must stay silent except the expected one.

But the body still says:

> it must not trigger predicates from unrelated families

and the procedure/pass criteria still use:

> no unrelated family to fire / no seed trips an unrelated family.

Those are weaker than full silence within layer.

A scorer could fire a second predicate in the same family/layer and still satisfy the old wording.

### Required action

Replace the old "unrelated family" language everywhere in the manifest with the exact campaign rule:

> for a seed, every other ACTIVE predicate in that seed's `parent_type` layer must remain silent.

The harness answer key may still group predicates by family for reporting, but family-level silence is not the acceptance rule.

---

# 4. BLOCKER — campaign identity is still incomplete in the governing Gate 0 manifest

The generated manifest and seed spec carry:

- `GATE0-C1`;
- `PILOT-2`;
- `ACTIVE-PILOT-2`;
- `SCHEMA-2`;
- `ORACLE-2.0`.

The Gate 0 header carries the first four but omits `ORACLE-2.0`.

This is small but material because the oracle is a governing scorer input and is separately hashed.

### Required action

Include `ORACLE-2.0` in the explicit campaign identity block.

---

# 5. BLOCKER — S3 reason/basis semantics are still not mechanically specified

The schema now says:

> `NOT_RENDERED` requires a typed `reason`. `basis` is required when the reason family depends on upstream state.

That is directionally correct, but `S3-CAND-01` is declared MECHANICAL.

A mechanical scorer therefore needs a closed source of truth for:

1. allowed reason values;
2. which reason values require basis;
3. what kind of ids each basis may reference;
4. whether basis must be non-empty;
5. whether each basis id must exist in the relevant upstream artifact.

Current source is inconsistent:

- schema example uses `NO_APPROVED_REPRESENTATION` with `basis: [S02]`;
- current seed generator uses `NO_PROPOSAL`;
- the canonical interface says basis references are to upstream state when the reason depends on upstream state.

A source span id such as `S02` may or may not be a valid basis for `NO_APPROVED_REPRESENTATION`; the contract does not define that.

### Required action

Before calibrating missing-reason/missing-basis branches, freeze the minimal reason/basis registry required by the pilot.

Do not invent a full production taxonomy. It may be experiment-local.

---

# 6. BLOCKER — the S4 projection map is still too coarse for a MECHANICAL S4-PROJ-01

The new schema has a useful group table:

- `from_s1`;
- `from_s3`;
- `from_s2`;
- `from_ingest`;
- `from_contracts`.

But review 075 required an exact nested source map so a scorer can prove that a projected value came from the correct source path.

Current table says, for example:

> `from_s2.members, relations, claim_relations, duplicate_groups` copied from S2 output.

It does not define exact source paths, destination paths, required/optional/conditional status, or permitted transforms.

For `S4-PROJ-01` to be mechanical, "trace to source" cannot rely on a human guessing which S2 field corresponds.

### Required action

Freeze an experiment-local path map, e.g. conceptually:

```text
destination path
source owner
source path
required / optional / conditional
permitted transform
```

The exact serialization is implementation detail.

---

# 7. BLOCKER — direct SCHEMA-2 vs S4 parent naming mismatch

SCHEMA-2 defines:

```text
from_s2.claim_relations
```

The live `S4_PARENT.json` contains:

```text
from_s2.claim_relation
```

singular.

That is already a schema-parent mismatch independent of the larger projection-authoring problem.

Choose one representation and use it consistently.

The canonical interface says:

> the selected representation's own claim relation where it has one.

A singular field may be appropriate for the selected representation, while S2 output may contain relations per problem. But the schema must explicitly define the projection transform if plural source state becomes singular selected state.

Do not let S4 silently choose that transformation.

---

# 8. STILL BLOCKING — S4 projection authors values

DeepSeek correctly left this unresolved.

Current S4 input contains S2-owned:

- `relations`;
- `claim_relation`;
- `duplicate_groups`;

that do not exist in the current S2 parent.

It also contains S3-owned:

- `use`;
- `reuse`;

that do not exist in the current S3 parent.

The projection therefore still creates values.

### Required action

Enrich the source parents only with fields needed by the campaign, then construct the S4 view mechanically from them.

---

# 9. STILL BLOCKING — S3-CAND-01 branch isolation

DeepSeek correctly left this unresolved.

A clean NOT_RENDERED parent/reference is still needed so:

- equality mismatch;
- missing reason;
- missing basis

can each be seeded while all other S3-CAND-01 clauses remain valid.

This must be coordinated with the reason/basis registry in section 5 above.

---

# 10. Gate 0 semantic repetition rule needs one clarification

The Gate 0 manifest says:

> semantic predicates are model- or human-judged; three runs; must detect 3/3.

The active semantic modes are now intended to be HUMAN_REVIEW.

Repeatedly asking the **same human reviewer** to judge the same static seed three times does not measure meaningful scorer variance.

Before scorer implementation, define what "three runs" means for HUMAN_REVIEW:

- three independent blinded reviewers; or
- one human adjudication with no repetition; or
- another explicitly justified calibration procedure.

Do not mechanically inherit the 3-run rule from model judging when the scorer is human.

This is a scorer-calibration contract question, not an architecture reopen.

---

# 11. Required next pass

The source-contract completion pass should now include:

1. add execution mode for active semantic `S2-REP-01`;
2. make Gate 0 specificity language uniformly FULL_SILENCE-WITHIN-LAYER;
3. add `ORACLE-2.0` to explicit campaign identity;
4. freeze minimal experiment-local S3 reason/basis registry;
5. add a valid clean NOT_RENDERED S3 parent/reference;
6. rebuild equality/reason/basis seeds from valid parents;
7. enrich S2/S3 source parents with only the projection fields needed;
8. freeze exact S4 source-path map;
9. generate S4_INPUT_VIEW mechanically;
10. resolve `claim_relation` vs `claim_relations` explicitly;
11. define the HUMAN_REVIEW Gate 0 repetition rule;
12. regenerate twice and prove zero diff.

Then return for independent review.

Do not build the scorer in the same pass.

---

# 12. Current state

- Architecture: **CLOSED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Build-system path: **PASS**
- SCHEMA-2 rewrite direction: **PASS WITH REMAINING CONTRACT DETAILS**
- Gate 0 campaign rewrite direction: **PASS WITH INTERNAL SPECIFICITY CONFLICT**
- Execution source contract: **NOT ACCEPTED**
- Scorer: **NOT AUTHORIZED**
- Gate 0: **UNRUN**
- Doximity: **UNRUN**
- Phase 0: **UNTOUCHED**
