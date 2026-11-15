# MODULE 01V — SEMANTIC CORRECTIONS

## PURPOSE

Propose corrections to the fixed `01` candidate decomposition.

It does **not** emit a validated table. It does not rewrite objects. It proposes changes; deterministic code applies them.

---

## INPUTS

1. **Source material** — the `[A]`–`[D]` blocks, headers included.
2. **Candidate table** — the raw `01` output labelled with temporary `C1…Cn` IDs:

```text
C1 | DEMOGRAPHIC | 68F | [A, Neurology consult, 2026-11-14]
C2 | COURSE | admitted 11/12 | [A, Neurology consult, 2026-11-14]
```

`C#` is a review handle only. Final `O#` IDs are assigned by the apply script, never by this module.

---

## THE FOUR INVARIANTS

**1. Coverage** — no clinically meaningful proposition in the source is missing.

**2. Atomicity** — separable propositions are not merged; a COURSE or MANAGEMENT atom missing its governing subject is completed from the source.

**3. Kind correctness** — each object satisfies one of the six kinds defined in `01`.

**4. Attribution and provenance fidelity** — attribution, uncertainty, conditionality, source name, date are preserved. Do not restate provenance: the apply script assigns it from the authoritative headers.

---

## ALLOWED OPERATIONS

Only these four. **`DROP` is not an operation.**

### `RECLASSIFY`
Change the kind only. Text and provenance stay identical.

```text
RECLASSIFY | CANDIDATE: C33 | TEXT: "that is not today's issue" | NEW_KIND: OBSERVATION | INVARIANT: kind
```

### `COMPLETE_CONTEXT`
Restore the governing subject or verb from the same source sentence, so an elliptical atom stands alone. Add only words that govern the phrase; no paraphrase, no synonym, no new relation.

```text
COMPLETE_CONTEXT | CANDIDATE: C28 | TEXT: "not until six months seizure-free" | NEW_TEXT: "not driving until six months seizure-free" | INVARIANT: atomicity
```

It also covers **anaphora resolution** — replacing a pronoun or elliptical referent with its explicit antecedent — only when the antecedent is in the same source sentence, is unambiguous, adds no clinical content, every substantive word comes from that span, and no inference is required.

```text
COMPLETE_CONTEXT | CANDIDATE: C33 | TEXT: "that is not today's issue" | NEW_TEXT: "family's concern about her memory is not today's issue" | NEW_KIND: OBSERVATION | INVARIANT: atomicity
```

`NEW_KIND` is optional and corrects the kind in the same change when the completion makes it clear.

### `SPLIT`
Divide one candidate into two or more atomic objects. Lexical overlap between the results is allowed and expected; each result must be supported by the candidate object or the sentence it came from.

```text
SPLIT | CANDIDATE: C5 | TEXT: "postictal confusion lasting an hour" | RESULT: "OBSERVATION: postictal confusion" ; "COURSE: postictal confusion lasting an hour" | INVARIANT: atomicity
```

### `RESTORE`
Add a proposition the candidate omitted entirely. `QUOTE` must be an exact span from the named source; `NEW_TEXT` must be drawn from that span. Arithmetic, derived dates, and synthesised wording are rejected by construction.

```text
RESTORE | SOURCE: D | QUOTE: "Neurosurgery recommended follow-up imaging in two years" | NEW_TEXT: "Neurosurgery recommended follow-up imaging in two years" | NEW_KIND: MANAGEMENT | AFTER: C54 | INVARIANT: coverage
```

---

## RULES

- Reference objects by `C#`, and quote the candidate text exactly as written.
- One change per line. Do not propose two changes for the same candidate.
- `RESTORE` needs `SOURCE`, `QUOTE`, `NEW_TEXT`, `NEW_KIND`, `AFTER`.
- `COMPLETE_CONTEXT` may only add words that appear in the source sentence (grammatical inflection accepted), or replace a single pronoun with a verbatim span from that sentence.
- `SPLIT` must produce at least two results, each written `KIND: text`.
- Never state provenance, source name, or date — the apply script assigns them.
- If nothing needs repair, emit exactly:

```text
NO_CHANGE
```

---

## OUTPUT

A single `CHANGES` block. No validated table, no prose, no markdown.

```text
CHANGES
<change line>
<change line>
```

Nothing else. The apply script rejects the whole transaction if any line is invalid.
