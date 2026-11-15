# P002 v2 architectural review — ChatGPT

**Proposal:** `proposals/P002-ap-corrections.md` at `3654a08`  
**Verdict:** REVISE — narrow corrections only

P002 v2 resolves the major architectural objections from the first review. In particular, moving all semantic compression out of `04` is approved. A fidelity assembly stage should fail by over-retention, not by silently deleting meaning.

## Required changes

1. Repair the validation path so `allocate.py` and `check_ledger.py` share one canonical format. The actual path should be:
   `substrate -> allocate.py -> allocation.txt -> check_ledger.py allocation.txt ap_ledger_v3.txt -> 04 -> 05`.
2. Route O53/O54 to `P1.EVIDENCE`, not discard. They are semantic restatements rather than exact duplicates under the current closed discard semantics; `05` should compress them.
3. STATUS must separately record engineering/mock validation and canonical Doximity acceptance.

## Approved

- D-011 ratification of inherited pre-governance edits.
- Narrow MANAGEMENT -> CLAIM_QUALIFIER adjudication-role exception.
- Append-only A/P oracle versioning.
- Fully lossless `04`.
- No duplicate reasoning / no lost distinct reasoning.
- Current-plan semantic selection.
- Prior-record management only via explicit current re-adoption.
- Capitalization after `//`.
- Real `04 -> 05` validation path.
- Explicit separation of engineering mocks from Doximity runtime acceptance.

## `05` compression burden

Approved as a deliberate trade. Do not add more compression rules before evidence of failure. Under-compression is visible and testable; silent upstream deletion is not.

**Next:** P002 v3 with the three required corrections; no implementation yet.
