# ChatGPT review 071 — experiment-program specification freeze

## Verdict

> **EXPERIMENT PROGRAM SPECIFICATION IS SUBSTANTIVELY FROZEN.**

The post-DC002 propagation is now complete enough to drive execution-layer regeneration.

The latest program/spec commit `ee526bdc` correctly instantiates the substantive requirements from reviews 068–070.

No further architecture or experiment-design review cycle is required before regenerating the stale execution package.

Two remaining items are editorial/status bookkeeping only and may be corrected without another review:
1. the program status paragraph still mentions only DC-001 in one sentence;
2. AX-SHARED's Question sentence is grammatically malformed after the action-identity rewrite.

These do not change the experiment design.

---

# 1. Program-level requirements — VERIFIED

The program now correctly includes:

- exactly eight architecture experiments;
- Gate 0 as prerequisite, not a ninth experiment;
- AX-T as a production-transfer gate;
- paste-layout characterization as a prerequisite, not a ninth experiment;
- E1-style integrated raw-paste → Case-IR preflight as a program screen;
- preflight comparison vector across:
  - object coverage/identity;
  - S1 candidate set;
  - relevant S2 state;
  - S3 rendered/selected state;
  - S4 membership, roles, operators, problem order and unit order;
- S4 ordering dependency;
- AX-R2 signer-quality target prerequisite;
- AX-SHARED occurrence policy PENDING_SIGNER;
- no-self-attested-total rule;
- interaction follow-up for AX-LEAK × AX-SCALE;
- claim scope limited to tested frozen conditions.

This is sufficient for program-level freeze.

---

# 2. AX-I3 — VERIFIED

AX-I3 now has both required dimensions:

## Operational proposition-boundary rule
Split propositions when they can vary independently in:
- truth;
- temporality;
- negation;
- condition;
- attribution;
- certainty/hedge;
- downstream use.

Scoped qualifiers remain with the proposition unless independently meaningful.

## Constructibility
Downstream modules may:
- group several objects into one render unit.

They may not:
- split one I3 object into smaller source propositions;
- fuse several objects into a new source proposition merely to repair I3 granularity.

This closes the I3 design gap.

---

# 3. AX-S1S2-D — VERIFIED through DC-002

The experiment now freezes the current interface through DC-002.

It explicitly includes:

## D1
- S1 problem-candidate / claim-candidate partition authority.

## D2
- exactly one S3 outcome per S1 problem candidate;
- no silent candidate loss.

## D3
- relevance-based `S4_INPUT_VIEW`;
- projection carries selected/retained state only;
- projection itself creates no semantic decision.

## Observable artifacts
The spec now requires:
- S1 problem candidates + claim candidates/partition;
- S3 candidate outcomes + rendered/selected/retained state;
- observable `S4_INPUT_VIEW` or mechanical equivalent;
- S4 blueprint.

## New predicates
The spec explicitly separates:
- `S3-CAND-01` candidate accounting;
- `S3-ACCT-01` object accounting;
- `S4-PROJ-01` packaging/projection;
- `S4-REP-01` downstream representation consumption.

That distinction is correct and important.

---

# 4. Authority-leak design — VERIFIED

The spec now distinguishes:

1. **producer authority violation**;
2. **consumer leakage**;
3. **clean-producer / consumer-reconstruction control**.

Consumer arms require:
- an illicit or tempting cue;
- a conflicting explicit authoritative owner state;
- downstream behavior that must follow the authoritative state.

The clean consumer-reconstruction control keeps:
- producer valid;
- no illicit producer field;
- alternative semantic material visible elsewhere in shared context;
- explicit owner state;
- downstream required to obey owner state.

This correctly tests downstream reconstruction/leakage independently from producer noncompliance.

AX-LEAK remains separately scoped to:
> raw-source → RENDER leakage.

The distinction is now usable.

---

# 5. AX-S4 — VERIFIED subject to dependency

Both:
- final problem order;
- unit order

are now `PENDING_DEPENDENCY` until the ordering contract/oracle exists.

No ordering score may be produced before that prerequisite is frozen.

---

# 6. AX-SHARED — VERIFIED as a design with a pending product choice

The spec now correctly treats the architecture invariant as:

- one underlying action identity;
- one A/P owner;
- preserved secondary relevance;
- preserved clinically material rationales;
- no fake second ownership.

Textual occurrence count is:

> **UNSCORED / PENDING_SIGNER**

until the signer chooses the final-note policy.

This is now compatible with one-owner semantics.

### Editorial defect only
The current Question sentence reads roughly:

> "with one underlying action identity, losing a rationale, or violating..."

It should be grammatically corrected to:

> Can the architecture represent one underlying clinical action that serves multiple neurologic problems while preserving one-owner semantics and all clinically material cross-problem relevance/rationale?

This is editorial, not a design blocker.

---

# 7. Two bookkeeping edits authorized without re-review

DeepSeek may make one tiny program-freeze bookkeeping commit:

## Program status paragraph
Current stale sentence:
> The interface design is converged and DC-001 is APPLIED / VERIFIED...

Change to:
> The interface design is converged; DC-001 and DC-002 are APPLIED / VERIFIED, but the architecture is not empirically validated.

Optionally change the program status line from:
> DESIGN ONLY / UNRUN

to:
> **SPECIFICATION FROZEN / UNRUN**

That is the preferred durable status.

## AX-SHARED Question
Apply the grammatical wording above.

No further ChatGPT review is required for those exact editorial/status changes.

---

# 8. Execution-layer regeneration is now authorized

After the tiny bookkeeping commit, regenerate the stale execution package against the frozen post-DC002 program.

Recommended order:

1. regenerate AX-S1S2-D experiment-local schema;
2. regenerate CASE-01 clean parent/oracle under DC-002;
3. freeze the new active predicate set;
4. ensure `S3-CAND-01` and `S4-PROJ-01` are represented in schema and active-set logic where the pilot can exercise them;
5. regenerate Gate 0 seed definitions;
6. regenerate instantiated seed artifacts;
7. regenerate campaign manifest and canonical hashes;
8. independently review the regenerated execution package;
9. only then build the scorer;
10. independently review the scorer;
11. run Gate 0.

Do not build the scorer against the stale pre-DC002 artifacts.

---

# 9. Product dependency still open

AX-SHARED final-note occurrence remains:

> **PENDING_SIGNER**

This does not block regeneration of unrelated Gate 0 / AX-S1S2-D execution artifacts.

It blocks only the final-note occurrence assertions for AX-SHARED.

Do not silently choose the product policy during execution regeneration.

---

# 10. Current state

## Architecture
**CLOSED / VERIFIED**

## DC-001
**APPLIED / VERIFIED**

## DC-002
**APPLIED / VERIFIED**

## Experiment program specification
**SUBSTANTIVELY FROZEN**

## Execution package
**STALE / REGENERATION AUTHORIZED**

## Scorer
**NOT BUILT**

## Gate 0
**UNRUN**

## Doximity
**UNRUN**

## Phase 0
**UNTOUCHED**
