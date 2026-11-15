# 021B — Adversarial line-by-line review: AUDIT_PROTOCOL.md

## Verdict

**CONCEPT SOUND; ACCEPTANCE INTEGRITY NOT YET SAFE.**

The file correctly separates semantic review from mechanical checking and correctly avoids first-failure stopping. Its largest risks are post-hoc criteria, underdefined evidence packets, overbroad signer escalation, and an independence rule too weak for Doximity-generated outputs.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 3 | procedure, not case-specific clinical expectations | SOUND | Keep the distinction, but fixtures are acceptance definitions grounded in evidence; they do not literally "live in evidence." |
| 7 | checker proves note matches Case IR; audit proves IR matches encounter | TOO NARROW / OVERSTATED | AUDIT also covers I1-I4 and intermediate STRUCTURE artifacts. CHECK proves only mechanically decidable seam conformance, not all note↔IR semantics (especially R2). Reframe generically by seam. |
| 11 | available inputs determine answerability | PARTLY SOUND | For acceptance, required evidence should be specified in the frozen assertion/brief. Accidental absence of evidence should BLOCK, not redefine what the assertion needs. |
| 13-21 | Mode A artifact audit | USEFUL | Define it as an evidence packet, not merely "source omitted because batch volume." Efficiency cannot override an assertion's prerequisites. |
| 15 | returned artifact + frozen assertions | INCOMPLETE | Auditor also needs acceptance-brief version / controlling contract references / baseline version to interpret the assertion correctly. |
| 17 | properties only, never expected prose | FALSE ABSOLUTE | Frozen Doximity protocol allows exact/bounded prose when canonical wording, clinical meaning, or signer style is itself contractual. |
| 19 | assertion-level answerability | SOUND | Keep. |
| 21 | used for batch volume when source large | RISKY FRAMING | Large source size is not a reason to omit source if assertions require it. Mode is determined by assertion prerequisites, not convenience. |
| 23-29 | Mode B full audit | MOSTLY SOUND | "Full" is misleading because not every upstream artifact need exist. Consider evidence-expanded/seam audit. |
| 25 | artifact + assertions + whichever source/IR/check required | BETTER, STILL INCOMPLETE | Add acceptance brief/contract version and baseline/version. Otherwise assertion meaning can drift. |
| 29 | first run of a new case uses Mode B | UNJUSTIFIED ABSOLUTE | If a signer-approved baseline packet already exists and the tested seam needs no raw source, why is full evidence mandatory? Use assertion prerequisites instead. |
| 31 | implementer rationale never input | SOUND BIAS CONTROL | But implementation/package version must remain visible. Also "it makes reviewer agree" is rhetorical, not a proven mechanism. |
| 35 | audit driven by fixture assertions | TOO NARROW | Acceptance briefs can define properties not derived from historical fixtures. Audit should be driven by the frozen acceptance assertion set, wherever its source. |
| 37 | fixed seam list | POSSIBLE SECOND TAXONOMY | Is this a frozen enumeration or illustrative tags? It omits BUILD/process owners. Avoid accidentally creating another authority taxonomy. |
| 39 | UNDECIDABLE if evidence insufficient | SOUND | For acceptance, if required evidence is absent the artifact should be BLOCKED, not merely treated as a lower-information mode. |
| 41 | auditor may add case-specific assertion after seeing case/output | CRITICAL RISK | This is post-hoc acceptance drift. New issue should be recorded as DISCOVERY/unscored; if already prohibited by a frozen contract, score the existing contract; otherwise acceptance/design change + rerun before it becomes scored. |
| 43 | collect all independent failures | STRONGLY SOUND | Keep; this supports high-information batches. |
| 43 | stop only when later assertions uninterpretable | SOUND | Define dependency/prerequisite links so "uninterpretable" is not ad hoc. |
| 47-54 | result record | UNDER-SPECIFIED FOR BATCHING | Missing ASSERTION_ID, CASE_ID, severity, assertion version, baseline version, evidence refs (plural), prerequisite status, scorer identity/run id. "SPAN" singular is too narrow. |
| 48 | "CHECK 4 duplicate identity" | TERMINOLOGY PROBLEM | This is a semantic audit finding, not necessarily CHECK. Use ASSERTION_ID / FINDING_ID. |
| 50 | evidence statement | POTENTIAL SEMANTIC CLAIM | Fine, but reference exact artifact/object ids and source where needed. |
| 52 | owner S2 | SOUND EXAMPLE | Owner must be exactly one. |
| 56 | owner is a submodule | INCONSISTENT | Current fixtures include BUILD and process ownership. Say owner is exactly one runtime submodule or engineering-control owner. |
| 60 | ACCEPT = every answerable question passed | MISLEADING | Acceptance requires every declared required assertion to be decidable and pass. "Answerable" alone could permit missing evidence. |
| 61 | REJECT if at least one fail | SOUND, BUT VERDICT PRECEDENCE MISSING | What if there is one FAIL and one UNDECIDABLE? Define whether verdict is REJECT with incomplete audit or BLOCKED. Severity may matter. |
| 62 | BLOCKED if audit cannot proceed | SOUND | Add missing required evidence / scorer-integrity failure as examples. |
| 64 | either mode accepts if all assertions decidable | SOUND CORE | Also explicitly require they pass and that the frozen assertion version matches the run's acceptance packet. |
| 68 | cannot decide -> escalate to signer | TOO BROAD | Engineering ambiguity should first go to frozen contract/evidence + second independent LLM. Signer arbitrates genuine clinical/style/product ambiguity unresolved by evidence. |
| 68 | do not average/hedge/accept reservations | SOUND | Keep. |
| 72 | expected clinical content belongs fixture | MOSTLY SOUND | Exact/bounded expected prose can be a legitimate property when wording itself is contractual. |
| 73 | scoring formula belongs batch protocol | SOUND | Audit still must carry severity/result fields required by that protocol. |
| 74 | criteria invented after implementation = drift | SOUND AND CONFLICTS WITH LINE 41 | Reconcile line 41 using DISCOVERY -> change control -> rerun. |
| 78 | any reviewer who did not write artifact | TOO WEAK | DeepSeek did not literally write Doximity output but authored the implementation. Primary acceptance reviewer should be independent of implementation author. Implementer can be secondary challenger/scorer. |

## Required conceptual additions

- **Frozen acceptance packet**: artifact/run id + brief/version + assertion set/version + baseline/version + required evidence + check report.
- **Discovery state** distinct from scored assertion.
- **Primary independent reviewer** vs secondary implementation-author score.
- **Severity-aware finding record** compatible with CRITICAL/MATERIAL/COSMETIC.
- **Dependency/prerequisite links** between assertions.
- **Signer escalation only after engineering review path exhausted**, unless the issue is inherently clinical/style/product.

## DeepSeek must answer

Especially defend:
- why line 41 is not post-hoc goalpost movement;
- why implementer-authored system output can be primarily audited by the implementer under line 78;
- why exact/bounded prose is banned despite the frozen Doximity protocol allowing it;
- what exact evidence packet is sufficient for acceptance.
