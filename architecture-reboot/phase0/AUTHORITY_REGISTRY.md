# AUTHORITY_REGISTRY — decisions, contracts, owners, namespaces

Canonical for: **who owns each semantic decision, under which contract, at which version.**

This registry is **downstream of the frozen architecture**. It cannot move a responsibility by editing a row. A change here that alters a responsibility boundary is a `DESIGN CHANGE`.

---

## 1. Decision records

A decision is registered when it is **normative and externally consequential**: interface-visible, cross-referenced by another contract, multiply governed, referenced by an acceptance predicate or coverage obligation, or such that changing its owner or value semantics requires a `DESIGN CHANGE` or `ACCEPTANCE CHANGE`.

Anything else stays local and unregistered.

```yaml
decision: AP_ORDER_WITHIN_PROBLEM
question: "In what order do lines appear inside one problem block?"
semantic_owner: S4                 # who decides — a submodule or support authority
governing_contract: AP_RENDER_CONTRACT
authority_scope: STRUCTURE         # where the decision is made
obligated_scopes: [RENDER]         # who must comply; compliance is not ownership
status: FROZEN                     # FROZEN | PROVISIONAL | WITHDRAWN
version: 1
depends_on: []
```

Two fields, never one: `semantic_owner` is the module that decides; `governing_contract` is the document that says what the decision is. Conflating them is how "owner" started meaning two different things.

**`authority_scope` vs `obligated_scopes`.** Only the authority scope may decide. An obligated scope must obey the decision and may not redefine it. A consumer that needs a different behaviour has found a missing decision, not a licence.

### Direction of the relation

`decision → governing_contract` is canonical. Any `contract → decisions` list is **derived**; it may be generated and displayed, never edited, and a disagreement between the two is an error.

### Seed decisions

| decision | semantic_owner | authority_scope | obligated | status |
|---|---|---|---|---|
| `AP_ORDER_WITHIN_PROBLEM` | S4 | STRUCTURE | RENDER | FROZEN |
| `SECTION_LIST` | S4 | STRUCTURE | RENDER | FROZEN |
| `DUPLICATE_IDENTITY` | S2 | STRUCTURE | — | FROZEN |
| `PROBLEM_MEMBERSHIP` | S3 | STRUCTURE | — | FROZEN |
| `CURRENT_ADOPTION` | S2 | STRUCTURE | S3, S4 | FROZEN |
| `UNIT_COMPLETENESS` | S4 | STRUCTURE | — | FROZEN |
| `OPERATOR_SELECTION` | S4 | STRUCTURE | RENDER | PROVISIONAL |
| `STANDING_ITEM_TRIGGER` | S4 | STRUCTURE | — | PROVISIONAL |
| `SPAN_COVERAGE` | I2 | INGEST | — | FROZEN |
| `OBJECT_DISPOSITION` | S3 | STRUCTURE | — | FROZEN |
| `SOURCE_FAMILY` | I1 | INGEST | — | PROVISIONAL |
| `RENDER_VOICE` | R1 | RENDER | — | FROZEN |
| `RENDER_CONTAINMENT` | R1 | RENDER | — | PROVISIONAL |

`SPAN_COVERAGE` and `OBJECT_DISPOSITION` are separate decisions that used to share a name: ingest accounts for spans, structure disposes of objects. They fail differently and have different owners.

---

## 2. Contract records

```yaml
contract: AP_RENDER_CONTRACT
version: 3
content_hash: sha256:…
status: FROZEN          # FROZEN | PROVISIONAL | WITHDRAWN
source: CONSENSUS_ARCHITECTURE_v0.1 §7–§9
```

A version binds to an **immutable content hash**. New content means a new version; a version number that can point at different text is not a version.

A contract at version 0 may own decisions but may not declare them `FROZEN`.

---

## 3. Owner IDs

Every owner referenced anywhere in Phase 0 is one of these, by id. Free-text owners are invalid.

| id | kind |
|---|---|
| `I1` `I2` `I3` `I4` | runtime submodule |
| `S1` `S2` `S3` `S4` | runtime submodule |
| `R1` `R2` `R3` | runtime submodule |
| `BUILD` | support authority |
| `PROCESS` | support authority |
| `AUDIT` | support authority |
| `SCORER` | support authority |

Runtime submodules own case assertions. Support authorities own gates and controls. This preserves the frozen rule that a runtime case assertion has exactly one owning submodule.

---

## 4. Identifier namespaces

Typed before any automation, so a lint never has to guess what an id refers to.

| prefix | record |
|---|---|
| `DEC-` | decision |
| `CON-` | contract |
| `CASE-` | fixture case |
| `AS-` | assertion set |
| `PRD-` | predicate |
| `PKT-` | acceptance packet |
| `EXP-` | experiment |
| `OBL-` | coverage obligation |
| `CHG-` | change ledger entry |
| `CTL-` | control (Phase 0 document) |

---

## 5. Conflict rules

1. Architecture beats this registry. A registry row that contradicts a frozen contract is wrong, not authoritative.
2. `decision → governing_contract` beats any derived list.
3. A decision with two owners is an error, not a merge.
4. A rule citing a `WITHDRAWN` decision fails the build.
