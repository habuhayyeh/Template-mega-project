# DeepSeek verdict — pointer-only F1

**Question:** quote-anchored F1 or pointer-only F1, given the immutable Scribe packet remains available
downstream?

**Answer:** **pointer-only.**

I was wrong to push exact quote anchors as the default. They duplicate the packet, recreate a
copy-fidelity surface, and add output that GPT-4o can get subtly wrong. The 028 example proved the point:
the illustrative anchors were not exact to the frozen packet.

## Why pointer-only wins

1. **No claim layer.** F1 states only which records are about the same topic. It does not state what they
   prove. There is no support obligation to validate.
2. **No source duplication.** The Scribe packet remains canonical. F1 carries only IDs and labels, so it
   cannot truncate from anchor copying or drift from source wording.
3. **Downstream dereferences the real text.** F2/F3/F4 open the cited records and decide polarity,
   certainty, action state and problem identity from the source, not from an F1 paraphrase.
4. **No F1V.** With no claims, a semantic support validator has nothing to validate. Remove it from the
   production path.
5. **Smaller runtime.** Pointer index is cheap to generate and cheap to check.

## Conditions

Pointer-only only works if these are enforced:

### 1. Labels are non-assertive

A label names the topic; it does not state the answer.

Allowed:
- `prior seizure history`
- `family seizure history`
- `Wednesday event`
- `Keppra mentions`
- `ED examination`

Forbidden:
- `no prior seizures`
- `focal seizure`
- `Keppra administered`
- `normal workup`
- `PNES likely`

### 2. No claim fields

No `fact:`, `reasoning:`, `issue:`, `support:`, `assessment:`, `plan:`, or copied source spans.

### 3. No materiality filter hidden inside F1

The current candidate says "route all records that may materially affect..." That asks F1 to decide
materiality, which is the same kind of semantic judgment that caused the claim layer.

Use a mechanical coverage rule instead:

- every Scribe record appears in at least one cluster, **or** in an explicit `UNCLUSTERED`/`NONCLINICAL`
  group;
- a record may appear in more than one cluster when genuinely useful;
- no record silently disappears from the index.

This is checkable without clinical judgment. The original packet is still canonical; the index is
navigation, not a partition.

### 4. Downstream cites record IDs, not cluster labels

F2/F3/F4 must dereference and cite the exact Scribe record IDs. A cluster label is never evidence.

### 5. Mechanical checks only

External/engineering checks:

- every listed record ID exists verbatim;
- every cluster has at least one record;
- cluster IDs are unique;
- every packet record appears at least once (or in `UNCLUSTERED`);
- output starts/ends correctly.

No semantic PASS/FAIL validator.

## Recommended runtime

```text
Scribe V2.2 packet
  -> F1 pointer-only evidence index
  -> F2 semantic reconciliation + action state
  -> F3 problem architecture
  -> F4 note compiler
  -> F5 renderer
```

F1V is removed. If later evidence shows a specific downstream failure, add a narrow check for that
failure, not a general semantic validator.

## If quote anchors ever return

Only as a **targeted exception** for a high-risk claim that cannot be safely dereferenced, and only with:

- the exact record ID;
- an exact substring verifiable mechanically;
- no duplicate full-record copying.

Do not make anchors the general F1 format. Pointer-only is the default.

## Recommendation

Adopt proposal 133 with the coverage/label conditions above, run it once on the frozen packet, and judge
it on:

- completion;
- every record routed or explicitly unclustered;
- non-assertive labels;
- no claim fields;
- downstream ability to dereference and reason from the packet.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
