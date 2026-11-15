# ChatGPT review 085 — Gate 0 reviewer-policy proposal

## Verdict

> **REVISE Option E. Recommend Option F: signer-anchored semantic baseline + two blinded LLM judges, with hash-based reuse.**

DeepSeek's proposal correctly identifies the operational problem with the current three-human rule and
correctly rejects substituting deterministic checks for genuinely semantic judgment.

However, Option E should not be adopted as written.

The main correction is conceptual:

> the signer is not a third independent scorer. The signer should establish the clinical/reference verdict;
> the LLM judges should be calibrated against that reference.

That is both more honest and more efficient.

---

## 1. PASS — the three-human default is unnecessarily impractical

The current Gate 0 rule was designed to avoid one-reviewer blind spots, not because three humans are a
clinically necessary quorum.

For this project, requiring three independent humans for every semantic calibration packet is not an
operationally realistic default.

A mixed human/model policy is defensible if its claim is narrow and its independence limitations are
recorded explicitly.

---

## 2. BLOCKER in Option E — clean packets do not expect FIRED

Option E says, for each semantic packet:

> all three must return FIRED and satisfy within-layer specificity.

That is wrong for clean parents.

Current active human-review predicates are:

- S1-CAND-01
- S2-ADOPT-01
- S2-REP-01

The current corpus contains:

- **4 semantic seed artifacts**
  - G0-S1-05 -> S1-CAND-01
  - G0-S2-01 -> S2-REP-01
  - G0-S2-02 -> S2-REP-01
  - G0-S2-06 -> S2-ADOPT-01
- **3 clean semantic packets**
  - clean S1 -> S1-CAND-01
  - clean S2 -> S2-ADOPT-01
  - clean S2 -> S2-REP-01

Total: **7 semantic packets = 3 clean + 4 seeded**, not 2 clean + 5 seeded.

Correct expectations:

- clean semantic packet -> reference verdict **SILENT**
- seeded semantic packet -> reference verdict **FIRED**
- same-layer specificity must still hold for seeded artifacts

The replacement policy must encode both branches explicitly.

---

## 3. BLOCKER in Option E — signer should not be treated as statistically independent

The proposal itself acknowledges that the signer is not statistically independent.

Therefore the panel should not be described as three peer independent judges.

Use two roles:

### Reference authority

The signer/clinician establishes the packet's accepted semantic reference verdict.

### Calibrated evaluators

Two blinded LLM judges independently evaluate the packet and must match the signer reference.

This yields a cleaner validity claim:

> two independent model evaluators detected the same semantic condition as the signer-defined reference
> under blinded packet-only review.

That is more precise than saying "3/3 independent panel".

---

## 4. Major efficiency correction — semantic reference judgments should be reusable

DeepSeek's Option E assumes one recalibration costs seven new signer judgments.

That should not be the default.

The packet already has a deterministic packet id/hash derived from:

- predicate rule;
- target artifact;
- allowed dependency context;
- allowed oracle material.

Therefore a signer reference judgment should be reusable while the semantic packet is identical.

### Baseline identity

Store a semantic baseline keyed at minimum by:

- packet_id / packet hash;
- predicate id;
- predicate/contract version;
- oracle/context hashes included in the packet;
- reviewer-policy version.

### Reuse rule

If all semantic inputs above are unchanged:

> **reuse the signer reference verdict. Do not ask the signer to re-judge it.**

If only mechanical scorer/harness code changes while packet hashes remain identical:

> no semantic re-review is required.

If the packet/predicate/oracle/relevant dependency content changes:

> re-review only the affected semantic packets.

This directly follows the program's existing principle that one calibration may serve a campaign while
the relevant scorer logic and predicate definitions remain unchanged.

---

## 5. LLM judgments are model-version-specific

Signer reference evidence and LLM calibration evidence have different lifetimes.

### Signer reference

Reusable while the packet's semantic identity is unchanged.

### LLM judge calibration

Tied to:

- model family;
- model/version;
- packet hash;
- policy version.

If a model judge/version materially changes and that model will be used as a semantic evaluator later,
rerun that model's calibration on the frozen packet set.

Do **not** make the signer repeat unchanged reference judgments just because an LLM version changed.

---

## 6. Transfer boundary must be explicit

The experiment program says Gate 0 calibrates the CHECK/AUDIT scorer that will later score acceptance
evidence.

Therefore:

> Gate 0 evidence transfers only to the semantic evaluator mode actually calibrated.

If later architecture experiments use:

- the same dual-LLM semantic evaluator policy -> Gate 0 can gate that evaluator;
- signer-only scoring -> the dual-LLM Gate 0 does not calibrate signer-only scoring;
- a different model/family/version -> recalibrate the affected semantic evaluator;
- a new semantic scoring procedure -> that procedure requires its own Gate 0 calibration.

Do not create a Gate-0-only reviewer panel and then score the real experiments by a different method while
claiming transfer.

---

## 7. Cross-family requirement — useful but not mechanically provable

Using different model families is a sensible anti-correlation control.

But the harness cannot truly prove:

- that a session was fresh;
- that a model had no prior project context;
- that two vendor/model-family implementations are genuinely independent.

It can only record the operator's declared model/session metadata.

Therefore phrase this as an **eligibility/control requirement**, not as a mechanically proven independence
property.

For full calibration evidence:

- two separate packet-only sessions;
- distinct judge ids;
- different model families where the project can actually supply them;
- model family/version recorded;
- no project-context agents such as this ongoing ChatGPT or DeepSeek thread counted as fresh judges.

If the required evaluator configuration is unavailable, calibration stays INCOMPLETE; do not fabricate
independence.

---

# 8. Recommended policy — Option F

## Option F: signer-anchored baseline + dual-LLM calibration

For each **new or semantically changed** packet:

1. **Signer/clinician establishes the reference verdict first**
   - clean packet: expected SILENT if valid;
   - seeded packet: expected FIRED if the planted semantic defect is valid;
   - signer may return UNDECIDABLE if the packet itself is not fit for calibration.

2. **Two blinded LLM judges independently score the same packet**
   - packet-only context;
   - no answer key, seed id, mutation metadata, signer verdict, or other judge verdict;
   - separate judge identities;
   - different model families for full calibration when available;
   - family/version/session metadata recorded.

3. **Calibration result**
   - both LLM judges exactly match the signer reference and required specificity -> PASS;
   - either LLM gives the opposite determinate verdict -> FAIL;
   - missing / duplicate / UNDECIDABLE evidence -> INCOMPLETE.

4. **Reuse**
   - signer reference is reused while semantic packet identity is unchanged;
   - LLM judgment is reused only for the same packet + same evaluator model/version + same policy;
   - only changed packets/evaluators are recalibrated.

This is not majority voting.

The signer defines the reference; the model judges are being calibrated against it.

---

## 9. Why Option F is better than Option E

Option E:

- unnecessarily treats the signer as an independent peer judge;
- incorrectly requires FIRED on clean packets;
- miscounts the current clean/seed packet split;
- implies repeated signer work even when semantic packet identity is unchanged;
- does not clearly state transfer to downstream experiment scoring.

Option F:

- preserves the clinical anchor;
- calibrates the actual model evaluators;
- makes disagreement fail rather than majority-pass;
- reuses immutable semantic reference evidence;
- recalibrates only what actually changed;
- gives Gate 0 a precise, bounded transfer claim.

---

## 10. Contract changes if signer approves Option F

Change only the reviewer-policy layer.

### Required

1. `AX-S1S2-D/predicates.md`
   - semantic Gate 0 mode becomes signer-reference + calibrated evaluator;
   - predicate meaning unchanged.

2. `gate0/00-GATE0-MANIFEST.md`
   - clean vs seeded semantic expectations;
   - signer reference role;
   - two blinded LLM evaluator rules;
   - PASS / FAIL / INCOMPLETE;
   - hash-based reference reuse;
   - evaluator-version recalibration;
   - transfer boundary.

3. `tools/gate0_harness.py`
   - distinguish `REFERENCE` from `EVALUATOR` judgments;
   - signer record: HUMAN / reference;
   - two LLM evaluator records;
   - enforce packet/predicate binding;
   - compare evaluator verdicts with signer reference;
   - support baseline evidence keyed by packet/policy/evaluator identity;
   - record reference/evaluator provenance in EVIDENCE.json.

4. Tests
   - clean reference SILENT + both LLM SILENT -> PASS;
   - seed reference FIRED + both LLM FIRED -> PASS;
   - one determinate model mismatch -> FAIL;
   - UNDECIDABLE / missing -> INCOMPLETE;
   - reference reuse on unchanged packet;
   - changed packet invalidates reference reuse;
   - changed evaluator model/version invalidates only that evaluator's cached calibration;
   - project-context agent / missing eligibility metadata rejected where policy requires it.

5. `scorer/README.md`, `HANDOFF.md`, `WORKING_RULES.md`, `AGENTS.md`, `DECISIONS.md`
   - describe the accepted policy and no-status-next behavior.

### Not required

- architecture consensus;
- DC-001/DC-002;
- experiment hypotheses;
- seed mutations;
- predicate meaning;
- mechanical scorer semantics.

---

## 11. Signer decision required

Recommendation:

> **Approve Option F, not Option E.**

This is a governed acceptance-policy change, so do not patch it until the signer approves.

If approved, DeepSeek should implement the contract/harness policy change, regenerate governing hashes,
run preflight, and return the diff for independent review.

Gate 0 acceptance itself remains unrun during that patch pass.
