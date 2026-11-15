# Phase 0 — Control Plane (rebuilt)

Phase 0 defines what correct means and how correctness is established. It contains no runtime behaviour.

## Lifecycle state

Every control has one state. The state is part of the control, not a note about it.

| State | Meaning | Who enforces |
|---|---|---|
| **SPEC** | written, no instrument exists | nobody; it is a design obligation |
| **M0** | enforced by a manual checklist a reviewer signs | the reviewer |
| **ACTIVE** | enforced by an instrument that fails closed | the instrument |

A control may not be cited as a guarantee above its state. Citing a SPEC control as if it prevented something is the error that made the last review necessary.

## Authorities

| Authority | Owns | File |
|---|---|---|
| Decision registry | who owns each semantic decision, its allowed scopes, its status | `REGISTRIES.md` §1 |
| Contract registry | contract identity and version | `REGISTRIES.md` §2 |
| Implementation manifest | artifacts, versions, dependencies, readiness | `REGISTRIES.md` §3 |
| Acceptance packet | the unit of acceptance | `PACKET.md` §1 |
| Change ledger | every governed change | `PACKET.md` §2 |
| Obligation ledger | downstream duties that must not vanish | `OBLIGATIONS.md` |
| Fixture register | reference cases and their assertions | `FIXTURE_REGISTER.md` |

## Controls

| Control | State | Purpose |
|---|---|---|
| `BUILD_LINT.md` | **SPEC** (M0 checklist in §7) | contradictory or unowned rules cannot ship |
| `AUDIT_PROTOCOL.md` | **SPEC** | semantic correctness is judged by procedure, not expectation |
| `ACCEPTANCE_BRIEF_TEMPLATE.md` | **SPEC** | implementation starts from a stated definition of correct |
| `CHANGE_CONTROL.md` | **M0** | edits are classified by effect, and the definition of success cannot drift |
| `FIXTURE_REGISTER.md` | **SPEC** (index only) | evidence-grounded reference cases |
| `PACKET.md` | **SPEC** | what a scored run must carry |
| `OBLIGATIONS.md` | **M0** | downstream duties have an owner and a future test |

## The rule that governs Phase 0 itself

Phase 0 is not exempt. Any change to a Phase 0 control is governed by `CHANGE_CONTROL.md`, and any change to what counts as correct is an `ACCEPTANCE CHANGE`.

That includes this file.

## What Phase 0 does not do

- It does not implement. All instruments are downstream.
- It does not restate the architecture. Contracts are referenced by version, not summarised.
- It does not promise reproducibility outside the mechanical subset. That limit is recorded in `OBLIGATIONS.md` O-21.
