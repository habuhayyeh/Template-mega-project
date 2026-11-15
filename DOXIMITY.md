# DOXIMITY

What the runtime is, what it does unreliably, and how to read every claim in this repository in that light.

Both agents work locally. Neither can run Doximity. Local runs are engineering mocks and prove contract coherence only; they say nothing about production behaviour. The signer runs Doximity, and only that run counts as acceptance.

## What the runtime is

One template: a standing instruction block, separately attached files, and a short dispatcher prompt. There is no chaining of calls, no tool use, no carried state between runs, and no way to read back a previous stage's output inside the same run. Every stage must therefore be self-contained in what it is handed.

## What the runs show

Evidence lives in `runs/2026-11-14-06-doximity/` (three raw ledgers) and `artifacts/06_doximity_run3.md` (scored).

1. **Semantic instability.** Three runs of the same `06` contract on the same 60 objects produced 12, then 6, then 9 unacceptable routing differences. The membership moved between runs; only O32 and O57 were wrong every time. A single run is not a sample of behaviour, it is one draw.
2. **Schema non-compliance.** Run 3 emitted a free-text `REUSE` line instead of the contracted `distinct function:` field, and the mechanical validator failed it. The same format had been followed in the two previous runs. A stage can satisfy the semantics and still break its own output contract.
3. **Prompt sensitivity.** A clause added to fix one object moved a different one: O51 went from `WORKUP` to `NEURO_HISTORY` in the run immediately after the prior-record clause was added. Edits do not act locally.
4. **No conversational wrapper observed here.** The three `06` runs and the P002 `05` runs begin at their first token. Earlier project history records a conversational sentence before and after output that resisted five suppression attempts; it is not reproduced in any run on this branch, so treat it as unconfirmed here and strip defensively when copying.
5. **Formatting drift in prose stages.** Two `05` runs on one Handoff differed in bullet punctuation, capitalisation, and item merging. The differences were cosmetic on the surface and structural underneath — one run merged apixaban hold with its resume condition, the other split it.

## What follows for design

- A validator that passes proves the format, never the content. Both are required.
- One run is never an acceptance artifact. Reproducibility is a property to be tested, not assumed.
- No stage may depend on state another stage produced in an earlier call; it must be given everything it needs.
- An instruction that fixes a defect can create another elsewhere. One change at a time, and re-score the whole output, not the fixed line.
- When a stage is unstable, the artifact is the reviewed output plus the record of what varied — not a hand-picked good run presented as generated.

## Where the evidence is

| Path | What it holds |
|---|---|
| `runs/2026-11-14-06-doximity/run1..3.txt` | the three raw `06` ledgers |
| `artifacts/06_doximity_run3.md` | run 3 scored, with the drift table |
| `runs/2026-11-14-p002/ap_run1.txt`, `ap_run2.txt` | two `05` runs, same input |
| `DECISIONS.md` D-006 | production `06` unresolved |
| `STATUS.md` | current `05` stability state |
