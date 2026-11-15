#!/usr/bin/env python3
"""Gate 0 harness.

The harness owns the answer key. The scorer does not.

Modes:
  packets     build blinded semantic packets and per-artifact scorer evidence
  acceptance  aggregate one signer reference + two LLM evaluators and evaluate Gate 0

The acceptance mode is intentionally not run by the build or tests. Building the
scorer is not Gate 0 execution.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scorer import FIRED, SILENT, UNDECIDABLE, score  # noqa: E402
from scorer import registry  # noqa: E402

GEN = os.path.join(ROOT, 'experiments/gate0/seeds/generated')
AX = os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D')
SCHEMA = os.path.join(AX, 'schema.md')
PREDICATES = os.path.join(AX, 'predicates.md')
ORACLE = os.path.join(AX, 'fixtures/CASE-01/oracle.json')
MANIFEST = os.path.join(GEN, 'MANIFEST.json')
G0_SEEDS = os.path.join(ROOT, 'experiments/gate0/seeds/G0-SEEDS.md')
G0_MANIFEST = os.path.join(ROOT, 'experiments/gate0/00-GATE0-MANIFEST.md')
PROGRAM = os.path.join(ROOT, 'experiments/architecture/00-ARCHITECTURE-EXPERIMENT-PROGRAM.md')
AX_SPEC = os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D.md')
INTERFACES = os.path.join(ROOT, 'CONSENSUS_SUBMODULE_INTERFACES_v1.md')
ARCHITECTURE = os.path.join(ROOT, 'CONSENSUS_ARCHITECTURE_v0.1.md')

GOVERNING_PATHS = {
    'CONSENSUS_SUBMODULE_INTERFACES_v1.md': INTERFACES,
    'CONSENSUS_ARCHITECTURE_v0.1.md': ARCHITECTURE,
    '00-ARCHITECTURE-EXPERIMENT-PROGRAM.md': PROGRAM,
    'AX-S1S2-D.md': AX_SPEC,
    'schema.md': SCHEMA,
    'predicates.md': PREDICATES,
    'G0-SEEDS.md': G0_SEEDS,
    'make_seeds.py': os.path.join(ROOT, 'tools/make_seeds.py'),
    '00-GATE0-MANIFEST.md': G0_MANIFEST,
    'oracle.json': ORACLE,
}
EXPECTED_IDENTITIES = {
    'campaign': 'GATE0-C1',
    'registry': 'PILOT-2',
    'active_set': 'ACTIVE-PILOT-2',
    'schema': 'SCHEMA-2',
    'oracle': 'ORACLE-2.0',
    'specificity_policy': 'FULL_SILENCE-WITHIN-LAYER',
}
REVIEW_POLICY = 'REVIEW-POLICY-F-1'


class InputIntegrityError(Exception):
    pass


def canon(value):
    return 'sha256:' + hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    ).hexdigest()


def file_sha(path):
    with io.open(path, 'rb') as fh:
        return 'sha256:' + hashlib.sha256(fh.read()).hexdigest()


def read_block(path, name):
    with io.open(path, encoding='utf-8') as fh:
        text = fh.read()
    pat = re.compile(
        r'<!-- BEGIN:' + re.escape(name) + r' -->\s*```json\s*(.*?)```\s*<!-- END:' + name + r' -->',
        re.S)
    match = pat.search(text)
    if not match:
        raise InputIntegrityError('%s is missing %s' % (path, name))
    return json.loads(match.group(1))


def load_json(path):
    with io.open(path, encoding='utf-8') as fh:
        return json.load(fh)


def active_predicates_from_source(path=PREDICATES):
    with io.open(path, encoding='utf-8') as fh:
        text = fh.read()
    match = re.search(r'## Pilot ACTIVE_PREDICATE_SET.*?```text\s*(.*?)```', text, re.S)
    if not match:
        raise InputIntegrityError('predicates.md has no ACTIVE_PREDICATE_SET block')
    return {p.strip() for p in re.split(r'[,\n]', match.group(1)) if p.strip()}


def verify_governing_hashes(manifest, paths=None):
    paths = paths or GOVERNING_PATHS
    recorded = manifest.get('governing_hashes')
    if not isinstance(recorded, dict) or not recorded:
        raise InputIntegrityError('MANIFEST governing_hashes is missing')
    missing = set(paths) - set(recorded)
    if missing:
        raise InputIntegrityError('MANIFEST is missing governing hashes: %s'
                                  % sorted(missing))
    for key, expected in recorded.items():
        if key not in paths:
            raise InputIntegrityError('unknown governing hash %s' % key)
        actual = file_sha(paths[key])
        if actual != expected:
            raise InputIntegrityError('governing hash mismatch for %s' % key)


def verify_campaign_contract(manifest):
    for key, expected in EXPECTED_IDENTITIES.items():
        if manifest.get(key) != expected:
            raise InputIntegrityError('campaign identity %s=%r, expected %r'
                                      % (key, manifest.get(key), expected))
    verify_governing_hashes(manifest)
    source_active = active_predicates_from_source()
    if source_active != set(registry.PREDICATES):
        raise InputIntegrityError('scorer registry does not match accepted active set')


def write_json(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(value, fh, indent=2, sort_keys=True)
        fh.write('\n')


def load_campaign():
    manifest = load_json(MANIFEST)
    verify_campaign_contract(manifest)
    oracle = load_json(ORACLE)
    rules = {
        'reason_registry': read_block(SCHEMA, 'REASON_REGISTRY'),
        'projection_map': read_block(SCHEMA, 'PROJECTION_MAP'),
    }
    clean = {}
    for parent_id, rec in manifest['clean_parents'].items():
        artifact = load_json(os.path.join(GEN, rec['artifact']))
        if canon(artifact) != rec['hash']:
            raise InputIntegrityError('clean parent %s hash mismatch' % parent_id)
        clean[parent_id] = artifact
    return manifest, clean, oracle, rules


def dependency_context(manifest, clean, target_type):
    """Return hash-checked, seed-independent upstream context for a target type."""
    if target_type not in manifest['dependency_context']:
        raise InputIntegrityError('no dependency matrix for %s' % target_type)
    context = {}
    pinned = []
    for entry in manifest['dependency_context'][target_type]:
        parent_id = entry['parent_id']
        if parent_id not in clean:
            raise InputIntegrityError('dependency %s is absent' % parent_id)
        artifact = clean[parent_id]
        if artifact.get('parent_type') != entry['parent_type']:
            raise InputIntegrityError('dependency %s type mismatch' % parent_id)
        if canon(artifact) != entry['hash']:
            raise InputIntegrityError('dependency %s hash mismatch' % parent_id)
        context[parent_id] = artifact
        pinned.append({
            'parent_id': parent_id,
            'parent_type': entry['parent_type'],
            'hash': entry['hash'],
        })
    return context, pinned


def _subset_oracle(oracle, expected_keys):
    out = {}
    if 'expected' in oracle:
        expected = {k: oracle['expected'][k] for k in expected_keys if k in oracle['expected']}
        if expected:
            out['expected'] = expected
    for key in ('objects', 'spans', 'matching'):
        if key in oracle:
            out[key] = oracle[key]
    return out


def _dep_by_type(context, parent_type):
    hits = [a for a in context.values() if a.get('parent_type') == parent_type]
    return hits[0] if len(hits) == 1 else None


def build_packet(predicate_id, target, context, oracle):
    spec = registry.PREDICATES[predicate_id]
    if predicate_id == 'S1-CAND-01':
        packet_oracle = _subset_oracle(oracle, ['candidate_concepts_must_exclude'])
        packet_context = {}
        instructions = (
            'Decide whether every S1 candidate names a neurologic subject for which the '
            'encounter poses its own assessment question. Use only the target artifact, '
            'the supplied oracle material and the rule. Record FIRED or SILENT.'
        )
    elif predicate_id == 'S2-ADOPT-01':
        packet_oracle = _subset_oracle(oracle, ['adoption'])
        packet_context = {}
        instructions = (
            'Compare S2 adoption verdicts with the oracle expected.adoption entries. '
            'Objects not named in the oracle are not scored. Record FIRED or SILENT.'
        )
    elif predicate_id == 'S2-REP-01':
        packet_oracle = _subset_oracle(oracle, [])
        s1 = _dep_by_type(context, 'S1_OUTPUT')
        packet_context = {'S1_OUTPUT': s1} if s1 else {}
        instructions = (
            'Judge whether each approved representation is semantically supported by '
            'its members and their relations, not merely whether ids and support refs '
            'exist. The S1 problem/claim context is supplied so you can identify the '
            'claim being supported. Record FIRED or SILENT.'
        )
    else:
        raise ValueError('no semantic packet defined for %s' % predicate_id)

    packet_body = {
        'predicate': {
            'id': predicate_id,
            'owner': spec['owner'],
            'assertion': spec['assertion'],
            'mode': spec['mode'],
            'instructions': instructions,
        },
        'target_artifact': target,
        'dependency_context': packet_context,
        'oracle': packet_oracle,
    }
    digest = hashlib.sha256(
        json.dumps(packet_body, sort_keys=True, separators=(',', ':')).encode()
    ).hexdigest()
    packet = dict(packet_body)
    packet['packet_id'] = 'pkt-' + digest[:24]
    packet['judgment_schema'] = {
        'required': ['packet_id', 'predicate_id', 'judge_id', 'judge_type',
                     'role', 'verdict', 'rationale', 'policy_version'],
        'judge_types': ['HUMAN', 'LLM'],
        'roles': ['REFERENCE', 'EVALUATOR'],
        'verdict_values': [FIRED, SILENT, UNDECIDABLE],
        'reference': 'one HUMAN / REFERENCE judgment with authority SIGNER_CLINICIAN',
        'reference_authority': 'SIGNER_CLINICIAN',
        'evaluators': 'two independent LLM / EVALUATOR judgments, different model families and sessions',
        'policy_version': REVIEW_POLICY,
    }
    return packet


def attach_packets(result, context, oracle, packet_dir=None):
    packets = {}
    for finding in result['findings']:
        if not finding.get('human_review'):
            continue
        pid = finding['predicate_id']
        packet = build_packet(pid, result['target_for_packet'], context, oracle)
        packets[pid] = packet
        finding['packet_id'] = packet['packet_id']
        if packet_dir:
            write_json(os.path.join(packet_dir, packet['packet_id'] + '.json'), packet)
    return packets


def _validate_review_record(record, index):
    if not isinstance(record, dict):
        raise ValueError('review record %d is not an object' % index)
    for key in ('packet_id', 'predicate_id', 'judge_id', 'judge_type',
                'role', 'verdict', 'rationale', 'policy_version'):
        if key not in record:
            raise ValueError('review record %d is missing %s' % (index, key))
    if record['policy_version'] != REVIEW_POLICY:
        raise ValueError('review record %d has policy %r, expected %r'
                         % (index, record['policy_version'], REVIEW_POLICY))
    if record['role'] not in ('REFERENCE', 'EVALUATOR'):
        raise ValueError('review record %d has invalid role' % index)
    if record['verdict'] not in (FIRED, SILENT, UNDECIDABLE):
        raise ValueError('review record %d has invalid verdict' % index)
    if record['role'] == 'REFERENCE':
        if record['judge_type'] != 'HUMAN':
            raise ValueError('reference record %d must be HUMAN' % index)
        if record.get('authority') != 'SIGNER_CLINICIAN':
            raise ValueError('reference record %d must declare SIGNER_CLINICIAN authority' % index)
    else:
        if record['judge_type'] != 'LLM':
            raise ValueError('evaluator record %d must be LLM' % index)
        for key in ('model_family', 'model_version', 'session_id'):
            if not record.get(key):
                raise ValueError('evaluator record %d is missing %s' % (index, key))
        if record.get('context_scope') != 'PACKET_ONLY':
            raise ValueError('evaluator record %d is not packet-only' % index)
        if record.get('project_context_agent') is not False:
            raise ValueError('evaluator record %d is a project-context agent' % index)


def load_review_evidence(path):
    if not path:
        return {'policy_version': REVIEW_POLICY, 'references': [], 'evaluators': []}
    data = load_json(path)
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        if data.get('policy_version') not in (None, REVIEW_POLICY):
            raise ValueError('review evidence policy version is not %s' % REVIEW_POLICY)
        if data.get('review_policy') not in (None, REVIEW_POLICY):
            raise ValueError('review evidence policy is not %s' % REVIEW_POLICY)
        records = list(data.get('references', [])) + list(data.get('evaluators', []))
    else:
        raise ValueError('review evidence must be a list or object')
    references, evaluators = [], []
    for i, record in enumerate(records):
        _validate_review_record(record, i)
        (references if record['role'] == 'REFERENCE' else evaluators).append(record)
    return {
        'policy_version': REVIEW_POLICY,
        'references': references,
        'evaluators': evaluators,
    }


def _reference_key(record):
    return (record['packet_id'], record['predicate_id'], record['policy_version'])


def _evaluator_key(record):
    return (record['packet_id'], record['predicate_id'], record['policy_version'],
            record['judge_id'], record['model_family'], record['model_version'])


def merge_review_evidence(baseline, current):
    out_refs, out_evals = {}, {}
    for source in (baseline, current):
        for record in source.get('references', []):
            key = _reference_key(record)
            if key in out_refs and out_refs[key]['verdict'] != record['verdict']:
                raise ValueError('conflicting reference verdict for %s' % (key,))
            out_refs[key] = record
        for record in source.get('evaluators', []):
            key = _evaluator_key(record)
            if key in out_evals and out_evals[key]['verdict'] != record['verdict']:
                raise ValueError('conflicting evaluator verdict for %s' % (key,))
            out_evals[key] = record
    return {
        'policy_version': REVIEW_POLICY,
        'references': list(out_refs.values()),
        'evaluators': list(out_evals.values()),
    }


def validate_review_evidence(packets_by_id, references, evaluators):
    ref_by_packet = {}
    eval_judges = {}
    for record in list(references) + list(evaluators):
        packet = packets_by_id.get(record.get('packet_id'))
        if packet is None:
            raise ValueError('review evidence references unknown packet %r'
                             % record.get('packet_id'))
        if record.get('predicate_id') != packet['predicate']['id']:
            raise ValueError(
                'review predicate %r does not match packet predicate %r'
                % (record.get('predicate_id'), packet['predicate']['id']))
        if packet['predicate']['id'] not in registry.SEMANTIC_PREDICATES:
            raise ValueError('review evidence targets a non-semantic predicate %s'
                             % packet['predicate']['id'])
        if record['role'] == 'REFERENCE':
            if record['packet_id'] in ref_by_packet:
                raise ValueError('multiple reference records for packet %s'
                                 % record['packet_id'])
            ref_by_packet[record['packet_id']] = record
        else:
            seen = eval_judges.setdefault(record['packet_id'], set())
            if record['judge_id'] in seen:
                raise ValueError('duplicate evaluator judge for packet %s'
                                 % record['packet_id'])
            seen.add(record['judge_id'])


def aggregate_semantic(result, packets, references, evaluators, expected_by_pid):
    packets_by_id = {p['packet_id']: p for p in packets.values()}
    validate_review_evidence(packets_by_id, references, evaluators)
    ref_by_packet = {r['packet_id']: r for r in references}
    eval_by_packet = {}
    for r in evaluators:
        eval_by_packet.setdefault(r['packet_id'], []).append(r)

    for finding in result['findings']:
        pid = finding['predicate_id']
        if not finding.get('human_review'):
            continue
        finding.pop('calibration_failure', None)
        finding.pop('reference', None)
        finding.pop('evaluators', None)
        packet = packets.get(pid)
        if packet is None:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'SEMANTIC_PACKET_MISSING'
            continue
        reference = ref_by_packet.get(packet['packet_id'])
        if reference is None:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'SIGNER_REFERENCE_MISSING'
            continue
        evals = eval_by_packet.get(packet['packet_id'], [])
        if len(evals) != 2 or len({e['judge_id'] for e in evals}) != 2:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'TWO_EVALUATOR_JUDGMENTS_REQUIRED'
            continue
        if len({e['model_family'] for e in evals}) != 2:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'EVALUATOR_MODEL_FAMILIES_NOT_INDEPENDENT'
            continue
        if len({e['session_id'] for e in evals}) != 2:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'EVALUATOR_SESSIONS_NOT_INDEPENDENT'
            continue
        expected = expected_by_pid.get(pid, SILENT)
        if reference['verdict'] == UNDECIDABLE:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'SIGNER_REFERENCE_UNDECIDABLE'
            finding['reference'] = reference
            finding['evaluators'] = evals
            continue
        if reference['verdict'] != expected:
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'SIGNER_REFERENCE_MISMATCH'
            finding['calibration_failure'] = True
            finding['reference'] = reference
            finding['evaluators'] = evals
            continue
        if any(e['verdict'] == UNDECIDABLE for e in evals):
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'EVALUATOR_UNDECIDABLE'
            finding['reference'] = reference
            finding['evaluators'] = evals
            continue
        if any(e['verdict'] != reference['verdict'] for e in evals):
            finding['status'] = UNDECIDABLE
            finding['detail'] = 'EVALUATOR_MISMATCH'
            finding['calibration_failure'] = True
            finding['reference'] = reference
            finding['evaluators'] = evals
            continue
        finding['status'] = reference['verdict']
        finding['detail'] = 'signer reference + 2/2 evaluator match: %s' % reference['verdict']
        finding['reference'] = reference
        finding['evaluators'] = evals
    return result


def prepare_artifact(target, context, oracle, rules, packet_dir=None):
    """Score one target and attach blinded packets; no answer-key comparison."""
    result = score(target, context, oracle, rules)
    # The packet builder needs the target, but this field is removed before evidence.
    result['target_for_packet'] = target
    packets = attach_packets(result, context, oracle, packet_dir=packet_dir)
    result.pop('target_for_packet', None)
    result['packets'] = packets
    return result


def evaluate_artifact(target, context, oracle, rules, references=None,
                      evaluators=None, expected_by_pid=None, packet_dir=None):
    """Run the scorer, attach packets, and aggregate Option-F evidence."""
    result = prepare_artifact(target, context, oracle, rules, packet_dir=packet_dir)
    aggregate_semantic(result, result['packets'], references or [], evaluators or [],
                       expected_by_pid or {})
    return result


def clean_verdict(findings):
    if any(f.get('calibration_failure') for f in findings):
        return 'FAIL'
    statuses = [f['status'] for f in findings]
    if FIRED in statuses:
        return 'FAIL'
    if UNDECIDABLE in statuses:
        return 'INCOMPLETE'
    return 'PASS'


def aggregate_parent_type(records):
    statuses = [r['verdict'] for r in records]
    if 'FAIL' in statuses:
        return 'FAIL'
    if 'INCOMPLETE' in statuses or not statuses:
        return 'INCOMPLETE'
    return 'PASS'


def aggregate_campaign(parent_type_verdicts, required_types):
    statuses = [parent_type_verdicts.get(t, 'INCOMPLETE') for t in required_types]
    if 'FAIL' in statuses:
        return 'FAIL'
    if 'INCOMPLETE' in statuses:
        return 'INCOMPLETE'
    return 'PASS'


def specificity(target_type, findings, expected):
    status = {f['predicate_id']: f['status'] for f in findings}
    active = registry.predicates_for(target_type)
    other = [pid for pid in active if pid != expected]
    missed = [pid for pid in other if status.get(pid) != SILENT]
    return {
        'expected': expected,
        'expected_status': status.get(expected),
        'other_active': other,
        'non_silent_other': missed,
        'pass': status.get(expected) == FIRED and not missed,
    }


def verdict_for(target_type, findings, expected):
    spec = specificity(target_type, findings, expected)
    if any(f.get('calibration_failure') for f in findings):
        return 'FAIL', spec
    statuses = {f['predicate_id']: f['status'] for f in findings}
    if any(s == UNDECIDABLE for s in statuses.values()):
        return 'INCOMPLETE', spec
    return ('PASS' if spec['pass'] else 'FAIL'), spec


def _artifact_rows(manifest, clean):
    rows = []
    for parent_id, rec in manifest['clean_parents'].items():
        rows.append({
            'kind': 'clean',
            'artifact': clean[parent_id],
            'artifact_name': rec['artifact'],
            'parent_type': rec['parent_type'],
            'parent_id': parent_id,
            'expected': None,
        })
    for seed in manifest['seeds']:
        artifact = load_json(os.path.join(GEN, seed['artifact']))
        if canon(artifact) != seed['hash']:
            raise InputIntegrityError('seed %s hash mismatch' % seed['artifact'])
        rows.append({
            'kind': 'seed',
            'artifact': artifact,
            'artifact_name': seed['artifact'],
            'parent_type': seed['parent_type'],
            'parent_id': seed['parent_id'],
            'expected': seed['must_fire'],
        })
    return rows


def filter_baseline_evidence(baseline, current, global_packets):
    """Drop baseline evidence whose packet or evaluator identity is stale."""
    current_eval_keys = {(r['packet_id'], r['judge_id'])
                         for r in current['evaluators']}
    return {
        'policy_version': REVIEW_POLICY,
        'references': [
            r for r in baseline['references']
            if r['packet_id'] in global_packets
        ],
        'evaluators': [
            r for r in baseline['evaluators']
            if r['packet_id'] in global_packets
            and (r['packet_id'], r['judge_id']) not in current_eval_keys
        ],
    }


def run(mode, out_dir, evidence_path=None, baseline_path=None, limit=None):
    if mode not in ('packets', 'acceptance'):
        raise ValueError('unsupported mode %s' % mode)
    manifest, clean, oracle, rules = load_campaign()
    current = load_review_evidence(evidence_path)
    baseline = load_review_evidence(baseline_path)
    rows = _artifact_rows(manifest, clean)
    if limit:
        rows = rows[:limit]
    packets_dir = os.path.join(out_dir, 'packets')

    prepared = []
    for row in rows:
        context, pinned = dependency_context(manifest, clean, row['parent_type'])
        result = prepare_artifact(row['artifact'], context, oracle, rules,
                                  packet_dir=packets_dir)
        prepared.append({'row': row, 'result': result, 'pinned': pinned})

    global_packets = {}
    for item in prepared:
        for packet in item['result']['packets'].values():
            global_packets[packet['packet_id']] = packet

    # Current evidence must bind to known packets. Baseline evidence for old
    # packet versions is discarded rather than becoming a hidden mutation.
    validate_review_evidence(global_packets, current['references'],
                             current['evaluators'])
    baseline = filter_baseline_evidence(baseline, current, global_packets)
    merged = merge_review_evidence(baseline, current)
    validate_review_evidence(global_packets, merged['references'],
                             merged['evaluators'])

    records = []
    for item in prepared:
        row = item['row']
        result = item['result']
        semantic_pids = [p for p in registry.predicates_for(row['parent_type'])
                         if p in registry.SEMANTIC_PREDICATES]
        if row['kind'] == 'clean':
            expected_by_pid = {p: SILENT for p in semantic_pids}
        else:
            expected_by_pid = {
                p: (FIRED if p == row['expected'] else SILENT)
                for p in semantic_pids
            }
        local_ids = {p['packet_id'] for p in result['packets'].values()}
        local_refs = [r for r in merged['references'] if r['packet_id'] in local_ids]
        local_evals = [r for r in merged['evaluators'] if r['packet_id'] in local_ids]
        aggregate_semantic(result, result['packets'], local_refs, local_evals,
                           expected_by_pid)
        if row['kind'] == 'clean':
            verdict = clean_verdict(result['findings'])
            spec = None
        else:
            verdict, spec = verdict_for(row['parent_type'], result['findings'],
                                        row['expected'])
        record = {
            'kind': row['kind'],
            'artifact_name': row.get('artifact_name'),
            'parent_id': row['parent_id'],
            'parent_type': row['parent_type'],
            'artifact_hash': canon(row['artifact']),
            'dependency_context': item['pinned'],
            'scorer_version': result['scorer_version'],
            'findings': result['findings'],
            'packets': sorted(result['packets']),
            'verdict': verdict,
            'specificity': spec,
        }
        records.append(record)
        write_json(os.path.join(out_dir, 'records',
                                row['parent_id'] + '-' + str(len(records)) + '.json'),
                   record)

    required_types = manifest.get('parent_model', {}).get('parent_types')
    if not required_types:
        required_types = sorted({r['parent_type'] for r in records})
    parent_type_verdicts = {}
    for parent_type in required_types:
        parent_records = [r for r in records if r['parent_type'] == parent_type]
        parent_type_verdicts[parent_type] = aggregate_parent_type(parent_records)
    campaign_verdict = aggregate_campaign(parent_type_verdicts, required_types)
    if limit:
        campaign_verdict = 'INCOMPLETE'

    implementation_hashes = {
        'projection_contract.py': file_sha(os.path.join(ROOT, 'projection_contract.py')),
        'scorer/scorer.py': file_sha(os.path.join(ROOT, 'scorer/scorer.py')),
        'scorer/registry.py': file_sha(os.path.join(ROOT, 'scorer/registry.py')),
        'scorer/projection.py': file_sha(os.path.join(ROOT, 'scorer/projection.py')),
        'tools/gate0_harness.py': file_sha(os.path.join(ROOT, 'tools/gate0_harness.py')),
    }
    evidence = {
        'mode': mode,
        'run_id': datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' +
                  canon(records)[-8:],
        'campaign': manifest['campaign'],
        'review_policy': REVIEW_POLICY,
        'identities': {
            'registry': manifest['registry'],
            'active_set': manifest['active_set'],
            'schema': manifest['schema'],
            'oracle': manifest['oracle'],
            'specificity_policy': manifest['specificity_policy'],
        },
        'scorer_version': registry.SCORER_VERSION,
        'implementation_hashes': implementation_hashes,
        'governing_hashes': manifest['governing_hashes'],
        'references': merged['references'],
        'evaluators': merged['evaluators'],
        'reference_count': len(merged['references']),
        'evaluator_count': len(merged['evaluators']),
        'parent_type_verdicts': parent_type_verdicts,
        'campaign_verdict': campaign_verdict,
        'records': records,
    }
    write_json(os.path.join(out_dir, 'EVIDENCE.json'), evidence)
    return evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description='Gate 0 harness')
    parser.add_argument('--mode', choices=['packets', 'acceptance'], required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--evidence', '--judgments', dest='evidence')
    parser.add_argument('--baseline')
    parser.add_argument('--limit', type=int)
    args = parser.parse_args(argv)
    evidence = run(args.mode, args.out, args.evidence, args.baseline, args.limit)
    print('mode:', evidence['mode'])
    print('run_id:', evidence['run_id'])
    print('records:', len(evidence['records']))
    for rec in evidence['records']:
        print(rec['kind'], rec['parent_id'], rec['verdict'])


if __name__ == '__main__':
    main()
