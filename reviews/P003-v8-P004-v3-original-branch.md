# P003 v8 / P004 v3 review — original architecture branch

## P003 v8
**Verdict: ACCEPT ARCHITECTURE; correct the frozen acceptance target before implementation**

The architecture and I10 fix are accepted.

One source-fidelity inconsistency remains:

- §2 explicitly classifies O7 + O8 as a MODIFIER pair and says O8 `left MCA infarct two years ago` renders.
- §7 instead requires `known left MCA infarct, recorded 2024-02 (prior neurology)`.
- `2024-02` is the provenance date of O53/O54, not the event date in O8.
- `recorded` is also not currently an allowed transformation word.

Do not let historical provenance replace the retained COURSE fact.

For the P003 baseline, keep the source-faithful timing (e.g. `2 yrs ago` under transformation 8) and, if O53 is also rendered, its provenance may separately appear as the permitted parenthetical `(prior neurology, 2024-02)`.

Do not infer an absolute infarct date.

After this acceptance-target correction, P003 is ready for implementation approval.

---

## P004 v3
**Verdict: HOLD — representation gap currently makes the proposed production implementation non-executable without violating D-015**

The proposal correctly identifies that the frozen oracle is ahead of the representation. But that is not merely a documented caveat; it blocks implementation of the general rule on this substrate.

D-015 says:
- a chronic block requires a source-grounded management-to-problem link;
- no target may be inferred from medication identity/class/general knowledge.

Current substrate objects O11/O12/O25/O30/O31 do not encode their management target.

Therefore a compliant production `03` reading only the current frozen representation **cannot derive the chronic-infarct block that the proposed v4 oracle expects**.

An oracle may record the signer's adjudication, but the production stage cannot use that adjudication unless it is represented in its input. Otherwise the acceptance test measures whether the model guesses the signer's hidden mapping — exactly what D-015 forbids.

### Required architecture sequence

Do not implement P004 against the current substrate.

1. Implement and validate P003 first.
2. Create a separate representation proposal that exposes the management-to-problem relation (or otherwise source-faithfully carries the target) before production `03` is expected to create chronic managed blocks.
3. Only then update the frozen substrate/oracle and implement the general chronic-block rule.

Do not solve this with medication-specific heuristics or by feeding the oracle to `03`.

### Frozen-case oracle corrections

There are also two bookkeeping/source-state errors in the current P004 table:

1. **O9 current state is wrong.** In `ap_ledger_v3.txt`, O9 is already:
   `DISCARD: IRRELEVANT_TO_RETAINED_PROBLEMS`
   It is not currently `P1.EVIDENCE`.

   The signer-approved chronic block can be represented without restoring O9: O54 provides `residual mild expressive aphasia` with prior-neurology provenance. Keep O9 discarded unless a separate reason is proposed to restore the current-consult duplicate.

2. **Assignment-count statement is wrong.** P004 says `Seven assignments move`, but the table as written moves substantially more than seven before even counting P2 -> P3 renumbering. Replace the prose count with an exact generated diff after v4 is actually constructed; do not hand-state a count now.

### D-014 supersession

The logic remains accepted:
- O54 may render under the chronic infarct block;
- it remains excluded as seizure evidence;
- the new permanent decision must explicitly supersede D-014 only in that context.

### O10

O10 -> DISCARD remains accepted.

No signer escalation is needed. The blocker is architectural: production cannot derive a hidden management target that its input does not contain.
