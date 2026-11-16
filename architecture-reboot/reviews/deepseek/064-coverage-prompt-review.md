# DeepSeek review — coverage/action recoverability prompt

**Verdict:** use this as an **Ask/B prompt**, not a Scribe prompt. It is coherent there, with four corrections.

Do not put it in Scribe. Scribe must return the source-faithful packet; this prompt returns clinical
synthesis. If Scribe runs this, the canonical packet is replaced by a downstream product.

## Contradictions and gaps

### 1. Role contradiction if placed in Scribe

The prompt says:

- “Scribe packet is canonical”;
- “return a source-coverage index followed by a clinical synthesis.”

That is a downstream B stage, not Scribe. Scribe cannot both preserve the packet and replace it with
coverage/synthesis.

**Use in Ask after Scribe.** Scribe may emit record IDs/source sections; it must not emit PROBLEM,
CLINICAL_UNIT or ACTION_VIEW.

### 2. Unresolved with no source

`SYNTHESIS_UNRESOLVED` requires `source_records=<IDs>`. If the issue is “no source exists,” there is no ID.

Change to:

```text
source_records=<IDs or NONE>
```

and define `NONE` as “no source record supports this unresolved item.”

### 3. Action-bearing records can still be dropped

The final check says body/action categories are represented, but a specific action-bearing record can be
in the census and never used.

Add:

> Every record in `action_bearing_records` must yield at least one `ACTION_VIEW` or a
> `SYNTHESIS_UNRESOLVED` entry explaining why no action can be represented.

That is the action-recoverability guarantee.

### 4. `contains` and `separate_from` have no evidence requirement

These are clinical relationships. The prompt requires evidence for `PROBLEM`, but not for containment or
separation.

Add:

> `contains` and `separate_from` may be stated only when the cited `evidence` supports the relationship.
> Otherwise use `SYNTHESIS_UNRESOLVED`.

### 5. “If uncertain, include under context” can hide actions

If a record is uncertain between action-bearing and context, placing it only in `context` loses action
recoverability.

Change to:

> If uncertain whether a record is action-bearing, include it in `action_bearing_records` and `context`.

### 6. Redundancy

The “Why this step exists,” Phase 1 check and final check repeat coverage requirements. Some repetition is
useful for a long prompt, but do not add more. Keep the final check short.

The prompt is long. GPT-4o may lose middle rules. The highest-risk rules are:

- record IDs only;
- no uncited state;
- action-bearing coverage;
- census-to-synthesis closure.

Keep those repeated; trim explanatory prose.

## Can recoverability live here?

**Yes, if “here” means this Ask/B prompt.** Phase 1 is the B-internal coverage census; that is exactly the
current experiment.

**No, if “here” means Scribe.** Scribe should stay source-faithful. Coverage categories and clinical
synthesis are downstream decisions.

If you want recoverability before B as a separate read-only check, that is a different prompt/stage:
record IDs only, no selectors, no synthesis. Do not merge that into Scribe.

## Minimal corrected prompt changes

1. Add at top: “This is an Ask/B stage. Input is the Scribe packet; output is coverage + synthesis. Do not
   run this as a Scribe note-generation prompt.”
2. `SYNTHESIS_UNRESOLVED source_records=<IDs or NONE>`.
3. Add every-action-bearing-record rule.
4. Add `contains`/`separate_from` evidence rule.
5. Change uncertain action/context to include both.
6. Keep final check short.

No architecture change. No new stage. No selectors. No action-state enums.
