# SUPERSEDED BY D-053 — DO NOT RUN

Normalized action-state/B1 architecture is retired. Active path: `01-SOURCE-LOCAL-INGESTION.md` -> `02-CLINICAL-SYNTHESIS.md` -> `03-NOTE-COMPILER.md`.

# A -> B1 INTEGRATION TEST

**Experimental version:** A-B1-INTEGRATION-V1  
**Purpose:** run final Stage A and then B1 action-state interpretation in one Ask invocation.

## Inputs

Provide:

1. one complete canonical `SCRIBE_EVIDENCE_V2_2` packet;
2. `01-SOURCE-LOCAL-INGESTION.md`;
3. `02A-B1-ACTION-STATE-INTERPRETATION-TEST.md`.

## Execution order

### Phase 1 — Stage A

Apply `01-SOURCE-LOCAL-INGESTION.md` to the complete Scribe packet.

Produce the complete:

`@@HANDOFF A_SOURCE_LOCAL_INGESTION_V2_1 ... @@END`

Do not stop for user review.

### Phase 2 — B1 action-state interpretation

Immediately use the `ACTION_SPANS` from the Phase-1 A handoff as B1 input.

Apply `02A-B1-ACTION-STATE-INTERPRETATION-TEST.md`.

Use the original Scribe packet only to dereference source records already cited by those A action spans.

Do not scan the packet for actions that A omitted.
Do not repair or rewrite A.
Do not perform problem architecture, section assignment, final-plan selection, note compilation, or prose rendering.

Produce the complete:

`@@HANDOFF B1_ACTION_STATE_V1 ... @@END`

## Return format

Return exactly two handoffs, in this order:

1. the complete `A_SOURCE_LOCAL_INGESTION_V2_1` handoff;
2. the complete `B1_ACTION_STATE_V1` handoff.

Do not add commentary before, between, or after them.
