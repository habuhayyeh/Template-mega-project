# Review 141 — first A1 -> A2 combined run

## Verdict

**FAIL — the A1/A2 split is directionally justified, but neither boundary is yet reliable enough to advance to B.**

The run is useful because it separates two failure classes that were conflated in single-pass A:

1. **A1 source-local preservation still has source-fidelity and coverage defects.**
2. **A2 then violates A1's protected semantics and invents/reassigns states.**

This means the split itself is not disproven. In fact, the output makes the boundary failure easier to see.

However, the next step should **not** be B/C integration.

---

# A1 assessment

## What A1 improved

A1 materially improves preservation compared with single-pass A:

- current ED exam survives;
- safety counseling survives;
- ED differential survives;
- Keppra actions are source-local rather than globally merged;
- no global speaker identity table is emitted;
- the output is auditable at span level.

This is the right direction.

## A1 blocking failures

### 1. Exact source-pointer rule is violated

A1 contract requires:
- one source record;
- one selector actually present in that record;
- no adjacent-record synthesis.

But examples violate this directly.

#### S052

A1 writes:

`selector=P1.040: "Skin: warm. Neurological: no focal deficit present; alert and oriented..."`

The actual source has:
- P1.040 = Skin: warm.
- P1.041 = Neurological: no focal deficit; alert/oriented.

So one A1 span merges two source records and mislabels the neurologic exam as P1.040.

#### S053

A1 writes:

`P1.030: "Constitutional appearance: normal. Head: normocephalic and atraumatic. Eyes: EOM intact."`

But those are distributed across:
- P1.030 constitutional;
- P1.031 head;
- P1.035 eyes.

Again: one synthesized selector attached to one source pointer.

#### S047

A1 writes T162 as including:
- Flavilla;
- vitamins/calcium;
- Chlorella;
- Q10;
- enzymes.

But T162 contains only Flavilla + vitamins/calcium.
Chlorella/Q10 are T179, enzymes are T180.

This is exactly the source-local synthesis A1 was created to prevent.

### 2. A1 is not complete enough yet

Two oracle-critical source distinctions are absent from A1:

- family seizure history answer T155;
- ED seizure precautions P1.044.

Also absent:
- explicit no-tongue-bite/current ED exam qualifier from P1.043.

A1 therefore still fails the "if uncertain, include" preservation rule.

### 3. Multi-assertion records are not split enough

P1.045 is represented as one action span S055 containing:
- CT;
- labs;
- UA;
- neurology consult;
- likely admission for EEG.

Those are separate downstream action trajectories.

T141 is represented as one action span S062 containing:
- need EEG;
- question about prior EEG;
- CT already performed/not reviewed;
- MRI needed;
- inpatient/outpatient discussion.

Because A1 does not split these, A2 later has to rediscover or invent the individual states.

### 4. `source=` does not follow the contract

A1 uses:
- `source=P1`
- `source=T`

while the exact record identity is embedded in selector text.

The contract says `source=<record ID>`.

This weakens machine/audit traceability and likely contributes to pointer drift.

### 5. Some source-local action states are still interpretive

Example:
- P1.054 `Neuro: Keppra load 1500; will come evaluate`
  becomes `decision:planned`.

That shorthand may reflect a recommendation/order, but does not explicitly say "planned."

A1 should prefer a minimally interpretive source-state representation when the exact state is ambiguous, or mark unresolved rather than force one enum.

---

# A2 assessment

A2 fails more severely because it violates the exact invariants that the split was intended to create.

## 1. Question-as-answer returns

U004:
- concept = no prior diagnosed seizure history;
- evidence includes S003:T153.

But S003 is explicitly an A1 `assertion_type=question`.

A2 therefore again uses a question inside support for a negative statement.

This violates:
> A question cannot corroborate a statement.

## 2. A2 invents speaker identities

Examples:
- U001 attribution = `Patient/fiance/mother collateral`;
- U003 = `Patient via mother collateral`;
- U005 = `Patient self-report + fiance observation`;
- U006 = `Mother/patient`;
- U007 = `Patient/mother`.

A1 intentionally preserved raw SPK labels because the packet is not identity-stable.

A2 is therefore reopening the exact identity inference A1 was designed to freeze.

## 3. A2 invents action states absent from A1

Examples:

### A003
- A1 S056 = `decision:planned`.
- A2 adds `execution=ordered@S056`.

Forbidden.

### A004
- A1 S060 = `decision:continue`.
- A2 adds `execution=not_started@S060`.

Forbidden.

### A005
- A1 S062 = only `decision:planned`.
- A2 creates:
  - `execution=reported_performed`;
  - `result=pending`.

The source text may mention prior CT, but A1 did not preserve those as source-local action states. A2 is silently repairing A1 by rereading the packet.

### A006/A007
A2 adds:
- `execution=not_started`;
- `result=pending`;

without those states existing in A1.

### A008
A2 creates:
- `execution=ordered@S055`;

although S055 contains only `decision:planned`.

It also attaches cruise-lab final results to an ED labs/UA action, conflating distinct episodes.

## 4. A2 action episode identity is unreliable

A001 is labeled "Keppra drip cruise first night" but:
- `source_spans=S019 S020` are blood tests/IV-for-BP spans;
- decision/execution point to S059, which A1 timestamps Thursday after cluster.

This is internally inconsistent.

A001 appears to invent a Wednesday Keppra episode from unrelated spans.

## 5. Disposition accounting is not trustworthy

Example:
- S007 = allergy statement.
- A1_DISPOSITION says `represented_in:U005` with reason `no allergies`.
- But U005 is recurrent staring/zone-out spells.

So the ledger says a source span is preserved when it is not actually represented in that unit.

Similarly:
- S055 contains CT + labs + UA + consult + admission;
- disposition maps only to A005 CT.

The remaining content is not faithfully accounted for.

This defeats the reason `A1_DISPOSITION` exists.

## 6. Malformed evidence pointer

U004 contains:

`S049:S186-068`

which is not a valid A1 span/source reference.

---

# Architectural interpretation

The split is **still the right direction**, because the output now cleanly exposes where corruption occurs.

But the contracts are not yet strict enough to force the intended isolation.

The evidence suggests two different fixes:

## A1 needs stronger mechanical source-locality

A1 should be even less semantic.

Recommended changes:

1. `source_record=<exact ID>` mandatory.
2. `selector=<exact substring from that one record>`.
3. No selector may contain text from another record.
4. One span cannot contain multiple materially distinct action/result assertions.
5. For action-state ambiguity, preserve source wording + unresolved rather than force an enum.
6. Explicit coverage floor for:
   - all current exam findings relevant to neurology;
   - all management/safety actions;
   - all explicit patient/family seizure-history answers/questions;
   - all workup state changes.
7. Add a mechanical span check: every selector must be a literal substring of the cited source record.

This last check can be development-time code/lint, not another LLM stage.

## A2 needs harder immutability rules

A2 should not be allowed to write free-form attribution or action states.

Recommended changes:

1. `attribution` must be assembled only from A1 speaker/source tokens; no patient/mother/fiance labels unless A1 explicitly contains those identities.
2. Every A2 action state must cite an A1 span whose `action_state` is exactly that same state.
3. A question span may only have evidence role `context` or `question`, never `support` for a statement.
4. A2 may not reread source text to infer a state A1 failed to encode.
5. `A1_DISPOSITION` should be mechanically checkable:
   - represented span must actually appear in the referenced UNIT/ACTION.
6. No action can contain source spans from a different setting/time episode.

---

# Important runtime lesson

This was a combined A1 -> A2 execution, not a clean standalone A1 capability run.

Therefore:

- we can inspect the A1 artifact;
- but we have **not yet demonstrated** that A1 alone behaves the same when A2 instructions are absent.

The combined run already fails, so no downstream progression is justified.

The clean next experiment should be:
1. patch A1/A2 contracts narrowly;
2. run **A1 alone** on the frozen packet;
3. validate exact source-pointer/selector fidelity and coverage;
4. only then feed that exact frozen A1 artifact to A2;
5. evaluate A2 against immutability + the existing oracle.

Do not run A1 and A2 together again until each standalone boundary works.

---

# Verdict on architecture

**KEEP A1/A2. DO NOT REVERT TO SINGLE-PASS A.**

The split made the failure location clearer:

- A1 still needs a stricter source-local representation.
- A2 still behaves like a second semantic editor instead of a reconciliation-only consumer.

This is a contract/isolation problem, not evidence that the decomposition itself is wrong.
