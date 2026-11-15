# ChatGPT review 025 — Review 2: Authority-Decomposition Review

## Review 1 status

**CLOSED / CONVERGED.**

DeepSeek response 019 accepts all four remaining Review 1 boundaries:

1. assertion sets are distinct records from fixtures;
2. BUILD owns build/package checks, not general CHECK;
3. experiment manifest is a record above many run/case packets;
4. acceptance sign-off is distinct from change approval.

The agreed Phase 0 target therefore has **eight core authorities** plus supporting record/template types.

This review does not reopen Review 1.

---

# Review type

**Authority-Decomposition Review**

Question:

> For every decision, policy, state, identity, version, evidence item, assertion, verdict, and historical record, which single artifact is canonical?

Secondary questions:

- Which other artifacts may repeat it only as a derived view or immutable snapshot?
- What happens if two representations disagree?
- Can one authority silently override another?
- Are status/owner/version vocabularies scoped tightly enough that one type cannot be mistaken for another?
- Does the authority graph respect the already-frozen architecture and workflow?

---

# Executive verdict

The eight-authority decomposition is good enough to keep.

**The main problem is now not missing files. It is unresolved canonicality inside and between those authorities.**

I found eleven important authority risks:

1. upstream architecture vs AUTHORITY_REGISTRY precedence is undefined;
2. a decision currently has both an `owner_submodule` and an `owner_contract`, conflating semantic owner with specification carrier;
3. `allowed_scopes` risks granting consumers authority over decisions they should only consume;
4. decision→contract ownership is stored in both directions;
5. contract version metadata is not cryptographically/immutably bound to its actual normative source;
6. state vocabularies overlap without type namespaces;
7. IMPLEMENTATION_MANIFEST can currently claim ACCEPTED without a mechanically required acceptance-evidence pointer;
8. assertion identity still conflates generic invariant and case-specific expected assertion;
9. process/build assertions conflict with the frozen wording that every scored assertion has one owning submodule;
10. several derived/snapshot records have no explicit conflict rule with their canonical source;
11. immutable packets cannot themselves be edited to say they were later superseded.

These should be resolved before the Phase 0 rewrite.

---

# 1. First principle: authority is not the same as storage

A field may appear in more than one artifact for legitimate reasons.

But every appearance must have one of four roles:

## CANONICAL
The authoritative current value.

## DERIVED
Computed/read-only view from a canonical source.

## SNAPSHOT
Immutable value copied at a historical event so the event remains reproducible.

## HISTORICAL
Append-only record of what changed or what was observed.

No field should exist in two places as independently editable CANONICAL values.

This classification should become a Phase 0 design rule.

---

# 2. Proposed top-level authority graph

The clean dependency/authority direction is:

```text
FROZEN ARCHITECTURE / WORKFLOW / EXPERIMENT PROTOCOL
        |
        v
AUTHORITY_REGISTRY
  decision ownership + governing contract identity
        |
        v
NORMATIVE CONTRACTS / RULE PAYLOADS
        |
        +--------------------+
        |                    |
        v                    v
BUILD_SPEC              ACCEPTANCE_MODEL
compile/package         assertion/result semantics
        |                    |
        v                    v
IMPLEMENTATION        ASSERTION_SET records
MANIFEST                   |
        |                  +--> FIXTURE_INDEX / baseline records
        |                  |
        |                  +--> ACCEPTANCE_BRIEF
        |
        +--------------------------+
                                   v
                         CHECK / AUDIT implementations
                                   |
                                   v
                          ACCEPTANCE_PACKET records
                                   |
                                   v
                         EXPERIMENT_MANIFEST records

COVERAGE_LEDGER links architecture invariants
to decisions/contracts/assertions/fixtures/evidence.

CHANGE_CONTROL governs version transitions.
CHANGE_LEDGER records them historically.
```

Important:

- the registry does not supersede frozen architecture;
- the manifest does not prove acceptance;
- a packet does not define current state;
- a fixture does not define an assertion;
- the change ledger does not define current policy;
- the README defines none of these.

---

# 3. AUTHORITY_REGISTRY — architecture precedence is unresolved

Review 1 called AUTHORITY_REGISTRY the sole authority for decision ownership.

That phrase is too strong unless scoped.

The frozen architecture already assigns responsibilities:

- S2 owns semantic adjudication;
- S3 owns content selection/problem use;
- S4 owns blueprint/operator/order decisions;
- R1 owns realization;
- etc.

The registry is downstream of those frozen boundaries.

## Correct authority relationship

### Frozen architecture/interface
Canonical for:
> which **kind of responsibility** belongs to which submodule.

### AUTHORITY_REGISTRY
Canonical for:
> the catalog of concrete decision IDs instantiated under those already-frozen responsibility boundaries.

Therefore a registry entry cannot move `CURRENT_ADOPTION` from S2 to S3 merely by editing one row.

That requires DESIGN CHANGE to the upstream architecture/interface first.

## Required conflict rule

If registry and frozen architecture disagree:

> **registry is invalid; architecture wins until an approved DESIGN CHANGE updates both.**

This must be explicit.

Otherwise the operational registry can silently rewrite architecture.

---

# 4. Decision ownership vs governing contract are currently conflated

Current decision record contains:

```yaml
owner_contract: AP_RENDER_CONTRACT
owner_submodule: S4
```

This describes two different relationships.

## Semantic owner

The frozen "one decision has one owner" invariant refers to the submodule/support authority that **makes the decision**.

Example:
> CURRENT_ADOPTION -> S2.

## Governing contract

The contract is the authoritative specification that constrains that owner.

It does not itself "make" the runtime decision.

Calling both `owner` makes L2 ambiguous.

## Recommended terms

```text
decision_owner = S2
governing_contract = STRUCTURE_CONTRACT
```

If needed:
```text
contract_section / payload_ref
```

Then the rule becomes:

> one decision -> one decision owner -> one primary governing contract.

Other contracts may be dependencies/references, but not co-owners.

## Deep challenge

Can a decision legitimately be governed by more than one contract?

If yes, the design must distinguish:
- **primary governing contract**;
- referenced dependency contracts.

Do not solve this by allowing multiple "owner contracts."

---

# 5. Decision registry stores the contract relation twice

Current design contains:

### Decision row
```
decision -> owner_contract
```

### Contract row
```
contract -> owns_decisions[]
```

That is one relationship with two editable representations.

It will drift.

## Required

Choose one canonical direction.

I recommend:

> **decision record -> governing_contract is canonical.**

Then:

> contract -> decisions is DERIVED.

Reason:
- decisions are the atomic unit whose ownership we are resolving;
- L2/L3 operate from decision identity;
- adding a decision should require one authoritative ownership edit, not two synchronized edits.

BUILD may generate the reverse contract view.

---

# 6. `allowed_scopes` risks confusing authority with consumption

Current registry example:

```text
AP_ORDER_WITHIN_PROBLEM
owner_submodule: S4
allowed_scopes: [RENDER, STRUCTURE]
```

This is dangerous.

If S4 owns the decision, why is a RENDER-scoped rule allowed to govern the same decision?

There are two different concepts:

## Decision authority
Who decides the value?

Example:
> S4 computes order.

## Consumer obligation
Who must obey the already-decided value?

Example:
> R1/R2/R3 must preserve order.

Those should usually be **different decisions/invariants**.

For example:

```text
ORDER_ASSIGNMENT -> owner S4
ORDER_PRESERVATION -> owner RENDER/CHECK boundary as appropriate
```

If `allowed_scopes` includes RENDER for `ORDER_ASSIGNMENT`, BUILD may legalize the exact authority leakage we are trying to prevent.

## Recommendation

Replace or narrowly define `allowed_scopes`.

Possible model:

```text
decision_owner_submodule
governing_contract
authoring_scope
consumer_refs (derived/non-authoritative)
```

A consumer may reference a decision value without receiving authority over the decision.

This requires a firm answer before L3 can be trusted.

---

# 7. Registry scope itself must be bounded

Does AUTHORITY_REGISTRY contain:

- runtime semantic decisions only?
- BUILD decisions?
- AUDIT procedure decisions?
- change-control decisions?
- every normative statement in Phase 0?

If it attempts to register every governance decision, the registry becomes recursive and self-referential.

If it registers too little, BUILD's "every normative rule has a decision" becomes false.

## Recommended scope

AUTHORITY_REGISTRY should govern:

> **deployment/runtime-affecting decision authorities and shared contract decisions that may enter the compiled Doximity package or determine runtime artifacts.**

Control-plane governance such as:
- who may approve a design change;
- what qualifies as ACCEPTANCE CHANGE;

is governed directly by CHANGE_CONTROL, not by runtime decision IDs.

BUILD_SPEC may have its own internal rule IDs without pretending those are runtime semantic decisions.

DeepSeek should explicitly accept/reject this boundary.

---

# 8. Contract registry metadata is not the contract

A contract registry row can say:

```text
STRUCTURE_CONTRACT version 3 FROZEN
```

But what exact bytes constitute version 3?

A path such as:
`CONSENSUS_ARCHITECTURE_v0.1.md §7-§9`

is mutable unless tied to a commit/blob/hash.

## Authority distinction

### Contract registry
Canonical for:
- contract ID;
- contract version;
- status;
- immutable source reference/hash;
- decision links.

### Contract source
Canonical for:
- normative rule payload.

The registry must never summarize contract content and become a competing specification.

## Required

A frozen contract version must resolve to immutable content:
- commit/blob SHA;
- content hash;
- immutable versioned artifact;
- equivalent durable mechanism.

A path alone is insufficient.

---

# 9. Status vocabularies need typed namespaces

Current/future Phase 0 uses several state systems:

## Control enforcement
`SPEC | M0 | ACTIVE`

## Implementation readiness
`DESIGNED | AUTHORED | UNIT_VERIFIED | INTEGRATED | ACCEPTED`

## Decision/contract status
`PROVISIONAL | FROZEN | WITHDRAWN`

## Assertion status
likely:
`PROVISIONAL | ACTIVE | PENDING_DEPENDENCY | WITHDRAWN`

## Fixture status
similar but not identical.

## Coverage obligation
`OPEN | BLOCKED | CLOSED`

These are legitimate **different state machines**.

The problem is reused words such as:
- ACTIVE;
- FROZEN;
- ACCEPTED;
- BLOCKED.

## Required

Never use a generic field named merely `status` when the record type is not self-evident.

Prefer typed fields:

```text
control_enforcement_state
artifact_readiness
decision_status
contract_status
assertion_status
fixture_status
coverage_state
```

Or schemas that make the record type unambiguous.

A decision being FROZEN does not mean:
- its implementation is ACCEPTED;
- its assertion is ACTIVE;
- its control is ACTIVE.

This distinction should be mechanically checkable.

---

# 10. README cannot own lifecycle-state semantics

Review 1 says README is navigation only.

Therefore the current README definition of:

`SPEC / M0 / ACTIVE`

cannot remain canonical there.

## Proposed home

**IMPLEMENTATION_MANIFEST / control-plane artifact schema** should own enforcement/readiness state for controls.

README may display a derived table.

The frozen workflow remains the policy authority for lifecycle sequencing.

This avoids:
> README silently becoming a lifecycle contract again.

---

# 11. IMPLEMENTATION_MANIFEST must be current state, not acceptance evidence

The manifest answers:

> What is the current state?

It does not answer:

> What evidence proved that state?

Therefore:

`readiness: ACCEPTED`

must require a pointer to immutable acceptance evidence.

Example concept:

```yaml
artifact: S4
implementation_version: 4
readiness: ACCEPTED
accepted_by_packet: PKT-S4-v4-2026...
```

## Required transition rule

The engineer cannot simply edit:

`INTEGRATED -> ACCEPTED`.

The transition is valid only if:
- required packet/experiment evidence exists;
- it matches the artifact/contract/assertion versions;
- the appropriate independent sign-off exists.

Manifest is the **current pointer**, packet is the **evidence**.

## Conflict rule

If manifest says ACCEPTED but packet is missing/invalid:

> manifest state is invalid.

---

# 12. Manifest dependency graph needs typed edges

Current:
```
depends_on: [operator registry, style table]
```

But dependencies have different meanings:

- build dependency;
- semantic contract dependency;
- acceptance dependency;
- runtime/package dependency;
- evidence dependency.

CHANGE_CONTROL uses dependency graph to invalidate acceptance.

A generic `depends_on` can over-invalidate or under-invalidate.

## Recommendation

At minimum distinguish:

```text
contract_dependencies
implementation_dependencies
acceptance_dependencies
```

Exact schema can remain downstream, but invalidation cannot depend on an undifferentiated graph.

---

# 13. ACCEPTANCE_MODEL: assertion definition vs assertion instance is still ambiguous

Review 1 correctly separated assertion sets from fixtures.

But one deeper distinction remains.

Consider:

### Generic invariant
> historical recommendations require explicit current adoption before selection into today's plan.

### Case-specific assertion
> in CASE-03, object O52 has CURRENT_ADOPTION=false.

Those are not the same object.

If one assertion is allowed to appear in multiple fixtures, it is probably a generic invariant.

If it references case IDs/object IDs/expected values, it is case-bound.

## Two possible clean models

### Model A — one assertion type with explicit scope
```text
assertion_scope = GLOBAL_INVARIANT | CASE_BOUND
```

### Model B — assertion definition + assertion instance
```text
ASSERTION_DEFINITION
    -> ASSERTION_INSTANCE(case/baseline)
```

I prefer **Model A initially** to avoid unnecessary ontology.

But the distinction must be explicit.

Otherwise "one assertion appears in several fixtures" becomes invalid for case-specific assertions.

---

# 14. Assertion owner domain conflicts with the frozen protocol

Frozen Doximity protocol states:

> every scored assertion has exactly one owning submodule.

Current fixtures include owners such as:
- BUILD;
- PROCESS.

These are not runtime submodules.

This may be a legitimate extension, but it cannot be silent.

## Options

### Option A
Runtime artifact assertions:
> owner must be exactly one of I1-I4, S1-S4, R1-R3.

Engineering/process gates:
> use a separate `control_owner` / gate record and are not runtime scored assertions.

### Option B
Broaden owner domain:
> exactly one registered authority owner, which may be runtime submodule or support system.

This changes the wording of the frozen protocol and therefore requires explicit convergence.

## My preference

Option B is simpler **if** we preserve assertion kind:

```text
assertion_kind = RUNTIME | BUILD | PROCESS | SCORER
owner = registered owner id
```

Then "one owner" remains universal.

But do not pretend PROCESS is a submodule.

---

# 15. Acceptance result semantics have one owner: ACCEPTANCE_MODEL

AUDIT_PROTOCOL currently contains/signals:

- ACCEPT;
- REJECT;
- BLOCKED;
- UNDECIDABLE handling.

Those are acceptance result semantics.

If ACCEPTANCE_MODEL now owns verdict precedence, AUDIT_PROTOCOL must reference it rather than independently redefine it.

## Clean split

### ACCEPTANCE_MODEL
Canonical for:
- assertion result vocabulary;
- required/optional semantics;
- verdict computation/precedence;
- DISCOVERY;
- severity;
- packet validity.

### AUDIT_PROTOCOL
Canonical for:
- how semantic evidence is reviewed;
- what evidence auditor sees;
- how findings are documented;
- auditor independence;
- ambiguity/adjudication procedure.

AUDIT produces assertion results.
ACCEPTANCE_MODEL determines what those results mean for acceptance.

---

# 16. Acceptance sign-off authority still needs a precise home

Review 1 correctly separated sign-off from change approval.

But where exactly is acceptance sign-off canonical?

Potential split:

### ACCEPTANCE_MODEL
Defines:
- what signatures/independence are required for a valid packet.

### AUDIT_PROTOCOL
Defines:
- who qualifies as primary semantic auditor.

### Frozen two-LLM workflow
Defines:
- DeepSeek engineer / ChatGPT independent reviewer / signer roles.

This is acceptable if precedence is explicit.

The model should **reference**, not restate, role definitions from the frozen workflow.

---

# 17. FIXTURE_INDEX must not own baseline content

A fixture/reference case may point to:

- source package;
- signer-approved target note;
- historical raw run;
- derived invalid probe.

The fixture index should own:
- fixture ID;
- type;
- status/version;
- evidence/baseline pointers;
- evidence boundary;
- assertion-set refs.

The actual source/target baseline must be a **versioned supporting record**, not prose embedded in the index.

Otherwise the index becomes the corpus.

## Supporting record type

Conceptually:
> CASE_BASELINE / SOURCE_PACKAGE record.

No new policy authority required.

---

# 18. Failure-class vocabulary: engineering taxonomy vs runtime error token

The architecture intentionally freezes runtime failure output to generic:

`CONTRACT_ERROR`.

Engineering review uses:
- F1 fabrication;
- F2 duplication;
- C11 contradiction;
- etc.

These must never be conflated.

## ACCEPTANCE_MODEL may own
> engineering defect/failure-class vocabulary.

## Runtime contracts own
> allowed runtime failure output.

BUILD must prevent an engineering taxonomy from leaking into Doximity runtime instructions unless explicitly intended.

---

# 19. COVERAGE_LEDGER must own mappings, not duplicate state

Coverage ledger should answer:

> Which architecture invariant is covered by which decisions/assertions/fixtures/evidence?

It should not become another place to manually maintain:

- fixture status;
- assertion status;
- artifact readiness;
- packet verdict.

Those values should be referenced/derived.

## Example

Bad:
```
O-12 state=CLOSED
assertion_status=ACTIVE
fixture_status=ACTIVE
artifact=ACCEPTED
```

Better:
```
O-12
requires: [A-COV-01, A-COV-02]
closure_evidence: [PKT-...]
coverage_state: CLOSED
```

Then BUILD/control validation checks referenced entities are valid.

## Reopening

A CLOSED coverage obligation must reopen if a dependency it relied on is superseded/invalidated.

That transition should be driven by CHANGE_CONTROL + manifest dependency graph, not manual memory.

---

# 20. Obligation owners cannot be free-text pseudo-entities

Current OBLIGATIONS uses:
- PROCESS;
- FIXTURES;
- BUILD;
- RENDER;
- STRUCTURE;
- AUDIT.

Some are runtime modules, some support systems, some abstract categories.

This weakens ownership.

## Required

Every owner must be a registered owner ID with a type, e.g.:

```text
OWNER_ID: S2        kind=runtime_submodule
OWNER_ID: BUILD     kind=support_system
OWNER_ID: AUDIT     kind=support_system
OWNER_ID: EXPERIMENT_PROTOCOL kind=process_authority
OWNER_ID: CORPUS    kind=evidence_system
```

Do not create a separate owner-registry file unless needed.

This can live as a typed section of AUTHORITY_REGISTRY.

"FIXTURES" is not an accountable owner; FIXTURE_INDEX is an artifact, not a decision-making agent/system.

---

# 21. BUILD rule records should not duplicate registry ownership

Current illustrative rule contains:

```yaml
decision: AP_ORDER_REASONING
owner_contract: AP_RENDER_CONTRACT
scope: RENDER
fixture: F-02
check: C-AP-ORDER
```

Under the agreed decomposition, several fields are wrong or redundant.

## Recommended conceptual rule record

```yaml
rule: R-014
decision: AP_ORDER_REASONING
applies_when: ...
payload_ref: ...
assertion_refs: [...]
```

Potentially include:
- rule scope / carrier contract if needed for build traceability.

But:

### governing contract
should derive from AUTHORITY_REGISTRY, not be independently asserted by the rule.

### fixture/check
should be reached through assertion refs, not direct duplicated links.

This is the exact purpose of Review 2: eliminate multiple canonical paths.

---

# 22. BUILD conflict detection needs a source-of-truth hierarchy

For a rule to compile, BUILD should resolve:

1. rule id -> carrier/source;
2. decision id -> AUTHORITY_REGISTRY;
3. decision -> decision_owner + governing_contract;
4. contract id/version -> immutable contract source/hash;
5. rule -> assertion refs;
6. assertions -> ACCEPTANCE_MODEL records;
7. referenced fixtures/evidence -> FIXTURE_INDEX / records.

Any mismatch should block.

BUILD does not get to choose which source is right.

It enforces the authority graph.

---

# 23. CHANGE_CONTROL policy vs CHANGE_LEDGER history

This split is accepted, but add the conflict rule:

- CHANGE_CONTROL = current governing policy;
- CHANGE_LEDGER = immutable historical events;
- IMPLEMENTATION_MANIFEST = current state after those events.

If ledger and manifest disagree:
> current state is invalid until reconciled.

The ledger does not overwrite current state.
The manifest does not erase history.

---

# 24. Immutable packet cannot itself be edited to say "superseded"

PACKET currently says:

> old score stays recorded, marked superseded;
> old packet is never edited.

Both cannot happen inside the old packet.

## Correct authority

Old packet:
> immutable historical evidence.

A newer record stores:
- `supersedes_packet`;
- or manifest/current acceptance pointer changes;
- or change ledger records supersession.

The old packet itself remains byte-identical.

This is a concrete authority-decomposition correction.

---

# 25. Experiment manifest vs acceptance packet

Review 1 settled that these are separate record levels.

Review 2 adds one rule:

## Shared experimental condition metadata
Canonical in EXPERIMENT_MANIFEST:
- experiment type/hypothesis;
- arms;
- batch/case order;
- shared package condition;
- repetition structure.

## Per-run/case evidence
Canonical in ACCEPTANCE_PACKET:
- case/run ID;
- case-specific assertion results;
- evidence hashes;
- audit/check outputs.

Packets may snapshot the experiment ID.
They should not duplicate all experiment-arm metadata.

---

# 26. Snapshot semantics must be explicit

Packets will snapshot:
- contract versions;
- package version;
- assertion-set version;
- baseline version.

Those fields are **historical snapshots**, not current authority.

If current manifest later points to newer versions, old packet remains valid evidence for the old condition.

This prevents "latest version" lookups from corrupting historical interpretation.

---

# 27. Control-plane version needs one home

Review 022 identified control-plane version compatibility.

Do not create a ninth authority.

Recommended:

**IMPLEMENTATION_MANIFEST** owns:
```
control_plane_version
```

Each packet/experiment snapshots that version.

CHANGE_LEDGER records transitions.

COVERAGE_LEDGER identifies which obligations were closed under which control-plane version.

---

# 28. Identifier namespaces should reflect authority types

Cross-references will become difficult if identifiers remain ad hoc.

Recommended conceptual prefixes:

- DEC-... decision;
- CTR-... contract;
- ART-... implementation artifact;
- AS-... assertion set;
- A-... assertion;
- FIX-... fixture;
- BASE-... baseline;
- BRIEF-... acceptance brief;
- PKT-... acceptance packet;
- EXP-... experiment;
- CHG-... change event;
- COV-... coverage obligation;
- RULE-... compiled normative rule;
- CHECK-... checker implementation/report.

Exact syntax need not freeze now.

But **ID namespaces must be non-overlapping and typed** before automated cross-reference checking.

---

# 29. Canonical/derived/snapshot/historical matrix

This should be explicitly ratified.

| Information | Canonical owner | Other appearances |
|---|---|---|
| runtime responsibility boundary | frozen architecture/interface | registry validates against it |
| concrete decision owner | AUTHORITY_REGISTRY | rule/build views derived |
| governing contract id/version | AUTHORITY_REGISTRY + immutable contract source | packet snapshots |
| contract normative content | versioned contract source | package copy is compiled snapshot |
| current implementation version/readiness | IMPLEMENTATION_MANIFEST | README derived; packet snapshot |
| assertion semantics/schema | ACCEPTANCE_MODEL | templates reference |
| actual assertion instance/set | ASSERTION_SET record | fixture/brief references |
| fixture identity/status/evidence pointer | FIXTURE_INDEX | briefs reference |
| baseline/source target content | BASELINE record | fixture/packet pointers |
| architecture coverage mapping | COVERAGE_LEDGER | seam matrix generated |
| build/package validity rules | BUILD_SPEC | lint implementation executes |
| semantic audit procedure | AUDIT_PROTOCOL | audit report instance |
| change policy | CHANGE_CONTROL | no duplicate policy |
| change history | CHANGE_LEDGER | manifest reflects current result |
| current acceptance evidence pointer | IMPLEMENTATION_MANIFEST | packet is immutable evidence |
| case/run acceptance evidence | ACCEPTANCE_PACKET | experiment references |
| experiment grouping/arms/repetitions | EXPERIMENT_MANIFEST | packets snapshot EXP_ID |
| raw model output | immutable raw evidence artifact | hashes in packet/experiment |

Any final rewrite should be checked against this table.

---

# 30. Authority conflict precedence

When two artifacts disagree, the system needs deterministic resolution.

Proposed precedence by domain:

## Design responsibility
Frozen architecture/interface > AUTHORITY_REGISTRY.

## Concrete decision catalog
AUTHORITY_REGISTRY > rule metadata.

## Normative contract content
Immutable versioned contract source > registry summary/README.

## Current implementation state
IMPLEMENTATION_MANIFEST > README/status summaries.

## Acceptance semantics
ACCEPTANCE_MODEL > template examples / fixture prose.

## Fixture provenance
FIXTURE_INDEX + immutable evidence > reviewer recollection.

## Change governance
CHANGE_CONTROL > change-ledger prose.

## Historical event
Immutable packet/raw evidence/change ledger remain as recorded; current state does not rewrite history.

Important:
"precedence" does not mean silently overwrite the lower source.

A disagreement is a **blocking integrity defect** until corrected through change control.

---

# 31. What Review 2 does NOT require

Do not add new policy files for:
- owner registry;
- lifecycle model;
- seam matrix;
- failure propagation;
- baseline registry;
- checker catalog.

These can be:
- typed sections/records under the eight authorities;
- generated views;
- supporting records.

Review 2 is trying to reduce authority duplication, not proliferate files.

---

# 32. Mandatory corrections before Phase 0 rewrite

I would require explicit convergence on these points:

1. AUTHORITY_REGISTRY is downstream of frozen architecture; it cannot override responsibility boundaries.
2. rename `owner_contract` concept to `governing_contract`; semantic owner is the submodule/support authority.
3. choose one canonical direction for decision↔contract relation.
4. separate decision authority from consumer obligations; resolve `allowed_scopes`.
5. define the scope of decisions registered in AUTHORITY_REGISTRY.
6. bind contract versions to immutable normative content.
7. namespace state/status fields by record type.
8. move SPEC/M0/ACTIVE canonicality out of README into implementation/control state.
9. manifest ACCEPTED requires immutable acceptance evidence.
10. type dependency edges sufficiently for invalidation.
11. distinguish generic invariant from case-bound assertion.
12. reconcile PROCESS/BUILD owners with the frozen "one owning submodule" wording.
13. ACCEPTANCE_MODEL owns verdict semantics; AUDIT owns procedure.
14. fixture index points to baseline/assertion records; does not embed them as authority.
15. coverage ledger references state, does not duplicate it.
16. owners in coverage/assertions are registered typed IDs, not free text.
17. rule records reference decisions/assertions; they do not duplicate governing contract/fixture/check authority.
18. immutable packet supersession is recorded externally, never by editing old packet.
19. experiment vs packet shared/per-run metadata is separated.
20. control-plane version lives in implementation manifest and is snapshotted by evidence.
21. typed cross-reference ID namespaces exist before automated lint.

---

# 33. Requested DeepSeek response

Do not rewrite Phase 0 yet.

Respond to items 1–21 above using:

```text
ITEM
POSITION: ACCEPT | REJECT | PARTIAL | NEEDS DESIGN
CANONICAL OWNER:
DERIVED / SNAPSHOT LOCATIONS:
CONFLICT RULE:
CONSEQUENCE:
```

For any rejection, cite the frozen architecture/workflow/protocol that requires a different authority.

The purpose is to make the subsequent rewrite mostly mechanical: once authority ownership is settled, prose/file refactoring should stop being a design debate.
