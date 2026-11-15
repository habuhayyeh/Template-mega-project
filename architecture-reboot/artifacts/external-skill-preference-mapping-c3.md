# External skill preference mapping to GATE0-C3

## Source

Signer supplied a completed retrieval-only questionnaire from a separate LLM environment whose skill
was built from prior signer answers.

This artifact records the mapping only. Per D-032, the external LLM output is prior-policy evidence,
not automatically a new Gate-0 signer reference.

## Retrieval result

- 18/20 questions: EXPLICITLY DOCUMENTED.
- Q1: AMBIGUOUS/PARTIAL in the external skill as a general rule.
- Q17: AMBIGUOUS/PARTIAL.
- Q1 is nevertheless resolved for CASE-01 by the signer's direct answer in this chat: both falls and
  the prior stroke deserve A/P representation, with falls PRIMARY and stroke BACKGROUND/compact.
- Therefore Q17 is the only remaining case-specific clinical preference gap.

## Rule families recovered

### A/P representation and encounter role
- major established neurologic disease may retain compact A/P representation while BACKGROUND;
- compact representation does not imply PRIMARY;
- medication alone does not create a neurologic problem;
- a background disease can become PRIMARY when independently evaluated/managed;
- PRIMARY problems receive greater prominence than BACKGROUND problems.

Maps primarily to:
- S1-CAND-01
- S3-ROLE-01
- medication-candidate seed G0-S1-05
- role-flip seed G0-S3-11

### Historical presence vs current adoption
- chart presence is not current adoption;
- current explicit formulation may adopt a chronic residual deficit while the underlying old disease
  remains historical/background;
- historical presence alone does not establish current status, management, follow-up or causality.

Maps primarily to:
- S2-ADOPT-01 CASE-01 clean
- S2-ADOPT-01 CASE-10 clean
- S2-ADOPT semantic variants

### Causality
- causal relation is independent of PRIMARY/BACKGROUND;
- BACKGROUND disease may contribute through an established consequence;
- acting residual deficit/mechanism should be named instead of merely the historical disease;
- POSSIBLE must not be upgraded to LIKELY/definite;
- coexistence alone does not establish causality;
- preserve unequal causal weighting.

Maps primarily to:
- S2-CAUSAL-01 CASE-01 clean/negative branch
- G0-S2-07 history-only invented causality
- CASE-10 clean positive branch
- G0-S2-09 wrong historical-disease subject
- G0-S2-10 POSSIBLE -> LIKELY overstatement

### Representation/reuse
- prior stroke + established residual deficit may form one compact background representation;
- unrelated aspirin does not belong in the falls claim merely because it appears in chart;
- intentional reuse is allowed when the same information performs different clinical jobs.

Maps primarily to:
- S2-REP-01 stroke representation
- G0-S2-02 aspirin-member semantic seed
- later rendering/reuse rules

## Remaining clinical gap

Q17:

> In CASE-01, is "no new weakness or speech trouble" clinically pertinent enough to be retained as
> supporting/negative evidence within the falls representation?

The skill supports the general rule that pertinent negatives belong with a problem, but does not decide
that these exact negatives are pertinent to these falls.

One signer answer can resolve this same question for both CASE-01 and CASE-10 because the relevant
falls representation uses the same O03/O04 pairing.

## Calibration defects exposed by the mapping

### 1. S2-CAUSAL semantic/mechanical overlap

G0-S2-08 changes causal strength to invalid `CERTAIN`.

- must-fire = S2-CAUSAL-02 mechanical shape/enum;
- current index nevertheless expects S2-CAUSAL-01 semantic SILENT;
- but S2-CAUSAL-01 explicitly asks whether causal **strength is correct**.

A correct signer would reasonably flag CERTAIN, so current full-silence specificity is contradictory.

Required correction: semantic causality is defined only over structurally valid causal entries, with
S2-CAUSAL-02 as a prerequisite/domain gate. Structural-invalid artifacts must not require a human
S2-CAUSAL-01 judgment.

### 2. S3-ROLE semantic/mechanical overlap

G0-S3-12 changes role to invalid `UNKNOWN`.

- must-fire = S3-ROLE-02 mechanical enum;
- current index expects S3-ROLE-01 semantic SILENT;
- but S3-ROLE-01 asks whether every rendered encounter role is clinically supported.

UNKNOWN is not a clinically supported PRIMARY/BACKGROUND role.

Required correction: S3-ROLE-01 applies only after S3-ROLE-02 structural validity; no semantic signer
packet should be required on an invalid role enum.

### 3. G0-S2-01 is not a valid S2-REP-01 semantic seed

G0-S2-01 deletes `support_refs` but leaves:
- the same representation members;
- the same clinically relevant source objects;
- the same relations.

The blinded S2-REP-01 instructions explicitly say to judge semantic support by members/relations and
not merely whether support refs exist.

Therefore deleting support_refs alone cannot validly be expected to make the semantic predicate fire.

Required correction:
- move support-ref presence/integrity to a mechanical representation-source predicate (preferred), or
  remove this seed from S2-REP-01 calibration if that integrity is already enforced elsewhere;
- retain G0-S2-02 (unrelated aspirin member) as the true semantic S2-REP-01 failure seed.

## NEXT

DeepSeek performs only the three calibration-domain fixes above, regenerates the packet set and reports
the reduced signer workload. Preserve D-030/D-031 clinical truth.

After that, ChatGPT asks the signer the single unresolved Q17 clinical question and maps the answer to
the clean CASE-01/CASE-10 representation packets.

No Gate-0 acceptance, Doximity or Phase 0.
