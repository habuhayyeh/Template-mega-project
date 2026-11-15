# Proposal 024 — first Doximity Ask experiment (revised)

**Status:** PROPOSED — experiment design only. No implementation, no patient data in the repo.

## Goal

Test whether Ask, given a V2.2 Scribe packet + a compact semantic contract + the final USF template,
can produce a clinically faithful note while owning IDENTITY, RELEVANCE/ROLE, STATE, RELATIONS and
USE/REALIZATION.

The first run answers four practical questions:

1. Did Ask identify the right independent neurologic problems and keep manifestations contained?
2. Did Ask reach a defensible current stance/role without blindly copying source labels?
3. Did Ask preserve source fidelity and relation/uncertainty boundaries?
4. Did the final note use the evidence appropriately and fit the template?

## Inputs

1. **Scribe V2.2 packet** — provisional frozen baseline.
2. **Compact Ask semantic contract** — five domains as ownership boundaries, not five scored gates:
   - IDENTITY — independent problem or contained information;
   - RELEVANCE/ROLE — render in this encounter? PRIMARY or BACKGROUND?
   - STATE — current encounter stance, preserving uncertainty;
   - RELATIONS — source-supported relation, direction, strength, participants;
   - USE/REALIZATION — selected content, template section, rendering.
3. **Final USF neurology note template.**
4. Raw source only if using the optional comparator.

## Conditions

### P — production candidate
`packet + semantic contract + template`

### N — no-contract baseline
`packet + template`

Optional later comparator:

### R — raw + semantic contract + template
Only when the exact raw source is available and a specific raw-vs-packet question needs answering.
Raw is a comparator, not a fidelity ceiling; it can be noisier and harder to use than the packet.

Do not add a separate provisional-label condition. The STATE rule covers it generally.

## Core STATE rule

> A proposition appearing in any source — transcript, current prechart note, prior note, consultant
> note, problem list, medication list, imaging report, or collateral statement — is source evidence,
> not automatically the final encounter stance. Ask decides the final stance from the whole current
> evidence set, preserving uncertainty.

This covers the encephalopathy/provisional A/P example without a diagnosis-specific guard. If P shows
blind inheritance, add a focused ablation later; do not build it into the first run.

## Ask output

### 1. Problem audit ledger

List **independent problems only**. Contained manifestations belong inside `contained:`, not as
additional PROBLEM records.

```text
PROBLEM <id>
  label: <plain-language problem identity>
  evidence: <source record ids>
  contained: <important manifestations/status/evidence under this problem>
  stance: <plain-language current encounter stance>
  role: PRIMARY | BACKGROUND | NOT_RENDERED
  relations: <source/evidence-supported relation or none>
  render: <where/how this problem appears in the final note>
```

Do not freeze a STATE enum for the first run. Use constrained plain language that:

- distinguishes current adopted stance from historical/source-only statements;
- preserves uncertainty;
- does not silently import an old/current-source label into final truth.

### 2. Final note

Rendered from the ledger + template. The ledger is an audit surface, not inline markup for every
sentence.

## Provenance requirement

Require mapping for:

- every independent problem in the A/P;
- every causal/diagnostic conclusion;
- every care-changing plan statement, or a clear marker that it is Ask-generated reasoning if the
  contract permits that.

Body sections must remain source-faithful, but do not require sentence-by-sentence source IDs.

## Success criteria

Do not use “no unsupported clinical claim” as a blanket gate. Ask is supposed to reason.

Use:

> No invented patient-specific fact. Any diagnostic, causal or management inference must be traceable
> to supplied evidence, must not strengthen uncertainty beyond that evidence, and must remain within the
> Ask contract.

Plus:

- independent problems correct; contained manifestations not promoted;
- stance/role defensible and not blindly copied;
- no invented/strengthened/reversed relations;
- template fit and clinical adequacy acceptable to the signer/clinician.

## Scoring

Score four outcomes, not seven independent gates:

1. **Problem model** — identity/containment.
2. **Stance/role** — current stance and PRIMARY/BACKGROUND.
3. **Fidelity** — source facts, uncertainty, attribution, chronology, relations.
4. **Final note** — template fit, organization, clinical adequacy.

Record failures by type, not prose impression.

## Failure localization

- evidence missing/altered in packet -> Scribe problem;
- evidence present but semantic decision wrong -> Ask contract problem;
- semantics correct but note malformed/poorly organized -> realization/template problem.

This is more useful than a large predicate grid.

## Cases and blinding

- Start with one case where the exact raw source is available, so P vs N is interpretable and R is
  possible if needed.
- If P works, run one held-out case with structural ground truth.
- De-identify; do not commit patient-specific content. Store protocol, prompts, aggregate scores and
  de-identified failure examples.

## Stop rule

- P materially better than N on the four outcomes -> keep semantic contract; proceed to held-out case.
- P ≈ N -> the contract may be ceremony; inspect whether Ask already encodes the rules or the contract
  is too vague.
- P worse than N -> diagnose contract overload or conflict before adding more rules.
- If failure is Scribe source loss, do not tune Ask; fix Scribe separately.
- No architecture change, Gate-0 acceptance, production change or Phase 0 from this experiment.

## Deliverables

- experiment manifest (case id, condition, packet hash, contract version, template version);
- Ask ledger and note;
- four-outcome score and failure taxonomy;
- short decision: keep, revise or reject the packet+contract baseline.

No implementation before this protocol is reviewed. No Gate-0 acceptance. No Doximity. No Phase 0.
