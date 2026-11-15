# P002 v3 — A/P assembly and rendering corrections

**Status:** revised after review `9ce1268` (v2 review). Awaiting review.
**Supersedes:** P002 v2 at `3654a08`.
**Affects:** `tools/check_ledger.py`, `oracles/` (new append-only version), `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`, `DECISIONS.md`, `STATUS.md`, `tests/acceptance/`.
**Does not affect:** substrate, `01`, `02`, `03` semantics, `06`, `07`, the six kinds.

## What changed from v2

| # | v2 | v3 |
|---|---|---|
| 1 | validator command reversed; `check_ledger.py` cannot read `allocate.py` output | real chain fixed, and the validator made to consume the canonical allocator format |
| 2 | O53/O54 discarded as duplicates | both to `P1.EVIDENCE`; `05` compresses them |
| 3 | STATUS updated only after the Doximity run | STATUS carries engineering and canonical states separately |

Everything else in v2 stands as approved.

## 1. Repair the validator path

v2 wrote `check_ledger.py ledger objects` — reversed — and, worse, the tool does not read the six-kind substrate. It expects the old heading-based allocation, while `allocate.py` emits:

```text
O# | BUCKET | KIND | text | [provenance]
```

Two components are out of sync with already-approved architecture. Repair, no redesign:

1. `tools/allocate.py substrate/acceptance_v2.txt` → `runs/<date>-p002/allocation.txt`.
2. `tools/check_ledger.py` parses that format directly: `O#`, `BUCKET`, `KIND`, text, provenance. The `NOT_ALLOCATED` demographic row (O1) is accepted and excluded from the ledger population, so the expected count is **59 assignments**, not 60.
3. `tools/check_ledger.py runs/<date>-p002/allocation.txt oracles/ap_ledger_v3.txt` — objects first, ledger second, as the tool's own usage demands.
4. Exit 0 recorded, with the command and output, under `runs/`.

The role exception from v2 (`MANAGEMENT → CLAIM_QUALIFIER`) lands in the same file, and the fixture proves the other three roles are still rejected.

## 2. Corrected A/P oracle, append-only

`oracles/ap_ledger_v2.txt` implements the superseded evidence rule. `oracles/ap_ledger_v3.txt` applies the accepted `03` rule; v2 is untouched.

| Object | v2 | v3 | Why |
|---|---|---|---|
| O9, O10, O26, O27, O41, O47, O48 | P1.EVIDENCE | DISCARD | context, unrelated normals, preference, baseline deficit |
| O28 | P1.EVIDENCE | DISCARD | preference; the plan carries the restriction |
| O53, O54 | P2.EVIDENCE | **P1.EVIDENCE** | restatements of O7/O9, wrongly attached to the memory problem |
| O23, O39 | P1.MANAGEMENT | P1.CLAIM_QUALIFIER | adjudication language |

O53/O54 are neither exact duplicates under the closed discard set nor irrelevant. They are restatements of P1 facts, and with `04` lossless the place to collapse them is `05`. No new discard reason is proposed.

Resulting P1 evidence: O3, O5, O7, O13, O14, O17, O18, O19, O43, O44, O45, O53, O54 — thirteen entries, several of them near-duplicates by construction, which is the compression `05` now owns.

## 3. `04` stops deleting

Unchanged from v2 and approved: `04` becomes a lossless dereference — every retained ID, its text word for word, its provenance verbatim, in the field the ledger assigned. No completion-statement deletion, no duplicate deletion.

Exact-duplicate removal stays in `03`; rhetorical compression in `05`. Keeping any deletion at the fidelity stage keeps OD-2 alive where a deletion cannot be told from a drop.

## 4. Reasoning criterion

> No duplicated reasoning; every distinct clinician-reasoning proposition survives; reasoning bullets appear after the factual evidence and before `Plan:`.

O38 (confusion is postictal) and the MRI adjudication (O23/O39, compressed to one) are two bullets. Merging distinct propositions to hit a count is forbidden.

## 5. Plan compression

> When entries describe the same action, retain the one that best represents the current clinician's plan. A later plan statement is not improved by being longer. Distinct conditions, rationales, or incompatible states are never merged.

`fluid restriction` (current consult) beats `fluid restriction started` (earlier ED note).

## 6. Prior-record management

> A prior-record MANAGEMENT object does not become today's plan. It enters the plan only through a separate current-encounter MANAGEMENT object that re-adopts, continues, or restates it.

O52 `no further workup [D, 2025-06]` is dropped unless a current object re-adopts it.

## 7. Capitalisation

Approved: first word after `//` is capitalised.

## 8. STATUS carries two states

```text
P002 implementation:      engineering/mock validated | in progress | not started
Doximity acceptance:      PENDING | PASS | FAIL
Canonical acceptance:     NOT YET ESTABLISHED | established <run path>
```

Rule: **mock validation establishes engineering coherence, never Doximity acceptance.** STATUS moves after the mock run and architectural diff review; the user's Doximity run then advances the second and third lines. The repository never claims production acceptance it has not observed.

## 9. Validation path, executable

```text
allocate  python tools/allocate.py substrate/acceptance_v2.txt
                              → runs/<date>-p002/allocation.txt
check     python tools/check_ledger.py runs/<date>-p002/allocation.txt oracles/ap_ledger_v3.txt
                              → exit 0 recorded
stage 04  run 04_ASSEMBLE on substrate + v3 ledger
                              → runs/<date>-p002/handoff.txt
stage 05  run 05_WRITE_AP on that Handoff
                              → runs/<date>-p002/ap.txt
trace     every generated sentence traces to a Handoff entry
score     against pipeline/AP_ANCHOR.md
```

The legacy Handoff fixture is retained for isolated `05` tests only and does not claim to exercise `04`.

**Execution reality.** Stages 04 and 05 here are mocks executed by an LLM, not Doximity. They establish contract coherence and regression, not production behaviour.

## 10. Implementation order

1. D-011 ratification (already on main at `6178a76`).
2. `check_ledger.py`: allocator-format parsing, `NOT_ALLOCATED` handling, MANAGEMENT role exception, fixture coverage.
3. `oracles/ap_ledger_v3.txt`; validator PASS recorded.
4. `04` rewrite to lossless assembly.
5. `05`: capitalisation, reasoning criterion, plan selection, prior-record management, per-fact evidence.
6. Mock run end to end; record outputs and the traceability check.
7. STATUS to `engineering/mock validated`, `Doximity acceptance: PENDING`.
8. Request the user's Doximity run.

## 11. Risks

- `05` now owns all compression. Under-compression lengthens the A/P visibly; that is the safer failure, and the first Doximity run decides whether more guidance is needed. No further `05` rules are added pre-emptively.
- The validator repair touches a tool that has not been exercised against the current allocator. The fixture and the 59-assignment count are the guard.

## Out of scope

Substrate, `06`, the section branch, the six kinds, and any second discard reason.
