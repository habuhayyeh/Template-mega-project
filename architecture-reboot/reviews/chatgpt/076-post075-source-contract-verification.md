# ChatGPT review 076 — post-075 source-contract completion verification

## Verdict

> **PARTIAL PASS. SOURCE CONTRACT STILL NOT ACCEPTED. SCORER REMAINS BLOCKED.**

The live branch has advanced beyond review 075 to DeepSeek commit `fe3c63f`.

DeepSeek accurately described that commit as partial. Four review-075 classes are materially improved:

- true wrong-owner S4 projection seed now exists;
- harmless variation now exists;
- every generated seed record carries `parent_type`;
- governing-source vs canonical-JSON hash methods are split, and the Gate 0 manifest is now hashed.

Those fixes should be preserved.

However, the execution source contract still has four blocking families.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. BLOCKER — SCHEMA-2 is still internally invalid

The current live `schema.md` still contains review-075 failures.

## 1a. Wrong type remains

Current example:

```yaml
management_reference_spans: true
```

The verified interface requires a span-id list such as:

```yaml
management_reference_spans: [S03]
```

The source S1 parent already uses the correct list form.

Therefore the schema example is now inconsistent with its own canonical parent.

## 1b. Malformed remnant remains

Current text still says:

> Each candidate carries `claim_candidates` (not `claim_candidates`)

This is self-contradictory residue and cannot remain in a clean SCHEMA-2 source contract.

## 1c. Active field→predicate map is still stale

The map still omits active:
- `S3-CAND-01`;
- `S4-PROJ-01`;
- `S4-REP-01`.

Worse, the prose still says:

> `S4-REP-01` ... not scored yet — no pilot case produces their condition

but the live seed corpus contains:

`G0-S4-05 -> S4-REP-01`.

That is direct source-source contradiction.

## 1d. S3 schema contradicts DC-002

Current schema says:

> `No reason field is required.`

But the verified DC-002 interface requires:
- `NOT_RENDERED` + typed reason;
- basis refs where the reason family depends on upstream state.

The schema therefore cannot currently define the very `S3-CAND-01` branches being calibrated.

### Required action

Rewrite `schema.md` as one clean SCHEMA-2 authority.

Do not patch isolated lines again.

---

# 2. BLOCKER — S4_INPUT_VIEW is still not mechanically derivable

The live `S4_PARENT.json` still contains source-owned state that does not exist in the committed source parents.

## S2-owned projection values that first appear in S4

Live S4 view contains:

```json
from_s2.relations
from_s2.claim_relation
from_s2.duplicate_groups
```

Live `S2_PARENT.json` contains none of those fields.

## S3-owned projection values that first appear in S4

Live S4 view contains:

```json
from_s3.use
from_s3.reuse
```

Live `S3_PARENT.json` contains neither.

Therefore the current projection still authors semantic state rather than copying it.

This remains a direct violation of DC-002:

> S4_INPUT_VIEW is a mechanically projected interface view and creates no new semantic decisions.

### Required action

Choose explicitly per field:

1. **needed by this calibration campaign**
   - add it to the correct source-owned parent/schema;
   - freeze source path -> destination path.

2. **not needed by this campaign**
   - remove it from the S4 calibration parent/view.

Then generate S4_INPUT_VIEW mechanically from the source parents rather than hand-authoring it.

---

# 3. BLOCKER — S3-CAND-01 branch isolation remains invalid

DeepSeek correctly acknowledged this in the channel.

Current seeds still use the all-rendered S3 parent.

## G0-S3-08

Changes only:

`RENDERED -> NOT_RENDERED`

but does not provide a valid NOT_RENDERED reason/basis state.

Therefore it is not a pure rendered-set-equality mutation.

## G0-S3-09

Appends another C1 outcome lacking reason.

This violates both:
- exclusivity;
- missing reason.

## G0-S3-10

Replaces the rendered outcome with NOT_RENDERED + empty basis while `rendered[]` still contains C1.

This violates:
- rendered-set equality;
- missing/invalid basis.

### Required construction

Add a second clean S3 calibration parent/reference, e.g. conceptually:

```text
S3_PARENT_RENDERED
S3_PARENT_NOT_RENDERED
```

The NOT_RENDERED parent must itself satisfy all S3-CAND-01 clauses:
- exactly one outcome;
- candidate known;
- absent from rendered set;
- valid typed reason;
- valid basis when required;
- object accounting otherwise valid.

Then derive:
- missing reason;
- missing basis;
- equality mismatch

as isolated single-defect mutations from the appropriate clean parent.

A seed name per branch is not enough. The parent must make every non-target branch valid.

---

# 4. BLOCKER — Gate 0 control-plane manifest still describes the old calibration model

The live `00-GATE0-MANIFEST.md` still does not freeze the campaign actually being generated.

Missing or stale:

- campaign id `GATE0-C1`;
- registry `PILOT-2`;
- active set `ACTIVE-PILOT-2`;
- `SCHEMA-2`;
- `ORACLE-2.0`;
- four layer-specific clean-parent model;
- `FULL_SILENCE-WITHIN-LAYER`;
- source-first generation rule;
- generated-directory no-hand-edit rule;
- second-run zero-diff requirement;
- harmless-variation control;
- distinction between scorer inputs and harness-only answer key.

Current specificity still says:

> no unrelated family to fire

The implemented calibration policy is stricter/more exact:

> every other active predicate in the same calibrated layer remains silent.

### Required action

Rewrite `00-GATE0-MANIFEST.md` to describe the actual GATE0-C1 campaign before scorer design.

The file is now hashed by the generator, which is good; therefore its current stale semantics are especially important because changing it correctly will intentionally change campaign identity.

---

# 5. RESOLVED — true S4 wrong-owner calibration

`G0-S4-09` now places:

```text
S3-owned selected_rep
under from_s2
```

That is a genuine wrong-owner-group mutation.

PASS.

---

# 6. RESOLVED — harmless variation exists

The generator now emits:

`VARIATION.json`

from the S3 parent with consistent id renaming and:

> expect: zero findings.

PASS as a calibration-control artifact.

A later scorer review should still verify that the renaming preserves every required cross-reference, but the source/generator mismatch from review 075 is fixed.

---

# 7. RESOLVED — seed manifest parent_type

Every visible generated seed record carries:

`parent_type`.

PASS.

When the second S3 NOT_RENDERED parent is added, `parent_type` alone may not distinguish the two S3 parent variants. Add an explicit parent id/name rather than overloading parent_type.

---

# 8. RESOLVED — hash-method separation, with one follow-on consequence

The live generator now records:

- governing source = SHA-256 over file bytes;
- generated artifact = SHA-256 over canonical JSON.

It also hashes `00-GATE0-MANIFEST.md`.

PASS.

Consequence:

Once schema / S3 parent / Gate 0 manifest are corrected, regenerate and accept the new campaign hashes. The current hashes are correctly describing a still-invalid source contract; they are not acceptance evidence.

---

# 9. One additional source-contract clarification before scorer design

Review 075 asked to freeze how active SEMANTIC predicates are actually judged.

The live Gate 0 manifest still says:

> semantic predicates are model- or human-judged.

That is not enough for implementation.

Before scorer construction, each active semantic predicate must name its execution mode, e.g.:

- deterministic code;
- LLM judge;
- human adjudication;
- hybrid.

This does **not** reopen the experiment program.

It is part of the scorer/source contract.

---

# 10. Required next pass — source contract completion only

DeepSeek should now do exactly four source-level tasks:

1. **rewrite SCHEMA-2 cleanly**;
2. **make every S4 projected field mechanically source-owned** and freeze exact nested source mapping;
3. **add a valid S3 NOT_RENDERED clean parent/reference** and rebuild the three affected CAND seeds for branch isolation;
4. **rewrite the Gate 0 control-plane manifest** to the actual GATE0-C1 layer-specific campaign and freeze semantic-predicate execution modes or a referenced scorer-mode table.

Then:

5. regenerate;
6. regenerate again;
7. prove zero diff on second run;
8. return exact changed source files + generated counts/hashes.

Do not build the scorer in the same pass.

---

# 11. Current canonical state

- Architecture: **CLOSED / VERIFIED**
- DC-001: **APPLIED / VERIFIED**
- DC-002: **APPLIED / VERIFIED**
- Experiment program: **SPECIFICATION FROZEN / UNRUN**
- Build-system path: **PASS**
- Execution source contract: **NOT ACCEPTED**
- Scorer: **NOT AUTHORIZED**
- Gate 0: **UNRUN**
- Doximity architecture experiments: **UNRUN**
- Phase 0: **UNTOUCHED**

The next task is source-contract completion, not architecture work.
