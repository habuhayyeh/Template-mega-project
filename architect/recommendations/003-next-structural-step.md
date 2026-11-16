# Decision 003 — next structural step

**Status:** architect decision. No code, prompt text or schema.

## Decision

**Patch B's problem threshold first. Defer A's polarity. Then run C.**

Do not patch A before C. A's selector text is faithful; its polarity is advisory. If C produces a
polarity inversion, patch A then. Do not run C before B stops creating a separate baseline-spell
problem.

## 1. B threshold patch

One rule:

> A chronic or baseline phenomenon becomes a separate BACKGROUND problem only if it has independent
> neurologic disease identity or its own current assessment/management. If it is only a comparator or
> context for the primary problem, it stays inside that problem as comparator evidence.

This is not “chronic symptoms never become problems.” Known epilepsy with independent seizure
management remains a BACKGROUND problem.

### Minimum test

Two synthetic cases:

1. **Comparator case:** current recurrent events plus chronic baseline staring spells, no independent
   diagnosis or management of the spells.
   - Expected: one PRIMARY problem.
   - Baseline spells appear under that problem as comparator/contained evidence.
   - No separate BACKGROUND problem.

2. **Independent disease case:** known chronic epilepsy with its own treatment/assessment.
   - Expected: BACKGROUND problem remains.
   - It is not collapsed into the primary event.

Pass only if both hold. If case 1 passes by collapsing case 2, the rule is wrong.

Do not reopen B beyond this threshold. No new B stage, no reconciliation changes, no action changes.

## 2. A polarity

Defer.

A's mixed-polarity span is a contract weakness, but the selector is faithful and B's stance is the
authoritative clinical synthesis. C must treat A polarity as advisory, not truth. C renders from B's
stance and the exact source selector.

Gate: if the C blueprint or final note contains a polarity inversion, patch A to split mixed-polarity
spans and rerun A. Do not patch A for cosmetic variance before that evidence exists.

## 3. C design

C owns the **blueprint**, not clinical meaning.

### C owns

- section allocation;
- HPI chronology;
- neurologic history selection;
- other PMH;
- medication-at-presentation representation;
- current exam selection;
- workup/result placement;
- A/P claim/evidence/counterevidence composition;
- action placement and shared-action ownership;
- minimum-sufficient inclusion;
- legitimate cross-section reuse;
- unit order.

### C must not own

- problem identity or containment;
- PRIMARY/BACKGROUND;
- diagnosis or diagnostic stance;
- causality;
- current vs historical;
- action decision/execution/response/result;
- source reconciliation;
- new facts;
- prose.

### Typed groups and operators

B supplies typed groups: problem groups, evidence groups, action groups, and section candidates. C maps
those groups to a **closed set of canonical render operators**. C chooses the operator that matches the
already-decided type; it does not invent operators or reinterpret the content.

A blueprint unit is conceptually:

```text
section + problem + operator + member IDs + order + source refs
```

No prose in the blueprint. No new clinical claim. If no operator fits, C marks the unit unresolved rather
than inventing structure.

### Blueprint/render boundary

The blueprint ends at:

- section;
- problem;
- operator;
- members;
- order;
- source references;
- explicit unresolved markers.

The renderer lexicalizes only. It may reread the packet for exact source wording. It may not change
section, problem, operator, members, order, polarity, certainty or action state.

## 4. Sequence and gates

1. **B threshold patch.**
   Gate: comparator case has no separate problem; independent-disease case keeps its BACKGROUND problem.

2. **C blueprint run on the clean packet.**
   Gate:
   - one PRIMARY problem; baseline spells are comparator evidence, not a block;
   - sections and HPI chronology correct;
   - no new problem, role, diagnosis, causality or action state;
   - evidence and counterevidence present;
   - actions placed under the correct problem;
   - source refs intact;
   - template coverage complete.

3. **Renderer run.**
   Gate:
   - no new clinical claim;
   - no polarity, certainty, currentness or action-state change;
   - no counterevidence loss;
   - prose is faithful to the blueprint.

Do not run render before the blueprint gate passes.

## 5. Delete or defer

Delete/defer:

- separate baseline-spell BACKGROUND problem;
- A polarity patch for now;
- B1 reconciliation stage;
- normalized action-state enums;
- new validators;
- new micro-prompts for cosmetic variance;
- renderer discretion over clinical content.

## 6. Main risk

C becomes a second problem architect, or the renderer silently repairs missing structure in prose.

Mitigation: blueprint-only gate, closed operator set, no prose until the blueprint passes, and a renderer
that cannot change blueprint decisions.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
