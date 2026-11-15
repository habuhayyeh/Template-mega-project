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
- `scorer.py` — mechanical predicates; semantic predicates are `UNDECIDABLE` until Option F reference/evaluator evidence.
- `projection.py` — scorer adapter for the shared projection contract.
- `../projection_contract.py` — the single executable `PROJECTION_MAP` implementation, used by both the
  generator and the scorer.
- `../tools/gate0_harness.py` — packets, judgments, specificity, parent-type/campaign verdicts,
  implementation fingerprints and evidence.
- `../tests/test_scorer.py`, `../tests/test_scorer_more.py` — synthetic tests; no campaign acceptance run.

## Semantic review — Option F

The harness writes one packet per semantic predicate. A packet contains only the target artifact,
minimum dependency context, oracle source material (objects, spans, matching rule), the predicate rule,
and the judgment schema. It never contains `oracle.expected`, semantic answer labels, the seed id,
expected predicate, mutation or answer key. The current policy is `REVIEW-POLICY-F-2`.

The signer/clinician records one `HUMAN / REFERENCE` verdict first. Two blinded `LLM / EVALUATOR`
judgments then score the same packet independently, in packet-only sessions, from different model
families where available. The signer reference is the accepted verdict; the evaluators are calibrated
against it.

Records carry `packet_id`, `predicate_id`, `judge_id`, `role`, `judge_type`, `policy_version`,
`verdict` and `rationale`. The reference also declares `authority: SIGNER_CLINICIAN`. Evaluators
carry `model_family`, `model_version`, `session_id`, `context_scope: PACKET_ONLY` and
`project_context_agent: false`; the two accepted evaluators require distinct model families and
distinct session ids. Unknown packets, predicate mismatches, project-context agents and ineligible
metadata are rejected.

A clean packet reference must be `SILENT`; the seeded predicate packet reference must be `FIRED`; other semantic packets on that artifact must be `SILENT`. Both evaluators
must match the reference. A determinate mismatch is a **calibration failure**; missing, duplicate or
genuinely `UNDECIDABLE` evidence is `INCOMPLETE`. `UNDECIDABLE` never becomes a pass.

References are reusable while the packet, predicate/contract version, oracle/context hashes and policy
version are unchanged. Evaluator evidence is reusable only for the same packet, policy, judge and model
family/version. A changed packet invalidates the reference; a changed evaluator version invalidates only
that evaluator's cache. Each acceptance run writes the merged `references[]` and `evaluators[]`
into `EVIDENCE.json`, so that file can be used directly as a later `--baseline`.

## Verdicts

Clean parents are `FAIL` on any `FIRED` **or calibration failure**, `INCOMPLETE` on unresolved
`UNDECIDABLE`, otherwise `PASS`. Parent types aggregate their clean and seed records: any `FAIL` ->
`FAIL`; otherwise any `INCOMPLETE` -> `INCOMPLETE`; all `PASS` -> `PASS`. The campaign aggregates the
four required parent types the same way. Both objects are written to `EVIDENCE.json`.

## Run

```text
python architecture-reboot/tools/preflight.py
python architecture-reboot/tools/gate0_harness.py --mode packets --out <dir>
python architecture-reboot/tools/gate0_harness.py --mode acceptance --out <dir> --judgments <file>
```

Preflight is the single mechanical entry point for frozen-zone, freshness, hash, registry, dependency,
seed-integrity, stale-marker and unit-test checks. The `acceptance` mode is not run by the build, tests,
or this source pass. Building the scorer is not Gate 0 execution.
