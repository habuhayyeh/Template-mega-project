# DeepSeek response 004 — answers to the three schema questions, and consensus confirmation

---

## 1. Checker boundary — agreed, and it corrects me

Yes: **mechanical check is IR → note. Source → IR is a semantic audit**, not a deterministic check, unless a specific predicate is genuinely mechanical (span containment, id existence, operator validity).

This corrects a sentence in my earlier proposal. I wrote that the checker "recomputes units from objects and compares them to the units the planner emitted". Unit selection is semantic; recomputing it mechanically is impossible in the general case, and calling it a check would have been the same category error as calling `PROJECT` deterministic.

The mechanical checks that do survive are all IR-local or note-local:

- every unit references existing object ids and a valid operator;
- every object appears in ≥1 unit or carries a disposition;
- every note line maps to a unit; every unit maps to ≥1 note line;
- no note word outside the referenced objects, the operator's fixed text, or the section's transformation table;
- section-scoped voice;
- ordering and bucket conformance.

Everything about whether the IR is *right* is the semantic audit's job, and it is a different instrument.

## 2. Problem ownership — accepted, one object, many units

I withdraw the "two objects with the same span" proposal. One stable object, used by as many render units as the note needs, with an optional `primary_problem` for accounting only.

Why your version is better: duplicating a proposition to give it two homes duplicates its provenance and creates two objects that can drift apart. The span is one; the uses are many.

One consequence to write down, because it changes an invariant:

> An object is **covered** when it appears in at least one render unit, or carries an explicit disposition. It is not covered by being assigned to exactly one problem.

Accounting therefore moves from the object to the unit: every object accounted for (used or dispositioned), and every unit owning exactly one problem. That is still total and still checkable.

## 3. Source coverage — larger spans, many objects per span

**Take the second option, with one constraint: spans are bounded mechanically, not semantically.**

A span is a line, an utterance, or a speaker turn as it appears in the paste. It is not "one proposition". Splitting prose into proposition-sized spans is itself a semantic act, and it is exactly the kind of act that has produced our instability — a model deciding where one clinical thought ends.

So:

```text
span S12  (utterance, source B, turn 4)
  → OBJECT O36   memory worsening over a year
  → OBJECT O37   clinic said dementia
  DISPOSITION: OBJECTS (2)
```

- every span has ≥1 disposition;
- a span may yield several objects;
- every object names its span;
- a span with no objects still needs a disposition: `NOT_CLINICAL` or `NOT_USED_BY_THIS_NOTE` with a reason.

The invariant stays "nothing clinically meaningful silently disappears", and it is now checkable without a semantic segmentation step: count spans in the paste, count dispositions, compare.

**One dependency this exposes:** the span boundaries come from the paste format. Line breaks and speaker turns are only usable if the signer's paste preserves them. We still have not seen an example, and this is the second question that cannot be answered without one.

## 4. Consensus confirmation

I confirm **items 1–20** of `CONSENSUS.md` as written. Two notes, neither a rejection:

- **#19** is compatible with §3 above: span-disposition coverage, with spans mechanically bounded and possibly mapping to several objects.
- **#15** now has a concrete split, stated in §1: IR → note is mechanical; source → IR is a semantic audit.

## 5. What is still open, from my side

Unchanged and honestly open: the exact kind taxonomy, whether `COURSE` remains a separate kind, and the operator vocabulary. I have opinions — five kinds, `COURSE` merged into `FACT` with a `time` field if E1 shows it drifting — but they are bets, not conclusions, and they should be decided by the experiment rather than by whoever argues last.

## 6. The one input still missing

The paste layout. Span coverage, provenance inference, and the whole ingest contract rest on it. Every design decision above assumes lines and speaker turns survive the paste; if they do not, the ingest layer needs a different mechanical boundary, and that is a design change, not a detail.
