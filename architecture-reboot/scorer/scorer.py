"""Pure Gate 0 scorer.

The scorer receives only:
  target artifact, read-only dependency context, case oracle, frozen rules.

It does not read files, the seed manifest, seed ids, expected predicates, mutation
metadata or the specificity answer key. All predicate results are derived from the
arguments above.
"""
from dataclasses import dataclass, field
import hashlib
import json

from . import registry
from .projection import ProjectionError, build_expected_view

FIRED = "FIRED"
SILENT = "SILENT"
UNDECIDABLE = "UNDECIDABLE"


def _canon(value):
    return "sha256:" + hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass
class Finding:
    predicate_id: str
    owner: str
    status: str
    path: str | None = None
    expected: object = None
    observed: object = None
    detail: str = ""
    evidence: list = field(default_factory=list)
    human_review: dict | None = None

    def to_dict(self):
        out = {
            "predicate_id": self.predicate_id,
            "owner": self.owner,
            "status": self.status,
            "path": self.path,
            "expected": self.expected,
            "observed": self.observed,
            "detail": self.detail,
            "evidence": self.evidence,
        }
        if self.human_review is not None:
            out["human_review"] = self.human_review
        return out


def _fired(pid, path, expected, observed, detail, evidence=None):
    return Finding(pid, registry.PREDICATES[pid]["owner"], FIRED, path, expected,
                   observed, detail, evidence or [])


def _silent(pid, detail="no violation"):
    return Finding(pid, registry.PREDICATES[pid]["owner"], SILENT, detail=detail)


def _undecidable(pid, detail, evidence=None):
    return Finding(pid, registry.PREDICATES[pid]["owner"], UNDECIDABLE,
                   detail=detail, evidence=evidence or [])


def _human(pid):
    return Finding(
        pid, registry.PREDICATES[pid]["owner"], UNDECIDABLE,
        detail="human review required",
        human_review={
            "required": True,
            "packet_kind": pid,
            "reason": "HUMAN_JUDGMENT_REQUIRED",
        },
    )


def _dep(dependencies, parent_type):
    hits = [a for a in dependencies.values() if a.get("parent_type") == parent_type]
    if len(hits) == 1:
        return hits[0]
    return None


def _objects(oracle):
    objects = oracle.get("objects")
    return objects if isinstance(objects, dict) else None


def _candidates(target):
    candidates = target.get("s1", {}).get("candidates")
    return candidates if isinstance(candidates, list) else None


def _outcomes(target):
    outcomes = target.get("s3", {}).get("candidate_outcomes")
    return outcomes if isinstance(outcomes, list) else None


def _rendered(target):
    rendered = target.get("s3", {}).get("rendered")
    return rendered if isinstance(rendered, list) else None


def _view(target):
    view = target.get("s4_input_view")
    return view if isinstance(view, dict) else None


def _first_diff(expected, observed, path=""):
    """Return (path, expected, observed) for the first structural difference."""
    if type(expected) is not type(observed):
        return path or "/", expected, observed
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(observed)):
            p = path + "/" + key
            if key not in expected:
                return p, "<absent>", observed[key]
            if key not in observed:
                return p, expected[key], "<absent>"
            diff = _first_diff(expected[key], observed[key], p)
            if diff:
                return diff
        return None
    if isinstance(expected, list):
        if len(expected) != len(observed):
            return path or "/", expected, observed
        for i, (a, b) in enumerate(zip(expected, observed)):
            diff = _first_diff(a, b, path + "/" + str(i))
            if diff:
                return diff
        return None
    if expected != observed:
        return path or "/", expected, observed
    return None


# ---------------------------------------------------------------------------
# S1


def _s1_auth_01(target, dependencies, oracle, rules):
    pid = "S1-AUTH-01"
    forbidden = {"adopted", "adoption", "adoption_verdict", "resolved", "status_current"}
    candidates = _candidates(target)
    if candidates is None:
        return _undecidable(pid, "s1.candidates is not a list")
    hits = []
    for i, cand in enumerate(candidates):
        if not isinstance(cand, dict):
            return _undecidable(pid, "candidate %d is not an object" % i)
        for key in forbidden:
            if key in cand:
                hits.append({"path": "/s1/candidates/%d/%s" % (i, key),
                             "field": key})
    if hits:
        return _fired(pid, hits[0]["path"], "field absent", "present",
                      "adoption/final-state field present", hits)
    return _silent(pid)


def _s1_auth_02(target, dependencies, oracle, rules):
    pid = "S1-AUTH-02"
    forbidden = {"selected_claim", "final_claim", "chosen_claim"}
    candidates = _candidates(target)
    if candidates is None:
        return _undecidable(pid, "s1.candidates is not a list")
    hits = []
    for i, cand in enumerate(candidates):
        if not isinstance(cand, dict):
            return _undecidable(pid, "candidate %d is not an object" % i)
        for key in forbidden:
            if key in cand:
                hits.append({"path": "/s1/candidates/%d/%s" % (i, key),
                             "field": key})
    if hits:
        return _fired(pid, hits[0]["path"], "field absent", "present",
                      "selected-claim field present", hits)
    return _silent(pid)


def _s1_cand_02(target, dependencies, oracle, rules):
    pid = "S1-CAND-02"
    candidates = _candidates(target)
    if candidates is None:
        return _undecidable(pid, "s1.candidates is not a list")
    hits = []
    for i, cand in enumerate(candidates):
        if not isinstance(cand, dict):
            return _undecidable(pid, "candidate %d is not an object" % i)
        anchors = cand.get("anchors")
        if not isinstance(anchors, list):
            return _undecidable(pid, "candidate %s anchors is not a list"
                                % cand.get("id"))
        if not anchors:
            hits.append({"path": "/s1/candidates/%d/anchors" % i,
                         "candidate": cand.get("id")})
    if hits:
        return _fired(pid, hits[0]["path"], "at least one anchor", "[]",
                      "candidate has no source anchor", hits)
    return _silent(pid)


# ---------------------------------------------------------------------------
# S2


def _s2_temp_01(target, dependencies, oracle, rules):
    pid = "S2-TEMP-01"
    objects = _objects(oracle)
    if objects is None:
        return _undecidable(pid, "oracle.objects is missing")
    adjudication = target.get("s2", {}).get("adjudication")
    if not isinstance(adjudication, list):
        return _undecidable(pid, "s2.adjudication is not a list")
    for i, entry in enumerate(adjudication):
        if not isinstance(entry, dict):
            return _undecidable(pid, "adjudication %d is not an object" % i)
        oid = entry.get("object")
        src = objects.get(oid)
        if not isinstance(src, dict):
            return _undecidable(pid, "oracle object %r is missing" % oid)
        if "temporal" not in src:
            continue
        expected = src["temporal"]
        observed = entry.get("temporal")
        if observed != expected:
            return _fired(
                pid, "/s2/adjudication/%d/temporal" % i, expected, observed,
                "S2 altered substrate temporality for %s" % oid,
                [{"object": oid}],
            )
    return _silent(pid)


# ---------------------------------------------------------------------------
# S3


def _s3_inc_01(target, dependencies, oracle, rules):
    pid = "S3-INC-01"
    rendered = _rendered(target)
    if rendered is None:
        return _undecidable(pid, "s3.rendered is not a list")
    for i, entry in enumerate(rendered):
        if not isinstance(entry, dict):
            return _undecidable(pid, "rendered %d is not an object" % i)
        if not entry.get("approved_representation"):
            return _fired(
                pid, "/s3/rendered/%d/approved_representation" % i,
                "non-null approved representation",
                entry.get("approved_representation"),
                "rendered problem %s has no approved representation"
                % entry.get("problem"),
            )
    return _silent(pid)


def _s3_sel_01(target, dependencies, oracle, rules):
    pid = "S3-SEL-01"
    s2 = _dep(dependencies, "S2_OUTPUT")
    if s2 is None:
        return _undecidable(pid, "S2 dependency context is missing")
    reps = s2.get("s2", {}).get("representations")
    if not isinstance(reps, list):
        return _undecidable(pid, "S2 dependency has no representations list")
    rendered = _rendered(target)
    if rendered is None:
        return _undecidable(pid, "s3.rendered is not a list")
    for i, entry in enumerate(rendered):
        if not isinstance(entry, dict):
            return _undecidable(pid, "rendered %d is not an object" % i)
        problem = entry.get("problem")
        selected = entry.get("selected_rep")
        approved = {
            r.get("id") for r in reps
            if isinstance(r, dict) and r.get("problem") == problem
        }
        if selected not in approved:
            return _fired(
                pid, "/s3/rendered/%d/selected_rep" % i,
                "selected_rep in S2 approved set %s" % sorted(approved),
                selected,
                "selected representation is not in S2's approved set for %s"
                % problem,
                [{"problem": problem, "approved_ids": sorted(approved)}],
            )
    return _silent(pid)


def _s3_acct_01(target, dependencies, oracle, rules):
    pid = "S3-ACCT-01"
    objects = _objects(oracle)
    if objects is None:
        return _undecidable(pid, "oracle.objects is missing")
    s3 = target.get("s3", {})
    retained = s3.get("retained")
    dispositions = s3.get("dispositions")
    if not isinstance(retained, list) or not isinstance(dispositions, list):
        return _undecidable(pid, "s3.retained/dispositions is not a list")
    accounted = set(retained)
    for i, d in enumerate(dispositions):
        if not isinstance(d, dict) or "object" not in d:
            return _undecidable(pid, "disposition %d is malformed" % i)
        accounted.add(d["object"])
    missing = sorted(set(objects) - accounted)
    if missing:
        return _fired(
            pid, "/s3/dispositions", "all substrate objects accounted", missing,
            "unaccounted substrate objects: %s" % ", ".join(missing),
            [{"missing": missing}],
        )
    return _silent(pid)


def _s3_cand_01(target, dependencies, oracle, rules):
    pid = "S3-CAND-01"
    s1 = _dep(dependencies, "S1_OUTPUT")
    if s1 is None:
        return _undecidable(pid, "S1 dependency context is missing")
    s1_candidates = s1.get("s1", {}).get("candidates")
    if not isinstance(s1_candidates, list):
        return _undecidable(pid, "S1 dependency has no candidates list")
    candidate_ids = {c.get("id") for c in s1_candidates if isinstance(c, dict)}
    objects = _objects(oracle)
    if objects is None:
        return _undecidable(pid, "oracle.objects is missing")
    reason_reg = rules.get("reason_registry")
    if not isinstance(reason_reg, dict):
        return _undecidable(pid, "REASON-1 is missing")
    by_code = {r.get("code"): r for r in reason_reg.get("reasons", [])
               if isinstance(r, dict)}
    if not by_code:
        return _undecidable(pid, "REASON-1 has no reasons")

    outcomes = _outcomes(target)
    rendered = _rendered(target)
    if outcomes is None or rendered is None:
        return _undecidable(pid, "candidate_outcomes/rendered is not a list")

    violations = []
    seen = set()
    rendered_from_outcomes = set()
    for i, outcome in enumerate(outcomes):
        if not isinstance(outcome, dict):
            return _undecidable(pid, "outcome %d is not an object" % i)
        cid = outcome.get("candidate")
        if cid not in candidate_ids:
            violations.append({
                "path": "/s3/candidate_outcomes/%d/candidate" % i,
                "kind": "UNKNOWN_CANDIDATE",
                "candidate": cid,
            })
        if cid in seen:
            violations.append({
                "path": "/s3/candidate_outcomes/%d/candidate" % i,
                "kind": "EXCLUSIVITY",
                "candidate": cid,
            })
        seen.add(cid)
        result = outcome.get("outcome")
        if result == "RENDERED":
            if "reason" in outcome or "basis" in outcome:
                violations.append({
                    "path": "/s3/candidate_outcomes/%d" % i,
                    "kind": "RENDERED_HAS_REASON",
                    "candidate": cid,
                })
            rendered_from_outcomes.add(cid)
        elif result == "NOT_RENDERED":
            reason = outcome.get("reason")
            spec = by_code.get(reason)
            if spec is None:
                violations.append({
                    "path": "/s3/candidate_outcomes/%d/reason" % i,
                    "kind": "MISSING_OR_UNKNOWN_REASON",
                    "reason": reason,
                })
                continue
            basis = outcome.get("basis")
            if spec.get("requires_basis"):
                if not isinstance(basis, list) or len(basis) < spec.get("basis_min_items", 1):
                    violations.append({
                        "path": "/s3/candidate_outcomes/%d/basis" % i,
                        "kind": "MISSING_BASIS",
                    })
                else:
                    if spec.get("basis_unique") and len(set(basis)) != len(basis):
                        violations.append({
                            "path": "/s3/candidate_outcomes/%d/basis" % i,
                            "kind": "DUPLICATE_BASIS",
                        })
                    for item in basis:
                        if item not in objects:
                            violations.append({
                                "path": "/s3/candidate_outcomes/%d/basis" % i,
                                "kind": "UNKNOWN_BASIS_TARGET",
                                "target": item,
                            })
            else:
                if "basis" in outcome and outcome["basis"] is not None:
                    violations.append({
                        "path": "/s3/candidate_outcomes/%d/basis" % i,
                        "kind": "BASIS_NOT_ALLOWED",
                    })
        else:
            violations.append({
                "path": "/s3/candidate_outcomes/%d/outcome" % i,
                "kind": "UNKNOWN_OUTCOME",
                "outcome": result,
            })

    missing = sorted(candidate_ids - seen)
    if missing:
        violations.append({
            "path": "/s3/candidate_outcomes",
            "kind": "COVERAGE",
            "missing": missing,
        })

    rendered_set = {r.get("problem") for r in rendered if isinstance(r, dict)}
    if rendered_from_outcomes != rendered_set:
        violations.append({
            "path": "/s3/rendered",
            "kind": "RENDERED_SET_EQUALITY",
            "from_outcomes": sorted(rendered_from_outcomes),
            "rendered": sorted(rendered_set),
        })

    if violations:
        first = violations[0]
        return _fired(
            pid, first["path"], "S3-CAND-01 constraints satisfied",
            first["kind"], "%d S3-CAND-01 violation(s)" % len(violations),
            violations,
        )
    return _silent(pid)


# ---------------------------------------------------------------------------
# S4


def _s4_inc_01(target, dependencies, oracle, rules):
    pid = "S4-INC-01"
    view = _view(target)
    problems = target.get("s4", {}).get("problems")
    if view is None or not isinstance(problems, list):
        return _undecidable(pid, "S4 input view/problems missing")
    rendered = view.get("from_s3", {}).get("rendered")
    if not isinstance(rendered, list):
        return _undecidable(pid, "from_s3.rendered is missing")
    sources = {p.get("source") for p in problems if isinstance(p, dict)}
    if sources != set(rendered):
        return _fired(
            pid, "/s4/problems",
            "problem sources equal from_s3.rendered %s" % sorted(rendered),
            sorted(sources),
            "S4 problem set diverges from S3 rendered set",
            [{"s4_sources": sorted(sources), "rendered": sorted(rendered)}],
        )
    return _silent(pid)


def _s4_rep_01(target, dependencies, oracle, rules):
    pid = "S4-REP-01"
    view = _view(target)
    units = target.get("s4", {}).get("units")
    problems = target.get("s4", {}).get("problems")
    if view is None or not isinstance(units, list) or not isinstance(problems, list):
        return _undecidable(pid, "S4 view/units/problems missing")
    rendered = view.get("from_s3", {}).get("rendered")
    selected_reps = view.get("from_s3", {}).get("selected_reps")
    if not isinstance(rendered, list) or not isinstance(selected_reps, dict):
        return _undecidable(pid, "from_s3 rendered/selected_reps missing")
    source_by_problem = {
        p.get("id"): p.get("source") for p in problems if isinstance(p, dict)
    }
    for i, unit in enumerate(units):
        if not isinstance(unit, dict):
            return _undecidable(pid, "unit %d is not an object" % i)
        source = source_by_problem.get(unit.get("problem"))
        if source is None or source not in rendered:
            # Missing problem membership is S4-INC-01's finding.
            continue
        selected = selected_reps.get(source)
        if selected is None:
            return _undecidable(pid, "from_s3.selected_reps lacks %s" % source)
        if unit.get("representation") != selected:
            return _fired(
                pid, "/s4/units/%d/representation" % i, selected,
                unit.get("representation"),
                "unit representation differs from selected_reps for %s" % source,
            )
    return _silent(pid)


def _s4_mem_01(target, dependencies, oracle, rules):
    pid = "S4-MEM-01"
    view = _view(target)
    units = target.get("s4", {}).get("units")
    if view is None or not isinstance(units, list):
        return _undecidable(pid, "S4 view/units missing")
    use = view.get("from_s3", {}).get("use")
    if not isinstance(use, dict):
        return _undecidable(pid, "from_s3.use is missing")
    retained_use = set(use)
    for i, unit in enumerate(units):
        if not isinstance(unit, dict):
            return _undecidable(pid, "unit %d is not an object" % i)
        members = unit.get("members")
        if not isinstance(members, list):
            return _undecidable(pid, "unit %d members is not a list" % i)
        for j, member in enumerate(members):
            if member not in retained_use:
                return _fired(
                    pid, "/s4/units/%d/members/%d" % (i, j),
                    "member in retained-use map", member,
                    "unit member is absent from from_s3.use",
                )
    return _silent(pid)


def _s4_comp_01(target, dependencies, oracle, rules):
    pid = "S4-COMP-01"
    view = _view(target)
    problems = target.get("s4", {}).get("problems")
    units = target.get("s4", {}).get("units")
    if view is None or not isinstance(problems, list) or not isinstance(units, list):
        return _undecidable(pid, "S4 view/problems/units missing")
    rendered = view.get("from_s3", {}).get("rendered")
    retained = view.get("from_s3", {}).get("retained")
    if not isinstance(rendered, list) or not isinstance(retained, list):
        return _undecidable(pid, "from_s3 rendered/retained missing")
    plan_items = oracle.get("expected", {}).get("plan_items_requiring_units")
    if not isinstance(plan_items, list):
        return _undecidable(pid, "oracle plan_items_requiring_units is missing")

    claim_operators = {"FACT", "REASONING", "CLAIM"}
    domain = [p for p in problems if isinstance(p, dict) and p.get("source") in rendered]
    for problem in domain:
        pid_s4 = problem.get("id")
        has_claim = any(
            isinstance(u, dict) and u.get("problem") == pid_s4
            and u.get("operator") in claim_operators
            for u in units
        )
        if not has_claim:
            return _fired(
                pid, "/s4/problems", "claim-bearing unit for %s" % pid_s4,
                "absent", "in-domain problem has no claim-bearing unit",
                [{"problem": pid_s4, "source": problem.get("source")}],
            )

    for item in plan_items:
        if item not in retained:
            continue
        has_plan = any(
            isinstance(u, dict) and u.get("operator") == "PLAN"
            and isinstance(u.get("members"), list) and item in u["members"]
            for u in units
        )
        if not has_plan:
            return _fired(
                pid, "/s4/units", "PLAN unit for retained plan item %s" % item,
                "absent", "retained plan item has no PLAN unit",
                [{"plan_item": item}],
            )
    return _silent(pid)


def _s4_proj_01(target, dependencies, oracle, rules):
    pid = "S4-PROJ-01"
    pmap = rules.get("projection_map")
    if not isinstance(pmap, dict):
        return _undecidable(pid, "PROJECTION_MAP is missing")
    view = _view(target)
    if view is None:
        return _fired(pid, "/s4_input_view", "mapped projection object", "<absent>",
                      "S4 input view is missing")
    try:
        expected = build_expected_view(dependencies, oracle, pmap)
    except ProjectionError as exc:
        return _undecidable(pid, "cannot build expected projection: %s" % exc)
    diff = _first_diff(expected, view)
    if diff:
        path, expected_value, observed_value = diff
        return _fired(
            pid, "/s4_input_view" + path, expected_value, observed_value,
            "S4 input view does not match the mapped source projection",
            [{"first_diff": path}],
        )
    return _silent(pid)



def _s2_causal_02(target, dependencies, oracle, rules):
    pid = "S2-CAUSAL-02"
    rels = target.get("s2", {}).get("causal_relations")
    if not isinstance(rels, list):
        return _undecidable(pid, "causal_relations is missing")
    objects = oracle.get("objects", {})
    spans = oracle.get("spans", {})
    nouns = {"CONTRIBUTOR", "ETIOLOGY", "MECHANISM", "CAUSE"}
    strengths = {"LIKELY", "POSSIBLE", "UNLIKELY"}
    for i, rel in enumerate(rels):
        if not isinstance(rel, dict):
            return _fired(pid, "/s2/causal_relations/%d" % i,
                          "causal relation object", repr(rel),
                          "causal relation is not an object")
        for key in ("from", "to", "relation", "strength", "support"):
            if key not in rel:
                return _fired(pid, "/s2/causal_relations/%d/%s" % (i, key),
                              "required causal field", "absent",
                              "causal relation is missing %s" % key)
        if rel["relation"] not in nouns:
            return _fired(pid, "/s2/causal_relations/%d/relation" % i,
                          sorted(nouns), rel["relation"],
                          "causal relation noun is outside the closed set")
        if rel["strength"] not in strengths:
            return _fired(pid, "/s2/causal_relations/%d/strength" % i,
                          sorted(strengths), rel["strength"],
                          "causal strength is outside the closed set")
        if rel["from"] not in objects:
            return _fired(pid, "/s2/causal_relations/%d/from" % i,
                          "known oracle object", rel["from"],
                          "causal from endpoint is not an oracle object")
        if rel["to"] not in objects:
            return _fired(pid, "/s2/causal_relations/%d/to" % i,
                          "known oracle object", rel["to"],
                          "causal to endpoint is not an oracle object")
        if rel["from"] == rel["to"]:
            return _fired(pid, "/s2/causal_relations/%d" % i,
                          "distinct endpoints", "same object",
                          "causal relation is self-referential")
        support = rel["support"]
        if not isinstance(support, list) or not support:
            return _fired(pid, "/s2/causal_relations/%d/support" % i,
                          "non-empty support span list", support,
                          "causal support is missing")
        for j, span in enumerate(support):
            if span not in spans:
                return _fired(pid, "/s2/causal_relations/%d/support/%d" % (i, j),
                              "known oracle span", span,
                              "causal support span is unknown")
    return _silent(pid)


def _s3_role_02(target, dependencies, oracle, rules):
    pid = "S3-ROLE-02"
    rendered = target.get("s3", {}).get("rendered")
    if not isinstance(rendered, list):
        return _undecidable(pid, "rendered is missing")
    for i, entry in enumerate(rendered):
        if not isinstance(entry, dict):
            return _fired(pid, "/s3/rendered/%d" % i,
                          "rendered entry object", repr(entry),
                          "rendered entry is not an object")
        if entry.get("encounter_role") not in ("PRIMARY", "BACKGROUND"):
            return _fired(pid, "/s3/rendered/%d/encounter_role" % i,
                          "PRIMARY or BACKGROUND", entry.get("encounter_role"),
                          "rendered problem has missing or invalid encounter_role")
    return _silent(pid)


def _s4_role_01(target, dependencies, oracle, rules):
    pid = "S4-ROLE-01"
    view = _view(target)
    problems = target.get("s4", {}).get("problems")
    if view is None or not isinstance(problems, list):
        return _undecidable(pid, "S4 view/problems missing")
    roles = view.get("from_s3", {}).get("selected_roles")
    if not isinstance(roles, dict):
        return _undecidable(pid, "from_s3.selected_roles is missing")
    for i, problem in enumerate(problems):
        if not isinstance(problem, dict):
            return _undecidable(pid, "problem %d is not an object" % i)
        source = problem.get("source")
        expected = roles.get(source)
        if expected is None:
            continue
        if problem.get("encounter_role") != expected:
            return _fired(pid, "/s4/problems/%d/encounter_role" % i,
                          expected, problem.get("encounter_role"),
                          "S4 encounter role does not match S3 selected role")
    return _silent(pid)

MECHANICAL = {
    "S1-AUTH-01": _s1_auth_01,
    "S1-AUTH-02": _s1_auth_02,
    "S1-CAND-02": _s1_cand_02,
    "S2-TEMP-01": _s2_temp_01,
    "S2-CAUSAL-02": _s2_causal_02,
    "S3-INC-01": _s3_inc_01,
    "S3-SEL-01": _s3_sel_01,
    "S3-ACCT-01": _s3_acct_01,
    "S3-CAND-01": _s3_cand_01,
    "S3-ROLE-02": _s3_role_02,
    "S4-INC-01": _s4_inc_01,
    "S4-MEM-01": _s4_mem_01,
    "S4-COMP-01": _s4_comp_01,
    "S4-REP-01": _s4_rep_01,
    "S4-PROJ-01": _s4_proj_01,
    "S4-ROLE-01": _s4_role_01,
}


def score(target, dependencies, oracle, rules):
    """Score all active predicates owned by the target artifact's parent_type."""
    if not isinstance(target, dict):
        raise ValueError("target artifact must be an object")
    parent_type = target.get("parent_type")
    if parent_type not in registry.ACTIVE_BY_LAYER:
        raise ValueError("unknown target parent_type %r" % parent_type)
    if not isinstance(dependencies, dict):
        raise ValueError("dependencies must be an object keyed by parent_id")
    if not isinstance(oracle, dict):
        raise ValueError("oracle must be an object")
    if not isinstance(rules, dict):
        raise ValueError("rules must be an object")

    findings = []
    for pred_id in registry.predicates_for(parent_type):
        if pred_id in registry.SEMANTIC_PREDICATES:
            findings.append(_human(pred_id))
            continue
        try:
            finding = MECHANICAL[pred_id](target, dependencies, oracle, rules)
        except Exception as exc:  # malformed input is explicit, not silent
            finding = _undecidable(pred_id, "scorer error: %s" % exc)
        findings.append(finding)

    return {
        "scorer_version": registry.SCORER_VERSION,
        "target": {
            "case": target.get("case"),
            "parent_id": target.get("parent_id"),
            "parent_type": parent_type,
            "hash": _canon(target),
        },
        "findings": [f.to_dict() for f in findings],
        "by_predicate": {f.predicate_id: f.status for f in findings},
    }
