# MODULE 04 — ASSEMBLE

## PURPOSE

Take the problem blocks from `03_SELECT_ORGANIZE.md` and produce the Handoff.

This module selects, orders, and deletes. It does not write. It does not reword, compress, merge, or summarise — that is `05`.

The Handoff is a working artifact, not a note section. It is read by `05` and not printed. Its only virtue is fidelity: every line it carries is a line the record contains.

---

## INPUT

Two parts, both supplied:

1. **Object table** — every object with its ID, bucket, text, and provenance marker.
2. **Routing ledger** — one assignment line per object ID, produced by `03V`: `O# → P#.ROLE` or `O# → DISCARD: <reason>`.

Dereference every retained ID back to its object text, word for word, and append that object's provenance marker verbatim — `probable vascular dementia [D, 2025-06]`, `MMSE 24 [D, 2025-06]`, `left MCA infarct [D, 2024-02]`. Do not rewrite, normalise, or expand the marker, and do not add one the table does not contain. A `DISCARD` line means the object is dropped; a `REUSE` line means the object also appears in the listed second block. The ledger decides membership and role; `04` does not re-route.

---

## 1. COPY, DO NOT COMPOSE

Every entry in the Handoff is an entry from the block, word for word.

- You may **delete** words from it.
- You may **not** add a word, substitute a word, or reorder words.
- You may **not** join two entries into one string.
- You may **not** turn a sentence into a noun phrase or a heading.

If a sentence needs a word that is not in it, the Handoff goes without the sentence.

---

## 2. DELETE, DO NOT TIDY

Remove a whole entry when it adds nothing:

- a completion statement whose result is already recorded (`MRI was completed` when `MRI confirmed infarct` follows)
- an entry duplicated by another

Never remove: a state word, a condition, a reason, a date, a laterality, a negation, or a number.

`ETIOLOGY` and `CLAIM_QUALIFIER` entries are exempt from the duplicate rule. A reasoning entry is never deleted because the facts it interprets already appear under `EVIDENCE` — the overlap is expected, and that entry is the one `05` renders last.

---

## 3. STATES TRAVEL WITH THEIR ENTRY

`ordered`, `requested`, `pending`, `held`, `not started`, `unless`, `once`, `recommended`, `declined`, `deferred`.

None of these may be dropped to make a line read better. A conditional that loses `unless` is a different plan.

---

## 4. ONE ENTRY, ONE FIELD

Do not split an entry across two fields. Do not move an entry to another field — allocation made that decision in `02`.

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

`PRIMARY_CLAIM` is the one current formulation the A/P problem line is built from. `PROBLEM_LABEL` is a distinct field for a block that has no current formulation but is named by a prior or symptom-level proposition; it goes under its own heading and is never written as `PRIMARY_CLAIM`. `CLAIM_QUALIFIER` holds the additional formulations, exclusions, and interpretation that `05` renders as reasoning or evidence bullets. All three come from the ledger; none may be dropped here.

Omit a field with no entry — do not print an empty header. Number problems in the order the ledger set. Do not reorder.

The number of problems in your output equals the number in the input. Never drop a block, and never merge two into one.

---

## 7. BEFORE YOU RETURN

Read every line and ask one question: *is this a sentence the source contains, with words removed?*

If a line contains a word no source sentence contains, delete the line. That test is the whole module.

Then: a block with no `MANAGEMENT` entry is not a problem. Delete it.
