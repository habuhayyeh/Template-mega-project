# DeepSeek review — A2 coverage/reproducibility failure

**Reviewed:** review 145, two A2 wording-only runs.
**Status:** architecture review. No implementation.

## Verdict

This is a **contract/execution problem inside A2**, not an architecture change.

D-049 holds: both runs obeyed wording-only A2, no state normalization. The failure is selection and
source-local decomposition: the model does not reproducibly enumerate all action identities in compound
or distributed records.

Do not freeze A2. Do not run B1 yet.

## Narrowest fix

Strengthen A2’s enumeration contract. Do not add a stage or a validator.

### 1. Record-by-record traversal

Process source records in packet order. For every record containing action-like wording:

- enumerate every distinct source-local action target/operation in that record;
- do not skip a record because another action is more salient;
- do not select a subset of a compound list.

This directly addresses:

- P1.045 CT only vs CT + labs + UA;
- P1.018 CBC only vs CBC/CMP/lactate/EKG/electrolytes;
- P1.055 discontinuation omitted;
- P1.044 precautions omitted;
- T258 MRI plan omitted.

### 2. Compound-list expansion

When a shared action verb governs a coordinate/list of targets, distribute the action over each distinct
target:

```text
Plan: CT head, basic labs, urinalysis
-> CT head span
-> basic labs span
-> urinalysis span
```

```text
CBC, CMP, lactate, EKG, electrolytes were performed
-> one span per distinct test/procedure
```

Do not select the first or most familiar item.

If the source treats a panel as one named indivisible test, one span may be correct. Otherwise split.

### 3. Decision-target rule

For a decision, the target is the object being decided, not the evidence/condition.

Example:

```text
decision tomorrow after EEG/MRI whether to continue or stop [medication]
```

- target = medication continuation/stop decision;
- condition = after EEG/MRI;
- EEG/MRI are not the target.

This fixes the T258 misidentification.

### 4. Replace `material` as the inclusion gate

“Material” is causing variable selection. Use an objective inclusion list:

Include explicit actions involving:

- diagnosis/workup;
- medication;
- consultation;
- admission/disposition;
- precautions;
- driving/activity/water/heights counseling or restrictions;
- other management that changes neurologic care.

Exclude only a closed list:

- transport/arrival;
- administrative/logistics;
- social coordination;
- conversational repair;
- pure documentation.

If uncertain whether an action is clinical, include it and mark `unresolved`. Do not omit.

### 5. Optional per-record disposition

If omissions persist after 1–4, add a narrow `RECORD_ACTION_DISPOSITION` line only for records that
contain action-like wording:

```text
RECORD_ACTION_DISPOSITION P1.045 spans=A001,A002,A003 reason=compound workup
RECORD_ACTION_DISPOSITION T005 spans=none reason=transport logistics
```

Do not create a per-line map of the whole packet. This is a coverage guard for action-bearing records, not
global atomicization.

## Test

### Small probe first

Create one synthetic packet with:

- a compound test list;
- a medication decision conditioned on a test;
- a logistics action;
- a safety counseling action.

Expected: all clinical actions split; logistics excluded; decision target correct.

### Full packet

Run A2 wording-only twice on the frozen packet. Score the existing A2 oracle, plus reproducibility:

- same set of material action identities across runs;
- same compound splits;
- no omission of precautions/disposition/counseling;
- no normalized state.

Allow different IDs/order. Do not allow different action sets.

Only after both runs pass should B1 run.

## What not to do

- do not pick the better run;
- do not union runs manually;
- do not add a validator;
- do not add a stage;
- do not move action identity into B1.

No acceptance, production change or Phase 0.
