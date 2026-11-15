# ChatGPT review 068 — post-DC002 experiment-program propagation audit

## Verdict

> **PROGRAM PROPAGATION IS PARTIALLY CORRECT BUT NOT YET READY TO FREEZE OR DRIVE EXECUTION REGENERATION.**

DC-002 remains CLOSED / VERIFIED.

The current program/spec update correctly adds:
- AX-T as a production-transfer gate;
- an AX-I3 constructibility dimension;
- authority-leak probes in AX-S1S2-D;
- an E1-style integrated preflight;
- centralized S4-ordering dependency;
- AX-R2 signer-target prerequisite;
- AX-SHARED PENDING_SIGNER note;
- no-self-attested-total rule.

However, four exact specification defects remain.

Do not regenerate the stale execution campaign yet.

---

# 1. AX-SHARED still contradicts its own new PENDING_SIGNER rule

The new section correctly says:

> Whether a shared action renders once, or once under its primary problem with a terse reference from the second, is a product decision, PENDING_SIGNER.

But the same file still freezes the opposite conclusion in three earlier places.

## Current contradictions

### Architecture claim
It says the system must preserve sharing:

> "without duplicating the action"

and with a schema:

> "that does not duplicate rendered actions."

### Required output behavior
It still requires:

> "shared action renders exactly once"

and:

> "no duplicated order/action"

### Scoring
It still scores:
- action cardinality;
- no duplicate render.

Those are product-policy assertions, not architecture invariants.

## Required correction

Before signer decision, freeze only the architecture-neutral invariants:

- the shared clinical action is represented as one underlying action identity;
- one A/P owner is explicit;
- secondary problem relevance is preserved;
- all clinically material problem-specific rationales remain recoverable in structured state;
- no fake second ownership is created;
- final-note realization follows the **selected signer/product policy** once that policy is frozen.

Until the signer chooses a final-note policy:
- final textual occurrence count is **UNSCORED / PENDING_SIGNER**;
- once vs once+cross-reference must not be used as a pass/fail criterion;
- "no duplicated order/action" may apply to the structured action identity, but not to textual mention count.

### Suggested wording

Replace the architecture claim with:

> One underlying shared clinical action can retain exactly one A/P owner while preserving clinically meaningful secondary cross-problem relevance and rationale.

Replace Required output behavior with two layers:

**IR invariants**
- one underlying action identity;
- one owner;
- both rationales recoverable;
- problem-specific actions under their own problems;
- no fake second ownership.

**Final-note behavior**
- PENDING_SIGNER; scored only after the occurrence/cross-reference policy is frozen.

This is a blocker for AX-SHARED specification closure, though it need not block unrelated experiment regeneration later.

---

# 2. AX-I3 still lacks the operational proposition-boundary rule

The added section asks:

> is the object set stable and at an operationally useful size?

and adds constructibility.

That is useful, but it does **not** supply the operational extraction rule required by review 058/067.

Without a rule, "split rate" and "merge rate" have no gold boundary. A model could emit stable but systematically over-broad objects and still appear stable.

## Required I3 rule

Add a frozen operational rule along these lines:

> I3 emits one object per clause-level clinical proposition. Split coordinated content when the propositions can differ independently in truth value, temporality, negation, condition, attribution, certainty/hedging, or downstream clinical use. Keep a qualifier attached to the proposition it qualifies unless that qualifier is itself independently meaningful.

Examples should include:

### Must split
> "MRI was negative and sodium was 128."

because the propositions can differ independently in truth, provenance, use and temporality.

### Usually keep together
> "MRI showed no acute infarct."

Negation/findings belong to one proposition.

### Split when scope differs
> "If weakness worsens, return to the ED; continue aspirin."

Conditional return precaution and unconditional medication plan have different condition scope.

### Preserve qualifier with claim
> "Stroke is less likely given the normal MRI."

Do not detach "less likely" from the claim it scopes unless the representation explicitly requires separate reasoning objects downstream.

The exact examples can be refined, but the rule must be explicit enough that:
- human/independent audit can judge merge/split;
- constructibility failure can be attributed to I3 granularity rather than vague preference.

## Constructibility criterion

Keep the new constructibility check, but define success more tightly:

> Using only the frozen I3 objects plus downstream relations/annotations, the required valid units can be built without changing an object's proposition boundary. Downstream modules may group several objects into one unit; they may not split one I3 object into smaller propositions or fuse several objects into a new source proposition.

This distinguishes:
- **grouping objects into a render unit** — allowed;
- **repairing proposition boundaries downstream** — forbidden.

---

# 3. Integrated preflight is currently too weak to detect the failure it was added for

The program now says:

> a pass states only that the pipeline runs end to end under the tested condition.

That makes the preflight little more than a smoke test.

Review 058/067 added E1-style preflight specifically to catch **whole-chain semantic drift** that isolated seam experiments cannot see.

## Required preflight observations

For one fixed representative raw paste, three fresh runs, compare at minimum:

1. source/object coverage and semantic object identity;
2. S1 problem-candidate set;
3. S2 approved/adopted semantic state relevant to rendered problems;
4. S3 rendered-problem set;
5. S3 selected representation per rendered problem;
6. S4 unit membership;
7. S4 member roles where relevant;
8. S4 operator selection;
9. final problem/unit order.

Use semantic/source-anchor matching where literal ids are not contractual.

## Interpretation

The preflight remains:
- a program-level **screen**;
- not a ninth experiment;
- not independent acceptance evidence.

But its result should be:

> whole-chain screen completed with/without drift across the predefined comparison vector.

Not merely:

> the pipeline ran end to end.

If any high-impact dimension drifts, the screen should direct which component experiment is prioritized. It does **not** itself reopen architecture.

---

# 4. Authority-leak probes currently conflate producer violation with downstream leakage

The new AX-S1S2-D probes are directionally correct, but the scoring sentence says:

> Each probe is scored structurally: the module owning the decision must be the only one expressing it.

That only detects an **upstream authority violation**. It does not test whether a downstream module then obeys or reconstructs that illicit decision.

The original concern from the ten-question review had two distinct failure modes:

1. **decision laundering at the producer seam** — a module encodes a decision it does not own inside an allowed field;
2. **behavioral leakage at the consumer seam** — downstream behavior follows the illicit cue instead of the owner's explicit state.

These must be scored separately.

## Required probe structure

For each adversarial probe, freeze:

### Producer assertion
Did the upstream artifact contain a decision outside its authority?

### Consumer assertion
Given a conflicting authoritative owner state, did downstream output obey the authoritative state rather than the illicit cue?

Example:

### S1 adoption laundering
S1 allowed subject text contains an illicit adoption-like cue, while:
- S2 explicit adoption = NOT_ADOPTED;
- S3 = NOT_RENDERED.

Score:
- producer violation = S1 authority failure;
- if S3/S4 renders the problem because of the S1 cue = downstream authority-leak failure.

### S4 re-selection
S3 explicitly selects R1.
An alternative semantically tempting R2 is visible elsewhere.
Score:
- S4 unit must remain on R1;
- any R2 use is consumer-side authority leakage/re-selection.

This distinction matters because a shared-context one-call model can fail even when the formal projected interface is clean.

## AX-LEAK relationship

Keep:
- AX-LEAK = raw-source → RENDER leakage with fixed IR;
- AX-S1S2-D adversarial probes = logical-owner → downstream-owner authority leakage.

Do not collapse them.

---

# 5. S4 ordering dependency is correctly centralized, but AX-S4 should self-declare it

The program-level prerequisite is correct:

> no ordering predicate may be scored until ordering contract + salience values are frozen.

AX-S4 still lists:
- final problem order;
- unit order

as scored dimensions without a local PENDING_DEPENDENCY note.

This is not a conceptual blocker, but executable specs should be self-contained.

## Required local annotation

In AX-S4:

> Final problem/unit order dimensions are PENDING_DEPENDENCY until the frozen ordering contract, salience inputs, and oracle exist. They are not omitted; they are unscoreable until that prerequisite is satisfied.

Do not invent the ordering contract in this correction.

---

# 6. AX-R2 propagation is adequate

AX-R2 already requires:
- 5–10 realistic signer-quality HPI/history targets;
- signer-marked mandatory content/relations;
- independent upstream constructors.

The program-level prerequisite correctly blocks execution until those targets exist.

No further spec edit is required unless adding a one-line status marker for visibility.

---

# 7. AX-T propagation is adequate

The production-transfer gate concept is correctly instantiated.

One refinement for later implementation:

> "package change reopens the gate" should be interpreted as a runtime-relevant package/instruction/model/mode change, not arbitrary repository metadata.

No correction is necessary before spec closure if the executable manifest freezes the actual runtime package hash/version.

---

# 8. No-self-attested-total rule is acceptable with a narrow interpretation

The program says artifacts must not carry aggregate counts they are also asserting.

Accept this as:

> self-attested totals are not acceptance authority; CHECK derives authoritative totals.

Diagnostic telemetry may exist later if useful, but it cannot substitute for derived accounting.

No current correction required.

---

# 9. Status

## Architecture
**CLOSED / VERIFIED**

## DC-002
**APPLIED / VERIFIED**

## Program propagation
**REVISE BEFORE FREEZE**

Blocking program-spec corrections:
1. remove AX-SHARED exactly-once contradiction;
2. add explicit I3 operational proposition-boundary rule;
3. strengthen integrated preflight from run-success to predefined drift-vector screen;
4. split producer-authority vs consumer-leak scoring in adversarial probes.

Nonblocking but required for self-contained execution spec:
5. mark AX-S4 order dimensions PENDING_DEPENDENCY locally.

## Execution package
**STALE / DO NOT REGENERATE YET**

## Scorer
NOT BUILT.

## Gate 0
UNRUN.

## Doximity
UNRUN.

## Phase 0
UNTOUCHED.

---

# 10. Next action

DeepSeek should make a **program/spec-only correction commit** touching:
- `00-ARCHITECTURE-EXPERIMENT-PROGRAM.md`;
- `AX-I3.md`;
- `AX-S1S2-D.md`;
- `AX-SHARED.md`;
- `AX-S4.md`.

No execution schema/parent/seed/scorer regeneration yet.

Return the commit and changed-file list for verification.

If these corrections pass, the experiment program can be frozen again and execution-layer regeneration may begin.
