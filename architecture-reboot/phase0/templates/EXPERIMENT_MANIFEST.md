# EXPERIMENT_MANIFEST — template

One experiment binds many packets. Shared experimental condition lives here; per-run evidence lives in the packets.

A packet may repeat a shared field only as a checked snapshot with a hash. A packet that invents its own shared condition is invalid.

---

```yaml
experiment: EXP-03
control_plane: 2
hypothesis: "structure is stable across three same-condition runs"
design: REPETITION            # REPETITION | AB | ORDER | CORPUS

shared:
  model: doximity-ask
  mode: PRODUCTION
  package_version: pkg-7
  brief_version: B-04-v1
  assertion_set: AS-CASE02-v1
  baseline: BASE-02-v1
  cases: [CASE-02, CASE-05]
  repetitions: 3

arms:                         # for AB / ORDER designs
  - arm: A
    condition: current contract
  - arm: B
    condition: candidate contract

packets:
  - PKT-…-run1
  - PKT-…-run2
  - PKT-…-run3

gates:
  - PRD-070  PROCESS_GATE  "structure identical across runs"

result: pending
```

---

## Rules

1. Shared fields are declared once, here. Packets reference `EXP-` and an arm.
2. An experiment-level gate is decided by the manifest, never by a single packet.
3. Three repetitions establish variation, not a rate. The manifest states what its repetition count can and cannot support.
4. A negative control is required: one seeded defect the scorer must localise.
5. `result` is `pending`, `passed`, `failed`, or `inconclusive`. It is not a verdict on any single case.
