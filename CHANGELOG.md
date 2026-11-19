# CHANGELOG

One entry per accepted proposal. Three lines. History lives in git and in `proposals/`; this file only marks time.

## 2026-11-14 — import/v2

Imported the canonical Doximity note project: `pipeline/` 00–07 with `AP_ANCHOR`, `SECTION_CONTRACT`, `STANDING_ITEMS`; substrate v2; both accepted oracles; tools and fixtures; the diagnostic runs and the assembled note.

Includes three contract edits made immediately before governance existed — `03` evidence eligibility and reasoning protection, `04` reasoning exemption from dedup, `05` reasoning rendering. They are recorded in `pipeline/` and are the baseline P002 corrects further.

Superseded material (`step4`–`step6`, v1 substrate, stale README) is not on `main`.

## 2026-11-14 — P002 implementation

`04` is lossless: it dereferences and appends provenance, deletes nothing. `05` gained capitalisation, one-fact-one-bullet, a reasoning criterion (no duplicates, no losses), current-plan selection, and the prior-record plan exclusion. `allocate.py` and `check_ledger.py` repaired and put back in sync with the substrate.

New append-only `oracles/ap_ledger_v3.txt`, validated at 59 assignments. Mock run recorded in `runs/2026-11-14-p002/`: allocate → check_ledger → 04 → 05. One open defect (O54 over-compression) held for review. Doximity acceptance not attempted.

## 2026-11-14 - P002 review round 2

Review accepted the O54 outcome and both must-changes. The ETIOLOGY bullet and the sentence-initial conjunction are gone in the second run; so, wrongly, are the merged apixaban item, the seizure standing item, and the infarct evidence. Two runs, two different regressions: 05 is not stable yet. D-014 records the O54 decision. Reviewed artifact at runs/2026-11-14-p002/ap_reviewed.txt.

## 2026-11-14 — Doximity limitations recorded

`DOXIMITY.md` added: what the runtime is, the five observed limitations with their evidence paths, and the design consequences. No pipeline change. Written because both agents work locally and neither can run the runtime that decides acceptance.

## 2026-11-19 — D-018 V3 targeted testing plan

User-approved controlled comparison of source-first, meaning-first, and assessment-guided extraction recorded in `reviews/V3_TARGETED_TESTING_PLAN.md`.
Branch navigation and status updated; existing runtime contracts and acceptance artifacts unchanged. No new Doximity runs or method-selection results.
