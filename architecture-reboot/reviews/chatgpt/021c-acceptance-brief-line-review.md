# 021C — Adversarial line-by-line review: ACCEPTANCE_BRIEF_TEMPLATE.md

## Verdict

**GOOD CORE IDEA; TEMPLATE CURRENTLY HIDES POLICY AND LACKS VERSION/SEVERITY SUPPORT.**

The five-field concept can remain thin, but only if the missing implementation manifest and assertion registry carry artifact identity, versions, dependencies, severity, and lifecycle state.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 3 | brief written before implementation and says what correct means | SOUND | Keep. The brief is not the only authority; it references frozen contracts/assertions. |
| 3 | never restates architecture | SOUND INTENT | It still must translate contract obligations into observable properties. Avoid treating any explanation as forbidden duplication. |
| 9 | exact section references, not summaries | SOUND, VERSIONING MISSING | Paths/sections drift. References should pin a version/commit or manifest-controlled contract version. |
| 13-15 | example references | CONCRETE DEFECT | `phase0/BUILD_LINT §1 L1–L6` is internally wrong: L1–L6 are under §2. Examples must themselves be valid. |
| 18 | if brief needs explanation, contract is unclear and should be fixed | TOO ABSOLUTE | A test brief may need to operationalize a clear high-level contract into an observable property without changing it. Distinguish explanation from specification invention. |
| 22 | all relevant historical fixtures + justified derived | SOUND | Also allow signer reference-case assertions that are neither "historical failure" nor derived boundary fixtures. |
| 22 | fixture id only | VERSIONING GAP | Pin fixture/assertion version/status. An id whose expectation later changed is insufficient for reproducibility. |
| 24-29 | fixture examples | MOSTLY OK | Ensure examples do not imply only historical-failure fixtures are valid reference cases. |
| 33 | properties stated so named check can decide | SOUND | Every property needs a stable PROPERTY/ASSERTION_ID and prerequisite evidence, not merely prose order. |
| 37 | every unit names exactly one problem | POSSIBLE HIDDEN ARCHITECTURE | Is this actually frozen? Body-section render units may not all be problem-specific. Do not use unratified substantive examples in a template. |
| 38 | operator in closed vocabulary | VALID FUTURE PROPERTY | Only mechanically decidable after operator registry exists; brief must be able to mark dependency pending. |
| 39 | section list no duplicate section | PROBABLY SOUND | Still an example, not template authority. |
| 44 | validation modes canonical | SOUND | Keep MECHANICAL / SEMANTIC_AUDIT / HYBRID. |
| 47-52 | P1-P4 checks | MAPPING DEFECT | PROPERTIES above have no P1/P2/P3/P4 labels, so checks are not actually traceable to the stated properties. |
| 51 | "operator renders the payload" semantic audit | AMBIGUOUS | Does this test semantic adequacy of selected operator, fidelity of realization, or both? One assertion should have one owner/seam. Split if necessary. |
| 54 | property without check is hope | SOUND PRINCIPLE | Also require the deciding check/audit exists or has an explicit pending dependency before implementation freeze. |
| 58 | failure behavior named by failure class | INCOMPLETE TRACEABILITY | Failure class alone is too broad. Tie behavior to PROPERTY/ASSERTION_ID and owner. |
| 62 | F2 -> reject unit pair, fail closed | HIDDEN POLICY / PROBABLY WRONG GENERICALLY | Duplicate identity is semantic upstream; not every apparent pair should be runtime-rejected. This template example risks becoming an unauthorized rule. Replace with neutral placeholders or exact fixture assertion refs. |
| 63-64 | C13 reject proposed note use, preserve object/reuse | GOOD PRINCIPLE | Better as a referenced established rule, not template authority. |
| 65 | C11 build fails | SOUND | Again, reference BUILD assertion rather than restating if possible. |
| 68 | failure class makes it auditable later | OVERSTATED | Durable auditability requires assertion id/version, fixture/baseline version, and evidence; class alone is insufficient. |
| 72 | exactly five fields, no more | ONLY SAFE WITH EXTERNAL MANIFEST/ASSERTION SCHEMA | Severity, prerequisites, artifact/version, dependency state must live elsewhere. If no manifest exists, this rule makes the brief under-specified. |
| 73 | no code/prompt text | SOUND | Keep. Exact expected bounded prose may still appear as an acceptance property/reference when wording itself is contractual. |
| 74 | every property has a check/mode | SOUND | Add status: active vs pending dependency where mechanical checker cannot yet exist. |
| 75 | fixture id must exist | TOO WEAK | It must be ACTIVE/eligible, version-pinned, and relevant. Provisional/withdrawn fixtures should fail acceptance-brief validation. |
| 76 | brief frozen before implementation | SOUND | Record version in manifest; acceptance change must not retroactively rescore old runs. |
| 80 | engineer reviews brief and may reject | SOUND | Require a recorded disposition and independent acceptance owner to resolve; engineer must not rewrite criteria unilaterally. |
| 82 | engineer stopping is better than knowingly wrong brief | SOUND RHETORIC | Fine, but not a testable rule. |
| 86 | target one page; three pages means artifact too large | UNSUPPORTED HEURISTIC | Brief length can grow because fixture coverage is rich even if artifact responsibility is coherent. Treat length as warning, not decomposition criterion. |

## Missing authority split

The brief should remain thin only if other control artifacts own:

- artifact id/version/status/owner/dependencies → **implementation manifest**
- assertion id/property/mode/severity/prerequisites → **assertion/fixture packet**
- contract version pins → **manifest/contract registry**
- run/package/baseline version → **experiment manifest**

## DeepSeek must answer

Defend:
- whether "every unit has exactly one problem" is already frozen;
- where severity lives;
- how brief references are version-pinned;
- why line 62 is not hidden runtime policy;
- why page count is a valid artifact-splitting criterion.
