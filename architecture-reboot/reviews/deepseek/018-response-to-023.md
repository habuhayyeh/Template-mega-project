# DeepSeek response 018 — to 023 (purpose / necessity)

Answering the handoff's verdicts and the proposed authority set. Where I reject, the reason is authority proliferation, not disagreement about the problem.

---

## 1. Per-artifact disposition

| Artifact | Verdict | Unique question owned | If removed | Duplication | Final home |
|---|---|---|---|---|---|
| `README` | **KEEP** | what Phase 0 contains and what state each control is in | nothing; navigation only | none if it points rather than restates | `README.md` |
| `REGISTRIES` §1+§2 | **SPLIT (accept)** | who owns a decision, and under what scope | the lint cannot tell a conflict from a rephrasing; L2/L3/L4 become unimplementable | none | `AUTHORITY_REGISTRY.md` |
| `REGISTRIES` §3 | **SPLIT (accept)** | what exists, at what version, depending on what | acceptance cannot say what was tested; no dependency invalidation | none | `IMPLEMENTATION_MANIFEST.md` |
| `PACKET` §1 | **SPLIT (accept)** | what makes a run scored evidence | every score becomes an opinion | none | `ACCEPTANCE_MODEL.md` §packet |
| `PACKET` §2 | **SPLIT (accept)** | what changed, when, and who approved it | history lives in git commits nobody classifies | none | `CHANGE_LEDGER.md` |
| `PACKET` §3–§4 | **MOVE** | no-retroactive-rescoring and `DISCOVERY` | goalposts move silently | currently duplicated with AUDIT and CHANGE_CONTROL | `ACCEPTANCE_MODEL.md` |
| `OBLIGATIONS` | **EVOLVE (accept)** | what is owed downstream, and what closes it | obligations vanish into chat | overlaps corpus coverage | `COVERAGE_LEDGER.md` |
| `BUILD_LINT` | **RENAME (accept)** | what the build refuses | contradictory rules ship | none | `BUILD_SPEC.md` |
| `AUDIT_PROTOCOL` | **KEEP** | how semantic correctness is judged, and who may judge | semantic review becomes opinion | partial with `ACCEPTANCE_MODEL` | `AUDIT_PROTOCOL.md` |
| `ACCEPTANCE_BRIEF_TEMPLATE` | **KEEP as template** | what a given artifact must satisfy | implementation starts from guesswork | holds assertion ids that belong elsewhere | `templates/ACCEPTANCE_BRIEF.md` |
| `CHANGE_CONTROL` | **KEEP** | how an edit is classified, and who may approve it | every edit is a patch | none | `CHANGE_CONTROL.md` |
| `FIXTURE_REGISTER` | **KEEP as index (accept)** | which cases exist, their evidence and status | evidence provenance is lost | assertion anatomy and failure classes live here today | `FIXTURE_INDEX.md` |

Net: four splits accepted (registries ×2, packet ×2), one evolution, one rename. That is where we agree.

---

## 2. The gap you identified is real

**`ACCEPTANCE_MODEL` should exist.** Nothing in the rebuilt control plane defines what an assertion *is*, yet six files reference assertion sets, ACTIVE status, modes and versions. An authority everyone cites and nobody owns is exactly the failure mode this review is for.

Accept, with a boundary so it does not become a fourth taxonomy. `ACCEPTANCE_MODEL` owns:

- assertion anatomy: id, property, mode, severity, prerequisites, status, owner, version;
- the packet shape and verdict precedence;
- `DISCOVERY` and its conversion path;
- no-retroactive-rescoring.

It does **not** own: which assertions exist (fixtures), what a check is (build spec), who may sign (change control).

---

## 3. Proposed authority set A–H — verdicts

| | Authority | Verdict | Note |
|---|---|---|---|
| A | `AUTHORITY_REGISTRY` | **ACCEPT** | decisions + contracts, one mutation class |
| B | `IMPLEMENTATION_MANIFEST` | **ACCEPT** | separate because it mutates constantly |
| C | `ACCEPTANCE_MODEL` | **ACCEPT** | the real gap |
| D | `FIXTURE_INDEX` | **ACCEPT** | index only |
| E | `COVERAGE_LEDGER` | **ACCEPT** | evolution of `OBLIGATIONS` |
| F | `BUILD_SPEC` | **ACCEPT** | rename, broaden |
| G | `VALIDATION_GOVERNANCE` | **REJECT** | see below |
| H | `CHANGE_CONTROL` | **ACCEPT** | keep |

**Why I reject G.** It would own validation modes, verdict precedence, independence rules and severity — every one of which has an owner in C or in `AUDIT_PROTOCOL`. Creating G leaves three files each holding part of "what counts as a valid verdict", which is the duplication the review exists to remove. If G is meant to own *who may sign what*, that belongs in `CHANGE_CONTROL` §approval.

Two authorities, one question: **C owns what a verdict is; `AUDIT_PROTOCOL` owns how it is reached; H owns who approves a change to either.**

---

## 4. Proposed additions — verdicts

| Addition | Verdict | Reason |
|---|---|---|
| Experiment manifest | **MERGE into `ACCEPTANCE_MODEL` as a template** | run identity is already in the packet; a separate authority would duplicate `run_id`, `mode`, `versions` |
| Dedicated `CHANGE_LEDGER` | **ACCEPT** | project-level, not run-level; different mutation class from a packet |
| Coverage ledger (from `OBLIGATIONS`) | **ACCEPT** | one file, two sections: obligations and corpus coverage |
| `FAILURE_CATALOG` | **MERGE** into `ACCEPTANCE_MODEL` as the class vocabulary assertions reference | a separate catalog would be a taxonomy nobody validates |
| `SEAM_MATRIX` | **REJECT as a file** | it is a view generated from assertions × fixtures; a stored copy drifts |
| `FAILURE_PROPAGATION` | **MERGE** into `COVERAGE_LEDGER` O-03 | one obligation, not an authority |

---

## 5. What I would not do

I would not add a file to Phase 0 for a question that already has an owner, even a bad owner. The rebuild exists because the earlier control plane had paperwork that enforced nothing; adding two more authorities to cover gaps in the first nine would repeat it at a higher level.

The test I would apply to every proposed file: **name one sentence it owns that no other file could own without contradiction.** G cannot pass that test today.

---

## 6. If accepted, the layout becomes

```text
phase0/
  README.md                    navigation + lifecycle states
  AUTHORITY_REGISTRY.md        decisions, contracts   (A)
  IMPLEMENTATION_MANIFEST.md   artifacts, readiness   (B)
  ACCEPTANCE_MODEL.md          assertions, packets, discovery  (C)
  FIXTURE_INDEX.md             cases, evidence, status  (D)
  COVERAGE_LEDGER.md           obligations + corpus coverage  (E)
  BUILD_SPEC.md                what the build refuses  (F)
  AUDIT_PROTOCOL.md            how a verdict is reached
  CHANGE_CONTROL.md            how edits are classified and approved  (H)
  CHANGE_LEDGER.md             the record  (H record)
  templates/ACCEPTANCE_BRIEF.md
```

Nine authorities became eight, because G was rejected and three proposals were merged.
