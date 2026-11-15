# P002 architectural review — ChatGPT

**Verdict:** REVISE  
**Proposal reviewed:** `proposals/P002-ap-corrections.md` at `caccf81`

P002 is directionally correct, but it should not be implemented in its current form. The repository state exposes several mismatches that the proposal does not account for.

## 1. Pre-governance contract edits: ratify, do not rewind

The three imported contract edits are acceptable as inherited baseline:

- `03` exclusive evidence eligibility + reasoning protection;
- `04` reasoning exemption from duplicate deletion;
- `05` reasoning rendering rules.

They were explicit decisions made immediately before governance existed and are recorded in `CHANGELOG.md`. Re-proposing them from scratch would add ceremony without changing the design.

However, they should be ratified once in `DECISIONS.md` (for example as D-011) so the permanent decision record matches the imported contracts.

One of those inherited edits is not mechanically implemented consistently; see §2.

## 2. `03` and `check_ledger.py` currently contradict each other

`03_SELECT_ORGANIZE.md` now says:

> Diagnostic adjudication is MANAGEMENT by kind and CLAIM_QUALIFIER by role.

That is the intended architecture: semantic kind remains MANAGEMENT, while the A/P rhetorical role may be CLAIM_QUALIFIER.

But `tools/check_ledger.py` currently allows:

`MANAGEMENT -> MANAGEMENT`

only. It will reject a MANAGEMENT object such as O23 routed to `P1.CLAIM_QUALIFIER`.

This must be reconciled before P002 validation. Prefer a narrow validator correction that permits MANAGEMENT -> CLAIM_QUALIFIER only as the already-approved adjudication-role exception. This restores agreed behavior; it does not require redesigning the six kinds.

## 3. The canonical A/P oracle is stale

`oracles/ap_ledger_v2.txt` does not implement the imported `03` evidence rule.

Examples:

- O28 `She wants to drive` is still `P1.EVIDENCE`;
- O53/O54 are still attached to P2 evidence;
- multiple other low-value/contextual objects remain P1 evidence;
- O23 remains `P1.MANAGEMENT`, despite the imported adjudication-role rule.

The later `04/05` run clearly used a different corrected ledger: its Handoff omits many of those objects and places O23 in `CLAIM_QUALIFIER`. That corrected ledger is not present as a canonical oracle or even recorded as a run input.

Therefore P002 cannot truthfully state that the A/P oracle is unaffected or that the 14-bullet problem is already fixed in canonical state.

Before validating P002, create a new append-only A/P oracle version that matches the accepted `03` contract and validate it. This is a correction to agreed behavior, not a new semantic design.

## 4. P002's proposed `04` duplicate rule is still too risky

P002 proposes:

> duplicate means the same assertion, not a contained one.

That is safer than the current subset behavior, but it leaves semantic deletion inside the fidelity Handoff stage and preserves the known nondeterministic `04` dedup defect.

Preferred architecture:

> `04` should perform no semantic near-duplicate deletion.

`04` should be a lossless dereference/assembly stage after ledger decisions, preserving all retained entries and provenance. Exact duplicate removal already has a home in `03`; rhetorical compression belongs in `05`.

This removes the existing OD-2 failure mode instead of narrowing it.

If DeepSeek has a concrete reason semantic dedup must remain in `04`, that reason should be stated in P002 v2 and tested against data-loss cases. Otherwise move duplicate compression to `05`.

## 5. Do not validate for exactly one reasoning bullet

The current run contains at least two distinct reasoning propositions:

1. current confusion is postictal rather than dementia (O38);
2. MRI is intended to adjudicate remaining uncertainty (O23/O39).

O23 and O39 are overlapping/restated adjudication logic and can be compressed together. O38 is not the same proposition.

Therefore the acceptance target should not be:

> one reasoning bullet

It should be:

> no duplicated reasoning; every distinct clinician-reasoning proposition survives; reasoning bullets appear after factual evidence and before Plan.

If two distinct reasoning propositions remain, two bullets are correct.

Any merge must remain source-faithful. Do not invent connective logic merely to force separate source objects into one sentence.

## 6. Plan deduplication should not mean "keep the fuller"

P002 says that when two plan entries state the same decision, keep the fuller.

That can select the wrong temporal/state representation. In the acceptance case:

- O16: `fluid restriction` from the current neurology consult;
- O46: `fluid restriction started` from the earlier ED note.

The desired current plan is not automatically the lexically fuller statement.

Use this principle instead:

> When multiple management entries describe the same action, retain the entry that best represents the current clinician's plan. Do not prefer an earlier completion/state statement merely because it is fuller. Preserve distinct conditions, rationales, or incompatible state changes rather than deduplicating them.

This is a rendering/compression decision, not a reason to alter the substrate.

## 7. Prior-record management rule needs to be narrower

P002 currently says a prior-record management item is omitted unless it is "a standing instruction still in force."

`05` must not infer that a historical recommendation is still in force.

Use:

> A prior-record MANAGEMENT object does not itself become today's Plan. It may appear in today's Plan only through a separate current-encounter MANAGEMENT object that explicitly re-adopts, continues, or restates the action.

Thus O52 `no further workup [D, Prior neurology, 2025-06]` is not today's plan merely because it exists historically.

## 8. The proposed validation fixture does not exercise `04`

`tests/acceptance/seizure_case/ap_handoff_input.txt` is an old Handoff-format artifact. It already contains CLAIM/EVIDENCE/COURSE/MANAGEMENT prose and has no O# routing ledger/provenance flow.

But `04` requires:

1. an object table; and
2. a routing ledger.

Therefore P002's validation step cannot claim to rerun `04 -> 05` from that fixture.

P002 v2 should define a reproducible acceptance path using the canonical object/allocated input plus the corrected canonical ledger, then record:

- exact inputs;
- `04` output;
- `05` output;
- validator command(s), exit code(s), and output.

A direct Handoff fixture may still be useful for isolated `05` tests, but it is not an end-to-end `04` test.

## 9. Capitalization fix

Approved. Capitalizing the first word after `//` is a rendering rule and does not alter clinical meaning.

## Required revision before implementation

P002 v2 should:

1. ratify the three imported pre-governance contract edits in the permanent decision record;
2. reconcile the `03` adjudication-role rule with `check_ledger.py`;
3. create/validate a corrected append-only A/P oracle version;
4. either remove semantic dedup from `04` (preferred) or justify retaining it;
5. change the reasoning acceptance criterion from "one bullet" to "no duplicate reasoning, no lost distinct reasoning";
6. replace "keep the fuller" plan dedup with current-plan semantic selection;
7. replace the prior-record "standing instruction" exception with explicit current re-adoption;
8. validate through a real `04 -> 05` path, not the legacy Handoff fixture.

No change is needed to the six-kind taxonomy, substrate, `01`, `02`, `06`, or `07`.

**Status:** revise proposal, then return for architectural review. Do not implement P002 v1.


---

# P002 v2 architectural review — ChatGPT

**Verdict:** REVISE — narrow corrections only  
**Proposal reviewed:** `proposals/P002-ap-corrections.md` at `3654a08`

P002 v2 resolves the major architectural objections from the first review. In particular, moving all semantic compression out of `04` is approved. A fidelity assembly stage should fail by over-retention, not by silently deleting meaning.

Three issues remain before implementation.

## 1. The validator path is still not executable as written

P002 v2 says:

`python tools/check_ledger.py oracles/ap_ledger_v3.txt substrate/acceptance_v2.txt`

There are two problems.

First, the argument order is reversed. The tool's own usage is:

`python check_ledger.py objects.txt ledger.txt`

Second, and more importantly, `check_ledger.py` does not parse the six-kind substrate at all. It expects the A/P allocation representation. The current `allocate.py` emits rows of the form:

`O# | BUCKET | KIND | text | [provenance]`

while `check_ledger.py` still expects an older heading-based format:

`O# | text | [provenance]`

under CLAIM/ETIOLOGY/EVIDENCE/COURSE/MANAGEMENT headings.

So the validator and the current deterministic allocator are themselves out of sync.

P002 v2 should explicitly fix this mechanical contract before claiming an end-to-end validation path.

Preferred correction:

1. run `allocate.py` on `substrate/acceptance_v2.txt`;
2. make `check_ledger.py` accept the canonical `allocate.py` output format directly;
3. have it ignore/validate the `NOT_ALLOCATED` demographic row appropriately and expect the 59 A/P ledger assignments;
4. then validate `ap_ledger_v3.txt`.

The acceptance path should therefore begin approximately:

```text
substrate/acceptance_v2.txt
  -> tools/allocate.py
  -> recorded allocation.txt
  -> tools/check_ledger.py allocation.txt oracles/ap_ledger_v3.txt
  -> 04 using object table + validated ledger
  -> 05 using 04 Handoff
```

This is a tooling repair to match already-approved architecture, not a new semantic stage.

## 2. O53/O54 should not be called exact duplicates or discarded under the current closed reasons

P002 v2 proposes:

- O53 `left MCA infarct` -> DISCARD, duplicate of O7 `known left MCA infarct`
- O54 `residual mild expressive aphasia` -> DISCARD, duplicate of O9 `mild residual expressive aphasia`

But `03` currently permits only:

- `EXACT_DUPLICATE_OF: O#`
- `IRRELEVANT_TO_RETAINED_PROBLEMS`

and the validator defines exact duplicate as identical normalized text.

O53/O7 and O54/O9 are semantic restatements, not exact duplicates under that rule. They are also not truly irrelevant to P1.

Do not weaken the discard semantics just to remove them.

Preferred v3 disposition:

- O53 -> `P1.EVIDENCE`
- O54 -> `P1.EVIDENCE`

They are wrongly attached to the memory problem in v2, but they are relevant historical restatements of P1 facts. With `04` now lossless, `05` is exactly where those near-duplicates should be compressed to one rendered fact.

If DeepSeek instead wants a semantic-restatement discard reason in `03`, that is a separate contract change and should be proposed explicitly; P002 does not need it.

## 3. Doximity acceptance and STATUS need two states, not a stale repo

The proposal correctly says that local/agent execution is an engineering mock and Doximity is canonical runtime acceptance.

However, §10 says to request the Doximity run before the status update. That can leave `STATUS.md` factually stale after implementation has already changed the repository.

After implementation + mock validation + architectural diff review, `STATUS.md` should be allowed to say something like:

```text
P002 implementation: engineering/mock validated
Doximity acceptance: PENDING
Canonical production acceptance: NOT YET ESTABLISHED
```

Then the user's raw Doximity run advances it to PASS or FAIL.

The rule should be:

> Mock validation may establish engineering coherence, never Doximity acceptance. STATUS records both states explicitly.

This preserves GitHub as the source of truth without conflating local validation with production behavior.

## Approved parts of P002 v2

The following are approved:

- D-011 ratification of the three inherited pre-governance edits;
- the narrow MANAGEMENT -> CLAIM_QUALIFIER validator exception for diagnostic adjudication;
- append-only A/P oracle versioning;
- `04` becoming fully lossless;
- no duplicate reasoning / no lost distinct reasoning as the acceptance criterion;
- O38 and MRI-adjudication logic remaining distinct;
- current-plan semantic selection instead of longest-string selection;
- prior-record management entering today's plan only through explicit current re-adoption;
- capitalization after `//`;
- real `04 -> 05` testing rather than calling the legacy Handoff fixture end-to-end;
- explicit separation of engineering mocks from Doximity runtime testing.

## About the `05` compression burden

Approved as a deliberate trade.

Moving seizure/sodium/CT near-duplicates into `05` increases the writer's compression burden, but that is preferable to semantic deletion in `04`. Under-compression is visible and testable; silent upstream loss is not.

Do not add more `05` rules pre-emptively. Implement the minimal rules in P002, mock-test them, then use the first canonical Doximity run to determine whether further compression guidance is actually needed.

## Required P002 v3 changes before implementation

1. Correct the validator/input path so `allocate.py` output and `check_ledger.py` have one real shared format, and fix the argument order.
2. Route O53/O54 to P1 evidence rather than falsely treating them as exact duplicates/irrelevant; leave their near-duplicate compression to `05`.
3. Define explicit STATUS states for engineering/mock validation versus canonical Doximity acceptance.

Everything else in P002 v2 is architecturally approved.

**Status:** revise narrowly to P002 v3; no implementation yet.
