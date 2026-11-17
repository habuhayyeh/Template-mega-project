# Clinical reference checks — post-synthesis use

**Evidence class:** OBSERVED
**Date:** 2026-11-16
**Scope:** Doximity clinical tools used after synthesis, before the final note.

## Purpose

Use Doximity's clinical reference tools to check medication and guideline claims **after** synthesis. They are
not source evidence and must not enter the coverage census or change patient facts.

Useful tools observed:

1. Doximity Drug Monographs — indications, dosing, interactions, warnings, pregnancy/lactation.
2. Clinical literature/reference search — guidelines, journals, consensus statements.

Not useful for this pipeline: physician-profile lookup, Amion scheduling.

## Rules

1. Run after synthesis, before final note approval.
2. Deidentify all inputs. No PHI.
3. Check only claims already produced by synthesis; do not ask for new patient facts.
4. Output JSON with a verdict and citation.
5. No citation means `unverified`.
6. `unsupported` or `unverified` goes back to synthesis for a new version; do not silently rewrite.
7. Reference-check output is not packet evidence and does not belong in coverage.
8. If the tool is unavailable, return `NO_TOOL`.

## Example 1 — Drug Monograph check

```text
You are a medication reference checker. Do not write note text. Do not add patient facts.

Use Doximity Drug Monographs only. If that tool is unavailable, return NO_TOOL.

Check these claims:

M1: Levetiracetam has no clinically significant interaction with combined oral contraceptives.
M2: Levetiracetam requires renal dose adjustment when creatinine clearance is below 50 mL/min.

Return only JSON:

{
  "checks": [
    {
      "claim_id": "M1",
      "verdict": "supported | unsupported | uncertain | unverified",
      "source": "<label or monograph name>",
      "section": "<interactions | dosing | warnings | pregnancy>",
      "correction": "<one line or NONE>"
    }
  ]
}

No prose. No citation, no support.
```

## Example 2 — Literature/reference check

```text
You are a guideline reference checker. Do not write note text. Do not add patient facts.

Use clinical literature/reference search only. If unavailable, return NO_TOOL.

Check this claim:

G1: For adults with a first unprovoked seizure, EEG and MRI are recommended as part of the initial evaluation.

Return only JSON:

{
  "checks": [
    {
      "claim_id": "G1",
      "verdict": "supported | unsupported | uncertain | unverified",
      "citation": "<organization, title, year, DOI/PMID/URL>",
      "applicability": "<one line>",
      "caveat": "<one line or NONE>"
    }
  ]
}

No prose. No citation, no support.
```

## Integration

```text
Scribe packet -> coverage -> synthesis -> reference check -> final note
                                             |
                                             +-> unsupported/unverified -> synthesis revision
```

Do not route reference-check output into coverage. Do not let a guideline answer become a patient-specific
fact.
