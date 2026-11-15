# 021D — Adversarial line-by-line review: CHANGE_CONTROL.md

## Verdict

**NEEDS GOVERNANCE REVISION.**

The four-category model is valuable. The current definitions still contain unsafe edit-type assumptions, missing semantic-authority protection, overbroad invalidation, and acceptance-history rules that do not scale or preserve experiment provenance.

| Lines | Claim | Assessment | Challenge / required defense |
|---|---|---|---|
| 3 | old work moved goalposts under patch | PLAUSIBLE MOTIVATION | If retained as factual history, cite a concrete example or soften to motivation rather than evidence claim. |
| 7 | typo/formatting/comment/link/whitespace = patch | UNSAFE | Whitespace can alter YAML/prompt semantics; links can change authoritative dependency; comments may be parsed into prompt packages. Classify by verified behavioral/contract effect, not edit type. |
| 9 | patch requires only commit | TOO PERMISSIVE | A claimed patch should at least pass BUILD/serialization sanity where relevant. |
| 9 | may not touch rule/check/fixture/contract statement | SOUND GUARD | Keep, but a nonsemantic typo inside a rule may then be impossible to classify as patch. Clarify. |
| 11 | if governing word changes, not patch | SOUND | Effect-based framing should dominate line 7. |
| 15 | implementation change preserves contract/interface/acceptance | INCOMPLETE | Add semantic authority/decision ownership. Frozen workflow explicitly treats authority changes as DESIGN. |
| 15 | outputs may vary within properties | SOUND | Keep. |
| 17 | error-message improvement as implementation change | CONDITIONAL | If error text/token is an acceptance property, this becomes acceptance change. Example needs caveat. |
| 19 | altering a check/assertion always acceptance change | OVERBROAD | Changing the *acceptance definition/check specification* is acceptance change. Fixing implementation code of a checker to correctly implement an unchanged check is an implementation change. Distinguish spec from checker code. |
| 22 | frozen properties hold | SOUND | Add semantic authority. |
| 23 | no contract file changes | TOO FILE-CENTRIC | A file can contain implementation + contract, or formatting patch. Classify by semantic authority/content, not file path. Better separation is preferable. |
| 24 | module regression fixtures | TOO NARROW FOR DOXIMITY | C14 showed non-local prompt sensitivity. Doximity-facing changes need targeted + dependency-based + non-local sentinel/full relevant corpus, possibly paired A/B. |
| 28 | design change if shared contract or decision affects >1 module | INCOMPLETE/OVERBROAD | A semantic-authority change within one module is also design. Conversely a purely nonsemantic shared-file refactor may not be. Define by authority/contract semantics, not number of modules. |
| 31-34 | proposal/review/signer/dependent regressions | GOOD CORE | Dependency graph needed to know what is dependent. |
| 36 | any design change invalidates prior acceptance results | OVERBROAD | Invalidate changed artifact + dependent artifacts whose assumptions may be affected, not unrelated accepted modules. |
| 40 | acceptance change definition | INCOMPLETE | Add severity, scoring rule, baseline/reference expectation, and acceptance-gate logic. |
| 40 | any alteration of a check = acceptance change | NEEDS SPEC/IMPLEMENTATION DISTINCTION | Same as line 19. |
| 42 | test added after implementation is shaped by implementation | OVERGENERALIZATION | New historical evidence can motivate a valid test. The risk is post-hoc scoring, not mere timing. |
| 44 | "most dangerous" because makes failing test pass | RHETORICALLY FALSE FOR ADDITIONS | Adding a stricter test can make passing harder. The dangerous subset is relaxing/redefining success after failure. |
| 47 | every acceptance change explains why old expectation wrong | DOES NOT FIT ADDITIONS | A newly added invariant may not make any old expectation wrong. Separate ADD vs MODIFY/REMOVE. |
| 48 | approval from reviewer who wrote original | NOT DURABLE | Use current independent acceptance owner/reviewer role. Original agent/session may not exist later. |
| 49 | old/new expectation always in fixture register | WRONG AUTHORITY | Acceptance changes can affect threshold/check/scoring/brief property without changing a fixture. Record all in change ledger; fixture history only when fixture/assertion changes. |
| 50 | failing implementation cannot justify goalpost movement without evidence | STRONGLY SOUND | Keep. |
| 52 | repeated acceptance changes = evidence architecture wrong | OVERCLAIM | Could indicate bad baseline, checker bugs, evolving signer preference, or architecture. Treat as trigger for design review, not proof. |
| 54-61 | role table | GOOD BASE | IMPLEMENTATION CHANGE reviewer should confirm authority invariance and non-local regression obligations; acceptance-change signer involvement should include style/product baselines, not only clinical. |
| 63 | engineer cannot self-approve acceptance change | SOUND | Keep. |
| 65 | signer "approves or is informed" | AMBIGUOUS | Table contains none/conditional approval, not an explicit informed state. Define when notification is required. |
| 69 | record in CHANGELOG.md | AUTHORITY AMBIGUITY | Root CHANGELOG is old/main pipeline history. Decide dedicated reboot changelog vs shared project changelog explicitly. |
| 72 | example F-09 seizure precautions | STALE/WRONG | F-09 is not the current fixture id and seizure precautions is F-06. The governance example itself is inconsistent with the register. |
| 72 | approved reviewer only | POTENTIAL POLICY VIOLATION | If this changed a signer-approved clinical baseline, signer approval would also be required. |
| 75 | unrecorded change "did not happen" | GOVERNANCE FICTION | The git change may have happened; it should be "not valid for acceptance / not recognized as governed." |

## Missing change-control rules

1. **No retroactive rescoring**
   - a run is interpreted under the acceptance version frozen when it ran;
   - changed criteria require a new scored result/rerun where material.

2. **Dependency-based invalidation**
   - requires implementation manifest/dependency graph.

3. **Checker implementation vs check specification**
   - bugfix to validator code ≠ changing success definition.

4. **Semantic authority/decision ownership**
   - moving a decision between submodules is DESIGN even if surface output unchanged.

5. **Doximity non-local regression**
   - targeted + dependency + sentinel/full relevant corpus.

6. **Role-based approval**
   - survive agent/session replacement.

## DeepSeek must answer

Defend especially:
- why whitespace/link edits are safe patches;
- why checker-code bugfixes are acceptance changes;
- why every design change invalidates all prior acceptance;
- why every acceptance change belongs in FIXTURE_REGISTER;
- where reboot change history should live.
