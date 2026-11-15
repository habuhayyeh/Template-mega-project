import copy
import json
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(__file__)
BASE = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, 'tools'))
sys.path.insert(0, HERE)

from scorer import FIRED, SILENT, UNDECIDABLE, score  # noqa: E402
from scorer import registry  # noqa: E402
import gate0_harness  # noqa: E402
from gate0_harness import build_packet, canon  # noqa: E402
from test_scorer import base_fixtures, find  # noqa: E402


class AdditionalPredicateTests(unittest.TestCase):
    def setUp(self):
        self.s1, self.s2, self.s3, self.s4, self.oracle, self.rules = base_fixtures()
        self.deps_s2 = {'S1_SYN': self.s1}
        self.deps_s3 = {'S1_SYN': self.s1, 'S2_SYN': self.s2}
        self.deps_s4 = {'S1_SYN': self.s1, 'S2_SYN': self.s2, 'S3_SYN': self.s3}

    def test_s3_inclusion(self):
        self.s3['s3']['rendered'][0]['approved_representation'] = None
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-INC-01')['status'], FIRED)

    def test_s3_cand_exclusivity(self):
        self.s3['s3']['candidate_outcomes'].append({
            'candidate': 'C1', 'outcome': 'NOT_RENDERED',
            'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O1'],
        })
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        finding = find(result, 'S3-CAND-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertIn('EXCLUSIVITY', [v['kind'] for v in finding['evidence']])

    def test_s3_cand_unknown_id(self):
        self.s3['s3']['candidate_outcomes'].append({
            'candidate': 'C9', 'outcome': 'NOT_RENDERED',
            'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O1'],
        })
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        finding = find(result, 'S3-CAND-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertIn('UNKNOWN_CANDIDATE', [v['kind'] for v in finding['evidence']])

    def test_s3_cand_equality(self):
        self.s3['s3']['candidate_outcomes'] = [{
            'candidate': 'C1', 'outcome': 'NOT_RENDERED',
            'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O1'],
        }]
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        finding = find(result, 'S3-CAND-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertIn('RENDERED_SET_EQUALITY',
                      [v['kind'] for v in finding['evidence']])

    def test_s4_claim_bearing_unit(self):
        self.s4['s4']['units'] = [u for u in self.s4['s4']['units'] if u['id'] != 'U1']
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-COMP-01')['status'], FIRED)

    def test_s1_cand_packet_is_minimal(self):
        packet = build_packet('S1-CAND-01', self.s1, {}, self.oracle)
        self.assertEqual(packet['dependency_context'], {})
        self.assertIn('candidate_concepts_must_exclude', packet['oracle']['expected'])
        self.assertNotIn('plan_items_requiring_units', json.dumps(packet))

    def test_s2_adopt_packet_contains_expected_adoption(self):
        packet = build_packet('S2-ADOPT-01', self.s2, {'S1_SYN': self.s1}, self.oracle)
        self.assertEqual(packet['oracle']['expected']['adoption'], {'O1': True})

    def test_human_status_not_promoted_by_absence_of_judgments(self):
        result = score(self.s2, self.deps_s2, self.oracle, self.rules)
        self.assertEqual(find(result, 'S2-REP-01')['status'], UNDECIDABLE)

    def test_harness_packets_run_on_synthetic_fixture(self):
        s1 = copy.deepcopy(self.s1)
        seed = copy.deepcopy(self.s1)
        seed['s1']['candidates'][0]['adopted'] = True
        clean_parent = {
            'artifact': 'PARENT-S1.json',
            'parent_id': 'S1_SYN',
            'parent_type': 'S1_OUTPUT',
            'hash': canon(s1),
        }
        seed_record = {
            'artifact': 'G0-S1-01.json',
            'hash': canon(seed),
            'parent_id': 'S1_SYN',
            'parent_type': 'S1_OUTPUT',
            'must_fire': 'S1-AUTH-01',
        }
        manifest = {
            'campaign': 'SYN-CAMPAIGN',
            'registry': 'PILOT-2',
            'active_set': 'ACTIVE-PILOT-2',
            'schema': 'SCHEMA-2',
            'oracle': 'ORACLE-2.0',
            'specificity_policy': 'FULL_SILENCE-WITHIN-LAYER',
            'governing_hashes': {},
            'clean_parents': {'S1_SYN': clean_parent},
            'dependency_context': {'S1_OUTPUT': []},
            'seeds': [seed_record],
        }
        with tempfile.TemporaryDirectory() as tmp:
            gen = os.path.join(tmp, 'generated')
            out = os.path.join(tmp, 'run')
            os.makedirs(gen)
            with open(os.path.join(gen, 'MANIFEST.json'), 'w', encoding='utf-8') as fh:
                json.dump(manifest, fh)
            with open(os.path.join(gen, 'PARENT-S1.json'), 'w', encoding='utf-8') as fh:
                json.dump(s1, fh)
            with open(os.path.join(gen, 'G0-S1-01.json'), 'w', encoding='utf-8') as fh:
                json.dump(seed, fh)
            oracle_path = os.path.join(tmp, 'oracle.json')
            with open(oracle_path, 'w', encoding='utf-8') as fh:
                json.dump(self.oracle, fh)
            with mock.patch.object(gate0_harness, 'GEN', gen), \
                    mock.patch.object(gate0_harness, 'MANIFEST',
                                      os.path.join(gen, 'MANIFEST.json')), \
                    mock.patch.object(gate0_harness, 'ORACLE', oracle_path):
                evidence = gate0_harness.run('packets', out)
            self.assertEqual(len(evidence['records']), 2)
            self.assertEqual(evidence['mode'], 'packets')
            self.assertTrue(os.path.isfile(os.path.join(out, 'EVIDENCE.json')))
            self.assertTrue(os.path.isdir(os.path.join(out, 'packets')))

    def test_registry_matches_accepted_active_set(self):
        path = os.path.join(BASE, 'experiments/architecture/AX-S1S2-D/predicates.md')
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        match = re.search(
            r'## Pilot ACTIVE_PREDICATE_SET.*?```text\s*(.*?)```', text, re.S)
        active = {p.strip() for p in re.split(r'[,\n]', match.group(1)) if p.strip()}
        self.assertEqual(active, set(registry.PREDICATES))
        for pid in registry.HUMAN_PREDICATES:
            self.assertRegex(
                text,
                r'\|\s*`' + re.escape(pid) + r'`\s*\|\s*SEMANTIC / HUMAN_REVIEW\s*\|')


if __name__ == '__main__':
    unittest.main()
