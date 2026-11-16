# Direct-B internal SOURCE_COVERAGE follow-up

## Question

Can direct-B preserve complete source coverage and reliable clinical synthesis when it performs a mandatory record-ID census before synthesis in the same invocation?

## Runs

Run the internal-coverage B module twice.

Use:

- the same clean `SCRIBE_EVIDENCE_V2_2` packet;
- two fresh Doximity Ask conversations;
- identical prompt and module;
- no previous output;
- no oracle attached;
- no A/C/renderer files attached.

Save as:

- COV1
- COV2

## Blocking dimensions

Both runs must pass all blocking dimensions.

### 1. Census fidelity

Every SOURCE_COVERAGE ID must:

- exist in the packet;
- belong plausibly to its stated category;
- not substitute a question record for a separate substantive answer record.

The census must preserve, when present:

- current-event records;
- baseline/prior comparator records;
- neurologic/seizure history;
- relevant family neurologic history;
- medication/supplement context;
- current neurologic exam;
- relevant workup/results;
- clinically meaningful action-bearing records;
- relevant context.

### 2. Census-to-synthesis use

A materially important record present in SOURCE_COVERAGE must not be silently lost when its content is required downstream.

The emitted synthesis does not need one output unit per census record.

It must preserve all required clinical concepts.

### 3. Record-ID fidelity

Every record ID cited in PROBLEM / CLINICAL_UNIT / ACTION_VIEW / SYNTHESIS_UNRESOLVED must:

- exist;
- materially support the associated output;
- not be a neighboring-record substitution.

### 4. No uncited state

No output may import material:

- chronology;
- provenance;
- action status;
- diagnostic state;
- result availability;
- management wording

from an uncited record.

### 5. Body/nonproblem coverage

The final synthesis must preserve, when present:

- presenting-event chronology;
- baseline comparator;
- prior neurologic/seizure history;
- relevant family neurologic history;
- relevant medications/supplements;
- current neurologic exam;
- outside/current workup and results;
- clinically relevant context.

### 6. Actions

Preserve all clinically material action concepts needed downstream.

Distinct targets must remain recoverable.

No invented action.

No action-state upgrade.

### 7. Provenance

Preserve direct versus mediated evidence and outside versus current source status when material.

### 8. Problem architecture

Expected behavior:

- one PRIMARY current neurologic problem when supported;
- baseline comparator not promoted solely because it is distinct/chronic;
- no unnecessary non-neurologic problems.

### 9. Diagnostic stance

Preserve uncertainty.

No certainty upgrade.

### 10. Representation burden

Record:

- output lines;
- approximate characters;
- number of coverage IDs per category;
- number of CLINICAL_UNITs;
- number of ACTION_VIEWs.

Pass requires materially lower burden than old A->B.

## Decision

### Retire old A if both COV1 and COV2:

- pass census fidelity;
- pass census-to-synthesis use;
- pass record-ID fidelity;
- contain no uncited material state;
- pass body/nonproblem coverage;
- pass action coverage;
- pass provenance;
- pass problem architecture;
- pass diagnostic stance;
- retain materially lower burden than old A->B.

### Build minimal coverage A only if:

- the internal B census itself repeatedly loses material records or selects wrong records;
- while the rest of B remains clinically strong.

Do not restore old A.

Do not move the census into Scribe based on this experiment alone.

## Not authorized

This experiment does not authorize:

- Scribe coverage categories;
- old A restoration;
- selectors;
- action-state enums;
- semantic validators;
- C;
- renderer changes.
