# DeepSeek response 031 — architecture experiment program

Eight specs reviewed as a program. Verdict: **the set is sound and the individual designs are mostly well isolated. Six gaps, one of which changes the order of work.**

---

## 1. Program-level

**P1 — no negative control anywhere.** Every experiment scores correct behaviour; none demonstrates that the scorer can detect a failure. A scoring rig that passes everything is indistinguishable from a working system. One seeded-defect case per experiment (or one shared calibration case) closes this. It is not optional: AX-LEAK in particular cannot distinguish "no leakage" from "diff detector returning empty".

**P2 — all eight are pass/fail with 3 repetitions.** Fine for structural claims where any difference is a fail. Not fine for AX-I3, where the question is *boundary stability* — three runs cannot separate a stable boundary from a lucky one. AX-I3 needs either more repetitions on a single span or a smaller claim ("3/3 identical"), stated in the spec.

**P3 — no interaction test.** In one call, scale, leakage, and S4 density interact: a renderer that ignores raw source at small IR size may not at 3× size. One minimal crossed arm — AX-LEAK arm B at AX-SCALE's largest size — would say whether the pass claims compose. Without it, eight passes support eight separate claims and no integrated one.

**P4 — sample sizes are undefined.** "Small artifact batch first; full batch if stable" does not say how many cases constitute a batch, what the full set is, or what corpus the fixtures come from. The first case comes from the signer's ten; the program should say so and cap the count.

**P5 — no experiment covers cross-run object identity.** O-08 in the Phase 0 ledger. Every experiment holds input fixed and compares output; none checks whether the same object keeps the same id across two runs, which determines whether any diff-based scoring is meaningful at all. It is cheap: one case, two runs, compare id sets.

**P6 — two known risks are uncovered.** O-11 contradictory sources and O-10 paste-layout sensitivity. Both are S2/ingest behaviours the architecture now depends on, and neither has an experiment or a fixture family.

---

## 2. AX-S1S2-D

**Isolates:** yes, provided the ingest substrate is frozen from a *scored* ingest run or hand-built. If the substrate is produced by the same model in the same session, an ingest error reappears as a STRUCTURE error and the experiment blames the wrong module.

**Confound:** the assertions mix two kinds of claim. "No adoption verdict appears in S1" is structural and checkable. "Candidacy is correct" is semantic and judgemental. A case can pass structure and fail semantics, or the reverse, and the spec has one verdict. Split the score: structural leakage (reopens the interface) vs semantic correctness (contract/schema defect). Only structural failures justify reopening S1/S2.

**Reopen criterion is unquantified.** "Unavoidable across realistic cases" needs a number — for example, structural leakage in ≥1 of 10 fixtures across 3 runs.

## 3. AX-LEAK

Strongest design in the set. Two additions:

- **Arm 0 — no raw source visible.** Without it, arm A's fidelity may come from the source rather than the IR, and a pass would prove nothing about seam enforcement.
- **Two-call upper bound.** Render the same IR in a separate call with no source. That is the best fidelity achievable, and it tells you whether a leak-free result means "seams hold" or "the renderer is weak enough not to be tempted".

## 4. AX-S4

Accept as designed, including the refusal to collapse dimensions. One confound to state: with hand-frozen S1/S2/S3 outputs, this measures S4's **ceiling**, not its production behaviour. It should also include one arm where the frozen S3 output carries two approved representations — valid input, real ambiguity — because that is the condition the approval-safety rule exists for.

## 5. AX-I3, AX-T, AX-SCALE

- **AX-I3** — see P2. State the claim narrowly or raise repetitions.
- **AX-T** — the comparison risks being "prompt with trace request" vs "prompt without", not "instrumented" vs "uninstrumented". Hold everything constant but the trace instruction, and state that the measured effect includes the instruction itself.
- **AX-SCALE** — define the scaling variable (cases per call, objects per case, IR bytes) and label the result **platform-bound**: truncation is a Doximity property, not an architectural one. Do not let a scale failure reopen the module design.

## 6. AX-R2

Accept, with one methodological defect: the "minimum upstream representation" is constructed by the experimenter, so the outcome depends on their judgement — a representation that is too rich makes weak R2 look good, too poor makes it look bad. Use **two independent constructors** who do not see each other's work, and score both. Also, the signer must mark which differences from the target are acceptable in advance, or prose style differences will be scored as semantic failure.

## 7. AX-SHARED

Accept. Add one fixture the current design does not force: the shared action has **different rationales per problem** (not one rationale that happens to apply twice). That is the case where a one-owner representation is most likely to lose something, and it is absent from the current fixture shape. A second variant where the shared action must appear in both a body section and the A/P would stress section-scoping too.

---

## 8. What I would change in the order

1. **Calibration case first** (P1). If the scorer cannot fail, nothing downstream is evidence.
2. **AX-S1S2-D structural half**, since DC-001 is the change under test.
3. **Identity stability** (P5) — cheap, and it validates the diff method every other experiment relies on.
4. Then LEAK, S4, SHARED, R2, and finally I3 / T / SCALE, which are the most expensive and the least architecture-deciding.

AX-LEAK's arm 0 and P5 are a morning's work between them and they decide whether the rest is measurable at all.

---

## 9. What the program gets right

- Every spec states what it cannot prove.
- Failure interpretation is separated from pass criteria, and reopening is limited to structural evidence.
- AX-S4 and AX-SHARED both refuse to pre-freeze schema, which is the discipline the last month was missing.
- "A pass means only: passed under the tested frozen condition" is the correct sentence, and it should survive into every result report.
