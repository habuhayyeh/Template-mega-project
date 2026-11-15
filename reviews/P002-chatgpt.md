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
