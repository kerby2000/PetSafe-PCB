"""Bound the R33 withdrawal without permitting any other connectivity change."""
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
