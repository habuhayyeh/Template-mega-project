# DeepSeek adjudication — post-D053 architecture review

**Reviewed:** ChatGPT review 150.
**Status:** architecture adjudication. No implementation.

## Verdict

Mostly accept. The review identifies real gaps, but the order needs one correction.

Do the **A-necessity comparator first**, with the B problem threshold patched so P002 does not confound
it. Do not redesign C yet.

Then, if A survives, add B reconciled clinical units and redesign C around typed groups/operators.

## Accept / reject

### 1. A necessity — ACCEPT as an experiment, not a conclusion

The omission-sink argument is real: B cannot discover actions A omitted. But direct-B may omit too, and
may lose A’s source-local discipline. The clean packet is compact enough to test.

Run one controlled comparator:

- Arm 1: `Scribe -> A -> B`
- Arm 2: `Scribe -> B-direct`

Same B synthesis responsibilities, same source-qualified wording, no action-state enums, same target
note/oracle. B-direct must cite exact Scribe record IDs/selectors itself and preserve action splitting.

Do not delete A before the result. If direct-B matches or improves, A is unnecessary for this packet
class. If A wins, minimize A’s polarity/certainty metadata.

### 2. B reconciled clinical units — ACCEPT

B owns episode/baseline reconciliation but emits only problems/actions. C would have to redo event
identity and baseline-vs-current placement. That violates ownership.

Add a compact `CLINICAL_UNIT` output:

```text
CLINICAL_UNIT U001
  kind=current_event | baseline_comparator | longitudinal_history | exam | workup | context
  label=<short>
  evidence=<A/Scribe refs>
  chronology=<supported order>
  relation_to_problem=<P handle or none>
```

This is not an episode model stage. It is B’s reconciled output. It also solves P002: baseline spells
become a `baseline_comparator` unit under P001, not a problem.

### 3. C typed groups/operators — ACCEPT, but after B units

Current C is not decision-complete. `content/function/preserve` leaves merge/split, rhetorical class,
head/modifier, condition, coverage and order to the renderer. That contradicts the B+ and operator-stress
evidence.

Redesign C around:

- typed render groups;
- HEAD/MODIFIER/CONDITION/COVERED;
- rhetorical class;
- explicit order;
- canonical operator;
- fail-closed malformed groups.

Reuse tested operator families; do not invent an open prose schema.

Do this after B emits reconciled units, otherwise C has nothing stable to compile.

### 4. C raw-source freedom — ACCEPT

C should consume A/B decisions and mechanically dereference cited A/B records only. Do not give C full
packet semantic freedom. C must not discover new clinical content.

### 5. P002 — ACCEPT

B threshold defect, not architecture. Patch B:

> A chronic/baseline phenomenon becomes a separate problem only if it has independent neurologic
> disease/syndrome identity or would independently merit substantive assessment/management. Otherwise it
> stays as comparator/evidence/context under the relevant problem.

Use the counterfactual test and three fixtures:

1. baseline spells used only as comparator -> no separate problem;
2. same spells independently evaluated -> separate problem;
3. established chronic neurologic disease with current event comparison -> disease identity retained,
   role per activity.

### 6. Preserve — ACCEPT

Keep:

- source-qualified action wording;
- one Ask call with logical phases;
- B as clinical synthesis/problem owner;
- renderer as bounded lexicalizer;
- final-note signer review.

Do not reopen B1/enums, validators, micro-stages, or final-writer reasoning.

## Corrected sequence

1. **Patch B threshold** and run the three fixtures.
2. **A vs direct-B comparator** on the clean packet, same B contract and oracle.
3. Decide A: keep/minimize or delete.
4. **Add B `CLINICAL_UNIT` output**; test B alone.
5. **Redesign C** with typed groups/canonical operators; test blueprint only.
6. **Render**; final-note comparison.

Do not run current C.

## Comparator design

### Arm 1

`Scribe -> A -> B`

Use the frozen A output and current B contract.

### Arm 2

`Scribe -> B-direct`

B-direct contract:

- source-local exact record IDs/selectors;
- no invented facts/actions;
- source-qualified wording;
- problem architecture, diagnostic stance, action ownership;
- unresolved rather than guessing;
- same output shape as B.

### Compare

- clinical coverage;
- attribution/provenance;
- action preservation/splitting;
- problem identity/containment;
- diagnostic stance;
- hidden semantic errors;
- concision/output size.

Use the existing target-note oracle. Do not compare prose style.

## Biggest risk

Direct-B looks better because it avoids A’s visible intermediate errors, but silently loses source-local
discipline. Mitigation: score action coverage and pointer/provenance fidelity from the Scribe packet, not
just final B plausibility.

No C until B output is decision-complete. No acceptance, production change or Phase 0.
