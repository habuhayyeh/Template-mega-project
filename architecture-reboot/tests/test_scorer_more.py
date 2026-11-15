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
from scorer import projection, registry  # noqa: E402
from scorer.projection import ProjectionError  # noqa: E402
import gate0_harness  # noqa: E402
import preflight  # noqa: E402
from gate0_harness import (  # noqa: E402
    InputIntegrityError,
    REVIEW_POLICY,
    aggregate_campaign,
    aggregate_parent_type,
    aggregate_semantic,
    build_packet,
    canon,
    clean_verdict,
    dependency_context,
    filter_baseline_evidence,
    load_review_evidence,
    merge_review_evidence,
    validate_review_evidence,
    verify_governing_hashes,
)
from test_scorer import base_fixtures, find  # noqa: E402


def ref_record(packet_id, predicate_id, verdict=FIRED):
    return {
        'packet_id': packet_id, 'predicate_id': predicate_id,
        'judge_id': 'signer', 'judge_type': 'HUMAN', 'role': 'REFERENCE',
        'verdict': verdict, 'rationale': 'x', 'policy_version': REVIEW_POLICY,
    }


def eval_record(packet_id, predicate_id, judge_id, family, version='1',
                verdict=FIRED):
    return {
        'packet_id': packet_id, 'predicate_id': predicate_id,
        'judge_id': judge_id, 'judge_type': 'LLM', 'role': 'EVALUATOR',
        'verdict': verdict, 'rationale': 'x', 'policy_version': REVIEW_POLICY,
        'model_family': family, 'model_version': version, 'session_id': 's1',
        'context_scope': 'PACKET_ONLY', 'project_context_agent': False,
    }


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
            'parent_model': {'parent_types': ['S1_OUTPUT']},
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
                    mock.patch.object(gate0_harness, 'ORACLE', oracle_path), \
                    mock.patch.object(gate0_harness, 'verify_campaign_contract',
                                      lambda manifest: None):
                evidence = gate0_harness.run('packets', out)
            self.assertEqual(len(evidence['records']), 2)
            self.assertEqual(evidence['mode'], 'packets')
            self.assertEqual(evidence['campaign_verdict'], 'INCOMPLETE')
            self.assertIn('S1_OUTPUT', evidence['parent_type_verdicts'])
            self.assertTrue(os.path.isfile(os.path.join(out, 'EVIDENCE.json')))
            self.assertTrue(os.path.isdir(os.path.join(out, 'packets')))
            for record in evidence['records']:
                self.assertIn('dependency_context', record)
            self.assertIn('implementation_hashes', evidence)

    def test_option_f_acceptance_and_reference_reuse(self):
        s1 = copy.deepcopy(self.s1)
        seed = copy.deepcopy(self.s1)
        seed['s1']['candidates'][0]['adopted'] = True
        manifest = {
            'campaign': 'SYN-CAMPAIGN',
            'registry': 'PILOT-2',
            'active_set': 'ACTIVE-PILOT-2',
            'schema': 'SCHEMA-2',
            'oracle': 'ORACLE-2.0',
            'specificity_policy': 'FULL_SILENCE-WITHIN-LAYER',
            'governing_hashes': {},
            'clean_parents': {
                'S1_SYN': {'artifact': 'PARENT-S1.json', 'parent_id': 'S1_SYN',
                           'parent_type': 'S1_OUTPUT', 'hash': canon(s1)},
            },
            'dependency_context': {'S1_OUTPUT': []},
            'parent_model': {'parent_types': ['S1_OUTPUT']},
            'seeds': [{
                'artifact': 'G0-S1-01.json', 'hash': canon(seed),
                'parent_id': 'S1_SYN', 'parent_type': 'S1_OUTPUT',
                'must_fire': 'S1-AUTH-01',
            }],
        }
        clean_packet = build_packet('S1-CAND-01', s1, {}, self.oracle)
        seed_packet = build_packet('S1-CAND-01', seed, {}, self.oracle)
        refs = [
            ref_record(clean_packet['packet_id'], 'S1-CAND-01', SILENT),
            ref_record(seed_packet['packet_id'], 'S1-CAND-01', SILENT),
        ]
        evals = [
            eval_record(clean_packet['packet_id'], 'S1-CAND-01', 'a', 'famA', '1', SILENT),
            eval_record(clean_packet['packet_id'], 'S1-CAND-01', 'b', 'famB', '1', SILENT),
            eval_record(seed_packet['packet_id'], 'S1-CAND-01', 'a', 'famA', '1', SILENT),
            eval_record(seed_packet['packet_id'], 'S1-CAND-01', 'b', 'famB', '1', SILENT),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            gen = os.path.join(tmp, 'generated')
            out = os.path.join(tmp, 'run')
            out_baseline = os.path.join(tmp, 'run-baseline')
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
            evidence_path = os.path.join(tmp, 'evidence.json')
            with open(evidence_path, 'w', encoding='utf-8') as fh:
                json.dump({'policy_version': REVIEW_POLICY, 'references': refs,
                           'evaluators': evals}, fh)
            with mock.patch.object(gate0_harness, 'GEN', gen), \
                    mock.patch.object(gate0_harness, 'MANIFEST',
                                      os.path.join(gen, 'MANIFEST.json')), \
                    mock.patch.object(gate0_harness, 'ORACLE', oracle_path), \
                    mock.patch.object(gate0_harness, 'verify_campaign_contract',
                                      lambda manifest: None):
                evidence = gate0_harness.run('acceptance', out,
                                              evidence_path=evidence_path)
                self.assertEqual(evidence['campaign_verdict'], 'PASS')
                self.assertEqual(evidence['reference_count'], 2)
                self.assertEqual(evidence['evaluator_count'], 4)
                reused = gate0_harness.run('acceptance', out_baseline,
                                           baseline_path=evidence_path)
                self.assertEqual(reused['campaign_verdict'], 'PASS')
                self.assertEqual(reused['reference_count'], 2)
                self.assertEqual(reused['evaluator_count'], 4)

    def test_registry_matches_accepted_active_set(self):
        path = os.path.join(BASE, 'experiments/architecture/AX-S1S2-D/predicates.md')
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        match = re.search(
            r'## Pilot ACTIVE_PREDICATE_SET.*?```text\s*(.*?)```', text, re.S)
        active = {p.strip() for p in re.split(r'[,\n]', match.group(1)) if p.strip()}
        self.assertEqual(active, set(registry.PREDICATES))
        for pid in registry.SEMANTIC_PREDICATES:
            self.assertRegex(
                text,
                r'\|\s*`' + re.escape(pid) + r'`\s*\|\s*SEMANTIC / SIGNER_REFERENCE\s*\|')


    def test_frozen_zone_pin_detects_committed_drift(self):
        with self.assertRaises(RuntimeError):
            preflight.check_frozen_zones({
                'architecture-reboot/CONSENSUS.md': '0' * 40,
            })

    def test_governing_hash_mismatch_fails(self):
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(b'x')
            path = fh.name
        try:
            manifest = {'governing_hashes': {'synthetic': 'sha256:bad'}}
            with self.assertRaises(InputIntegrityError):
                verify_governing_hashes(manifest, {'synthetic': path})
        finally:
            os.unlink(path)

    def test_projection_map_drift_fails(self):
        bad = copy.deepcopy(self.rules['projection_map'])
        for rule in bad['rules']:
            if rule['op'] == 's2_relations':
                rule['source_path'] = '/s2/nope'
        deps = {'S1_SYN': self.s1, 'S2_SYN': self.s2, 'S3_SYN': self.s3}
        with self.assertRaises(ProjectionError):
            projection.build_expected_view(deps, self.oracle, bad)

    def test_dependency_context_pins_type_and_hash(self):
        manifest = {
            'dependency_context': {
                'S2_OUTPUT': [{
                    'parent_id': 'S1_SYN',
                    'parent_type': 'S1_OUTPUT',
                    'artifact': 'PARENT-S1.json',
                    'hash': canon(self.s1),
                }],
            },
        }
        context, pinned = dependency_context(manifest, {'S1_SYN': self.s1},
                                             'S2_OUTPUT')
        self.assertEqual(list(context), ['S1_SYN'])
        self.assertEqual(pinned[0]['parent_type'], 'S1_OUTPUT')
        self.assertEqual(pinned[0]['hash'], canon(self.s1))

    def test_clean_verdict_three_branches(self):
        self.assertEqual(clean_verdict([{'status': FIRED}]), 'FAIL')
        self.assertEqual(clean_verdict([{'status': UNDECIDABLE}]), 'INCOMPLETE')
        self.assertEqual(clean_verdict([{'status': SILENT}]), 'PASS')
        self.assertEqual(clean_verdict([
            {'status': UNDECIDABLE, 'calibration_failure': True},
        ]), 'FAIL')

    def test_review_evidence_binding_and_reuse(self):
        packet = build_packet('S2-REP-01', self.s2, {'S1_SYN': self.s1}, self.oracle)
        pid = packet['packet_id']
        by_pid = {'S2-REP-01': packet}
        global_packets = {pid: packet}
        ref = ref_record(pid, 'S2-REP-01', FIRED)
        ev1 = eval_record(pid, 'S2-REP-01', 'a', 'famA', FIRED)
        ev2 = eval_record(pid, 'S2-REP-01', 'b', 'famB', FIRED)

        with self.assertRaises(ValueError):
            validate_review_evidence(
                global_packets, [dict(ref, predicate_id='S2-ADOPT-01')], [ev1, ev2])
        with self.assertRaises(ValueError):
            validate_review_evidence(
                global_packets, [ref],
                [ev1, dict(ev2, predicate_id='S2-ADOPT-01')])

        baseline = {'policy_version': REVIEW_POLICY, 'references': [ref],
                    'evaluators': [ev1, ev2]}
        empty = {'policy_version': REVIEW_POLICY, 'references': [],
                 'evaluators': []}
        filtered = filter_baseline_evidence(baseline, empty, global_packets)
        merged = merge_review_evidence(filtered, empty)
        self.assertEqual(len(merged['references']), 1)
        self.assertEqual(len(merged['evaluators']), 2)

        # A changed signer reference for the same packet is a conflict, not a
        # silent override.
        conflict = {'policy_version': REVIEW_POLICY,
                    'references': [dict(ref, verdict=SILENT)],
                    'evaluators': []}
        filtered = filter_baseline_evidence(baseline, conflict, global_packets)
        with self.assertRaises(ValueError):
            merge_review_evidence(filtered, conflict)

        # A changed packet is not the same packet: the old baseline is dropped.
        other_packets = {'pkt-other': packet}
        filtered = filter_baseline_evidence(baseline, empty, other_packets)
        self.assertEqual(filtered['references'], [])
        self.assertEqual(filtered['evaluators'], [])

        # A changed evaluator model/version invalidates only that judge's cache.
        new_ev2 = eval_record(pid, 'S2-REP-01', 'b', 'famB', '2', FIRED)
        current = {'policy_version': REVIEW_POLICY, 'references': [],
                   'evaluators': [new_ev2]}
        filtered = filter_baseline_evidence(baseline, current, global_packets)
        merged = merge_review_evidence(filtered, current)
        self.assertEqual(len(merged['evaluators']), 2)
        self.assertEqual(
            [e['model_version'] for e in merged['evaluators']
             if e['judge_id'] == 'b'],
            ['2'])

        # Duplicate/missing judgments stay incomplete, not pass.
        result = score(self.s2, {'S1_SYN': self.s1}, self.oracle, self.rules)
        finding = find(result, 'S2-REP-01')
        finding['packet_id'] = pid
        aggregate_semantic(result, by_pid, [ref], [ev1], {'S2-REP-01': FIRED})
        self.assertEqual(finding['status'], UNDECIDABLE)
        self.assertEqual(finding['detail'], 'TWO_EVALUATOR_JUDGMENTS_REQUIRED')

    def test_evaluator_eligibility_metadata_required(self):
        ev = eval_record('pkt-x', 'S2-REP-01', 'a', 'famA', FIRED)
        bad = dict(ev, project_context_agent=True)
        data = {'policy_version': REVIEW_POLICY, 'references': [],
                'evaluators': [bad]}
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as fh:
            json.dump(data, fh)
            path = fh.name
        try:
            with self.assertRaises(ValueError):
                load_review_evidence(path)
        finally:
            os.unlink(path)

        missing = {k: v for k, v in ev.items() if k != 'model_family'}
        data = {'policy_version': REVIEW_POLICY, 'references': [],
                'evaluators': [missing]}
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as fh:
            json.dump(data, fh)
            path = fh.name
        try:
            with self.assertRaises(ValueError):
                load_review_evidence(path)
        finally:
            os.unlink(path)

    def test_parent_type_and_campaign_aggregation(self):
        self.assertEqual(aggregate_parent_type([{'verdict': 'PASS'}]), 'PASS')
        self.assertEqual(aggregate_parent_type(
            [{'verdict': 'PASS'}, {'verdict': 'FAIL'}]), 'FAIL')
        self.assertEqual(aggregate_parent_type(
            [{'verdict': 'PASS'}, {'verdict': 'INCOMPLETE'}]), 'INCOMPLETE')
        self.assertEqual(aggregate_campaign(
            {'S1_OUTPUT': 'PASS', 'S2_OUTPUT': 'PASS'},
            ['S1_OUTPUT', 'S2_OUTPUT']), 'PASS')
        self.assertEqual(aggregate_campaign(
            {'S1_OUTPUT': 'PASS', 'S2_OUTPUT': 'FAIL'},
            ['S1_OUTPUT', 'S2_OUTPUT']), 'FAIL')
        self.assertEqual(aggregate_campaign(
            {'S1_OUTPUT': 'PASS', 'S2_OUTPUT': 'INCOMPLETE'},
            ['S1_OUTPUT', 'S2_OUTPUT']), 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
