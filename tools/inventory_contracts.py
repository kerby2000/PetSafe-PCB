"""Apply only explicitly documented inventory and connectivity corrections."""
import json
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def verify_bridge_asset_bytes(data, record, key):
    """Imported live assets use exact LF bytes; original-source digests stay separate."""
    assert record['hash_policy']=='exact-lf-bytes-v1', 'Unknown bridge asset hash policy'
    assert b'\r' not in data, 'Imported bridge asset must use committed LF bytes'
    assert hashlib.sha256(data).hexdigest()==record[key], (key, 'Imported asset content changed')

def with_current_capacitor_rationale(inventory):
    """Only C19/C20's superseded text changes; estimated values and ratings do not."""
    import copy
    result=copy.deepcopy(inventory)
    proposal=json.loads((ROOT/'evidence/capacitor_value_review_20261015.json').read_text())
    for c in proposal['components']:
        if c['ref'] not in {'C19','C20'}:continue
        evidence=result[c['ref']]['value_evidence']
        assert evidence['basis']==c['historical_rationale']['basis']
        assert evidence['qualification']==c['historical_rationale']['remaining']
        evidence.update(basis=c['basis'],qualification=c['remaining'])
    return result

def with_reviewed_diode_symbols(inventory):
    """D1/D3 retain the BAV99 numbered direction; D2 remains the opposite equivalent."""
    import copy
    result=copy.deepcopy(inventory)
    assert result['D2']['library_symbol']=='Connector_Generic:Conn_01x03'
    result['D2']['library_symbol']='Device:D_Dual_Series_KAC'
    for ref in ['D1','D3']:
        assert result[ref]['library_symbol']=='Diode:BAV99'
        result[ref]['library_symbol']='Device:D_Dual_Series_AKC'
    return result

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


def with_r39_output_pullup(partitions):
    """Original IMG_2425 moves only R39.1 from Q2 base to its single-pad output."""
    result={name:sorted(pads) for name,pads in partitions.items()}
    assert result['PIR_BASE']==['Q2.R','R38.2','R39.1']
    assert result['H_PIR_SIG']==['Q2.S','TP16.1','U4.21']
    result['PIR_BASE'].remove('R39.1')
    result['H_PIR_SIG']=sorted(result['H_PIR_SIG']+['R39.1'])
    return result


def with_receiver_input_split_v0946(partitions):
    """Separate only the measured D2/C20/R28 group from the inherited input."""
    record=json.loads((ROOT/'evidence/receiver_input_correction_v0946.json').read_text())
    readings=json.loads((ROOT/record['measurement_source']).read_text())
    assert [r['resistance_ohms'] for r in readings['measurements']]==[1023000,998000,1.5]
    assert record['moved_endpoints']==['C20.2','D2.R','R28.2']
    result={name:sorted(pads) for name,pads in partitions.items()}
    assert result['RX_A_PLUS']==record['before']['RX_A_PLUS']
    assert 'D2_C20' not in result
    assert record['after']=={'RX_A_PLUS':['C19.1','U3.3'],'D2_C20':['C20.2','D2.R','R28.2']}
    result.update(record['after'])
    return result


def with_receiver_capacitor_separations(partitions):
    """RX-1/RX-2 withdraw exactly two inherited joins; no replacement feed inferred."""
    record=json.loads((ROOT/'evidence/receiver_input_correction_v0947.json').read_text())
    measured=json.loads((ROOT/'evidence/receiver_input_results_20261015.json').read_text())['round2']
    assert measured['shorted_probe_ohms']==1
    assert [(r['pair'],r['resistance_ohms']) for r in measured['measurements']]==[(['C19.1','U3.3'],1023000),(['C20.1','GND.1'],271000)]
    result={name:sorted(pads) for name,pads in partitions.items()}
    assert result['RX_A_PLUS']==['C19.1','U3.3'] and 'C20.1' in result['GND']
    assert record['moved_endpoints']==['C19.1','C20.1']
    assert record['before']=={k:result[k] for k in ['RX_A_PLUS','GND']}
    assert 'C19_LOWER' not in result and 'C20_UPPER' not in result
    result['RX_A_PLUS']=['U3.3'];result['GND'].remove('C20.1')
    result['C19_LOWER']=['C19.1'];result['C20_UPPER']=['C20.1']
    assert record['after']=={k:result[k] for k in ['RX_A_PLUS','GND','C19_LOWER','C20_UPPER']}
    return result


def with_receiver_input_split(partitions):
    """Preserve measured exclusions, then apply only three owner-reported joins."""
    return with_receiver_destinations(with_receiver_capacitor_separations(with_receiver_input_split_v0946(partitions)))


def with_receiver_destinations(partitions):
    record=json.loads((ROOT/'evidence/receiver_connections_v0948.json').read_text())
    assert record['baseline_commit']=='034b6cea0cf5a019cbd589007edfcaf4beab44e6'
    changes=[('U3.3','RX_A_PLUS','VREF'),('C20.1','C20_UPPER','H_D3_SIGNAL'),('C19.1','C19_LOWER','D2_C20')]
    assert [(c['endpoint'],c['old_net'],c['new_net']) for c in record['changes']]==changes
    result={name:sorted(pads) for name,pads in partitions.items()}
    assert record['before']=={n:result[n] for n in record['before']}
    for endpoint,old,new in changes:
        assert result.pop(old)==[endpoint] and endpoint not in result[new]
        result[new]=sorted(result[new]+[endpoint])
    assert record['after']=={n:result[n] for n in record['after']}
    assert len(result)==len(partitions)-3
    return result


def verify_receiver_open_erc(erc):
    """The three supported joins resolve receiver findings; retain U6A's conflict."""
    expected={
        ('pin_to_pin', tuple(sorted(['Symbol U6 Pin 3 [VOUT, Power output, Line]', 'Symbol U106 Pin 2 [VO, Power output, Line]']))),
    }
    findings=[v for sheet in erc['sheets'] for v in sheet['violations']]
    actual={(v['type'],tuple(sorted(i['description'] for i in v['items']))) for v in findings}
    assert len(findings)==len(expected) and actual==expected, 'Unexpected ERC finding or hidden U6A conflict'
    return {'pin_to_pin':1}
