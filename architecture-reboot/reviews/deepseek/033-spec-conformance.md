# DeepSeek response 033 — exact-spec conformance read

**Verdict: CONFORMANT. All eleven agreed corrections are represented.** Two wording ambiguities worth fixing before run, neither a contradiction of the architecture.

---

## 1. Corrections confirmed present

| Correction | Where | Status |
|---|---|---|
| Gate 0 scorer calibration | program §Gate 0 | present, and stated as a prerequisite not a ninth experiment |
| Manifests freeze case IDs, count, order, package + control-plane/scorer versions | program; each spec's run design | present |
| AX-S1S2-D structural vs semantic score families | spec §assertions split | present |
| AX-S1S2-D explicit contradictory-source fixture | fixture 11 | present |
| No arbitrary reopen percentage | spec §failure interpretation | present |
| AX-LEAK IR-only / isolated-call reference controls | spec §arms | present |
| AX-LEAK IR-positive / source-negative fixture | spec | present |
| LEAK × SCALE interaction later | program + spec | present |
| AX-S4 receives exactly one S3-selected representation | spec §fixtures, §scoring, plus an explicit "malformed upstream structure" note | present, and better than my draft |
| AX-I3 claim narrowed to 3/3 | spec | present |
| AX-T measures the extra-output instruction | spec | present |
| AX-SCALE decomposes burden variables + failure attribution | spec §variables, §failure attribution | present |
| AX-R2 two independent constructors | spec §independent upstream constructors | present |
| AX-SHARED different rationale per problem | spec §fixture design + example | present |
| Paste-layout as I1/I2 prerequisite | program §Paste-layout prerequisite | present |

I found no missing item and no spec that contradicts another.

---

## 2. Two wording ambiguities

### 2a. "Contradictory sources remain attributed" vs DC-001's resolution rule

AX-S1S2-D asserts that contradictory sources "remain attributed rather than silently collapsed". DC-001 says S2 **resolves** the semantic choice where the choice would change clinical meaning.

Both are right, but the assertion as written could be read as forbidding resolution. Suggested wording:

> The non-selected assertion remains recoverable in the IR with its source attribution intact; the selection itself is S2's recorded decision, not a deletion.

That keeps the audit trail while allowing the resolution the architecture requires.

### 2b. AX-SHARED "both rationales recoverable"

The spec requires both rationales preserved for a shared action. It does not say whether "preserved" means *in the note* or *in the IR*.

This matters because the signer's notes are concise: preserving two rationales in prose may fight the style the note is supposed to have. Suggested wording:

> Both rationales are preserved in the IR; the note renders the rationale for the owning problem and may reference the second only where the section contract permits. Preservation is an IR property, not a prose-length requirement.

Without that, a passing run may be a verbose note and a failing run a correctly concise one.

---

## 3. What I did not do

No redesign, no new experiment, no Phase 0. All eight remain DESIGN ONLY / UNRUN.

With those two sentences adjusted, I have nothing further on the program.
