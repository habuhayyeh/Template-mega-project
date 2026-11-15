# STATUS

Current state only. Regenerated, never appended. Under twenty lines.

```text
Stage           07 accepted for the acceptance case; P003 implemented, mock FAILED
Substrate       substrate/acceptance_v2.txt                (60 objects, six kinds)
A/P oracle      oracles/ap_ledger_v3.txt                   (59 assignments, PASS)
Section oracle  oracles/section_ledger_v2.txt
Production 06   UNRESOLVED — contract and oracle accepted, Doximity execution not reliable

P003 implementation:   complete — 05 rewritten, anchor cause rule updated
05 mock acceptance:    FAILED — I2/I3/I4/I7/I10 differ across three runs on one Handoff
Doximity acceptance:   PENDING
Canonical acceptance:  NOT YET ESTABLISHED

Next            fix the three causes named in runs/2026-11-14-p003/validation.txt
```

Open:

- `05` renders different facts on identical input: `admitted 11/12`, `encephalomalacia`, `no new focal lesion`, and the CT entry drift between runs.
- Run 1 rendered O54, which `D-014` excludes. Nothing in `05` enforces a decided exclusion.
- `Seizure precautions` — a triggered `STANDING_ITEMS` entry — is missing from all three runs.
- `P004` is held until a representation proposal exposes the management-to-problem link.
