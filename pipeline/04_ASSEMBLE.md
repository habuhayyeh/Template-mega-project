# MODULE 04 — ASSEMBLE

## PURPOSE

Turn the routing ledger into the Handoff.

This module dereferences. It selects nothing, deletes nothing, rewords nothing, merges nothing, compresses nothing. Every retained ID becomes one entry carrying its own words and its own provenance.

The Handoff is a working artifact, not a note section. It is read by `05` and not printed. Its only virtue is fidelity: every line it carries is a line the record contains.

---

## INPUT

Two parts, both supplied:

1. **Object table** — every object with its ID, kind, text, and provenance marker.
2. **Routing ledger** — one assignment line per object ID, produced by `03`: `O# → P#.ROLE` or `O# → DISCARD: <reason>`.

Dereference every retained ID back to its object text, word for word, and append that object's provenance marker verbatim — `probable vascular dementia [D, 2025-06]`, `MMSE 24 [D, 2025-06]`, `left MCA infarct [D, 2024-02]`. Do not rewrite, normalise, or expand the marker, and do not add one the table does not contain. A `DISCARD` line means the object is dropped; a `REUSE` line means the object also appears in the listed second block. The ledger decides membership and role; `04` does not re-route.

---

## 1. NO DELETION

Every retained entry appears in the Handoff. None is dropped for being short, obvious, repetitive, already implied, or a completion statement whose result follows.

Removing an exact duplicate is `03`'s job under its one-fact-one-entry rule. Compressing near-duplicates into one sentence is `05`'s job. `04` cannot tell a harmless repetition from a lost meaning, so it keeps both.

---

## 2. COPY, DO NOT COMPOSE

Every entry in the Handoff is an entry from the block, word for word.

- You may **delete** words from it.
- You may **not** add a word, substitute a word, or reorder words.
- You may **not** join two entries into one string.
- You may **not** turn a sentence into a noun phrase or a heading.

If a sentence needs a word that is not in it, the Handoff goes without the sentence.

---

## 3. STATES TRAVEL WITH THEIR ENTRY

`ordered`, `requested`, `pending`, `held`, `not started`, `unless`, `once`, `recommended`, `declined`, `deferred`.

None of these may be dropped to make a line read better. A conditional that loses `unless` is a different plan.

---

## 4. ONE ENTRY, ONE FIELD

Do not split an entry across two fields. Do not move an entry to another field — the ledger made that decision.

An entry whose role is `CLAIM_QUALIFIER` sits under `CLAIM_QUALIFIER` even when it is a `MANAGEMENT` object by kind. That is the adjudication exception, and the ledger has already applied it.

---

## 5. COURSE IS NOT WRITTEN HERE

If the block has no `COURSE` entry, the Handoff has no `COURSE` line. Never supply one, however obvious the state seems.

---

## 6. FORMAT

```text
PROBLEM 1
PRIMARY_CLAIM: …
CLAIM_QUALIFIER:
- …
ETIOLOGY:
- …
EVIDENCE:
- …
COURSE:
- …
MANAGEMENT:
- …
```

`PRIMARY_CLAIM` is the one current formulation the A/P problem line is built from. `PROBLEM_LABEL` is a distinct field for a block that has no current formulation but is named by a prior or symptom-level proposition; it goes under its own heading and is never written as `PRIMARY_CLAIM`. `CLAIM_QUALIFIER` holds the additional formulations, exclusions, interpretations, and adjudication logic that `05` renders as reasoning bullets. All three come from the ledger; none may be dropped here.

Omit a field with no entry — do not print an empty header. Number problems in the order the ledger set. Do not reorder.

The number of problems in your output equals the number in the input. Never drop a block, and never merge two into one.

---

## 7. BEFORE YOU RETURN

Read every line and ask two questions:

1. *Is this the object's text, with its marker, unaltered?*
2. *Is every retained ID present exactly once?*

If a line contains a word no object contains, or if an ID the ledger retains is absent, the assembly is wrong. Fix the assembly; do not fix the ledger here.

A block with no `MANAGEMENT` entry is not a valid problem and `03` guarantees none exists. If one appears, report it — do not delete the block.
