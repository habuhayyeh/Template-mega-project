"""Scorer-facing wrapper around the shared projection contract.

The executable map and op contracts live only in `projection_contract.py`.
"""
from projection_contract import ProjectionError, build_view as _build_view


def build_expected_view(dependencies, oracle, projection_map):
    by_type = {}
    for artifact in dependencies.values():
        parent_type = artifact.get("parent_type")
        if parent_type in by_type:
            raise ProjectionError("duplicate dependency parent_type %s" % parent_type)
        by_type[parent_type] = artifact
    try:
        s1p = by_type["S1_OUTPUT"]
        s2p = by_type["S2_OUTPUT"]
        s3p = by_type["S3_OUTPUT"]
    except KeyError as exc:
        raise ProjectionError("missing dependency %s" % exc.args[0])
    return _build_view(s1p, s2p, s3p, oracle, projection_map)


__all__ = ["ProjectionError", "build_expected_view"]
