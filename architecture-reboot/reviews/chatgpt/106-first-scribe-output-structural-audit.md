# ChatGPT review 106 — first Scribe output structural audit

## Scope

A user-provided Scribe output was inspected in chat. The clinical content itself is **not committed to the repository**. Raw prechart/transcript input is not yet available here, so this review can assess only output structure and visible provenance behavior, not omission/coverage fidelity.

No architecture or contract change is authorized.

## Findings

### 1. Source-first organization is viable
The output preserved the current encounter transcript as a large ordered source block and kept the ED note as a separate supplied source. Attribution, chronology, uncertainty, pertinent negatives, and explicit clinician reasoning were generally retained in a form that appears usable by Ask.

### 2. The baseline prompt causes cross-source duplication
Because it requests both source-family blocks and normalized sections such as imaging, labs, medication/treatment, and collateral, the output restates facts that already appeared in the transcript/ED source blocks.

This creates:
- multiple representations of the same clinical proposition;
- extra Ask token burden;
- risk that one copy is paraphrased differently from another;
- a new deduplication problem downstream.

### 3. Embedded/mentioned sources can be incorrectly promoted to direct sources
The output created an apparent standalone source block from documentation that was only described/reviewed inside another supplied note. Likewise, collateral already present in the transcript was re-emitted as a separate collateral source block.

General rule needed:
> a source mentioned, quoted, or summarized inside a supplied source is **nested provenance**, not a separately supplied source unless its actual text was independently provided.

### 4. Some local semantic organization is acceptable; cross-source semantic reorganization is not
Within one supplied source, headings such as event chronology or exam/MDM can improve readability while preserving order. The risk begins when Scribe re-groups facts across sources or re-labels them as a new source.

### 5. Visible inferential repair occurred
At least one garbled clinician statement was accompanied by an explanatory interpretation of its apparent intent. That is useful to a reader but crosses the source-preservation boundary. The safer behavior is to preserve the garbled/uncertain statement and mark uncertainty rather than repair intended meaning.

### 6. Compression behavior cannot yet be evaluated
The Scribe output is roughly 16.8 KB, but raw input length is unknown. We therefore cannot determine:
- compression ratio;
- omitted information;
- qualifier loss;
- whether near-limit behavior is safe;
- whether the current output is materially smaller than the raw source.

## Prompt correction suggested by this run

For the next Scribe baseline:
- emit each **supplied source exactly once**;
- keep embedded/quoted sources nested under the supplied source that reported them;
- do not create cross-source imaging/lab/medication/collateral summaries unless those were standalone supplied sources;
- allow local within-source compression/organization;
- preserve uncertainty rather than interpret garbled intent;
- no final cross-source synthesis.

## Evidence still required

Need the raw material that produced this Scribe output, or a fully de-identified equivalent, to score:
- omissions;
- additions;
- source attribution drift;
- qualifier distortion;
- chronology;
- contradiction preservation;
- duplicate handling;
- compression ratio.

## NEXT

Obtain the raw prechart + transcript for this run (synthetic or fully de-identified for repository use). Then perform raw->Scribe fidelity audit before changing the architecture or freezing the Scribe->Ask contract.
