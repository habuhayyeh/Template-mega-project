# ChatGPT review 115 — Scribe V2.2 held-out structural generalization

## Scope

Review of a second, morphologically different Scribe V2.2 output. No patient-specific clinical content is committed.

Important limitation: only the Scribe output was available for this review. The exact raw transcript/prechart used to generate it was not available, so source-fidelity, omission, and hallucination cannot be fully adjudicated.

## Verdict

**STRUCTURAL GENERALIZATION PASS; FIDELITY FREEZE PENDING RAW-INPUT COMPARISON.**

V2.2 successfully generalizes beyond the first seizure-like-event case to a long chronic neuromuscular encounter with extensive comorbidity, medication history, prior specialty documentation, results, procedures, and noisy diarized dialogue.

## What generalized successfully

1. Transcript remains turn-oriented rather than being rewritten as a narrative.
2. Raw speaker labels remain visible and no global speaker-identity ontology is introduced.
3. Garbled/odd transcript content is usually retained and marked rather than silently normalized.
4. Current encounter chronology, symptoms, patient-reported history, clinician questions, exam prompts, and management discussion remain locally attributable.
5. Large prechart content is retained without an observed length-driven truncation, supporting D-035.
6. Explicit section labels, medication/allergy lists, labs, historical diagnoses, historical plans, and unavailable-result states remain visible.
7. Historical specialty-note assessment/plan content remains source-qualified instead of being silently promoted to current encounter truth.

## Important stress-test properties exposed

### A. Ask will receive substantial clinically irrelevant/noisy history

The held-out packet retains extensive old procedures, long medication/allergy lists, remote labs, repeated no-result statements, and many non-neurologic diagnoses.

This is not automatically a Scribe failure. It is exactly the kind of source-preserving noise that the downstream semantic layer must filter by neurologic relevance and current encounter role.

Do not respond by teaching Scribe to decide which chronic diagnoses are important. That would move semantic ownership upstream.

### B. Temporal conflict is preserved for Ask

The packet contains prior outpatient statements about chronic disease status alongside current encounter symptoms and possible acute worsening.

This is desirable: Scribe should preserve both source states; Ask should decide current state/adoption and whether the old assessment remains applicable.

### C. Direct-source boundary cannot be fully validated from output alone

The prechart is represented as one direct source containing prior notes/results/intake, with an outpatient neurology note represented as nested VIA content.

That may be correct if the raw prechart supplied one combined source block containing an embedded prior note. It would be incorrect if the outpatient note was independently supplied as a separate direct source.

Without the raw input, this cannot be adjudicated.

### D. Transcript fidelity cannot be fully validated from output alone

The output looks much more literal/turn-preserving than earlier versions, but unsupported paraphrase, omission, or subtle reattribution can only be detected against the raw transcript.

## Non-blocking observations

- The packet is long, but no hard-output truncation is evident.
- Some conversational noise remains; this is preferable to semantic loss at the Scribe layer.
- Many [UNCLEAR] markers are expected with poor speech-to-text and are safer than model repair.
- The packet provides enough provenance and chronology for a downstream Ask experiment.

## Decision

Do not revise the Scribe prompt based on this output alone.

Do not add relevance filtering, problem selection, current-state adjudication, contradiction resolution, or problem hierarchy to Scribe.

V2.2 remains the baseline.

## NEXT

Two valid next steps depend on the purpose of the next experiment:

1. For **Scribe contract freeze**: compare this packet to the exact raw transcript/prechart and audit source boundaries, omission, unsupported inference, negation, chronology, and rationale.
2. For **end-to-end architecture testing**: this packet is already suitable as a stress-test input to Doximity Ask because it contains the noisy history, nested prior assessments, medication burden, and current neurologic symptoms the semantic layer must handle.

Recommendation: proceed to the Ask experiment now, while keeping the Scribe contract provisionally frozen; perform raw-input fidelity audit in parallel when the exact raw source is available.

No Gate-0 acceptance follows from this review alone.