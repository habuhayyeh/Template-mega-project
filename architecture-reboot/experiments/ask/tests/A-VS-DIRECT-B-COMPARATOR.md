# A vs direct-B comparator

**Purpose:** decide whether Stage A earns its place when the Scribe packet is already clean and source-separated.

This comparator evaluates two architecture arms on the **same complete clean Scribe packet**.

## Arms

### Arm A — current architecture

```text
SCRIBE_EVIDENCE_V2_2
  -> 01-SOURCE-LOCAL-INGESTION.md
  -> 02-CLINICAL-SYNTHESIS.md
```

Run with:
- `01-SOURCE-LOCAL-INGESTION.md`;
- `02-CLINICAL-SYNTHESIS.md`;
- `02A-A-TO-B-CLINICAL-SYNTHESIS-TEST.md`.

Return both A and B handoffs unchanged.

### Arm B — direct clinical synthesis

```text
SCRIBE_EVIDENCE_V2_2
  -> 02B-DIRECT-CLINICAL-SYNTHESIS-TEST.md
```

Return the direct-B handoff unchanged.

## Execution control

Use:
- the exact same clean Scribe packet in both arms;
- separate fresh Doximity Ask conversations;
- no prior arm output in the other conversation;
- no comparator/oracle attached to Doximity;
- no C/compiler/render files.

Do not manually correct either output before comparison.

## Scoring dimensions

The comparator is architecture evidence, not a prose contest.

### 1. Source pointer fidelity — BLOCKING

Check every source citation/selector used to support clinically meaningful output.

Pass requires:
- cited record exists;
- selector belongs to that exact record;
- no neighboring-record drift;
- no paraphrase presented as selector;
- no merged selector across records.

A hidden pointer mismatch is a material failure.

### 2. Clinical coverage — BLOCKING

Both arms must preserve enough evidence for the signer’s target note, including:

- new recurrent seizure-like events;
- no prior seizure history;
- no known family seizure history;
- Wednesday initial event with chest/throat symptoms, limp/slump event, eye/eyelid findings, no clear limb shaking,
  amnesia/recovery;
- Thursday recurrent event/cluster with staring/unresponsiveness, eye/head findings, limited responsiveness between
  portions, inability to speak, no clear limb convulsions;
- reported ship medical evaluation/testing;
- reported levetiracetam treatment and absence of further reported events afterward;
- longstanding interruptible baseline staring spells as a **baseline comparator**, not automatically a separate
  problem;
- current Neurology stance: events not clearly epileptic; PNES/nonepileptic events suspected/considered but not
  established; epileptic seizure remains under evaluation;
- EEG and MRI needed;
- CT completed but result not available to Neurology / absent from supplied ED result;
- continue levetiracetam for now and reassess after EEG/MRI;
- favored inpatient completion of workup;
- LOC/seizure precautions and driving restriction counseling;
- vitamins/supplements with incomplete reconciliation;
- ED exam;
- outside reported lab results.

A clinically material hidden omission is a failure.

### 3. Action coverage and splitting — BLOCKING

Required action concepts:
- ship blood testing;
- additional ship testing;
- reported levetiracetam treatment;
- EEG;
- MRI brain;
- CT completion/status;
- current levetiracetam continuation/reassessment;
- inpatient vs outpatient evaluation with inpatient preference;
- seizure/LOC safety counseling;
- driving restriction counseling.

Pass requires:
- no material action omitted;
- no clinically distinct targets bundled such that downstream rendering loses the distinction;
- no action invented.

### 4. Provenance/attribution fidelity — BLOCKING

Check:
- patient vs collateral vs clinician;
- mother/fiance/paramedic brother mediation when material;
- outside testing remains reported;
- outside levetiracetam remains reported;
- CT result availability is not converted into a result claim.

Hidden source promotion is a failure.

### 5. Problem architecture — BLOCKING

Expected:
- one PRIMARY problem for current recurrent seizure-like events / unclear etiology;
- longstanding interruptible baseline staring is comparator/background evidence under the primary problem, **not**
  a separate problem unless independent assessment/management appears;
- no fabricated diagnosis;
- no unnecessary non-neurologic problem blocks.

### 6. Diagnostic stance — BLOCKING

Must preserve:
- not clearly epileptic;
- PNES/nonepileptic events suspected/considered;
- diagnosis not established from history alone;
- epileptic seizure remains under evaluation;
- baseline staring appears phenomenologically different/not clearly seizure.

No certainty upgrade.

### 7. Source-qualified management wording — BLOCKING

Must not invent:
- order from need/recommendation;
- performance from plan;
- `not_started`;
- `pending`;
- `unavailable` from silence;
- objective treatment from mediated report.

No decision/execution/response/result enum schema.

### 8. Hidden semantic error count

Count only meaning-changing errors likely to survive into the final note.

Do not count:
- numbering differences;
- harmless wording variation;
- minor formatting;
- obvious cosmetic omissions with no clinical consequence.

Lower is better.

### 9. Representation burden

Record:
- output line count;
- approximate character count;
- number of intermediate semantic/action records generated before B;
- duplicate restatement of source material.

This dimension is nonblocking by itself, but matters when clinical fidelity is equivalent.

## Decision rule

### Prefer direct-B and retire A if:

Direct-B:
- passes every blocking dimension;
- has no more hidden semantic errors than A->B;
- has equal or better action/provenance coverage;
- produces equivalent or better problem architecture/diagnostic stance;
- materially reduces intermediate representation burden.

### Keep A if:

A->B demonstrates a concrete fidelity advantage that direct-B cannot match, especially:
- better action coverage;
- better source/provenance fidelity;
- safer separation of clinically distinct source assertions;
- fewer hidden meaning-changing synthesis errors.

Do **not** keep A merely because it is more structured.

### Inconclusive

If each arm has different material failures, do not average them. Identify the exact responsibility causing the
difference and run the smallest targeted follow-up.

## Important

This test decides only whether A earns its place **for the clean Scribe contract**.

It does not authorize:
- C redesign;
- renderer changes;
- action-state enums;
- validators;
- extra stages.
