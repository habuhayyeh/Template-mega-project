# DeepSeek response 023 — Review 3, items A1–L1

Almost all accepted. Where I hold, it is noted.

| Item | Position | Upstream | Rewrite consequence |
|---|---|---|---|
| A1 F-11b/F-11c vs temporality | **ACCEPT** | §5 temporality ≠ adoption | F-11b: a historical-source object renders in plan **when adopted**; F-11c: plan members are adopted-current, not source-current |
| A2 PROSE_POLICY erased | **ALREADY FIXED BY R-2 TARGET** | control modes | `payload_ref` + embedded hash; the current sentence stays, the payload rule is added |
| A3 order authority leaks to RENDER | **ACCEPT** | S4 owns ordering | `AP_ORDER_WITHIN_PROBLEM.owner = S4`, `authority_scope = STRUCTURE`, RENDER only `obligated` |
| A4 COVERAGE_DISPOSITION too broad | **ACCEPT** | I2 accounts spans, S3 disposes objects | split into `SPAN_COVERAGE` (I2) and `OBJECT_DISPOSITION` (S3) |
| B1 AUDIT overstates CHECK | **ACCEPT** | CHECK is mechanical conformance to the IR | CHECK proves IR→note conformance only; semantic adequacy is AUDIT's |
| B2 no expected prose | **ACCEPT** | operator-fixed wording is contractual | bounded expected prose allowed where the operator fixes it |
| B3 signer escalation too broad | **ACCEPT** | workflow | contract + independent review first; signer for clinical/style/product |
| B4 trace acceptance not blocked | **ACCEPT** | protocol | trace runs are structurally non-scorable; packet rejects them |
| C1 packet too strong | **ACCEPT** | protocol repetition gates | experiment manifest decides experiment-level gates; a packet is per-run evidence |
| C2 production packet assumes IR | **ACCEPT** | production suppresses IR | `case_ir` optional; production packets carry note + hashes |
| C3 DISCOVERY as verdict | **ACCEPT** | — | `DISCOVERY` is a finding state, not a verdict value |
| D1 A-02a narrows reuse | **ACCEPT** | consensus #23 | restate as *unapproved* duplicate; approved reuse is explicit and passes |
| D2 A-02b too broad | **ACCEPT** | #23 | scope to the adjudicated duplicate relation, not global |
| D3 A-01a freezes normalisation | **ACCEPT** | normalisation table unfrozen | `PENDING_DEPENDENCY` |
| D4 A-01c depends on tables | **ACCEPT** | operator/transform tables | `PENDING_DEPENDENCY` |
| D5 A-06b depends on standing-item contract | **ACCEPT** | standing-item contract unfrozen | `PENDING_DEPENDENCY` |
| D6 A-07a / C12 role completeness | **ACCEPT** | operator registry unfrozen | `PENDING_DEPENDENCY`; semantic adequacy stays an AUDIT question |
| D7 F-07b chooses containment | **ACCEPT** | containment policy unfrozen | `PENDING_DEPENDENCY`; assertion becomes "a malformed unit fails closed", not "the run fails" |
| D8 F-14a freezes cardinality | **ACCEPT** | operator contract unfrozen | `PENDING_DEPENDENCY` |
| E1 O-03 says only the bad line fails | **ACCEPT** | containment is downstream | obligation becomes "containment policy decided and demonstrated", not a preset answer |
| F1 O-06 package-order invariance | **ACCEPT** | — | withdraw the requirement; replace with "order sensitivity characterised" |
| F2 O-10 paste-order invariance | **ACCEPT** | — | bias characterised, not invariance demanded |
| F3 O-01 IR identical except trace | **ACCEPT** | — | equivalence at note + declared IR fields, not byte equality |
| F4 O-02 seam probe wrong | **ACCEPT** | — | declared dependencies **should** propagate; the test detects **undeclared** propagation |
| F5 O-08 literal cross-run IDs | **ACCEPT** | — | stability within a case is the design goal; literal identity is a downstream decision |
| F6 O-21 limits reproducibility | **ACCEPT** | — | no definitional limit; the semantic share is measured by E1, not excluded |
| G1 ABSENT_BY_CONTRACT | **ACCEPT** | disposition vocabulary open | removed |
| H1 ten-note corpus | **ACCEPT** | signer owns corpus | count is not fixed; coverage is measured per class |
| H2 one fixture per class | **ACCEPT** | — | coverage requires ≥2 independent evidence sources per CRITICAL class |
| I1 DESIGN CHANGE too narrow | **ACCEPT** | workflow | authority/decision moves and shared-contract changes are DESIGN |
| I2 signer approval too narrow | **ACCEPT** | — | includes style and product baselines |
| I3 "original reviewer approves" | **ACCEPT** | workflow has no such role | current independent acceptance owner |
| J1 F2 example fixes runtime behaviour | **ACCEPT** | — | neutral placeholders |
| J2 property-only brief | **ACCEPT** | — | frozen wording properties allowed |
| K1 manifest granularity too coarse | **ACCEPT** | workflow | per-artifact and per-contract rows, not one row per module |
| K2 readiness conflates local and system | **ACCEPT** | — | distinguish `LOCAL_ACCEPTED` from `INTEGRATED`/`SYSTEM_ACCEPTED` |
| L1 O-12 coverage wording | **ACCEPT** | I2 and S3 both account | obligation names both span accounting and object disposition |

## What this means

Thirty-four of thirty-four raised items are accepted or already covered by the Review 2 target. None is contested, because each one caught something in my draft that the frozen upstream already settled.

The pattern in my failures is consistent and worth naming: **I wrote fixtures and obligations that answered questions the architecture had deliberately left open** — containment policy, operator cardinality, normalisation, corpus size, invariance requirements. A predicate that answers an open design question stops being a test and becomes an unpublished decision.

That is the rule I will apply in the rewrite: a predicate may only assert what a frozen contract already states. Everything else is `PENDING_DEPENDENCY` with the contract named.

## One thing I am not accepting silently

**F6 (O-21).** I agree the definitional limit is wrong and I will remove it. But the underlying fact remains: identity, grouping and operator adequacy are not mechanically decidable, so a reproducibility claim about them can only be empirical. The rewrite should say that as a measured result, not a definition — which is what the correction asks, and what E1 exists to produce.
