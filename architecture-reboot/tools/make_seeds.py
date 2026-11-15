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

REG, ACTIVE, SCHEMA, ORACLE_VER = 'PILOT-2', 'ACTIVE-PILOT-2', 'SCHEMA-2', 'ORACLE-2.0'
CAMPAIGN = 'GATE0-C1'

PARENT_FILES = [
    'S1_PARENT.json',
    'S2_PARENT.json',
    'S3_PARENT.json',
    'S3_PARENT_NOT_RENDERED.json',
    'S4_PARENT.json',
]
PARENT_TYPES = {'S1_OUTPUT', 'S2_OUTPUT', 'S3_OUTPUT', 'S4_BLUEPRINT'}
PENDING_PREDICATES = ['S2-ADOPT-02', 'S4-ORD-01']


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


def set_path(root, dst, value):
    parts = [p for p in dst.strip('/').split('/') if p]
    if not parts:
        fail('empty destination path')
    cur = root
    for p in parts[:-1]:
        nxt = cur.setdefault(p, {})
        if not isinstance(nxt, dict):
            fail('destination path collision at %s' % dst)
        cur = nxt
    if parts[-1] in cur:
        fail('duplicate destination %s' % dst)
    cur[parts[-1]] = value


OPS = {
    's1_problem': lambda c: c['cand']['id'],
    's1_salience': lambda c: copy.deepcopy(c['cand']['salience']),
    's3_selected_rep': lambda c: c['rendered'][0]['selected_rep'],
    's3_rendered': lambda c: [r['problem'] for r in c['rendered']],
    's3_retained': lambda c: list(c['retained']),
    's3_use': lambda c: copy.deepcopy(c['use']),
    's3_reuse': lambda c: copy.deepcopy(c['reuse']),
    's2_members': lambda c: list(c['members']),
    's2_relations': lambda c: copy.deepcopy(c['relations']),
    's2_claim_relations': lambda c: copy.deepcopy(c['claim_relations']),
    's2_duplicate_groups': lambda c: copy.deepcopy(c['duplicate_groups']),
    'oracle_ingest': lambda c: copy.deepcopy(c['ingest']),
    'contract_section': lambda c: c['contracts']['section'],
    'contract_operator_set': lambda c: c['contracts']['operator_set'],
}

# Each op has exactly one valid map contract. The build compares every map rule
# against this table; a changed destination, owner, source path, condition,
# requirement or transform fails instead of silently running old code.
OP_CONTRACTS = {
    's1_problem': {
        'dst': '/from_s1/problem',
        'owner': 'S1',
        'source': 'S1_PARENT.json',
        'source_path': '/s1/candidates[id=P]/id',
        'condition': 'P is the unique rendered problem',
        'required': 'required',
        'transform': 'copy id',
    },
    's1_salience': {
        'dst': '/from_s1/salience',
        'owner': 'S1',
        'source': 'S1_PARENT.json',
        'source_path': '/s1/candidates[id=P]/salience',
        'condition': 'same candidate as /from_s1/problem',
        'required': 'required',
        'transform': 'copy object',
    },
    's3_selected_rep': {
        'dst': '/from_s3/selected_rep',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/rendered[problem=P]/selected_rep',
        'condition': 'exactly one rendered entry for P',
        'required': 'required',
        'transform': 'copy id',
    },
    's3_rendered': {
        'dst': '/from_s3/rendered',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/rendered[i]/problem',
        'condition': 'all i, source order',
        'required': 'required',
        'transform': 'collect problem ids',
    },
    's3_retained': {
        'dst': '/from_s3/retained',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/retained[i]',
        'condition': 'all i, source order',
        'required': 'required',
        'transform': 'collect ids',
    },
    's3_use': {
        'dst': '/from_s3/use',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/use/{object}',
        'condition': 'object keys must be a subset of T',
        'required': 'required',
        'transform': 'copy map',
    },
    's3_reuse': {
        'dst': '/from_s3/reuse',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/reuse[i]',
        'condition': 'all i, source order',
        'required': 'required',
        'transform': 'copy list',
    },
    's2_members': {
        'dst': '/from_s2/members',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/representations[id=R]/members[i]',
        'condition': 'R is from_s3.selected_rep; all i, source order',
        'required': 'required',
        'transform': 'copy ids',
    },
    's2_relations': {
        'dst': '/from_s2/relations',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/relations[i]',
        'condition': 'from in M and to in M; source order',
        'required': 'required',
        'transform': 'filter and copy',
    },
    's2_claim_relations': {
        'dst': '/from_s2/claim_relations',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/claim_relations[i]',
        'condition': 'problem == P and representation == R; source order',
        'required': 'required',
        'transform': 'filter and copy',
    },
    's2_duplicate_groups': {
        'dst': '/from_s2/duplicate_groups',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/duplicate_groups[i]',
        'condition': 'set(group) intersects M; source order',
        'required': 'required',
        'transform': 'filter and copy',
    },
    'oracle_ingest': {
        'dst': '/from_ingest',
        'owner': 'I3/I4',
        'source': 'fixtures/CASE-01/oracle.json',
        'source_path': '/objects[{object in T}]/{text,provenance,temporal|status}',
        'condition': 'one entry per T; exactly one of temporal/status',
        'required': 'payload and provenance required; exactly one of temporal/status',
        'transform': 'text→payload; copy provenance; copy temporal or status',
        'expands': {
            '/from_ingest/{object}/payload': '/objects[{object in T}]/text',
            '/from_ingest/{object}/provenance': '/objects[{object in T}]/provenance',
            '/from_ingest/{object}/temporal': '/objects[{object in T}]/temporal when present',
            '/from_ingest/{object}/status': '/objects[{object in T}]/status when temporal is absent',
        },
    },
    'contract_section': {
        'dst': '/from_contracts/section',
        'owner': 'frozen contracts',
        'source': 'SCHEMA-2 contracts block',
        'source_path': '#/contracts/section',
        'condition': 'always',
        'required': 'required',
        'transform': 'copy constant',
    },
    'contract_operator_set': {
        'dst': '/from_contracts/operator_set',
        'owner': 'frozen contracts',
        'source': 'SCHEMA-2 contracts block',
        'source_path': '#/contracts/operator_set',
        'condition': 'always',
        'required': 'required',
        'transform': 'copy constant',
    },
}



def build_view(s1p, s2p, s3p, oracle, pmap):
    """Construct S4_INPUT_VIEW from upstream artifacts using the schema map.

    The map in schema.md is the authority for destinations, source owners and
    source paths. This function supplies one operation per mapped destination;
    it authors no value that is not copied from a named source.
    """
    rendered = s3p['s3']['rendered']
    if len(rendered) != 1:
        fail('S4_INPUT_VIEW scope requires exactly one rendered problem, found %d'
             % len(rendered))

    problem_id = rendered[0]['problem']
    candidates = [c for c in s1p['s1']['candidates'] if c.get('id') == problem_id]
    if len(candidates) != 1:
        fail('expected one S1 candidate for problem %s, found %d'
             % (problem_id, len(candidates)))
    cand = candidates[0]

    selected_rep = rendered[0]['selected_rep']
    reps = [r for r in s2p['s2']['representations'] if r.get('id') == selected_rep]
    if len(reps) != 1:
        fail('expected one S2 representation for selected_rep %s, found %d'
             % (selected_rep, len(reps)))
    rep = reps[0]
    if rep.get('problem') != problem_id:
        fail('selected representation %s belongs to %r, not rendered problem %s'
             % (selected_rep, rep.get('problem'), problem_id))
    members = list(rep['members'])
    if not members:
        fail('selected representation %s has no members' % selected_rep)

    relations = [
        copy.deepcopy(r) for r in s2p['s2'].get('relations', [])
        if r.get('from') in members and r.get('to') in members
    ]

    claim_relations = []
    for r in s2p['s2'].get('claim_relations', []):
        if 'problem' not in r or 'representation' not in r:
            fail('S2 claim_relation lacks problem/representation selectors: %r' % (r,))
        if r['problem'] == problem_id and r['representation'] == selected_rep:
            claim_relations.append(copy.deepcopy(r))

    duplicate_groups = [
        list(g) for g in s2p['s2'].get('duplicate_groups', [])
        if set(g) & set(members)
    ]

    retained = list(s3p['s3']['retained'])
    use = copy.deepcopy(s3p['s3']['use'])
    if set(use) - set(retained):
        fail('S3 use map references objects outside retained: %s'
             % sorted(set(use) - set(retained)))

    ingest = {}
    for oid in retained:
        if oid not in oracle['objects']:
            fail('retained object %s is absent from the oracle' % oid)
        src = oracle['objects'][oid]
        if 'text' not in src or 'provenance' not in src:
            fail('oracle object %s lacks text or provenance' % oid)
        has_temporal = 'temporal' in src
        has_status = 'status' in src
        if has_temporal == has_status:
            fail('oracle object %s must carry exactly one of temporal/status' % oid)
        rec = {'payload': src['text'], 'provenance': src['provenance']}
        if has_temporal:
            rec['temporal'] = src['temporal']
        else:
            rec['status'] = src['status']
        ingest[oid] = rec

    contracts = pmap.get('contracts')
    if not contracts:
        fail('projection map has no contracts block')

    ctx = {
        'cand': cand,
        'rendered': rendered,
        'retained': retained,
        'use': use,
        'reuse': copy.deepcopy(s3p['s3']['reuse']),
        'members': members,
        'relations': relations,
        'claim_relations': claim_relations,
        'duplicate_groups': duplicate_groups,
        'ingest': ingest,
        'contracts': contracts,
    }

    view = {}
    seen = set()
    for rule in pmap['rules']:
        dst = rule.get('dst')
        op = rule.get('op')
        if not dst or dst in seen:
            fail('projection map has missing or duplicate dst %r' % dst)
        if set(rule) - {'dst', 'op', 'owner', 'source', 'source_path',
                        'condition', 'required', 'transform', 'expands'}:
            fail('projection map rule %s has unknown keys' % dst)
        if op not in OPS or op not in OP_CONTRACTS:
            fail('projection map rule %s uses unknown op %r' % (dst, op))
        contract = OP_CONTRACTS[op]
        for key in ('dst', 'owner', 'source', 'source_path',
                    'condition', 'required', 'transform'):
            if rule.get(key) != contract.get(key):
                fail('projection map rule %s %s=%r does not match op contract %r'
                     % (dst, key, rule.get(key), contract.get(key)))
        if rule.get('expands') != contract.get('expands'):
            fail('projection map rule %s expands=%r does not match op contract %r'
                 % (dst, rule.get('expands'), contract.get('expands')))
        seen.add(dst)
        set_path(view, dst, OPS[op](ctx))

    if set(OP_CONTRACTS) != set(OPS):
        fail('op registry and op contract table do not cover the same ops')
    if {r['op'] for r in pmap['rules']} != set(OPS):
        fail('projection map ops do not match the implemented op set')
    if set(view) != set(pmap['groups']):
        fail('projected groups %s do not match frozen groups %s'
             % (sorted(view), sorted(pmap['groups'])))
    return view


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
        'id': 'C2', 'subject': 'old left MCA infarct', 'anchors': ['S01'],
        'salience': {'acuity': 'LOW', 'management_reference_spans': []},
        'claim_candidates': [{'id': 'CC2', 'text': 'known left MCA infarct', 'support': ['S01']}]})
def s1_06(a): a['s1']['candidates'][0]['status_current'] = True

def s2_01(a): a['s2']['representations'][0]['support_refs'] = []
def s2_02(a): a['s2']['representations'][0]['members'].append('O07')
def s2_03(a): a['s2']['adjudication'][0]['temporal'] = 'now'
def s2_06(a): a['s2']['adjudication'][0]['adoption'] = None

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
        'problem': 'C1', 'approved_representation': 'R1', 'selected_rep': 'R1'})
def s3_09(a):
    a['s3']['candidate_outcomes'][0]['reason'] = None
def s3_10(a):
    a['s3']['candidate_outcomes'][0]['basis'] = []

def s4_01(a): a['s4']['problems'].pop()
def s4_02(a): a['s4']['problems'].append({'id': 'P2', 'source': 'C9', 'order': 2})
def s4_04(a): a['s4']['units'][0]['members'].append('O99')
def s4_05(a): a['s4']['units'][0]['representation'] = 'R-999'
def s4_06(a): a['s4']['units'] = [u for u in a['s4']['units'] if u['id'] != 'U2']
def s4_07(a): a['s4_input_view']['adoption'] = True
def s4_08(a): a['s4_input_view']['from_s2']['members'] = ['O03', 'O04', 'O05']
def s4_09(a): a['s4_input_view']['from_s2']['selected_rep'] = 'R-999'
def s4_10(a):
    a['s4_input_view']['from_ingest']['O05']['payload'] = 'vitamin D'
def s4_11(a): a['s4_input_view']['from_s2']['duplicate_groups'] = [['O03', 'O04']]


SEEDS = [
 ('S1_PARENT.json', 'G0-S1-01', 'S1-AUTH-01', s1_01, '/s1/candidates/0/adopted', '<absent>', 'true'),
 ('S1_PARENT.json', 'G0-S1-02', 'S1-AUTH-02', s1_02, '/s1/candidates/0/selected_claim', '<absent>', 'CC1'),
 ('S1_PARENT.json', 'G0-S1-04', 'S1-CAND-02', s1_04, '/s1/candidates/0/anchors', '["S02"]', '[]'),
 ('S1_PARENT.json', 'G0-S1-05', 'S1-CAND-01', s1_05, '/s1/candidates', '<absent>', 'C2 context-only'),
 ('S1_PARENT.json', 'G0-S1-06', 'S1-AUTH-01', s1_06, '/s1/candidates/0/status_current', '<absent>', 'true'),
 ('S2_PARENT.json', 'G0-S2-01', 'S2-REP-01', s2_01, '/s2/representations/0/support_refs', '["S02"]', '[]'),
 ('S2_PARENT.json', 'G0-S2-02', 'S2-REP-01', s2_02, '/s2/representations/0/members', '["O03","O04"]', 'adds O07 medication'),
 ('S2_PARENT.json', 'G0-S2-03', 'S2-TEMP-01', s2_03, '/s2/adjudication/0/temporal', '2024-02 documented', 'now'),
 ('S2_PARENT.json', 'G0-S2-06', 'S2-ADOPT-01', s2_06, '/s2/adjudication/0/adoption', 'false', 'null'),
 ('S3_PARENT.json', 'G0-S3-01', 'S3-INC-01', s3_01, '/s3/rendered/0/approved_representation', 'R1', 'null'),
 ('S3_PARENT.json', 'G0-S3-02', 'S3-SEL-01', s3_02, '/s3/rendered/0/selected_rep', 'R1', 'R-999'),
 ('S3_PARENT.json', 'G0-S3-04', 'S3-ACCT-01', s3_04, '/s3/dispositions', 'O07 recorded', 'O07 unaccounted'),
 ('S3_PARENT.json', 'G0-S3-05', 'S3-CAND-01', s3_05, '/s3/candidate_outcomes', 'C1 RENDERED', '[] coverage'),
 ('S3_PARENT.json', 'G0-S3-06', 'S3-CAND-01', s3_06, '/s3/candidate_outcomes', 'one outcome', 'two exclusivity'),
 ('S3_PARENT.json', 'G0-S3-07', 'S3-CAND-01', s3_07, '/s3/candidate_outcomes', '<absent>', 'unknown id C9'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-08', 'S3-CAND-01', s3_08, '/s3/rendered', '[]', 'C1 rendered while outcome is NOT_RENDERED'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-09', 'S3-CAND-01', s3_09, '/s3/candidate_outcomes/0/reason', 'NO_APPROVED_REPRESENTATION', 'null'),
 ('S3_PARENT_NOT_RENDERED.json', 'G0-S3-10', 'S3-CAND-01', s3_10, '/s3/candidate_outcomes/0/basis', '["O03","O04"]', '[]'),
 ('S4_PARENT.json', 'G0-S4-01', 'S4-INC-01', s4_01, '/s4/problems', '1 problem', '0 problems'),
 ('S4_PARENT.json', 'G0-S4-02', 'S4-INC-01', s4_02, '/s4/problems', '<absent>', 'P2 not rendered'),
 ('S4_PARENT.json', 'G0-S4-04', 'S4-MEM-01', s4_04, '/s4/units/0/members', '<absent>', 'O99'),
 ('S4_PARENT.json', 'G0-S4-05', 'S4-REP-01', s4_05, '/s4/units/0/representation', 'R1', 'R-999'),
 ('S4_PARENT.json', 'G0-S4-06', 'S4-COMP-01', s4_06, '/s4/units', 'U2 present', 'U2 removed'),
 ('S4_PARENT.json', 'G0-S4-07', 'S4-PROJ-01', s4_07, '/s4_input_view/adoption', '<absent>', 'adoption schema'),
 ('S4_PARENT.json', 'G0-S4-08', 'S4-PROJ-01', s4_08, '/s4_input_view/from_s2/members', '["O03","O04"]', 'adds O05 invented'),
 ('S4_PARENT.json', 'G0-S4-09', 'S4-PROJ-01', s4_09, '/s4_input_view/from_s2/selected_rep', '<absent>', 'S3-owned field under S2 wrong-owner group'),
 ('S4_PARENT.json', 'G0-S4-10', 'S4-PROJ-01', s4_10, '/s4_input_view/from_ingest/O05/payload', 'S03 payload', 'fabricated payload'),
 ('S4_PARENT.json', 'G0-S4-11', 'S4-PROJ-01', s4_11, '/s4_input_view/from_s2/duplicate_groups', '[]', '[[O03,O04]] authored'),
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
        fail('projection map identity does not match SCHEMA-2/S4_INPUT_VIEW')

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

    built_view = build_view(s1p, s2p, s3p, oracle, pmap)
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
            'selected_problem': built_view['from_s1']['problem'],
            'selected_rep': built_view['from_s3']['selected_rep'],
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
    for a, b in (('"C1"', '"CX"'), ('"R1"', '"RX"'), ('"O03"', '"OX3"'),
                 ('"O04"', '"OX4"'), ('"O05"', '"OX5"'), ('"O06"', '"OX6"')):
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
