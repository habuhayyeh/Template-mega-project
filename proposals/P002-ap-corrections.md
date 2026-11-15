# P002 v2 — A/P assembly and rendering corrections

**Status:** revised after review `db20d6b`. Awaiting review.
**Supersedes:** P002 v1 at `caccf81`.
**Affects:** `tools/check_ledger.py`, `oracles/` (new append-only version), `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`, `DECISIONS.md`, `tests/acceptance/`.
**Does not affect:** substrate, `01`, `02`, `03` semantics, `06`, `07`, the six kinds.

## What changed from v1

| # | v1 | v2 |
|---|---|---|
| 1 | imports unratified | D-011 ratifies them before anything else |
| 2 | not noticed | `check_ledger.py` contradicts `03` on MANAGEMENT → CLAIM_QUALIFIER; fixed first |
| 3 | "oracle unaffected" | oracle is stale; new append-only `ap_ledger_v3.txt` required |
| 4 | narrower `04` duplicate rule | `04` performs no semantic deletion at all |
| 5 | one reasoning bullet | no duplicated reasoning, no lost distinct reasoning |
| 6 | "keep the fuller" plan entry | current-plan semantic selection |
| 7 | standing-instruction exception | explicit current re-adoption only |
| 8 | validation used the legacy Handoff | real `04 → 05` from substrate + ledger |
| 9 | capitalisation | unchanged, approved |

## 1. Ratify the inherited baseline

D-011 records that the three imported contract edits are accepted as baseline, not re-proposed: `03` exclusive evidence eligibility and reasoning protection, `04` reasoning exemption from duplicate deletion, `05` reasoning rendering rules.

## 2. Reconcile `03` with `check_ledger.py`

`03` says adjudication is MANAGEMENT by kind and CLAIM_QUALIFIER by role. `tools/check_ledger.py` line 36 allows `MANAGEMENT → MANAGEMENT` only and rejects the approved exception.

Correction: permit `MANAGEMENT → CLAIM_QUALIFIER` as the single named exception, and nothing else. `MANAGEMENT → EVIDENCE`, `→ PRIMARY_CLAIM`, `→ COURSE` stay rejected. The validator gains one role, not a relaxation.

This is a task, not a design change: the contract already states the rule.

## 3. Corrected A/P oracle, append-only

`oracles/ap_ledger_v2.txt` implements the superseded evidence rule: O28 still `P1.EVIDENCE`, O53/O54 on P2, O23 still `P1.MANAGEMENT`, and further context objects still in P1 evidence. The `04/05` run that produced the current Handoff used a corrected ledger that was never committed.

Create `oracles/ap_ledger_v3.txt` — v2 is left untouched — applying the imported `03` rule:

| Object | v2 | v3 | Why |
|---|---|---|---|
| O9, O10, O26, O27, O41, O47, O48 | P1.EVIDENCE | DISCARD | context, unrelated normals, preference, baseline deficit |
| O28 | P1.EVIDENCE | DISCARD | preference; the plan carries the restriction |
| O53, O54 | P2.EVIDENCE | DISCARD | duplicates of O7 and O9 |
| O23, O39 | P1.MANAGEMENT | P1.CLAIM_QUALIFIER | adjudication language |

Then `python tools/check_ledger.py oracles/ap_ledger_v3.txt substrate/acceptance_v2.txt` must pass, and the result is recorded under `runs/`.

## 4. `04` stops deleting

`04` becomes a lossless dereference: every retained ID, its object text word for word, its provenance verbatim, in the field the ledger assigned. No completion-statement deletion, no duplicate deletion, no reasoning exemption needed because there is no deletion at all.

Rationale, accepted from the review: exact-duplicate removal already has a home in `03`'s one-fact-one-entry rule; rhetorical compression belongs in `05`. Retaining a narrowed dedup rule keeps OD-2 alive at the fidelity stage, where a deletion cannot be distinguished from a drop.

Consequence to be handled in `05`: near-duplicate entries now arrive there — `witnessed GTC` from [A] and [C], sodium twice, CT twice. `05` renders each fact once.

## 5. Reasoning criterion

Replace "one reasoning bullet" with:

> No duplicated reasoning; every distinct clinician-reasoning proposition survives; reasoning bullets appear after the factual evidence and before `Plan:`.

Two distinct propositions — confusion is postictal, and the MRI will adjudicate — are two bullets. O23 and O39 say the same thing and compress to one. Merging distinct propositions to hit a bullet count is forbidden.

## 6. Plan compression

Replace "keep the fuller" with:

> When entries describe the same action, retain the one that best represents the current clinician's plan. A later plan statement is not improved by being longer. Distinct conditions, rationales, or incompatible states are never merged.

`fluid restriction` (current consult) therefore beats `fluid restriction started` (earlier ED note), even though the second is longer.

## 7. Prior-record management

> A prior-record MANAGEMENT object does not become today's plan. It enters the plan only through a separate current-encounter MANAGEMENT object that re-adopts, continues, or restates it.

O52 `no further workup [D, 2025-06]` is dropped unless a current object re-adopts it. The system never infers that an old recommendation is still in force.

## 8. Validation through the real path

The legacy Handoff fixture cannot test `04` — it contains no O# ledger and no provenance flow. It is retained for isolated `05` tests only, and relabelled as such.

End-to-end acceptance path:

```text
inputs   substrate/acceptance_v2.txt
         oracles/ap_ledger_v3.txt
stage 1  python tools/check_ledger.py oracles/ap_ledger_v3.txt substrate/acceptance_v2.txt
stage 2  run 04_ASSEMBLE on both inputs        → runs/<date>-p002/handoff.txt
stage 3  run 05_WRITE_AP on that Handoff       → runs/<date>-p002/ap.txt
check    every generated sentence traces to a Handoff entry
score    against pipeline/AP_ANCHOR.md
```

Recorded for each stage: the exact input, the command, the exit code, the output.

**Execution reality, stated plainly.** Both agents are LLMs without Doximity access. Stages 2 and 3 above are engineering mocks executed in isolation, not the production platform. They can show whether the contract is coherent and whether the output regresses; they cannot establish that Doximity will produce it. The acceptance decision requires a Doximity run by the user, and P002 does not claim one.

## 9. Capitalisation

Approved as proposed: first word after `//` is capitalised.

## 10. Implementation order

1. D-011 ratification.
2. `check_ledger.py` management-role exception; fixture proving it rejects the other three roles.
3. `oracles/ap_ledger_v3.txt`; validator PASS recorded.
4. `04` rewrite to lossless assembly.
5. `05` rules: capitalisation, reasoning criterion, plan selection, prior-record management, per-fact evidence.
6. Mock run end to end; record outputs and the traceability check.
7. Subject to §8, request a Doximity acceptance run by the user before the status update.

## 11. Risks

- Removing `04` deletion moves all compression into `05`, which is already the most rule-dense stage. If `05` under-compresses, the A/P lengthens rather than loses facts — the safer direction.
- `ap_ledger_v3.txt` discards eight evidence objects. Each was tested against the exclusive rule and each discard is listed above; none is a fact the note body loses, since the body branch carries them independently.

## Out of scope

The 14-bullet problem is resolved by the `03` rule and the new oracle, not by `05`. Nothing here touches the substrate, `06`, the section branch, or the six kinds.
