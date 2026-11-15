# DOXIMITY

What the runtime is, what has actually been observed misbehaving, and what is only inferred. Both agents work locally. Neither can run Doximity. The signer runs it, and only that run counts as acceptance.

**Evidence boundary.** Claims here are limited to the raw artifacts present in this repository. Local mocks are labelled as local mocks; they are not Doximity evidence.

## What the runtime is

One template: a standing instruction block, separately attached files, and a short dispatcher prompt. No chaining of calls, no tool use, no carried state between runs, and no way to read back a previous stage's output inside the same run. Every stage must be self-contained in what it is handed.

## Observed in actual Doximity

1. **Semantic instability across runs.** Three runs of the same `06` contract on the same 60 objects produced 12, then 6, then 9 unacceptable routing differences. The membership moved between runs; only O32 and O57 were wrong every time. One run is one draw, not a sample.
2. **Schema non-compliance.** Run 3 emitted a free-text `REUSE` line instead of the contracted `distinct function:` field, and the mechanical validator failed it, after two runs that held the format. A stage can satisfy the semantics and still break its own output contract.
3. **Non-local prompt sensitivity.** A clause added to fix one object moved a different one: O51 went from `WORKUP` to `NEURO_HISTORY` in the run immediately after the prior-record clause was added. Edits do not act locally.

## Observed in local/mock execution only

4. **Prose-stage drift on identical input.** Two local `05` runs on one Handoff differed in bullet punctuation, capitalisation, and item merging — cosmetic on the surface, structural underneath: one run merged apixaban hold with its resume condition, the other split it. This proves the `05` contract is unstable under an LLM. It does **not** by itself establish a Doximity behaviour; treat a matching Doximity result as an inference until the signer runs it.

## Not observed, and not evidence

5. **Conversational wrapper.** Earlier project history records a sentence before and after output that resisted five suppression attempts. None of the five raw suppression outputs are in this repository, and no run on this branch shows the behaviour. It is unconfirmed here; strip defensively when copying, and do not cite it as an established limitation.

**Coverage gap.** This repository does not contain every Doximity test the signer recalls. Only the three raw `06` runs under `runs/2026-11-14-06-doximity/` are canonical Doximity artifacts here. Missing historical tests should be imported before they are treated as evidence.

## What follows for design

**More prompt prose is not automatically a fix.** The errors moved non-locally across runs, and one correction caused a different regression. Before adding a rule, separate a prompt defect from platform or model stochasticity — otherwise each revision trades one error for another and looks like progress.

- A validator that passes proves the format, never the content. Both are required.
- One run is never an acceptance artifact. Reproducibility is tested, not assumed.
- No stage may depend on state another stage produced in an earlier call.
- When a stage is unstable, the artifact is the reviewed output plus the record of what varied — not a hand-picked good run presented as generated.

## Where the evidence is

| Path | Provenance |
|---|---|
| `runs/2026-11-14-06-doximity/run1..3.txt` | actual Doximity, raw |
| `artifacts/06_doximity_run3.md` | actual Doximity, scored |
| `runs/2026-11-14-p002/ap_run1.txt`, `ap_run2.txt` | local/mock |
| `DECISIONS.md` D-006 | production `06` unresolved |
| `STATUS.md` | current `05` stability state |
