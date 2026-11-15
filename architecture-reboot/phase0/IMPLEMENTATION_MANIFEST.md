# IMPLEMENTATION_MANIFEST — artifacts, readiness, control state

Canonical for: **what exists, at what version, depending on what, and in what state.**

The manifest is current state. It is not acceptance evidence — evidence lives in packets, and the manifest points at them.

---

## 1. Readiness

| state | means |
|---|---|
| `DESIGNED` | specified, nothing written |
| `AUTHORED` | written, not tested |
| `UNIT_VERIFIED` | passed its own unit assertions |
| `INTEGRATED` | passed seam assertions with its neighbours |
| `LOCAL_ACCEPTED` | passed a case packet in isolation |
| `SYSTEM_ACCEPTED` | passed an experiment packet including repetition gates |

`LOCAL_ACCEPTED` is not `SYSTEM_ACCEPTED`. A module that passes one case has shown it works once, in that configuration; it has not shown it works with the others or repeats.

**`SYSTEM_ACCEPTED` requires an `EXP-` reference.** It cannot be set from a single packet. Acceptance above the local level is decided by the experiment, not by a run.

---

## 2. Entry

```yaml
artifact: STRUCTURE
version: 2
readiness: AUTHORED
depends_on:
  - edge: requires        target: DEC-OPERATOR_SELECTION
  - edge: consumes        target: CON-OPERATOR_REGISTRY
  - edge: provides        target: CASE_IR_SCHEMA
  - edge: invalidates     target: RENDER
acceptance_state:
  packets: []
  experiment: null
```

Typed edges exist so invalidation is computable. An `invalidates` edge means: changing this artifact invalidates previous acceptance of the target.

| edge | meaning |
|---|---|
| `requires` | cannot function without |
| `consumes` | reads its output |
| `provides` | is the source of |
| `invalidates` | a change here voids that artifact's acceptance |

---

## 3. Control state

Canonical home of the SPEC / M0 / ACTIVE distinction. `README.md` displays a derived copy; a mismatch is a manifest error.

```yaml
control: CTL-BUILD_SPEC
state: SPEC            # SPEC | M0 | ACTIVE
enforced_by: null      # the instrument, when ACTIVE
m0_checklist: BUILD_SPEC §7
```

| control | state | enforced by |
|---|---|---|
| `CTL-AUTHORITY_REGISTRY` | M0 | reviewer check per change |
| `CTL-IMPLEMENTATION_MANIFEST` | M0 | reviewer check per change |
| `CTL-ACCEPTANCE_MODEL` | SPEC | — |
| `CTL-FIXTURE_INDEX` | SPEC | — |
| `CTL-COVERAGE_LEDGER` | M0 | review at each phase gate |
| `CTL-BUILD_SPEC` | SPEC | M0 checklist |
| `CTL-AUDIT_PROTOCOL` | SPEC | — |
| `CTL-CHANGE_CONTROL` | M0 | reviewer at each change |
| `CTL-CHANGE_LEDGER` | M0 | reviewer at each change |

A control may not be cited as a guarantee above its state. That rule is the reason this section exists.

---

## 4. Control-plane version

The manifest carries a `control_plane_version`. Every packet snapshots it. A verdict without a control-plane version is unscorable, because the rules that judged it may have changed.

```yaml
control_plane_version: 2
```

---

## 5. Current state

All artifacts `DESIGNED`. No packets, no experiments, no acceptance. The control plane is `version 2` — the first version after the review stack, and the first with registries rather than a single file.

---

## 6. Rules

1. Readiness only moves forward, and only with evidence.
2. A change to an artifact updates `depends_on` invalidation before the change is merged.
3. An artifact may not cite a contract version the registry does not hold.
