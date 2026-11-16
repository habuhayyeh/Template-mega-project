# DeepSeek review — record-ID-only direct-B follow-up

**Verdict:** READY TO RUN.

The experiment is a clean test of the only unresolved question: can direct-B preserve body/action evidence
with record-ID-only citations and no Stage A?

## What is right

- `source_records` only; no selectors.
- All supporting records must be cited.
- No state/chronology/provenance/action meaning from uncited records.
- Compound records may support multiple ACTION_VIEWs using the same IDs.
- If a sub-record distinction is needed, mark unresolved; no invented selector.
- CLINICAL_UNIT lane retained for body/nonproblem evidence.
- Two fresh runs; both must pass.
- No A rebuild, validator, stage or C.

## Audit

Record-ID fidelity is semantic support plus correct ID, not exact-string proof. That is the intended
tradeoff.

The test should explicitly check:

- cited ID exists;
- cited record materially supports the unit/action;
- no neighboring ID substitution;
- no uncited state/wording;
- body/action coverage;
- problem architecture/stance;
- burden below A→B.

## Decision

Retire A only if both R1 and R2 pass every blocking dimension.

If either fails, identify the exact preservation function A uniquely supplies. Do not rebuild A or add a
selector layer.

If record granularity is the cause, fix Scribe record boundaries; do not reintroduce copying.

No C/render changes. No acceptance or production change.
