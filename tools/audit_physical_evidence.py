"""Small independent evidence-coverage pass used by verify_evidence_contracts.

Only explicitly selected source pairs enter the graph. Modeled net membership
is the comparison target, never an input edge. Component paths are not edges.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def source_digest(path):
    data = path.read_bytes()
    # Git may convert JSON line endings on checkout. Preserve all other bytes;
    # photographs always use their exact original binary hash.
    if path.suffix.lower() == '.json':
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def compare(membership, joins, separations, observed_pads):
    parent = {p: p for p in membership}

    def root(p):
        while parent[p] != p:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p

    missing, splits, merges = [], [], []
    for edge in joins + separations:
        for p in edge['pair']:
            if p not in membership:
                missing.append({'pad': p, 'source': edge['source']})
    for item in observed_pads:
        for p in item['pads']:
            if p not in membership:
                missing.append({'pad': p, 'source': item['source']})
    for edge in joins:
        a, b = edge['pair']
        if a not in parent or b not in parent:
            continue
        if membership[a] != membership[b]:
            splits.append(edge)
        parent[root(b)] = root(a)
    for edge in separations:
        a, b = edge['pair']
        if a in parent and b in parent and membership[a] == membership[b]:
            merges.append(edge)
    groups = {}
    for p, net in sorted(membership.items()):
        groups.setdefault(net, {}).setdefault(root(p), []).append(p)
    gaps = []
    for net, components in sorted(groups.items()):
        parts = sorted(components.values())
        if len(parts) > 1:
            gaps.append({'net': net, 'groups': parts,
                         'representative_bridges': [[parts[0][0], g[0]] for g in parts[1:]],
                         'meaning': 'Missing independent support in this encoded corpus; not proof of a board error or a measurement request.'})
    return {'split_findings': splits, 'incorrect_merge_findings': merges,
            'unmapped_observed_pads': missing, 'unsupported_join_questions': gaps,
            'supported_net_groups': sum(len(c) == 1 for c in groups.values())}


def run():
    def read(path):
        return json.loads((ROOT / path).read_text(encoding='utf-8'))

    spec = read('evidence/physical_evidence_review_20261015.json')
    model = read('evidence/reconstruction.json')
    joins, separate = [], []
    for path, expected in spec['source_sha256'].items():
        assert source_digest(ROOT / path) == expected, (path, 'Evidence source changed; review supersessions')
    for imp in spec['imports']:
        data = read(imp['source'])
        for key in imp['field'].split('.'):
            data = data[key]
        if imp.get('single_pair'):
            data = [data]
        target = joins if imp['relation'] == 'same' else separate
        for pair in data:
            assert len(pair) == 2
            target.append({'pair': pair, 'source': imp['source'] + '#' + imp['field'],
                           'basis': imp['basis'], 'kind': imp['kind']})
    for observation in spec['observations']:
        target = joins if observation['relation'] == 'same' else separate
        for pair in observation['pairs']:
            target.append({'pair': pair, 'source': observation['source'],
                           'basis': observation['basis'], 'kind': observation['kind']})
    membership = {p: n['net'] for n in model['nets'] for p in n['endpoints']}
    # A photographed intentional NC remains an inventory terminal, not a net.
    for item in model['intentional_no_connects']:
        membership[item['endpoint']] = 'NC:' + item['endpoint']
    result = compare(membership, joins, separate, spec['observed_pads'])
    # Known withdrawn claims must never be reintroduced as direct copper edges.
    joined_pairs = {frozenset(e['pair']) for e in joins}
    for exclusion in spec['excluded_as_direct_edges']:
        assert frozenset(exclusion['pair']) not in joined_pairs, exclusion
    result.update(date=spec['date'], revision=model['revision'],
                  result='PASS_WITH_EVIDENCE_GAPS' if not any(result[k] for k in ['split_findings','incorrect_merge_findings','unmapped_observed_pads']) else 'CONFLICT',
                  source_record='evidence/physical_evidence_review_20261015.json',
                  direct_observations=len(joins), separation_observations=len(separate),
                  modeled_nets=len(model['nets']), joins=joins, separations=separate,
                  photo_reviews=spec['photo_reviews'], device_qualifications=spec['device_qualifications'],
                  targeted_questions=spec['targeted_questions'], supersessions=spec['supersessions'],
                  coverage_limit='A selected independent corpus, not a whole-board certification. Unrepresented source evidence may already resolve generic gaps. No netlist-derived support edges; no component/coil/DNP bridges.')
    (ROOT/'evidence/topology_closure_audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    lines = ['# Physical-evidence closure audit', '',
             f'Generated for **{model["revision"]}** by `verify_evidence_contracts.py`. Source: [selected independent evidence](../evidence/physical_evidence_review_20261015.json); [machine-readable comparison](../evidence/topology_closure_audit.json).', '',
             f'**{len(result["split_findings"])} supported joins split; {len(result["incorrect_merge_findings"])} measured separations merged; {len(result["unmapped_observed_pads"])} photographed pads missing mappings in the reviewed regions.**', '',
             f'{len(joins)} sourced join observations and {len(separate)} separation observations were checked. {len(result["unsupported_join_questions"])} modeled nets still contain separate evidence groups in this corpus. This is an evidence-coverage result, not a count of proven wrong wires. Existing native checks separately establish file consistency.', '',
             '## Decisions and specific remaining joins', '',
             '| Area | Assessment / missing evidence | Action |', '|---|---|---|']
    for q in spec['targeted_questions']:
        lines.append('| '+q['area']+' | '+q['assessment']+' | '+q['action']+' |')
    lines += ['', 'The issue register owns owner actions and closure criteria: [OPEN_ITEMS.md](OPEN_ITEMS.md#e11). The [completed original-photo probe guide](measurement-images/receiver_input_bridge.svg) is retained for orientation; C20-to-U3.3, TP7 and R28 results are recorded and must not be repeated. Generic graph gaps below are not an all-to-all bench queue.', '',
              '## Original-photo review', '', '| Region | Source | Finding |', '|---|---|---|']
    for r in spec['photo_reviews']:
        sources='; '.join(f'[{Path(p).name}](../{p})' for p in r['photos'])
        lines.append('| '+r['region']+' | '+sources+' | '+r['finding']+' |')
    lines += ['', '## Device interpretation, separate from copper', '']
    for d in spec['device_qualifications']:
        lines += ['### '+d['area'], '', d['assessment'], '', 'Sources: '+', '.join('['+Path(p).name+']('+('' if p.startswith('https:') else '../')+p+')' for p in d['sources'])+'.', '']
    lines += ['## Evidence boundaries', '',
              '- TP11/TP17: local PIC routes supported; additional hidden branches and firmware purpose remain unexcluded.',
              '- The roughly 5-ohm antenna is an external winding, not PCB copper. The 500-uH report has unspecified frequency and isolation conditions.',
              '- Fitted low-ohm readings retain contact/configuration qualifications. R5 feed pairs are photo-supported with 3.3/4-ohm corroboration, not treated as ideal meter shorts.',
              '- DNP options are not internally bridged. S1 permanent row contacts are supported by B38/B39; its pressed-state closure is not a copper edge.',
              '- Scope work and component isolation remain deferred. Capacitor candidates and values were not revised by this audit.',
              '- Inventory coverage is limited to the explicitly reviewed photo regions; numbering gaps do not establish missing parts.', '',
              '## Unsupported joins in the encoded corpus', '',
              'Each brace is a group connected by independent evidence. Separate braces on one modeled net need supporting evidence to justify their common membership. The JSON gives representative bridges; they are evidence-search targets, not automatically tests. No connection is removed solely because an edge has not been encoded.', '',
              '| Modeled net | Independently supported groups |', '|---|---|']
    for gap in result['unsupported_join_questions']:
        lines.append('| '+gap['net']+' | '+'; '.join('{'+', '.join(g)+'}' for g in gap['groups'])+' |')
    lines += ['', '## Supersessions respected', '']
    lines += ['- '+s for s in spec['supersessions']]
    (ROOT/'docs/TOPOLOGY_AUDIT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    assert result['result'] != 'CONFLICT', result
    print(f'Physical evidence: {len(joins)} join / {len(separate)} separation observations; no split/merge/mapping conflict; {len(result["unsupported_join_questions"])} nets retain evidence gaps (not presumed errors).')
    return result


if __name__ == '__main__':
    run()
