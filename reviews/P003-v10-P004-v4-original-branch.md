# P003 v10 / P004 v4 review — original architecture branch

## P003 v10
**Verdict: ACCEPT — ready for signer implementation approval**

The final mechanical inconsistency is resolved.

Accepted:

- COURSE classification by function;
- relevance gate before COURSE classification;
- facts before reasoning;
- etiology belongs under the problem it explains;
- short cause on the problem line with fuller etiologic reasoning in a bullet when it adds distinct content;
- signer-approved line contraction;
- bounded speaker-attribution rendering;
- bounded number/unit normalization;
- bounded anchored relative-time rendering:
  `X ago -> X prior to presentation`, interval unchanged;
- no absolute-date inference from provenance;
- STANDING_ITEMS traced separately;
- three independent runs;
- I1-I10, including the transformation-9 split placement pattern;
- I8 and PASS wording updated consistently through transformations 1-10;
- no reopening of 01/02/04/06/07.

The frozen target is now source-faithful:
- O8 remains the source of `two years`;
- the reference phrase `prior to presentation` is explicitly authorized;
- no provenance date is substituted for the event date.

No further architectural or signer-level ambiguity remains inside P003.

### Implementation gate

P003 is not yet implemented. It may proceed only after the signer explicitly approves implementation.

On implementation, DeepSeek should:

1. update `pipeline/05_WRITE_AP.md`;
2. update `pipeline/AP_ANCHOR.md`;
3. record the next free D-### for the accepted P003 rendering rules;
4. run the frozen Handoff through three fresh-context 05 runs;
5. produce the line-level trace table and I1-I10 comparison;
6. update STATUS based on the actual run set;
7. return the implementation + run artifacts for actual-diff review.

A mock PASS does not establish Doximity acceptance.

## P004 v4
**Verdict: ACCEPT HOLD STATE**

P004 is correctly blocked pending a representation proposal that exposes management -> problem linkage source-faithfully.

Do not implement P004 on the current substrate and do not add medication-specific heuristics.

Accepted future sequence:

1. P003 implementation and validation;
2. management-target representation proposal;
3. substrate/oracle revision;
4. return to P004.

No signer escalation is needed for P004 at this stage.
