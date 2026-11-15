# Proposal and contract index

**Purpose:** one place to see what is canonical, what is an active input, what is folded into the new
six-file Ask flow, and what is historical. This does not delete history; it stops old proposals from
competing with the current contract.

## Canonical now

| item | status | note |
|---|---|---|
| `CONSENSUS_ARCHITECTURE_v0.1.md` | CANONICAL, with one pending amendment | INGEST → STRUCTURE → RENDER and the Case IR are canonical; §1 "one paste / one Ask call" is superseded by D-034 two-surface Scribe + Ask. Amend the production-constraint paragraph only. |
| `CONSENSUS_SUBMODULE_INTERFACES_v1.md` | CANONICAL | Eleven logical modules remain responsibility boundaries. |
| `CONSENSUS.md` | CANONICAL decisions, with the same §1 amendment | Ratified structural decisions remain; Scribe-first topology is superseded by D-034. |
| `DESIGN_CHANGE_LEDGER.md` DC-001 / DC-002 | APPLIED / VERIFIED | Historical design changes, not open proposals. |
| `proposals/chatgpt/113-scribe-evidence-packet-v2.2-turn-preserving-transcript.md` | CURRENT PROVISIONAL | Scribe V2.2 baseline; D-035 removes the 20K design constraint. |
| `proposals/deepseek/026-ask-six-file-decomposition.md` | CURRENT PROPOSAL | Six Ask files/functions and the file-1 handoff. |

## Active inputs

| item | status | disposition |
|---|---|---|
| `proposals/chatgpt/119-ask-semantic-contract-v1.md` | ACTIVE INPUT | Fold the five-domain semantics into files 2–4 of 026; do not keep it as a separate Ask contract. |
| `proposals/deepseek/016-containment-semantics.md` | ACTIVE INPUT | Fold containment/state wording into files 2–3; do not keep as a separate schema proposal. |
| `proposals/deepseek/020-simplification-report.md` | ROADMAP | Option B/D-033 staged simplification; not a contract. |
| `proposals/deepseek/024-ask-experiment.md` | SUPERSEDED IN FORM | The six-file flow replaces the single-contract P/N form. Preserve the four-outcome scoring and failure localization. |
| `experiments/ask/P-N-RUN.md` | HISTORICAL EXPERIMENT TEMPLATE | Superseded by the six-file run protocol; retain scoring ideas. |

## Superseded / historical

| item | status | superseded by |
|---|---|---|
| `proposals/chatgpt/001-state-model-and-view-renderers.md` | SUPERSEDED | `CONSENSUS_ARCHITECTURE_v0.1` + DC-001/002 |
| `proposals/chatgpt/002-doximity-native-execution-model.md` | PARTIALLY SUPERSEDED | Platform facts retained; topology superseded by D-034 |
| `proposals/chatgpt/006-submodule-interface-contracts.md` | SUPERSEDED | `CONSENSUS_SUBMODULE_INTERFACES_v1.md` |
| `proposals/chatgpt/007-function-control-allocation.md` | HISTORICAL REFERENCE | Consensus interfaces + current implementation |
| `proposals/chatgpt/008-two-llm-implementation-workflow.md` | SUPERSEDED | `WORKING_RULES.md`, D-018, D-028 |
| `proposals/chatgpt/009-doximity-experimental-protocol.md` | REFERENCE | Experiment protocol only; no runtime contract |
| `proposals/chatgpt/108-scribe-evidence-packet-v1.md` | SUPERSEDED | Scribe V2.2 |
| `proposals/chatgpt/109-scribe-evidence-packet-v2.md` | SUPERSEDED | Scribe V2.2 |
| `proposals/chatgpt/111-scribe-evidence-packet-v2.1-final-baseline.md` | SUPERSEDED | Scribe V2.2 |
| `proposals/deepseek/001-deepseek-architecture.md` | PARTIALLY SUPERSEDED | Consensus architecture; PROJECT stage withdrawn |
| `proposals/deepseek/002-pipeline-modules.md` | HISTORICAL | Consensus interfaces |
| `proposals/deepseek/003-module-functions.md` | HISTORICAL | Consensus interfaces |
| `proposals/deepseek/004-submodule-goals.md` | HISTORICAL | Consensus interfaces |
| `proposals/deepseek/005-internal-functions.md` | HISTORICAL | Consensus interfaces |
| `proposals/deepseek/006-function-performance.md` | HISTORICAL | Consensus architecture |
| `proposals/deepseek/007`–`012` | APPLIED HISTORY | DC-001/DC-002, not open proposals |
| `proposals/deepseek/013-gate0-reviewer-policy.md` | SUPERSEDED | D-021/D-029 and `REVIEW-POLICY-F-2` |
| `proposals/deepseek/014-semantic-packet-blinding.md` | IMPLEMENTED | F-2 packet policy |
| `proposals/deepseek/024-ask-experiment.md` | SUPERSEDED IN FORM | 026 six-file flow |

## Canonicalization rule

A proposal becomes canonical only when:

1. it describes a current runtime or governance contract, not a historical alternative;
2. its owner and scope are explicit;
3. its inputs/outputs are typed enough to test;
4. it survives review against the current architecture, not an older topology;
5. no later decision supersedes it.

Use `CANONICAL`, `CURRENT PROVISIONAL`, `ACTIVE INPUT`, `FOLD`, `SUPERSEDED`, `APPLIED HISTORY`,
`ROADMAP`, or `REFERENCE`. Do not leave a proposal at "PROPOSED" once it is replaced.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
