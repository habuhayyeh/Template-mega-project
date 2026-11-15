# DeepSeek review — A0/A1/A2 three-way split

**Question:** is a three-way split better than the A1 preservation / A2 reconciliation split?

## Verdict

It is better on **speaker attribution** and **action isolation**. It is not sufficient, because it has no
owner for cross-record reconciliation.

Your A0 and A2 are right. A1 needs one correction: source-local assertion, not “one event/state” if that
means merging records.

## A0 — source registry

Keep it, but make it **mechanical**, not a generative pass.

It should carry:

- source IDs and record ranges;
- source type/date/author;
- section labels;
- raw speaker labels;
- explicit local identity only when the same record establishes it;
- no global `SPK# -> person` map;
- no inferred patient/family/clinician role.

If identity is unstable, record `role=unresolved`. Do not spend a model pass on this; Scribe already
provides most of it. A tool or a strict prompt can emit the registry.

## A1 — semantic units

“One question, one subject, one event/state, one semantic type” is the right shape only if it means
**source-local assertion/span**.

If A1 merges records into one event/state, it is doing reconciliation. That is the job that caused the
pointer fabrication and material omissions.

A1 should own:

- one source-local assertion/span;
- record ID + selector;
- assertion type: statement, question, observation, result, diagnosis, reasoning;
- raw speaker/source label;
- explicit local time/polarity/certainty;
- note-relevance class: HPI, neuro history, other PMH, meds, exam, workup, safety/function;
- local unresolved.

A1 must not:

- merge records;
- assign same_event/evolution/conflict;
- compress across sources;
- globally map speakers;
- decide problems/sections/prose.

It should include every material source-local assertion, including exam, meds, workup and safety. If
uncertain, include. Exclude only greetings, filler, nonassertion or nonclinical logistics.

## A2 — action lane

Keep it separate. It is orthogonal and high-risk.

Use source-local fields:

```text
target
operation
decision
execution
response
result
actor
setting
explicit time
condition
source record + selector
```

One episode per actor + target + operation + setting + time. Do not merge cruise, ED and longitudinal
continuation into one object. Do not infer intermediate states. Unknown fields absent.

But A2 should be **source-local action episodes**, not the final action reconciliation. Grouping repeated
mentions across records is reconciliation.

## Missing — A3 reconciliation

Your three-way split has no owner for:

- duplicate/corroboration;
- same event/state;
- evolution over time;
- conflict;
- cross-source synthesis;
- action-episode grouping;
- unresolved cross-record conflicts.

If A1 does it, A1 becomes the old overloaded pass. If B does it, B stops being problem architecture.

So the smallest correct map is:

```text
A0 Source Registry (mechanical)
  -> A1 Source-Local Semantic Units
  -> A2 Source-Local Action Episodes
  -> A3 Reconciliation
  -> B Problem Architecture
  -> C Note Compiler
  -> Render
```

A3 may compress A1/A2 into the sparse ledger B/C use. It may not alter A1/A2 source pointers, assertion
type, attribution, polarity, explicit action state or local unresolved. If it drops a unit, record a
disposition.

This is four logical phases, but A0 is mechanical and the other three are small. It is still one Ask call.

## Could you keep three?

Yes, if you fold A0 into Scribe/mechanical metadata and accept:

```text
A1 source-local units + actions
  -> A2 reconciliation
  -> B
```

But you lose the action separation that fixed the Keppra episode problem. I would not.

## Recommendation

Adopt A0 and A2 as you described. Correct A1 to source-local assertion/span. Add A3 reconciliation.

Do not let A1 merge; do not let A2 group across records; do not let B reconcile.

No acceptance, production change or Phase 0.
