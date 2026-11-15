import copy
import json
import os
import sys
import unittest
from unittest import mock

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, 'tools'))

from scorer import FIRED, SILENT, UNDECIDABLE, score  # noqa: E402
from scorer import projection  # noqa: E402
from gate0_harness import (  # noqa: E402
    InputIntegrityError,
    aggregate_human,
    build_packet,
    dependency_context,
    evaluate_artifact,
    read_block,
    specificity,
    verdict_for,
)

SCHEMA = os.path.join(BASE, 'experiments/architecture/AX-S1S2-D/schema.md')


def rules():
    return {
        'reason_registry': read_block(SCHEMA, 'REASON_REGISTRY'),
        'projection_map': read_block(SCHEMA, 'PROJECTION_MAP'),
    }


def base_fixtures():
    oracle = {
        'case': 'SYN-1',
        'matching': 'concept identity',
        'objects': {
            'O1': {'text': 'three falls since June', 'provenance': 'A', 'temporal': 'June'},
            'O2': {'text': 'no new weakness', 'provenance': 'A', 'temporal': 'now'},
            'O3': {'text': 'aspirin 81 daily', 'provenance': 'A', 'status': 'current'},
        },
        'spans': {'S1': {'text': 'Three falls since June. No new weakness.'}},
        'expected': {
            'adoption': {'O1': True},
            'candidate_concepts_must_exclude': ['infarct'],
            'candidate_outcomes': {'C1': 'RENDERED'},
            'plan_items_requiring_units': ['O2'],
            'rendered_problems': 1,
            's4_input_view_groups': ['from_s1', 'from_s3', 'from_s2',
                                     'from_ingest', 'from_contracts'],
        },
    }
    s1 = {
        'case': 'SYN-1', 'parent_id': 'S1_SYN', 'parent_type': 'S1_OUTPUT',
        'registry': 'PILOT-2', 'schema': 'SCHEMA-2',
        's1': {'candidates': [{
            'id': 'C1', 'subject': 'falls since June', 'anchors': ['S1'],
            'salience': {'acuity': 'MODERATE', 'management_reference_spans': ['S1']},
            'claim_candidates': [{'id': 'CC1', 'text': 'three falls since June',
                                  'support': ['S1']}],
        }]},
    }
    s2 = {
        'case': 'SYN-1', 'parent_id': 'S2_SYN', 'parent_type': 'S2_OUTPUT',
        'registry': 'PILOT-2', 'schema': 'SCHEMA-2',
        's2': {
            'adjudication': [{'object': 'O1', 'temporal': 'June', 'adoption': True,
                              'evidence': ['S1']}],
            'relations': [{'type': 'SUPPORTS', 'from': 'O2', 'to': 'O1'}],
            'claim_relations': [],
            'duplicate_groups': [],
            'representations': [{'id': 'R1', 'problem': 'C1', 'members': ['O1', 'O2'],
                                 'support_refs': ['S1'], 'selection_safe': True}],
        },
    }
    s3 = {
        'case': 'SYN-1', 'parent_id': 'S3_SYN', 'parent_type': 'S3_OUTPUT',
        'registry': 'PILOT-2', 'schema': 'SCHEMA-2',
        's3': {
            'rendered': [{'problem': 'C1', 'approved_representation': 'R1',
                          'selected_rep': 'R1'}],
            'candidate_outcomes': [{'candidate': 'C1', 'outcome': 'RENDERED'}],
            'retained': ['O1', 'O2'],
            'use': {'O1': 'C1', 'O2': 'C1'},
            'reuse': [],
            'dispositions': [{'object': 'O3', 'disposition': 'MEDICATION_RECORD'}],
        },
    }
    view = {
        'from_s1': {'problem': 'C1',
                    'salience': {'acuity': 'MODERATE',
                                 'management_reference_spans': ['S1']}},
        'from_s3': {'selected_rep': 'R1', 'rendered': ['C1'],
                    'retained': ['O1', 'O2'],
                    'use': {'O1': 'C1', 'O2': 'C1'}, 'reuse': []},
        'from_s2': {'members': ['O1', 'O2'],
                    'relations': [{'type': 'SUPPORTS', 'from': 'O2', 'to': 'O1'}],
                    'claim_relations': [], 'duplicate_groups': []},
        'from_ingest': {
            'O1': {'payload': 'three falls since June', 'provenance': 'A',
                   'temporal': 'June'},
            'O2': {'payload': 'no new weakness', 'provenance': 'A',
                   'temporal': 'now'},
        },
        'from_contracts': {'section': 'AP', 'operator_set': 'PILOT-OPERATORS-1'},
    }
    s4 = {
        'case': 'SYN-1', 'parent_id': 'S4_SYN', 'parent_type': 'S4_BLUEPRINT',
        'registry': 'PILOT-2', 'schema': 'SCHEMA-2',
        's4_input_view': view,
        's4': {
            'sections': ['AP'],
            'problems': [{'id': 'P1', 'source': 'C1', 'order': 1}],
            'units': [
                {'id': 'U1', 'problem': 'P1', 'representation': 'R1',
                 'members': ['O1', 'O2'], 'operator': 'FACT', 'order': 10,
                 'roles': {'O1': 'HEAD', 'O2': 'MODIFIER'}},
                {'id': 'U2', 'problem': 'P1', 'representation': 'R1',
                 'members': ['O2'], 'operator': 'PLAN', 'order': 20,
                 'roles': {'O2': 'HEAD'}},
            ],
        },
    }
    return s1, s2, s3, s4, oracle, rules()


def find(result, pid):
    for f in result['findings']:
        if f['predicate_id'] == pid:
            return f
    raise AssertionError('missing finding %s' % pid)


class ScorerTests(unittest.TestCase):
    def setUp(self):
        self.s1, self.s2, self.s3, self.s4, self.oracle, self.rules = base_fixtures()
        self.deps_s2 = {'S1_SYN': self.s1}
        self.deps_s3 = {'S1_SYN': self.s1, 'S2_SYN': self.s2}
        self.deps_s4 = {'S1_SYN': self.s1, 'S2_SYN': self.s2, 'S3_SYN': self.s3}

    def test_clean_mechanical_findings_are_silent(self):
        cases = [
            (self.s1, {}, ['S1-AUTH-01', 'S1-AUTH-02', 'S1-CAND-02']),
            (self.s2, self.deps_s2, ['S2-TEMP-01']),
            (self.s3, self.deps_s3, ['S3-CAND-01', 'S3-INC-01', 'S3-SEL-01',
                                     'S3-ACCT-01']),
            (self.s4, self.deps_s4, ['S4-INC-01', 'S4-MEM-01', 'S4-COMP-01',
                                     'S4-REP-01', 'S4-PROJ-01']),
        ]
        for target, deps, pids in cases:
            result = score(target, deps, self.oracle, self.rules)
            for pid in pids:
                self.assertEqual(find(result, pid)['status'], SILENT, pid)

    def test_s1_auth_field(self):
        self.s1['s1']['candidates'][0]['adopted'] = True
        result = score(self.s1, {}, self.oracle, self.rules)
        self.assertEqual(find(result, 'S1-AUTH-01')['status'], FIRED)
        self.assertEqual(find(result, 'S1-AUTH-01')['path'],
                         '/s1/candidates/0/adopted')

    def test_s1_candidate_anchor(self):
        self.s1['s1']['candidates'][0]['anchors'] = []
        result = score(self.s1, {}, self.oracle, self.rules)
        self.assertEqual(find(result, 'S1-CAND-02')['status'], FIRED)

    def test_s1_selected_claim_field(self):
        self.s1['s1']['candidates'][0]['selected_claim'] = 'CC1'
        result = score(self.s1, {}, self.oracle, self.rules)
        self.assertEqual(find(result, 'S1-AUTH-02')['status'], FIRED)

    def test_s2_temporality(self):
        self.s2['s2']['adjudication'][0]['temporal'] = 'now'
        result = score(self.s2, self.deps_s2, self.oracle, self.rules)
        self.assertEqual(find(result, 'S2-TEMP-01')['status'], FIRED)

    def test_s3_sel_uses_s2_approved_set_not_proxy(self):
        # Both S3 fields say R-999. A proxy equality check would pass; S2 only approves R1.
        self.s3['s3']['rendered'][0]['approved_representation'] = 'R-999'
        self.s3['s3']['rendered'][0]['selected_rep'] = 'R-999'
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        finding = find(result, 'S3-SEL-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertEqual(finding['observed'], 'R-999')

    def test_s3_cand_uses_s1_candidate_set(self):
        self.s3['s3']['candidate_outcomes'] = []
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        finding = find(result, 'S3-CAND-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertIn('COVERAGE', [v['kind'] for v in finding['evidence']])

    def test_s3_cand_reason_and_basis(self):
        self.s3['s3']['rendered'] = []
        self.s3['s3']['candidate_outcomes'] = [{
            'candidate': 'C1', 'outcome': 'NOT_RENDERED',
            'reason': 'NO_APPROVED_REPRESENTATION', 'basis': ['O1'],
        }]
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-CAND-01')['status'], SILENT)

        missing_reason = copy.deepcopy(self.s3)
        missing_reason['s3']['candidate_outcomes'][0]['reason'] = None
        result = score(missing_reason, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-CAND-01')['status'], FIRED)

        missing_basis = copy.deepcopy(self.s3)
        missing_basis['s3']['candidate_outcomes'][0]['basis'] = []
        result = score(missing_basis, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-CAND-01')['status'], FIRED)

    def test_s3_accounting(self):
        self.s3['s3']['dispositions'] = []
        result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-ACCT-01')['status'], FIRED)

    def test_s4_inclusion(self):
        self.s4['s4']['problems'] = []
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-INC-01')['status'], FIRED)

    def test_s4_membership(self):
        self.s4['s4']['units'][0]['members'].append('O3')
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-MEM-01')['status'], FIRED)

    def test_s4_completeness(self):
        self.s4['s4']['units'] = [u for u in self.s4['s4']['units'] if u['id'] != 'U2']
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-COMP-01')['status'], FIRED)

    def test_s4_representation(self):
        self.s4['s4']['units'][0]['representation'] = 'R-999'
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-REP-01')['status'], FIRED)

    def test_s4_projection_uses_upstream_sources(self):
        self.s4['s4_input_view']['from_s2']['members'].append('O3')
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        finding = find(result, 'S4-PROJ-01')
        self.assertEqual(finding['status'], FIRED)
        self.assertIn('/from_s2/members', finding['path'])

    def test_s4_projection_rejects_extra_key(self):
        self.s4['s4_input_view']['adoption'] = True
        result = score(self.s4, self.deps_s4, self.oracle, self.rules)
        self.assertEqual(find(result, 'S4-PROJ-01')['status'], FIRED)

    def test_human_predicates_are_undecidable_not_fired(self):
        result = score(self.s1, {}, self.oracle, self.rules)
        self.assertEqual(find(result, 'S1-CAND-01')['status'], UNDECIDABLE)
        result = score(self.s2, self.deps_s2, self.oracle, self.rules)
        self.assertEqual(find(result, 'S2-ADOPT-01')['status'], UNDECIDABLE)
        self.assertEqual(find(result, 'S2-REP-01')['status'], UNDECIDABLE)

    def test_scorer_does_not_open_files(self):
        with mock.patch('builtins.open', side_effect=AssertionError('file access')):
            result = score(self.s3, self.deps_s3, self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-SEL-01')['status'], SILENT)

    def test_answer_key_metadata_does_not_change_findings(self):
        polluted = dict(self.rules)
        polluted['expected'] = {'S3-SEL-01': 'FIRED', 'S3-CAND-01': 'FIRED'}
        a = score(self.s3, self.deps_s3, self.oracle, self.rules)
        b = score(self.s3, self.deps_s3, self.oracle, polluted)
        self.assertEqual(a['findings'], b['findings'])


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.s1, self.s2, self.s3, self.s4, self.oracle, self.rules = base_fixtures()

    def test_specificity_exact(self):
        findings = [
            {'predicate_id': 'S1-AUTH-01', 'status': FIRED},
            {'predicate_id': 'S1-AUTH-02', 'status': SILENT},
            {'predicate_id': 'S1-CAND-01', 'status': SILENT},
            {'predicate_id': 'S1-CAND-02', 'status': SILENT},
        ]
        self.assertTrue(specificity('S1_OUTPUT', findings, 'S1-AUTH-01')['pass'])
        findings[1]['status'] = FIRED
        self.assertFalse(specificity('S1_OUTPUT', findings, 'S1-AUTH-01')['pass'])

    def test_verdict_incomplete_on_undecidable(self):
        findings = [
            {'predicate_id': 'S1-AUTH-01', 'status': UNDECIDABLE},
            {'predicate_id': 'S1-AUTH-02', 'status': SILENT},
            {'predicate_id': 'S1-CAND-01', 'status': SILENT},
            {'predicate_id': 'S1-CAND-02', 'status': SILENT},
        ]
        verdict, _ = verdict_for('S1_OUTPUT', findings, 'S1-AUTH-01')
        self.assertEqual(verdict, 'INCOMPLETE')

    def test_s2_rep_packet_contains_s1_claim_context(self):
        packet = build_packet('S2-REP-01', self.s2, {'S1_SYN': self.s1}, self.oracle)
        self.assertIn('S1_OUTPUT', packet['dependency_context'])
        text = json.dumps(packet['dependency_context'])
        self.assertIn('three falls since June', text)
        dumped = json.dumps(packet)
        self.assertNotIn('G0-S', dumped)
        self.assertNotIn('must_fire', dumped)

    def test_aggregate_human_three_judgments(self):
        packet = build_packet('S2-REP-01', self.s2, {'S1_SYN': self.s1}, self.oracle)
        result = score(self.s2, {'S1_SYN': self.s1}, self.oracle, self.rules)
        finding = find(result, 'S2-REP-01')
        finding['packet_id'] = packet['packet_id']
        packets = {'S2-REP-01': packet}
        base = {'packet_id': packet['packet_id'], 'predicate_id': 'S2-REP-01',
                'judge_type': 'HUMAN', 'verdict': FIRED, 'rationale': 'x'}
        aggregate_human(result, packets, [dict(base, judge_id='j1'),
                                          dict(base, judge_id='j2')])
        self.assertEqual(finding['status'], UNDECIDABLE)
        aggregate_human(result, packets, [dict(base, judge_id='j1'),
                                          dict(base, judge_id='j2'),
                                          dict(base, judge_id='j3')])
        self.assertEqual(finding['status'], FIRED)
        mixed = [dict(base, judge_id='j1'), dict(base, judge_id='j2'),
                 dict(base, judge_id='j3', verdict=SILENT)]
        aggregate_human(result, packets, mixed)
        self.assertEqual(finding['status'], UNDECIDABLE)

    def test_dependency_hash_mismatch_fails(self):
        manifest = {
            'dependency_context': {
                'S2_OUTPUT': [{
                    'parent_id': 'S1_SYN', 'parent_type': 'S1_OUTPUT',
                    'artifact': 'PARENT-S1.json', 'hash': 'sha256:bad',
                }],
            },
        }
        with self.assertRaises(InputIntegrityError):
            dependency_context(manifest, {'S1_SYN': self.s1}, 'S2_OUTPUT')

    def test_evaluate_artifact_does_not_accept_expected(self):
        # The function signature has no expected-predicate argument; this test
        # records the boundary and proves findings do not depend on it.
        result = evaluate_artifact(self.s3, {'S1_SYN': self.s1, 'S2_SYN': self.s2},
                                   self.oracle, self.rules)
        self.assertEqual(find(result, 'S3-SEL-01')['status'], SILENT)

    def test_projection_builder_matches_synthetic_clean_view(self):
        built = projection.build_expected_view(
            {'S1_SYN': self.s1, 'S2_SYN': self.s2, 'S3_SYN': self.s3},
            self.oracle, self.rules['projection_map'])
        self.assertEqual(built, self.s4['s4_input_view'])


if __name__ == '__main__':
    unittest.main()
