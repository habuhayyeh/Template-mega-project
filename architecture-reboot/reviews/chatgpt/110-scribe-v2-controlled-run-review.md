# ChatGPT review 110 — controlled Scribe V2 run

## Scope

Review of the controlled V2 Scribe rerun using the same raw case. Patient-specific source content is not committed. This records only protocol behavior.

## Verdict

V2 is close enough that the remaining work is prompt tuning, not architecture redesign.

## What V2 fixed

1. No Markdown-table corruption after removing pipe delimiters.
2. Direct-source separation remained intact.
3. Nested/reported sources remained nested rather than being promoted to direct sources.
4. Final note template/scaffold was excluded from the evidence packet.
5. Cross-source re-synthesis of labs/imaging/medications/collateral disappeared.
6. Exact event timing and inter-event intervals were better preserved.
7. Explicit unavailable lab/imaging/EKG states were preserved.
8. Superseded Keppra plan and rationale were preserved.

## Remaining failure modes

### A. Unsupported inference from garbled dialogue
A transcript question with no clear answer was converted into a negative statement. This violates the no-inference rule.

### B. Interpretive repair of garbled wording
A raw phrase transcribed as "hip trauma" was rewritten as "head trauma" because context appeared to suggest it. V2 explicitly forbids guessing; the correct behavior is to retain the wording with [UNCLEAR] rather than repair it.

### C. Multi-speaker records still merge provenance
Records such as SPK1/SPK3 or SPK1/SPK2/SPK3 combine statements from multiple diarized speakers into one evidence record. This reduces local provenance and can hide diarization uncertainty.

Recommended rule:
- default one evidence record to one raw speaker/source;
- combine speakers only when the record explicitly preserves each speaker's separate contribution and no semantic merge is performed.

### D. Speaker diarization remains unreliable
The same SPK label can correspond to different real people in raw transcription. Preserve SPK labels mechanically; do not derive a stable person identity from SPK alone.

### E. Some neurologically relevant negatives can still be lost
The ED note contains a "no tongue bite" finding that did not appear in V2 output. Event-fidelity rules should explicitly protect:
- tongue bite;
- incontinence;
- injury;
- cyanosis/apnea/abnormal breathing;
- post-event confusion/somnolence;
- focal deficit after event.

### F. Template-relevant source fields need mechanical preservation
V2 omitted an explicit "no family history on file" source statement even though it preserved PMH/PSH/allergy/vitals. Ask may need explicit source absence/status for template filling. The rule should be:
- if a direct source contains a template-relevant field, preserve its stated value/status exactly, including "not on file"/"none"/"no result available".

### G. Redaction tokens are external to the protocol
User-provided PERSON_A/PERSON_B-style tokens are post-synthesis redactions and should be treated as opaque strings. Production Scribe should not infer meaning from them. This is not a semantic architecture issue.

## Minimal V2.1 patch direction

Do not add new ontology.

Only:
1. strengthen NO-INFERENCE for unanswered/garbled questions;
2. strengthen NO-REPAIR: use [UNCLEAR] instead of contextual correction;
3. prefer one speaker/source per evidence line;
4. add event-negative fidelity examples;
5. preserve direct-source template-relevant absent/unavailable states mechanically.

## NEXT

DeepSeek reviews this actual-run evidence together with proposal 109 and identifies whether any of the five V2.1 changes are unnecessary or insufficient. Then produce one final baseline Scribe prompt and stop iterating unless a new observed failure appears.
