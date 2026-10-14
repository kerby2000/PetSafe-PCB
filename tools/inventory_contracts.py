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

def with_ra0_tp6(partitions):
    """Allow only the B59-supported union; preserve every other partition."""
    record=json.loads((ROOT/'evidence/ra0_tp6_connection_v0938.json').read_text())
    assert record['baseline_commit']=='9c71f92'
    assert record['measured_pair']==['C25.1','TP6.1'] and record['measured_ohms']==1.5
    expected={'PIC_RA0_FILTER':['C25.1','U4.2'],'RX_A_FILTER':['C18.2','R27.1','TP6.1']}
    assert record['before']==expected
    result={name:sorted(pads) for name,pads in partitions.items()}
    for net,pads in expected.items():assert result[net]==pads,(net,result[net])
    result['RX_A_FILTER']=sorted(result.pop('PIC_RA0_FILTER')+result['RX_A_FILTER'])
    assert record['after']=={'RX_A_FILTER':result['RX_A_FILTER']}
    assert len(result)==len(partitions)-1
    return result

def with_tp14_motor_output(partitions):
    """Move only TP14 and its established R43 pad, following measured OUTA continuity."""
    record=json.loads((ROOT/'evidence/tp14_motor_output_correction_v0939.json').read_text())
    assert record['baseline_commit']=='9c71f92'
    assert record['measured_pair']==['TP14.1','U5.8'] and record['measured_ohms']==1.5
    before={'BATTERY+':['BATP.1','Q1.S','R43.2','TP14.1'],'H_MOTOR_A':['J5.A','U5.8']}
    after={'BATTERY+':['BATP.1','Q1.S'],'H_MOTOR_A':['J5.A','R43.2','TP14.1','U5.8']}
    assert record['before']==before and record['after']==after
    result={name:sorted(pads) for name,pads in partitions.items()}
    for net,pads in before.items():assert result[net]==pads,(net,result[net])
    result.update(after)
    return result


def with_u2_r5_topology(partitions):
    """Allow only the measured supply correction and photo-supported output route."""
    record=json.loads((ROOT/'evidence/u2_r5_topology_correction_v0940.json').read_text())
    assert record['baseline_commit']=='476ebfe'
    result={name:sorted(pads) for name,pads in partitions.items()}
    for net,pads in record['before'].items():assert result[net]==pads,(net,result[net])
    assert result['H_RF_OUT_CAND']==['Q8.B1','Q8.B3','R5.1']
    assert result['H_ANT_A']==['ANT1.1','R5.2']
    assert 'U2_VCC' not in result
    for pad in ['C7.1','U2.B2']:result['VDD'].remove(pad)
    result['H_RF_VDD']=sorted(result['H_RF_VDD']+['R5.1'])
    result['U2_VCC']=['C7.1','R5.2','U2.B2']
    result['H_ANT_A']=['ANT1.1','Q8.B1','Q8.B3']
    del result['H_RF_OUT_CAND']
    assert record['after']=={k:result[k] for k in ['VDD','H_RF_VDD','U2_VCC','H_ANT_A']}
    assert len(result)==len(partitions)
    return result
