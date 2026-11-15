# Phase 0 — Control Plane

Five documents, no runtime code. Each one exists because we hit the failure it prevents.

| File | Prevents |
|---|---|
| `BUILD_LINT.md` | contradictory contract rules shipping in one compiled package (C11) |
| `AUDIT_PROTOCOL.md` | semantic criteria being written to fit whatever got built |
| `ACCEPTANCE_BRIEF_TEMPLATE.md` | implementation without a stated definition of correct |
| `CHANGE_CONTROL.md` | goalposts moving while the measurement stays the same (C14) |
| `FIXTURE_REGISTER.md` | testing invented cases instead of defects that reached output |

Order of use: brief → implementation → lint → check → audit → acceptance → freeze → record.

None of these change during Phase 1 unless a `DESIGN CHANGE` or `ACCEPTANCE CHANGE` is recorded.
