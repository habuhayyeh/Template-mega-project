#!/usr/bin/env python3
"""Build the DC-002 execution package from source artifacts.

Source (hand-authored, authoritative):
  AX-S1S2-D/parents/S1_PARENT.json
  AX-S1S2-D/parents/S2_PARENT.json
  AX-S1S2-D/parents/S3_PARENT.json
  AX-S1S2-D/parents/S3_PARENT_NOT_RENDERED.json
  AX-S1S2-D/parents/S4_PARENT.json
  AX-S1S2-D/fixtures/CASE-01/oracle.json
  AX-S1S2-D/schema.md (PROJECTION_MAP and REASON_REGISTRY blocks)
  AX-S1S2-D/predicates.md (active predicate set)
  gate0/seeds/G0-SEEDS.md
  projection_contract.py (shared executable map, also used by the scorer)
  this file's SEEDS table

Generated (never hand-edited):
  gate0/seeds/generated/PARENT-*.json, G0-*.json, VARIATION.json, MANIFEST.json

Run: python architecture-reboot/tools/make_seeds.py
Idempotent: a second run must produce no diff.
"""
import copy
import hashlib
import io
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AX = os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D')
G0 = os.path.join(ROOT, 'experiments/gate0')
GEN = os.path.join(G0, 'seeds/generated')
PAR = os.path.join(AX, 'parents')
SCHEMA_PATH = os.path.join(AX, 'schema.md')
PREDICATES_PATH = os.path.join(AX, 'predicates.md')

REG, ACTIVE, SCHEMA, ORACLE_VER = 'PILOT-3', 'ACTIVE-PILOT-3', 'SCHEMA-4', 'ORACLE-4.0'
CAMPAIGN = 'GATE0-C3'

PARENT_FILES = [
    'S1_PARENT.json',
    'S2_PARENT.json',
    'S2_CASE10_CAUSAL.json',
    'S3_PARENT.json',
    'S3_PARENT_NOT_RENDERED.json',
    'S4_PARENT.json',
]
PARENT_TYPES = {'S1_OUTPUT', 'S2_OUTPUT', 'S3_OUTPUT', 'S4_BLUEPRINT'}
PENDING_PREDICATES = ['S2-ADOPT-02', 'S4-ORD-01']

sys.path.insert(0, ROOT)
from projection_contract import ProjectionError, build_view


def fail(msg):
    raise SystemExit('BUILD FAILURE: ' + msg)


def canon(o):
    return 'sha256:' + hashlib.sha256(
        json.dumps(o, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


ABSENT = object()


def diff_json(a, b, path=''):
    """Return the structural differences between two JSON values.

    A changed list of the same length is diffed element-wise, so the path is
    exact. A length change is one operation on the list itself: the declared
    before/after values are then the whole lists.
    """
    if type(a) is not type(b):
        return [(path, a, b)]
    if isinstance(a, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            p = path + '/' + key
            if key not in a:
                out.append((p, ABSENT, b[key]))
            elif key not in b:
                out.append((p, a[key], ABSENT))
            else:
                out.extend(diff_json(a[key], b[key], p))
        return out
    if isinstance(a, list):
        if a == b:
            return []
        if len(a) == len(b):
            out = []
            for i, (x, y) in enumerate(zip(a, b)):
                out.extend(diff_json(x, y, path + '/' + str(i)))
            return out
        return [(path, a, b)]
    return [] if a == b else [(path, a, b)]


def fmt_value(v):
    if v is ABSENT:
        return '<absent>'
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def checked_mutation(parent, seed, sid, expected_path, before_label, after_label):
    """Fail unless the seed differs from its parent at exactly one declared path."""
    if canon(seed) == canon(parent):
        fail('seed %s is a no-op copy of its parent' % sid)
    ops = diff_json(parent, seed)
    if len(ops) != 1:
        fail('seed %s has %d diffs, expected exactly one: %r'
             % (sid, len(ops), [o[0] for o in ops]))
    path, before, after = ops[0]
    if path != expected_path:
        fail('seed %s changed %s, declared %s' % (sid, path, expected_path))
    return {
        'path': path,
        'before': fmt_value(before),
        'after': fmt_value(after),
        'label': '%s -> %s' % (before_label, after_label),
    }



def fsha(p):
    return 'sha256:' + hashlib.sha256(io.open(p, 'rb').read()).hexdigest()


def load_json(path):
    with io.open(path, encoding='utf-8') as fh:
        return json.load(fh)


def load_parent(name):
    p = load_json(os.path.join(PAR, name))
    if not isinstance(p.get('parent_id'), str) or not p['parent_id']:
        fail('%s has no non-empty parent_id' % name)
    if p.get('parent_type') not in PARENT_TYPES:
        fail('%s has invalid parent_type %r' % (name, p.get('parent_type')))
    return p


def read_block(path, name):
    text = io.open(path, encoding='utf-8').read()
    pat = re.compile(
        r'<!-- BEGIN:' + re.escape(name) + r' -->\s*(.*?)\s*<!-- END:' + re.escape(name) + r' -->',
        re.S)
    m = pat.search(text)
    if not m:
        fail('%s is missing the %s block' % (path, name))
    block = m.group(1).strip()
    if block.startswith('```'):
        lines = block.splitlines()
        if len(lines) < 3 or lines[-1].strip() != '```':
            fail('%s block %s has a malformed fence' % (path, name))
        block = '\n'.join(lines[1:-1])
    try:
        return json.loads(block)
    except ValueError as exc:
        fail('%s block %s is not valid JSON: %s' % (path, name, exc))


def load_active_predicates():
    text = io.open(PREDICATES_PATH, encoding='utf-8').read()
    m = re.search(
        r'## Pilot ACTIVE_PREDICATE_SET.*?```text\s*(.*?)```',
        text, re.S)
    if not m:
        fail('predicates.md has no ACTIVE_PREDICATE_SET fenced block')
    preds = [p.strip() for p in re.split(r'[,\n]', m.group(1)) if p.strip()]
    if len(preds) != len(set(preds)):
        fail('predicates.md ACTIVE_PREDICATE_SET contains duplicates')
    for p in preds:
        if not re.match(r'^S[1-4]-[A-Z]+-\d\d$', p):
            fail('predicates.md has malformed predicate id %r' % p)
    return preds


def reason_by_code(reason_reg):
    out = {}
    for r in reason_reg.get('reasons', []):
        code = r.get('code')
        if not code or code in out:
            fail('reason registry has missing or duplicate code %r' % code)
        out[code] = r
    if not out:
        fail('reason registry is empty')
    return out


def validate_s3_clean(name, parent, s1p, oracle, reason_reg):
    s3 = parent.get('s3')
    if not isinstance(s3, dict):
        fail('%s has no s3 object' % name)
    outcomes = s3.get('candidate_outcomes')
    if not isinstance(outcomes, list):
        fail('%s has no candidate_outcomes list' % name)

    candidate_ids = {c['id'] for c in s1p['s1']['candidates']}
    by_code = reason_by_code(reason_reg)
    seen, rendered_from_outcomes = set(), set()

    for o in outcomes:
        cid = o.get('candidate')
        if cid in seen:
            fail('%s violates outcome exclusivity for %s' % (name, cid))
        seen.add(cid)
        if cid not in candidate_ids:
            fail('%s has outcome for unknown candidate %s' % (name, cid))
        outcome = o.get('outcome')
        if outcome == 'RENDERED':
            if 'reason' in o or 'basis' in o:
                fail('%s carries reason/basis on a RENDERED outcome' % name)
            rendered_from_outcomes.add(cid)
        elif outcome == 'NOT_RENDERED':
            spec = by_code.get(o.get('reason'))
            if not spec:
                fail('%s has NOT_RENDERED outcome with invalid reason %r'
                     % (name, o.get('reason')))
            basis = o.get('basis')
            if spec['requires_basis']:
                if not isinstance(basis, list) or len(basis) < spec['basis_min_items']:
                    fail('%s has NOT_RENDERED outcome with missing basis' % name)
                if spec.get('basis_unique') and len(set(basis)) != len(basis):
                    fail('%s has duplicate basis entries' % name)
                for b in basis:
                    if b not in oracle['objects']:
                        fail('%s basis target %s is absent from oracle.objects'
                             % (name, b))
            else:
                if 'basis' in o and basis is not None:
                    fail('%s has basis on a no-basis reason' % name)
        else:
            fail('%s has invalid outcome %r' % (name, outcome))

    if seen != candidate_ids:
        fail('%s candidate coverage is %s, expected %s'
             % (name, sorted(seen), sorted(candidate_ids)))

    rendered_set = {r['problem'] for r in s3.get('rendered', [])}
    if rendered_from_outcomes != rendered_set:
        fail('%s RENDERED outcomes %s do not equal rendered[] %s'
             % (name, sorted(rendered_from_outcomes), sorted(rendered_set)))
    for entry in s3.get('rendered', []):
        if entry.get('encounter_role') not in ('PRIMARY', 'BACKGROUND'):
            fail('%s rendered problem %s has invalid encounter_role %r'
                 % (name, entry.get('problem'), entry.get('encounter_role')))

    objects = set(oracle['objects'])
    retained = s3.get('retained', [])
    if len(set(retained)) != len(retained):
        fail('%s retained has duplicates' % name)
    if set(retained) - objects:
        fail('%s retained has unknown objects' % name)
    dispositions = [d['object'] for d in s3.get('dispositions', [])]
    if len(set(dispositions)) != len(dispositions):
        fail('%s dispositions has duplicates' % name)
    if set(dispositions) - objects:
        fail('%s dispositions has unknown objects' % name)
    if set(retained) & set(dispositions):
        fail('%s retains and dispositions the same object' % name)
    if set(retained) | set(dispositions) != objects:
        fail('%s retained union dispositions does not cover oracle.objects' % name)
    if set(s3.get('use', {})) - set(retained):
        fail('%s use map references non-retained objects' % name)


def s1_01(a): a['s1']['candidates'][0]['adopted'] = True
def s1_02(a): a['s1']['candidates'][0]['selected_claim'] = 'CC1'
def s1_04(a): a['s1']['candidates'][0]['anchors'] = []
def s1_05(a):
    a['s1']['candidates'].append({
        'id': 'C3', 'subject': 'aspirin 81 daily', 'anchors': ['S04'],
        'salience': {'acuity': 'LOW', 'management_reference_spans': []},
        'claim_candidates': [{'id': 'CC3', 'text': 'aspirin 81 daily', 'support': ['S04']}]})
def s1_06(a): a['s1']['candidates'][0]['status_current'] = True

def s2_01(a): a['s2']['representations'][0]['support_refs'] = []
def s2_02(a): a['s2']['representations'][0]['members'].append('O07')
def s2_03(a): a['s2']['adjudication'][0]['temporal'] = 'now'
def s2_06(a): a['s2']['adjudication'][0]['adoption'] = None
def s2_07(a):
    a['s2']['causal_relations'] = [{
        'from': 'O01', 'to': 'O03', 'relation': 'CONTRIBUTOR',
        'strength': 'POSSIBLE', 'support': ['S01']}]
def s2_08(a):
    a['s2']['causal_relations'] = [{
        'from': 'O02', 'to': 'O03', 'relation': 'CONTRIBUTOR',
        'strength': 'CERTAIN', 'support': ['S01', 'S02']}]
def s2_09(a):
    a['s2']['causal_relations'][0]['from'] = 'O01'
def s2_10(a):
    a['s2']['causal_relations'][0]['strength'] = 'LIKELY'

def s3_01(a): a['s3']['rendered'][0]['approved_representation'] = None
def s3_02(a): a['s3']['rendered'][0]['selected_rep'] = 'R-999'
def s3_04(a):
    a['s3']['dispositions'] = [d for d in a['s3']['dispositions'] if d['object'] != 'O07']
def s3_05(a): a['s3']['candidate_outcomes'] = []
def s3_06(a):
    a['s3']['candidate_outcomes'].append({
        'candidate': 'C1', 'outcome': 'NOT_RENDERED',
        'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O03']})
def s3_07(a):
    a['s3']['candidate_outcomes'].append({
        'candidate': 'C9', 'outcome': 'NOT_RENDERED',
        'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O03']})
def s3_08(a):
    a['s3']['rendered'].append({
        'problem': 'C1', 'approved_representation': 'R1', 'selected_rep': 'R1',
        'encounter_role': 'PRIMARY'})
def s3_09(a):
    a['s3']['candidate_outcomes'][0]['reason'] = None
def s3_10(a):
    a['s3']['candidate_outcomes'][0]['basis'] = []
def s3_11(a): a['s3']['rendered'][1]['encounter_role'] = 'PRIMARY'
def s3_12(a): a['s3']['rendered'][0]['encounter_role'] = 'UNKNOWN'

def s4_01(a): a['s4']['problems'] = []
def s4_02(a): a['s4']['problems'].append({'id': 'P3', 'source': 'C9', 'order': 3})
def s4_04(a): a['s4']['units'][0]['members'].append('O99')
def s4_05(a): a['s4']['units'][0]['representation'] = 'R-999'
def s4_06(a): a['s4']['units'] = [u for u in a['s4']['units'] if u['id'] != 'U2']
def s4_07(a): a['s4_input_view']['adoption'] = True
def s4_08(a): a['s4_input_view']['from_s2']['selections'][0]['members'] = ['O03', 'O04', 'O05']
def s4_09(a): a['s4_input_view']['from_s2']['selected_rep'] = 'R-999'
def s4_10(a):
    a['s4_input_view']['from_ingest']['O05']['payload'] = 'vitamin D'
def s4_11(a): a['s4_input_view']['from_s2']['selections'][0]['duplicate_groups'] = [['O03', 'O04']]
def s4_12(a): a['s4_input_view']['from_s3']['selected_roles']['C9'] = 'BACKGROUND'
def s4_13(a):
    a['s4_input_view']['from_s2']['causal_relations'] = [{
        'from': 'O02', 'to': 'O03', 'relation': 'CONTRIBUTOR',
        'strength': 'POSSIBLE', 'support': ['S01', 'S02']}]
def s4_14(a): a['s4']['problems'][1]['encounter_role'] = 'PRIMARY'


SEEDS = [
 ('S1_PARENT.json', 'G0-S1-01', 'S1-AUTH-01', s1_01, '/s1/candidates/0/adopted', '<absent>', 'true'),
 ('S1_PARENT.json', 'G0-S1-02', 'S1-AUTH-02', s1_02, '/s1/candidates/0/selected_claim', '<absent>', 'CC1'),
 ('S1_PARENT.json', 'G0-S1-04', 'S1-CAND-02', s1_04, '/s1/candidates/0/anchors', '["S02"]', '[]'),
 ('S1_PARENT.json', 'G0-S1-05', 'S1-CAND-01', s1_05, '/s1/candidates', '<absent>', 'C3 medication-only'),
 ('S1_PARENT.json', 'G0-S1-06', 'S1-AUTH-01', s1_06, '/s1/candidates/0/status_current', '<absent>', 'true'),
 ('S2_PARENT.json', 'G0-S2-02', 'S2-REP-01', s2_02, '/s2/representations/0/members', '["O03","O04"]', 'adds O07 medication'),
 ('S2_PARENT.json', 'G0-S2-03', 'S2-TEMP-01', s2_03, '/s2/adjudication/0/temporal', '2024-02 documented', 'now'),
 ('S2_PARENT.json', 'G0-S2-06', 'S2-ADOPT-01', s2_06, '/s2/adjudication/0/adoption', 'false', 'null'),
 ('S2_PARENT.json', 'G0-S2-07', 'S2-CAUSAL-01', s2_07, '/s2/causal_relations', '[]', 'history-only causal relation'),
 ('S2_PARENT.json', 'G0-S2-08', 'S2-CAUSAL-02', s2_08, '/s2/causal_relations', '[]', 'invalid strength'),
 ('S2_CASE10_CAUSAL.json', 'G0-S2-09', 'S2-CAUSAL-01', s2_09, '/s2/causal_relations/0/from', 'O02', 'O01 historical stroke subject'),
 ('S2_CASE10_CAUSAL.json', 'G0-S2-10', 'S2-CAUSAL-01', s2_10, '/s2/causal_relations/0/strength', 'POSSIBLE', 'LIKELY'),
 ('S3_PARENT.json', 'G0-S3-01', 'S3-INC-01', s3_01, '/s3/rendered/0/approved_representation', 'R1', 'null'),
 ('S3_PARENT.json', 'G0-S3-02', 'S3-SEL-01', s3_02, '/s3/rendered/0/selected_rep', 'R1', 'R-999'),
 ('S3_PARENT.json', 'G0-S3-04', 'S3-ACCT-01', s3_04, '/s3/dispositions', 'O07 recorded', 'O07 unaccounted'),
 ('S3_PARENT.json', 'G0-S3-05', 'S3-CAND-01', s3_05, '/s3/candidate_outcomes', 'C1 RENDERED', '[] coverage'),
 ('S3_PARENT.json', 'G0-S3-06', 'S3-CAND-01', s3_06, '/s3/candidate_outcomes', 'one outcome', 'two exclusivity'),
 ('S3_PARENT.json', 'G0-S3-07', 'S3-CAND-01', s3_07, '/s3/candidate_outcomes', '<absent>', 'unknown id C9'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-08', 'S3-CAND-01', s3_08, '/s3/rendered', '[]', 'C1 rendered while outcome is NOT_RENDERED'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-09', 'S3-CAND-01', s3_09, '/s3/candidate_outcomes/0/reason', 'NO_APPROVED_REPRESENTATION', 'null'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-10', 'S3-CAND-01', s3_10, '/s3/candidate_outcomes/0/basis', '["O03","O04"]', '[]'),
 ('S3_PARENT.json', 'G0-S3-11', 'S3-ROLE-01', s3_11, '/s3/rendered/1/encounter_role', 'BACKGROUND', 'PRIMARY'),
 ('S3_PARENT.json', 'G0-S3-12', 'S3-ROLE-02', s3_12, '/s3/rendered/0/encounter_role', 'PRIMARY', 'UNKNOWN'),
 ('S4_PARENT.json', 'G0-S4-01', 'S4-INC-01', s4_01, '/s4/problems', '2 problems', '0 problems'),
 ('S4_PARENT.json', 'G0-S4-02', 'S4-INC-01', s4_02, '/s4/problems', '<absent>', 'P3 not rendered'),
 ('S4_PARENT.json', 'G0-S4-04', 'S4-MEM-01', s4_04, '/s4/units/0/members', '<absent>', 'O99'),
 ('S4_PARENT.json', 'G0-S4-05', 'S4-REP-01', s4_05, '/s4/units/0/representation', 'R1', 'R-999'),
 ('S4_PARENT.json', 'G0-S4-06', 'S4-COMP-01', s4_06, '/s4/units', 'U2 present', 'U2 removed'),
 ('S4_PARENT.json', 'G0-S4-07', 'S4-PROJ-01', s4_07, '/s4_input_view/adoption', '<absent>', 'adoption schema'),
 ('S4_PARENT.json', 'G0-S4-08', 'S4-PROJ-01', s4_08, '/s4_input_view/from_s2/selections/0/members', '["O03","O04"]', 'adds O05 invented'),
 ('S4_PARENT.json', 'G0-S4-09', 'S4-PROJ-01', s4_09, '/s4_input_view/from_s2/selected_rep', '<absent>', 'S3-owned field under S2 wrong-owner group'),
 ('S4_PARENT.json', 'G0-S4-10', 'S4-PROJ-01', s4_10, '/s4_input_view/from_ingest/O05/payload', 'S03 payload', 'fabricated payload'),
 ('S4_PARENT.json', 'G0-S4-11', 'S4-PROJ-01', s4_11, '/s4_input_view/from_s2/selections/0/duplicate_groups', '[]', '[[O03,O04]] authored'),
 ('S4_PARENT.json', 'G0-S4-12', 'S4-PROJ-01', s4_12, '/s4_input_view/from_s3/selected_roles/C9', '<absent>', 'BACKGROUND'),
 ('S4_PARENT.json', 'G0-S4-13', 'S4-PROJ-01', s4_13, '/s4_input_view/from_s2/causal_relations', '[]', 'causal relation authored'),
 ('S4_PARENT.json', 'G0-S4-14', 'S4-ROLE-01', s4_14, '/s4/problems/1/encounter_role', 'BACKGROUND', 'PRIMARY'),
]


def write_json(path, obj):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(obj, fh, indent=2, sort_keys=True)
        fh.write('\n')


def main():
    pmap = read_block(SCHEMA_PATH, 'PROJECTION_MAP')
    reason_reg = read_block(SCHEMA_PATH, 'REASON_REGISTRY')
    active = load_active_predicates()

    if pmap.get('schema') != SCHEMA or pmap.get('view') != 'S4_INPUT_VIEW':
        fail('projection map identity does not match SCHEMA-4/S4_INPUT_VIEW')

    parents = {f: load_parent(f) for f in PARENT_FILES}
    parent_ids = [p['parent_id'] for p in parents.values()]
    if len(parent_ids) != len(set(parent_ids)):
        fail('parent_id values are not unique: %s' % parent_ids)
    if 's4_input_view' in parents['S4_PARENT.json']:
        fail('S4_PARENT.json must not hand-author s4_input_view')

    s1p = parents['S1_PARENT.json']
    s2p = parents['S2_PARENT.json']
    s3p = parents['S3_PARENT.json']
    s4p = parents['S4_PARENT.json']
    oracle = load_json(os.path.join(AX, 'fixtures/CASE-01/oracle.json'))

    try:
        built_view = build_view(s1p, s2p, s3p, oracle, pmap)
    except ProjectionError as exc:
        fail(str(exc))
    clean_s4 = {
        'case': s4p['case'],
        'parent_id': s4p['parent_id'],
        'parent_type': 'S4_BLUEPRINT',
        'registry': REG,
        'schema': SCHEMA,
        's4_input_view': built_view,
        's4': copy.deepcopy(s4p['s4']),
    }

    contracts = pmap['contracts']
    if set(clean_s4['s4'].get('sections', [])) - set(contracts['sections']):
        fail('S4 section is outside the frozen contract')
    for u in clean_s4['s4'].get('units', []):
        if u.get('operator') not in contracts['operators']:
            fail('S4 unit %s uses operator %r outside the contract'
                 % (u.get('id'), u.get('operator')))

    clean = {f: copy.deepcopy(parents[f]) for f in PARENT_FILES}
    clean['S4_PARENT.json'] = clean_s4

    validate_s3_clean('S3_PARENT.json', clean['S3_PARENT.json'], s1p, oracle, reason_reg)
    validate_s3_clean('S3_PARENT_NOT_RENDERED.json',
                      clean['S3_PARENT_NOT_RENDERED.json'], s1p, oracle, reason_reg)

    os.makedirs(GEN, exist_ok=True)
    for f in os.listdir(GEN):
        if f.endswith('.json'):
            os.remove(os.path.join(GEN, f))

    for f in PARENT_FILES:
        write_json(os.path.join(GEN, 'PARENT-' + f), clean[f])

    manifest = {
        'campaign': CAMPAIGN,
        'registry': REG,
        'active_set': ACTIVE,
        'schema': SCHEMA,
        'oracle': ORACLE_VER,
        'specificity_policy': 'FULL_SILENCE-WITHIN-LAYER',
        'hash_methods': {
            'governing_source': 'sha256 over file bytes',
            'artifacts': 'sha256 over canonical JSON (sorted keys, compact separators)',
        },
        'parent_model': {
            'parent_types': sorted({p['parent_type'] for p in clean.values()}),
            'clean_parents': len(PARENT_FILES),
            's3_parent_ids': sorted(
                p['parent_id'] for p in clean.values() if p['parent_type'] == 'S3_OUTPUT'),
        },
        'governing_hashes': {
            'CONSENSUS_SUBMODULE_INTERFACES_v1.md': fsha(
                os.path.join(ROOT, 'CONSENSUS_SUBMODULE_INTERFACES_v1.md')),
            'CONSENSUS_ARCHITECTURE_v0.1.md': fsha(
                os.path.join(ROOT, 'CONSENSUS_ARCHITECTURE_v0.1.md')),
            '00-ARCHITECTURE-EXPERIMENT-PROGRAM.md': fsha(
                os.path.join(ROOT, 'experiments/architecture/00-ARCHITECTURE-EXPERIMENT-PROGRAM.md')),
            'AX-S1S2-D.md': fsha(os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D.md')),
            'schema.md': fsha(SCHEMA_PATH),
            'predicates.md': fsha(PREDICATES_PATH),
            'G0-SEEDS.md': fsha(os.path.join(G0, 'seeds/G0-SEEDS.md')),
            'make_seeds.py': fsha(os.path.abspath(__file__)),
            '00-GATE0-MANIFEST.md': fsha(os.path.join(G0, '00-GATE0-MANIFEST.md')),
            'oracle.json': fsha(os.path.join(AX, 'fixtures/CASE-01/oracle.json')),
        },
        'projection': {
            'name': 'S4_INPUT_VIEW',
            'map_block': 'PROJECTION_MAP',
            'map_source': 'experiments/architecture/AX-S1S2-D/schema.md',
            'map_sha256': canon(pmap),
            'view_sha256': canon(built_view),
            'problems': [p['problem'] for p in built_view['from_s1']['problems']],
            'selected_reps': built_view['from_s3']['selected_reps'],
            'selected_roles': built_view['from_s3']['selected_roles'],
            'retained': built_view['from_s3']['retained'],
            'rule_count': len(pmap['rules']),
        },
        'reason_registry': {
            'name': reason_reg['registry'],
            'hash': canon(reason_reg),
            'codes': [r['code'] for r in reason_reg['reasons']],
        },
        'clean_parents': {},
        'seeds': [],
    }

    for f in PARENT_FILES:
        p = clean[f]
        manifest['clean_parents'][p['parent_id']] = {
            'file': f,
            'artifact': 'PARENT-' + f,
            'parent_id': p['parent_id'],
            'parent_type': p['parent_type'],
            'hash': canon(p),
        }

    dependency_files = {
        'S1_OUTPUT': [],
        'S2_OUTPUT': ['S1_PARENT.json'],
        'S3_OUTPUT': ['S1_PARENT.json', 'S2_PARENT.json'],
        'S4_BLUEPRINT': ['S1_PARENT.json', 'S2_PARENT.json', 'S3_PARENT.json'],
    }
    manifest['dependency_context'] = {}
    manifest['dependency_context_by_parent'] = {'S2_CASE10_CAUSAL': []}
    for target, files in dependency_files.items():
        manifest['dependency_context'][target] = [
            {
                'parent_id': clean[f]['parent_id'],
                'parent_type': clean[f]['parent_type'],
                'artifact': 'PARENT-' + f,
                'hash': canon(clean[f]),
            }
            for f in files
        ]

    by_predicate = Counter()
    checked = 0
    for pfile, sid, pred, fn, path, before, after in SEEDS:
        if pred not in active:
            fail('seed %s targets inactive predicate %s' % (sid, pred))
        art = copy.deepcopy(clean[pfile])
        fn(art)
        mutation = checked_mutation(clean[pfile], art, sid, path, before, after)
        checked += 1
        name = sid + '.json'
        write_json(os.path.join(GEN, name), art)
        manifest['seeds'].append({
            'artifact': name,
            'parent': 'PARENT-' + pfile,
            'parent_id': clean[pfile]['parent_id'],
            'parent_type': clean[pfile]['parent_type'],
            'must_fire': pred,
            'mutations': [mutation],
            'hash': canon(art),
        })
        by_predicate[pred] += 1

    var = copy.deepcopy(clean['S3_PARENT.json'])
    text = json.dumps(var, sort_keys=True)
    for a, b in (('"C1"', '"CX"'), ('"C2"', '"CY"'), ('"R1"', '"RX"'),
                 ('"R2"', '"RY"'), ('"O01"', '"OX1"'), ('"O02"', '"OX2"'),
                 ('"O03"', '"OX3"'), ('"O04"', '"OX4"'), ('"O05"', '"OX5"'),
                 ('"O06"', '"OX6"')):
        text = text.replace(a, b)
    var = json.loads(text)
    var['parent_id'] = 'S3_CASE01_RENDERED_VARIATION'
    write_json(os.path.join(GEN, 'VARIATION.json'), var)
    manifest['variation'] = {
        'artifact': 'VARIATION.json',
        'parent': 'PARENT-S3_PARENT.json',
        'parent_id': var['parent_id'],
        'expect': 'zero findings',
        'basis': 'identical semantics, all content ids renamed',
        'hash': canon(var),
    }

    missing = set(active) - set(by_predicate)
    extra = set(by_predicate) - set(active)
    if missing or extra:
        fail('seed coverage does not match active set; missing=%s extra=%s'
             % (sorted(missing), sorted(extra)))

    manifest['seed_integrity'] = {
        'checked': checked,
        'noop': 0,
        'multi_diff': 0,
        'rule': 'each seed differs from its parent at exactly the declared path; manifest values are the checked diff',
    }

    manifest['counts'] = {
        'clean_parents': len(manifest['clean_parents']),
        'parent_types': len(manifest['parent_model']['parent_types']),
        'seeds': len(manifest['seeds']),
        'active_predicates': len(active),
        'by_predicate': dict(sorted(by_predicate.items())),
        'pending_predicates': list(PENDING_PREDICATES),
        'seed_mutations_checked': checked,
    }

    write_json(os.path.join(GEN, 'MANIFEST.json'), manifest)
    print('built: %d clean parents across %d parent types, %d seeds, %d active predicates'
          % (manifest['counts']['clean_parents'], manifest['counts']['parent_types'],
             manifest['counts']['seeds'], manifest['counts']['active_predicates']))
    for pred, n in sorted(by_predicate.items()):
        print('  %-14s %d' % (pred, n))


if __name__ == '__main__':
    main()
