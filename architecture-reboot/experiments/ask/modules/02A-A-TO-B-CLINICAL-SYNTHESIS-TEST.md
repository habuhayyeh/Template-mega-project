# A -> B CLINICAL SYNTHESIS INTEGRATION TEST

**Experimental version:** A-B-CLINICAL-SYNTHESIS-V1

## Inputs

Provide:

1. one complete canonical `SCRIBE_EVIDENCE_V2_2` packet;
2. `01-SOURCE-LOCAL-INGESTION.md`;
3. `02-CLINICAL-SYNTHESIS.md`.

## Execution order

### Phase 1 — Stage A

Apply `01-SOURCE-LOCAL-INGESTION.md` to the complete Scribe packet.

Produce the complete:

`@@HANDOFF A_SOURCE_LOCAL_INGESTION_V2_1 ... @@END`

Do not stop for user review.

### Phase 2 — Stage B

Immediately apply `02-CLINICAL-SYNTHESIS.md` to the complete Stage A handoff.

Use the original Scribe packet only to dereference source records/selectors already cited by A.

Do not create an action absent from A.
Do not emit action-state enums.
Do not perform note section allocation, NOTE_BLUEPRINT compilation, or final prose rendering.

Produce the complete:

`@@HANDOFF B_CLINICAL_SYNTHESIS_V1 ... @@END`

## Return format

Return exactly two handoffs, in this order:

1. complete `A_SOURCE_LOCAL_INGESTION_V2_1`;
2. complete `B_CLINICAL_SYNTHESIS_V1`.

Do not add commentary before, between, or after them.
