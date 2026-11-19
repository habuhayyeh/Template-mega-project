# Source-preserving packets and physician-review worksheets

## Status and evidence boundary

This is the decision record for the staged neurology A/P workflow discussed on November 18, 2026. It preserves agreed project constraints and candidate design lessons, not newly established universal Doximity capabilities.

Classification: **DESIGN CONSEQUENCE / DEVELOPMENT BASELINE**. Unless individually stated below, these are architecture decisions, not controlled model-performance findings. No new repeated-run or deterministic-performance claim is made.

The latest supplied source-packet example was inspected during this update. It visibly contains a source index, passage IDs, source-text blocks, navigation headings, three input layers, and source/organization limitations. That observation establishes the presence of those features in that example; it does not certify complete coverage, verbatim copying, correct speaker identity, or source fidelity.

The exact Step 1 V2 prompt was not recoverable for this repository update. Its identifier and agreed interface are recorded here, but **no reconstructed prompt is represented as the frozen original**. Exact per-version run counts and full prompt/output pairings for the earlier iterative trials are not established here. Under [13-TEST-PROMPT-TRACEABILITY.md](13-TEST-PROMPT-TRACEABILITY.md), those trials remain unverified for new empirical claims.

No patient transcripts, clinical case passages, chart records, names, or patient-specific outputs are included in this update.

## 1. Accepted development sequence

```text
Original sources
    |
    v
Step 1 V2: source-preserving organization
    |
    v
Step 2 V1 candidate: proposed problem-review worksheet
    |
    v
Physician edits, discrepancy resolution, and approval
    |
    v
Future validated structured handoff / compilation
    |
    v
Final A/P renderer: approved wording and order only
```

Develop one boundary at a time. Do not simultaneously redesign extraction, reconciliation, problem architecture, clinical wording, approval, and rendering.

The source packet is a recovery aid, not an adjudicated clinical model. The worksheet is a review surface, not a deterministic machine contract. Approval is a later event, not something inferred from a well-formatted output.

This sequence does not establish the optimal number of calls, production performance, or a completed implementation.

## 2. What is frozen now

- **Step 1 V2 prompt and output format:** frozen as the development baseline while Step 2 is developed. Output identifier: `NEUROLOGY_SOURCE_PACKET_V2_CANDIDATE`.
- **Step 1 interface:** source index, three input layers, navigation headings, source-preserving passages with IDs, and material organization limitations.
- **Individual patient packets:** not certified or permanently frozen. Factual and provenance corrections remain permitted.
- **Original sources:** remain the source of record.
- **Step 2:** `NEUROLOGY_REVIEW_WORKSHEET_V1_CANDIDATE`, a candidate for testing; not approved or validated.
- **Final compiler/renderer contract:** not completed or validated by these decisions.

Freeze means stop moving a component while developing the next component. It does not mean ignore a consequential defect. Record the defect, correct the affected packet, and change the baseline only through an explicit versioned decision. Preserve the old prompt if a replacement is adopted.

Do not confuse this development freeze with clinical approval or a later exact-wording freeze.

## 3. Step 1: preserve recoverability, not clinical conclusions

Organize supplied material into three source containers:

### A. Encounter transcript

Preserve symptoms, chronology, reported treatment response, preferences, and clinician statements made during the encounter. Keep patient report, caregiver observation, and clinician speech distinguishable when the source supports that distinction.

Raw speaker labels are source labels, not reliable person identities. Do not assume that one numbered speaker remains the same clinical participant throughout a transcript. Preserve ambiguity rather than inventing attribution.

### B. Chart material

Preserve document identity, service, date, and explicit source status. Keep pre-visit material labeled as pre-visit, even if it carries the encounter date. Keep nested provenance: a note reporting a test result is not the original test report.

Historical examination, control, adherence, doses, recommendations, and execution states do not become current merely because they are present in the packet. Templates, placeholders, and boilerplate are not proof that the described care occurred.

### C. My separately supplied current assessment / exam / plan

Use this container only for separately supplied material. Do not silently duplicate or promote transcript speech into a separately supplied assessment.

Absence of Layer C does not prove that there are no clinician assessment statements in the transcript. Step 2 may use clearly attributable transcript statements with their actual provenance.

### Navigation and passages

Navigation headings answer where content can be found, not what it proves. A heading does not establish diagnosis, adoption, causation, or final Plan membership.

Keep passage IDs stable within a packet and retain one canonical source passage for reuse. Record packet revisions when editing passages; an ID alone does not certify immutable content.

Do not describe a packet as lossless, complete, or verbatim without an appropriate source comparison. Some residual conversational noise is not, by itself, a reason to redesign the whole pipeline.

## 4. Step 2: organize around the physician's formulation

Start with the physician's current formulation, then check the rest of the packet for meaningful omitted problems, material counterevidence, and management.

A current formulation anchors organization; it does not overwrite conflicting objective reports. Distinguish an adopted diagnosis from an option discussed with the patient, a patient-reported diagnosis, an outside assessment, and a historical diagnosis.

Create supported neurologic problem identities, not a problem for every mentioned symptom, test abnormality, exposure, stressor, or counseling topic. Preserve uncertainty. Use a presenting syndrome if no disease is favored.

Keep established manifestations within the parent problem; distinct downstream disorders may remain separate. Do not infer causation merely by placing a finding under a heading. Routine continuation or surveillance does not automatically make a problem Primary.

This worksheet deliberately does not ask the physician to review every internal semantic field.

## 5. Six visible sections and an approval state

Each problem exposes:

1. **Problem heading and role:** proposed final claim, certainty/qualifiers, and Primary/Background role.
2. **Status:** supported current condition, control, trajectory, or established consequence.
3. **Evidence:** minimum sufficient source-supported facts, including material counterevidence.
4. **Interpretation:** supplied synthesis, differential, or causal formulation, when nonredundant.
5. **Actions:** proposed wording that preserves source-supported decision and execution states.
6. **Needs review:** specific issue and decision needed, not a numerical confidence score.

Each problem also has **Review status**, initially Unreviewed. Only physician review can change it to Approved.

Use a single encounter-level **Unassigned / needs review** list for relevant content that cannot be confidently placed. This is not a dump of every excluded source detail. Facts appropriately retained only in other note sections need not appear in the A/P.

A compact source reference is necessary but insufficient: it must support the wording actually proposed. Keep original passages accessible outside the visible worksheet.

## 6. Fidelity rules that prompted the staged design

These are requirements for the candidate workflow, not claims that the model now reliably meets them.

- Separate documented content from proposed organization.
- Preserve supplied reasoning; do not generate new diagnostic or causal links.
- Preserve outside-service attribution unless the current physician adopts the formulation.
- No automatic plan completion from disease labels.
- No automatic carry-forward of old status or actions.
- Preserve clinically meaningful negatives, uncertainty, chronology, and ownership.
- Distinguish recommendation, order, scheduling, performance, completion, and result availability.
- Distinguish patient preference, refusal, and clinician deferral.
- Preserve meaningful conditions and pending approval. Anticipated clearance is not clearance.
- Retain material counterevidence; first consider time, source, and assertion type before labeling a conflict.
- Avoid redundant interpretation bullets and fully duplicated shared actions.
- Flag material safety/document-integrity concerns separately; do not turn uncertain or unsafe source text into an endorsed directive.

Generic action-state example: “Investigation indicated; patient prefers outpatient” supplies neither an order nor a refusal nor an appointment.

## 7. Source access before approval versus after approval

During worksheet preparation, available original sources may be consulted to resolve incomplete or ambiguous passages. If unavailable, state the specific limitation. Do not imply they were reviewed.

During final deterministic rendering, clinical source fallback is prohibited. The renderer must consume only the approved complete payload and fixed formatting rules. Missing approved content must stop or flag the affected rendering rather than trigger fresh extraction or clinical interpretation.

This distinction is compatible with [11-IN-PROMPT-HANDOFF.md](11-IN-PROMPT-HANDOFF.md): semantic review may reopen evidence; an approved render-only handoff may not.

## 8. Human-readable review is not machine serialization

The worksheet is intentionally editable prose. Do not treat it as evidence that Doximity can supply a reliable arbitrary nested schema or that another LLM can deterministically infer all missing fields from it.

Existing handbook guidance remains in force: JSON for model-authored structured handoffs; no custom `@@` output records, pipe delimiters, or fragile bracket sentinels.

The archived Step 2 candidate uses bracketed source references. Their transport/display stability is **not validated** by this update. Preserve this candidate as issued; if a change is needed, version it rather than silently editing the historical prompt.

A future deterministic handoff must explicitly preserve actual approved heading/bullet wording, placement, order, source links, approval state, and approved cross-references. Required structural fields and validation behavior still need specification. Do not introduce an unapproved schema during this documentation update.

## 9. How to continue without another all-at-once redesign

Use a reviewed Step 1 packet as fixed input while developing Step 2. Evaluate Step 2 against problem eligibility, attribution, status fidelity, evidence/counterevidence, supplied reasoning, action states, and useful review flags.

Separate failures into:
- Upstream source/coverage defects.
- Worksheet organization or wording defects.
- Future serialization/rendering defects.

Change the smallest responsible component. Do not call every wording difference a model failure; do not call a plausible output deterministic.

For subsequent tests, preserve the full exact prompt, packet version, run count, output location in an appropriately protected environment, observed defects, and physician adjudication. No patient-level material belongs in this handbook.

Doximity remains the chosen workflow tool. The practical objective is a manageable, source-faithful review burden and controlled downstream behavior, not a capability debate disconnected from that constraint.

## 10. Prompt archive and open items

- Step 1: `NEUROLOGY_SOURCE_PACKET_V2_CANDIDATE`; frozen by project decision; exact prompt **not archived here** because it was not recoverable during this update.
- Step 2: [NEUROLOGY_REVIEW_WORKSHEET_V1_CANDIDATE.txt](prompts/NEUROLOGY_REVIEW_WORKSHEET_V1_CANDIDATE.txt); full prompt as issued in the conversation, not a replacement revision.
- Step 2 execution evidence: no valid execution of this exact candidate is established in this update.
- Structured approval handoff, fail-closed validation, and final renderer: future work, not certified.
