# Gate 0 scorer and harness

## Input boundary

The scorer receives four inputs:

1. target artifact;
2. read-only dependency context (upstream layer outputs required by the frozen dependency graph);
3. case oracle;
4. frozen predicate/contract rules (`REASON-1`, `PROJECTION_MAP`).

It never reads the seed manifest, seed id, expected predicate, mutation metadata or specificity answer
key. `scorer/scorer.py` does not open files; `tests/test_scorer.py` patches `builtins.open` to prove it.

The harness owns the answer key. It selects the artifact, builds the dependency context, calls the
scorer, and compares the result with the manifest. Before packets or acceptance it recomputes every
governing-source hash, verifies the frozen campaign identities, and checks the scorer registry against
the accepted active set. A stale manifest is an `InputIntegrityError`.

## Dependency context

| target | context |
|---|---|
| `S1_OUTPUT` | none |
| `S2_OUTPUT` | clean S1 |
| `S3_OUTPUT` | clean S1 + clean S2 |
| `S4_BLUEPRINT` | clean S1 + clean S2 + clean rendered S3 |

Context is unmutated, hash-pinned in `MANIFEST.json` and identical for the clean parent and every seed in
the lineage. The harness raises `InputIntegrityError` on a mismatch. Each evidence record stores the
exact dependency `parent_id`, `parent_type` and hash supplied to the scorer.

## Files

- `registry.py` — frozen predicate ids, owners, parent types and modes.
- `scorer.py` — mechanical predicates; semantic predicates are `UNDECIDABLE` until human judgment.
- `projection.py` — scorer adapter for the shared projection contract.
- `../projection_contract.py` — the single executable `PROJECTION_MAP` implementation, used by both the
  generator and the scorer.
- `../tools/gate0_harness.py` — packets, judgments, specificity, parent-type/campaign verdicts,
  implementation fingerprints and evidence.
- `../tests/test_scorer.py`, `../tests/test_scorer_more.py` — synthetic tests; no campaign acceptance run.

## Human review

The harness writes one packet per semantic predicate. A packet contains only the target artifact,
minimum dependency context, minimum oracle material, the predicate rule, and the judgment schema. It
does not contain the seed id, expected predicate, mutation or answer key.

A judgment record carries `packet_id`, `predicate_id`, `judge_id`, `judge_type: HUMAN`, `verdict` and
`rationale`. The harness rejects unknown packet ids and a `predicate_id` that does not match the packet.
Aggregation requires exactly three unique human judges with the same verdict. Fewer, duplicate judges,
disagreement, or `UNDECIDABLE` keeps the predicate `UNDECIDABLE`; `UNDECIDABLE` never becomes a pass.

## Verdicts

Clean parents are `FAIL` on any `FIRED`, `INCOMPLETE` on `UNDECIDABLE`, otherwise `PASS`. Parent types
aggregate their clean and seed records: any `FAIL` -> `FAIL`; otherwise any `INCOMPLETE` -> `INCOMPLETE`;
all `PASS` -> `PASS`. The campaign aggregates the four required parent types the same way. Both objects
are written to `EVIDENCE.json`.

## Run

```text
python architecture-reboot/tools/preflight.py
python architecture-reboot/tools/gate0_harness.py --mode packets --out <dir>
python architecture-reboot/tools/gate0_harness.py --mode acceptance --out <dir> --judgments <file>
```

Preflight is the single mechanical entry point for frozen-zone, freshness, hash, registry, dependency,
seed-integrity, stale-marker and unit-test checks. The `acceptance` mode is not run by the build, tests,
or this source pass. Building the scorer is not Gate 0 execution.
