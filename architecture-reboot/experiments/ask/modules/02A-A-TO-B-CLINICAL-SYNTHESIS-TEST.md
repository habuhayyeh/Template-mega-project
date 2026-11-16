# A -> B CLINICAL SYNTHESIS INTEGRATION TEST

## EXECUTION GATE

1. Read this entire controller before producing output.
2. Read both attached stage files completely before starting.
3. Read the complete Scribe packet before starting Phase 1.
4. Do not emit Stage A while still reading or interpreting Stage B instructions.
5. Silently complete Phase 1 and Phase 2 before emitting either handoff.
6. Keep the complete Stage A handoff internally available to Stage B.
7. Apply each stage's own EXECUTION GATE and FINAL OUTPUT GATE.
8. Do not emit reasoning, partial results, progress text, or commentary.

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

## FINAL OUTPUT GATE

Before emitting:

1. Verify Phase 1 satisfies the complete Stage A contract.
2. Verify Phase 2 satisfies the complete Stage B contract.
3. Verify Stage B used only A-cited Scribe records for dereference.
4. Verify exactly two complete handoffs are present.
5. Emit both handoffs once, in the required order.
6. Emit nothing else.


## Return format

Return exactly two handoffs, in this order:

1. complete `A_SOURCE_LOCAL_INGESTION_V2_1`;
2. complete `B_CLINICAL_SYNTHESIS_V1`.

Do not add commentary before, between, or after them.
