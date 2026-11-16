# Direct-B CLINICAL_UNIT follow-up

## Question

Can direct-B preserve required body/nonproblem evidence without recreating Stage A?

## Runs

Run the new direct-B-with-units module twice.

Use:

- the same clean `SCRIBE_EVIDENCE_V2_2` packet;
- two fresh Doximity Ask conversations;
- identical prompt and file;
- no prior run output;
- no oracle attached;
- no A/B/C files attached.

Save as:

- U1
- U2

## Blocking dimensions

Both U1 and U2 must pass all of these.

### 1. Pointer fidelity

Every cited selector must:

- belong to the cited record;
- be exact;
- be contiguous;
- contain no neighboring-record text;
- contain no paraphrase presented as selector.

Any hidden pointer drift fails the run.

### 2. Body/nonproblem coverage

The returned CLINICAL_UNIT set must preserve, when present:

- current-event chronology needed for HPI;
- baseline comparator;
- prior neurologic/seizure history;
- relevant family neurologic history;
- relevant medications/supplements;
- current neurologic examination;
- relevant outside/current workup and results;
- clinically relevant context.

No exhaustive ledger is required.

### 3. Actions

Preserve all clinically material action concepts needed downstream.

Distinct targets must remain recoverable.

No invented action.

### 4. Provenance

Preserve:

- direct versus mediated report;
- outside versus current source;
- result reviewed versus merely performed/reported when material.

### 5. Problem architecture

Expected behavior:

- one PRIMARY current neurologic problem when supported;
- baseline comparator not promoted solely because it is distinct/chronic;
- no unnecessary non-neurologic problems.

### 6. Diagnostic stance

Preserve uncertainty.

No certainty upgrade.

### 7. Representation burden

Record:

- output line count;
- approximate character count;
- number of CLINICAL_UNITs;
- number of ACTION_VIEWs.

Pass requires materially lower burden than the A->B runs.

## Decision

### Retire A if both U1 and U2:

- pass pointer fidelity;
- pass body/nonproblem coverage;
- pass action coverage;
- pass provenance;
- pass problem architecture;
- pass diagnostic stance;
- retain materially lower burden than A->B.

### Keep investigating A's preservation role if either run:

- loses required body evidence;
- has material pointer drift;
- requires an A-like exhaustive ledger to succeed.

Do not average a blocking failure away.

## Important

This follow-up does not authorize:

- C;
- renderer changes;
- validators;
- new stages;
- action-state enums.
