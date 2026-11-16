# Decision 004 — revised next step

**Status:** architect decision. Supersedes decision 003 where it deferred A polarity.

## Decision

Accept the expert’s challenge.

1. Patch B’s problem-identity threshold.
2. **Quarantine A polarity from C** — do not merely defer it and hope C ignores it.
3. Run C against frozen B outputs.
4. Gate the blueprint structurally.
5. Render.

Do not redesign A polarity now. Do not let C consume the field.

## 1. B threshold

Rule:

> A chronic/baseline phenomenon is a separate neurologic problem only if it has independent
> disease/syndrome identity or would independently merit substantive neurologic assessment/management
> apart from its role in characterizing another problem. Otherwise it stays as comparator/evidence/
> context inside the relevant problem.

Use the counterfactual test:

> If the primary presenting problem disappeared, would the clinician still regard this phenomenon as a
> problem worth naming, evaluating, monitoring or managing?

- No -> comparator/evidence.
- Yes -> candidate separate problem.

Test fixtures:

1. Baseline staring spells used only to distinguish current events -> no separate problem.
2. Same spells independently under current evaluation -> separate problem.
3. Established chronic neurologic disease with current event comparison -> disease identity retained;
   role according to activity.

All three must pass. This prevents a rule that fixes case 1 by collapsing case 3.

## 2. A polarity quarantine

A’s mixed-polarity span is known-bad. Do not let it remain consumable.

C must not use unit-level polarity to:

- negate content;
- infer presence/absence;
- decide abnormality;
- decide evidence direction;
- change inclusion;
- rewrite mixed assertions as uniformly positive/negative.

If the field remains for telemetry, it is non-operative. If A is touched minimally, mixed assertions
should be `MIXED`/`UNSPECIFIED`, not `affirmed`/`negative`. Do not build a polarity model now.

## 3. C ownership

C owns **document function and placement**, not clinical meaning.

C may:

- place content in a section;
- include/omit according to B’s disposition;
- order by chronology, B problem order, or source-supported action order;
- link an item to a problem using a B-authorized role;
- repeat an item for a permitted function;
- group/compress an already-typed group;
- cross-reference an action.

C may not:

- decide whether evidence supports or opposes a problem;
- decide which problem owns an action;
- change problem identity, class, claim, certainty, currentness, causality or action state;
- split, merge or promote a problem;
- invent a relationship.

B must supply the relationship:

```text
item -> problem
role = evidence | counterevidence | comparator | context | plan
```

C instantiates that relationship; it does not infer it.

## 4. Operators

Closed set is enough:

```text
HOME(section)
INCLUDE / OMIT
ORDER(chronology | problem order | action order)
LINK(problem_id, role)
REPEAT(destination, function)
GROUP(group_id)
COMPRESS(group_id)
CROSSREF(action_id)
```

C chooses an operator; it does not invent a role or a clinical claim. If no operator fits, the blueprint
item is unresolved, not repaired.

## 5. Gates

### Gate 1 — B problem identity

Hand-authored fixtures, expected problem identity set predeclared. Pass all three threshold cases.

### Gate 2 — C no-new-meaning

```text
problem IDs(C) == problem IDs(B)
problem class(C) == problem class(B)
claim identity(C) == claim identity(B)
```

No split, merge, promotion, role change, certainty change, new causality, new currentness, new action
state.

### Gate 3 — relationship provenance

Every C link must trace to a B-authorized relationship. If C has to decide support/opposition or action
ownership, the B->C contract is incomplete.

### Gate 4 — no semantic inversion

C may shorten, relocate or repeat. It may not change subject, attribution, temporal scope, certainty,
presence/absence or action state.

### Gate 5 — render

No new clinical claim; no polarity, certainty, currentness or action-state change; no counterevidence
loss.

## 6. Biggest risk

C becomes a clinically intelligent allocator that quietly repairs B. It will look good on easy cases and
hide bad B outputs.

Mitigation: immutable B problem IDs, B-authorized relationship labels, closed operator set, blueprint gate
before prose.

## 7. Delete/defer

Delete from C authority:

- deciding evidence support/opposition;
- deciding action ownership;
- any C-level problem threshold.

Defer:

- full A polarity redesign;
- new C repair layer;
- same-model blueprint validator;
- new stages or action-state enums.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
