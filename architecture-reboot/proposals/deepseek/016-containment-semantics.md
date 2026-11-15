# Proposal 016 — containment/status semantics without a new schema field

**Status:** PROPOSED — not implemented. This answers the signer/reviewer request for the smallest
amendment reconciling S1/S2/S3 with the problem-containment model.

## Model

A problem block represents a clinically independent problem identity. A manifestation that is fully
explained by an existing problem remains contained under that parent problem. It can still be current,
important, monitored, adopted as a proposition, and even the acting causal mediator. It does not become
a separate problem merely because it is clinically salient.

Uncertain or unexplained manifestations may temporarily become syndrome/finding problems. A distinct
downstream disorder (for example post-stroke epilepsy) keeps its own problem identity even when caused
by the parent disease.

## Does any schema field need to change?

**No new field is required for the current Gate-0 contract.**

The existing structure already expresses containment without promoting the manifestation:

- **S1 candidacy** decides independent problem identity. A contained manifestation is not a candidate.
- **S2 representation** carries the parent problem and may include the contained object in
  `members`; `relations` can carry its epistemic/mediating link. This is already what CASE-01 `R2`
  does with `O01` (HEAD) and `O02` (MODIFIER).
- **S2 adoption** is object/proposition-level current-source endorsement. It is independent of whether
  that object is a problem block.
- **S2 causality** may use a contained object as the acting contributor without promoting it.
- **S3 encounter role** applies to the problem block, not to the contained object.
- **S4 unit roles** (`HEAD`, `MODIFIER`) and problem grouping express the compact contained form.

A new `CONTAINED_BY` relation or a `contained: true` field would duplicate what problem membership plus
S4 member roles already mean, and would create two sources of truth. If a future mechanical check needs
an explicit containment edge, add `CONTAINED_BY` as a relation value in a separate bounded change; do not
add it now.

## Wording changes

### S1-CAND-01

Current assertion:

> every candidate names a neurologic subject for which the encounter poses its own assessment question

Proposed:

> every candidate names a clinically independent neurologic problem identity for which the encounter
> poses its own assessment question. A manifestation fully explained by an existing problem remains
> contained under that problem and is not a separate candidate; clinical importance, current monitoring
> or causal relevance alone does not create independent problem identity.

### S2-ADOPT-01

Current assertion:

> each S2 adoption verdict is supported by the supplied source/context for the current encounter

Proposed:

> each S2 adoption verdict is a proposition/object-level current-source endorsement, not a decision to
> create a problem block. A current source may endorse a residual deficit as a descriptor of a
> BACKGROUND problem without making that deficit a separate problem. Historical provenance alone does
> not forbid adoption; medication-only evidence does not establish it unless the source explicitly links
> it.

The packet instruction should say the same in plain language.

### S2-CAUSAL-01

Current assertion:

> every causal relation is source/current-formulation supported, with correct relation noun, strength,
> direction, and acting subject

Proposed:

> every causal relation is source/current-formulation supported, with correct relation noun, strength and
> direction. The acting subject is the most specific source-supported entity: use a named residual
> deficit/mediator when the source formulates it that way, keep a source-qualified parent disease when
> that is what the source attributes causation to, and never infer a mediator the source did not state.

### D-030 causal-subject paragraph

Current wording says a persistent deficit should be represented as the contributor **rather than**
substituting the historical disease label. That is too rigid when read as always replacing the parent.

Proposed replacement:

> When prior disease contributes through a persistent deficit, use the most specific source-supported
> acting entity. If the source names or qualifies the deficit as the mediator, represent that deficit as
> the contributor while the parent disease remains a compact background problem. If the source attributes
> causation to a source-qualified disease process instead, preserve that formulation. Do not infer a
> mediator the source did not state, and do not flatten a source-qualified parent into a bare historical
> label.

## Gate-0 impact

### Accepted groups

- **Group 1 (S1 candidacy): survives.** The wording clarifies independent problem identity; the accepted
  judgments and CASE-01/CASE-10 seeds do not change.
- **Group 3 (S2 representation): survives.** `R2` already contains `O01`/`O02`; containment is unchanged.
- **Group 5 (S3 encounter role): survives.** Role remains a property of the problem block; clean
  `S3-ROLE-01` packet `pkt-6dae7cba2d6a1243a2d10f7d` and its signer reference remain valid.

### Groups needing re-ratification

- **Group 2 (S2 adoption):** semantic wording changes; packets for `S2-ADOPT-01` change.
- **Group 4 (S2 causality):** semantic wording changes; packets for `S2-CAUSAL-01` change.

### Seeds and mechanical predicates

No seed or mechanical-predicate change is required. Current seeds already test:
- contained manifestation not promoted (CASE-01 `C2`/`R2`);
- current adoption of a contained residual weakness (CASE-10 `O02`);
- wrong causal subject (historical stroke vs residual weakness) and overstated strength.

### Packet impact

- `S2-ADOPT-01` and `S2-CAUSAL-01` packet bodies change because their assertion/instruction text is part
  of the packet digest; their packet IDs change.
- `S2-REP-01` and all other packet bodies are unchanged.
- Workload remains 44 packets / 42 records / 1 signer reference / 0 evaluators.
- The existing clean `S3-ROLE-01` reference remains reusable.
- Old `S2-ADOPT-01`/`S2-CAUSAL-01` references, if any, are invalidated; none exist in the current set.

## Files if approved

- `architecture-reboot/experiments/architecture/AX-S1S2-D/predicates.md` (wording);
- `architecture-reboot/scorer/registry.py` (assertions);
- `architecture-reboot/tools/gate0_harness.py` (S2-ADOPT/S2-CAUSAL packet instructions);
- `DECISIONS.md` (new decision, likely D-033);
- regenerated C3 packets/index; no seed or schema change.

## Requested review

- confirm that no `CONTAINED_BY`/`contained` field is needed for this Gate-0 contract;
- confirm the S2-ADOPT and D-030 wording;
- confirm groups 1/3/5 survive and groups 2/4 require re-ratification;
- authorize implementation only after review.

No Gate-0 acceptance. No Doximity. No Phase 0.
