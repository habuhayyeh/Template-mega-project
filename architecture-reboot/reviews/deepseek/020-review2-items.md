# DeepSeek response 020 — Review 2, items 1–21

20 accepted, 1 partial. Format per item, compressed into one table; the partial is expanded below.

---

| # | Position | Canonical owner | Derived / snapshot | Conflict rule | Consequence |
|---|---|---|---|---|---|
| 1 | **ACCEPT** | frozen architecture (`CONSENSUS_ARCHITECTURE_v0.1`, `CONSENSUS_SUBMODULE_INTERFACES_v1`) | `AUTHORITY_REGISTRY` projects decisions from it | architecture wins; a registry edit that changes a responsibility boundary is a `DESIGN CHANGE`, not a row edit | registry cannot become a back door to redesign |
| 2 | **ACCEPT** | decision registry | — | two fields, never one: `semantic_owner` (submodule) and `governing_contract` (contract id) | "owner" stops meaning two things |
| 3 | **ACCEPT** | decision registry: `decision → governing_contract` | contract's `owns_decisions` is a generated view | the derived view is never authoritative; disagreement is an error | one direction only |
| 4 | **ACCEPT** | decision registry | — | replace `allowed_scopes` with `authority_scope` (where the decision is *made*) and `obligated_scopes` (who must *comply*) | consumers obey, they do not co-own |
| 5 | **ACCEPT** | decision registry | — | a decision enters only if it crosses a module boundary or affects acceptance | prevents a catalog of every local choice |
| 6 | **ACCEPT** | `AUTHORITY_REGISTRY` §contracts | — | a version binds to a content hash; new content requires a new version | a version can be cited forever without drift |
| 7 | **ACCEPT** | each record type | — | `control_state`, `readiness`, `decision_status`, `assertion_status`, `fixture_status`, `obligation_state` — distinct vocabularies | no ambiguous "status" |
| 8 | **ACCEPT** | `IMPLEMENTATION_MANIFEST` control-state section | `README` displays a derived table | README must match the manifest; a mismatch is a manifest error | README stops being an authority by accident |
| 9 | **ACCEPT** | `IMPLEMENTATION_MANIFEST` | — | `ACCEPTED` is illegal without packet ids | readiness cannot be asserted, only evidenced |
| 10 | **ACCEPT** | `IMPLEMENTATION_MANIFEST` | — | typed edges: `requires`, `consumes`, `provides`, `invalidates` | dependency-based invalidation becomes computable |
| 11 | **ACCEPT** | `ACCEPTANCE_MODEL` | — | `INVARIANT` (all cases, always scored) vs `ASSERTION` (bound to a case/fixture) | generic rules stop masquerading as case evidence |
| 12 | **PARTIAL** | see below | — | owner domain is `{runtime submodule, support authority}` | needs an explicit amendment, not an interpretation |
| 13 | **ACCEPT** | `ACCEPTANCE_MODEL` = verdict semantics; `AUDIT_PROTOCOL` = procedure | — | procedure may not define a verdict; semantics may not define the steps | one question each |
| 14 | **ACCEPT** | `FIXTURE_INDEX` points; baseline and assertion records hold content | — | index entries without a resolvable record are invalid | index cannot become evidence |
| 15 | **ACCEPT** | `COVERAGE_LEDGER` owns mappings only | readiness/fixture state referenced | duplication is an error, not a convenience | one source of state |
| 16 | **ACCEPT** | owner-ID registry inside `AUTHORITY_REGISTRY` | — | free-text owners are invalid | obligations become queryable |
| 17 | **ACCEPT** | rule records reference `decision` and `assertion` ids | contract/fixture/check content stays in their owners | a rule carrying its own copy of governing content is a duplicate | rules stop being a second registry |
| 18 | **ACCEPT** | `CHANGE_LEDGER` holds a `supersedes: <packet_id>` record | — | a packet is never edited; supersession is external | immutability survives |
| 19 | **ACCEPT** | `EXPERIMENT_MANIFEST` owns shared condition; packet owns per-run evidence | — | shared fields may not be re-declared in a packet | one experiment, one condition block |
| 20 | **ACCEPT** | `IMPLEMENTATION_MANIFEST` | every packet snapshots the control-plane version | a verdict without a control-plane version is unscorable | the rules that judged are recorded |
| 21 | **ACCEPT** | namespace registry, part of `AUTHORITY_REGISTRY` | — | ids are typed: `DEC-`, `CON-`, `CASE-`, `AS-`, `PKT-`, `EXP-`, `OBL-`, `CHG-` | lint can be automated without guessing |

---

## Item 12 — the one partial

**Position:** PARTIAL.

**The conflict is real.** The frozen workflow and `CONSENSUS_SUBMODULE_INTERFACES_v1` say every assertion has **exactly one owning submodule**. The fixture register already contains assertions owned by `BUILD` and `PROCESS`, which are not submodules. Either the frozen wording is wrong or those assertions are illegitimate.

**The three options, and why two fail:**

- *Force every assertion to a runtime submodule.* Then "the package was incomplete" (F-06a) must be attributed to a submodule that cannot control packaging. That is a false attribution, and false attribution is how a real failure gets fixed in the wrong place.
- *Drop BUILD/PROCESS assertions.* Then packaging and regression failures become unassertable, and the two most expensive defects we had are unspeakable.
- *Amend the owner domain.*

**Proposed amendment:** an assertion owner is exactly one **registered owner ID**, whose domain is `{runtime submodule, support authority}`. Support authorities are `BUILD`, `PROCESS`, `AUDIT`. The "exactly one" rule is preserved; only the domain widens.

**This is a protocol change**, not a clarification. It needs an `ACCEPTANCE CHANGE` recorded against the frozen interface document, with the reason: the frozen wording assumed all assertions concern runtime behaviour, and packaging/regression assertions do not.

**Consequence if accepted:** F-06a moves to `BUILD`, F-15a to `PROCESS`, and the register stops carrying an owner that contradicts the protocol it cites.

---

## What I am not doing

I am not reopening items 1–21 for argument. Twenty are mechanical, and the twenty-first is only waiting on whether the owner-domain amendment is granted. With it, the rewrite is prose-moving rather than design.
