# ChatGPT review 019 — Phase 0 freeze blockers, final four

## Verdict

**REVISE — four concrete corrections only.**

No architecture, workflow, or testing-protocol changes are requested. BUILD_LINT and ACCEPTANCE_BRIEF are otherwise acceptable.

---

# 1. AUDIT_PROTOCOL — Mode B still assumes Case IR exists

Current Mode B inputs:

> artifact; Case IR; source package; check report; fixture assertions

That is invalid for artifact-level acceptance of I1/I2/I3/I4, where Case IR may not exist yet.

Replace with a seam-general definition:

> Inputs: artifact under test; source package when required; relevant frozen upstream artifact(s) needed by the declared assertions; applicable check report; fixture assertions.

Then add:

> Case IR is included only when it exists and is relevant to the seam being audited.

This keeps the protocol artifact/seam-driven.

---

# 2. CHANGE_CONTROL — stale table language remains

Section 2 now correctly says observed outputs may vary while frozen contract/interface/acceptance properties remain unchanged.

But §5 still says for IMPLEMENTATION CHANGE:

> reviewer: confirms locality

Replace with:

> confirms contract/interface/acceptance invariance and required regression results

Also remove/fix the sentence:

> signer approves or is informed per the table below

There is no table below. The existing table is above.

Suggested:

> Signer involvement follows the table above; notification occurs before a change is used in an acceptance result.

---

# 3. FIXTURE_REGISTER — F-06 cites the wrong historical review

Current F-06 evidence cites:

`reviews/P006-operator-stress-evidence-original-branch.md` as "the P003 packaging review".

That is not the packaging evidence.

Use:

`reviews/P003-implementation-doximity-original-branch.md`

That file explicitly establishes:
- `STANDING_ITEMS.md` was absent from the original package;
- the omission was therefore a packaging defect, not a valid runtime standing-item failure.

Keep:
- `PACKAGE.md`
- `runs/2026-11-14-p003-doximity/set2/validation.txt`
- `runs/2026-11-14-p003-doximity/set3/validation.txt`

as the corrected-package / 3-of-3 + 3-of-3 evidence.

---

# 4. FIXTURE_REGISTER — make evidence paths literal and C-01 wording owner-safe

The register says:

> Evidence is a path, not a recollection.

But some evidence lists still shorten later paths:
- F-02/F-03/F-04: first full path then `set3/run2.txt`, `set3/run3.txt`;
- F-11: first full directory then abbreviated run references.

Write every path literally in full.

For C-01 assertion, current wording:

> build fails when two rules own one decision with incompatible normative fields

"Own" is inaccurate because contradictory rules may live under the same owning contract.

Use:

> build fails when two rules govern the same decision with incompatible normative fields.

Owner remains BUILD.

---

# Freeze expectation

After these four corrections, I see no remaining Phase 0 conceptual blocker.

Please apply only these items, then return the five files unchanged otherwise. On the next sync I will perform a narrow verification and, if they are present, mark Phase 0 **ACCEPTED / FROZEN**.
