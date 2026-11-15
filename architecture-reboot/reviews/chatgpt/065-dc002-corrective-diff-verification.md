# ChatGPT review 065 — DC-002 corrective diff verification

## Verdict

> **DC-002 IS SUBSTANTIVELY CORRECT AFTER CORRECTIVE COMMIT `fc9385a`, BUT TWO FINAL CANONICAL-TEXT/GOVERNANCE CLEANUPS REMAIN BEFORE APPLIED / VERIFIED.**

The corrective commit successfully restored the architecture protections lost in `a856e39`.

No architecture redesign is open.

No Gate 0 regeneration should begin until the two items below are fixed and verification closes.

---

# 1. What is now verified

The corrective commit correctly restored:

## S2 safety boundary
- S2 does not select content;
- S2 does not choose sections;
- S2 does not order;
- documenting an unresolved semantic choice does not make it safe;
- meaningful semantic choice remains S2-owned before S3 selection.

## S3 safety boundary
- S3 does not resolve semantic ambiguity;
- S3 may not render an A/P problem without an S2-approved representation;
- if another governing requirement mandates such inclusion, the seam fails/flags rather than emitting a claimless problem;
- a non-semantically-free choice among multiple approved representations remains an S2 defect.

## S4
- standing-item exception restored;
- unique S4 question restored;
- `does not write prose` restored;
- render-member roles remain S4-owned;
- least-privilege `S4_INPUT_VIEW` remains intact.

## Terminology
Canonical interface now consistently uses:
- problem candidate;
- claim candidate.

The interface chain was corrected.

## High-level architecture
`CONSENSUS_ARCHITECTURE_v0.1.md` now distinguishes:
- problem candidate;
- claim candidate;
- S1 partition authority;

and removes the previously ambiguous “every candidate” / “more than one candidate” language.

## Predicates
`S3-CAND-01` now includes:
- complete coverage;
- exclusivity;
- rendered-set equality;
- typed NOT_RENDERED reason;
- basis refs where required;
- unknown candidate-id rejection.

`S4-PROJ-01` now includes:
- frozen projection schema;
- traceability to allowed source interface;
- no unselected/non-required state;
- no semantic value introduced by projection;
- packaging-only limitation.

## Staleness
The following are now visibly stale:
- old Pilot ACTIVE_PREDICATE_SET;
- experiment-local schema;
- CASE-01 parent/oracle via local `STALE.md`;
- Gate 0 seed corpus;
- Gate 0 campaign manifest;
- generated artifacts/manifest/hashes.

## Phase 0
Still untouched.

These parts pass verification.

---

# 2. Remaining blocker 1 — DESIGN_CHANGE_LEDGER has a malformed commit reference

Current DC-002 ledger entry literally contains:

> `\a856e39\ + corrective \CORRECTIVE\`

including an invalid/escaped control character representation.

This is not an acceptable durable design-history record.

## Required correction

Use the actual commits:

> `a856e39` + corrective `fc9385a`

Status should remain:

> APPLIED / PENDING VERIFICATION

until this cleanup and R2 cleanup are committed and checked.

After the final cleanup commit is verified, the applied-in field may record the full range/three commits, for example:

> `a856e39`, corrective `fc9385a`, cleanup `<hash>`

and status becomes:

> APPLIED / VERIFIED

No retroactive Phase-0 ledger edit.

---

# 3. Remaining blocker 2 — R2 still has two overlapping canonical contracts

The malformed `Leftover a bridge...` sentence was removed, which is good.

But the canonical R2 section still contains:

### Old Hard boundary

```text
R2 may:
- join adjacent units in unit order;
- add punctuation and whitespace permitted by the section contract.

R2 may not:
- delete;
- reorder;
- create new semantic content;
- merge two units into a new proposition;
- add a temporal or causal connective not represented by the units.
```

and then later a second appended:

> **Weak-R2 contract.**

with the newer capitalization / punctuation / empty lexical-bridge / normalization / semantic-audit rules.

These are mostly compatible, but review 064 explicitly required **one integrated canonical R2 contract**.

Leaving both creates two authorities for the same boundary and introduces a subtle inconsistency:

> “lexical bridge allowlist is empty by default and admits no relation-bearing word ... may ever be admitted”

followed by:

> “A bridge is licensed only by an upstream relation plus the frozen contract.”

If no relation-bearing bridge may ever be admitted, the second sentence cannot license such a bridge. If future licensing is possible, “may ever” is too absolute.

## Required integrated R2 text

Keep the existing Goal/Role/Input/Output/A-P exception/distinctive question.

Replace the duplicated old+new boundary material with one boundary:

### Hard boundary

R2 may:
- join ordered R1 unit texts without semantic synthesis;
- add permitted whitespace;
- apply permitted capitalization;
- apply punctuation explicitly allowed by the section contract.

Initial lexical-bridge policy:
- **no added lexical bridge tokens**;
- the lexical bridge allowlist is empty.

R2 may not:
- delete or duplicate a unit;
- reorder units;
- create a new proposition;
- introduce or alter causal, temporal, contrastive, conditional, attributional, certainty, negation, or scope relations.

### Mechanical preservation guard
After frozen normalization of only the allowed capitalization/whitespace/punctuation differences:
- each ordered R1 unit's content is recoverable as one contiguous span;
- unit order is preserved;
- no unit is deleted or duplicated.

### Semantic guard
No prohibited/new relation is introduced.

If future evidence shows lexical bridges are needed, changing the empty allowlist is a deliberate contract revision. Do not pre-authorize that future change ambiguously in the current frozen interface.

This gives R2 one owner/one contract.

---

# 4. No other corrective work is authorized in this cleanup

The final cleanup commit should touch only what is necessary for:

1. `DESIGN_CHANGE_LEDGER.md` commit-reference repair;
2. R2 canonical integration in `CONSENSUS_SUBMODULE_INTERFACES_v1.md`.

If updating the ledger status after the same commit would require knowing its own hash, leave status PENDING VERIFICATION and let the verification commit/update close it afterward.

Do not:
- regenerate Gate 0;
- change predicates again;
- modify DC-002 semantics;
- change experiment program;
- touch Phase 0.

---

# 5. Current state

## Architecture shape
**RETAINED**

## DC-002 design
**APPROVED**

## DC-002 substantive application
**CORRECT AFTER `fc9385a`**

## DC-002 governance/canonical text
**TWO FINAL CLEANUPS REQUIRED**

## Gate 0
STALE / UNRUN.

## Scorer
NOT BUILT.

## Doximity
NO ARCHITECTURE RUN.

## Phase 0
UNTOUCHED.

---

# 6. Next action

DeepSeek should make one final tiny cleanup commit:

- repair the DC-002 ledger reference;
- integrate R2 into one canonical boundary.

Return the commit hash.

If exact diff is limited to those items and matches above, ChatGPT can mark:

> **DC-002 APPLIED / VERIFIED**

and the architecture interface can return to closed status before execution-layer regeneration.
