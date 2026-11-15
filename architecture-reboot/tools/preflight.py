#!/usr/bin/env python3
"""Single mechanical preflight for architecture-reboot.

Consolidates existing checks; it does not add acceptance criteria and does not
run Gate 0. Exit 0 only when every check passes.
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

import gate0_harness as harness  # noqa: E402

GENERATED = os.path.join(ROOT, 'experiments/gate0/seeds/generated')
TESTS = os.path.join(ROOT, 'tests')
SOURCE_DOCS = [
    os.path.join(ROOT, 'HANDOFF.md'),
    os.path.join(ROOT, 'experiments/gate0/00-GATE0-MANIFEST.md'),
    os.path.join(ROOT, 'experiments/gate0/seeds/G0-SEEDS.md'),
    os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D/schema.md'),
    os.path.join(ROOT, 'experiments/architecture/AX-S1S2-D/predicates.md'),
    os.path.join(ROOT, 'scorer/README.md'),
]
STALE_MARKERS = [
    'AUTHORED / UNRUN',
    'No scorer exists yet',
    'Scorer: not built',
    'four layer-specific parents',
    '27 seeds',
    '27/27',
    'unrelated family',
]
FROZEN_GIT_OBJECTS = {
    'architecture-reboot/CONSENSUS.md':
        '2d433fe021dbccee727255c4237f8eda5aff90c1',
    'architecture-reboot/CONSENSUS_ARCHITECTURE_v0.1.md':
        'cf097f93eee27ca48f45ac5a319d29287a738aee',
    'architecture-reboot/CONSENSUS_SUBMODULE_INTERFACES_v1.md':
        '897d08521fabcd6bf028e301edbdf96b1fd54baf',
    'architecture-reboot/experiments/architecture/00-ARCHITECTURE-EXPERIMENT-PROGRAM.md':
        '277e4f7f39e9e068140192439f6815dfd453a8c8',
    # Tree object pins the entire Phase-0 directory, not just one file.
    'architecture-reboot/phase0':
        '056793cbbded76bea1b13a3a4fe2fd20be04570d',
}
FORBIDDEN_PATHS = sorted(FROZEN_GIT_OBJECTS)


def check(name, fn):
    try:
        detail = fn()
        return {'name': name, 'status': 'PASS', 'detail': detail or ''}
    except SystemExit as exc:
        return {'name': name, 'status': 'FAIL', 'detail': 'SystemExit: %s' % exc}
    except Exception as exc:
        return {'name': name, 'status': 'FAIL', 'detail': '%s: %s' % (type(exc).__name__, exc)}


def snapshot(directory):
    out = {}
    for name in sorted(os.listdir(directory)):
        if name.endswith('.json'):
            with open(os.path.join(directory, name), encoding='utf-8') as fh:
                value = json.load(fh)
            out[name] = json.dumps(
                value, sort_keys=True, separators=(',', ':')).encode()
    return out


def load_make_seeds():
    path = os.path.join(ROOT, 'tools/make_seeds.py')
    spec = importlib.util.spec_from_file_location('preflight_make_seeds', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def regenerate(mod, directory):
    old = mod.GEN
    try:
        mod.GEN = directory
        with contextlib.redirect_stdout(io.StringIO()):
            mod.main()
    finally:
        mod.GEN = old


def check_frozen_zones(expected=None):
    expected = expected or FROZEN_GIT_OBJECTS
    for path, pinned in expected.items():
        proc = subprocess.run(
            ['git', 'rev-parse', 'HEAD:' + path],
            cwd=REPO, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(
                'cannot resolve frozen path %s: %s'
                % (path, proc.stderr.strip() or 'git rev-parse failed'))
        observed = proc.stdout.strip()
        if observed != pinned:
            raise RuntimeError(
                'committed frozen-zone drift at %s: %s != pinned %s'
                % (path, observed, pinned))

    proc = subprocess.run(
        ['git', 'status', '--porcelain', '--'] + sorted(expected),
        cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'git status failed')
    if proc.stdout.strip():
        raise RuntimeError('uncommitted frozen-zone drift:\n' + proc.stdout.strip())
    return 'pinned consensus/program/phase0 git objects and working tree unchanged'


def check_generation():
    mod = load_make_seeds()
    with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
        regenerate(mod, one)
        first = snapshot(one)
        regenerate(mod, two)
        second = snapshot(two)
    if first != second:
        raise RuntimeError('second regeneration differs from first')
    current = snapshot(GENERATED)
    if first != current:
        only_temp = sorted(set(first) - set(current))
        only_current = sorted(set(current) - set(first))
        changed = [name for name in sorted(set(first) & set(current))
                   if first[name] != current[name]]
        raise RuntimeError(
            'generated package is stale; only in regeneration=%s, only in repo=%s, '
            'changed=%s' % (only_temp, only_current, changed))
    return '%d generated JSON files; second run zero diff' % len(first)


def check_contract():
    manifest, clean, oracle, rules = harness.load_campaign()
    return '%s; %d clean parents; %d seeds' % (
        manifest['campaign'], len(clean), len(manifest['seeds']))


def check_dependency_context():
    manifest, clean, oracle, rules = harness.load_campaign()
    for parent_type in manifest['dependency_context']:
        harness.dependency_context(manifest, clean, parent_type)
    return 'all target types hash-pinned: %s' % ', '.join(
        sorted(manifest['dependency_context']))


def check_seed_integrity():
    manifest = harness.load_json(harness.MANIFEST)
    clean_hashes = {pid: rec['hash'] for pid, rec in manifest['clean_parents'].items()}
    seed_integrity = manifest.get('seed_integrity', {})
    if seed_integrity.get('checked') != len(manifest['seeds']):
        raise RuntimeError('seed mutation check count mismatch')
    if seed_integrity.get('noop') or seed_integrity.get('multi_diff'):
        raise RuntimeError('no-op or multi-diff seed recorded')
    for seed in manifest['seeds']:
        if seed['hash'] == clean_hashes[seed['parent_id']]:
            raise RuntimeError('seed %s equals its parent' % seed['artifact'])
        artifact = harness.load_json(os.path.join(GENERATED, seed['artifact']))
        if harness.canon(artifact) != seed['hash']:
            raise RuntimeError('seed %s hash mismatch' % seed['artifact'])
        if len(seed.get('mutations', [])) != 1:
            raise RuntimeError('seed %s does not have exactly one mutation'
                               % seed['artifact'])
    return '%d/%d seeds non-noop and hash-pinned' % (
        len(manifest['seeds']), len(manifest['seeds']))


def check_stale_markers():
    hits = []
    for path in SOURCE_DOCS:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        for marker in STALE_MARKERS:
            if marker in text:
                hits.append('%s: %s' % (os.path.relpath(path, ROOT), marker))
    if hits:
        raise RuntimeError('; '.join(hits))
    return 'no stale source markers'


def check_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(TESTS, pattern='test_*.py')
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    if not result.wasSuccessful():
        tail = '\n'.join(stream.getvalue().strip().splitlines()[-8:])
        raise RuntimeError('unit tests failed:\n' + tail)
    return '%d tests passed' % result.testsRun


def run_preflight():
    checks = [
        check('frozen architecture/phase0 drift', check_frozen_zones),
        check('source/generated freshness + determinism', check_generation),
        check('governing hashes + identities + active registry', check_contract),
        check('dependency context integrity', check_dependency_context),
        check('seed mutation integrity', check_seed_integrity),
        check('stale source markers', check_stale_markers),
        check('scorer/unit tests', check_tests),
    ]
    verdict = 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL'
    return {'verdict': verdict, 'checks': checks}


def main(argv=None):
    parser = argparse.ArgumentParser(description='architecture-reboot preflight')
    parser.add_argument('--json', action='store_true', help='print machine-readable JSON')
    args = parser.parse_args(argv)
    result = run_preflight()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result['checks']:
            print('%-4s %-45s %s' % (item['status'], item['name'], item['detail']))
        print('VERDICT:', result['verdict'])
    raise SystemExit(0 if result['verdict'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
