"""Execute the accepted PROJECTION_MAP against upstream dependency context.

Pure data transform: no file access, no manifest access, no expected-answer access.
"""


class ProjectionError(Exception):
    pass


def _index_by_type(dependencies):
    out = {}
    for artifact in dependencies.values():
        parent_type = artifact.get("parent_type")
        if parent_type in out:
            raise ProjectionError("duplicate dependency parent_type %s" % parent_type)
        out[parent_type] = artifact
    return out


def build_expected_view(dependencies, oracle, projection_map):
    """Return the S4_INPUT_VIEW implied by the upstream context and the frozen map."""
    if not isinstance(projection_map, dict):
        raise ProjectionError("PROJECTION_MAP is missing")
    contracts = projection_map.get("contracts")
    if not isinstance(contracts, dict):
        raise ProjectionError("PROJECTION_MAP contracts are missing")

    by_type = _index_by_type(dependencies)
    try:
        s1p = by_type["S1_OUTPUT"]
        s2p = by_type["S2_OUTPUT"]
        s3p = by_type["S3_OUTPUT"]
    except KeyError as exc:
        raise ProjectionError("missing dependency %s" % exc.args[0])

    try:
        rendered = s3p["s3"]["rendered"]
        if len(rendered) != 1:
            raise ProjectionError("S4_INPUT_VIEW scope requires exactly one rendered problem")
        problem_id = rendered[0]["problem"]
        selected_rep = rendered[0]["selected_rep"]

        candidates = [c for c in s1p["s1"]["candidates"] if c.get("id") == problem_id]
        if len(candidates) != 1:
            raise ProjectionError("expected one S1 candidate for %s" % problem_id)
        cand = candidates[0]

        reps = [r for r in s2p["s2"]["representations"] if r.get("id") == selected_rep]
        if len(reps) != 1:
            raise ProjectionError("expected one S2 representation for %s" % selected_rep)
        rep = reps[0]
        if rep.get("problem") != problem_id:
            raise ProjectionError("selected representation problem mismatch")
        members = list(rep["members"])
        if not members:
            raise ProjectionError("selected representation has no members")

        relations = [
            r for r in s2p["s2"].get("relations", [])
            if r.get("from") in members and r.get("to") in members
        ]
        claim_relations = []
        for r in s2p["s2"].get("claim_relations", []):
            if "problem" not in r or "representation" not in r:
                raise ProjectionError("claim_relation lacks selectors")
            if r["problem"] == problem_id and r["representation"] == selected_rep:
                claim_relations.append(r)
        duplicate_groups = [
            list(g) for g in s2p["s2"].get("duplicate_groups", [])
            if set(g) & set(members)
        ]

        retained = list(s3p["s3"]["retained"])
        use = dict(s3p["s3"]["use"])
        if set(use) - set(retained):
            raise ProjectionError("S3 use map references a non-retained object")

        ingest = {}
        for oid in retained:
            src = oracle.get("objects", {}).get(oid)
            if not isinstance(src, dict):
                raise ProjectionError("missing oracle object %s" % oid)
            if "text" not in src or "provenance" not in src:
                raise ProjectionError("oracle object %s lacks text/provenance" % oid)
            has_temporal = "temporal" in src
            has_status = "status" in src
            if has_temporal == has_status:
                raise ProjectionError("oracle object %s must have one of temporal/status" % oid)
            rec = {"payload": src["text"], "provenance": src["provenance"]}
            if has_temporal:
                rec["temporal"] = src["temporal"]
            else:
                rec["status"] = src["status"]
            ingest[oid] = rec
    except (KeyError, TypeError, AttributeError) as exc:
        raise ProjectionError("malformed dependency context: %s" % exc)

    return {
        "from_s1": {"problem": cand["id"], "salience": cand["salience"]},
        "from_s3": {
            "selected_rep": selected_rep,
            "rendered": [r["problem"] for r in rendered],
            "retained": retained,
            "use": use,
            "reuse": list(s3p["s3"]["reuse"]),
        },
        "from_s2": {
            "members": members,
            "relations": relations,
            "claim_relations": claim_relations,
            "duplicate_groups": duplicate_groups,
        },
        "from_ingest": ingest,
        "from_contracts": {
            "section": contracts.get("section"),
            "operator_set": contracts.get("operator_set"),
        },
    }
