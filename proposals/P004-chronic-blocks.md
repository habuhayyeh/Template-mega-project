# P004 v2 — chronic problems get their own block

**Status:** v2, revised after `reviews/P004-original-branch.md` and the signer's scope decision. Awaiting review. Not implemented.
**Supersedes:** P004 v1.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `oracles/ap_ledger_v4.txt` (new, append-only), `tests/acceptance/`, `runs/`, `STATUS.md`, `DECISIONS.md` (D-015 recorded; D-016 at approval).
**Does not affect:** substrate, `01`, `02`, `04`, `05` contract, `06`, `07`, the six kinds.

---

## 1. The rule, and its status

The signer chose the general rule, not a case-specific exception:

> A chronic neurologic problem gets its own shorter A/P block when the encounter contains a management decision directed at that problem.

Recorded as **D-015**. The guardrails are part of the decision, not commentary:

- Diagnosis alone does not create a block.
- A listed home medication alone does not create a block.
- The management decision must be **source-grounded as directed at that chronic problem in this encounter**. Do not infer the target from general clinical knowledge or drug class.
- Active problems stay ordered ahead of chronic managed problems.
- A chronic block stays short: problem-defining facts, the reasoning that explains it, and the management directed at it.
- A non-neurologic problem does not become a block unless it materially affects neurologic assessment or management under the existing rules.

Why a rule and not a preference: a preference cannot be executed twice the same way, and the signer has said consistency matters more than fit (channel, 21:35).

## 2. Partition — one home per object

The A/P branch has no `REUSE`, so each retained object has exactly one block.

| Object | Now | Proposed | Why |
|---|---|---|---|
| O7, O53 | P1.EVIDENCE | P2.EVIDENCE | the infarct block's label and record |
| O8 | P1.COURSE | P2.COURSE | the infarct's date |
| O9, O54 | P1.EVIDENCE | P2.EVIDENCE | residual deficit of the infarct |
| O11, O30, O31 | P1.MANAGEMENT | P2.MANAGEMENT | home regimen continued |
| O12, O25 | P1.MANAGEMENT | P2.MANAGEMENT | apixaban held, resume condition |
| O18, O19 | P1.EVIDENCE | P1.EVIDENCE | encephalomalacia and no new lesion establish the seizure substrate |
| O3–O6, O13–O15, O17 | P1 | P1 | unchanged |
| memory objects | P2 | P3 | renumbered, content unchanged |
| O10 | P1.EVIDENCE | **DISCARD** | see §3 |

The seizure block keeps the semiology, the durations, the CT, the sodium trend and the encephalomalacia. The infarct block carries its own facts and the secondary-prevention decisions. Memory becomes P3.

## 3. O10 `atrial fibrillation` — discarded

Under the accepted exclusive evidence rule, O10 does not establish, confirm, localise, refute, discriminate, or explain uncertainty for either claim. It cannot be promoted to the infarct's etiology because the source never says the stroke came from AF.

So O10 is `DISCARD` from the A/P. It stays available to the body branch through its own routing, where it already appears. The A/P does not need to name every comorbidity.

Consequence worth stating: the A/P will not mention AF at all, although the patient is on apixaban. That is the honest output of this substrate. A later substrate carrying the signer's `unanticoagulated AF` sentence would let the infarct block state its own etiology; until then the note cannot.

## 4. D-014 is superseded, explicitly

`D-014` says the residual expressive aphasia stays out of the A/P. The signer's approved chronic-infarct example places it under that block. Both cannot stand.

At approval of P004, record **D-016**, naming D-014:

> D-016 supersedes D-014 for the chronic-infarct context. Residual expressive aphasia may render under the chronic infarct block when it describes that problem. It remains excluded from the seizure block, and the reasoning in D-014 — that a sequela of the infarct is not evidence for the seizure — stands.

Not a silent reversal. It changes what one block says because the signer added a block that owns the fact.

## 5. Oracle

`oracles/ap_ledger_v4.txt`, append-only; `v3` untouched. Seven assignments move, the memory block renumbers P2 → P3, and O10 joins the discard set. The A/P population stays 59.

Renumbering is the most likely thing to break a downstream test that assumed two problems. `check_ledger.py` does not read P-numbers, but anything that prints or scores blocks does.

## 6. Effect on P003

P003's acceptance target names two problems; with P004 it is three. The rendering rules do not change. The invariants do:

- I1 becomes three problems, ordered seizure → infarct → memory.
- I5/I6 gain the infarct's decisions and lose them from the seizure block.
- The trace table gains a block column.

Implementation order: P003 first, three-run baseline against the two-block oracle, then P004 and a second baseline. Each run set measures one change.

## 7. Risks

- **Block inflation**, contained by the management trigger and the source-grounding guardrail. `Continue amlodipine` is a decision; a drug merely listed is not.
- **The cause appears twice by design** — once on the seizure line, once as the infarct block's own label. Intended, and the first thing to check in review.
- **AF disappears from the A/P.** Accepted in §3. If the signer wants it visible, the substrate has to say why it matters.

## Out of scope

Substrate, `01`, `02`, `04`, `05` contract, `06`, `07`, the six kinds, the body note.
