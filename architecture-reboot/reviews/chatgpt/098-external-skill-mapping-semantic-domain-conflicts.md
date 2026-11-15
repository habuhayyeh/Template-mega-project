# ChatGPT review 098 — external skill mapping exposes semantic-domain conflicts

## Verdict

> **PAUSE signer collection. Prior preference retrieval is highly successful, but it exposed three
> calibration-domain defects in the current C3 packet set.**

The external skill resolved 18/20 preference questions explicitly. Q1 is already resolved for CASE-01
by the signer's direct chat judgment. Q17 is the only remaining clinical preference question.

However, current packet construction asks the signer to make contradictory semantic judgments on
mechanically invalid artifacts.

### Blocker 1 — S2-CAUSAL-01 vs S2-CAUSAL-02

`G0-S2-08` uses invalid strength `CERTAIN`.

Current packet `pkt-1abf288d40eb11102b1a3183` asks the signer whether relation strength is correct,
while the index expects S2-CAUSAL-01 SILENT because S2-CAUSAL-02 owns the seed.

Fix:
- define S2-CAUSAL-02 validity as a prerequisite/domain gate for S2-CAUSAL-01;
- do not generate/require a signer semantic judgment for S2-CAUSAL-01 on structurally invalid causal
  entries.

### Blocker 2 — S3-ROLE-01 vs S3-ROLE-02

`G0-S3-12` uses invalid role `UNKNOWN`.

Current packet `pkt-e17fa41dd6803760f415bf3e` asks whether the role is clinically supported while the
index expects semantic SILENT.

Fix:
- S3-ROLE-02 structural validity is prerequisite/domain gate for S3-ROLE-01;
- do not generate/require signer role semantics on invalid role enum artifacts.

### Blocker 3 — G0-S2-01 is a metadata seed masquerading as semantic support

`G0-S2-01` deletes `support_refs` only.

Its S2-REP packet `pkt-9c460bd22965e3f0b1fd496d` explicitly instructs the signer to judge semantic
support by members/relations, "not merely whether ids and support refs exist."

The members/relations and source truth remain clinically unchanged.

Fix:
- add/move to a mechanical support-ref integrity predicate if non-empty support_refs are contractually
  required; or drop this seed if already enforced elsewhere;
- do not expect S2-REP-01 semantic FIRED from support_refs deletion alone;
- keep G0-S2-02 as the semantic representation failure seed because it inserts unrelated aspirin into
  the falls representation.

## Identity/evidence handling

No new signer reference has been recorded after the clean S3 role answer. Preserve that direct signer
reference only if its packet identity remains byte-for-byte unchanged under the correction; otherwise
mark it stale and re-ask once.

External-skill retrieval is not itself signer evidence under D-032.

## NEXT

DeepSeek makes this bounded calibration-domain correction, regenerates packets and returns:
- exact diff;
- revised active predicate/seed count;
- revised semantic packet count;
- explicit list of packets removed from signer workload by mechanical gating;
- whether the existing clean S3 role packet id remained unchanged.

Then ChatGPT asks only the remaining Q17 clinical question before grouped signer ratification.

No Gate-0 acceptance. No Doximity. No Phase 0.
