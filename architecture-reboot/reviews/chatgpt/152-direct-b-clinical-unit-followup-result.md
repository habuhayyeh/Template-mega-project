# Review 152 — direct-B CLINICAL_UNIT follow-up result

## Verdict

**FOLLOW-UP FAILED. Do not retire A yet.**

Both direct-B-with-units runs fail blocking pointer fidelity.
Both also have body/action coverage defects.

The important result is structural:

> Exact substring reproduction from a long Scribe packet remains unreliable even when the model's clinical synthesis is otherwise good.

This failure is shared by:
- A;
- original direct-B;
- direct-B with CLINICAL_UNIT.

Therefore another A prompt patch is unlikely to solve the root problem.

## Run order

Signer clarified:
- first submitted block = U2;
- second submitted block = U1.

Same clean Scribe packet as prior comparator.

## U2

### Pointer fidelity — FAIL

Clear neighboring-record drift:
- baseline-comparator selector attached to T144, while the described collateral content is in T145.

Nonliteral selector:
- one problem-evidence selector for an ED-source event summary is not an exact substring of its cited source record.

Cross-record semantic leakage:
- one CLINICAL_UNIT chronology field imports Thursday chronology into a unit whose cited record supports only the Wednesday statement.

### Body coverage — FAIL

- prior seizure history preserved;
- supplements preserved;
- outside labs preserved;
- current exam content preserved but misclassified as neuro_history rather than exam;
- family seizure history not preserved.

### Actions — FAIL

Several ACTION_VIEW wordings import state from uncited neighboring/different records:
- CT wording adds completion information not present in its cited plan selector;
- cruise levetiracetam wording adds additional dosing from another source;
- ED levetiracetam recommendation wording adds discontinuation from another source.

Seizure precautions are omitted as a distinct action.

## U1

### Pointer fidelity — FAIL

Multiple neighboring-record errors:
- eye-fluttering evidence attached to the clinician question record rather than the answer record;
- no-shaking evidence attached to the clinician question record rather than the answer record;
- no-arm/leg-posturing evidence attached to the clinician question record rather than the answer record;
- baseline-comparator collateral description attached to T144 rather than T145.

Cross-record chronology leakage also appears in CLINICAL_UNIT chronology.

### Body coverage — FAIL

- family history preserved;
- supplements preserved;
- current exam preserved;
- outside labs preserved;
- explicit no-prior-seizure history omitted.

### Actions — FAIL

Material wording/state leakage:
- EEG wording adds timing from another source;
- MRI wording adds timing from another source;
- cruise levetiracetam wording merges later ED actions;
- neurology-consult wording upgrades a plan/request to completed consultation.

Current levetiracetam continuation/reassessment is omitted as its own action.

## What succeeded

Both runs:
- kept one PRIMARY event problem;
- did not promote baseline zoning-out spells to a separate problem;
- preserved diagnostic uncertainty;
- preserved compact body evidence much better than original direct-B;
- remained materially smaller than A->B.

Thus CLINICAL_UNIT solves much of the **representation-home** problem.

It does **not** solve pointer fidelity or action-state leakage.

## Architectural interpretation

The recurring failure pattern is now independent of whether A exists.

The unstable operation is:

> asking the LLM to copy an exact substring from a long packet while simultaneously performing clinical synthesis.

The Scribe packet already provides stable record IDs and source-local provenance boundaries.

Therefore the next architecture question should be:

> Does B need exact selectors at all, or should B cite stable Scribe record IDs and let downstream code mechanically dereference the complete record?

Potential simpler contract:

```text
CLINICAL_UNIT CU001
  unit_type=...
  source_records=T123 [or multiple explicit IDs]
  chronology=...
  problem_relation=...
```

```text
ACTION_VIEW AV001
  source_records=T123
  target=...
  wording=...
```

No selector copying.

Audit becomes:
- record ID exists;
- cited record semantically supports the unit/action;
- no neighboring record ID substitution.

C/renderer can mechanically dereference the full Scribe record by ID.

This removes the exact-substring reproduction task that has failed in A, direct-B, and direct-B+units.

## Important caution

Record-ID-only citation is a contract change.

Do not implement it yet without architecture review.

Need to decide:
1. whether whole-record dereference is safe given Scribe record width;
2. whether compound records require multiple explicit action targets rather than selectors;
3. whether any cases truly require sub-record selection;
4. whether current Scribe records are sufficiently coherent to serve as the smallest stable source unit.

## Current architecture status

- A cannot be retired from this follow-up.
- A is still not empirically justified as the solution to pointer fidelity.
- direct-B+CLINICAL_UNIT is closer to the desired minimal architecture but fails the current exact-selector contract.
- C remains blocked.

## Recommended next step

Architecture review of **record-ID-only source references** as the smallest targeted fix.

Do not:
- rebuild A;
- add validators;
- add another stage;
- add action-state enums;
- advance C.
