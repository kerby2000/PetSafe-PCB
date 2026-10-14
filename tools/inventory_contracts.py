"""Apply only explicitly documented inventory and connectivity corrections."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def without_withdrawn_r33(partitions):
    record=json.loads((ROOT/'evidence/r33_withdrawal_v0932.json').read_text())
    assert record['baseline_commit']=='9ad2715'
    assert record['removed_net_members']=={'H_PIR_RAW':['R33.1'],'H_PIR_VDD':['R33.2']}
    result={name:list(pads) for name,pads in partitions.items()}
    for name,pads in record['removed_net_members'].items():
        for pad in pads:
            assert pad in result[name],(name,pad)
            result[name].remove(pad)
    assert not any(p.startswith('R33.') for pads in result.values() for p in pads)
    return {name:sorted(pads) for name,pads in result.items()}

def retained_crosswalk(crosswalk):
    assert {k:v for k,v in crosswalk.items() if k.startswith('R33.')}=={'R33.1':'R33.1','R33.2':'R33.2'}
    return {k:v for k,v in crosswalk.items() if not k.startswith('R33.')}

def with_antenna_outer_rail(partitions):
    record=json.loads((ROOT/'evidence/antenna_outer_rail_correction_v0937.json').read_text())
    expected={ref+'.1' for ref in ['C11','C14','C29','C44','C47']}
    assert record['baseline_commit']=='2bd82bc'
    assert record['measured_pair']==['C11.1','ANT2.1'] and record['measured_ohms']==1.4
    assert len(record['changes'])==5
    assert {c['endpoint'] for c in record['changes']}==expected
    result={name:list(pads) for name,pads in partitions.items()}
    for change in record['changes']:
        assert (change['old_net'],change['new_net'])==('GND','H_ANT_B')
        pad=change['endpoint']
        assert pad in result['GND'] and pad not in result['H_ANT_B']
        result['GND'].remove(pad);result['H_ANT_B'].append(pad)
    assert set(record['unchanged_rear_ground_pads']) <= set(result['GND'])
    return {name:sorted(pads) for name,pads in result.items()}
