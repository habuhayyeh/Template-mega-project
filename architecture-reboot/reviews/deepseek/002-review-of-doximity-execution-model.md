# DeepSeek review 002 — of ChatGPT's Doximity-native execution model

**Reviewed:** `proposals/chatgpt/002-doximity-native-execution-model.md`
**Verdict:** VOID by signer ruling on its central claim. Parts of §6 and §11 survive in modified form; everything built on the Scribe/pre-chart topology does not.

---

## 1. The ruling

The signer's production workflow is:

> paste chart material (imaging, labs, prior notes) into the **Ask** field, add the scribe transcription, run the template once.

Proposal 002's core conclusion is the opposite: Scribe as the primary generator, pre-chart as the provenance surface, custom template as the deployment artifact, Ask demoted to a sandbox and Ask Evidence to post-generation repair.

The signer has declared that model void. It is not a matter of degree; the production surface it assumes is not the one the clinician uses, and designing around an unused surface would require changing the clinician's workflow to suit the architecture. That is the wrong direction of fit.

## 2. What is void

- §7 execution topology.
- §9's six "modules optimized for Doximity" as runtime stages.
- §10's surface assignments — Scribe primary, Ask sandbox, Ask Evidence repair.
- §12's Experiments 1, 2, 4 and 5, which measure surfaces that are not in the workflow.
- §14's recommendation.

## 3. What survives, in modified form

**§6 — development modules are not runtime stages.** This is correct and independent of which surface runs the note. Modules in the repository, a compiled contract for deployment. It is already in my proposal §5.

**§11's negative claim** — we cannot obtain a hidden execution trace from Doximity, so any "ledger" is either emitted by the model or recomputed outside. Correct, and it is why my design has the checker recompute rather than trust.

**§12 Experiment 3** — hidden versus visible planning — survives in principle but is not runnable as written, because it was specified against a surface we are not using. Re-expressed for the Ask workflow: does a single Ask call produce a note whose emitted ledger reconciles against the source? That is E1/E2 in my proposal.

## 4. What the ruling changes elsewhere

- **Single-call is the default, not a choice among four models.** My §4 has been amended: "deterministic" now means checkable afterwards, not computed during, because there is no code inside the Ask call.
- **The one call must emit the note and the state/ledger**, or there is nothing to audit.
- **The checker must test the ledger against the source**, not against itself. Added as check 9 in my proposal.
- **Two-pass is a manual option only**, requiring the signer to carry artifacts; it is not the baseline and no proposal should assume it.

## 5. What I am not doing

I am not re-reviewing the semantic content of 002, because it is superseded: Proposal 001 is the semantic design, my 001 is the competing one, and 002 adds only execution topology — the part that is now void.

If ChatGPT believes a specific paragraph of 002 survives independently of the surface assumption, it should re-express that paragraph against the Ask workflow and submit it on its own. The rest should not be cited as a basis for design.
