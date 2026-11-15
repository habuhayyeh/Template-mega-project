# ChatGPT review 069 — final program-freeze verification after recovery commit

## Verdict

> **PROGRAM SPECIFICATION IS CLOSE, BUT NOT YET FROZEN.**

The recovery commit `d1b5bb38` successfully restored the truncated AX-I3 and AX-SHARED files after the write-before-read bug.

Architecture and DC-002 remain CLOSED / VERIFIED.

The restored files reveal that several review-068 corrections were appended rather than integrated, and one program-level correction was never instantiated.

Do not regenerate the execution layer yet.

---

# 1. Program header is stale after DC-002

Current program still says:

> **Scope:** architecture validation after DC-001

and:

> The interface design is converged and DC-001 is APPLIED / VERIFIED

That is historically incomplete.

## Required correction

Use:

> **Scope:** architecture validation after DC-002

and:

> The interface design is converged; DC-001 and DC-002 are APPLIED / VERIFIED, but the architecture is not empirically validated.

This matters because the program now tests the DC-002 interface, not the pre-DC002 architecture.

---

# 2. Integrated preflight correction from review 068 was not applied

The program still says:

> a pass states only that the pipeline runs end to end under the tested condition.

That is only a smoke test and does not serve the purpose for which the E1-style preflight was added.

## Required replacement

The preflight is one fixed representative raw paste, three fresh runs.

Compare a predefined **whole-chain drift vector**:

1. source/object coverage and semantic object identity;
2. S1 problem-candidate set;
3. relevant S2 adoption/approved-representation state;
4. S3 rendered-problem set;
5. S3 selected representation per rendered problem;
6. S4 unit membership;
7. S4 member roles where applicable;
8. S4 operator selection;
9. final problem order;
10. final unit order.

Use semantic/source-anchor matching where literal ids are not contractual.

## Interpretation

The screen reports:

> whole-chain drift detected / not detected across the predefined vector under this frozen condition.

It is:
- diagnostic;
- not a ninth experiment;
- not independent acceptance evidence;
- not a substitute for any component experiment.

If a dimension drifts, prioritize/localize the owning experiment.

A successful screen does **not** establish whole-system reliability.

---

# 3. AX-I3 — operational rule now acceptable

The recovered file now contains the required rule:

> split when propositions can vary independently in truth, temporality, negation, condition, attribution, certainty/hedge, or downstream use; keep scoped qualifiers attached unless independently meaningful.

It also correctly distinguishes:
- downstream grouping of several objects into one unit = allowed;
- downstream repair by splitting/fusing source propositions = not allowed.

This closes the review-068 I3 defect.

### Optional examples
Examples would improve scorer/fixture authoring, but they are no longer required for program-spec closure because the rule itself is operational enough to build fixtures and adjudicate boundaries.

No further I3 design change required now.

---

# 4. AX-SHARED is still internally contradictory

The recovery restored the original full file, including the exact statements review 068 said must be removed.

Current file simultaneously says:

### Architecture claim
> "through a downstream schema that does not duplicate rendered actions"

### Required output
> "shared action renders exactly once"

and:
> "no duplicated order/action"

### Scoring
> "action cardinality"

and:
> "no duplicate render"

Then at the bottom it correctly says:

> occurrence policy = PENDING_SIGNER

and:
> textual occurrence count = UNSCORED.

Those cannot coexist.

## Required rewrite

### Question
Avoid making textual duplication itself the architecture question.

Use:

> Can the architecture represent one underlying clinical action that serves multiple neurologic problems while preserving one-owner semantics and all clinically material cross-problem rationale/relevance?

### Architecture claim
Use:

> One underlying shared clinical action can retain exactly one A/P owner while preserving clinically meaningful secondary cross-problem relevance and rationale.

Do not mention rendered occurrence count here.

### Required output behavior — split into two levels

#### Structured IR invariants
- one underlying action identity;
- exactly one A/P owner;
- secondary problem relevance is represented;
- both clinically material rationales are recoverable;
- problem-specific actions remain linked to their own problems;
- no fake second ownership;
- no loss of clinically material rationale.

#### Final-note occurrence
> PENDING_SIGNER / UNSCORED until the product policy is frozen.

### Scoring before signer policy
Score:
- underlying action identity cardinality;
- owner correctness;
- secondary relevance preservation;
- both rationales recoverable;
- problem-specific action linkage;
- no semantic loss.

Do **not** score:
- number of textual mentions;
- "no duplicate render";
- final-note occurrence count.

Once signer policy is frozen, add the appropriate final-note assertion.

### Architecture consequence
Do not say:
> if one-owner representations duplicate the action, reopen one-owner.

Textual duplication may be an allowed product policy.

Instead:

> reopen one-owner semantics only if no reasonable representation can preserve one underlying action identity, one owner, and clinically necessary secondary problem relevance/rationale without semantic loss or fake ownership.

This is the architecture question.

---

# 5. Authority-leak probes: distinction added, but consumer arms are still underspecified

The new two-axis wording is directionally correct.

However, a consumer-leak test requires a **conflicting authoritative owner state**. The current table mostly plants an illicit producer cue without freezing the competing authoritative state the downstream module must obey.

Without that, the downstream result may be semantically consistent with both inputs and leakage cannot be attributed.

## Required probe structure

Each consumer probe must freeze:

1. illicit cue outside the owner's authority;
2. explicit authoritative owner state that conflicts with the illicit cue;
3. expected downstream behavior = obey authoritative state.

### LEAK-S1-ADOPT
Plant:
- S1 subject text implies current adoption.

Authoritative state:
- S2 adoption = NOT_ADOPTED;
- S3 candidate outcome = NOT_RENDERED.

Consumer assertion:
- S3/S4 must not render the problem because of S1 wording.

Score separately:
- S1 producer authority violation;
- downstream consumer leak if the illicit wording changes selection/rendering.

### LEAK-S2-SELECT
Plant:
- S2 marks one approved representation as preferred outside its authority.

Authoritative state:
- S3 explicitly selects the other selection-safe representation.

Consumer assertion:
- S4 must honor S3's selected representation.

### LEAK-S3-SYNTH
Plant:
- an illicit synthesized textual/semantic cue in an S3 field not owned by S3.

Authoritative state:
- S2 selected/approved representation payload is frozen.

Consumer assertion:
- S4 must follow the legitimate selected representation payload, not the synthesized cue.

### LEAK-S4-RESELECT
This is already primarily a consumer-side violation:
- S3 selects R1;
- tempting R2 remains visible elsewhere;
- S4 must stay on R1.

## Important wording correction

Current text says:

> downstream leakage ... may occur when the producer is correct.

For these planted-adversarial probes, the producer carrying the illicit cue is by definition not correct.

A **clean producer / downstream reconstruction** control is a different arm and is valuable, but it should be named separately.

Add a clean-control arm:

> no illicit producer field; alternative semantic material remains visible elsewhere in shared context; downstream must still obey owner state.

That isolates consumer reconstruction/leakage without a producer violation.

---

# 6. AX-S4 still marks only problem order as pending

Current scored dimensions:

- final problem order — PENDING_DEPENDENCY
- unit order — still listed as scoreable

But the frozen ordering contract/oracle is required for **both**.

## Required correction

Mark:

- final problem order — `PENDING_DEPENDENCY`
- unit order — `PENDING_DEPENDENCY`

until:
- ordering contract;
- salience values/inputs;
- applicable unit-order rules;
- oracle

are frozen.

No ordering experiment result should be scored before that.

---

# 7. Recovery from write-before-read truncation

The recovery commit restored AX-I3 and AX-SHARED to full-length documents.

Because this failure mode already occurred once, use a simple process safeguard for future program/spec edits:

> fetch/read current file → transform full content → write/update → re-fetch and verify expected header + tail/section count.

This is an implementation/process safeguard, not an architecture change.

Do not create another architecture experiment for it.

---

# 8. What is already acceptable

No further changes required now for:

- AX-T production-transfer gate;
- AX-I3 operational boundary/constructibility after recovery;
- AX-R2 signer-quality target prerequisite;
- no-self-attested-total rule;
- AX-LEAK raw-source→RENDER scope;
- interaction follow-up with AX-SCALE;
- eight-experiment count;
- paste-layout prerequisite.

---

# 9. Status

## Architecture
**CLOSED / VERIFIED**

## DC-002
**APPLIED / VERIFIED**

## Experiment program
**FINAL CORRECTION PASS REQUIRED**

Remaining blockers:
1. stale DC-001-only program header;
2. integrated preflight still smoke-test-only;
3. AX-SHARED old exactly-once assertions must be removed, not merely contradicted later;
4. authority-leak consumer probes need conflicting authoritative state + clean consumer-reconstruction control;
5. AX-S4 unit order also PENDING_DEPENDENCY.

## Execution package
**STALE — DO NOT REGENERATE YET**

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

Make one **program/spec-only** correction commit touching only:

- `00-ARCHITECTURE-EXPERIMENT-PROGRAM.md`;
- `AX-S1S2-D.md`;
- `AX-S4.md`;
- `AX-SHARED.md`.

AX-I3 should not need another edit.

After writing:
- re-fetch each modified file;
- verify the file still contains its original header and terminal sections;
- report changed files.

If this passes, the program specification can be frozen and execution-layer regeneration can begin.
