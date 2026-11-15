# ChatGPT review 094 — D-030 structural extension incomplete

## Verdict

> **STRUCTURAL DIRECTION ACCEPTED; CALIBRATION CONTRACT REJECTED AS INCOMPLETE.**

Target: DeepSeek commit `6766898`.

The new fields are placed under the correct owners:

- S2: `causal_relations[]`;
- S3: `encounter_role`;
- S4: projected roles + causal relations.

This preserves the 11-module architecture and D-030 ownership.

However, the current Gate-0 package can validate only that these fields exist and are projected. It
cannot determine whether their **clinical values are correct**.

## Blocking defects

### 1. No semantic predicate for encounter role

A run may label the old infarct `PRIMARY` instead of `BACKGROUND` and still pass all active S3
predicates.

Required:

`S3-ROLE-01` — SEMANTIC / SIGNER_REFERENCE

> every rendered problem's encounter role is clinically supported by the current encounter:
> PRIMARY only when actively evaluated/managed now or independently driving current neurologic
> assessment/management; otherwise BACKGROUND.

Add at least one structurally valid semantic seed that flips a role without triggering a mechanical
predicate.

Also add a local mechanical role-shape predicate (or equivalent S3-local validator) so missing/invalid
role values fail in S3 rather than being discovered only while projecting into S4.

### 2. No semantic predicate for causal relations

A run may invent:

> old stroke LIKELY contributes to falls

from historical coexistence alone and still pass.

Required:

`S2-CAUSAL-01` — SEMANTIC / SIGNER_REFERENCE

It must judge:
- whether a causal relation is source/current-formulation supported at all;
- relation noun/type;
- strength: LIKELY / POSSIBLE / UNLIKELY;
- direction;
- correct acting subject — residual deficit/mechanism rather than historical disease label when that
  is what currently acts.

Add an S2-local mechanical causal-shape/reference predicate for closed vocabularies, known object ids,
non-empty/valid support spans and required fields.

### 3. CASE-01 alone cannot positively calibrate D-030 causality

CASE-01 correctly has **no causal relation**. It can test "do not infer causality", but cannot test:
- residual deficit vs historical disease as the causal subject;
- LIKELY vs POSSIBLE preservation.

Do **not** rewrite CASE-01 to manufacture causality.

Add the smallest separate positive causal calibration fixture, for example a current source statement
that chronic right-sided weakness from prior stroke **may contribute** to falls.

Clean truth should then carry:
- acting subject = chronic residual weakness object;
- relation = CONTRIBUTOR;
- strength = POSSIBLE.

Use separate single-mutation semantic seeds to test:
- historical stroke object substituted for the residual-deficit object;
- POSSIBLE changed to LIKELY.

### 4. S4 role propagation is unguarded

S4 problems now carry `encounter_role`, but no active predicate checks that the S4 problem's role
equals S3's role for that source problem.

Add a mechanical role-propagation predicate, or extend an existing S4 predicate only if ownership and
specificity remain unambiguous.

### 5. Causal-relation projection leaks an unresolvable endpoint

Current projection condition is effectively:

> include relation if **from OR to** is retained.

That allows S4 to receive a causal relation whose other endpoint has no retained payload in
`from_ingest`.

For S4 rendering, both endpoints must be resolvable. Change the projection boundary to require both
`from` and `to` in the retained set, unless a separately frozen external-endpoint representation is
defined. None exists now.

### 6. Governing identities were mutated in place

D-030 changed:
- schema fields;
- seed corpus (28 -> 30);
- clinical semantic truth;
- soon, active predicate set.

Do not continue under unchanged `SCHEMA-3 / PILOT-2 / ACTIVE-PILOT-2 / GATE0-C2` identities.

Use new identities for the rebuilt package (next sequential versions are appropriate), and bump oracle
identity if its expected semantic content is extended.

This is necessary for evidence invalidation and reproducibility.

### 7. Stale CASE-01 wording

`predicates.md` still says the infarct is retained because it is a:

> "major established primary neurologic diagnosis"

That contradicts D-030.

CASE-01 truth is:

- falls = PRIMARY;
- prior L MCA infarct = BACKGROUND;
- compact A/P representation remains appropriate;
- no causal contribution is asserted unless supported by current source/formulation.

## What is preserved

Keep the following from `6766898`:

- S2 ownership of causal relations;
- S3 ownership of encounter role;
- S4 receipt of both axes;
- clean CASE-01 role assignments;
- no causal relation in CASE-01;
- structural projection machinery, after the endpoint condition is corrected.

No architecture reopening is warranted.

## NEXT

DeepSeek performs a bounded rebuild under D-031:

1. new governing identities;
2. add S2 causal semantic + mechanical predicates;
3. add S3 role semantic + mechanical predicates;
4. add S4 role-propagation mechanical predicate;
5. add the smallest positive causal calibration fixture and isolated semantic seeds;
6. fix causal projection to require both endpoints retained;
7. correct stale D-030/CASE-01 wording;
8. regenerate source-first artifacts;
9. run tests + preflight + packets mode only;
10. return exact diff, counts and packet workload to ChatGPT.

Do not collect signer references until this rebuild is accepted.
No Gate 0 acceptance. No Doximity. No Phase 0.
