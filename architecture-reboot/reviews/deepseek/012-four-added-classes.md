# DeepSeek response 012 — the four added classes, and where they belong

**Answer: yes, I accept all four.** They are real and I have seen each one. But two of them are not submodule failures, and putting them in the submodule matrix would assign responsibility to modules that cannot control it.

---

## 1. Accepted, with owners

| Class | What it is | Owner |
|---|---|---|
| **C11** contract contradiction / duplicate rule authority | two clauses governing one decision; the writer obeys different ones on different runs | **M6 BUILD**, not any submodule |
| **C12** stable bad output from representation incompleteness | faithfully rendered, clinically thin — `The MRI to show.` | **S4** (operator choice) and **R1** (operator fixed text) |
| **C13** over-inclusion / wrong note use | a fact included that the note does not need, or used in the wrong place — O54 as seizure evidence | **S3** (retention) and **S4** (placement) |
| **C14** non-local regression after a contract change | fixing object A moves object B — O51 after the prior-record clause | **the acceptance protocol**, not a module |

**C11 belongs to the build.** The old `05` ended up saying "reasoning first" and "reasoning last" in adjacent sections. No runtime module can detect that it is being governed by contradictory instructions; the compiler can.

**C14 belongs to the change process.** It is not a defect in any module — it is the observation that a local edit has non-local effects, which is true of every system. The control is: after any contract change, rerun the frozen acceptance case and diff the IR. If that is not routine, C14 will keep happening regardless of the architecture.

## 2. C12 is the one I would add to the matrix, and it is underrated

`MRI to show.` is the clearest example of a failure that no check catches: it is faithful, stable, grammatical, and clinically useless. The token guard passes it. The line-to-unit check passes it. Nothing in the design objects.

It has two owners and needs two checks:

- **S4** — an operator whose fixed text carries less than its head should not be selected when a fuller operator exists. Detectable by comparing rendered length against head length, with a floor.
- **R1** — an operator that discards a member's payload is malformed by definition. Detectable by checking that every member's content tokens survive into the line.

That second check is the same token containment as I3, applied at the other end. It is worth stating explicitly, because "the renderer may only delete words" is exactly the liberty that produced a one-clause bullet from a two-clause thought.

## 3. On the DO / AVOID / DETECT / FAILURE BEHAVIOR requirement

Accepted, and `DETECT` is the column that matters. A spec without a detection method is a preference, and the old system was full of them.

One addition: `DETECT` should say **which of the three validation modes** answers it — mechanical, semantic audit, or human — because a spec that says "detect this" without saying how is how we ended up with validators that could not be written.

## 4. What I would not do

Do not put C11 and C14 in the submodule matrix as if a module owns them. The matrix is a map of where defects enter the pipeline; two of these enter outside it. Mixing them in makes the matrix unusable for its actual purpose — deciding which checks live where.
