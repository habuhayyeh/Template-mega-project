"""Pure PROJECTION_MAP contract and executor shared by generator and scorer.

No file access, no manifest access and no expected-answer access. Both the seed
generator and the scorer call this module so the written map and the executable
semantics cannot drift apart.
"""
import copy


class ProjectionError(Exception):
    pass


OPS = {
    's1_problems': lambda c: copy.deepcopy(c['problems']),
    's3_selected_reps': lambda c: copy.deepcopy(c['selected_reps']),
    's3_selected_roles': lambda c: copy.deepcopy(c['selected_roles']),
    's3_rendered': lambda c: [r['problem'] for r in c['rendered']],
    's3_retained': lambda c: list(c['retained']),
    's3_use': lambda c: copy.deepcopy(c['use']),
    's3_reuse': lambda c: copy.deepcopy(c['reuse']),
    's2_selections': lambda c: copy.deepcopy(c['selections']),
    's2_causal_relations': lambda c: copy.deepcopy(c['causal_relations']),
    'oracle_ingest': lambda c: copy.deepcopy(c['ingest']),
    'contract_section': lambda c: c['contracts']['section'],
    'contract_operator_set': lambda c: c['contracts']['operator_set'],
}

# Each op has exactly one valid map contract. A changed destination, owner,
# source path, condition, requirement or transform fails instead of silently
# running old code.
OP_CONTRACTS = {
    's1_problems': {
        'dst': '/from_s1/problems',
        'owner': 'S1',
        'source': 'S1_PARENT.json',
        'source_path': '/s1/candidates[id in rendered]/{id,salience}',
        'condition': 'one entry per rendered problem, S3 order',
        'required': 'required',
        'transform': 'collect objects',
    },
    's3_selected_reps': {
        'dst': '/from_s3/selected_reps',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/rendered[i]/{problem,selected_rep}',
        'condition': 'all i, source order',
        'required': 'required',
        'transform': 'collect problem->rep map',
    },
    's3_selected_roles': {
        'dst': '/from_s3/selected_roles',
        'owner': 'S3',
        'source': 'S3_PARENT.json',
        'source_path': '/s3/rendered[i]/{problem,encounter_role}',
        'condition': 'all i, source order',
        'required': 'required',
        'transform': 'collect problem->role map',
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
    's2_selections': {
        'dst': '/from_s2/selections',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/representations[id=R]/members + /s2/relations + /s2/claim_relations + /s2/duplicate_groups',
        'condition': 'one per rendered problem; R = selected_reps[P]; relations filtered to members; claim relations filtered P/R; duplicate groups intersect members',
        'required': 'required',
        'transform': 'collect objects',
    },
    's2_causal_relations': {
        'dst': '/from_s2/causal_relations',
        'owner': 'S2',
        'source': 'S2_PARENT.json',
        'source_path': '/s2/causal_relations[i]',
        'condition': 'from and to in T; source order',
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
        'source': 'SCHEMA-4 contracts block',
        'source_path': '#/contracts/section',
        'condition': 'always',
        'required': 'required',
        'transform': 'copy constant',
    },
    'contract_operator_set': {
        'dst': '/from_contracts/operator_set',
        'owner': 'frozen contracts',
        'source': 'SCHEMA-4 contracts block',
        'source_path': '#/contracts/operator_set',
        'condition': 'always',
        'required': 'required',
        'transform': 'copy constant',
    },
}


def _set_path(root, dst, value):
    parts = [p for p in dst.strip('/').split('/') if p]
    if not parts:
        raise ProjectionError('empty destination path')
    cur = root
    for part in parts[:-1]:
        nxt = cur.setdefault(part, {})
        if not isinstance(nxt, dict):
            raise ProjectionError('destination path collision at %s' % dst)
        cur = nxt
    if parts[-1] in cur:
        raise ProjectionError('duplicate destination %s' % dst)
    cur[parts[-1]] = value


def validate_projection_map(pmap):
    """Fail unless every map rule exactly matches its frozen op contract."""
    if not isinstance(pmap, dict):
        raise ProjectionError('PROJECTION_MAP is missing')
    if not isinstance(pmap.get('groups'), list):
        raise ProjectionError('PROJECTION_MAP groups are missing')
    if not isinstance(pmap.get('contracts'), dict):
        raise ProjectionError('PROJECTION_MAP contracts are missing')
    if not isinstance(pmap.get('rules'), list):
        raise ProjectionError('PROJECTION_MAP rules are missing')
    if set(OP_CONTRACTS) != set(OPS):
        raise ProjectionError('op registry and op contract table do not cover the same ops')

    seen = set()
    for rule in pmap['rules']:
        if not isinstance(rule, dict):
            raise ProjectionError('projection map rule is not an object')
        dst = rule.get('dst')
        op = rule.get('op')
        if not dst or dst in seen:
            raise ProjectionError('projection map has missing or duplicate dst %r' % dst)
        if set(rule) - {'dst', 'op', 'owner', 'source', 'source_path',
                        'condition', 'required', 'transform', 'expands'}:
            raise ProjectionError('projection map rule %s has unknown keys' % dst)
        if op not in OPS or op not in OP_CONTRACTS:
            raise ProjectionError('projection map rule %s uses unknown op %r' % (dst, op))
        contract = OP_CONTRACTS[op]
        for key in ('dst', 'owner', 'source', 'source_path',
                    'condition', 'required', 'transform'):
            if rule.get(key) != contract.get(key):
                raise ProjectionError(
                    'projection map rule %s %s=%r does not match op contract %r'
                    % (dst, key, rule.get(key), contract.get(key)))
        if rule.get('expands') != contract.get('expands'):
            raise ProjectionError(
                'projection map rule %s expands=%r does not match op contract %r'
                % (dst, rule.get('expands'), contract.get('expands')))
        seen.add(dst)

    if {r['op'] for r in pmap['rules']} != set(OPS):
        raise ProjectionError('projection map ops do not match the implemented op set')


def build_view(s1p, s2p, s3p, oracle, pmap):
    """Construct the multi-problem S4_INPUT_VIEW from upstream artifacts."""
    validate_projection_map(pmap)
    try:
        rendered = s3p['s3']['rendered']
        if not isinstance(rendered, list) or not rendered:
            raise ProjectionError('S4_INPUT_VIEW requires at least one rendered problem')
        s1_by_id = {c.get('id'): c for c in s1p['s1']['candidates']}
        s2_by_id = {r.get('id'): r for r in s2p['s2']['representations']}
        problems = []
        selected_reps = {}
        selected_roles = {}
        selections = []
        seen = set()
        for entry in rendered:
            problem_id = entry.get('problem')
            selected_rep = entry.get('selected_rep')
            role = entry.get('encounter_role')
            if problem_id in seen:
                raise ProjectionError('duplicate rendered problem %s' % problem_id)
            if role not in ('PRIMARY', 'BACKGROUND'):
                raise ProjectionError(
                    'rendered problem %s has invalid encounter_role %r'
                    % (problem_id, role))
            seen.add(problem_id)
            cand = s1_by_id.get(problem_id)
            if not isinstance(cand, dict):
                raise ProjectionError('rendered problem %s has no S1 candidate' % problem_id)
            rep = s2_by_id.get(selected_rep)
            if not isinstance(rep, dict):
                raise ProjectionError(
                    'selected_rep %s has no S2 representation' % selected_rep)
            if rep.get('problem') != problem_id:
                raise ProjectionError(
                    'selected representation %s belongs to %r, not rendered problem %s'
                    % (selected_rep, rep.get('problem'), problem_id))
            members = list(rep.get('members') or [])
            if not members:
                raise ProjectionError('selected representation %s has no members'
                                      % selected_rep)
            relations = [
                copy.deepcopy(r) for r in s2p['s2'].get('relations', [])
                if r.get('from') in members and r.get('to') in members
            ]
            claim_relations = []
            for r in s2p['s2'].get('claim_relations', []):
                if 'problem' not in r or 'representation' not in r:
                    raise ProjectionError(
                        'S2 claim_relation lacks problem/representation selectors')
                if r['problem'] == problem_id and r['representation'] == selected_rep:
                    claim_relations.append(copy.deepcopy(r))
            duplicate_groups = [
                list(g) for g in s2p['s2'].get('duplicate_groups', [])
                if set(g) & set(members)
            ]
            problems.append({
                'problem': cand['id'],
                'salience': copy.deepcopy(cand.get('salience')),
            })
            selected_reps[problem_id] = selected_rep
            selected_roles[problem_id] = role
            selections.append({
                'problem': problem_id,
                'representation': selected_rep,
                'members': members,
                'relations': relations,
                'claim_relations': claim_relations,
                'duplicate_groups': duplicate_groups,
            })

        retained = list(s3p['s3']['retained'])
        causal_relations = []
        for rel in s2p['s2'].get('causal_relations', []):
            if not isinstance(rel, dict):
                raise ProjectionError('S2 causal_relation is not an object')
            if rel.get('relation') not in ('CONTRIBUTOR', 'ETIOLOGY', 'MECHANISM', 'CAUSE'):
                raise ProjectionError('S2 causal_relation has invalid type %r'
                                      % rel.get('relation'))
            if rel.get('strength') not in ('LIKELY', 'POSSIBLE', 'UNLIKELY'):
                raise ProjectionError('S2 causal_relation has invalid strength %r'
                                      % rel.get('strength'))
            if not isinstance(rel.get('support'), list) or not rel.get('support'):
                raise ProjectionError('S2 causal_relation lacks support spans')
            if rel.get('from') not in oracle.get('objects', {}):
                raise ProjectionError('S2 causal_relation from is not an oracle object')
            if rel.get('to') not in oracle.get('objects', {}):
                raise ProjectionError('S2 causal_relation to is not an oracle object')
            if rel.get('from') in retained and rel.get('to') in retained:
                causal_relations.append(copy.deepcopy(rel))
        use = copy.deepcopy(s3p['s3']['use'])
        if set(use) - set(retained):
            raise ProjectionError('S3 use map references objects outside retained: %s'
                                  % sorted(set(use) - set(retained)))

        ingest = {}
        for oid in retained:
            src = oracle.get('objects', {}).get(oid)
            if not isinstance(src, dict):
                raise ProjectionError('retained object %s is absent from the oracle' % oid)
            if 'text' not in src or 'provenance' not in src:
                raise ProjectionError('oracle object %s lacks text or provenance' % oid)
            has_temporal = 'temporal' in src
            has_status = 'status' in src
            if has_temporal == has_status:
                raise ProjectionError(
                    'oracle object %s must carry exactly one of temporal/status' % oid)
            rec = {'payload': src['text'], 'provenance': src['provenance']}
            if has_temporal:
                rec['temporal'] = src['temporal']
            else:
                rec['status'] = src['status']
            ingest[oid] = rec
    except (KeyError, TypeError, AttributeError) as exc:
        raise ProjectionError('malformed projection dependency: %s' % exc)

    ctx = {
        'problems': problems,
        'rendered': rendered,
        'selected_reps': selected_reps,
        'selected_roles': selected_roles,
        'selections': selections,
        'causal_relations': causal_relations,
        'retained': retained,
        'use': use,
        'reuse': copy.deepcopy(s3p['s3']['reuse']),
        'ingest': ingest,
        'contracts': pmap['contracts'],
    }
    view = {}
    for rule in pmap['rules']:
        _set_path(view, rule['dst'], OPS[rule['op']](ctx))
    if set(view) != set(pmap['groups']):
        raise ProjectionError('projected groups %s do not match frozen groups %s'
                              % (sorted(view), sorted(pmap['groups'])))
    return view
