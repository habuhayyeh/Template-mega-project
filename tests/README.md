# Tests

Test areas:

[v3/](v3/README.md) — targeted extraction experiments: synthetic packets, method prompts, shared requirements, reference answers, and raw results. The workspace is scaffolded; test content and runs are pending.

`acceptance/seizure_case/` — the reproducible input for the acceptance case: the section-routing payload and the A/P handoff input.

`validator-fixtures/` — inputs that must fail. A validator that passes everything proves nothing, so each fixture is a known-bad ledger with a fixed expected failure set.

## Running

```text
python tools/check_sections.py substrate/acceptance_v2.txt tests/validator-fixtures/bad_06_ledger.txt
```

Expected on `bad_06_ledger.txt`: exit 1, with failures for duplicate primary assignment (O1), ID not in the object table (O99), illegal destination (O2), illegal discard reason (O3), DEMOGRAPHIC routed away from HPI, formulation and etiology routed away from AP_ONLY, reuse of an unassigned object (O12), reuse of a discarded object (O3), duplicate reuse, and an accounting mismatch. Fifty-odd unassigned-ID failures follow from the fixture being partial.

Expected on the accepted oracle: exit 0.

```text
python tools/check_sections.py substrate/acceptance_v2.txt oracles/section_ledger_v2.txt
```
