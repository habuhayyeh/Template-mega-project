# Review 142 — unified source-local A full-packet run

## Verdict

**FAIL — A completes at scale, but action-state handling remains a fatal capability defect. Do not advance to B/C.**

This is the first standalone run of the accepted unified `01-SOURCE-LOCAL-INGESTION.md` contract on the frozen seizure packet.

The run is useful because it shows that the new source-local architecture materially improves several prior failure classes:
- output completes with `@@END`;
- current ED neurologic/general exam survives;
- patient prior-seizure history and family seizure history remain separate;
- baseline staring survives;
- ship/outside workup survives;
- seizure precautions and driving/water/heights safety content survive;
- current differential/reasoning survives;
- no cross-record same-event/evolution/conflict relations appear;
- no PRIMARY/BACKGROUND, containment, note-section, or final-prose decisions appear.

However the accepted contract's sparse-action rule is still not obeyed.

## Fatal action-state promotion

The contract says:
- preserve only source-local action state explicitly supported by the local source wording;
- `plan` does not imply `ordered`;
- `recommended` does not imply `ordered`;
- unknown fields stay absent;
- do not fill a template;
- if exact state is ambiguous, omit the state field and use `unresolved`.

The run repeatedly violates that rule.

### A001-A003 — planned ED workup is template-filled

For CT, labs, and urinalysis, the run emits:

- `decision=planned`;
- `execution=not_started`;
- `result=unavailable`.

The plan supports the decision state. It does not by itself establish either execution state or result state. Those extra fields are schema completion, not source-local preservation.

### A004 — consult plan upgraded to ordered

`P1.045` / `consult neurology` is represented as:

- `decision=planned`;
- `execution=ordered`.

This violates the explicit invariant that a plan does not imply an order.

### A006 — Keppra load receives two unsupported normalized states

`P1.054` / `Keppra load 1500` becomes:

- `decision=recommended`;
- `execution=ordered`.

Prior review of this exact record already established that the shorthand is ambiguous enough that A should not force a state beyond what the wording supports. The new contract specifically says ambiguous state stays absent/unresolved. This is therefore a material action-state promotion and a **fatal oracle failure**.

### A009-A012 — repeated template filling

EEG, MRI, continued Keppra, and admission all receive extra `execution=not_started` and/or `result=unavailable` fields despite the local action wording not establishing those states.

The most obvious example is:

`will keep on Keppra for now` -> `decision=continue` + `execution=not_started`.

The decision is supported; `not_started` is not.

## Lane-separation defects

The semantic lane is defined as source-local **non-action** assertions, but the run places action content there.

### S014

`put her on a Keppra drip` appears as a SEMANTIC_SPAN with `material_role=workup`, then appears again correctly as ACTION_SPAN A008 with `execution=reported_performed`.

That is a direct lane-boundary violation.

### Safety counseling

Driving/water/heights precautions survive as semantic safety spans, but no corresponding action spans represent the counseling/restriction action. A2 is supposed to preserve each source-local action assertion, so preservation is incomplete at the action lane even though the content survives somewhere in A.

## Semantic typing drift

The same T228 witness content is represented twice:
- S030 as a current-episode statement;
- S038 as reasoning.

The selector in S038 is descriptive witness evidence, not reasoning. This suggests that the semantic lane still performs some local type invention even without cross-record reconciliation.

## Coverage

Important improvements:
- P1.041/P1.043 current exam survives;
- P1.044 seizure precautions survive;
- patient and family seizure-history material survive separately;
- baseline zoning survives;
- ship workup survives;
- current ED workup plans survive;
- current safety counseling survives;
- differential/PNES reasoning survives.

One known medication/supplement coverage defect remains: the frozen packet contains later T179/T180 supplement material (Chlorella/Q10/enzymes) identified in Review 141. The new run correctly stops merging it into T162, but now omits it rather than preserving it source-locally. That is a coverage-floor failure, not a pointer fix.

## Mechanical selector lint

A complete exact-substring lint cannot be executed from this returned A artifact alone because the frozen clinical Scribe packet is intentionally not committed to GitHub.

The output does contain one internally suspicious pointer:
- A005: `source_record=P1.044`, selector `Placed on seizure precautions`;
- A013: `source_record=T044`, same selector, but `speaker_source=P1`.

That is highly suggestive of a source-record drift/duplicate and should be checked against the frozen packet before accepting any mechanical-fidelity claim.

This limitation does **not** change the verdict because the action-state promotion is already independently fatal.

## Failure classification under the frozen oracle

### Demonstrated
- **action-state handling:** FAIL — fatal;
- **source-semantic extraction/coverage:** partial FAIL;
- **lane classification:** FAIL.

### Not demonstrated as the cause
- context/output-size overload;
- truncation;
- cross-record reconciliation pressure.

## Architectural implication

Do **not** patch B/C and do not treat the unified A contract as passed.

The important new evidence is that the prompt already says:
- unknown fields absent;
- do not fill a template;
- plan != ordered;
- recommendation != ordered;
- ambiguous state -> omit + unresolved.

Yet GPT-4o still fills action-state slots.

So another prose-only repetition of the same rule is unlikely to be a meaningful experiment.

The next peer question should be narrower:

> Is the action lane itself too schema-completing for GPT-4o when embedded beside semantic ingestion, and should the next development experiment isolate the action lane or change its representation so unsupported state fields are structurally impossible?

Do not redesign the whole architecture from this one run. First isolate whether the failure is:
1. action-lane representation;
2. same-pass lane interference;
3. source-pointer fidelity.

No Gate-0 acceptance. No production change. No B/C progression.
