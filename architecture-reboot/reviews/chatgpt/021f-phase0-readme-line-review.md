# 021F — Adversarial line-by-line review: phase0/README.md

## Verdict

**CURRENTLY MISSTATES PHASE 0 SCOPE AND LIFECYCLE.**

A README should point to the authoritative lifecycle/state; it should not create a simplified competing process.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 1 | Phase 0 control plane | SOUND | Keep. |
| 3 | five documents | INCOMPLETE AGAINST FROZEN WORKFLOW | The workflow explicitly called for an implementation manifest/status ledger. Current Phase 0 has no such authority. Explain why it disappeared. |
| 3 | no runtime code | TRUE BUT MISLEADING FOR BUILD | BUILD_LINT claims active enforcement on every build, yet no lint implementation exists. "No runtime code" is not the same as "no engineering-control code." |
| 3 | each exists because we hit the failure it prevents | OVER-SIMPLIFIED | Some are generic governance instruments; one historical failure can motivate multiple controls. Do not imply one-to-one causal proof. |
| 5 | signer approved authoring via "go" | PROVENANCE CLAIM NEEDS EVIDENCE | Current visible thread did not contain that explicit go-ahead at the point Phase 0 appeared. Cite the exact signer message/source or state simply that drafts exist under review. |
| 5 | draft under review | SOUND | Keep until genuinely frozen. |
| 9 | BUILD_LINT prevents C11 | OVERCLAIM | It can only prevent structured contradictions it can detect; prose-policy conflicts and mis-tagged decisions can escape. |
| 10 | AUDIT prevents criteria written to fit build | PARTLY TRUE | Only if post-hoc assertions are prohibited from scoring the same run. Current line 41 undermines this. |
| 11 | brief prevents implementation without definition of correct | PARTLY TRUE | Only if lifecycle/manifest enforces no implementation before accepted brief. |
| 12 | change control prevents C14 | WRONG MAPPING | C14 is non-local regression; change control governs edits but regression protocol detects C14. It does not itself prevent prompt sensitivity. |
| 13 | fixture register prevents invented cases | OVERCLAIM | It can constrain acceptance evidence if enforced, but derived fixtures are intentionally allowed. Its purpose is evidence provenance/traceability, not banning invention entirely. |
| 15 | brief -> implementation -> lint -> check -> audit -> acceptance -> freeze -> record | CONFLICTS WITH FROZEN WORKFLOW | Engineer reviews brief before implementation; BUILD protects contracts before dependent implementation; CHECK is created as schemas appear; static/fixture validation precedes Doximity; repeated/robustness runs are separate; state is recorded throughout, not only after freeze. |
| 17 | none of these change during Phase 1 unless DESIGN or ACCEPTANCE CHANGE | FALSE | PATCH and implementation changes to engineering-control implementation can occur. Also BUILD/AUDIT specs may legitimately evolve through their own governed categories. |

## Missing README responsibilities

The README should point, not restate:

- authoritative implementation/status ledger;
- frozen lifecycle document;
- change-history authority;
- location/status of BUILD enforcement;
- fixture/assertion authority split;
- experiment protocol.

## DeepSeek must answer

Why was the manifest/status ledger omitted, and why should this simplified lifecycle be trusted over the already frozen workflow?
