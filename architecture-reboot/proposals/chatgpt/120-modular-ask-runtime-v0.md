# Proposal 120 — modular Doximity Ask runtime v0

**Status:** PROPOSED execution architecture under D-037. Later files are provisional until File 1 is tested.

## 1. Runtime model

Production target:

```text
Scribe V2.2 evidence packet
        ↓
Doximity Ask
  F1 → F2 → F3 → F4 → F5 → F6 → F7
        ↓
final neurology note
```

The files are modular functions with explicit input/output contracts. They may execute logically inside
one Ask call. Diagnostic runs may load only one function and request its handoff artifact.

This differs from the old micro-stage pipeline: preserve semantic ownership, but bundle operations into
larger cognitively coherent functions for GPT-4o.

## 2. What Scribe already owns

Scribe V2.2 already performs most deployment-facing I1/I2 work and part of I3/I4:

- direct source boundaries;
- source order;
- transcript turn boundaries;
- stable record ids;
- raw speaker labels;
- nested provenance via VIA;
- faithful compression;
- inline uncertainty;
- direct prechart section preservation.

Ask should not redo those from raw text.

## 3. Candidate Ask functions

### F1 — EVIDENCE OBJECTS

**Input:** Scribe V2.2 packet.

**Owns:** completion of the source-aware proposition substrate.

**Does:**
- split composite Scribe records into atomic clinical propositions;
- retain the originating Scribe record id;
- assign a small source-level semantic kind;
- preserve fact-time, explicit source stance/certainty, attribution and uncertainty;
- represent clinical questions as questions, never facts;
- preserve action mentions without adjudicating their final state.

**Does not:**
- reconcile across sources;
- deduplicate;
- create entity clusters;
- decide current encounter adoption;
- decide problems, relevance, roles or note sections.

**Output:** `F1_EVIDENCE_OBJECTS` handoff.

Architecture mapping: completes the useful I3/I4 substrate after Scribe.

---

### F2 — RECONCILIATION / LONGITUDINAL STATE

**Input:** F1 evidence objects.

**Owns:** source-level identity/reconciliation before problem reasoning.

**Does:**
- identify records referring to the same disease/event/finding;
- distinguish duplicates from longitudinal evolution and true conflict;
- preserve patient report vs objective finding;
- separate durable disease/event identity from source-specific state;
- prevent historical status from silently becoming current.

**Does not:**
- decide independent neurologic problem structure;
- decide encounter role;
- infer causality;
- select note content.

**Output:** reconciled fact/entity set with conflicts/evolution preserved.

This is normalization, not final encounter adjudication.

---

### F3 — ACTION STATE

**Input:** F1 action mentions + F2 reconciled entities/facts.

**Owns:** management/test action state fidelity.

**Does:**
- distinguish considered/recommended/planned/ordered/started/performed/completed/held/stopped where source supports it;
- preserve action owner, timing, condition, patient response and result state when supplied;
- distinguish test performed from result available;
- reconcile repeated action statements without upgrading state.

**Does not:**
- decide which problem owns the action;
- decide whether the action belongs in the final note.

**Output:** reconciled action set.

Separate because action-state errors are high-impact and semantically unlike ordinary fact reconciliation.

---

### F4 — PROBLEM ARCHITECTURE

**Input:** F2 reconciled facts + F3 actions.

**Owns:** the core STRUCTURE semantic decisions.

It executes three internal steps in fixed order:

1. **IDENTITY / partition (S1 responsibility)**
   - which neurologic subjects require independent assessment questions;
   - what is contained manifestation/status/evidence rather than another problem;
   - claim candidates belong to exactly one problem identity.

2. **STATE / RELATIONS (S2 responsibility)**
   - what the encounter supports now;
   - current vs historical/source-only stance;
   - uncertainty;
   - duplicate/modifier/reasoning relationships;
   - causal/contributory relationships only when evidence supports them.

3. **RELEVANCE / ROLE / USE (S3 responsibility)**
   - PRIMARY vs BACKGROUND;
   - rendered vs not rendered;
   - which defensible representation/content is used.

Later internal steps may not merge/split/re-parent the identity partition chosen in step 1.

**Output:** problem graph + retained content/problem-use map.

This bundles S1/S2/S3 for GPT-4o execution while preserving ownership order.

---

### F5 — NOTE COMPILER

**Input:** problem graph + retained facts + reconciled actions.

**Owns:** S4-equivalent note blueprint.

**Does:**
- build current-episode timeline;
- build neurologic-history packet by disease;
- build medication, exam and workup packets;
- build one A/P packet per rendered problem;
- attach actions to their primary problem/use;
- assign section homes and permitted reuse;
- choose the minimum sufficient evidence/counterevidence;
- determine problem order, unit order and render grouping.

**Output:** complete note blueprint / section packets.

All render-affecting semantic decisions are complete here.

---

### F6 — RENDERER

**Input:** F5 note blueprint.

**Owns:** R1/R2/R3 language realization only.

**Does:**
- render prepared units/packets into the agreed note structure and style;
- preserve order and semantic content;
- apply section-specific prose conventions.

**Does not:**
- add diagnoses;
- change certainty;
- reassign problems;
- invent relationships;
- change action state;
- fill unsupported template defaults.

**Output:** draft final note.

---

### F7 — OUTPUT GUARD

**Input:** F5 blueprint + F6 note.

**Owns:** bounded runtime conformance repair, not clinical re-reasoning.

Checks for:
- historical -> current leakage;
- certainty strengthening;
- symptom/finding -> unsupported diagnosis;
- contained manifestation -> duplicate problem;
- independent disorder collapsed;
- action-state upgrade;
- performed -> result-available upgrade;
- attribution/ownership change;
- lost material counterevidence;
- wrong section/repetition;
- invented patient fact.

May repair only a discrepancy between the F5 blueprint and F6 rendering.

It may not reopen F1-F5 semantic decisions.

**Important:** F7 self-checking is diagnostic/runtime hygiene only. It is never acceptance evidence under
Phase 0; external CHECK/AUDIT remains authoritative.

## 4. Why this granularity

The former architecture's decision ownership remains useful. The former number of micro-operations does
not need to be reproduced as separate prompts.

For GPT-4o:
- too many narrow passes increase context drift and reinterpretation;
- one monolithic pass hides the first failure point;
- 7 coherent transformations provide observable handoffs without making every metadata operation its own stage.

The count is provisional. Empirical results may justify merging or splitting a function.

## 5. Stronger-surface vs Doximity diagnostic

For each new function, initially run the same frozen function spec on the same frozen Scribe packet:

1. a stronger reasoning surface;
2. Doximity Ask / GPT-4o in a fresh session;
3. repeated GPT-4o runs where reproducibility matters.

The stronger surface is a **design diagnostic, not the clinical oracle**.

Interpretation:
- if both surfaces disagree materially or struggle, the function contract is probably ambiguous/overloaded;
- if the stronger surface is coherent but GPT-4o drifts, reduce cognitive load or move a mechanical task upstream/downstream;
- if GPT-4o is stable, proceed to the next function rather than adding rules.

## 6. Phase-0 implications to test, not yet edit

D-037 supplies new empirical evidence against the old assumption that logical submodules should not be
tested as execution passes.

Likely mappings after File 1 evidence:
- old AX-I3 -> F1 proposition/atomicity stability;
- source reconciliation/adoption tests -> F2/F4 boundary;
- AX-S1S2-D -> F4 internal ownership/order;
- AX-S4 -> F5 decision concentration;
- AX-LEAK -> integrated all-files run, because all files share one model context;
- AX-SCALE -> packet size + number of function files;
- AX-R2 -> F6 expressivity burden;
- AX-SHARED -> F3/F4/F5 shared-action behavior.

Do not rewrite Phase 0 before the execution evidence exists.

## 7. Immediate experiment

Freeze and run **F1 only**.

Do not finalize F2-F7 prompts first.

F1 is successful only if it gives the next function a stable, source-faithful, atomic evidence substrate
without performing downstream semantic work.

Then revise F1 or proceed to F2 based on observed Doximity behavior.
