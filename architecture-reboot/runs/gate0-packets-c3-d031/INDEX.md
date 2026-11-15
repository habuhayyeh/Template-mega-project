# Gate 0 semantic packet index — GATE0-C3 / SCHEMA-4 / D-031 / REVIEW-POLICY-F-2

**Mode:** packets only · **acceptance:** not run
**Run:** `20261115T193906Z-2a9c3508`
**Policy:** `REVIEW-POLICY-F-2`
**Semantic packets:** 44 · **records:** 42 · **references:** 0 · **evaluators:** 0

This run removes all `oracle.expected` labels from semantic packets. Judges receive source
objects/spans, target artifact, dependency context and predicate rule only.

| artifact | kind | parent | predicate | packet | expected reference |
|---|---|---|---|---|---|
| `PARENT-S1_PARENT.json` | clean | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-e61b1ead1920a55305beaa6c` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-a2dcf40e81302478a9d2925e` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-CAUSAL-01` | `pkt-1df7181920569739d9e4a6fb` | SILENT |
| `PARENT-S2_PARENT.json` | clean | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-d474bb130eacbf48f5ba45f4` | SILENT |
| `PARENT-S2_CASE10_CAUSAL.json` | clean | `S2_CASE10_CAUSAL` | `S2-ADOPT-01` | `pkt-2578f4a72e27caccf1e82d7a` | SILENT |
| `PARENT-S2_CASE10_CAUSAL.json` | clean | `S2_CASE10_CAUSAL` | `S2-CAUSAL-01` | `pkt-a9f7b83a4153cad92c56913d` | SILENT |
| `PARENT-S2_CASE10_CAUSAL.json` | clean | `S2_CASE10_CAUSAL` | `S2-REP-01` | `pkt-cb6cd7a8943d07cee9fdd979` | SILENT |
| `PARENT-S3_PARENT_NOT_RENDERED.json` | clean | `S3_CASE01_NOT_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-c2d599edac147564d9336589` | SILENT |
| `PARENT-S3_PARENT.json` | clean | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-6dae7cba2d6a1243a2d10f7d` | SILENT |
| `G0-S1-01.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-d38a0b056db32b7e7384a5ce` | SILENT |
| `G0-S1-02.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-244512aabc47f650636b0746` | SILENT |
| `G0-S1-04.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-4983f345d0d01b8a0ee95a39` | SILENT |
| `G0-S1-05.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-39b3a055c23a59f53be1a459` | FIRED |
| `G0-S1-06.json` | seed | `S1_CASE01_CLEAN` | `S1-CAND-01` | `pkt-63a66d986a06536d85f2edfd` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-90d1e7b7ab71ba07934ea75d` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-CAUSAL-01` | `pkt-499ef29e044d07368e3062b4` | SILENT |
| `G0-S2-02.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-44120c49b375bc1a66f6b63c` | FIRED |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-3cd127947ff9d2656295368e` | SILENT |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-CAUSAL-01` | `pkt-28c34b3fa981df66c9223ac2` | SILENT |
| `G0-S2-03.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-7095a6085459cd0c46915721` | SILENT |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-154e85054d5744a08f4c6770` | FIRED |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-CAUSAL-01` | `pkt-0d4d6b552e4a4a8bcf91dece` | SILENT |
| `G0-S2-06.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-67198a82d18dcd4cb887050b` | SILENT |
| `G0-S2-07.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-2e9932412b961f11a8dcf804` | SILENT |
| `G0-S2-07.json` | seed | `S2_CASE01_CLEAN` | `S2-CAUSAL-01` | `pkt-0b54e5ed007bbe894259eb54` | FIRED |
| `G0-S2-07.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-3595781258eac2b8661405da` | SILENT |
| `G0-S2-08.json` | seed | `S2_CASE01_CLEAN` | `S2-ADOPT-01` | `pkt-610460f4d65e8d3a51df7c43` | SILENT |
| `G0-S2-08.json` | seed | `S2_CASE01_CLEAN` | `S2-REP-01` | `pkt-6d86dcbd164dc132f44834e7` | SILENT |
| `G0-S2-09.json` | seed | `S2_CASE10_CAUSAL` | `S2-ADOPT-01` | `pkt-937aaee9c55e1d3a6635c95d` | SILENT |
| `G0-S2-09.json` | seed | `S2_CASE10_CAUSAL` | `S2-CAUSAL-01` | `pkt-b1248da45d1fabbf07f5615e` | FIRED |
| `G0-S2-09.json` | seed | `S2_CASE10_CAUSAL` | `S2-REP-01` | `pkt-b3dbc6f399b3785dd77881c0` | SILENT |
| `G0-S2-10.json` | seed | `S2_CASE10_CAUSAL` | `S2-ADOPT-01` | `pkt-c86be4c0a4d6ff5905f808ea` | SILENT |
| `G0-S2-10.json` | seed | `S2_CASE10_CAUSAL` | `S2-CAUSAL-01` | `pkt-cc45dadfb57344e3e970f32a` | FIRED |
| `G0-S2-10.json` | seed | `S2_CASE10_CAUSAL` | `S2-REP-01` | `pkt-c6ef29c7e658818919ae9328` | SILENT |
| `G0-S3-01.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-2ca7cb635a55fb2b903be138` | SILENT |
| `G0-S3-02.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-f78762b079d5c552a3ea898a` | SILENT |
| `G0-S3-04.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-28c1ec2556889b1c6d7fca47` | SILENT |
| `G0-S3-05.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-85ed041f9228be9e29423fc2` | SILENT |
| `G0-S3-06.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-8e38d2767da942329d25a0ff` | SILENT |
| `G0-S3-07.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-4b78fe190d1f52917282a1af` | SILENT |
| `G0-S3-08.json` | seed | `S3_CASE01_NOT_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-19386b6105a33e5894bf7c3c` | SILENT |
| `G0-S3-09.json` | seed | `S3_CASE01_NOT_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-d5e988b224fcd193779c1a63` | SILENT |
| `G0-S3-10.json` | seed | `S3_CASE01_NOT_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-baab43538d1f545135f9961e` | SILENT |
| `G0-S3-11.json` | seed | `S3_CASE01_RENDERED_CLEAN` | `S3-ROLE-01` | `pkt-267cb08264469475462cafb7` | FIRED |

## Workload

- **44 semantic packet instances:** 6 S1, 26 S2 (CASE-01 and CASE-10) and 12 S3 role packets. G0-S2-08 and G0-S3-12 are structural-only seeds with no semantic packet.
- The seeded predicate packet expects `FIRED`; every other semantic packet on the same artifact
  expects `SILENT` for specificity.
- Each packet needs one signer/clinician reference and two eligible packet-only LLM evaluator
  judgments. The reference is reusable while the packet/policy/oracle/context identity is unchanged.
- S4 creates no semantic packet; the S3-ROLE packet is the new D-031 semantic axis.
- Pre-D-031 packets/references are invalid and must not be reused.

## Status

All semantic packets are `UNDECIDABLE` because no reference/evaluator evidence is supplied. The
mechanical records are packet-mode evidence only; this is not a Gate 0 acceptance result.
