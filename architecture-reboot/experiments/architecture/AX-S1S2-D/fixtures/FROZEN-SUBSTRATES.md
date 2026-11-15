# AX-S1S2-D — frozen substrates

Three cases, one patient. All marked **DERIVED**: the substrate is reconstructed from the signer's material, not captured from a live encounter. They exist to separate adoption-from-evidence from adoption-from-convenience.

Format:

```text
SPAN  <id> | source <A transcript|B prior note|C study> <date> | "<verbatim>"
OBJ   <id> | <kind> | "<text>" | prov <source/date> | temporal <when> | span <ref>
```

`temporal` is what ingest recorded. S2 may consume it; it may not rewrite it.

---

## CASE-01 — prior diagnosis, not adopted today

**Scenario:** 72F, neurology follow-up for falls. The prior note documents a left MCA infarct. Today's encounter never restates it as a problem and never links it to a decision.

```text
SPAN S01 | source B prior neurology 2024-02 | "Known left MCA infarct with mild residual right faciobrachial weakness."
SPAN S02 | source A transcript 2026-11-16 | "Three falls since June. No new weakness or speech trouble."
SPAN S03 | source A transcript 2026-11-16 | "We should check her vitamin D and refer to PT for gait training."
SPAN S04 | source A transcript 2026-11-16 | "Aspirin 81 daily, unchanged."

OBJ O01 | FACT      | "known left MCA infarct" | prov B/2024-02 | temporal 2024-02 documented | span S01
OBJ O02 | FACT      | "mild residual right faciobrachial weakness" | prov B/2024-02 | temporal 2024-02 | span S01
OBJ O03 | FACT      | "three falls since June" | prov A/2026-11-16 | temporal June–November | span S02
OBJ O04 | FACT      | "no new weakness or speech trouble" | prov A/2026-11-16 | temporal now | span S02
OBJ O05 | PLAN      | "check vitamin D" | prov A/2026-11-16 | status current | span S03
OBJ O06 | PLAN      | "refer to PT for gait training" | prov A/2026-11-16 | status current | span S03
OBJ O07 | MEDICATION| "aspirin 81 daily, unchanged" | prov A/2026-11-16 | status current | span S04
```

**Frozen expectation**

- exactly one A/P problem: the falls, claim asserted today;
- `O01`/`O02` are **not** adopted: no assessment question is posed for them today;
- `O01` may appear as body/history context with attribution, never as a rendered A/P claim;
- `O07` is a medication fact, not a management decision, and cannot adopt anything;
- if a run renders a "prior infarct" A/P problem, that is `S1-CAND-01` failing, not a defensible variant.

---

## CASE-02 — historical diagnosis explicitly re-adopted

**Scenario:** same patient, different encounter. The clinician restates the infarct as the explanation for a new problem.

```text
SPAN S01 | source B prior neurology 2024-02 | "Known left MCA infarct with mild residual right faciobrachial weakness."
SPAN S02 | source A transcript 2026-11-16 | "She had a first focal seizure this week. We think this is post-stroke epilepsy from the old left MCA infarct."
SPAN S03 | source A transcript 2026-11-16 | "Start levetiracetam 500 mg BID."

OBJ O01 | FACT      | "known left MCA infarct" | prov B/2024-02 | temporal 2024-02 | span S01
OBJ O02 | FACT      | "first focal seizure this week" | prov A/2026-11-16 | temporal this week | span S02
OBJ O03 | REASONING | "post-stroke epilepsy from the old left MCA infarct" | prov A/2026-11-16 | role claim | span S02
OBJ O04 | PLAN      | "start levetiracetam 500 mg BID" | prov A/2026-11-16 | status current | span S03
```

**Frozen expectation**

- one A/P problem: seizure, claim `O03`;
- `O01` is **adopted**: `O03` names it as the cause and is asserted today;
- the claim representation carries attribution (`old left MCA infarct`, prior documentation);
- adoption evidence must be `S02`, not the plan line.

---

## CASE-09 — K2 rebuilt: explicit linkage to management

**Scenario:** same patient, encounter where the historical infarct is carried only because a management decision references it.

```text
SPAN S01 | source B prior neurology 2024-02 | "Known left MCA infarct."
SPAN S02 | source A transcript 2026-11-16 | "We will continue aspirin 81 daily for secondary prevention of the left MCA infarct."
SPAN S03 | source A transcript 2026-11-16 | "No new deficits. She is otherwise doing well."

OBJ O01 | FACT | "known left MCA infarct" | prov B/2024-02 | temporal 2024-02 | span S01
OBJ O02 | PLAN | "continue aspirin 81 daily for secondary prevention of the left MCA infarct" | prov A/2026-11-16 | status current | span S02
OBJ O03 | FACT | "no new deficits" | prov A/2026-11-16 | temporal now | span S03
```

**Frozen expectation**

- the infarct is **current** because `O02` links the action to it explicitly — this is the one case where a plan line does establish adoption, and only because the linkage is in the sentence;
- a problem may render with a claim assembled from relation (`O01` + `O02`), which `S2-REP-01` permits;
- if a run refuses to adopt here, the rule is too strict; if it adopts in `CASE-01`, the rule is too loose. The pair is the test.

---

## Why three cases and not one

`CASE-01` and `CASE-09` are the same clinical situation with one sentence different. If a run treats them the same, it is not reading the linkage — it is applying a policy, and the policy will be wrong in one direction or the other. `CASE-02` adds the explicit-restatement route.

The trio is the cheapest discriminating set for the adoption rule, and none of the three requires a full note: STRUCTURE artifacts are enough.

## Status

`AUTHORED / UNRUN`. Substrates frozen as written; to change one is an `ACCEPTANCE CHANGE`.
