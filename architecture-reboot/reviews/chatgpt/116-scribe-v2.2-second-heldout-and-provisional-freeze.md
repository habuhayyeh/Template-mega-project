# ChatGPT review 116 — Scribe V2.2 second held-out case and provisional freeze

## Scope

Structural review of a second held-out V2.2 output from a morphologically different neurology consult. Patient-specific content is not committed.

Only the Scribe output was available; exact raw transcript/prechart was not supplied for a full source-fidelity audit.

## Verdict

**PASS — V2.2 is provisionally frozen for end-to-end Ask testing.**

This case extends structural generalization beyond seizure-like events and chronic neuromuscular disease to an encephalopathy/cognitive-baseline consult with extensive collateral history, ADLs, medication-management uncertainty, old stroke, chronic pain/opioid exposure, malignancy, bedside exam, and a partially developed current neurology note.

## What this case demonstrates

1. Turn-preserving transcript extraction remains stable in long collateral-heavy dialogue.
2. Baseline-vs-current cognitive/function information remains locally attributable.
3. ADLs, mobility, falls, medication self-management, driving, finances, and home supports survive the ingestion layer.
4. Historical neurologic disease and residual deficits remain source statements rather than being converted into a final problem model.
5. Bedside exam questions/responses remain in transcript order.
6. Current prechart HPI, labs, medication list, and provisional A/P remain source-qualified.
7. Long output does not show evidence of hard truncation.

## Important downstream implication

The packet contains a current partial neurology consult note whose A/P names encephalopathy. Scribe should preserve it because it is supplied source material. Ask must not treat that provisional note label as automatically authoritative current truth; current adoption and final problem architecture remain STRUCTURE responsibilities.

This case therefore directly tests the need for the S2/STATE distinction between:
- a proposition documented in a current source;
- the final encounter stance adopted by the downstream model.

## No new Scribe-layer failure

No new failure appears that warrants prompt revision.

Do not add:
- relevance filtering;
- problem selection;
- diagnosis ranking;
- current-state adjudication;
- contradiction resolution;
- semantic collapsing of collateral/current-note/history.

Those belong downstream.

## Remaining limitation

A complete fidelity freeze still requires comparing at least one held-out packet to its exact raw transcript/prechart for:
- source-boundary fidelity;
- omission;
- unsupported paraphrase;
- negation;
- chronology;
- attribution;
- clinician rationale.

This limitation does not block end-to-end Ask testing.

## Decision

V2.2 becomes the **provisional Scribe baseline**.

No V2.3 unless a future end-to-end failure is traced specifically to Scribe and materially changes Ask reasoning or final-note fidelity.

## NEXT

Move to Ask.

Design the first Ask experiment around:
1. Scribe V2.2 packet as source substrate;
2. MD semantic contracts/pseudocode;
3. final USF note template;
4. Ask ownership of IDENTITY, RELEVANCE/ROLE, STATE, RELATIONS, and USE/REALIZATION;
5. explicit protection against blindly adopting provisional labels from current prechart notes;
6. final-note comparison against clinician expectations.

No Gate-0 acceptance follows from this review alone.