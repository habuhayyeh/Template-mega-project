# 021A — Adversarial line-by-line review: BUILD_LINT.md

## Verdict

**NOT FREEZEABLE.**

The concept of a package-level authority/conflict gate is correct. The present file overstates what can be mechanically detected, conflicts with the frozen PROSE_POLICY control mode, and lacks the registries/conditions needed for its own rules to be meaningful.

The review below challenges every substantive claim rather than assuming the intended mechanism works.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 1 | "what the compiler refuses" | OVERCLAIM | There is no compiler/lint implementation yet. Is this a specification for a future compiler or an active control? Name the state explicitly. |
| 3 | deployment package assembled from many files | SOUND, BUT UNGROUNDED STATE | True as design intent, but the package manifest/dependency graph does not yet exist in Phase 0. What defines the package membership? |
| 3 | lint runs on every build | CURRENTLY FALSE OPERATIONALLY | No executable lint exists. Either implement a minimal lint before Phase 1 depends on it or call this a future enforcement specification/manual gate. |
| 3 | fails build on any violation | CONDITIONAL | Fine once a build/lint exists. Define whether draft authoring builds and acceptance builds have the same gate. |
| 3 | "only instrument that can see contradiction" | FALSE / OVERCLAIM | A semantic reviewer can see prose-policy contradictions that structured metadata cannot prove. BUILD can be the automated package-level gate, not the only possible detector. |
| 7 | lint does not scan prose | MAJOR CONFLICT | Frozen architecture deliberately uses PROSE_POLICY for S1/S2/I3/R2. If prose is normative, BUILD cannot simply ignore it. |
| 7 | every normative statement is a rule record | POTENTIALLY SOUND ONLY AS METADATA | A rule record may wrap/reference authoritative prose/DSL. It cannot require all nuanced semantic policy to collapse into modality/subject/object. Defend the intended representation. |
| 10 | rule id | SOUND | Needs registry/version uniqueness rules. Is uniqueness package-wide, contract-wide, or branch-wide? |
| 11 | decision id | SOUND IN PRINCIPLE | A self-assigned decision id cannot catch a conflict if two authors name the same semantic decision differently. A canonical decision registry is required. |
| 12 | owner_contract | SOUND IN PRINCIPLE | Owner must be looked up from an authority registry, not trusted because each rule self-declares it. |
| 13 | scope only at module family level | TOO COARSE | Frozen boundaries are I1–R3. A rule can be valid for R1 and invalid for R3 while both are RENDER. Why is scope not at least submodule-capable? |
| 14-17 | normative modality/subject/object | UNDERSPECIFIED | Clinical rules are conditional and often not reducible to this tuple. Where is applicability/condition? Where is payload reference for prose policy? |
| 15 | modality list | INCOMPLETE SEMANTICS | MUST vs ALLOWED are not contradictory; MUST_FIRST/MUST_AFTER need compatibility semantics. A difference in enum values is not equivalent to incompatibility. |
| 18 | fixture direct reference | WEAK TRACEABILITY | A fixture reference does not prove this rule is tested by that fixture. The example F-02 is unrelated to AP ordering and demonstrates the problem. |
| 19 | check direct reference | WEAK TRACEABILITY | Same issue. Prefer RULE/DECISION -> ASSERTION_ID -> deciding check/audit -> fixture/case. |
| 22 | required fields | INCOMPLETE | Missing applicability/condition, control mode, authoritative payload/reference, and traceability to assertion(s). At minimum defend why these are unnecessary. |
| 22 | fixture/check optional | INTERNALLY ODD | L4 fails a rule with neither. If at least one is mandatory for compiled rules, the schema should say so or distinguish draft vs compiled state. |
| 24 | fields are frozen and machine-readable | PREMATURE FREEZE RISK | Exact downstream rule schema was not previously frozen. Phase 0 may define required metadata classes, but justify freezing this exact field set before Phase 1 exposes needs. |
| 30 | same decision + comparable + differ = contradiction | FALSE AS WRITTEN | Different values are not always incompatible. MUST and ALLOWED can coexist. Contradiction requires an explicit compatibility relation plus overlapping applicability. |
| 32 | "comparable" means both cannot hold | NOT MACHINE-SPECIFIED | This sentence describes the desired semantic test, not an implementable one. How does the machine know two rules cannot both hold? |
| 32 | MUST_FIRST vs MUST_AFTER example | CONDITIONALLY VALID | Contradictory only if they govern the same items under overlapping conditions. Applicability is absent. |
| 34 | rewording same requirement not contradiction | SOUND INTENT, UNSPECIFIED MECHANISM | If authoritative payload can be prose, semantic equivalence cannot be mechanically established by string inequality. What detects equivalence? |
| 36 | "Unresolved authority" | MISNAMED | Lines 38-40 describe unresolved compatibility, not authority. Authority is L2. Rename or explain. |
| 38 | same decision, noncomparable fields => block | MAY BE TOO BROAD | One decision id may legitimately contain orthogonal subrules unless decision ids are guaranteed atomic. That guarantee is not defined. |
| 40 | ambiguity resolves arbitrarily at runtime | OVERCLAIM | It may resolve arbitrarily, sequentially, or one clause may dominate. The reason to block is that compatibility is not established, not that arbitrary runtime resolution is proven. |
| 42-46 | duplicate authority | GOOD PRINCIPLE, MISSING SOURCE OF TRUTH | The owner_contract fields are self-declared. What canonical registry says who actually owns a decision? |
| 46 | exactly one owner per decision | SOUND IF DECISION IS ATOMIC | Needs explicit decision registry and inheritance rules. |
| 48-50 | orphan decision | SOUND, DEPENDENCY MISSING | Cannot evaluate "owner no longer exists" without a contract registry/status ledger. |
| 52-56 | out-of-scope rule | IMPORTANT BUT NOT MECHANICAL AS WRITTEN | A machine cannot infer that arbitrary prose "selects content." Either L3 is semantic BUILD review, or decision ids carry allowed owner/scope metadata that can be checked mechanically. |
| 58 | SHARED may define vocabulary but not per-module instructions | PROBABLY TOO RESTRICTIVE | Shared ordering/style/source-fidelity contracts may legitimately provide structured policy consumed by specific modules. Distinguish "shared authority" from "issuing a neighboring module's decision." |
| 60-62 | untested = no fixture/check pointer | INSUFFICIENT | This proves only that a pointer exists. It does not prove the rule is exercised. Require assertion-level coverage/traceability. |
| 64-66 | dangling reference | SOUND | Define whether historical references to withdrawn fixtures are illegal only in current compiled acceptance artifacts, not archival reviews. |
| 68-70 | conflict marker | SOUND | Mechanical and useful. |
| 72-85 | every violation fails | MOSTLY SOUND FOR ACCEPTANCE BUILD | Need lifecycle state: should an incomplete draft contract fail a working/draft lint or only be unfreezable? Avoid making normal authoring impossible. |
| 89-101 | sample output | POTENTIALLY MISLEADING | Counts look factual but are illustrative. Label the entire output explicitly illustrative. |
| 103 | localises, does not explain | REASONABLE | For semantic/manual L3/L1c findings, enough evidence must still be surfaced to permit review. |
| 107 | not clinical-rightness checker | SOUND | Keep. |
| 108 | no repair/suggest/downgrade | SOUND FOR ENFORCEMENT | A separate diagnostic report may suggest; the gate itself should not silently repair. |
| 109 | prose not rule-record = documentation and not compiled | CRITICAL CONFLICT | This deletes the frozen PROSE_POLICY control mode unless rule records can reference normative prose payloads. Must be redesigned or defended. |
| 111-113 | runs every contract commit/build/acceptance | CURRENTLY PAPER CONTROL | There is no enforcement implementation. Define temporary manual gate or implement minimal lint before multiple Phase 1 contracts exist. |

## Missing concepts that appear necessary

1. **Canonical decision registry**
   - DECISION_ID
   - semantic question governed
   - authoritative owner contract/submodule
   - allowed scope
   - status/version
   - dependencies

2. **Applicability/condition**
   - otherwise compatible conditional rules false-positive as contradictions.

3. **Normative payload reference**
   - structured metadata may point to precise prose, DSL, or operator definition.

4. **Control mode**
   - LLM_JUDGMENT / PROSE_POLICY / TYPED_DSL / CANONICAL_OPERATOR / MECHANICAL_RULE.

5. **Assertion traceability**
   - RULE/DECISION -> ASSERTION_ID -> deciding validator/audit -> fixture/case.

6. **Lifecycle state**
   - draft rule vs compiled/frozen rule.

## DeepSeek must answer

Do not patch first. Defend:
- how PROSE_POLICY survives line 109;
- how L1 knows incompatibility rather than mere difference;
- how conditions are represented;
- how decision identity/ownership is established independently of self-declared fields;
- how L3 is mechanically decidable;
- how L4 proves actual coverage;
- what enforces the lint before Phase 1.
