# DeepSeek response 015 — Doximity experimental protocol

**Verdict:** sound design. Five answers, one addition, and one warning about the batch idea.

---

## 1. All checkpoints in a 10-case batch — no, and we have evidence

A 10-case batch with five checkpoints each is roughly fifty structured outputs in one response. Our own record says that fails: Doximity broke its own output schema on the **third identical run** of a single stage with a sixty-line ledger, having complied twice.

Recommendation:

- **batches carry coverage, not checkpoints.** Per case: final note plus a one-line status. Nothing else.
- **checkpoint exposure is a single-case instrument**, used when localisation matters.
- if a batch must expose structure, keep it under ~10 KB total and expect decay beyond that.

The batch is for "does it work across variety", the single case is for "where did it break". Conflating them is how a batch failure becomes unattributable.

## 2. Three fresh runs — a gate, not a rate

Three runs are enough to *fail* a stage (any difference = fail, and our failures showed up within three). They are not enough to *claim stability*, because they cannot distinguish 90% from 60%.

Use three as the default gate, and scope the claim accordingly: "passed 3/3 on this case" rather than "reproducible". A rate claim needs either more runs on the expensive path or a much narrower case set.

## 3. The signer's baseline — ask for one artifact, not five layers

B0–B4 is coherent, but it is four artifacts the signer does not already produce. That is how a baseline becomes a burden and then becomes stale.

Ask for the one thing they make anyway: **the finished note for the case**. We derive B1–B4 from it, mark every derived assertion, and the signer signs off on one page: the derived assertions plus the three or four we flagged as ambiguous.

The signer's judgement should be spent on disagreement, not on authoring structure.

## 4. Order perturbation plus single-case controls — insufficient on its own

Order perturbation confounds two things: position effects and ordinary run variance. If a batch with shuffled order scores the same, you cannot tell whether the order had no effect or the variance swamped it.

Add the cheapest control: **the same batch, twice, same order.** Compare run-to-run on identical order first. Only then does a difference under perturbation mean position.

## 5. First divergence — correct, with one precondition

Assertion-level first-divergence is the right isolation mechanism, and it only works if:

- assertions are ordered by pipeline stage;
- each assertion has **exactly one owning submodule**.

An assertion that spans two modules makes "earliest owner" a guess. The rule should be: if an assertion needs two owners, it is two assertions.

## 6. The addition — a known-bad batch

Nothing in the protocol proves the scorer can detect a failure. A scoring pipeline that passes everything looks identical to a system that works.

Add one deliberate negative control per batch campaign: a batch with one seeded defect from the historical list (`C13 over-inclusion` is the easiest), and require the scorer to localise it to the right case and the right submodule. If it cannot, the score means nothing.

## 7. What I would not do

Do not run the batch phase before Phase 0 controls exist. A batch produces more evidence than our current tooling can score, and unscored evidence reads as success.
