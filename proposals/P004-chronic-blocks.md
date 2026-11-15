# P004 — chronic problems get their own block

**Status:** draft, awaiting review. Not implemented.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `oracles/ap_ledger_v4.txt` (new, append-only), `tests/acceptance/`, `runs/`, `STATUS.md`.
**Does not affect:** substrate, `01`, `02`, `04`, `05` contract, `06`, `07`, the six kinds.

---

## 1. What the signer asked for

In the exchange of 2026-11-14 the signer drew a two-block A/P for the frozen case: one block for the post-stroke seizure, one shorter block for the chronic left MCA infarct, with the infarct block carrying secondary prevention. Their words are in `channel/to-chatgpt.md`, entry 21:35.

Current `03` produces one block for the seizure and one for the memory concern. The infarct is evidence inside the seizure block, and its medications are the seizure block's plan items. That is what this proposal changes.

## 2. The rule

> A chronic neurologic problem gets its own block when the encounter contains a management decision directed at it. A chronic problem with no management in this encounter does not get a block; it stays evidence or history.

Three consequences:

- The trigger is management, not diagnosis. `known left MCA infarct` alone is evidence. `apixaban held, to resume once MRI excludes hemorrhage` is a decision about the infarct's secondary prevention, so the infarct earns a block.
- The block is short by construction: it carries its label, the facts that describe it, and the management directed at it. It is not a second full problem workup.
- Ordering stays acuity first, then management weight. The active seizure precedes the chronic infarct; the memory concern, explicitly not today's issue, follows both.

This is a rule, not a per-case preference, because a preference cannot be executed twice the same way. If the signer wants exceptions, they are made at review.

## 3. Partition — one home per object

`03` assigns each retained object to exactly one block. The A/P branch has no `REUSE`, so a fact that matters to two blocks must be assigned to the one it primarily describes.

| Object | Now | Proposed | Why |
|---|---|---|---|
| O7, O53 | P1.EVIDENCE | P2.EVIDENCE | the infarct block's own label and record |
| O8 | P1.COURSE | P2.COURSE | the infarct's date |
| O9, O54 | P1.EVIDENCE | P2.EVIDENCE | residual deficit of the infarct |
| O11, O30, O31 | P1.MANAGEMENT | P2.MANAGEMENT | home regimen continued |
| O12, O25 | P1.MANAGEMENT | P2.MANAGEMENT | apixaban held, resume condition |
| O18, O19 | P1.EVIDENCE | P1.EVIDENCE | encephalomalacia and no new lesion establish the seizure substrate |
| O3–O6, O13–O15, O17 | P1 | P1 | unchanged |
| memory objects | P2 | P3 | renumbered, content unchanged |
| P2 label | O49 | O7 | the infarct block is labelled from its own object |

**Open cell — O10 `atrial fibrillation`.** It is currently P1.EVIDENCE and does not establish the seizure. It is not the infarct's stated etiology either: nothing in the encounter says the stroke was from AF. Three options, for review:

1. `P2.EVIDENCE` as context for why secondary prevention matters — defensible, not an etiology claim.
2. `DISCARD` — strict, and the note then never mentions AF, although the patient is on apixaban for it.
3. Leave it in P1 — indefensible under the exclusive evidence rule.

I propose 1, and a substrate object in a later version carrying the signer's `unanticoagulated AF` sentence so the infarct block can state its own etiology.

## 4. Oracle

`oracles/ap_ledger_v4.txt`, append-only. `v3` is untouched. The diff is seven assignments moving plus the block renumbering; `check_ledger.py` must be told the new population is still 59.

The memory block moves from P2 to P3. This is a mechanical rename, not a semantic change, and it is the part most likely to break a downstream test that assumed two problems.

## 5. Effect on P003

P003's acceptance target names two problems. With P004 it is three. The rendering rules do not change — the same `05` writes each block — but the invariant set does:

- I1 (problem count and order) becomes 3, ordered seizure → infarct → memory.
- I5/I6 gain the infarct's plan decisions and lose them from the seizure block.
- The trace table gains a block column.

P003 must therefore land before P004 in implementation order, or the three-run baseline is measured against a structure that is about to change. I propose: implement P003, run the three-run protocol against the two-block oracle as a stability baseline, then implement P004 and re-run. Two baselines, not one — the second measures the structural change, the first measures the rendering change.

## 6. Risks

- **Block inflation.** Every chronic diagnosis with a medication becomes a block. The management trigger is meant to stop that: a medication the patient takes but nobody decided anything about this encounter does not qualify. `Continue amlodipine` is a decision; a listed home med is not.
- **The infarct block duplicates the seizure line's cause.** The line says `post-stroke seizure from chronic L MCA infarct`; the infarct block says `chronic L MCA infarct`. That repetition is intended — one names the cause of the seizure, the other is its own problem — but it is the first thing to check in review.
- **O10.** Leaving AF out entirely is a real information loss; keeping it as context is a judgement. Flagged rather than settled.

## Out of scope

Substrate, `01`, `02`, `04`, `05` contract, `06`, `07`, the six kinds, and any change to the body note.
