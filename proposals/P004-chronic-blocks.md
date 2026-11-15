# P004 v4 — chronic problems get their own block

**Status:** v4, revised after `reviews/P003-v8-P004-v3-original-branch.md`. **HELD**: production `03` cannot derive the block from the current representation without violating D-015. Table corrections applied. Not implementable until a representation proposal exposes the management target.
**Supersedes:** P004 v1.
**Affects:** `pipeline/03_SELECT_ORGANIZE.md`, `oracles/ap_ledger_v4.txt` (new, append-only), `tests/acceptance/`, `runs/`, `STATUS.md`, `DECISIONS.md` (D-015 recorded; a further entry at approval, ID assigned then).
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

**This proposal is blocked, and the block is architectural.** Production `03` reads the frozen representation. That representation does not say which problem a management item serves. Under D-015, `03` may not infer it. So the production rule cannot be implemented against this substrate at all — the oracle can record the signer’s adjudication, but the stage cannot derive it. Sequence: P003 first, then a representation proposal that exposes the management-to-problem relation, then this.

Why a rule and not a preference: a preference cannot be executed twice the same way, and the signer has said consistency matters more than fit (channel, 21:35).

## 2. Partition — one home per object

The A/P branch has no `REUSE`, so each retained object has exactly one block.

| Object | Now | Proposed | Why |
|---|---|---|---|
| O7, O53 | P1.EVIDENCE | P2.EVIDENCE | the infarct block's label and record |
| O8 | P1.COURSE | P2.COURSE | the infarct's date |
| O9 | DISCARD (already) | DISCARD | duplicate of O54; O54 carries the deficit with prior-neurology provenance |
| O54 | P1.EVIDENCE | P2.EVIDENCE | residual deficit of the infarct |
| O11, O30, O31 | P1.MANAGEMENT | P2.MANAGEMENT | home regimen continued |
| O12, O25 | P1.MANAGEMENT | P2.MANAGEMENT | apixaban held, resume condition |
| O18, O19 | P1.EVIDENCE | P1.EVIDENCE | encephalomalacia and no new lesion establish the seizure substrate |
| O3–O6, O13–O15, O17 | P1 | P1 | unchanged |
| memory objects | P2 | P3 | renumbered, content unchanged |
| O10 | P1.EVIDENCE | **DISCARD** | see §3 |

The seizure block keeps the semiology, the durations, the CT, the sodium trend and the encephalomalacia. The infarct block carries its own facts and the secondary-prevention decisions. Memory becomes P3.

### 2.1 The rule and this table use different evidence standards

They do, and the difference has to be visible.

**A. The production rule.** `03` creates a chronic block only when the representation contains a source-grounded link between a management decision and that problem. Where the link is absent, `03` does not infer it from the drug's identity, its class, or clinical knowledge. On the current substrate, the atomic texts `on apixaban`, `Continue amlodipine 10 mg daily`, `Continue atorvastatin 80 mg`, `apixaban held since admission` do not by themselves say which problem they are directed at.

**B. The frozen-case adjudication.** For this synthetic case the signer placed apixaban hold/resume, amlodipine and atorvastatin in the chronic infarct block. `oracles/ap_ledger_v4.txt` may encode that as a reviewed oracle decision — an explicit adjudication by the signer, on the record — even though the atomic representation does not expose the link.

**Representation gap.** The oracle is therefore ahead of what the rule can derive. That gap is recorded, not papered over: the oracle is an adjudicated answer for one case, not evidence that `03` can produce it. Solving it inside P004 with medication heuristics is forbidden; the durable fix is a management-target relation in a later representation, and that is a separate proposal.

## 3. O10 `atrial fibrillation` — discarded

Under the accepted exclusive evidence rule, O10 does not establish, confirm, localise, refute, discriminate, or explain uncertainty for either claim. It cannot be promoted to the infarct's etiology because the source never says the stroke came from AF.

So O10 is `DISCARD` from the A/P. It stays available to the body branch through its own routing, where it already appears. The A/P does not need to name every comorbidity.

Consequence worth stating: the A/P will not mention AF at all, although the patient is on apixaban. That is the honest output of this substrate. A later substrate carrying the signer's `unanticoagulated AF` sentence would let the infarct block state its own etiology; until then the note cannot.

## 4. D-014 is superseded, explicitly

`D-014` says the residual expressive aphasia stays out of the A/P. The signer's approved chronic-infarct example places it under that block. Both cannot stand.

At approval of P004, record a new **D-###** — ID assigned at recording, not reserved here — naming D-014:

> The new decision supersedes D-014 for the chronic-infarct context. Residual expressive aphasia may render under the chronic infarct block when it describes that problem. It remains excluded from the seizure block, and the reasoning in D-014 — that a sequela of the infarct is not evidence for the seizure — stands.

Not a silent reversal. It changes what one block says because the signer added a block that owns the fact.

## 5. Oracle

`oracles/ap_ledger_v4.txt`, append-only; `v3` untouched. The move set is larger than the table makes it look, and the P2 → P3 renumbering touches every memory line. **No count is stated here.** The oracle will be generated from the ledger and its diff measured; a hand-written count is how bookkeeping errors get into a proposal.

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
