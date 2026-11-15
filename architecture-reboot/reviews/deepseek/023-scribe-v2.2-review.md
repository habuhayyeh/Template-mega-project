# DeepSeek review — Scribe V2.2 turn-preserving transcript

**Reviewed:** `proposals/chatgpt/113-scribe-evidence-packet-v2.2-turn-preserving-transcript.md`,
`reviews/chatgpt/112-scribe-v2.1-controlled-run-review.md`
**Status:** review only; no implementation.

## Verdict

V2.2 is the right direction and should be tested. Turn-preserving extraction directly addresses the
three observed transcript failures. It is close to a final baseline.

Three wording issues should be fixed before the controlled run; none is architectural.

## Accept

- one T-record derives from one raw speaker turn;
- one turn may split into multiple records;
- no cross-turn question/answer synthesis;
- raw SPK labels, no global identity map;
- preserve raw content words; no STT repair;
- `[NO ANSWER CAPTURED]` for unanswered clinical questions;
- transcript order preserved;
- prechart rules unchanged from V2.1;
- no target packet length (D-035);
- `@@TRUNCATED` marker for an actual hard limit;
- redaction tokens treated as opaque;
- no automatic `[CONFLICT]` or `DUP_OF` tags is acceptable at this stage: source blocks preserve
  contradictions; Ask can reconcile. Do not add more cross-reference machinery.

## Modify before the run

### 1. `[UNCLEAR]` is being used for two different things

V2.2 says:

> If a content word or phrase is odd, garbled, or clinically implausible, copy the raw wording
> verbatim and append `[UNCLEAR]`.

That conflates **bad transcription** with **clear but clinically odd wording**. The `hip trauma` case is
clear text; it is not unclear. Marking it `[UNCLEAR]` tells Ask the transcription is unreliable when the
problem is that the wording is clinically unexpected.

Use two markers:

- `[UNCLEAR: raw text]` only for inaudible/garbled/uncertain transcription;
- `[VERBATIM: implausible/odd]` for clear raw wording that must not be corrected or normalized.

Example:

```text
T040 :: SPK1 :: Asked about previous "hip trauma." [VERBATIM: implausible wording]
```

Do not use `[UNCLEAR]` merely because the content is medically surprising.

### 2. Remove the “clinically useful question” judgment

Rules 10–11 ask Scribe to decide whether a clinician question is “clinically useful” or “clinically
important.” That is a semantic judgment and can drop the question that Ask needs to interpret a later
answer.

Replace with a mechanical rule:

- preserve every clinician question that contains clinical content or whose answer is captured;
- omit only greetings, logistics, and pure conversational repair;
- if the answer is missing, keep the question with `[NO ANSWER CAPTURED]`.

No “usefulness” test.

### 3. Clarify omission of “filler”

“Omit filler” can drop a patient statement that carries function, safety, social or symptom context.
Replace with:

- omit only greetings, nonclinical logistics, and repeated conversational repair;
- when in doubt, preserve the statement;
- never omit a statement about function, safety, home situation, substances, or symptoms as “filler.”

### 4. Exact line grammar

The prompt says:

> Use this separator exactly:
>  ::

but the grammar is ambiguous. State it as:

```text
<record-id> :: <SPK-or-source> :: <text>
```

with exactly one space around `::`, no standalone separator line, and no pipe/table/bullet syntax.
Also add: output only the packet; no preamble, code fence or closing summary.

## Prechart / length

Prechart rules are sufficient. D-035 removes the 20K target; keeping `@@TRUNCATED` is enough. Do not add
compression rules or an `OMITTED` priority list.

## Residual risk

Turn-preserving extraction cannot fix bad diarization that merges two real speakers into one raw turn.
That is acceptable: SPK is a raw label, not identity. Ask must treat it as unreliable. Do not add a
speaker-identity inference rule.

## Test

Run V2.2 once on the same case. Success criteria:

- no unanswered question becomes a denial/normal/patient statement;
- no clear content word is repaired (`hip trauma` stays `hip trauma`);
- no record mixes two raw turns;
- `[VERBATIM]` vs `[UNCLEAR]` used correctly;
- packet parses as `id :: label :: text`;
- prechart absent/unavailable states and event negatives survive;
- no length-driven omission.

If these pass, stop same-case tuning and run one held-out de-identified case. Do not add new ontology.
No architecture change, no Gate-0 acceptance, no Doximity, no Phase 0.
