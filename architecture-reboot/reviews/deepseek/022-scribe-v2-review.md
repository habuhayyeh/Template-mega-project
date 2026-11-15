# DeepSeek review — Scribe V2 proposal and controlled run

**Reviewed:** `proposals/chatgpt/109-scribe-evidence-packet-v2.md`,
`reviews/chatgpt/110-scribe-v2-controlled-run-review.md`
**Status:** review only; no implementation.

## Verdict

V2 is a real improvement and the remaining work is prompt-level. The five V2.1 directions are mostly
right, but two need stronger changes than "strengthen":

- the STT-repair allowance must be **removed**, not strengthened;
- event-negative guidance must be **generalized**, not turned into a closed checklist.

The protocol is close to a final baseline. Do not add ontology or another abstraction layer.

## Accept / modify / reject

### 1. Strengthen NO-INFERENCE for unanswered/garbled questions

**ACCEPT, with a concrete rule.** "Strengthen" is too vague. Add:

- if a clinician question has no captured answer, emit it as a question with
  `[NO ANSWER CAPTURED]`;
- never convert an unanswered question into a negative finding;
- never infer a denial, normal finding or absence from silence.

### 2. Strengthen NO-REPAIR

**MODIFY — delete the repair allowance.** V2 says:

> Correct an obvious speech-to-text error only when the intended wording is unambiguous from the
> immediate context.

That clause caused the observed `hip trauma` → `head trauma` repair. It contradicts "do not guess."
Replace it with:

> Do not correct, normalize or replace content words. Preserve the raw token/phrase. If meaning is
> uncertain, keep the raw wording and append `[UNCLEAR: raw wording]`.

Punctuation/casing cleanup is acceptable only when it cannot change meaning.

### 3. One speaker/source per evidence line

**ACCEPT with a joint-statement exception.** Default one raw SPK/source per line. A joint statement
may remain one line only when each speaker's contribution is separately labeled and no semantic merge
occurs. Otherwise split into separate records.

Do not use `SPK1/SPK3` as a synthetic merged speaker.

### 4. Event-negative fidelity examples

**MODIFY — generalize.** A fixed list (tongue bite, incontinence, injury, cyanosis/apnea, confusion,
focal deficit) is useful as examples but risks becoming a checklist that misses other stated negatives.
The rule should be:

> preserve every explicitly stated event-related negative, pertinent negative, and normal/absent
> finding, including but not limited to the listed examples.

### 5. Preserve direct-source template-relevant absent/unavailable states

**ACCEPT, with explicit-only scope.** Preserve a field only when the direct source states it:
`none`, `not on file`, `no result available`, `not performed`, `unavailable`, etc. Do not invent empty
fields, do not create a field because the final template has one, and do not convert absence of a
statement into a negative.

## Additional missing rules

1. **Contradictions.** V2 says "do not reconcile" but does not require marking contradictions. Add
   inline `[CONFLICT: <record-id>]` when the same fact differs, and never resolve it.
2. **Output completeness, not a 20K budget.** D-035 relaxes the earlier 20K assumption: Scribe may
   produce a longer packet when fidelity requires it. Do not compress to hit a length target. Control
   consistency with the fixed line protocol and stable IDs, not summarization. If a hard platform limit
   is actually hit, mark the truncation point explicitly; never silently paraphrase or omit.
3. **Source order/date.** Preserve supplied source order; include source date/author when stated. Do not
   reorder by semantic category.
4. **Exact duplicates.** Exact boilerplate may be `DUP_OF <id>`; source-distinct clinical statements
   stay separate. Do not deduplicate to save space.
5. **No semantic compression.** Compression may remove greetings, filler and repeated conversational
   repair. It must not change a proposition, qualifier, attribution, chronology, negation or clinician
   rationale. Replace "faithful compressed clinical statement" with "faithful clinical statement;
   compression only removes nonclinical filler."
6. **No question-only records unless clinically meaningful** is fine, but do not drop a question that
   contains reasoning or whose answer would be ambiguous without it.

## Overengineering check

V2 is already detailed. Do not add a new ontology, a new section type, or a new cross-reference
ledger. Keep the protocol compact; length is controlled by format, not by dropping content. `SEC=` and `VIA=` are mechanical source labels and should stay. The final
baseline should be **shorter**, with the above rules stated as principles plus a few examples.

One questionable element: `SEC=` can become a semantic classification if the source heading is
ambiguous. Keep it only when the heading is copied verbatim; otherwise omit `SEC=` rather than infer a
category.

## Recommended V2.1 patch (minimal)

Replace the repair clause; add unanswered-question format; add inline `[CONFLICT]`; state that there is
no 20K compression target (D-035); add explicit-only absent fields; generalize event negatives; one
speaker per line with the joint exception; preserve source order/date; use `DUP_OF`.

Do not add new record types beyond `[UNCLEAR]`, `[CONFLICT]`, `[NO ANSWER CAPTURED]` and `DUP_OF`.

## Evidence before freezing

- V2.1 on the same raw case: no repair, no inferred negative from unanswered question, no merged
  speakers, event negatives preserved, absent fields preserved, contradictions marked, output length and
  consistency across runs. No 20K target.
- One different de-identified case with different source families/format, to test generalization rather
  than one-case tuning.
- Ask on Scribe output vs Ask on raw input, same final template; compare problem identity, adoption,
  causality, source fidelity.
- At least two runs per case; record failure taxonomy and omissions.

Stop after V2.1 + one held-out case unless a new observed failure appears. Do not add compression rules
to fit 20K; longer output is acceptable under D-035. No architecture change, no
Gate-0 acceptance, no Doximity, no Phase 0.
