# Gate 0 — seed corpus (source spec)

**Identities:** registry `PILOT-2` · active set `ACTIVE-PILOT-2` · schema `SCHEMA-2` · campaign `GATE0-C1`.

Seeds are generated from four layer-specific parents by `architecture-reboot/tools/make_seeds.py`. Each seed mutates **one field of its own layer's parent**;
specificity (full silence) is therefore evaluated within a layer, never across a four-layer artifact.

The authoritative inventory is `seeds/generated/MANIFEST.json`. This table is a human view of it.

| predicate | seeds |
|---|---|
| `S1-AUTH-01` | `G0-S1-01`, `G0-S1-06` |
| `S1-AUTH-02` | `G0-S1-02` |
| `S1-CAND-01` | `G0-S1-05` |
| `S1-CAND-02` | `G0-S1-04` |
| `S2-ADOPT-01` | `G0-S2-06` |
| `S2-REP-01` | `G0-S2-01` |
| `S2-TEMP-01` | `G0-S2-03` |
| `S3-ACCT-01` | `G0-S3-04` |
| `S3-CAND-01` | `G0-S3-05`, `G0-S3-06`, `G0-S3-07`, `G0-S3-08`, `G0-S3-09`, `G0-S3-10` |
| `S3-INC-01` | `G0-S3-01` |
| `S3-SEL-01` | `G0-S3-02` |
| `S4-COMP-01` | `G0-S4-06` |
| `S4-INC-01` | `G0-S4-01`, `G0-S4-02` |
| `S4-MEM-01` | `G0-S4-04` |
| `S4-PROJ-01` | `G0-S4-07`, `G0-S4-08`, `G0-S4-09`, `G0-S4-10`, `G0-S4-11` |
| `S4-REP-01` | `G0-S4-05` |

**Counts:** 4 clean parents · 27 seeds · 16 active predicates.

Branch coverage — `S3-CAND-01` has coverage, exclusivity, unknown-id, rendered-set equality, missing
reason and missing basis. `S4-PROJ-01` has schema (injected field), invented member, wrong value,
fabricated payload and wrong-owner relation.

Pending: `S2-ADOPT-02` (schema), `S4-ORD-01` (ordering oracle). Not produced by any pilot case:
`S1-BODY-01`, `S2-REP-02`, `S2-CONF-01`.

A harmless variation and a clean parent per layer are produced by the generator; nothing here is
hand-edited.
