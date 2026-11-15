# ChatGPT review 112 — Scribe V2.1 controlled rerun

## Scope

Protocol-level review of the same-case V2.1 rerun. Patient-specific source content is not committed.

## Verdict

The prechart transformation is sufficiently structured for the next stage. The remaining material failure is concentrated in transcript transformation.

This is not an architecture failure. It is a mismatch between two different input morphologies:
- transcript = noisy diarized dialogue where cross-turn synthesis can invent attribution or repair speech;
- prechart = explicit document/section structure where source-preserving compression works well.

## What V2.1 fixed

- no Markdown-table corruption;
- no cross-source summary layer;
- nested sources stay nested;
- explicit family-history/vital/lab/imaging/EKG absence states are retained;
- no-tongue-bite and other event-relevant negatives can survive;
- changed Keppra decisions are retained;
- source headings and provenance remain visible.

## Remaining material transcript failures

### 1. Question/answer synthesis still creates unsupported meaning

A clinician turn containing a garbled question was summarized as though it included a patient/collateral response. The raw dialogue does not cleanly supply that response.

This is dangerous because an Ask model may treat the derived negative/normal statement as evidence.

### 2. Content-word repair still occurs

The raw transcript says "hip trauma"; V2.1 outputs "head trauma."

The prompt explicitly prohibited this, so additional prose prohibitions are unlikely to be the best fix.

### 3. One-speaker-per-record is still violated semantically

Several records are headed by one SPK label while also incorporating another speaker's answer/history into the same record. The body sometimes labels the second speaker, so information is recoverable, but the record header is no longer a reliable provenance key.

## Design correction

Do not ask GPT-4o to semantically compress transcript dialogue across turns.

Instead use **turn-preserving clinical extraction**:

- every transcript evidence record is derived from exactly one raw speaker turn;
- one raw turn may produce multiple records;
- one record may never incorporate words/facts from another raw speaker turn;
- preserve raw content words; no medical correction/normalization;
- unanswered questions stay questions;
- odd/garbled clinical wording is quoted verbatim and marked [UNCLEAR];
- omit nonclinical turns entirely;
- preserve transcript order.

Prechart behavior remains section-preserving source compression as in V2.1.

## Architecture implication

No change to Scribe -> Ask responsibility boundary.

Scribe remains evidence formatting. Ask remains semantic owner.

The only refinement is modality-specific INGEST behavior:
- transcript: turn-preserving extraction;
- chart/prechart: section-preserving compression.

## NEXT

Create a V2.2 prompt by changing only the TRANSCRIPT rules. Keep the V2.1 prechart rules unchanged. Run once on the same case. If the two observed material transcript errors disappear, stop same-case Scribe tuning and move to a held-out case.
