# Doximity Contract Checklist

Use this before running a new Doximity prompt/module.

---

# A. Prompt shape

- [ ] Hard read-all gate is first.
- [ ] Output is forbidden while instructions/input are still being read.
- [ ] Internal phases are explicit.
- [ ] Each function is written as short atomic imperatives.
- [ ] Permissions and prohibitions are separated.
- [ ] Runtime prompt contains no unnecessary architecture history.
- [ ] Output schema appears after semantic responsibilities are defined.
- [ ] Final output gate is the last substantive instruction.

---

# B. Function ownership

- [ ] This stage has one clear semantic owner.
- [ ] It does not reopen a decision already owned upstream.
- [ ] It does not make a downstream decision early.
- [ ] If a new function was added, there is evidence it cannot safely remain combined with an existing function.
- [ ] File count has not increased merely because function count increased.

---

# C. Source fidelity

- [ ] Source boundaries are preserved.
- [ ] Speaker labels are not converted into identities without explicit support.
- [ ] Questions do not become answers.
- [ ] Silence does not become a negative.
- [ ] Nested provenance is not promoted to direct provenance.
- [ ] Historical state is not promoted to current state.
- [ ] Reported outside result is not promoted to directly reviewed result.
- [ ] Completed study is distinct from result availability/review.

---

# D. Schema pressure

- [ ] Every field is necessary.
- [ ] Optional fields can remain absent naturally.
- [ ] The schema does not invite unsupported state completion.
- [ ] A repeated failure is not being addressed by another prose warning only.
- [ ] Closed enums have been empirically shown to be safe for this function.
- [ ] Source-qualified wording is preferred when normalization is brittle.

---

# D1. Serialization

- [ ] Model-authored handoff is one JSON object.
- [ ] No prose, Markdown, or code fence around the JSON.
- [ ] No custom `@@` output records.
- [ ] No pipe delimiter.
- [ ] Scribe `@@PACKET` / `@@SOURCE` / `@@END` markers are treated as input framing, not copied downstream.
- [ ] JSON keys and array types are validated mechanically; malformed output fails closed.
- [ ] JSON is the canonical handoff; CSV is used only for flat coverage or review export.
- [ ] YAML is not used for nested handoffs.

---

# D2. Execution boundary

- [ ] No stage requires Doximity Ask to execute code.
- [ ] Parsing, validation, retries, state and rendering run outside the model.
- [ ] A code-shaped prompt is not treated as execution.

---

# D3. Clinical reference checks

- [ ] Run after synthesis, not during coverage.
- [ ] Inputs are deidentified.
- [ ] Output is JSON with a verdict and citation.
- [ ] No citation means `unverified`.
- [ ] Unsupported/unverified claims go back to synthesis; they are not silently rewritten.
- [ ] Reference output is not packet evidence and does not enter the coverage census.

---

# E. Coverage

- [ ] The stage has a defined coverage responsibility.
- [ ] Material body evidence has a stable home.
- [ ] Material actions have a stable home.
- [ ] Compound records are split only when downstream recoverability requires it.
- [ ] Coverage enumeration is not silently mixed with clinical synthesis unless tested.
- [ ] No "better run" is being selected after a paired run omitted material content.

---

# F. Provenance references

- [ ] Prefer stable record IDs over copied selectors during synthesis.
- [ ] Every cited record exists.
- [ ] Every cited record materially supports the associated output.
- [ ] No output state comes from an uncited record.
- [ ] If exact source text is needed, dereference mechanically rather than asking a reasoning stage to recopy it.

---

# G. Clinical synthesis

- [ ] Uncertain episode identity remains unresolved.
- [ ] Same target does not automatically mean same action episode.
- [ ] Baseline symptom does not become a separate problem solely because it is chronic/distinct.
- [ ] Historical disease becomes BACKGROUND only when encounter-relevant.
- [ ] Diagnostic suspicion is not upgraded to diagnosis.
- [ ] Management intensity is not used as diagnostic proof.
- [ ] Source-qualified action wording is preserved.

---

# H. Compiler / render boundary

- [ ] Problem ownership is explicit before rendering.
- [ ] Rhetorical class is explicit.
- [ ] Group membership is explicit.
- [ ] Exactly one HEAD per group.
- [ ] MODIFIER/CONDITION/COVERED roles are explicit.
- [ ] One object appears in at most one group.
- [ ] Operator is explicit.
- [ ] Operator payload is proposition-complete.
- [ ] Order is explicit.
- [ ] Malformed structure fails closed.
- [ ] Renderer is not allowed to repair semantic defects.

---

# I. Validation

- [ ] Mechanical checks are truly mechanical.
- [ ] Semantic safety does not depend on same-context self-validation.
- [ ] A visible PASS ledger is not treated as proof of semantic correctness.
- [ ] Error taxonomy is small or has deterministic precedence.
- [ ] Correct valid/invalid boundary matters more than perfect diagnostic error labels.

---

# J. Experimental discipline

- [ ] Repeated-run axis uses fresh conversations when reproducibility matters.
- [ ] Same packet/input is used across compared arms.
- [ ] No prior outputs/oracle leak into the test session unless intentionally testing that condition.
- [ ] A stale/incorrect prompt execution is rejected as invalid evidence.
- [ ] A translated or inherited control is not treated as independent.
- [ ] Blocking failures are not averaged away.
- [ ] Do not manually union multiple runs and call that model capability.
- [ ] Stable wrong output is investigated as a contract/payload bug.
- [ ] Unstable semantic output is investigated as an upstream decision gap.

---

# K. Stop rules

Stop prompt tuning and reconsider the representation when:

- the same unsupported state reappears after multiple explicit warnings;
- exact phrase anchoring still permits semantic misclassification;
- same-context validator repeatedly false-passes;
- a stage repeatedly omits different material items across identical runs;
- a later stage keeps reconstructing decisions owned upstream;
- the final writer keeps making merge/split decisions;
- the renderer is asked to repair incomplete semantic payload.

Do not respond to these patterns by adding more prose.

---

# L. Preferred failure response

When an experiment fails:

1. identify the **function** that failed;
2. determine whether failure is:
   - coverage;
   - source fidelity;
   - semantic normalization;
   - reconciliation;
   - compilation;
   - rendering;
3. change the smallest ownership/representation boundary that isolates that function;
4. rerun the smallest targeted experiment;
5. do not redesign unrelated stages.

---

# M. One-line rule

> Make every Doximity stage decision-complete for its owned function and decision-incomplete for every other function.
