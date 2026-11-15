#!/usr/bin/env python3
"""Build the DC-002 execution package from source artifacts.

Source (hand-authored, authoritative):
  AX-S1S2-D/parents/S{1,2,3,4}_PARENT.json
  AX-S1S2-D/fixtures/CASE-01/oracle.json
  AX-S1S2-D/schema.md, predicates.md
  gate0/seeds/G0-SEEDS.md
  this file's SEEDS table

Generated (never hand-edited):
  gate0/seeds/generated/PARENT-*.json, G0-*.json, MANIFEST.json

Run: python architecture-reboot/tools/make_seeds.py
Idempotent: a second run must produce no diff.
"""
import copy
import hashlib
import io
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AX = os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D')
G0 = os.path.join(ROOT, 'experiments/gate0')
GEN = os.path.join(G0, 'seeds/generated')
PAR = os.path.join(AX, 'parents')

REG, ACTIVE, SCHEMA, ORACLE_VER = 'PILOT-2', 'ACTIVE-PILOT-2', 'SCHEMA-2', 'ORACLE-2.0'
CAMPAIGN = 'GATE0-C1'


def canon(o):
    return 'sha256:' + hashlib.sha256(
        json.dumps(o, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def fsha(p):
    return 'sha256:' + hashlib.sha256(io.open(p, 'rb').read()).hexdigest()


def load(name):
    return json.load(io.open(os.path.join(PAR, name), encoding='utf-8'))


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
def s2_03(a): a['s2']['adjudication'][0]['temporal'] = 'now'
def s2_06(a): a['s2']['adjudication'][0]['adoption'] = None

def s3_01(a): a['s3']['rendered'][0]['approved_representation'] = None
def s3_02(a): a['s3']['rendered'][0]['selected_rep'] = 'R-999'
def s3_04(a):
    a['s3']['dispositions'] = [d for d in a['s3']['dispositions'] if d['object'] != 'O07']
def s3_05(a): a['s3']['candidate_outcomes'] = []
def s3_06(a):
    a['s3']['candidate_outcomes'].append({'candidate': 'C1', 'outcome': 'NOT_RENDERED',
                                          'reason': 'NO_PROPOSAL'})
def s3_07(a):
    a['s3']['candidate_outcomes'].append({'candidate': 'C9', 'outcome': 'NOT_RENDERED',
                                          'reason': 'NO_PROPOSAL'})
def s3_08(a): a['s3']['candidate_outcomes'][0]['outcome'] = 'NOT_RENDERED'
def s3_09(a): a['s3']['candidate_outcomes'].append({'candidate': 'C1', 'outcome': 'NOT_RENDERED'})
def s3_10(a):
    a['s3']['candidate_outcomes'][0] = {'candidate': 'C1', 'outcome': 'NOT_RENDERED',
                                        'reason': 'NO_PROPOSAL', 'basis': []}

def s4_01(a): a['s4']['problems'].pop()
def s4_02(a): a['s4']['problems'].append({'id': 'P2', 'source': 'C9', 'order': 2})
def s4_04(a): a['s4']['units'][0]['members'].append('O99')
def s4_05(a): a['s4']['units'][0]['representation'] = 'R-999'
def s4_06(a): a['s4']['units'] = [u for u in a['s4']['units'] if u['id'] != 'U2']
def s4_07(a): a['s4_input_view']['adoption'] = True
def s4_08(a): a['s4_input_view']['from_s2']['members'] = ['O03', 'O04', 'O05']
def s4_09(a): a['s4_input_view']['from_s2']['selected_rep'] = 'R-999'
def s4_10(a):
    a['s4_input_view']['from_ingest']['O05'] = {'payload': 'vitamin D', 'provenance': 'A',
                                                'temporal': None}
def s4_11(a): a['s4_input_view']['from_s2']['claim_relation'] = 'COMPETING'


SEEDS = [
 ('S1_PARENT.json', 'G0-S1-01', 'S1-AUTH-01', s1_01, '/s1/candidates/0/adopted', '<absent>', 'true'),
 ('S1_PARENT.json', 'G0-S1-02', 'S1-AUTH-02', s1_02, '/s1/candidates/0/selected_claim', '<absent>', 'CC1'),
 ('S1_PARENT.json', 'G0-S1-04', 'S1-CAND-02', s1_04, '/s1/candidates/0/anchors', '["S02"]', '[]'),
 ('S1_PARENT.json', 'G0-S1-05', 'S1-CAND-01', s1_05, '/s1/candidates/-', '<absent>', 'C2 context-only'),
 ('S1_PARENT.json', 'G0-S1-06', 'S1-AUTH-01', s1_06, '/s1/candidates/0/status_current', '<absent>', 'true'),
 ('S2_PARENT.json', 'G0-S2-01', 'S2-REP-01', s2_01, '/s2/representations/0/support_refs', '["S02"]', '[]'),
 ('S2_PARENT.json', 'G0-S2-03', 'S2-TEMP-01', s2_03, '/s2/adjudication/0/temporal', '2024-02 documented', 'now'),
 ('S2_PARENT.json', 'G0-S2-06', 'S2-ADOPT-01', s2_06, '/s2/adjudication/0/adoption', 'false', 'null'),
 ('S3_PARENT.json', 'G0-S3-01', 'S3-INC-01', s3_01, '/s3/rendered/0/approved_representation', 'R1', 'null'),
 ('S3_PARENT.json', 'G0-S3-02', 'S3-SEL-01', s3_02, '/s3/rendered/0/selected_rep', 'R1', 'R-999'),
 ('S3_PARENT.json', 'G0-S3-04', 'S3-ACCT-01', s3_04, '/s3/dispositions', 'O07 recorded', 'O07 unaccounted'),
 ('S3_PARENT.json', 'G0-S3-05', 'S3-CAND-01', s3_05, '/s3/candidate_outcomes', 'C1 RENDERED', '[] coverage'),
 ('S3_PARENT.json', 'G0-S3-06', 'S3-CAND-01', s3_06, '/s3/candidate_outcomes', 'one outcome', 'two exclusivity'),
 ('S3_PARENT.json', 'G0-S3-07', 'S3-CAND-01', s3_07, '/s3/candidate_outcomes/-', '<absent>', 'unknown id C9'),
 ('S3_PARENT.json', 'G0-S3-08', 'S3-CAND-01', s3_08, '/s3/candidate_outcomes/0/outcome', 'RENDERED', 'NOT_RENDERED equality'),
 ('S3_PARENT.json', 'G0-S3-09', 'S3-CAND-01', s3_09, '/s3/candidate_outcomes/-', '<absent>', 'missing reason'),
 ('S3_PARENT.json', 'G0-S3-10', 'S3-CAND-01', s3_10, '/s3/candidate_outcomes/0/basis', '<absent>', '[] missing basis'),
 ('S4_PARENT.json', 'G0-S4-01', 'S4-INC-01', s4_01, '/s4/problems', '1 problem', '0 problems'),
 ('S4_PARENT.json', 'G0-S4-02', 'S4-INC-01', s4_02, '/s4/problems/-', '<absent>', 'P2 not rendered'),
 ('S4_PARENT.json', 'G0-S4-04', 'S4-MEM-01', s4_04, '/s4/units/0/members/-', '<absent>', 'O99'),
 ('S4_PARENT.json', 'G0-S4-05', 'S4-REP-01', s4_05, '/s4/units/0/representation', 'R1', 'R-999'),
 ('S4_PARENT.json', 'G0-S4-06', 'S4-COMP-01', s4_06, '/s4/units', 'U2 present', 'U2 removed'),
 ('S4_PARENT.json', 'G0-S4-07', 'S4-PROJ-01', s4_07, '/s4_input_view/-', '<absent>', 'adoption schema'),
 ('S4_PARENT.json', 'G0-S4-08', 'S4-PROJ-01', s4_08, '/s4_input_view/from_s2/members', '["O03","O04"]', 'adds O05 invented'),
 ('S4_PARENT.json', 'G0-S4-09', 'S4-PROJ-01', s4_09, '/s4_input_view/from_s2/selected_rep', '<absent>', 'S3-owned field under S2 wrong-owner group'),
 ('S4_PARENT.json', 'G0-S4-10', 'S4-PROJ-01', s4_10, '/s4_input_view/from_ingest/O05', 'S03 payload', 'fabricated payload'),
 ('S4_PARENT.json', 'G0-S4-11', 'S4-PROJ-01', s4_11, '/s4_input_view/from_s2/claim_relation', 'null', 'COMPETING wrong owner'),
]


def main():
    os.makedirs(GEN, exist_ok=True)
    for f in os.listdir(GEN):
        if f.endswith('.json'):
            os.remove(os.path.join(GEN, f))

    manifest = {
        'campaign': CAMPAIGN, 'registry': REG, 'active_set': ACTIVE,
        'schema': SCHEMA, 'oracle': ORACLE_VER,
        'specificity_policy': 'FULL_SILENCE-WITHIN-LAYER',
        'hash_methods': {
            'governing_source': 'sha256 over file bytes',
            'artifacts': 'sha256 over canonical JSON (sorted keys, compact separators)',
        },
        'governing_hashes': {
            'CONSENSUS_SUBMODULE_INTERFACES_v1.md': fsha(os.path.join(ROOT, 'CONSENSUS_SUBMODULE_INTERFACES_v1.md')),
            'CONSENSUS_ARCHITECTURE_v0.1.md': fsha(os.path.join(ROOT, 'CONSENSUS_ARCHITECTURE_v0.1.md')),
            '00-ARCHITECTURE-EXPERIMENT-PROGRAM.md': fsha(os.path.join(ROOT, 'experiments/architecture/00-ARCHITECTURE-EXPERIMENT-PROGRAM.md')),
            'AX-S1S2-D.md': fsha(os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D.md')),
            'schema.md': fsha(os.path.join(AX, 'schema.md')),
            'predicates.md': fsha(os.path.join(AX, 'predicates.md')),
            'G0-SEEDS.md': fsha(os.path.join(G0, 'seeds/G0-SEEDS.md')),
            'make_seeds.py': fsha(os.path.abspath(__file__)),
            '00-GATE0-MANIFEST.md': fsha(os.path.join(G0, '00-GATE0-MANIFEST.md')),
            'oracle.json': fsha(os.path.join(AX, 'fixtures/CASE-01/oracle.json')),
        },
        'clean_parents': {}, 'seeds': [],
    }

    parents = {}
    for f in ['S1_PARENT.json', 'S2_PARENT.json', 'S3_PARENT.json', 'S4_PARENT.json']:
        p = load(f)
        parents[f] = p
        manifest['clean_parents'][f] = {'parent_type': p['parent_type'], 'hash': canon(p)}
        with io.open(os.path.join(GEN, 'PARENT-' + f), 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(p, fh, indent=2, sort_keys=True)
            fh.write('\n')

    for pfile, sid, pred, fn, path, before, after in SEEDS:
        art = copy.deepcopy(parents[pfile])
        fn(art)
        name = sid + '.json'
        with io.open(os.path.join(GEN, name), 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(art, fh, indent=2, sort_keys=True)
            fh.write('\n')
        manifest['seeds'].append({
            'artifact': name, 'parent': 'PARENT-' + pfile,
            'parent_type': parents[pfile]['parent_type'], 'must_fire': pred,
            'mutations': [{'path': path, 'before': before, 'after': after}],
            'hash': canon(art)})

    # harmless variation: S3 parent with every id renamed consistently.
    var = copy.deepcopy(parents['S3_PARENT.json'])
    text = json.dumps(var, sort_keys=True)
    for a, b in (('"C1"', '"CX"'), ('"R1"', '"RX"'), ('"O03"', '"OX3"'),
                 ('"O04"', '"OX4"'), ('"O05"', '"OX5"'), ('"O06"', '"OX6"')):
        text = text.replace(a, b)
    var = json.loads(text)
    with io.open(os.path.join(GEN, 'VARIATION.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(var, fh, indent=2, sort_keys=True)
        fh.write('\n')
    manifest['variation'] = {'artifact': 'VARIATION.json', 'parent': 'PARENT-S3_PARENT.json',
                             'expect': 'zero findings',
                             'basis': 'identical semantics, all ids renamed',
                             'hash': canon(var)}

    from collections import Counter
    by = Counter(s['must_fire'] for s in manifest['seeds'])
    manifest['counts'] = {
        'clean_parents': len(manifest['clean_parents']),
        'seeds': len(manifest['seeds']),
        'active_predicates': 16,
        'by_predicate': dict(sorted(by.items())),
    }
    with io.open(os.path.join(GEN, 'MANIFEST.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print('built:', manifest['counts'])


if __name__ == '__main__':
    main()
