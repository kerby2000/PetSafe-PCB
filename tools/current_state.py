"""Derive current review metrics; remaining_work.json owns unresolved questions."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def current_state():
    model = read('evidence/reconstruction.json')
    validation = read('evidence/validation.json')
    work = read('evidence/remaining_work.json')
    components = {c['ref']: c for c in model['components']}
    fitted = sorted(p for p in model['unresolved_pins'] if components[p.rsplit('.', 1)[0]]['population'] != 'DNP')
    dnp = sorted(set(model['unresolved_pins']) - set(fitted))
    ceramics = sorted((c['ref'] for c in components.values() if c['kind'] == 'C' and c['population'] == 'populated' and c['ref'] != 'C5'), key=lambda ref:int(re.search(r'\d+', ref).group()))
    magnetic = sorted(c['ref'] for c in components.values() if c['kind'] == 'L' and c['population'] == 'populated')
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
        footprints=dict(assigned=len(components)-len(blank), unassigned=blank, qualification='Assigned is not the same as measured. R8 and C11 anchor photo-based package families.'),
        erc_total=validation['erc_total'], erc_by_type=validation['erc_by_type'],
        modeled_nets=validation['proposed_net_partitions'],
        schematic_sha256=hashlib.sha256((ROOT/'schematic/PetSafe_1001339.kicad_sch').read_bytes()).hexdigest(),
        known_identified_ICs_needing_new_symbols=[], complete_symbols_for_selected_candidates=True,
        available_instruments=['LCR meter', 'multimeter'],
        via_review=read('evidence/via_audit.json')['review_summary'],
        current_gaps=[dict(id=i['id'], area=i['area'], gap=i['unknown'], method=i['next_action']) for i in work['issues']],
        items=work['issues'], rails=work['rails'],
        population_note='Open pads include empty options, test pads and internally NC pins. Zero open PIC pads does not prove every onward route.',
        completed=work['confirmed_summary'], history='docs/history/README.md',
    )

if __name__ == '__main__':
    status = current_state()
    (ROOT/'evidence/completion_status.json').write_text(json.dumps(status, indent=2)+'\n', encoding='utf-8')
    print(f"Current status: {len(status['items'])} issue groups; {len(status['current_fitted_open_pads'])} fitted-entry open pads; {len(status['current_gpio_pins'])} open PIC pads")
