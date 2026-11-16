# DeepSeek review — Scribe V2.2 prompt

**Reviewed:** `proposals/chatgpt/113-scribe-evidence-packet-v2.2-turn-preserving-transcript.md`.

**Verdict:** close, but not clean enough to freeze. Two real format contradictions and two source-fidelity
traps.

## 1. Record grammar contradicts the prechart example

The prompt says every evidence line is exactly:

```text
<record-id> :: <SPK-or-source> :: <text>
```

But the prechart example is:

```text
P1.001 :: SEC=HPI :: VIA=EMS report :: faithful clinical statement
```

That is four or five fields, not three. A parser following the top rule will misread valid P records.

Fix with two explicit forms:

```text
T record:
T001 :: SPK2 :: text

P record:
P1.001 :: [SEC=<heading>] :: [VIA=<reported source>] :: text
```

Rules:

- T: two structural separators, then text.
- P: optional `SEC=` and `VIA=` fields, then text.
- Text is the remainder; it may contain `::`.
- Do not require empty `SEC=`/`VIA=` fields; omit them when absent.

## 2. “No pipe character” conflicts with source fidelity

If the source text contains `|`, the prompt forbids reproducing it. That forces alteration or omission.

Change to:

> Do not use pipe characters or Markdown tables as output structure. If the source text itself contains a
> pipe, preserve it literally inside the text field.

Same for bullets:

> Do not use Markdown bullets as structure. If the source contains bulleted content, preserve the content
> as plain text lines.

## 3. Header grammar is underspecified

`@@SOURCE P1 <SOURCE NAME> <DATE IF STATED>` has no delimiter between name and date. A source name with
spaces plus a date is ambiguous.

Define one form, e.g.:

```text
@@SOURCE P1 <source name> | <date or UNKNOWN>
```

or keep spaces but state that the parser treats the full remainder as name/date metadata and does not
split it semantically.

Do not add a pipe if you just prohibited pipes; choose one convention.

## 4. Redundancy is high but not fatal

The prompt repeats:

- no inference;
- no correction;
- preserve order;
- no summary;
- no reconciliation.

Some repetition protects high-risk rules. Do not add more. Trim only duplicate prose, not the concrete
examples.

## 5. What is good

- turn-preserving transcript extraction;
- separate question/answer records;
- raw SPK labels, no global identity;
- `[UNCLEAR]` vs `[VERBATIM]`;
- prechart source/section preservation;
- template exclusion;
- no target length;
- explicit truncation marker.

## Recommended minimal patch

1. Define T and P record forms separately.
2. Allow literal source `|`/bullets inside text; prohibit them only as output structure.
3. Define the `@@SOURCE` header grammar.
4. Keep the rest unchanged.

Do not add coverage/synthesis to Scribe. Coverage and action recovery stay in the Ask/B prompt.

No architecture change.
