# Gate 0 semantic packet index — GATE0-C2 / SCHEMA-3 / REVIEW-POLICY-F-2

**Mode:** packets only · **acceptance:** not run
**Run:** `20261115T164905Z-8f53d1b5`
**Policy:** `REVIEW-POLICY-F-2`
**Semantic packets:** 16 · **records:** 33 · **references:** 0 · **evaluators:** 0

This run removes all `oracle.expected` labels from semantic packets. Judges receive source
objects/spans, target artifact, dependency context and predicate rule only.

| artifact | kind | parent | predicate | packet | expected reference |
|---|---|---|---|---|---|
| `PARENT-S1_PARENT.json` | clean | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-a52ceb9eebabadf9685fe9c2` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-73f5f57e86a8a3ebde9254d9` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-3bdf13d0843200e173bd1b2a` | SILENT |
| `G0-S1-01.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-74133d70a2a3e32d0322b08f` | SILENT |
| `G0-S1-02.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-a507b837f8290d70e6bbc4b3` | SILENT |
| `G0-S1-04.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-0fd71382f25b2ef34f952836` | SILENT |
| `G0-S1-05.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-45fa443b5af39347fb89d988` | FIRED |
| `G0-S1-06.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-06659e4359d75158839565f5` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-1a01060e7f54115c95e3bcc0` | SILENT |
| `G0-S2-01.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-2fc411754ebd8f52f7af88ab` | FIRED |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-715f749cb0332ca92a7e6580` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-7501511036bc9336ff149941` | FIRED |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-b2432ea4c38e551e6b88b2e8` | SILENT |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-24cee276f64b8a8dd96f4b20` | SILENT |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-79153a82bcfdcae9d162daa6` | FIRED |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-0d0f27b03efaf605d42b8f35` | SILENT |

## Workload

- **16 semantic packet instances:** 6 S1 (clean + 5 seeds) and 10 S2 (clean + 4 seeds).
- The seeded predicate packet expects `FIRED`; every other semantic packet on the same artifact
  expects `SILENT` for specificity.
- Each packet needs one signer/clinician reference and two eligible packet-only LLM evaluator
  judgments. The reference is reusable while the packet/policy/oracle/context identity is unchanged.
- Mechanical S3/S4 artifacts create no semantic packets.
- Pre-D-023 and F-1 packets/references are invalid and must not be reused.

## Status

All semantic packets are `UNDECIDABLE` because no reference/evaluator evidence is supplied. The
mechanical records are packet-mode evidence only; this is not a Gate 0 acceptance result.
