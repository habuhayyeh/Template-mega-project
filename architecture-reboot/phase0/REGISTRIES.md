# REGISTRIES — decision, contract, manifest

Three authorities. Without them, the lint cannot tell whether two rules conflict, a rule cannot be traced to an owner, and acceptance cannot say what version was tested.

---

# §1 Decision registry

One row per **atomic** semantic decision. The registry, not the rule, says who owns it.

```yaml
- decision: AP_ORDER_WITHIN_PROBLEM
  question: "In what order do lines appear inside one problem block?"
  owner_contract: AP_RENDER_CONTRACT
  owner_submodule: S4
  allowed_scopes: [RENDER]
  status: FROZEN            # FROZEN | PROVISIONAL | WITHDRAWN
  version: 1
  depends_on: []
```

Rules that reference an unknown decision, or a decision whose status is WITHDRAWN, fail the build (L2b, L5).

**Atomicity rule.** A decision may contain orthogonal subrules only if those subrules have their own decision ids. If two rules for one decision address different subjects, that is either two decisions or a conflict — never one decision with two rules.

**Scope rule.** `allowed_scopes` is what L3 checks. A rule may not act outside its decision's allowed scopes.

Seed entries, from work already done:

| decision | owner_submodule | allowed_scopes | status |
|---|---|---|---|
| `AP_ORDER_WITHIN_PROBLEM` | S4 | RENDER, STRUCTURE | FROZEN |
| `DUPLICATE_IDENTITY` | S2 | STRUCTURE | FROZEN |
| `PROBLEM_MEMBERSHIP` | S3 | STRUCTURE | FROZEN |
| `CURRENT_ADOPTION` | S2 | STRUCTURE | FROZEN |
| `UNIT_COMPLETENESS` | S4 | STRUCTURE | FROZEN |
| `STANDING_ITEM_TRIGGER` | S4 | STRUCTURE | PROVISIONAL |
| `OPERATOR_SELECTION` | S4 | STRUCTURE | PROVISIONAL |
| `SPAN_BOUNDARY` | I2 | INGEST | FROZEN |
| `SOURCE_FAMILY` | I1 | INGEST | PROVISIONAL |
| `RENDER_VOICE` | R1 | RENDER | FROZEN |
| `SECTION_LIST` | S4 | STRUCTURE | FROZEN |
| `COVERAGE_DISPOSITION` | S3 | STRUCTURE | FROZEN |

---

# §2 Contract registry

Every contract that can own a decision, with a version. Rules reference the version, not the path, so a path move is not a semantic change.

```yaml
- contract: AP_RENDER_CONTRACT
  version: 3
  status: FROZEN
  source: architecture-reboot/CONSENSUS_ARCHITECTURE_v0.1.md §7-§9
  owns_decisions: [AP_ORDER_WITHIN_PROBLEM, SECTION_LIST]
```

| contract | version | status |
|---|---|---|
| `INGEST_CONTRACT` | 0 | PROVISIONAL |
| `STRUCTURE_CONTRACT` | 0 | PROVISIONAL |
| `RENDER_CONTRACT` | 0 | PROVISIONAL |
| `AP_RENDER_CONTRACT` | 0 | PROVISIONAL |
| `OPERATOR_REGISTRY` | 0 | PROVISIONAL |
| `STANDING_ITEM_CONTRACT` | 0 | PROVISIONAL |

A contract at version 0 may own decisions but may not declare any as FROZEN.

---

# §3 Implementation manifest

What exists, at what version, depending on what. Readiness is one of:

`DESIGNED | AUTHORED | UNIT_VERIFIED | INTEGRATED | ACCEPTED`

```yaml
- artifact: INGEST
  version: 0
  readiness: DESIGNED
  depends_on: [SPAN_BOUNDARY_DEF, SOURCE_FAMILY_DEF]
  acceptance_state: none
```

| artifact | readiness | depends on |
|---|---|---|
| INGEST | DESIGNED | span boundary, source family |
| STRUCTURE | DESIGNED | decision registry, operator registry |
| RENDER | DESIGNED | operator registry, style table |
| CHECK | DESIGNED | Case IR schema |
| AUDIT | DESIGNED | assertion packet |
| BUILD | SPEC | rule schema, registries |

**Readiness is not a quality claim.** `UNIT_VERIFIED` means the unit passed its own assertions; it says nothing about the integrated note. Only `ACCEPTED` means a packet passed.

---

# §4 Who maintains these

The engineer maintains them and the reviewer checks them. A registry that disagrees with reality is worse than no registry, because it is cited as authority.
