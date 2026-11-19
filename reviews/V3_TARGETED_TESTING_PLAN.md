# V3 targeted testing plan

Approved by the user on 2026-11-19 for the `third-version` branch.

## Purpose and scope

Build a dependable, human-readable middle layer between the original encounter materials and the approved A/P content. The production goal is one Doximity prompt covering extraction, source reconciliation, and problem architecture. These are evaluation capabilities; their implementation order and number of internal passes remain experimental. Development checkpoints do not imply three production calls or three physician approvals.

Keep the six-section review worksheet as the destination:
1. Problem heading and role.
2. Status.
3. Evidence.
4. Interpretation.
5. Actions.
6. Needs review.

Approval applies to this testing strategy. No extraction approach has been selected, no new prompt has passed, and no Doximity tests were performed as part of recording this plan. Existing pipeline contracts, schemas, oracles, and historical acceptance results remain intact. Their behavior is not automatically adopted as the V3 answer, nor silently replaced by this document.

## Design principles

### Evaluate capabilities without assuming a processing sequence

Extraction asks what each supplied source actually says. Reconciliation distinguishes current state, history, evolution, correction, and unresolved conflict. Architecture determines independent problems, roles, and relationships.

Test the three capabilities separately, but do not assume that a strictly source-first pipeline is optimal. The clinician's assessment may help retrieve relevant information; source-first work may better preserve provenance but create duplication. Compare methods before choosing one.

When diagnosing a downstream error, a manually reviewed upstream input can isolate the responsible capability. This is a development experiment, not an additional required production step.

### Fix expected meaning before each comparison

For each case, establish:
- **Must preserve:** facts, causal targets, relationships, uncertainty, attribution, temporal scope, and management details.
- **Must not infer:** unsupported diagnoses, causal links, current status, execution, or action rationale.
- **Acceptable alternatives:** wording or organization that preserves the same meaning.
- **Must flag:** genuinely unresolved information.

Expected results describe semantic requirements, not one mandatory paraphrase. Agree on them before evaluating output. A legitimate change to an expected answer must be versioned with its reason and applied consistently to all compared methods.

The original source packet remains authoritative. Earlier LLM extractions are not reference truth.

### Preserve complete meaning during extraction

Use the smallest statement that retains its complete meaning. Excessive fragmentation is a failure risk.

For example, "Consider investigation X if symptom Y persists" must preserve the tentative action and its condition together. It must not become "Obtain X." A causal assertion must preserve what is causing what, whose interpretation it is, and its certainty.

Retain management modifiers such as owner, timing, setting, condition, patient preference, and decision versus execution state. Unknown states remain unknown. Outside-service interpretations retain attribution unless the current clinician adopts them.

### Keep one auditable review record

Clinical statements need source references that actually support their wording. Proposed organization must remain distinguishable from documented clinical meaning. Assignment of a finding to a problem does not itself authorize "supports," "due to," or other new interpretation.

The readable worksheet and eventual machine payload should represent the same approved content. The deterministic boundary begins after approval of exact wording, placement, and order. A downstream LLM asked to reinterpret those fields is not deterministic rendering.

## Candidate extraction approaches

These are hypotheses to compare, not established winners.

| Approach | Initial organization | Potential advantage | Failure risk to test |
|---|---|---|---|
| A — Source-first | Extract within each document or speaker, then reconcile and associate with problems. | Preserves provenance, historical context, and outside opinions. | Duplication, verbosity, and missed links across sources. |
| B — Meaning-first | Organize source-linked statements into observations/history, clinical interpretations/relationships, and management statements. | Directly addresses blended evidence, interpretation, and actions. | Misclassification or fragmentation that detaches modifiers. |
| C — Assessment-guided | Start with provisional problems from the clinician's assessment, gather related information, then independently scan for unmatched and contradictory material. | May yield coherent problem-oriented output efficiently when the assessment is explicit. | Anchoring, lost independent problems, missing counterevidence, and forced grouping. |

All three use the same source-fidelity rules, packets, output requirements, and evaluation criteria. The initial organizing approach is the main experimental variable. Hold reconciliation and architecture instructions constant during the initial extraction comparison.

For C, the independent scan for unmatched and contradictory material is mandatory. The clinician's assessment guides retrieval; it does not authorize discarding conflicting reports.

Meaning-first extraction is the leading hypothesis for the reported failures involving altered causal targets, mixed interpretations/actions, and lost management modifiers. It must earn selection through testing. No method is preferred solely because it produces a shorter response.

## Test design

### Progress from isolated cases to realistic encounters

1. Construct synthetic cases that isolate one challenge.
2. Combine challenges to test interactions.
3. Evaluate original encounter packets with manually reviewed expectations.
4. Keep some cases unused during prompt revision to evaluate generalization.

Repository data must remain synthetic or fully de-identified under `AGENTS.md` and D-010. Do not commit real encounter text. Any later reference to an original encounter means its permitted de-identified representation for repository storage.

### Initial test families

| Capability | Challenge | Expected handling |
|---|---|---|
| Extraction | One sentence includes a finding, interpretation, and action. | Preserve each without blending their meanings. |
| Extraction | An action has timing, condition, owner, and patient preference. | Preserve each material modifier without upgrading its state. |
| Extraction | Two potential causal targets occur close together. | Attach the cause to the source-supported target. |
| Reconciliation | An old note says worsening; no current status update exists. | Do not make old worsening current. |
| Reconciliation | Patient, outside service, and current clinician express different positions. | Preserve source-specific positions without silent adoption. |
| Reconciliation | A later statement explicitly corrects an earlier one. | Distinguish supersession from unresolved conflict. |
| Architecture | A symptom is an established manifestation in one version and has an uncertain relationship in another. | Change containment only as justified by that relationship. |
| Architecture | Two diagnoses are alternative explanations in one version and additive contributors in another. | Preserve the distinction in the proposed structure. |

These describe tests to synthesize later; they are not completed fixtures or reviewed answers.

### Paired changes

Change one meaningful element while holding the rest of a packet constant:
- Possible contributor → likely contributor.
- Recommended → ordered.
- Prior neurologist's opinion → current clinician's assessment.
- Established consequence → relationship uncertain.

Specify the expected output change and the content that should stay the same. A changed word does not automatically require a changed block count; the rest of the clinical context still controls.

Also test irrelevant changes: document reordering, copied text, and unrelated chart detail. These should not change the clinical meaning unless new relevant information is introduced.

## Running the comparison

- Use the same fixed cases and reviewed expectations for every candidate.
- Initially focus evaluation on extraction fidelity, while holding reconciliation and architecture instructions constant.
- Record omissions, invented assertions, altered relationships, temporal/attribution errors, and changed management details separately.
- Evaluate concision and physician review burden after checking fidelity.
- Repeat identical tests in fresh Doximity conversations where available.
- Keep available settings constant; record the template/prompt version, packet version, settings, and exposed model/version information. Mark unavailable runtime details as unavailable.
- Preserve every raw output, including failed repetitions.
- Do not use one overall score to hide a consequential error among many correctly retained minor details.
- Structural checks verify fields, references, and formatting; they cannot certify clinical fidelity.
- Local runs or mocks are development evidence only. Doximity acceptance requires actual Doximity outputs under the evidence boundary in `DOXIMITY.md`.

Before each comparison, define its specific success criteria and repeat count. A single good result is insufficient, and finite passing tests do not establish zero hallucination risk.

## Refinement and development record

After comparing broad methods, refine the most promising approach against observed failures. Change one rule or a tightly related group per revision, use a minimal reproducing case, and rerun earlier tests to check regression.

Keep the record small:
- One current version per candidate during comparison, with prior versions recoverable.
- Fixed source packets and reviewed semantic expectations.
- Raw outputs and per-run findings.
- A short failure log.
- A method-selection rationale that includes remaining errors and review burden.

Each failure records: source passage/reference; expected handling; prohibited handling; actual output; prompt and packet version; run; responsible capability when identifiable; correction and regression result. Mark uncertain responsibility rather than forcing attribution.

Once extraction is dependable on the agreed suite, intensify reconciliation and architecture testing while preserving the accepted extraction approach. Test the combined workflow afterward to detect interactions or regressions.

## Immediate next experiment

Synthesize comparable A, B, and C prompts and a small shared set of targeted synthetic packets with reviewed semantic expectations. Define the comparison criteria before running them. The user will run the Doximity experiments; record and compare the raw results.

The present task records the approved plan only. Prompt synthesis, case creation, model execution, method selection, and pipeline implementation remain subsequent work.
