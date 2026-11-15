# Gate 0 semantic packet index — GATE0-C2 / SCHEMA-3

**BLOCKED:** semantic packets leak expected answers; do not collect evidence from this run.
See `PACKET_BLINDING_BLOCKED.md` and proposal 014.

**Mode:** packets only · **acceptance:** not run
**Run:** `20261115T160349Z-2d6284b7`
**Policy:** `REVIEW-POLICY-F-1`
**Semantic packets:** 16 · **records:** 33 · **references:** 0 · **evaluators:** 0

This index was produced by `gate0_harness.py --mode packets` after the D-023 / SCHEMA-3 rebuild.
No signer reference or evaluator judgment exists; every semantic packet is `UNDECIDABLE` until
real evidence is supplied.

| artifact | kind | parent | predicate | packet | expected reference |
|---|---|---|---|---|---|
| `PARENT-S1_PARENT.json` | clean | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-6b9b268bb32bce703f0e3926` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-ee3539a55fb7ebb415f1606c` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-228ca942cb5c1bfd995b4ee7` | SILENT |
| `G0-S1-01.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-1f944ac2b3d79d1b182cb92e` | SILENT |
| `G0-S1-02.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-bcdabc8aac3e7f9a19eff713` | SILENT |
| `G0-S1-04.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-20dde3bf4ff348c80002dc2b` | SILENT |
| `G0-S1-05.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-48eae69089c80e9c52cbd72d` | FIRED |
| `G0-S1-06.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-0746d6c306171bafdc73694f` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-3c5d39014637d286b3afed86` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-d871e4c6d7e1ca897c133c39` | FIRED |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-7ef4ae977f6b9f0bef90dee6` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-3c46bb83894cdbc5c06cacba` | FIRED |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-cf75782ba71b30d4a518d5e0` | SILENT |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-cf60d20bbc04e461e5555326` | SILENT |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-b09b26c7ff4d52e275cdb321` | FIRED |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-0e4b09cad044a2f67889b0de` | SILENT |

## Workload

- **16 semantic packet instances:** 6 S1 (clean + 5 seeds) and 10 S2 (clean + 4 seeds).
- The seeded predicate packet expects `FIRED`; every other semantic packet on the same artifact
  expects `SILENT` for specificity.
- Each packet needs one signer/clinician reference and two eligible packet-only LLM evaluator
  judgments. The reference is reusable while the packet/policy/oracle/context identity is unchanged.
- Mechanical S3/S4 artifacts create no semantic packets.
- Pre-D-023 signer references from `gate0-packets-c1` are invalid and must not be reused.

## Status

All semantic packets are `UNDECIDABLE` because no reference/evaluator evidence is supplied. The
mechanical records are packet-mode evidence only; this is not a Gate 0 acceptance result.
