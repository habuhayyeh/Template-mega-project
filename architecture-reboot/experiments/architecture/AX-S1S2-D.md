# AX-S1S2-D — STRUCTURE authority and claim-representation flow

**Status:** DESIGN ONLY / UNRUN

## Question

Can the repaired S1 -> S2 -> S3 -> S4 architecture produce correct problem candidacy, adoption, claim representations, note selection, and final ordering **without authority leakage across seams**?

## Architecture claims under test

- S1 owns candidacy/subject identity, not adoption or final claim.
- S2 owns semantic adjudication/adoption and approved claim representations.
- S3 owns rendered A/P problem inclusion and selection only within an S2-safe representation space.
- S4 owns blueprint and final order, not problem inclusion or semantic claim choice.
- A/P problems require approved claim representations.
- body content may remain valid without becoming an A/P problem.

## Required fixture families

At minimum include:
1. prior diagnosis, not referenced/adopted today;
2. historical diagnosis explicitly re-adopted today;
3. historical diagnosis disputed today;
4. current symptom/question with no final diagnosis;
5. explicit differential with two viable alternatives;
6. nested/more-specific claim relationship;
7. body-only historical neurologic fact;
8. historical condition used only as etiology/evidence for another problem;
9. rebuilt K2: explicit current linkage of a continued historical problem to management, so no medication->diagnosis inference is needed;
10. candidate mentioned but explicitly deferred / not independently assessed;
11. explicit contradictory-source case: two source families make incompatible assertions that must remain attributed/adjudicated rather than silently collapsed.

## Frozen inputs

For each case:
- source package;
- signer-approved target note;
- annotated ingest substrate when testing STRUCTURE in isolation;
- the current canonical interface through DC-002.

If STRUCTURE is isolated, the ingest substrate must be hand-frozen or come from a separately scored ingest artifact; do not let an unscored same-session ingest error masquerade as a STRUCTURE failure.

## Artifact under test

Preferred artifact-level output:
- S1 candidates + anchors + salience inputs;
- S2 adoption/relations + approved claim representations;
- S3 rendered-problem set + selected representation;
- S4 final ordered blueprint.

Avoid full final-note generation unless needed for a paired end-to-end check.

## Score families

### A. Structural/interface assertions

#### S1
- no adoption verdict appears in S1;
- no final claim selection appears in S1;
- no final render order appears in S1.

#### S2
- source temporality is consumed, not re-owned;
- approved representation(s) are source-grounded;
- S2 does not expose a choice set requiring further semantic adjudication by S3.

#### S3
- only S2-approved representations are selected;
- no new claim is synthesized;
- no A/P problem renders without an approved representation.

#### S4
- consumes S3 rendered-problem state and selected representation;
- does not re-decide inclusion or claim;
- final problem order is owned by S4, using S1 salience inputs rather than an upstream final order.

### B. Semantic correctness assertions

- the right neurologic subjects become S1 candidates;
- body-only context does not become a fake A/P problem;
- current adoption is clinically correct;
- competing/nested/complementary/contradictory relations are faithfully preserved/adjudicated;
- contradictory-source adjudication preserves the non-selected assertion in the IR with its source attribution intact; S2's selected resolution is recorded as a semantic decision rather than implemented by deleting the conflicting source assertion;
- rendered A/P problem inclusion is clinically correct;
- body-only content remains usable without problem promotion;
- final order satisfies the governing clinical/order contract.

Report structural/interface and semantic results separately.

## Run design

- Gate 0 scorer calibration first;
- small artifact batch first;
- executable manifest freezes exact case IDs/count/order/package/scorer versions;
- full batch only if schema/output is stable;
- exact same-order batch repeated in 3 fresh conversations;
- diagnostic trace only for failed cases.

## Architecture-reopen logic

Do **not** use an arbitrary percentage threshold.

A controlled logical counterexample can falsify a universal authority invariant if satisfying the correct clinical/structural requirement requires violating the canonical responsibility boundary.

Before reopening architecture, exclude:
- malformed fixture;
- scorer defect;
- implementation noncompliance;
- missing downstream schema/contract detail.

Ordinary semantic mistakes are implementation/contract/schema defects first.
A reproducible semantic failure becomes architectural when the interface cannot carry the information needed to make the correct decision without authority violation.

## What this experiment cannot prove

It does not test:
- raw-source leakage into RENDER;
- S4 concentration under fixed substrate independently;
- I3 proposition stability;
- test-mode observer effect;
- scale;
- R2 prose expressivity;
- shared-action rendering.

## Semantic authority-leak probes

AX-LEAK tests raw-source influence on RENDER. It does not test whether a module encodes a decision it
does not own. These probes do, and they run inside this experiment:

| probe | what is planted | what it catches |
|---|---|---|
| `LEAK-S1-ADOPT` | a candidate whose **subject text** implies adoption ("known infarct, continuing") with no adoption field | S1 encoding an adoption verdict in content rather than a field |
| `LEAK-S2-SELECT` | an adjudication record where one approved representation is pre-marked preferred | S2 making the S3 selection decision |
| `LEAK-S3-SYNTH` | a rendered representation whose text is not composed of its members | S3 synthesising content |
| `LEAK-S4-RESELECT` | a unit whose representation differs from S3's selection but is semantically equivalent | S4 re-selecting |

Each probe is scored along **two separate axes**, because they are different failures:

- **producer authority violation** — the decision is encoded outside the module that owns it
  (`LEAK-S1-ADOPT`, `LEAK-S2-SELECT`, `LEAK-S3-SYNTH`). The defect is in the producer.
- **downstream leakage** — a consumer follows the illicit cue despite authoritative owner state
  conflicting with it (`LEAK-S2-SELECT` → S3, `LEAK-S3-SYNTH` → S4, `LEAK-S4-RESELECT`). The defect is
  in the consumer, and it may occur when the producer is correct.

A run may pass one axis and fail the other; reporting them as one score hides which module to fix.

Scope split: **AX-LEAK** covers raw-source → RENDER. **These probes** cover logical-owner → downstream
owner.

### Consumer arms require conflicting authoritative state

A leakage probe is only meaningful if the legitimate owner's state is frozen and contradicts the
planted cue. Each probe therefore carries:

- the **planted illicit cue**, in the consuming module's input;
- the **frozen authoritative state**, from the owning module, saying something different;
- the requirement that the downstream artefact follow the authoritative state.

Without the conflicting state, "the consumer obeyed the cue" and "the cue was the only information
available" are indistinguishable.

**Separate control:** a clean-producer / consumer-reconstruction case — correct owner state, no planted
cue — must reproduce the expected downstream artefact. If it does not, the consumer arm cannot
distinguish leakage from ordinary failure, and the probe's result is void.

## DC-002 claims under test

- S1 owns the partition between problem candidates and claim candidates; downstream cannot merge,
  split, or re-parent it.
- S3 records exactly one outcome per S1 problem candidate: no silent candidate loss.
- S4 receives a relevance-based `S4_INPUT_VIEW` and nothing else.
- The projection introduces no semantic decision of its own.

## Artifact requirements added by DC-002

The artifact under test must expose:

- S1 problem candidates, their claim candidates, and the partition between them;
- S3 candidate outcomes, plus the rendered set, selected representations and retained use;
- an observable `S4_INPUT_VIEW` (or a mechanical equivalent that can be recorded), so `S4-PROJ-01`
  is scoreable rather than asserted;
- the S4 blueprint.

## Score families added by DC-002

| predicate | family | scored separately from |
|---|---|---|
| `S3-CAND-01` | candidate accounting | object accounting (`S3-ACCT-01`) — candidates and objects fail for different reasons |
| `S4-PROJ-01` | projection packaging | `S4-REP-01`, which checks consumption, not packaging |

Candidate accounting is never folded into object accounting. A run can account for every object and
still lose a candidate.

**Clean consumer-reconstruction control.** A producer-valid case, no illicit cue, with tempting
alternative semantic material still visible elsewhere in the shared context. The downstream artefact
must follow the explicit owner state. Without this control, a consumer arm cannot separate leakage from
the consumer merely being influenced by whatever else was in the window.
