# P003 v3 review — original architecture branch

**Reviewer:** ChatGPT (original architecture branch)  
**Proposal:** `proposals/P003-ap-render.md` v3  
**Verdict:** **REVISE — one material ETIOLOGY correction; all other P003 v3 changes accepted**

## Accepted

P003 v3 resolves the four v2 objections:

- relevance gate precedes COURSE classification;
- STANDING_ITEMS are valid traced output sources;
- non-clinician speaker attribution is preserved mechanically;
- transformation 8 is accepted as a bounded signer-style normalization:
  written number -> numeral, minutes/hours -> mins/hrs, about/approximately -> ~.

The transformation-8 exception does not weaken the clinical no-invention rule because it changes display only, not semantic quantity or certainty.

Also accepted:

- STATUS / MODIFIER / INDEPENDENT / IRRELEVANT COURSE architecture;
- facts before reasoning;
- three independent fresh-context runs;
- I1-I10 including O# pairing and placement;
- no semantic reordering beyond the stated deterministic order;
- O54 body-only;
- AP_ANCHOR update removing separate-ETIOLOGY import into the problem line.

## One remaining blocker — ETIOLOGY suppression is too broad

Current rule:

> suppress ETIOLOGY when the claim already expresses the same causal meaning.

That can delete exactly the explicit clinician reasoning D-004 protects.

The signer has repeatedly said the A/P should preserve the clinician's actual etiologic reasoning, even when the problem line already names the favored cause. A separate ETIOLOGY statement can add clinically meaningful content beyond the causal noun phrase:

- degree of certainty: likely / plausible / most likely;
- mechanism: epileptogenic substrate / scar;
- why it fits;
- why another explanation fits less well;
- a contrast or uncertainty.

Example:

PRIMARY_CLAIM:
`suspected post-stroke epilepsy`

ETIOLOGY:
`the chronic left MCA infarct is a plausible epileptogenic substrate`

These share a cause, but the ETIOLOGY adds explicit clinician reasoning and should survive.

### Required rule

Use:

1. **Suppress only if the ETIOLOGY adds no distinct reasoning content beyond the causal meaning already fully expressed in PRIMARY_CLAIM.**
2. **If ETIOLOGY adds certainty, mechanism, rationale, contrast, or uncertainty, render it as reasoning even when the claim names the same cause.**
3. Never import separate ETIOLOGY into the problem line.
4. Never synthesize new reasoning from evidence.

For the frozen case:
- claim: `post-stroke seizure from the old left MCA scar rather than a new lesion`
- etiology: `scar from your old stroke is the most likely cause of the seizure`

Whether this exact pair is redundant can be decided under the new rule: if the ETIOLOGY contributes only the same cause/certainty already fully present in the claim, suppress; if it contributes a distinct certainty statement not carried by the claim, retain. The important point is that "same cause" alone is not enough to delete clinician reasoning.

This is a direct D-004 protection, not a new architecture.

## P003 v4 requested

Revise only the ETIOLOGY suppression language above. Everything else in v3 is accepted.

Do not implement `05` or `AP_ANCHOR.md` until v4 is reviewed and the user approves.

---

## Separate review: DOXIMITY.md

The new root document is useful, but it needs one evidence-boundary correction before we rely on it as the shared runtime model.

### A. Separate actual Doximity evidence from local mock evidence

`runs/2026-11-14-p002/ap_run1.txt` and `ap_run2.txt` are local/mock LLM runs, not Doximity runs. Their formatting/selection drift demonstrates that the `05` contract is unstable under an LLM, but it does **not** directly establish a Doximity runtime limitation.

Split the document into:

**Observed in actual Doximity**
- semantic routing instability across the three 06 runs;
- schema non-compliance in run 3;
- non-local prompt sensitivity / regression after prompt edits.

**Observed in local/mock execution**
- 05 formatting/selection drift on identical Handoff input.

Keep the inference that Doximity may show similar prose-stage instability clearly labeled as an inference until tested there.

### B. State the evidence-coverage gap explicitly

The canonical repository currently exposes only three raw Doximity `06` runs under `runs/2026-11-14-06-doximity/` plus scored/history artifacts.

The earlier conversational-wrapper issue is only summarized in imported history; its five raw suppression-test outputs are not present in the current canonical repo.

Therefore add:

> This repository does not yet contain every historical Doximity test the signer recalls. Claims here are limited to the raw artifacts currently present; missing historical tests should be imported before they are treated as canonical evidence.

Do not imply that both agents currently have raw access to all prior Doximity testing.

### C. Preserve the strongest design conclusion

The strongest evidence-supported runtime lesson remains:

> More prompt prose is not automatically a fix. Doximity errors moved non-locally across runs, and one prompt correction caused a different routing regression. Distinguish prompt/contract defects from platform/model stochasticity before adding rules.

That should remain prominent.

No user action is required for the P003 logic. For the broader runtime evidence inventory, if additional raw historical Doximity tests exist outside the repo, we should eventually import them rather than rely on recollection.
