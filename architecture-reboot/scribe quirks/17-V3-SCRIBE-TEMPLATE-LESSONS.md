# Scribe template-writing lessons from V3

**Recorded:** 2026-11-26. **Evidence:** OBSERVED results plus explicitly labeled DESIGN CONSEQUENCES. This update imports lessons from a separate project, not its architecture or runtime contracts.

## Scope and gap audit

Compared handbook chapters 01–08 and 10–16 at `ae34d2ffb19edc1a5ff19533edd7feb294d78073` with the V3 D2.1–D2.4 J01 reviews. Chapter 09 concerns external clinical-reference checks and is outside this template-writing audit. No new Scribe execution occurred during this documentation update.

The existing handbook already covers atomic imperatives, read-all gates, function ownership, source-qualified action wording, schema-completion pressure, coverage before synthesis, semantic self-check failures, valid-ID versus semantic support, and function boundaries versus file count. Those are established documentation, not newly discovered quirks.

| Point from the V3 lessons | Existing coverage | Missing or newly qualified documentation |
|---|---|---|
| Concrete operations and explicit boundaries | 01, 03, 04, 05 | Reinforced, not new. B+ is the selected V3 instruction style; the D2 revisions do not isolate its causal contribution. Historical fixed-payload render results do not prove reliable free Scribe extraction. |
| Explicit source authority | 04, 16 preserve source/time/ownership | Direct Scribe observations now show consistent retention of the supplied current examination in this limited case. State who owns each input type; do not treat diagnostic inference as an examination source. |
| Concise worksheet, richer supporting reserve | 16 distinguishes review surface from original passages | V3 generates both together. A good worksheet can conceal an incomplete reserve; the two outputs need different inclusion thresholds. Important history/results must survive even when omitted from the editing surface. |
| Literal packaging contract | 06, 07, 11 cover structured Ask handoffs | V3 adds direct Scribe worksheet-plus-JSON examples. This is a deliberately framed combined artifact, not the machine-only JSON output contract tested earlier. |
| Snapshot and anchor correspondence | 13, 16 discuss traceability and passage IDs | D2.1 showed changed snapshot wording and missing passage anchors. Later batches showed better correspondence after shared-passage construction was introduced, with other changes bundled. Snapshot copying is stricter than clinically faithful paraphrasing. |
| Meaningful support, not just resolvable IDs | 01, 03, 05, 16 already require semantic support | New Scribe examples pass mechanical checks while linking a claim to an unrelated record or a current continuation instruction to reported response. Worksheet presence, record presence and correct linkage are separate questions. |
| Preserve final decisions and qualifiers | 01, 16 preserve states, conditions and preference | New paired representations drifted on relative timing and preference versus prerequisite. These are useful transformation boundaries to state explicitly, rather than relying on “preserve meaning.” |
| Avoid expanding the prompt after every defect | 01, 03, 05 reject repeated warnings and unnecessary stages | No controlled evidence shows each helper/checklist improves retention, or that prompt length caused the failures. Simplification is a reasoned design choice, not an established performance gain. |
| Proportionate testing and stopping | 02, 05, 13, 16 distinguish semantics from wording | The V3 policy explicitly separates meaningful reserve/action failures from harmless format variation. A selected usable output permits bounded development; it does not establish repeatable complete capture. |

## What these Scribe runs actually show

1. **Packaging is feasible; completeness remains variable.** Submitted outputs contain an editable worksheet, snapshot, source index, records and anchors. The earlier file-backed batches support mechanical inspection. That does not certify all source meaning survived.
2. **The editing surface is an insufficient coverage test.** Disease duration and dated investigation content disappeared from some supporting reserves while the principal assessment and plan remained readable. A source title or locator alone is not a substitute for usable finding/history content.
3. **Shared-passage construction is a promising packaging discipline.** D2.1 included snapshot wording drift and incomplete anchors. D2.2 had matching wording and complete substantive-passage coverage; two files differed only by one final LF. D2.3 met the prospectively revised structural contract. No isolated comparison establishes that the shared list alone caused the improvement.
4. **Mechanical agreement can preserve the same wrong association.** An anchor and visible citation can agree with each other while both point to unrelated evidence. A correct current action can remain in the worksheet without an explicit current-action record. Do not describe the latter as an invented action or an omission from the entire handoff.
5. **Management qualifiers require protection across every representation.** D2.3 included relative-timing drift and, on independent review, an added availability condition. D2.4's three visible worksheets retained the intended final management, but one reserve lost useful history/results and another lacked the current continuation record. This is observed batch behavior, not proof of a general repair.

## Template-writing guidance

These are DESIGN CONSEQUENCES for the V3 task, not a new mandatory topology for the historical pipeline.

- Give each internal pass a bounded responsibility: allowed input, meaning to preserve, forbidden transformations and output. Function-shaped text controls prompting; it does not execute code or prove the pass ran correctly.
- Use this logical sequence: **read all → capture meaningful source content → resolve explicit corrections and final decisions → synthesize and link → package**. A named source-first pass alone has not guaranteed complete retention.
- Define authority by input type. Preserve supplied current examination as examination; retain spoken clinician assessment/management with its actual source. Do not infer findings from diagnosis or import historical findings as current.
- Limit worksheet evidence to what makes review useful. Retain broader meaningful chronology, disease history, findings, responses, function/family context and management in supporting records for later sections. Do not apply “be concise” as a global deletion rule or demand every incidental detail.
- Preserve preferences as preferences, prerequisites as prerequisites, and relative timing without shifting the interval. Keep referral timing distinct from appointment timing. Resolve a revised decision to its final operative form without inventing an execution state.
- Match references to the actual claim: clinical target, assertion type, reporter, time and qualifier. Reported benefit from an existing treatment is not the current clinician instruction to continue it. Existing IDs and source labels do not establish this match.
- Derive the editable original, snapshot and anchors from one frozen passage representation. Preserve all substantive passages and their mappings. Keep the snapshot unchanged when the clinician subsequently edits the worksheet. This is an instruction contract requiring external checks, not deterministic model execution.
- Preserve source meaning without forcing every fact into every layer. Multiple independently rewritten copies increase opportunities for disagreement; that risk is observed, while its precise cause and best remedy remain unisolated.
- Replace a brittle representation or narrow an overloaded responsibility when failures persist. Do not add synonyms, exhaustive disposition bookkeeping, or another same-context PASS ledger as presumed proof of a fix. Keep useful B+ grouping and source boundaries unless evidence warrants changing them.

## Evaluation boundaries

Check package integrity and semantic fidelity separately. Parsers can test schema, IDs, snapshot identity and anchor coverage. They cannot establish source completeness, correct attribution, or whether a record actually supports a claim.

The V3 contract prospectively permits exactly one terminal framing LF; it does not permit arbitrary trimming, internal changes or paraphrasing of snapshot text. Earlier raw captures and historical judgments remain unchanged. This is a local formatting convention, not a universal relaxation of exact copying.

Important coverage includes material needed for later note sections, not only today's decisions. Conversely, harmless wording, bullet layout, redundant anchors and incidental omissions should not trigger an endless repair cycle when they do not alter useful meaning. Judge a defect's effect in its case; do not turn one fixture's details into universal mandatory fields.

The independent review recommended reducing internal bookkeeping and strengthening meaning-based checks. Those recommendations are not independent execution evidence for a revised prompt. Successive revisions changed several features together; neither simplification, B+ style, source-first ordering nor any individual helper has an isolated measured effect here.

## Traceable evidence

All links below freeze the V3 evidence at `27cbf5ab4ca9b33a5d0be0301139293e9fee86af`. The test case is synthetic. No case passages or raw outputs are copied into this handbook.

| Version | Exact prompt | Submitted outputs | Review and evidence availability |
|---|---|---:|---|
| D2.1 | [Prompt](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/templates/SCRIBE_D2.txt) | 3 | [Review, raw files and provenance links](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/tests/scribe-d2-j01/results/REVIEW.md). User confirmed full prompt, same recording and unchanged supplement. |
| D2.2 | [Prompt](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/templates/SCRIBE_D2_2.txt) | 3 | [Review, raw files and provenance links](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/tests/scribe-d2-j01/results-d2-2/REVIEW.md). Submitted after rerun instructions; exact runtime/input metadata not independently captured. |
| D2.3 | [Prompt](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/templates/SCRIBE_D2_3.txt) | 3 | [Review, raw files and provenance links](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/tests/scribe-d2-j01/results-d2-3/REVIEW.md), qualified by [fresh-context AI review](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/tests/scribe-d2-j01/independent-review/REVIEW.md). Runtime/input metadata not independently captured. |
| D2.4 | [Prompt](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/templates/SCRIBE_D2_4.txt) | 3 inline | [Manual review](https://github.com/habuhayyeh/Grand-doximity-project-V3.0/blob/27cbf5ab4ca9b33a5d0be0301139293e9fee86af/tests/scribe-d2-j01/results-d2-4/REVIEW.md). Originals remain in chat; no byte-identical raw archive or automated parse/hash/snapshot verification is claimed. |

Original audio was not independently inspected. Content review uses the written recording guide and unchanged prechart/examination supplement; the guide does not establish exact recorded speech. Fresh-session independence and exact generation metadata are not established for these batches. Four versions of one case do not demonstrate cross-case generalization. A best working example is not a repeatability result. Full-note generation remains unvalidated.

**Next:** use these bounded findings when reviewing templates; continue the V3 roadmap's controlled note-writer development while carrying reserve-completeness and semantic-link limitations forward. This update changes documentation only; it does not revise runtime templates or report new tests.
