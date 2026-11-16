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

Run **each arm twice**:

- Arm A1 — current A->B in a fresh Ask conversation;
- Arm A2 — current A->B in a second fresh Ask conversation;
- Arm B1 — direct-B in a fresh Ask conversation;
- Arm B2 — direct-B in a second fresh Ask conversation.

Use:
- the exact same clean Scribe packet in all four runs;
- a fresh Doximity Ask conversation for every run;
- identical files/prompt within each arm;
- no prior run output in any later conversation;
- no comparator/oracle attached to Doximity;
- no C/compiler/render files.

Do not manually correct any output before comparison.

The two runs per arm are the reproducibility axis. Do not average away material failures.

## Audit normalization before scoring

The two arms use different internal reference shapes. Normalize them to the same canonical evidence layer before
comparing fidelity.

### Arm A mapping

Arm A B-output may cite A span/action IDs.

For every clinically meaningful B reference:

```text
B reference
  -> A SPAN/ACTION_SPAN ID
  -> A source_record
  -> A selector/action_phrase
  -> exact Scribe record
```

Score the final Scribe linkage, not the presence of the intermediate A ID.

Do **not** penalize Arm A merely for using an intermediate handle.

Penalize Arm A only when:
- the A handle is missing;
- the A handle points to the wrong source record;
- selector/action phrase does not belong to that record;
- B cites an A handle whose source meaning does not support the B claim/action;
- a clinically material source item was lost before B.

### Direct-B mapping

For every clinically meaningful direct-B reference:

```text
B reference
  -> source_record
  -> exact selector
  -> exact Scribe record
```

Apply the same source-support standard.

### Canonical action-concept normalization

Compare action coverage by **clinical action concept**, not generated IDs or exact wording.

Normalize each arm to these concepts before scoring:

- ship blood testing;
- additional ship testing;
- ship levetiracetam treatment;
- EEG evaluation;
- MRI brain evaluation;
- CT head completion/result-availability status;
- current levetiracetam continuation with reassessment after EEG/MRI;
- inpatient-vs-outpatient evaluation with inpatient preference;
- seizure/LOC safety counseling;
- driving restriction counseling.

Equivalent source-faithful wording counts as the same action concept.

Do not reward or penalize an arm for:
- ACTION_SPAN vs ACTION_VIEW numbering;
- one lexical target label versus an equivalent one;
- harmless ordering differences.

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

**Both** direct-B runs:
- pass every blocking dimension;
- each has a hidden semantic-error count less than or equal to the **better A->B run**:
  `direct_errors <= min(A1_errors, A2_errors)`;
- have equal or better normalized action/provenance coverage than both A->B runs;
- produce equivalent or better problem architecture/diagnostic stance than both A->B runs;
- materially reduce intermediate representation burden.

A single excellent direct-B run is insufficient if the second has a material failure.

### Keep A if:

Both A->B runs pass the blocking dimensions and demonstrate a reproducible fidelity advantage that direct-B cannot
match, especially:
- better normalized action coverage;
- better source/provenance linkage;
- safer separation of clinically distinct source assertions;
- fewer hidden meaning-changing synthesis errors.

Do **not** keep A merely because it is more structured.

### Inconclusive

The result is **inconclusive** if:
- one run within an arm passes and the other has a material blocking failure;
- each arm has different material failures;
- direct-B is better on burden but worse on any blocking fidelity dimension;
- A is better on one material dimension but worse on another.

Do not average material failures into a score.

When inconclusive, identify the exact responsibility causing the difference and run the smallest targeted follow-up.

## Important

This test decides only whether A earns its place **for the clean Scribe contract**.

It does not authorize:
- C redesign;
- renderer changes;
- action-state enums;
- validators;
- extra stages.
