# 021E — Adversarial line-by-line review: FIXTURE_REGISTER.md

## Verdict

**NOT READY FOR THE FROZEN Doximity TESTING STRATEGY.**

This file preserves important historical lessons, but it currently mixes observation, inferred cause, regression guard, validation mode, and future schema assumptions. It also lacks severity/version/prerequisite metadata needed for the signer's multi-case batch protocol.

## File-level challenge

The register should distinguish:

1. **HISTORICAL_OBSERVATION** — what actually happened;
2. **EVIDENCE** — exact immutable source;
3. **EVIDENCE_BOUNDARY** — what the evidence does *not* establish;
4. **REGRESSION_ASSERTIONS** — guards inspired by the observation;
5. **ASSERTION PREREQUISITES** — contracts/tables needed before the assertion is executable;
6. **SEVERITY** — CRITICAL / MATERIAL / COSMETIC;
7. **STATUS/VERSION** — ACTIVE / PROVISIONAL / WITHDRAWN / PENDING_DEPENDENCY.

Without this split, a symptom can quietly become an invented causal diagnosis.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 1 | "failures that reached output" | INACCURATE TITLE | Register includes packaging failure, contract contradiction, process regression, derived fixture. Rename to evidence-grounded regression/fixture register. |
| 3 | fixture = defect + evidence + assertions | INCOMPLETE | Missing evidence boundary, severity, version, prerequisites/status. |
| 3 | exactly one owner per assertion | STRONGLY SOUND | Keep. Owner must allow runtime submodule and engineering-control owner. |
| 9 | F1 fabrication = content source never said | TOO LITERAL | Unsupported clinical meaning can be fabricated even if individual tokens appear in source. Keep class broad; do not equate it with token absence. |
| 10 | F2 duplication = one fact rendered twice | TOO BROAD | Intentional reuse across sections/problems may be valid. Use "unapproved duplicate rendering of the same proposition/use." |
| 11 | F3 silent omission = fact or line gone | TOO BROAD | Omission can be intended with disposition. Define required content disappearing without valid disposition/use. |
| 12 | F4 contract break = malformed output | TOO NARROW | Contract breach can be well-formed but violate cardinality/order/voice/etc. If F4 is schema-malformation specifically, rename it. |
| 13 | F5 instability = different decisions identical input | GOOD CORE | Clarify acceptance-relevant semantic/structural decisions, not allowed wording variation. |
| 14-18 | F6-F10 classes | REASONABLE | Need severity and concrete mandatory fixtures where historically central. |
| 20 | C12 = faithful but clinically empty | TOO NARROW | Stable bad representation may be incomplete/semantically insufficient rather than literally empty. |
| 24 | mandatory fixtures | AUTHORITY NOT DEFINED | "Mandatory" should mean ACTIVE + evidenced + eligible for briefs, with version. |
| 28-30 | F-01 observation/control/boundary | GOOD EVIDENCE BOUNDARY | Keep distinction that historical run does not establish I3 cause. |
| 33 | A-01a token containment mechanical | PREMATURE / POSSIBLY OVERSTRICT | Allowed morphology/abbreviation/synonym normalization table is not frozen. Mark PENDING_DEPENDENCY. Also token containment does not prove absence of fabricated relation/meaning. |
| 34 | A-01b package supplies every required contract | NEEDS MANIFEST/DEPENDENCY REGISTRY | "Every required" is not mechanically knowable without package/dependency authority. |
| 35 | A-01c R1 content bound | PENDING DEPENDENCY | Operator fixed text/transformation table are downstream. Mechanical only once those authorities are frozen. |
| 37 | F-02/F-03/F-04 grouped | SCORING ID PROBLEM | Three historical fixtures share A-02a/A-02b. For batch scoring, each fixture/case needs stable assertion instances or a clearly parameterized assertion template. |
| 39 | duplicated within one problem block | IMPORTANT SCOPE | This scope should constrain the assertions below. |
| 40 | evidence paths abbreviated | CLAIM-VS-FILE MISMATCH | DeepSeek claimed literal full paths; only first is full. Evidence rule later says evidence is a path. |
| 43 | object id at most one unit per (section, problem) | POSSIBLE ARCHITECTURE VIOLATION | Consensus #23 allows explicit reuse by multiple render units/problems and does not state this same-(section,problem) prohibition. Prove it is ratified or replace with explicit-reuse/accounting invariant. |
| 44 | same-proposition objects do not both render | OVERBROAD | Could be valid in different sections/problems/rhetorical functions. Scope to the adjudicated use-context / duplicate relationship and one problem block historical failure. |
| 46 | both needed | SOUND INSIGHT | Correct that id uniqueness cannot solve semantic duplicates. |
| 50 | F-06 defect = seizure precautions absent | MISLEADING HISTORICAL LABEL | Initial event was packaging-invalid/untestable, not model omission. Phrase observation as missing standing-item dependency made required behavior unavailable. |
| 51 | F-06 evidence | PARTLY GOOD, PATHS ABBREVIATED | Prefer exact P003 review + current PACKAGE + set2/set3 validation paths; six raw paths are unnecessary unless specifically needed. |
| 52 | defect packaging not model judgement | SOUND | Keep prominently. |
| 55 | BUILD package declares/supplies standing item | NEEDS MANIFEST | Requires declared dependency graph/package manifest. |
| 56 | trigger satisfied => unit exists mechanical | PENDING DEPENDENCY | Standing-item catalog/trigger schema are not frozen yet. |
| 60-61 | malformed REUSE historical evidence | SOUND | Keep. |
| 64 | every unit typechecks against operator | PENDING DEPENDENCY | Operator schema not frozen. |
| 65 | malformed unit -> CONTRACT_ERROR | SOUND FUTURE INVARIANT | Be precise whether R1 validates itself or consumes an S4-invalid artifact in one-call execution. |
| 69 | prior no-further-workup rendered current | SOUND HISTORICAL OBSERVATION | Exact evidence supports runs 1/2, not necessarily all runs. |
| 70 | raw runs + validation "records" | TOO VAGUE | Use exact validation path and identify which runs exhibit failure. |
| 73 | final plan rendering assertion owned by S2 | WRONG OWNERSHIP/SCOPE | S2 decides adoption, not final rendering. Split: I4 attribution if relevant; S2 current_adoption; S3 selection/current-plan use; S4 plan unit if needed. |
| 77 | voice = first person and conversational framing | OBSERVATION BROADER THAN ASSERTION | Assertion only bans first-person; it does not catch second-person/conversational `your old stroke` or other framing. |
| 81 | no first-person token mechanical | SOUND PARTIAL GUARD | Add separate assertion for other prohibited A/P conversational/person framing if frozen style requires it. |
| 85 | two rules in 05 caused different order | PLAUSIBLE / NEEDS EXACT EVIDENCE SCOPE | Cite exact preserved conflicting rules and distinguish evidence of contradiction from evidence of runtime variance. |
| 86 | L1 contradiction | SOUND CLASSIFICATION | But current BUILD schema may not mechanically detect prose-policy contradictions. Do not let fixture imply implemented capability. |
| 90 | BUILD mechanically catches incompatible fields | PENDING BUILD DESIGN | Valid only after applicability/compatibility/decision registry exists. |
| 94 | C-02 O51 moved as unrelated effect | FACTUALLY QUESTIONABLE | The added clause explicitly governed prior-record results and O51 is a prior MMSE result; its move is a direct consequence of the conflicting clause. C14 non-locality is better evidenced by other objects changing unexpectedly across prompt edits. Do not call O51 "unrelated" without defending that. |
| 98 | validation mode MEASURED | CONFLICTS WITH FROZEN VOCABULARY | Frozen modes are MECHANICAL / SEMANTIC_AUDIT / HYBRID. Either explicitly propose a process-metric category or split diff generation (mechanical) from acceptability judgment (semantic/hybrid). |
| 102 | "The MRI to show." grammatical, supported, carrying none payload | INACCURATE DESCRIPTION | It is unidiomatic/fragmentary, and it carries part of payload (MRI/test) but omits purpose. Describe as stable semantically incomplete representation. |
| 103 | B+ evidence | CORRECT PATH | Keep. |
| 104 | distinguish approved `MRI to show.` | CRITICAL / SOUND | Keep. |
| 107 | required roles present mechanical | INSUFFICIENT C12 GUARD | A too-thin operator schema can have all required roles and still be semantically inadequate. Add S4 SEMANTIC_AUDIT for operator/unit adequacy, then mechanical role completeness. |
| 108 | R1 does not infer missing role | SOUND | Pending operator schema; fail closed is correct. |
| 110-118 | provisional fixtures | GOOD HONESTY | Add severity/status/version and actively search exact evidence for historically important classes. |
| 122-123 | withdrawn items | GOOD | Keep evidence/reason. |
| 128-131 | D-01 derived | PENDING DEPENDENCY | Depends on standing-item/operator definitions; should be PENDING_DEPENDENCY until those are frozen. |
| 136 | all relevant historical fixtures | SOUND | Also include signer reference-case assertions; "historical" is not the only acceptance source. |
| 137 | fixture changes via acceptance change | SOUND | Version changes; do not mutate old assertion in place. |
| 139 | new defect registered before fixed | SOUND EVIDENCE PRESERVATION, ACCEPTANCE RISK | Register first as OBSERVATION/PROVISIONAL. It cannot retroactively become a scored criterion for the run that discovered it. |
| 140 | evidence is a path | SOUND | Enforce literally; several current paths are abbreviated. |
| 141 | one owner | STRONGLY SOUND | Keep. |

## Missing mandatory historical coverage

### Apixaban hold + resume-condition composition
Verified in:
`runs/2026-11-14-p003-doximity/set3/validation.txt`

- run1/run2 split hold and resume into separate bullets;
- run3 merged conditional correctly.

This is a direct S2/S4 regression for condition attachment and PLAN_CONDITIONAL composition. It should not disappear.

### Explicit reproducibility / F5 fixture
Instability was one of the defining old failures.

Use a verified within-set identical-condition run family (set2 or set3, with the documented mode/package caveats) to assert:
- same frozen input/package/mode;
- compare acceptance-relevant structural decisions;
- no claim of population failure rate.

## Missing assertion metadata required by frozen batch protocol

At minimum:
- CASE/FIXTURE_ID
- ASSERTION_ID
- owner
- expected property
- validation mode
- **severity CRITICAL/MATERIAL/COSMETIC**
- prerequisite/evidence requirements
- assertion status/version
- dependency contract(s)

Run RESULT belongs in score artifacts, not the registry definition.

## Scalability

Do not turn this one Markdown file into the corpus for 10–15 realistic cases × hundreds of assertions.

Recommended authority split:
- `FIXTURE_REGISTER.md`: index/status/evidence summary;
- per-case frozen baseline/assertion packet;
- per-experiment manifest/raw/scores/diffs/verdict.

## DeepSeek must answer

Especially defend:
- A-02a against consensus #23 reuse;
- A-02b's scope;
- F-11 ownership;
- MEASURED vs frozen validation vocabulary;
- why C12 has no semantic operator-adequacy assertion;
- why apixaban composition and F5 instability are absent;
- where severity and prerequisites live.
