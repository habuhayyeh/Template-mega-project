# Review 153 — record-ID-only direct-B follow-up result

## Verdict

**R1 FAIL. R2 FAIL. Do not retire A.**

Record-ID-only references successfully remove the exact-substring copying failure, but they do **not** make direct-B reliable enough to replace A.

The remaining failure is now localized:

> Direct-B does not reliably perform complete source coverage / source-record selection while also doing clinical synthesis.

This is different from the prior selector-copying defect.

## Runs

Same clean SCRIBE_EVIDENCE_V2_2 packet.

- R1 = first record-ID-only run
- R2 = second record-ID-only run

## R1

### Record-ID fidelity — FAIL

Examples:
- PROBLEM counterevidence includes T042, which is the clinician question; the actual negative answer is T043.
- PROBLEM counterevidence includes T084, which is the clinician question; the relevant arm/leg answer is in T085.
- Several category units cite clinician-question records alongside answer records even though the question itself does not materially support the represented evidence.

### No uncited state — FAIL

Three CLINICAL_UNITs contain semantic content without any source_records:
- CU001 current-event chronology;
- CU002 current-event chronology;
- CU007 workup.

These are direct contract failures.

### Body/nonproblem coverage — FAIL

Preserved:
- baseline comparator;
- family seizure history;
- supplement context;
- exam.

Lost or insufficient:
- explicit no-prior-seizure history;
- workup unit lacks source IDs.

### Actions — FAIL

Major neurologic actions are present, but coverage is incomplete:
- seizure precautions omitted;
- ED basic labs/UA/neurology-consult trajectory is incomplete as action coverage;
- ship testing is not represented as an action trajectory.

### Problem architecture / stance — PASS

- one PRIMARY problem;
- no separate baseline-staring problem;
- uncertainty and PNES-vs-epileptic distinction preserved.

## R2

### Record-ID fidelity — FAIL

Examples:
- PROBLEM counterevidence includes T106, which is a clinician question; T107 contains the reported result.
- baseline comparator unit cites question records such as T144/T147 while omitting the key collateral description record T145 and answer T148.
- neuro-history unit includes T121, a question, rather than preserving the explicit patient no-prior-seizure evidence from P2.001.

### No uncited state — FAIL

CU001 and CU002 contain detailed chronology but no source_records.

Action leakage:
- AV004 says “drip/load” while cited records support the cruise drip and continuation discussion, not an ED load.
- AV005 says “shared decision” but does not cite T115, the source record that explicitly states shared decision.

### Body/nonproblem coverage — FAIL

Preserved:
- baseline comparator;
- family seizure history;
- supplement context;
- outside workup.

Lost:
- explicit no-prior-seizure history;
- current neurologic exam.

### Actions — FAIL

Major management is present, but clinically material action coverage is incomplete:
- seizure precautions omitted;
- ED basic labs/UA omitted;
- neurology consultation omitted;
- supplemental review omitted.

### Problem architecture / stance — PASS

- one PRIMARY problem;
- baseline comparator remains nonproblem;
- diagnostic uncertainty preserved.

## Representation burden — PASS

Both record-ID-only runs are materially smaller than A->B.

Observed counts:
- R1: 8 CLINICAL_UNITs, 8 ACTION_VIEWs.
- R2: 8 CLINICAL_UNITs, 7 ACTION_VIEWs.

This is far below the 81–86 intermediate A records from the A->B comparator.

## What this experiment establishes

### 1. Exact selectors were a real problem

Removing selectors eliminates the recurrent exact-substring copying defect.

Keep record-ID-only references as the preferred provenance interface.

### 2. But selector removal is not enough

The model still:
- selects wrong neighboring/question records;
- omits source_records entirely for some synthesized units;
- misses required body evidence;
- misses clinically material actions;
- imports state from uncited records.

Therefore the remaining bottleneck is **coverage/source-record enumeration under synthesis pressure**.

## The unique function A appears to provide

A's empirically useful function is not:
- polarity normalization;
- certainty normalization;
- copied selectors;
- action-state enums;
- semantic span identity.

Its useful function is:

> a dedicated pass that enumerates clinically relevant source records before synthesis, so B does not have to discover coverage and synthesize simultaneously.

This is the narrowest function that direct-B has repeatedly failed to replace.

## Candidate minimal architecture question

Do not restore old A.

Consider a minimal record-ID-only coverage handoff:

```text
SOURCE_COVERAGE

current_event_records=...
baseline_comparator_records=...
neuro_history_records=...
medication_context_records=...
exam_records=...
workup_records=...
action_bearing_records=...
context_records=...
```

Properties:
- record IDs only;
- no selectors;
- no copied source text;
- no polarity/certainty/assertion types;
- no action state;
- no clinical synthesis;
- no problem architecture;
- no note sections;
- no per-utterance atomic objects.

B would then synthesize from:
1. the complete Scribe packet; and
2. this compact record-ID coverage index.

This would preserve A's demonstrated useful function while discarding most of A's prior complexity.

## Alternative location

Before building a new runtime stage, also consider whether the Scribe packet itself can emit the coarse record categories as part of ingestion, since Scribe already owns source-local boundaries.

If Scribe can reliably provide category tags/record IDs, then runtime could remain:

```text
Scribe-with-coverage-index -> B -> C -> render
```

rather than reintroducing A.

## Current status

- A cannot be retired.
- old A is not justified in its current form.
- record-ID-only provenance should be retained.
- direct-B alone is not reliable enough.
- the unresolved architecture decision is where the **coverage census** belongs: Scribe vs a minimal A-like index.

No C yet.
No validator.
No selector copying.
No action-state enums.
