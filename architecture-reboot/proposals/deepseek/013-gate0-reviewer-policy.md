# DeepSeek 013 — Gate 0 semantic reviewer policy

**Status:** PROPOSAL / NOT APPLIED
**Decision requested:** keep the current three-human rule, or replace it with the bounded panel below.
**Scope:** Gate 0 semantic calibration only. No predicate meaning, seed, scorer, architecture or clinical
acceptance change is proposed.

---

## 1. What the current rule buys

The current rule is not a statistical proof of clinical correctness. It is a **calibration control**:

- three independent blinded judgments reduce the chance that one judge's blind spot, fatigue or
  automation bias becomes the calibration result;
- requiring all three to detect the seeded defect prevents a 2/3 majority from passing a scorer that
  misses a known defect;
- requiring all three to satisfy `FULL_SILENCE-WITHIN-LAYER` prevents a judge who sees the defect from
  excusing unrelated over-firing;
- blinding to seed id, expected predicate and mutation metadata prevents the judge from reading the
  answer.

What it does **not** prove:

- that the scorer detects defects nobody seeded;
- that the judge panel generalizes beyond these seeds;
- that the underlying note is clinically correct;
- that three humans are statistically independent — shared training, specialty and project context can
  correlate them.

The current rule is defensible but operationally unavailable: the project has one signer and two AI
agents, and ChatGPT/DeepSeek cannot be counted as humans.

## 2. What actually needs a human

The active semantic predicates are:

- `S1-CAND-01` — candidacy: is this a neurologic subject with its own assessment question?
- `S2-ADOPT-01` — adoption: does the verdict match the source/oracle?
- `S2-REP-01` — representation support: do the members and relations semantically support the claim?

These require domain understanding, but Gate 0 is asking a narrower question than clinical acceptance:

> can an independent judge detect this planted semantic defect under blinding?

The signer's clinical judgment is necessary for the **clinical** part — especially candidacy and
adoption — and for final product acceptance. It is not necessary for every mechanical seed, and routine
recalibration should not consume the only clinician's time on branches a blinded panel can decide
reliably.

The policy should therefore preserve a human clinical anchor without pretending that three humans are
available.

## 3. Options compared

| option | panel | independence | main failure mode | operational cost | Gate 0 claim | harness change |
|---|---|---|---|---|---|---|
| A — keep current | 3 independent humans | strongest available | not operationally available | 21 human judgments for the current 7 semantic packets | human panel detection + specificity | none |
| B — signer + 2 LLM | 1 signer/clinician + 2 LLM judges | cross-family LLM independence; signer is accountable but not statistically independent | correlated LLM error; signer anchoring | 7 signer + 14 LLM judgments | human-anchored panel detection | judge type, model identity, panel composition |
| C — signer + 1 LLM + mechanical | 1 signer + 1 LLM + deterministic controls | weak: deterministic controls cannot decide semantic support | false confidence; one semantic judge only | 7 signer + 7 LLM | mechanical branches plus one semantic judgment | branch reclassification |
| D — model-only + spot-check | LLM panel, signer samples | weakest; no human per packet | correlated error escapes spot-check | lowest | model consensus only | judge type, sampling metadata |
| **E — signer-first + 2 fresh cross-family LLM** | 1 signer/clinician + 2 fresh LLM judges from different families | cross-family; signer verdict recorded before LLM verdicts; no shared answer key | residual correlated LLM error; signer may still recognize seeds | 7 signer + 14 LLM | human-anchored, sequenced panel detection | judge type, model family/version, sequence, signer-first enforcement |

Option C is rejected for the same reason review 080 rejected a mechanical pre-filter as a substitute
for a semantic judgment: if the mechanical check fully decides the branch, the branch is mechanical and
should be represented as such; if it does not, it cannot replace a judge.

Option D is rejected for Gate 0 semantic acceptance. It can remain useful for non-semantic mechanical
checks and for triage, not for the verdict.

Option A remains the fallback if genuine human judges are available. It is not practical as the default.

## 4. Recommendation — Option E

Use a **three-member sequenced panel** for each semantic packet:

1. **one signer/clinician**, who records a verdict first, before seeing either LLM verdict;
2. **two fresh LLM judges from different model families**, each seeing only the blinded packet;
3. all three must return `FIRED` and satisfy within-layer specificity;
4. `2/3` is a calibration **failure**, not a pass;
5. any `UNDECIDABLE`, missing judgment or duplicate judge keeps the packet `INCOMPLETE`;
6. the signer's clinical authority remains separate from scorer calibration.

The policy applies only to the three active semantic predicates. Mechanical predicates remain one
deterministic run.

### Why this is the smallest defensible replacement

- It preserves the property that matters for calibration: **independent detection under blinding**, with
  a human clinical anchor on every packet.
- It removes the impossible requirement for three humans while not counting an AI agent as a human.
- Cross-family judges reduce correlated error compared with two instances of one model.
- Signer-first sequencing prevents the signer from being anchored by the LLM verdicts.
- It is rerunnable: the current corpus has **7 semantic packets**, so one recalibration is 7 signer
  judgments and 14 LLM judgments, not 21 human reviews.
- It does not weaken any mechanical predicate or change the seed corpus.

### Independence conditions

An LLM judge is eligible only if:

- it is a fresh instance with no prior access to the seed corpus, answer key, mutations or this proposal;
- it is from a different model family from the other LLM judge;
- it is not the model family that authored or scored the artifact under review;
- its model identity and version are recorded.

If two eligible cross-family LLM judges are unavailable, the current three-human rule remains in force.
Do not substitute a same-family second instance, a project-context agent, or a mechanical score.

The signer is not statistically independent: the signer may recognize the case and owns the final
decision. That limitation is recorded. Signer-first sequencing and the blinded packet are the controls;
the policy does not claim more than that.

## 5. What Gate 0 would and would not prove under Option E

It would prove:

- the seeded semantic defect is detectable by a human-anchored, cross-family panel under blinding;
- the harness records and aggregates the three judgments correctly;
- the scorer's semantic packet is not answer-key-contaminated;
- specificity is satisfied by each accepted judgment.

It would not prove:

- clinical correctness of the note;
- generalization beyond the seven packets;
- that LLM judges are reliable in production;
- that LLM errors are uncorrelated in general;
- that the signer's clinical sign-off is unnecessary.

Clinical/product acceptance remains signer-owned and separate. A Gate 0 pass is a scorer-calibration
result, not a clinical verdict.

## 6. Exact contract changes if approved

1. `experiments/architecture/AX-S1S2-D/predicates.md`
   - replace the “Gate 0 repetition for HUMAN_REVIEW” section with Option E;
   - change the execution-mode label for the three active semantic predicates from
     `SEMANTIC / HUMAN_REVIEW` to `SEMANTIC / SEQUENCED_PANEL` (predicate meaning unchanged);
   - keep “no semantic predicate is scored by the model that produced the artifact”.
2. `experiments/gate0/00-GATE0-MANIFEST.md`
   - §3 semantic procedure: one signer-first judgment + two fresh cross-family LLM judgments;
   - §5 step 5 and §6 pass criteria: 3/3, specificity 3/3, 2/3 fail, missing/UNDECIDABLE incomplete;
   - §7a packet text: judge types and sequence.
3. `tools/gate0_harness.py`
   - allow `judge_type` `HUMAN` or `LLM` with `model_family` and `model_version`;
   - require exactly one HUMAN and two LLM records per packet, with distinct LLM families;
   - require the HUMAN record to precede the LLM records (`sequence` field; no clock reliance);
   - keep unknown/stale packet and predicate-mismatch rejection;
   - record panel composition in `EVIDENCE.json`.
4. `scorer/README.md` — human-review section becomes the sequenced-panel protocol.
5. `HANDOFF.md`, `WORKING_RULES.md` and `AGENTS.md` — replace the “three humans” operational statement
   with the accepted policy or its fallback.
6. `DECISIONS.md` — new decision recording signer approval and supersession of the three-human
   calibration rule; no architecture/DC change.
7. Tests — panel composition, signer-first, cross-family, 2/3 fail, UNDECIDABLE, stale/mismatched judge.

No change to:

- `CONSENSUS_*`, DC-001/DC-002, the experiment program;
- the 28-seed corpus or seed mutations;
- predicate meaning;
- scorer/projection/mechanical semantics;
- the three active semantic predicate IDs.

## 7. Risks and mitigations

- **Correlated LLM error.** Use two different families, fresh instances, and a signer on every packet;
  record the limitation. If the two LLM judges agree but the signer dissents, the packet fails, not
  passes.
- **Signer anchoring.** Signer records first; LLM verdicts are not shown until the signer record exists.
- **LLM judges recognize the project.** Exclude project-context agents and any model with answer-key
  access; use fresh packet-only instances.
- **Operational drift.** Pin model family/version in the judgment record; a material model change is a
  recalibration trigger.
- **Policy overreach.** Option E is for calibration only; it does not transfer clinical authority to an
  LLM or to ChatGPT/DeepSeek as project agents.

## 8. NEXT

**Signer decision:** approve Option E, choose a different option, or keep the three-human rule.
**ChatGPT review:** check the recommendation and the exact contract-change list before any patch.
**DeepSeek:** after signer approval, patch the listed contract/harness files, add the panel tests, run
`python architecture-reboot/tools/preflight.py`, and return the diff for independent review. Do not run
Gate 0 acceptance in the proposal or patch pass.
