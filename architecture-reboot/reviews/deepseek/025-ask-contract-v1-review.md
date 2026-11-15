# DeepSeek review — Ask semantic contract V1

**Reviewed:** `proposals/chatgpt/119-ask-semantic-contract-v1.md`
**Status:** review only; no implementation.

## Verdict

**ACCEPT with three small clarifications.** The contract is compact and directionally right. It does not
need another ontology or a larger scoring grid.

## Material ambiguity to fix

### 1. Problem identity is being conflated with encounter relevance

Rule 2 says:

> Create a separate problem only when the item has an independent clinical identity **in this encounter**.

That imports relevance into identity. The accepted five-domain model separates:

- IDENTITY — is this an independent problem at all, or a contained manifestation?
- RELEVANCE/ROLE — does it render in this note, and is it PRIMARY or BACKGROUND?

A historical independent problem can be real but `BACKGROUND` or `NOT_RENDERED`. It should not be
excluded from the ledger merely because it is not currently active.

Change to:

> Create a separate problem only when the item has an independent clinical identity, not merely a
> manifestation of an existing problem. Whether it renders, and whether it is PRIMARY or BACKGROUND, is
> a separate RELEVANCE/ROLE decision.

This also makes `NOT_RENDERED` coherent: an independent problem can be listed in the ledger and still
not receive an A/P block.

### 2. “Use only supplied patient-specific facts” is too strict for clinical reasoning

The final-note rule says:

> use only supplied patient-specific facts plus clinical conclusions traceable to those facts

Ask is supposed to reason. General medical knowledge is not a patient-specific fact. The intended rule
is:

- patient-specific facts must come from the packet;
- clinical reasoning may use general medical knowledge;
- no invented patient-specific facts, no unsupported patient-specific conclusions.

Add that distinction explicitly. Otherwise the model may refuse ordinary diagnostic reasoning or, worse,
treat general knowledge as an invented fact.

### 3. Add an explicit ledger/note boundary

The contract says return two parts but does not define a separator. A template with headings can blur
the ledger into the note.

Add:

```text
AUDIT LEDGER
...
--- END AUDIT LEDGER ---
FINAL NOTE
...
```

State that the ledger is not part of the note and must not appear in the final output.

## Smaller clarifications

- `NOT_RENDERED` means “independent problem, no own A/P block,” not “not a problem.” State that.
- `contained:` is a summary of important manifestations/evidence, not a second problem list. Do not let
  it become a dumping ground.
- Preserve disagreement/uncertainty in the final note, not only in the ledger. Rule 1 already says this;
  make it explicit in the FINAL NOTE rules.
- The self-check is fine; keep it short. Do not add more gates.

## What I would not change

- no frozen STATE enum;
- independent-problem-only ledger;
- plain-language stance;
- role separate from causality;
- source-supported relation fidelity;
- neurologic focus;
- no sentence-level provenance markup;
- impersonal A/P voice;
- compact contract.

## Readiness

With the three clarifications, the contract is ready for the first P/N run. No Scribe reopening, no new
ontology, no Gate-0 acceptance, no Doximity production change, no Phase 0.
