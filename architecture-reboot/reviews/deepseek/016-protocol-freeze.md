# DeepSeek response 016 — protocol freeze: all six accepted

Yes to all six. Two clarifications to keep the freeze tight.

---

## 1. Accepted

1. **No self-scoring.** A model reporting PASS is a claim, not evidence. Only contract-required failure states are emitted; scoring lives in CHECK/AUDIT, outside Doximity.
2. **Four run types** — artifact batch, replicated same-order batch, diagnostic single-case trace, robustness/order test. Clean taxonomy; each answers a different question.
3. **The trace is a probe.** Observing changes behaviour; a trace result localises, it never certifies.
4. **No frozen size threshold.** Mine was invented; measure.
5. **Baseline = source package + signer-approved target note.** Assertions derived, ambiguities escalated.
6. **Scorer negatives are offline; runtime invalid probes are separate.** Different instruments, different failure modes.

Optimisation target accepted: assertions per artifact, not checkpoints per case.

## 2. Clarification on (1) — keep the emitted failure vocabulary to one token

If the note is allowed to emit failure states, that is a surface the model can use to avoid rendering. Keep it to a single `CONTRACT_ERROR`, no taxonomy, consistent with consensus #11. A rich error vocabulary invites the model to explain itself instead of failing.

## 3. Clarification on (3) — trace results cannot be acceptance evidence

State it as a rule, not a caution: a diagnostic-trace run may be used to localise a defect but never to satisfy an acceptance criterion, because the trace itself changes what is being measured. Otherwise someone will eventually certify a batch from a trace run and the distinction will be lost.

---

**Position:** protocol frozen from my side. Phase 0 is the next thing, and it needs the signer's go-ahead.
