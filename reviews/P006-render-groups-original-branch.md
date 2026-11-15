# P006 render/compose groups review — original architecture branch

## Verdict

**REVISE — direction accepted; current proposal still leaves the decisive semantic choice inside 05.**

The architectural direction is correct:

- keep the six semantic kinds;
- keep 04 lossless;
- move duplicate/composition decisions upstream;
- preserve every O# and provenance for audit;
- let 05 format an already-decided structure rather than rediscover semantic equivalence.

However, P006 as written does not yet fully achieve that.

## 1. RENDER_GROUP still asks 05 to choose the representative

Current rule:

> 05 renders it once, using the member whose wording carries the most

That is another semantic selection rule. Two runs can choose different members, which is exactly the instability P006 is meant to remove.

### Required change

The group manifest must specify the rendering roles upstream, not only membership.

For example:

```text
RENDER_GROUP G1 | HEAD=O7 | MODIFIER=O8 | COVERED_DUPLICATE=O53
RENDER_GROUP G3 | HEAD=O44 | COVERED_DUPLICATE=O17
RENDER_GROUP G4 | HEAD=O23 | COVERED_DUPLICATE=O39
RENDER_GROUP G5 | HEAD=O34 | COVERED_DUPLICATE=O32
```

The exact role names can differ, but the principle is mandatory:

- **HEAD** = the member whose wording supplies the proposition;
- **MODIFIER** = distinct payload that must be folded into the HEAD;
- **COVERED_DUPLICATE** = retained source/provenance that the group accounts for but does not independently render.

05 must not choose among members.

## 2. COMPOSE_GROUP still asks 05 to judge compatibility

Current rule:

> renders them as one line when they are compatible — and as separate lines when they are not

That again leaves the semantic decision at render time.

If 03 creates a COMPOSE_GROUP, compatibility must already have been adjudicated upstream.

### Required change

A valid COMPOSE_GROUP is an instruction to compose.

Example:

```text
COMPOSE_GROUP G2 | ACTION=O12 | CONDITION=O25
```

05 renders one decision using the ordered roles.

If the group is structurally invalid, validation fails **before** 05. 05 should not decide to split it.

## 3. Group roles must preserve rhetorical class

Define allowed combinations.

Recommended minimum:

- factual RENDER group: EVIDENCE HEAD + optional COURSE MODIFIER + covered duplicate EVIDENCE/COURSE;
- reasoning RENDER group: CLAIM_QUALIFIER/ETIOLOGY members only, unless a future proposal explicitly allows otherwise;
- plan COMPOSE group: MANAGEMENT members only.

A group must not silently move an object between fact/reasoning/plan classes.

## 4. Frozen examples need source-fidelity correction

### G1
Current target:

`known left MCA infarct, two years prior to presentation (prior neurology, 2024-02)`

O7/O8 are current-encounter facts; O53 is only the prior-neurology duplicate.

Attaching O53's provenance to the whole merged sentence can imply that the prior record supplied the timing. It did not.

Prefer:

- HEAD O7;
- MODIFIER O8;
- O53 as covered duplicate whose provenance remains in the trace/group metadata but need not appear in prose.

Target:

`Known left MCA infarct, two years prior to presentation.`

No historical attribution is required merely because a duplicate source existed.

### G3
Current target:

`CT head without hemorrhage or acute abnormality`

The Handoff says `CT head no hemorrhage` and `CT head no acute abnormality`. The word `without` is not sourced by those objects or the accepted transformations.

If both payloads are intentionally retained, render source-faithfully, e.g. as the bounded combination of the source fragments. Better still, choose one as HEAD and the other as covered duplicate if 03 adjudicates them as one proposition.

Do not add a new synonym merely because the group exists.

### G4
Current target `the MRI will tell us` drops `but` from O23. If O23 is HEAD, preserve its wording under the existing transformations; if O39 is HEAD, use that wording. The group must name which one.

### G5
O34 already contains the full proposition `family's concern about her memory is not today's issue`. Use O34 as HEAD and O32 as covered duplicate rather than recomposing a new phrase.

## 5. "No member's distinct content may vanish" needs a formal distinction

A covered duplicate may disappear from prose precisely because it has **no distinct clinical payload**.

So define:

- HEAD payload must render;
- MODIFIER/CONDITION payload must render;
- COVERED_DUPLICATE payload is intentionally not rendered separately because its clinical content is already represented by another member;
- all O# and provenance remain auditable in metadata/trace.

Without this distinction, the rule conflicts with the purpose of deduplication.

## 6. 03 owns semantic grouping; 04 only transports it

Accepted architecture:

`03 semantic adjudication -> group roles -> 04 lossless dereference/pass-through -> 05 bounded formatting`

Do not describe 03 grouping as mechanical. It is semantic and reviewable. The **transport and validation** can be mechanical.

## 7. Validation requirements

Before 05:

- every referenced O# exists and is retained;
- no object is in more than one group;
- no group spans problems;
- group type/roles are valid;
- rhetorical classes are compatible;
- required roles are present;
- COMPOSE groups are already adjudicated as composable.

After 05:

- every HEAD/MODIFIER/CONDITION is traceable to the one rendered line;
- every COVERED_DUPLICATE is accounted for but not rendered independently;
- no group creates more than its permitted number of lines.

## 8. Relationship to P005

P005 remains a fail-only mechanical guard.

Once P006 groups are explicit, P005 can validate group conformance much more reliably than trying to discover semantic duplicates from prose.

That is a good interaction:
- P006 decides semantic equivalence once;
- P005 checks that 05 obeyed the group.

## 9. STATUS

STATUS is stale relative to set3. It still says the next step is P005 followed by another complete-package run and describes the earlier two-run state.

After P006/P005 direction is settled, regenerate STATUS to reflect:
- set3 completed in Instant mode;
- Doximity remains failed for semantic grouping/compression;
- P006 under review;
- P004 still held for management-target representation.

## Next

Revise P006 so the manifest carries **roles, not just membership**, and 05 has no semantic choice about representative member or compatibility.

No signer escalation is needed. This is an architecture/reproducibility correction, not a clinical or stylistic preference.
