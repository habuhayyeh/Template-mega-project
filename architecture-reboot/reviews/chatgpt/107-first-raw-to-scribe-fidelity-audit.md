# ChatGPT review 107 — first raw-to-Scribe fidelity audit

## Scope

The user supplied the raw production-shaped input corresponding to the previously inspected Scribe
output. The clinical source material itself is not committed to the repository. This review records
only abstract transformation findings.

No architecture, contract, schema, or prompt is changed here.

## Strong findings

### 1. Source-first compression is feasible

The raw transcript is highly conversational, repetitive and partially garbled. Scribe compressed it
substantially while preserving the major event chronology, eyewitness attribution, semiology,
clinician uncertainty, diagnostic plan, treatment discussion and pertinent historical/collateral
information.

This supports using Scribe as an upstream compression/organization surface rather than forcing Ask to
consume the verbatim transcript.

### 2. The final note template is contaminating the ingestion surface

The raw prechart packet contains:
- explicit meta-instructions about how prechart should be used;
- the final USF neurology note template;
- then the ED note.

Scribe subsequently extracted some template content as if it were chart/list-derived information
(e.g., home meds/allergies) while correctly ignoring much of the default normal neurologic exam.

This is unsafe by construction: a future Scribe run could treat prefilled template statements as
clinical evidence.

**Recommendation:** the final note template belongs in Ask, not in Scribe's evidence input. If Doximity
requires it in Scribe for some product reason, it must be strongly fenced as NON-EVIDENCE / OUTPUT
SCHEMA ONLY, but exclusion is preferred.

### 3. Scribe preserves high-value neurology semantics surprisingly well

Visible preservation includes:
- two-event chronology and stop-go cluster behavior;
- source-specific descriptions from fiancé, patient/mother and paramedic brother;
- preserved uncertainty in event laterality;
- explicit uncertainty over epileptic vs nonepileptic events;
- inpatient EEG/MRI plan;
- temporary Keppra plan;
- LOC safety counseling;
- historical zoning-out descriptions and clinician uncertainty.

This suggests Ask may not need to reconstruct chronology from raw dialogue if Scribe is prompted
carefully.

### 4. Some low-value conversational content is safely removed

Scribe omits greetings, repeated confirmations, conversational repair, family logistics and much
nonclinical filler. This is desirable compression.

### 5. Some clinically plausible details are also omitted

Examples include some lower-priority trigger/risk-factor questioning and individual conversational
details. Without a formal coverage ledger we should not yet declare recall sufficient.

Important principle:
> omission should be judged by whether Ask loses a proposition needed for clinical reasoning or note
> fidelity, not by raw transcript word coverage.

### 6. Scribe performs interpretive repair on garbled speech

At least one partially garbled clinician aside was emitted with an explanatory statement of the
speaker's apparent intent. That crosses from faithful compression into interpretation.

Prompt should require:
- preserve the recoverable statement;
- mark unclear/garbled portions as uncertain;
- do not supply the intended meaning unless explicitly supported elsewhere in the same source.

### 7. Scribe introduces duplicate cross-source summaries

After source blocks, it re-emits imaging, labs, medication/treatment and collateral information in
cross-source sections. This adds token cost and creates multiple paraphrases of the same proposition.

**Recommendation:** each supplied source appears once in the production evidence packet. Cross-source
normalization belongs in Ask unless a specific downstream experiment shows a benefit.

### 8. Scribe can promote nested provenance into false direct provenance

The ED note reports having reviewed cruise paperwork. Scribe later creates a standalone
"cruise ship documentation" source section, even though that document was not independently supplied
in the raw packet.

General rule:
> a source quoted, summarized or referenced inside another supplied source remains **nested provenance**
> under that supplied source. It does not become a direct source unless its own text was independently
> provided.

The same issue applies to family collateral already contained within the transcript.

### 9. Current source-family boundaries need one refinement

The first baseline should distinguish:
- **DIRECT SUPPLIED SOURCE** — actual transcript, actual ED note, actual imaging report, actual lab
  source, etc.;
- **NESTED/REPORTED SOURCE** — cruise paperwork summarized by ED, EMS report quoted by ED, family
  statement inside transcript.

This may be enough provenance structure; no segment-ID ontology is yet justified.

## Provisional production flow after this evidence

RAW CURRENT TRANSCRIPT
+ DIRECT PRECHART/CHART SOURCES
    |
    v
SCRIBE
- faithful compression
- preserve direct-source blocks
- preserve nested attribution
- no final template
- no cross-source synthesis
- no problem/causal/current-state adjudication
    |
    v
ASK + FINAL NOTE TEMPLATE
- semantic reconciliation
- problem model
- current-state/adoption
- relations/causality
- note-use
- final rendering

## What remains unresolved

We still need the exact Scribe prompt used for this run before attributing the observed behaviors to:
- Doximity defaults;
- the custom prompt;
- inline prechart instructions;
- the final template itself.

The prompt is therefore the next required evidence.

## NEXT

Obtain the exact Scribe prompt used for this run. Compare prompt clauses against the observed:
- strong chronology/attribution preservation;
- template contamination;
- cross-source duplication;
- nested-source promotion;
- interpretive repair.

Then draft the smallest V2 prompt and rerun the same raw case for an A/B comparison.
