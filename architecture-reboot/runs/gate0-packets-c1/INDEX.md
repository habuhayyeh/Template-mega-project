# Gate 0 semantic packet index — GATE0-C1

**Mode:** packets only · **acceptance:** not run
**Run:** `20261115T113041Z-b8bcbce9`
**Policy:** `REVIEW-POLICY-F-1`
**Semantic packets:** 16 · **records:** 33 · **references:** 0 · **evaluators:** 0

This index was produced by `gate0_harness.py --mode packets`. No signer reference or evaluator
judgment exists; every semantic packet is `UNDECIDABLE` until real evidence is supplied.

| artifact | kind | parent | predicate | packet | expected reference |
|---|---|---|---|---|---|
| `PARENT-S1_PARENT.json` | clean | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-16ced7dee2e14aec98b74e97` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-876bdd66fa7db9f55b3b388b` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-6e8fc6ddcd12ae7f2f7eb917` | SILENT |
| `G0-S1-01.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-9ccb3e56876196e560fb2d48` | SILENT |
| `G0-S1-02.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-e7dbed42337dc547369d4057` | SILENT |
| `G0-S1-04.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-995d0079ed67a340d3fe26a9` | SILENT |
| `G0-S1-05.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-c7ff8beb7be31a3c477b782b` | FIRED |
| `G0-S1-06.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-2ce5dbd0a6aa1898354b8b82` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-e503c5ad04f05e6145605ae5` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-a80d28edaad348d933f7709d` | FIRED |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-b55c0a355406bee7b8e660a7` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-a3a9ad7506d9ea1c7605c899` | FIRED |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-36c35eb264b6140753c7d5a0` | SILENT |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-054b2f788f871e0e635153fa` | SILENT |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-cc7b359b2179e787734bdbaa` | FIRED |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-02282d97e541275e53f0202f` | SILENT |

## Workload

- **16 semantic packet instances:** 6 S1 (clean + 5 seeds) and 10 S2 (clean + 4 seeds).
- The seeded predicate packet expects `FIRED`; every other semantic packet on the same artifact
  expects `SILENT` for specificity.
- Each packet needs one signer/clinician reference and two eligible packet-only LLM evaluator
  judgments. The reference is reusable while the packet/policy/oracle/context identity is unchanged.
- Mechanical S3/S4 artifacts create no semantic packets.

## Status

All semantic packets are `UNDECIDABLE` because no reference/evaluator evidence is supplied. The
mechanical records are packet-mode evidence only; this is not a Gate 0 acceptance result.
