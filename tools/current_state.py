"""Derive current review metrics; remaining_work.json owns unresolved questions."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def value_is_known(component):
    """Only an observed/measured individual value resolves an estimate or unknown."""
    evidence = component.get('value_evidence', {})
    return (evidence.get('state') in {'observed', 'measured'}
            and bool(evidence.get('source'))
            and component.get('value', '').upper() not in {'', 'UNKNOWN', 'TBD', 'DNP'}
            and '?' not in component.get('value', ''))


def component_summary(component):
    """Current interpretation, separate from preserved dated evidence events."""
    return component.get('current_summary') or component.get('hypothesis') or component.get('note') or 'See recorded component evidence.'

def validate_issue_register(model, work):
    """Require evidence for closures and cover current gaps with active issues."""
    issues = work['issues']; ids = [i['id'] for i in issues]
    assert len(ids) == len(set(ids))
    for issue in issues:
        assert issue['state'] in {'open', 'closed'}
        for key in ('known', 'unknown', 'next_action', 'closed_when'):
            assert issue[key].strip(), (issue['id'], key)
        if issue['state'] == 'closed':
            closure = issue.get('resolution', {})
            assert closure.get('result') and closure.get('evidence') and closure.get('date'), (issue['id'], 'Closure requires result, evidence and date')
    active = [i for i in issues if i['state'] != 'closed']
    covered = {p for i in active for p in i['open_pads']}
    components = {c['ref']:c for c in model['components']}
    unresolved = set(model['unresolved_pins'])
    fitted = {p for p in unresolved if components[p.rsplit('.',1)[0]]['population'] != 'DNP'}
    assert fitted <= covered, 'A fitted open pad has no active next action'
    assert covered <= unresolved, 'Resolved/nonexistent pad still called open'
    nets = {n['net'] for n in model['nets']}
    issue_nets = {n for i in active for n in i['nets']}
    assert issue_nets <= nets, 'Active issue references a nonexistent net'
    isolated = {n['net'] for n in model['nets'] if len(n['endpoints']) == 1}
    assert isolated <= issue_nets, 'An isolated modeled node has no active issue'
    blank = {c['ref'] for c in components.values() if not c['footprint']}
    assert blank <= {r for i in active for r in i['refs']}, 'A missing footprint has no active issue'
    return active, covered, isolated

def current_state(model=None, validation=None, work=None):
    model = read('evidence/reconstruction.json') if model is None else model
    validation = read('evidence/validation.json') if validation is None else validation
    work = read('evidence/remaining_work.json') if work is None else work
    components = {c['ref']: c for c in model['components']}
    fitted = sorted(p for p in model['unresolved_pins'] if components[p.rsplit('.', 1)[0]]['population'] != 'DNP')
    dnp = sorted(set(model['unresolved_pins']) - set(fitted))
    ceramics = sorted((c['ref'] for c in components.values() if c['kind'] == 'C' and c['population'] == 'populated' and not value_is_known(c)), key=lambda ref:int(re.search(r'\d+', ref).group()))
    magnetic = sorted(c['ref'] for c in components.values() if c['kind'] == 'L' and c['population'] == 'populated' and not value_is_known(c))
    blank = sorted(c['ref'] for c in components.values() if not c['footprint'])
    return dict(
        date=work['date'], revision=model['revision'], review_revision=work['review_revision'],
        interpretation='Every catalog entry is drawn. Hardware connectivity, values and identities are only partially verified. No routed PCB exists.',
        catalog_entries=len(components), physical_pins=sum(len(c['pins']) for c in components.values()),
        unresolved_physical_pins=len(model['unresolved_pins']),
        unresolved_pins_by_population=dict(Counter(components[p.rsplit('.', 1)[0]]['population'] for p in model['unresolved_pins'])),
        unresolved_pins_by_reference=dict(Counter(p.rsplit('.', 1)[0] for p in model['unresolved_pins'])),
        current_gpio_pins=sorted(int(p.split('.')[1]) for p in fitted if p.startswith('U4.')),
        current_fitted_open_pads=fitted, current_dnp_open_pads=dnp,
        unknown_ceramic_values=ceramics, unknown_magnetic_values=magnetic,
        footprints=dict(assigned=len(components)-len(blank), unassigned=blank, qualification='Assigned is not the same as measured. R8, C11 and S1 have user body dimensions; lead geometry and exact housing variants remain qualified.'),
        erc_total=validation['erc_total'], erc_by_type=validation['erc_by_type'],
        modeled_nets=validation['proposed_net_partitions'],
        schematic_sha256=hashlib.sha256((ROOT/'schematic/PetSafe_1001339.kicad_sch').read_bytes()).hexdigest(),
        known_identified_ICs_needing_new_symbols=[], complete_symbols_for_selected_candidates=True,
        available_instruments=['LCR meter', 'multimeter'],
        via_review=read('evidence/via_audit.json')['review_summary'],
        current_gaps=[dict(id=i['id'], area=i['area'], gap=i['unknown'], method=i['next_action']) for i in work['issues'] if i['state']!='closed'],
        items=[i for i in work['issues'] if i['state']!='closed'],
        finish_plan=work.get('finish_plan', []),
        settled_summary=work.get('settled_summary', []),
        closed_items=[i for i in work['issues'] if i['state']=='closed'], rails=work['rails'],
        milestones=work.get('milestones', []),
        population_note='Open pads include empty options, test pads and internally NC pins. Zero open PIC pads does not prove every onward route.',
        completed=work['confirmed_summary'], history='docs/history/README.md',
    )

if __name__ == '__main__':
    status = current_state()
    (ROOT/'evidence/completion_status.json').write_text(json.dumps(status, indent=2)+'\n', encoding='utf-8')
    print(f"Current status: {len(status['items'])} issue groups; {len(status['current_fitted_open_pads'])} fitted-entry open pads; {len(status['current_gpio_pins'])} open PIC pads")
