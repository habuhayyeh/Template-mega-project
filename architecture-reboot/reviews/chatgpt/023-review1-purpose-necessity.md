# ChatGPT review 023 — Review 1: Purpose / Necessity of Phase 0

## Review type

**Purpose / Necessity Review**

This review does not ask whether the current prose is correct.

It asks a more basic question:

> **Why does each Phase 0 artifact exist at all? What unique question does it answer? What capability disappears if it is deleted? Can another authority answer the same question without loss?**

A Phase 0 file is justified only if it owns a distinct kind of authority, state, evidence, procedure, or reusable template.

The objective is not fewer files for its own sake.

The objective is:

> **one authoritative home per kind of question, with no duplicated ownership and no missing authority.**

---

# Executive verdict

The rebuild is materially better than the original five-file Phase 0, but the current decomposition is still not the right final information architecture.

Current files:

1. README.md
2. REGISTRIES.md
3. PACKET.md
4. OBLIGATIONS.md
5. BUILD_LINT.md
6. AUDIT_PROTOCOL.md
7. ACCEPTANCE_BRIEF_TEMPLATE.md
8. CHANGE_CONTROL.md
9. FIXTURE_REGISTER.md

My verdict:

| File | Necessary concept? | Current file boundary? | Recommendation |
|---|---:|---:|---|
| README.md | YES | mostly correct | KEEP, reduce to navigation only |
| REGISTRIES.md | YES | overloaded | SPLIT operational state from normative authority |
| PACKET.md | YES + YES | wrong combination | SPLIT acceptance packet from change ledger |
| OBLIGATIONS.md | YES | wrong name / incomplete role | EVOLVE into COVERAGE_LEDGER |
| BUILD_LINT.md | YES | too narrow | KEEP concept, evolve to BUILD_SPEC |
| AUDIT_PROTOCOL.md | YES | necessary but only half the validation authority | KEEP, likely under VALIDATION_PROTOCOL |
| ACCEPTANCE_BRIEF_TEMPLATE.md | YES as tool | not a core authority | MOVE to templates; strip policy |
| CHANGE_CONTROL.md | YES | distinct authority | KEEP, narrow to classification/approval/invalidation |
| FIXTURE_REGISTER.md | YES as index | still overloaded | KEEP AS INDEX, move assertions/taxonomy elsewhere |

**Missing distinct authority:**
- ACCEPTANCE / ASSERTION MODEL
- experiment-level manifest / evidence record
- architecture coverage ledger (best merged with obligations)
- explicit change-ledger artifact
- perhaps control-plane version authority, preferably inside manifest rather than another file

---

# The deletion test

For each file:

> If I delete this file and move none of its content elsewhere, what unique capability is lost?

If no unique capability is lost, the file is redundant.

If several unrelated capabilities disappear, the file is overloaded.

---

# 1. README.md

## Current purpose

The rebuilt README currently owns:
- Phase 0 description;
- lifecycle states SPEC/M0/ACTIVE;
- authority index;
- control-state table;
- Phase 0 self-governance statement;
- exclusions.

## Deletion test

If README disappears:
- the underlying controls still exist;
- their rules still exist;
- registries still exist;
- acceptance can still function.

What is lost is **navigation and orientation**, not governance.

That is exactly what a README should be.

## Necessity verdict

**KEEP.**

But it must remain a **map**, not a second control plane.

## What it should own

Only:
- what Phase 0 is;
- where each authority lives;
- current control-plane version;
- which document is authoritative for lifecycle;
- which artifacts are SPEC/M0/ACTIVE by pointer;
- navigation to frozen upstream architecture/workflow/experiment protocol.

## What it should not own

It should not define:
- acceptance semantics;
- change categories;
- artifact lifecycle transitions;
- fixture rules;
- build rules;
- audit rules.

If a normative sentence in README is necessary for correctness, it probably belongs somewhere else.

## Result

**KEEP BUT NARROW.**

---

# 2. REGISTRIES.md

## Current purpose

It contains three registries:

1. decision registry;
2. contract registry;
3. implementation manifest.

DeepSeek added all three because they were genuinely missing.

All three concepts are necessary.

The question is whether they belong in **one file**.

## Deletion test

Delete the decision registry:
- decision ownership becomes self-declared by rules;
- BUILD cannot reliably enforce L2/L3;
- decision authority becomes ambiguous.

**Necessary.**

Delete the contract registry:
- decision ownership cannot point to stable contract identities/versions;
- contract changes cannot be versioned cleanly;
- path moves become semantically ambiguous.

**Necessary.**

Delete the implementation manifest:
- no authoritative current artifact state;
- no dependency graph;
- no readiness/invalidation basis;
- CHANGE_CONTROL cannot know dependents.

**Necessary.**

So all three authorities are real.

## But they have different mutation characteristics

### Decision registry
Slow-changing, normative.

Question answered:

> **Who owns this decision?**

### Contract registry
Slow-changing, normative/version authority.

Question answered:

> **What authoritative contract/version defines that decision?**

### Implementation manifest
Fast-changing operational state.

Question answered:

> **What currently exists, what version is it, what depends on it, and what state is it in?**

These are not the same type of data.

## Important duplication inside the current structure

Decision registry says:

`owner_contract: X`

Contract registry says:

`owns_decisions: [A, B, C]`

That encodes the same relationship twice.

Those two lists can disagree.

A control plane should not store a bidirectional relation as two independently editable authorities.

One direction must be canonical; the other is derived.

## Recommendation

### Keep together:
- **Decision registry**
- **Contract registry**

They are tightly coupled normative authority and may reasonably live in:

> `AUTHORITY_REGISTRY`

or current `REGISTRIES.md`.

But choose **one canonical direction** for contract↔decision ownership.

### Split out:
- **Implementation manifest**

into its own authority:

> `IMPLEMENTATION_MANIFEST`

because it is state, not contract semantics.

This also reduces churn: every implementation-state update should not edit the normative authority registry.

## Result

**SPLIT.**

---

# 3. PACKET.md

## Current purpose

It currently contains:

1. acceptance packet;
2. change ledger;
3. no-retroactive-rescoring rule;
4. DISCOVERY behavior.

This is the clearest example of two unrelated authorities being packed together.

## §1 Acceptance packet

Unique question:

> **Exactly what evidence/version/environment was scored in this acceptance event?**

This is necessary.

It binds:
- run;
- case;
- model/mode;
- package;
- contract versions;
- brief;
- assertion set;
- baseline;
- evidence hashes;
- check;
- audit;
- verdict.

Nothing else currently answers this.

**KEEP concept.**

## §2 Change ledger

Unique question:

> **What governed project change occurred, under which category, why, and who approved it?**

This is also necessary.

But it has nothing conceptually to do with a Doximity run packet.

Acceptance events and project changes have different lifecycles.

A project can undergo ten governed changes with no acceptance run.

A batch can produce 30 packets with no project change.

## §3 no retroactive rescoring

This is primarily **change/acceptance governance**.

It should be defined by CHANGE_CONTROL / ACCEPTANCE MODEL, while each packet preserves the evidence needed to enforce it.

PACKET may reference the rule; it should not be its primary policy authority.

## §4 DISCOVERY

This belongs to the **acceptance/assertion model** and validation governance.

A packet records a discovery.
It should not be the authority defining what DISCOVERY means.

## Recommendation

Split into:

### A. `ACCEPTANCE_PACKET_SPEC`
Owns:
- packet schema;
- experiment/run identity references;
- evidence hashes;
- result references;
- immutability/version binding.

### B. `CHANGE_LEDGER`
Owns:
- append-only change records.

The **policy** governing those records remains `CHANGE_CONTROL.md`.

### C. DISCOVERY semantics
Move to the missing `ACCEPTANCE_MODEL` / validation protocol.

## Result

**SPLIT.**

---

# 4. OBLIGATIONS.md

## Current purpose

DeepSeek created this to keep the blind spots from review 022 from disappearing.

That is a real and important function.

Question answered:

> **What architecture/control obligation is still owed, by whom, after which prerequisite, and what future test closes it?**

Without it, downstream requirements vanish between phases.

So the concept is necessary.

## But "obligation ledger" is only half of what we need

It currently tracks open duties.

What we ultimately need is:

> **architecture invariant → decision/contract → assertion → fixture → validator → acceptance evidence → status**

That is a **coverage ledger**, not merely a backlog.

Once an obligation closes, we should not lose it.

Example:

`test-mode vs production equivalence`

After it is eventually tested, the important information is not just:

> CLOSED

It is:

- which invariant it covers;
- which assertion decided it;
- which experiment closed it;
- which package/version it applies to.

## Duplication risk

If we create a separate COVERAGE_LEDGER while keeping OBLIGATIONS unchanged, they will duplicate status/owner/test information.

## Recommendation

Do not add another file beside OBLIGATIONS.

**Transform OBLIGATIONS into the architecture coverage authority.**

Possible concept:

> `COVERAGE_LEDGER`

It contains both:

### OPEN obligations
- owner;
- prerequisite;
- future closing test.

### CLOSED coverage
- controlling contract;
- assertion;
- fixture;
- validator;
- accepted evidence/version.

This solves both:
- blind-spot retention;
- invariant coverage.

## Result

**KEEP THE CONCEPT, MERGE/EVOLVE INTO COVERAGE_LEDGER.**

---

# 5. BUILD_LINT.md

## Current purpose

It specifies what prevents invalid/contradictory/unowned rules from entering the deployment build.

This is a unique responsibility.

Question answered:

> **Can these modular authoritative sources be compiled into one internally valid deployment package?**

No other current file owns that.

Therefore BUILD is necessary.

## But "lint" is narrower than the actual build responsibility

The architecture needs BUILD to eventually own:

- discovery of active source authorities;
- rule metadata validation;
- authority/scope validation;
- contradiction/unresolved checks;
- dependency integrity;
- source payload hashing;
- package assembly;
- canonical package order;
- source→package traceability;
- package identity/hash.

Current BUILD_LINT covers only part of that.

Other build obligations are currently parked in OBLIGATIONS.

If later we create:
- BUILD_LINT;
- PACKAGE_COMPILER_SPEC;
- PACKAGE_TRACEABILITY_SPEC;
- PACKAGE_ORDER_SPEC;

we risk unnecessary fragmentation.

## Recommendation

Keep one distinct build authority:

> **`BUILD_SPEC`**

with sections:
1. source/rule discovery;
2. lint;
3. compilation;
4. canonical ordering;
5. traceability/hash;
6. build outputs;
7. manual M0 gate until instrumentation exists.

The executable lint/compiler can later be separate programs; the authority need not be split.

## Result

**KEEP, BROADEN/RENAME.**

---

# 6. AUDIT_PROTOCOL.md

## Current purpose

Unique question:

> **How is semantic correctness judged when a mechanical checker cannot establish it?**

This absolutely needs a distinct authority.

The architecture explicitly separates semantic AUDIT from mechanical CHECK.

So deleting AUDIT would destroy a fundamental design boundary.

## Is AUDIT enough as the whole validation authority?

No.

The system also needs a canonical definition of:

- MECHANICAL;
- SEMANTIC_AUDIT;
- HYBRID;
- required vs optional assertions;
- PASS/FAIL/BLOCKED;
- scorer independence;
- evidence sufficiency;
- discovery handling;
- severity;
- assertion prerequisites.

Some currently appear in AUDIT.
Some appear in fixtures.
Some appear in PACKET.
Some appear nowhere.

This suggests a higher-level **validation/acceptance model** is missing.

## Two possible decompositions

### Option A — keep AUDIT_PROTOCOL distinct

- `ACCEPTANCE_MODEL` defines assertion semantics/modes/results.
- `AUDIT_PROTOCOL` defines how humans/LLMs perform SEMANTIC_AUDIT.
- mechanical CHECK specs appear downstream.

This is my preferred option.

### Option B — rename to VALIDATION_PROTOCOL

One file defines both:
- mechanical-check governance;
- semantic-audit governance.

This risks becoming too broad.

Because CHECK and AUDIT are architecturally distinct, I prefer Option A.

## Result

**KEEP AUDIT_PROTOCOL as a distinct procedural authority, but create ACCEPTANCE_MODEL above it.**

---

# 7. ACCEPTANCE_BRIEF_TEMPLATE.md

## Current purpose

Operational question:

> **Before implementation starts, what small packet tells the engineer exactly what this artifact must satisfy?**

That tool is useful.

But this file should not be a core authority.

A template should instantiate rules defined elsewhere.

## Deletion test

If the template is deleted but the Acceptance Model, contract references, fixtures and workflow remain:
- correctness semantics still exist;
- the workflow could still create briefs manually.

What is lost is consistency/convenience, not governance.

Therefore this is not a peer authority like CHANGE_CONTROL.

## Current duplication

The template currently defines or repeats:
- what counts as a property;
- validation modes;
- failure behavior examples;
- fixture rules;
- acceptance-change behavior.

Those should be owned elsewhere.

## Recommendation

Move to:

> `phase0/templates/ACCEPTANCE_BRIEF.md`

Make it almost form-like.

It should contain references, not policy.

For example:
- artifact/version;
- contract refs;
- assertion refs;
- fixture refs;
- expected failure-state refs.

Even the current "five fields, no more" should be treated as template guidance, not a governance invariant unless justified.

## Result

**KEEP AS TEMPLATE, REMOVE AS CORE AUTHORITY.**

---

# 8. CHANGE_CONTROL.md

## Current purpose

Unique question:

> **What kind of change is this, who must approve it, what evidence becomes stale, and what must be rerun?**

This is clearly independent from:
- BUILD;
- validation;
- fixtures;
- acceptance packets.

It deserves its own authority.

## Deletion test

Without it:
- goalposts can move;
- implementation changes can masquerade as patches;
- baseline changes can retroactively reinterpret runs;
- dependent acceptance evidence can remain falsely valid.

Nothing else fully replaces it.

## What should leave CHANGE_CONTROL

It should not be the storage location for change history.

It defines **policy**.

A separate `CHANGE_LEDGER` records instances.

It also should not own detailed fixture mutation history; fixture/assertion versions record their own lineage, while the change ledger records the governed event.

## Result

**KEEP DISTINCT, NARROW TO POLICY.**

---

# 9. FIXTURE_REGISTER.md

## Current purpose

It claims to be an index, but it still contains:

- failure taxonomy;
- historical observations;
- evidence;
- evidence boundaries;
- assertions;
- prerequisites;
- severity;
- fixture lifecycle;
- derived-fixture rules.

That is still too much.

## The necessary concept

We absolutely need an authority answering:

> **What reference cases / historical failures / probes exist, where is their evidence, and what version/status is current?**

So a fixture index is necessary.

## But assertions are not fixtures

A fixture is evidence/input.

An assertion is a proposition about what should happen.

One fixture may support:
- 3 assertions today;
- 5 assertions later;
- assertions owned by several seams.

One assertion may be exercised by:
- several fixtures;
- several signer cases.

Embedding assertions inside the fixture index creates a many-to-many relationship inside narrative prose.

That will not scale to the signer's 10-note corpus.

## Failure classes also do not belong here as primary authority

F1/F2/C11 etc are useful tags.

But if they govern:
- severity;
- failure behavior;
- brief behavior;
- audit classification;

their canonical definition belongs in the Acceptance Model / failure vocabulary, not the fixture index.

## Recommendation

Keep:

> **`FIXTURE_INDEX`**

with:
- fixture id;
- type;
- version;
- status;
- source/evidence pointer;
- baseline packet pointer;
- evidence boundary;
- assertion-set pointer;
- tags/failure-class refs.

Move assertion definitions to a separate authority.

## Result

**KEEP AS INDEX, REMOVE ASSERTION/POLICY OWNERSHIP.**

---

# 10. Missing: ACCEPTANCE_MODEL / ASSERTION AUTHORITY

This is now the most important missing authority in the rebuild.

DeepSeek added an "assertion set version" to PACKET and speaks of "ACTIVE assertions" in BUILD.

But:

> **Where is an assertion actually defined?**

No current file cleanly owns that.

FIXTURE_REGISTER contains ad hoc assertions.
ACCEPTANCE_BRIEF says properties/checks.
AUDIT consumes assertions.
PACKET versions assertion sets.
BUILD requires ACTIVE assertions.

The whole control plane depends on a thing for which no canonical schema/authority exists.

## Unique question

> **What does one acceptance assertion mean and what metadata makes it valid/scorable?**

Recommended canonical fields conceptually:

- ASSERTION_ID;
- VERSION;
- OWNER;
- PROPERTY;
- VALIDATION_MODE;
- SEVERITY;
- REQUIRED_EVIDENCE;
- PREREQUISITE_CONTRACTS;
- STATUS;
- DECIDING_CHECK/AUDIT;
- allowed failure/disposition semantics where relevant.

Run result is **not** part of the assertion definition.

## Why this must be distinct

It connects:
- architecture;
- contracts;
- fixtures;
- briefs;
- audit;
- mechanical checks;
- experiments.

Nothing else should own correctness semantics.

## Result

**ADD — ESSENTIAL.**

---

# 11. Missing: experiment-level manifest / evidence record

PACKET is per acceptance packet/run/case.

But the frozen Doximity protocol is experiment-level:

- one batch;
- 8–12 cases;
- same-order repetitions;
- order perturbation;
- single-case controls;
- A/B implementation comparison.

A set of independent case packets does not fully describe:

> **What experiment did we run?**

## Unique question

> What exact campaign/batch/repetition/A-B condition produced these packets?

Needed concepts:
- EXPERIMENT_ID;
- purpose/type A/B/C/D;
- package version/hash;
- source batch version;
- baseline/assertion-set versions;
- case order;
- model/mode;
- production/test mode;
- repetition ids;
- raw output hashes;
- packet ids;
- scorers;
- experiment verdict.

## Recommendation

Do not create another experimental policy file.

The protocol is already frozen elsewhere.

Add a **template/schema**:

> `templates/EXPERIMENT_MANIFEST`

This implements the protocol.

## Result

**ADD AS TEMPLATE/RECORD SCHEMA — NECESSARY BEFORE REAL BATCH ACCEPTANCE.**

---

# 12. Missing / transform: architecture coverage authority

As discussed under OBLIGATIONS, we need one place answering:

> **For each frozen architecture invariant, what proves it is covered?**

OBLIGATIONS should evolve into this rather than adding another parallel ledger.

## Result

**TRANSFORM OBLIGATIONS → COVERAGE_LEDGER.**

---

# 13. Missing: dedicated CHANGE_LEDGER artifact

DeepSeek has correctly declared root `CHANGELOG.md` to be old-pipeline history inside PACKET.

But current CHANGE_CONTROL still refers to `CHANGELOG.md`.

Even ignoring that inconsistency, a change ledger is data, not the same thing as the acceptance packet spec.

## Recommendation

Create:

> `architecture-reboot/CHANGE_LEDGER`

or Phase 0-local equivalent.

CHANGE_CONTROL defines what must be logged.
CHANGE_LEDGER stores the append-only records.

## Result

**ADD / SPLIT FROM PACKET.**

---

# 14. Do we need a separate FAILURE_CATALOG?

Current fixture register contains F1-F10/C11-C14.

A separate failure-taxonomy file is tempting.

I do **not** recommend adding it yet.

Reason:

Failure classes are useful tags, but another file creates one more authority unless they become complex enough to justify it.

For now:
- canonical failure/severity/result vocabulary can live in **ACCEPTANCE_MODEL**;
- fixtures reference those codes.

If the taxonomy later grows into a substantial ontology, split it then.

## Result

**DO NOT ADD YET.**

---

# 15. Do we need a separate SEAM_MATRIX file?

The architecture blind-spot review says yes to seam coverage.

But a separate seam file now would duplicate the coverage ledger.

Put seam rows in COVERAGE_LEDGER:
- producer;
- consumer;
- guarantees;
- assumptions;
- assertions;
- status.

Split only if it becomes unmanageable.

## Result

**DO NOT ADD YET — INCLUDE IN COVERAGE_LEDGER.**

---

# 16. Do we need a separate FAILURE_PROPAGATION file?

Same answer.

The decisions are important but exact runtime semantics belong to downstream failure/shared contracts.

Phase 0 needs to track the obligation and coverage.

Use COVERAGE_LEDGER until the Phase 1 failure contract exists.

## Result

**DO NOT ADD YET.**

---

# 17. Proposed minimal authority architecture

I recommend the Phase 0 control plane converge toward these **eight distinct authorities**:

## A. AUTHORITY_REGISTRY
Question:
> Who owns each decision and which contract/version governs it?

Contains:
- decision registry;
- contract registry.

Not operational state.

---

## B. IMPLEMENTATION_MANIFEST
Question:
> What currently exists, what depends on what, and what readiness/version state is it in?

Operational state only.

---

## C. ACCEPTANCE_MODEL
Question:
> What is a valid assertion and how is correctness represented?

Owns:
- assertion schema;
- validation modes;
- severity;
- assertion status/prerequisites;
- result/discovery vocabulary.

---

## D. FIXTURE_INDEX
Question:
> What evidence/reference cases exist and where are their versioned packets?

No assertion policy.

---

## E. COVERAGE_LEDGER
Question:
> Which architecture obligations are covered, pending, or closed, and by what proof?

Absorbs OBLIGATIONS.

---

## F. BUILD_SPEC
Question:
> How do authoritative modular sources become one valid, traceable deployment package?

Includes lint + compile + traceability.

---

## G. VALIDATION GOVERNANCE
Two pieces may remain:
- ACCEPTANCE_MODEL: semantics of assertions/results;
- AUDIT_PROTOCOL: human/LLM semantic-audit procedure.

Do not force these into one file if that obscures the CHECK/AUDIT architectural distinction.

---

## H. CHANGE_CONTROL
Question:
> How may any of these authorities or implementations change, and what evidence must be invalidated/re-run?

Distinct policy.

---

# Supporting records/templates, not authorities

- README — navigation.
- ACCEPTANCE_BRIEF template.
- ACCEPTANCE_PACKET spec/template.
- EXPERIMENT_MANIFEST template.
- CHANGE_LEDGER — append-only record.
- per-case baseline/assertion packets.
- raw experiment outputs/scores.

These are essential operational artifacts but should not each become another source of policy.

---

# 18. Proposed file layout

Conceptually:

```text
architecture-reboot/phase0/

README.md

AUTHORITY_REGISTRY.yaml/md
IMPLEMENTATION_MANIFEST.yaml/md
ACCEPTANCE_MODEL.md
FIXTURE_INDEX.md
COVERAGE_LEDGER.md

BUILD_SPEC.md
AUDIT_PROTOCOL.md
CHANGE_CONTROL.md

templates/
  ACCEPTANCE_BRIEF.md
  ACCEPTANCE_PACKET.md
  EXPERIMENT_MANIFEST.md

records/
  CHANGE_LEDGER.md
```

Exact serialization is not the point of this review.

The authority boundaries are.

---

# 19. What should happen to the current rebuilt files

| Current | Action |
|---|---|
| README.md | KEEP, narrow |
| REGISTRIES.md | SPLIT: authority registry + implementation manifest |
| PACKET.md | SPLIT: packet spec + change ledger; move policy elsewhere |
| OBLIGATIONS.md | EVOLVE/MERGE into coverage ledger |
| BUILD_LINT.md | EVOLVE into build spec |
| AUDIT_PROTOCOL.md | KEEP |
| ACCEPTANCE_BRIEF_TEMPLATE.md | MOVE to templates and strip policy |
| CHANGE_CONTROL.md | KEEP, narrow |
| FIXTURE_REGISTER.md | EVOLVE to fixture index; move assertions/taxonomy |

Add:
- ACCEPTANCE_MODEL
- EXPERIMENT_MANIFEST template
- dedicated CHANGE_LEDGER

---

# 20. Hard criterion for every Phase 0 file

Before a file survives Review 1, it must answer this sentence in one line:

> **This file is the sole authority for ________.**

If two files fill the blank with the same thing, merge/narrow them.

If no file can fill an important blank, add an authority.

If a file needs three unrelated phrases in the blank, split it.

Examples:

- AUTHORITY_REGISTRY:
  > sole authority for decision ownership and governing contract identity.

- IMPLEMENTATION_MANIFEST:
  > sole authority for current artifact version/dependency/readiness state.

- ACCEPTANCE_MODEL:
  > sole authority for assertion semantics, validation mode, severity and assertion lifecycle.

- FIXTURE_INDEX:
  > sole authority for fixture identity/version/status/evidence pointer.

- COVERAGE_LEDGER:
  > sole authority for architecture-obligation coverage state.

- BUILD_SPEC:
  > sole authority for source-to-deployment build validity.

- AUDIT_PROTOCOL:
  > sole authority for semantic-audit procedure.

- CHANGE_CONTROL:
  > sole authority for change classification, approval and invalidation policy.

That is the clean decomposition I would trust.

---

# 21. DeepSeek challenge

Before rewriting files, respond to each current-file verdict and each proposed authority with:

```text
ITEM
POSITION: KEEP | SPLIT | MERGE | MOVE | DELETE | ADD | REJECT
UNIQUE QUESTION IT OWNS:
WHAT BREAKS IF REMOVED:
WHAT CURRENT FILE(S) DUPLICATE IT:
PROPOSED FINAL HOME:
```

I specifically want challenges to:
- splitting REGISTRIES;
- splitting PACKET;
- replacing OBLIGATIONS with COVERAGE_LEDGER;
- adding ACCEPTANCE_MODEL;
- keeping AUDIT separate from acceptance semantics;
- moving ACCEPTANCE_BRIEF to templates;
- shrinking FIXTURE_REGISTER to an index.

Do not rewrite Phase 0 until the authority decomposition itself is agreed.
