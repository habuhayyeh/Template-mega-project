# ChatGPT review 117 — review of DeepSeek proposal 024 Ask experiment

## Verdict

**ACCEPT WITH SIMPLIFICATION.**

The core experiment is correct: test whether Ask can turn the V2.2 evidence packet into a clinically faithful neurology note while owning IDENTITY, RELEVANCE/ROLE, STATE, RELATIONS, and USE/REALIZATION.

However, proposal 024 reintroduces two forms of complexity we just spent substantial effort removing:

1. a case-specific provisional-label guard as a separate condition;
2. sentence-level ledger/source mapping across the entire final note.

Both should be generalized before the first Ask run.

## 1. Generalize the provisional-label guard into the STATE contract

Do **not** create a separate condition D for 'provisional A/P labels.'

The load-bearing principle is broader:

> A proposition appearing in any source — transcript, current prechart note, prior note, consultant note, problem list, medication list, imaging report, or collateral statement — is source evidence, not automatically the final encounter stance.

Ask must decide the final encounter stance from the whole current evidence set.

This directly covers the encephalopathy example without introducing a diagnosis-specific or source-type-specific exception.

Therefore:
- fold the provisional-label rule into condition C as the core STATE rule;
- remove D as a separate condition;
- only add an ablation/guard experiment later if the primary run actually shows blind inheritance.

This is the same simplification principle already accepted for problem identity and relation fidelity: general rule first, exception only if evidence demands one.

## 2. Condition A is a comparator, not a ceiling

`Raw + contracts + template` should not be called the fidelity ceiling.

The raw transcript/prechart may be longer, noisier, more repetitive, more contaminated by template boilerplate, and harder for Ask to use than the Scribe packet.

A can therefore be better or worse than C for reasons unrelated to information loss.

Use A only as a **raw-input comparator** when the exact raw source is available.

The main production question is still whether C works.

## 3. Reduce the first experiment to two conditions

For the first Ask experiment, use:

### P — production candidate
`V2.2 packet + semantic contract + final template`

### N — no-contract baseline
`V2.2 packet + final template`

Purpose:
- P tests the actual proposed production path;
- N tells us whether the semantic contract is helping or merely adding ceremony.

Optional later comparator:
- R = raw + semantic contract + template, only when raw-source comparison is specifically needed.

Do not run four conditions by default.

## 4. Simplify the ledger

Proposal 024 ledger currently makes contained manifestations look like problems:

`identity: INDEPENDENT | CONTAINED_UNDER <id>`

That conflicts with the user's accepted containment concept: a contained manifestation is information **inside** a problem, not another problem object.

Instead, the audit ledger should list **independent problems only**.

Recommended experimental ledger:

```text
PROBLEM <id>
  label: <plain-language problem identity>
  evidence: <source record ids>
  contained: <important manifestations/status/evidence that belong under this problem>
  stance: <plain-language current encounter stance>
  role: PRIMARY | BACKGROUND | NOT_RENDERED
  relations: <source/evidence-supported relation or none>
  render: <where/how this problem appears in final note>
```

Do not require a contained manifestation to receive its own PROBLEM record.

## 5. Do not freeze a STATE enum in the first Ask test

`DOCUMENTED_ONLY | CURRENT_ENDORSED | CURRENT_REJECTED | HISTORICAL_ONLY | UNRESOLVED` is a reasonable conceptual vocabulary, but the five-domain model is still provisional and the user explicitly does not want a large ontology forced into Doximity.

For the first Ask experiment, use a plain-language `stance:` field constrained by the general rule:

- distinguish current adopted stance from historical/source-only statements;
- preserve uncertainty;
- do not silently import an old/current-source label into final truth.

If repeated Ask runs show that a small fixed enum improves reliability, formalize it later.

## 6. Relax sentence-level provenance without losing auditability

Do not require every sentence/clinical claim in the final note to map individually to a ledger/source ID.

That creates a large bookkeeping surface and can distort the output.

For the diagnostic experiment require:

- every independent problem in the A/P maps to evidence IDs;
- every causal/diagnostic conclusion maps to the evidence IDs that support the reasoning;
- every care-changing plan statement must either be present in source/encounter plan or be clearly identified as Ask-generated reasoning if the experiment permits such reasoning;
- body sections should remain source-faithful, but do not require sentence-by-sentence inline IDs.

The ledger is an audit surface, not a provenance markup language for the whole note.

## 7. Correct the success criterion for clinical reasoning

`no unsupported clinical claim` is too broad because Ask is explicitly supposed to perform clinical reasoning.

Use:

> No invented patient-specific fact. Any diagnostic, causal, or management inference must be traceable to supplied evidence, must not strengthen uncertainty beyond that evidence, and must remain within the Ask contract.

This separates **facts** from **derived clinical conclusions**.

## 8. First Ask experiment should answer a small number of questions

Do not score seven separate domains as seven independent bureaucracy-heavy gates.

The first run needs to answer four practical questions:

1. **Did Ask identify the right independent neurologic problems and keep manifestations contained?**
2. **Did Ask reach a defensible current stance/role for each problem without blindly copying source labels?**
3. **Did Ask preserve source fidelity and relation/uncertainty boundaries?**
4. **Did the final note use the available evidence appropriately and fit the requested template?**

The five semantic domains remain explanatory ownership boundaries, not necessarily five separately scored instruments.

## Revised first experiment

### Input
- one V2.2 packet;
- compact Ask semantic contract;
- final USF note template.

### Conditions
- **P:** packet + semantic contract + template;
- **N:** packet + template.

### Output
1. compact problem audit ledger;
2. final note.

### Primary comparison

Does P outperform N on:
- problem identity/containment;
- current stance and role;
- source/uncertainty fidelity;
- final-note clinical adequacy?

### Failure localization

If P fails:
- missing/altered evidence in packet -> Scribe problem;
- evidence present but stance/problem model wrong -> Ask semantic contract problem;
- semantics correct but final note malformed/poorly organized -> realization/template problem.

This three-way localization is more useful than a large predicate grid.

## Recommendation

Proceed with the Ask experiment after rewriting proposal 024 around this simpler design.

Do not reopen Scribe.
Do not add a special provisional-label guard.
Do not freeze a large STATE ontology.
Do not require sentence-level source markup.

Use the first Ask run to discover whether the **five-domain conceptual architecture actually helps the final note**, not to validate another harness.

No Gate-0 acceptance or architecture freeze follows from this review.