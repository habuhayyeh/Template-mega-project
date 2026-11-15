# ChatGPT review 114 — Scribe V2.2 controlled rerun

## Scope

Protocol-level review of the same-case V2.2 rerun. Patient-specific content is not committed.

## Verdict

**PASS for same-case Scribe tuning.**

The two material transcript failures that justified V2.2 are no longer present:

1. clear-but-odd content words are preserved rather than medically repaired;
2. transcript evidence is organized by raw speaker turn rather than cross-turn question/answer synthesis.

The remaining deviations are non-blocking prompt-compliance issues, not clinically meaningful architecture failures.

## Success criteria

### 1. No unanswered question becomes a denial/normal/patient statement

PASS for the observed failure mode.

V2.2 now keeps ambiguous clinician questions as questions/uncertain records instead of manufacturing a patient response.

### 2. No clear content word repaired

PASS.

The prior raw phrase "hip trauma" remains "hip trauma" rather than being normalized to "head trauma."

### 3. No record semantically combines separate raw turns

PASS at the level Scribe can control.

Each T-record is derived from one raw diarized turn. A single raw diarization turn can itself contain apparent voices/answers from more than one real person; that is an upstream diarization limitation and should not be solved by Scribe inference.

### 4. Packet grammar

PASS.

The packet uses stable record IDs and the "id :: label :: text" grammar.

### 5. Prechart fidelity

PASS.

Direct-source section structure, explicit absent/unavailable states, event-related negatives, clinician reasoning, and superseded management decisions remain available.

### 6. Length/completeness

PASS.

The packet is longer than prior versions, but D-035 explicitly prefers fidelity over compression. No observed evidence of length-driven truncation.

## Non-blocking deviations

1. Some greetings/conversational fragments remain despite the omission rule.
2. [VERBATIM] / [UNCLEAR] use is not perfectly calibrated in every line.
3. Some raw diarization turns contain multiple apparent speakers; Scribe cannot safely repair this.
4. Prechart second-field labeling is somewhat redundant (P1.001 :: P1 :: SEC=...) but parseable.

These do not currently justify another prompt revision because they do not materially threaten Ask's clinical reasoning or final-note fidelity.

## Decision

Stop same-case Scribe prompt tuning.

Do **not** create V2.3 for cosmetic cleanup.

## NEXT

1. Run V2.2 on one different de-identified case with different source morphology.
2. If no new material failure appears, freeze the Scribe evidence-packet contract provisionally.
3. Then test Doximity Ask using:
   - the Scribe packet,
   - the MD semantic contracts,
   - the final note template.
4. Evaluate whether Ask can reconstruct problem identity, current state, relations, note role/use, and final note fidelity from the Scribe substrate.

No architecture change and no Gate-0 acceptance from this review alone.