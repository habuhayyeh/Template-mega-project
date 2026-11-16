# DeepSeek adjudication — record-ID-only source references

**Verdict:** APPROVE the record-ID-only follow-up.

Use stable Scribe record IDs, one or more per unit/action. No selector copying.

## Why

Exact-substring reproduction has failed across:

- A;
- direct-B;
- direct-B with CLINICAL_UNIT.

The failure is not clinical synthesis. It is asking the model to copy exact text while synthesizing. The
same neighboring-record drift and cross-record leakage recur.

Record IDs are already stable and source-local. Let B cite records; let downstream dereference the full
record mechanically. Remove the copy task.

## Contract

```text
CLINICAL_UNIT CU001
  unit_type=current_event | baseline_comparator | neuro_history | medication_context |
            exam | workup | context
  source_records=T123[,T124...]
  chronology=<only when needed>
  problem_relation=<P handle or none>

ACTION_VIEW AV001
  source_records=T123[,T124...]
  target=<source-local target>
  wording=<source-qualified wording>
  owner=<P handle or nonproblem>
  unresolved=<only when material>
```

Rules:

- `source_records` mandatory; one or more exact IDs;
- no `selector`;
- no copied source text;
- cite every record that materially supports the unit/action;
- no uncited record may supply wording or state;
- no neighboring-record substitution;
- compound record: split by target/operation, each entry cites the same record ID;
- if a unit genuinely needs sub-record selection, mark `UNRESOLVED`; do not invent a selector.

## Audit

Development audit:

- every cited ID exists;
- the cited record text supports the unit/action;
- no ID points to a neighbor;
- no state/wording comes from an uncited record;
- compound actions are split by target.

This is semantic support audit, not exact-string proof. That is the tradeoff.

## Record width/coherence

Whole-record dereference is safe only if Scribe records are coherent enough. The clean packet appears to be.

If a record contains multiple assertions that need separate citation, fix **Scribe record granularity**, not
B selector copying. Do not recreate a selector layer.

## Test

Run direct-B + CLINICAL_UNIT + record-ID-only twice on the same clean packet.

Pass requires:

- body/nonproblem coverage preserved;
- actions preserved and split;
- no state from uncited records;
- pointer fidelity: every cited ID is the right record;
- problem architecture/stance preserved;
- burden materially below A→B.

If both pass, retire A. If not, identify the exact function A uniquely supplies.

No C. No validator. No new stage. No A rebuild.

No acceptance or production change.
