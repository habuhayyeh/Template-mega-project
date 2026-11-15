# Ask P/N run template

**Purpose:** capture one controlled comparison of Ask with and without the semantic contract, without
committing patient-specific content.

## Run manifest

```text
case_id:
deidentified: yes/no
packet_hash:
contract_version: ASK-CONTRACT-V1 (or commit)
template_version:
ask_model/version:
run_date:
condition_order: P then N | N then P | randomized
```

## Inputs

- Scribe V2.2 packet (same bytes for both conditions).
- Final USF template (same bytes for both conditions).
- Contract V1 for P only.
- Raw source only for optional R comparator; never give raw source to P/N.

## Capture

For each condition, store outside the repo:

1. exact prompt;
2. exact output;
3. packet hash and template hash;
4. ledger (if P);
5. final note;
6. token/time if available.

Do not commit patient-specific text. Commit only manifest, aggregate scores and de-identified failure
examples.

## Four outcomes

Score each 0–2; explain one line per score.

### 1. Problem model

- 0: contained manifestation promoted, independent problem missed, or problem merged incorrectly.
- 1: mostly right with one material identity/containment error.
- 2: independent problems correct; manifestations contained.

### 2. Stance / role

- 0: source label blindly adopted or current/historical confused.
- 1: defensible with one material stance/role error.
- 2: defensible current stance and PRIMARY/BACKGROUND/NOT_RENDERED for each problem.

### 3. Fidelity

- 0: invented patient fact, negation/uncertainty flip, or invented/strengthened relation.
- 1: faithful with one material qualifier/attribution/relation error.
- 2: source facts, uncertainty, attribution, chronology and relations preserved.

### 4. Final note

- 0: template broken or clinically unusable.
- 1: usable with material organization/template defect.
- 2: fits template, organized, clinically adequate; no fabricated normal findings.

## Failure localization

Mark one per material failure:

- `SCRIBE` — evidence missing/altered in packet.
- `ASK-CONTRACT` — evidence present, semantic decision wrong.
- `REALIZATION` — semantics right, note malformed/poorly organized.
- `TEMPLATE` — template ambiguity/conflict.

## Comparison

- P vs N on the four outcomes.
- If P ≈ N, contract may be ceremony.
- If P worse, diagnose contract overload/conflict.
- If failure is Scribe source loss, do not change Ask.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
