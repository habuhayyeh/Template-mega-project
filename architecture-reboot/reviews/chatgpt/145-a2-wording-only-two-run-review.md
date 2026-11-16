# Review 145 — A2 wording-only two-run reproducibility review

## Verdict

**A2 V2 boundary succeeds; A2 coverage/reproducibility still fails. Do not freeze A2 or run B1 yet.**

Two independent Doximity Ask runs were returned for the same frozen packet and the same
`01C-ACTION-LANE-WORDING-ONLY-TEST.md` module.

The important result is not simply that Run 2 is better. The pair separates what is now stable from what
remains unstable.

## Stable across both runs

Both runs obey the new D-049 boundary:

- complete `@@HANDOFF A2_ACTION_WORDING_V1` output ending in `@@END`;
- no `decision=`, `execution=`, `response=`, or `result=` normalization;
- no `ASSERTED_STATE`;
- no raw-state-phrase surrogate;
- no cross-record action episode grouping;
- no problem architecture, section allocation, or prose;
- T131 blood / urine / monitoring are split;
- T132 EKG / urine are split;
- EEG and MRI appear as distinct actions;
- current Keppra continuation remains distinct from prior reported Keppra drip and current load shorthand.

Therefore D-049 solved the prior **state-promotion-at-A** failure.

## Run 1

Run 1 fails the frozen A2 identity oracle because it omits multiple material actions.

### Definite coverage failures

1. **P1.045 basic labs and urinalysis omitted**
   - CT head is emitted;
   - consult and admission are emitted;
   - basic labs and UA are absent.
   - Oracle item 13 therefore fails.

2. **P1.055 Keppra discontinuation omitted**
   - current load shorthand is present;
   - discontinuation is absent.
   - Oracle item 21 fails.

3. **P1.044 seizure precautions omitted**
   - Oracle item 22 fails.

4. **T258 open-plane precaution omitted**
   - higher elevation and pool/water are preserved;
   - open-plane counseling is absent.
   - This makes safety-counseling coverage incomplete under oracle item 23.

### Additional variance/noise

Run 1 includes several lower-value transport/logistics actions:
- deciding to go to medical;
- arrival at medical;
- medical team responded;
- wheelchair transport;
- calling a paramedic brother.

These are not the fatal problem. The fatal problem is that extra low-value capture coexists with omission
of clearly material care actions.

## Run 2

Run 2 fixes nearly all of the Run-1 oracle failures:

- P1.045 CT / basic labs / UA are split;
- P1.044 seizure precautions appear;
- P1.055 Keppra discontinuation appears;
- T258 higher-elevation / open-plane / pool-water counseling are split;
- EKG / urine and blood / urine / monitoring splits are preserved.

However Run 2 still has material identity/coverage defects.

### 1. T258 planned MRI omitted

Run 1 preserved:

`plan MRI either tonight or tomorrow`

Run 2 does not.

This is a material current workup action and therefore a fatal omission under the oracle's general
material-action rule.

### 2. T258 medication decision misidentified

Run 2 emits:

```text
selector=decision tomorrow after EEG/MRI whether to continue or stop before discharge
target=EEG/MRI
operation=decision tomorrow after
action_phrase=decision tomorrow after EEG/MRI
```

The action identity is the future **continue/stop medication decision**, conditioned on EEG/MRI, not
EEG/MRI themselves.

This is a source-local action-identity error. B1 would receive the wrong target and is prohibited from
repairing it under D-049.

### 3. P1.018 multi-test workup incompletely represented

The selector says:

`Cruise ship lab work including CBC, CMP, lactate, EKG, and electrolytes were performed ...`

Run 2 emits only one span with `target=CBC`.

If these are retained as action content, materially distinct tests/procedures must be split. Selecting only
CBC from the compound source omits the other source-local action identities.

At minimum this demonstrates that compound-list splitting remains unstable outside the explicitly salient
current-ED example.

### 4. Possible T076 disposition omission

The selector includes:

`they did blood tests and said everything was fine so they were going to let her go`

Only the blood-test action is emitted. The prospective discharge/disposition action is not represented.

Whether this is fatal depends on the frozen packet/oracle's materiality judgment, but it is another sign
that action extraction from compound source records remains inconsistent.

## Reproducibility result

The two runs disagree materially on what actions exist.

Examples:

- Run 1 has P1.045 CT only; Run 2 has CT + labs + UA.
- Run 1 omits seizure precautions; Run 2 includes them.
- Run 1 omits Keppra discontinuation; Run 2 includes it.
- Run 1 preserves the T258 MRI plan; Run 2 omits it.
- Run 1 captures several low-value transport/logistics actions that Run 2 drops.

This is not a state-normalization failure anymore.

It is a **selection + source-local decomposition reproducibility failure**.

## What not to do

Do not:
- proceed to B1 using either run as a frozen A2;
- pick the better run and call A2 passed;
- union the two runs manually and treat that as model capability;
- add a same-model validator;
- add another semantic stage.

## Architectural interpretation

D-049 remains correct.

The current problem is narrower:

> GPT-4o can obey the wording-only boundary, but it does not reproducibly enumerate all material source-local action identities from compound and distributed source records.

This should be reported to DeepSeek as an execution problem.

The next design choice should favor the signer's stated principle:
- strengthen the ingestion contract;
- avoid further decomposition.

Potential bounded directions to assess:
1. make action enumeration less discretionary by using source-record-by-source-record traversal and an explicit per-record action count/split rule;
2. separate **mechanical action candidate enumeration** from materiality, without adding a new semantic stage;
3. remove or narrow the word `material` as an inclusion gate if it is causing variable omission;
4. require every clinical source record containing an action verb/action phrase to yield either one-or-more ACTION_SPANs or an explicit no-action disposition, but only if this can be done without recreating global atomicization.

No implementation of these alternatives should occur until DeepSeek reviews the evidence.

## Mechanical selector lint limitation

The exact frozen Scribe packet is not available in GitHub, so this review cannot independently prove every
selector is a literal substring of its cited record.

That does not alter the FAIL verdict because the demonstrated coverage/action-identity failures are
already sufficient.

No B1 run. No C/render. No acceptance.
