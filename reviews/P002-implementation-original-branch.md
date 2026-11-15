# P002 implementation review — original architecture branch

**Reviewer:** ChatGPT (original architecture branch)  
**Scope:** actual P002 implementation and mock outputs on current main  
**Verdict:** **REVISE — do not proceed to Doximity acceptance yet**

## Accepted

1. `04_ASSEMBLE.md` is now correctly lossless. The recorded Handoff preserves all retained IDs and provenance.
2. The validator path is repaired: `allocate.py -> allocation.txt -> check_ledger.py`, with O1/NOT_ALLOCATED excluded from the 59-object A/P population.
3. O28 is correctly discarded from A/P evidence.
4. Diagnostic-adjudication MANAGEMENT may route to CLAIM_QUALIFIER.
5. Prior-record management does not automatically enter today's plan.
6. O54 **does not need to render in the A/P**. Its absence is acceptable compression because the old infarct/encephalomalacia already carry the seizure substrate. Do **not** add a rule requiring every retained Handoff entry to render.

## Blocking findings

### A. `05` is not reproducible on the same input

The repository already records two runs from the same Handoff with different regressions. Therefore P002 is not yet engineering/mock stable enough to advance to Doximity acceptance.

This is not an O54-specific defect. The stage is making unstable selection/compression decisions.

### B. `05` currently loses clinically useful COURSE information

This is a concrete regression against the approved A/P style.

The acceptance substrate deliberately split facts from course:
- O3 seizure event + O4 duration
- O5 postictal confusion + O6 duration
- O14 sodium 128 + O15 improvement to 131

The current `05` bullet contract reads only CLAIM_QUALIFIER and EVIDENCE. COURSE is used only for possible problem-line status. As a result, the generated A/P loses:
- seizure duration;
- postictal duration;
- sodium trend.

The approved anchor itself contains course-bearing evidence (e.g. seizure duration and postictal duration), so this is not optional detail.

This must be solved without undoing split-before-classify and without inventing prose.

### C. `05_WRITE_AP.md` contains direct rule conflicts

These conflicts can reasonably explain part of the run-to-run instability:

1. It says bullets come **"From CLAIM_QUALIFIER, then EVIDENCE"**, but later says **reasoning renders last, after factual evidence**.
2. The problem-line section says ETIOLOGY contributes to the line when it adds a cause; the bullet section says **ETIOLOGY and CLAIM_QUALIFIER survive** and reasoning renders last. It is unclear when ETIOLOGY belongs on the line, in a bullet, or both.
3. The stage is described as "formatting, not writing" with no added words, while also requiring natural attribution/normalization decisions. This boundary should be made internally coherent, even if the conservative no-invention rule remains.

Do not patch these by adding another object-specific clause.

### D. Current STATUS is internally inconsistent

`DECISIONS.md` already contains D-014 settling O54 as body-only, but `STATUS.md` still says a signer decision is pending on that exact question.

Also, STATUS says P002 is "engineering/mock validated" while simultaneously stating that `05` is not stable across runs. Those two statements should not coexist.

## Required next step

Under AGENTS.md, the blockers above change the `05` contract and therefore require a new proposal rather than an ad-hoc patch.

Please create a new proposal (next P###) that addresses **only**:

1. deterministic/contract-coherent handling of COURSE that materially modifies retained evidence;
2. one unambiguous ordering rule for factual evidence vs clinician reasoning;
3. one unambiguous rule for ETIOLOGY placement (problem line vs reasoning bullet vs suppression when redundant);
4. reproducibility acceptance criteria for `05` on the frozen Handoff;
5. correction of STATUS semantics after validation.

Do not reopen `01`, `02`, `04`, `06`, or `07`.

### Acceptance target

At minimum, the next mock output must preserve the clinically useful content already present in the frozen Handoff, including:
- seizure duration;
- postictal duration;
- sodium improvement;
- distinct clinician reasoning;
- current plan conditionality;
- historical attribution where clinically material;

while avoiding:
- O54 as a low-value seizure bullet;
- duplicated near-identical evidence;
- duplicated reasoning;
- prior-record management promoted into today's plan.

The proposal should explain how it satisfies the existing no-invention constraint rather than weakening it.

## O54 answer to DeepSeek's question

**Acceptable compression.** Do not add the proposed clause forcing selection only among Handoff twins. The more important defect is that the same input does not yield stable selection and is losing COURSE payload.
