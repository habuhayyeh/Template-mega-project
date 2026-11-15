# Phase 0 — Control Plane

Phase 0 defines what correct means and how correctness is established. No runtime behaviour.

**Control-plane version: 2** — the first version written after the review stack, with registries rather than a single file.

---

## Authorities

| file | owns | state |
|---|---|---|
| `AUTHORITY_REGISTRY.md` | who owns each decision, under which contract, at which version | M0 |
| `IMPLEMENTATION_MANIFEST.md` | what exists, readiness, control state, dependency edges | M0 |
| `ACCEPTANCE_MODEL.md` | what a predicate is, what a packet carries, what a verdict means | SPEC |
| `FIXTURE_INDEX.md` | which cases exist, their evidence, their references | SPEC |
| `COVERAGE_LEDGER.md` | what is owed downstream, where the corpus is thin | M0 |
| `BUILD_SPEC.md` | what the build refuses | SPEC (M0 checklist §7) |
| `AUDIT_PROTOCOL.md` | how a verdict is reached | SPEC |
| `CHANGE_CONTROL.md` | how an edit is classified and approved | M0 |
| `CHANGE_LEDGER.md` | the record of governed changes | M0 |

Supporting records, not authorities: `templates/ACCEPTANCE_BRIEF.md`, `templates/EXPERIMENT_MANIFEST.md`.

---

## Lifecycle states

| state | meaning | who enforces |
|---|---|---|
| **SPEC** | written, no instrument | nobody; it is an obligation |
| **M0** | manual checklist a reviewer signs | the reviewer |
| **ACTIVE** | an instrument fails closed | the instrument |

Canonical control state lives in `IMPLEMENTATION_MANIFEST.md` §3. The table above is a derived copy; a mismatch is a manifest error.

**A control may not be cited as a guarantee above its state.** That sentence is why this section exists.

---

## The rule for claims

> Every claim names the contract that grants it, or it is marked as a design proposal.

A predicate may assert only what a frozen contract states. A question the architecture left open becomes `PENDING_DEPENDENCY`, never a hidden test oracle.

---

## Where things stand

- Nine authorities, two templates, thirteen decisions registered, twelve cases indexed, twenty-one obligations open.
- All artifacts `DESIGNED`. No packets. No experiments. No acceptance.
- The largest open gap: only one of three seams has any case at all.
