# Direct-B record-ID-only follow-up

## Question

Can direct-B preserve required body evidence and actions using stable Scribe record IDs only, without selectors and without Stage A?

## Runs

Run the record-ID-only module twice.

Use:

- the same clean `SCRIBE_EVIDENCE_V2_2` packet;
- two fresh Doximity Ask conversations;
- identical prompt and file;
- no prior run output;
- no oracle attached;
- no A/B/C files attached.

Save as:

- R1
- R2

## Blocking dimensions

Both R1 and R2 must pass all of these.

### 1. Record-ID fidelity

Every cited record ID must:

- exist in the packet;
- materially support the associated output;
- not be a neighboring-record substitution.

Any wrong record ID fails the run.

### 2. No uncited state

No output may import:

- chronology;
- provenance;
- action status;
- diagnostic state;
- result availability;
- management wording

from a record that is not cited for that output.

If multiple records support the output, all must be cited.

### 3. Body/nonproblem coverage

CLINICAL_UNITs must preserve, when present:

- current-event chronology needed for HPI;
- baseline comparator;
- prior neurologic/seizure history;
- relevant family neurologic history;
- relevant medications/supplements;
- current neurologic examination;
- relevant outside/current workup and results;
- clinically relevant context.

No exhaustive ledger is required.

### 4. Actions

Preserve all clinically material action concepts needed downstream.

Distinct targets must remain recoverable.

No invented action.

Compound source records may support multiple ACTION_VIEWs using the same source record IDs.

### 5. Provenance

Preserve:

- direct versus mediated report;
- outside versus current source;
- result reviewed versus merely performed/reported when material.

### 6. Problem architecture

Expected behavior:

- one PRIMARY current neurologic problem when supported;
- baseline comparator not promoted solely because it is distinct/chronic;
- no unnecessary non-neurologic problems.

### 7. Diagnostic stance

Preserve uncertainty.

No certainty upgrade.

### 8. Representation burden

Record:

- output line count;
- approximate character count;
- number of CLINICAL_UNITs;
- number of ACTION_VIEWs.

Pass requires materially lower burden than A->B.

## Decision

### Retire A if both R1 and R2:

- pass record-ID fidelity;
- contain no uncited state;
- pass body/nonproblem coverage;
- pass action coverage;
- pass provenance;
- pass problem architecture;
- pass diagnostic stance;
- retain materially lower burden than A->B.

### Do not retire A if either run:

- cites wrong record IDs;
- imports material state from uncited records;
- loses required body evidence;
- loses clinically material actions;
- requires an A-like exhaustive ledger.

Do not average a blocking failure away.

## Important

This follow-up does not authorize:

- C;
- renderer changes;
- validators;
- new stages;
- action-state enums;
- A rebuild.
