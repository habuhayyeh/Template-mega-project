# BLOCKED — semantic packets leak expected answers

Review 089 found that S1-CAND-01 packets include `candidate_concepts_must_exclude` and S2-ADOPT-01
packets include `expected.adoption`. These packets must not be used for signer references or evaluator
judgments.

`proposals/deepseek/014-semantic-packet-blinding.md` defines the correction. Regenerate this run after
approval.
