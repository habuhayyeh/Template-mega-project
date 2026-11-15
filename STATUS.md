# STATUS

Current state only. Regenerated, never appended. Under twenty lines.

```text
Stage           07 accepted for the acceptance case; P003 implemented, Doximity FAILED
Substrate       substrate/acceptance_v2.txt                (60 objects, six kinds)
A/P oracle      oracles/ap_ledger_v4.txt                   (O54 excluded; 59 assignments, PASS)
Section oracle  oracles/section_ledger_v2.txt
Production 06   UNRESOLVED — contract and oracle accepted, Doximity execution not reliable

P003 implementation:   complete — 05 rewritten, anchor cause rule updated
Doximity acceptance:   FAILED — two dispatcher-qualified runs, four errors, no two alike
Canonical acceptance:  NOT YET ESTABLISHED

Next            P005 checker; then three runs from the complete package in PACKAGE.md
```

Open:

- The Doximity set was not a reproducibility set: one run had no dispatcher, and `STANDING_ITEMS.md` was never in the package. Both corrected in `PACKAGE.md`.
- `postictal confusion resolved` came from the no-dispatcher control. Evidence that an under-specified call invents a status, not that the dispatcher-qualified contract does.
- `05` cannot see `DECISIONS.md`; exclusions must be represented by absence in the input. `ap_ledger_v4.txt` now excludes O54.
- `P004` (chronic blocks) stays held until a representation proposal exposes the management-to-problem link.
