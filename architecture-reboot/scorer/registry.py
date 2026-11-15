"""Frozen Gate 0 predicate registry.

This module is data only. It does not read the seed manifest, artifacts or answer key.
"""

SCORER_VERSION = "GATE0-SCORER-1"

PREDICATES = {
    "S1-CAND-01": {
        "owner": "S1",
        "parent_type": "S1_OUTPUT",
        "mode": "HUMAN_REVIEW",
        "assertion": "every candidate names a neurologic subject for which the encounter poses its own assessment question",
    },
    "S1-CAND-02": {
        "owner": "S1",
        "parent_type": "S1_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "every candidate carries at least one source anchor",
    },
    "S1-AUTH-01": {
        "owner": "S1",
        "parent_type": "S1_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "no candidate carries an adoption or final-state field",
    },
    "S1-AUTH-02": {
        "owner": "S1",
        "parent_type": "S1_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "no candidate carries a selected-claim or final-claim field",
    },
    "S2-REP-01": {
        "owner": "S2",
        "parent_type": "S2_OUTPUT",
        "mode": "HUMAN_REVIEW",
        "assertion": "every approved representation is semantically supported by source objects and relations, not merely by reference existence",
    },
    "S2-TEMP-01": {
        "owner": "S2",
        "parent_type": "S2_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "S2 does not alter the temporality recorded in the substrate",
    },
    "S2-ADOPT-01": {
        "owner": "S2",
        "parent_type": "S2_OUTPUT",
        "mode": "HUMAN_REVIEW",
        "assertion": "for objects the oracle names in expected.adoption, the verdict matches",
    },
    "S3-CAND-01": {
        "owner": "S3",
        "parent_type": "S3_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "candidate outcomes cover every S1 candidate, are exclusive, use known ids, obey REASON-1 reason/basis rules, and equal rendered[]",
    },
    "S3-INC-01": {
        "owner": "S3",
        "parent_type": "S3_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "no rendered A/P problem lacks an approved representation",
    },
    "S3-SEL-01": {
        "owner": "S3",
        "parent_type": "S3_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "every selected representation exists in S2's approved set for that problem",
    },
    "S3-ACCT-01": {
        "owner": "S3",
        "parent_type": "S3_OUTPUT",
        "mode": "MECHANICAL",
        "assertion": "every substrate object is retained or carries a disposition entry",
    },
    "S4-INC-01": {
        "owner": "S4",
        "parent_type": "S4_BLUEPRINT",
        "mode": "MECHANICAL",
        "assertion": "S4 adds or removes no problem relative to S3's rendered set",
    },
    "S4-MEM-01": {
        "owner": "S4",
        "parent_type": "S4_BLUEPRINT",
        "mode": "MECHANICAL",
        "assertion": "every unit member exists in the retained-use map",
    },
    "S4-COMP-01": {
        "owner": "S4",
        "parent_type": "S4_BLUEPRINT",
        "mode": "MECHANICAL",
        "assertion": "every in-domain problem has a claim-bearing unit and every retained plan item has a PLAN unit",
    },
    "S4-REP-01": {
        "owner": "S4",
        "parent_type": "S4_BLUEPRINT",
        "mode": "MECHANICAL",
        "assertion": "every unit representation equals S3's selected_rep for that problem",
    },
    "S4-PROJ-01": {
        "owner": "S4",
        "parent_type": "S4_BLUEPRINT",
        "mode": "MECHANICAL",
        "assertion": "every S4 input-view field matches the exact mapped source path and owner in PROJECTION_MAP",
    },
}

ACTIVE_BY_LAYER = {}
for _pid, _spec in PREDICATES.items():
    ACTIVE_BY_LAYER.setdefault(_spec["parent_type"], []).append(_pid)
for _layer in ACTIVE_BY_LAYER:
    ACTIVE_BY_LAYER[_layer].sort()

HUMAN_PREDICATES = {pid for pid, spec in PREDICATES.items() if spec["mode"] == "HUMAN_REVIEW"}


def predicates_for(parent_type):
    return list(ACTIVE_BY_LAYER.get(parent_type, []))
