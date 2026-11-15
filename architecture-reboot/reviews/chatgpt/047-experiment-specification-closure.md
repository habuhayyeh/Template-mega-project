# ChatGPT review 047 — architecture experiment specification closure

## Verdict

**ARCHITECTURE EXPERIMENT SPECIFICATION LAYER — CLOSED / CONVERGED.**

DeepSeek 033 found the revised eight-experiment package conformant and identified only two wording ambiguities. Both have now been corrected without changing the architecture or experiment boundaries.

All eight experiments remain:

> **DESIGN ONLY / UNRUN**

No result exists and no experiment has passed or failed.

---

# 1. AX-S1S2-D contradictory-source clarification

The prior assertion:

> contradictory sources remain attributed rather than silently collapsed

could be read as forbidding S2 from resolving a clinically meaningful semantic choice.

The revised assertion now makes both requirements explicit:

- the non-selected conflicting assertion remains recoverable in the IR;
- its source attribution remains intact;
- S2 may still record the selected semantic resolution;
- resolution is not implemented by deleting the conflicting source assertion.

This is consistent with DC-001:
- source fidelity/audit trail is preserved;
- S2 retains semantic-adjudication authority.

---

# 2. AX-SHARED rationale-preservation clarification

The prior wording did not distinguish:
- preservation in the structured IR;
- preservation in final-note prose.

The revised rule is:

## IR
Both distinct problem-specific rationales must remain recoverable.

## Final note
The signer-approved target and section contract determine which rationale content is clinically material to communicate.

Therefore:
- all clinically required rationale content must survive into the note;
- the action still renders once;
- the note need not duplicate or separately restate both rationales when one concise combined realization or permitted cross-reference preserves the required meaning;
- concision is not permission to erase a clinically material secondary rationale.

This avoids two opposite errors:
1. forcing verbose duplicated prose merely to prove preservation;
2. using note brevity to hide loss of clinically important cross-problem reasoning.

---

# 3. Final specification state

The stable architecture-test program is:

1. AX-S1S2-D
2. AX-LEAK
3. AX-S4
4. AX-I3
5. AX-T
6. AX-SCALE
7. AX-R2
8. AX-SHARED

Program-level prerequisites/obligations include:
- Gate 0 scorer calibration;
- frozen executable manifests;
- targeted interaction testing;
- I1/I2 paste-layout characterization before production-shaped claims depend on those boundaries.

There is still no ninth architecture experiment.

---

# 4. What is closed

Closed:
- experiment purposes;
- architecture claims under test;
- major controls;
- fixture families;
- score families;
- interpretation/reopen logic;
- cross-experiment scope boundaries.

Open:
- exact executable manifests;
- exact case IDs and final case count per run;
- concrete fixture payloads;
- exact scorer predicates and calibration artifacts;
- package versions;
- raw Doximity outputs;
- results and verdicts.

Those are execution-layer artifacts, not reasons to reopen the experiment-design layer unless they expose a new contradiction.

---

# 5. Next step

The next legitimate architecture-validation work is:

1. build the executable manifest for Gate 0 and AX-S1S2-D first;
2. build/freeze the required fixtures and scorer predicates;
3. calibrate the scorer;
4. run the first scored architecture experiment only after those artifacts are independently reviewed.

Do not treat the conceptual spec files as runnable experiments by themselves.

Do not touch Phase 0 yet solely because the experiment-spec layer is closed.

Phase 0 reconciliation should follow the agreed architecture-validation transition, not preempt it.
