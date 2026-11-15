# Proposal 024 — first Doximity Ask experiment

**Status:** PROPOSED — experiment design only. No implementation, no patient data in the repo.

## Goal

Test whether Doximity Ask, given a V2.2 Scribe evidence packet + semantic contracts + the final USF
template, can own IDENTITY, RELEVANCE/ROLE, STATE, RELATIONS and USE/REALIZATION without:

- inventing facts not in the packet;
- losing provenance, negation, uncertainty or chronology;
- blindly inheriting provisional A/P labels from a current prechart note;
- collapsing containment into separate problems;
- strengthening or inventing causal relations.

## Inputs

1. **Scribe V2.2 packet** — provisional frozen baseline. Not a final production contract.
2. **Semantic contracts/pseudocode** for the five domains:
   - IDENTITY — independent problem vs contained information;
   - RELEVANCE/ROLE — render in this encounter? PRIMARY or BACKGROUND?
   - STATE — documented vs currently endorsed/rejected/historical/unresolved;
   - RELATIONS — source-supported relation, direction, strength, participants;
   - USE/REALIZATION — selected content, template section and rendering.
3. **Final USF neurology note template.**
4. **Raw source only for audit** — not shown to Ask. This is the fidelity ceiling.

## Conditions

Use the same case, same template, same Ask model/settings.

| condition | input | purpose |
|---|---|---|
| **A. Raw + contracts** | raw transcript/prechart + contracts + template | ceiling; what Ask can do without Scribe |
| **B. Packet + template** | Scribe packet + template | Scribe-only baseline |
| **C. Packet + contracts** | Scribe packet + contracts + template | primary test |
| **D. Packet + contracts + provisional-label guard** | C plus explicit guard | test the specific failure mode |

If cost/time is limited, run **A, C, D**; B is optional.

## Provisional-label guard

The key failure mode from the encephalopathy case: a current prechart note contains a provisional A/P
label (for example “encephalopathy”), and Ask may inherit it as final truth.

Required rule:

> Any diagnosis, problem label, assessment or plan statement appearing in a current prechart note is a
> **documented proposition**, not automatically the final encounter stance. Ask must classify it as
> `DOCUMENTED_ONLY` unless the current source evidence and the semantic contract support adoption. It may
> become `CURRENT_ENDORSED`, `CURRENT_REJECTED`, `HISTORICAL_ONLY` or `UNRESOLVED`, with evidence. Do not
> import a provisional label into the final A/P merely because it appears in a current note.

This is an Ask instruction, not a Scribe rule. Scribe must preserve the label; Ask must adjudicate it.

## Ask output shape

Before the final note, Ask emits a compact ledger:

```text
PROBLEM <id>
  identity: INDEPENDENT | CONTAINED_UNDER <id>
  source: <record ids>
  state: DOCUMENTED_ONLY | CURRENT_ENDORSED | CURRENT_REJECTED | HISTORICAL_ONLY | UNRESOLVED
  role: PRIMARY | BACKGROUND | NOT_RENDERED
  relations: <source-supported relation edges or none>
  use: <template section / units>
```

Then the final note. Every clinical claim in the note must map to ledger/problem/source IDs. The ledger
is the audit surface, not a second note.

## Scoring

For each condition, score independently:

1. **Source fidelity** — unsupported claims, negation flips, uncertainty strengthening, attribution loss,
   chronology reordering, missing source-only facts.
2. **Identity/containment** — independent problems vs contained manifestations; no promotion of a
   manifestation to a problem.
3. **STATE** — documented-only vs current-endorsed/rejected/historical/unresolved; no blind inheritance
   of provisional labels.
4. **RELEVANCE/ROLE** — render vs not rendered; PRIMARY/BACKGROUND; no historical-relevance promotion.
5. **RELATIONS** — source-supported relation, direction, strength, most specific participant; no
   inferred mediator.
6. **USE/REALIZATION** — template completeness, section placement, no unsupported content.
7. **Note-level clinical adequacy** — signer/clinician blind review, not style polish.

Record failures by type, not by prose impression. A lower-fidelity note that is fully traceable is
better for this experiment than a polished unsupported one.

## Success criteria

The primary condition C/D passes only if:

- no unsupported clinical claim in the note;
- no provisional label becomes final without evidence;
- identity/containment and role/state are correct on the known case;
- no relation is invented/strengthened/reversed;
- template fields are complete where source supports them;
- every note claim maps to a ledger/source ID.

If C is materially worse than A, the loss is in Scribe packet or Ask prompting; diagnose before
changing either. If D fixes a C failure, the guard is necessary in the Ask contract.

## Cases and blinding

- Start with one case where the exact raw source is available, so A vs C is auditable.
- Then run one held-out case with only a structural ground truth; do not overfit prompt wording to one
  case.
- Strip/redact identifiers; do not commit patient-specific content. Store only protocol, prompts,
  aggregate scores and de-identified failure examples.

## Stop rule

- If A > C: inspect whether Scribe lost content or Ask failed to use the packet. Do not tune Scribe
  unless the failure is source-loss at Scribe.
- If C ≈ A and D passes: provisional Scribe + Ask contract is viable; expand to held-out cases.
- If D fails: the provisional-label guard or STATE contract is insufficient; fix the semantic contract,
  not the Scribe prompt.
- No architecture change, Gate-0 acceptance, Doximity production change or Phase 0 from this experiment.

## Deliverables

- experiment manifest (case id, condition, packet hash, contract version, template version);
- Ask outputs and ledgers;
- scoring sheet and failure taxonomy;
- short decision: keep, revise, or reject the Scribe→Ask baseline.

No implementation before this protocol is reviewed. No Gate-0 acceptance. No Doximity. No Phase 0.
