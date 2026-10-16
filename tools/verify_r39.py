"""Bound the v0.9.45 R39 correction by physical memberships, not net counts."""
from pathlib import Path
import json, hashlib, subprocess, xml.etree.ElementTree as ET
from inventory_contracts import with_receiver_input_split, verify_receiver_open_erc
R=Path(__file__).resolve().parents[1]
def read(path):return json.loads((R/path).read_text(encoding='utf-8'))
record=read('evidence/r39_endpoint_correction_v0945.json')
def baseline(path):return subprocess.check_output(['git','show',record['baseline_commit']+':'+path],cwd=R)
m=read('evidence/reconstruction.json');old=json.loads(baseline('evidence/reconstruction.json'))
corrected=json.loads(subprocess.check_output(['git','show','891d69c:evidence/reconstruction.json'],cwd=R))
def partitions(model,omit=()):
    return sorted(sorted(set(n['endpoints'])-set(omit)) for n in model['nets'] if set(n['endpoints'])-set(omit))
assert partitions(corrected,['R39.1'])==partitions(old,['R39.1']), 'Historical R39 commit changed other partitions'
expected=with_receiver_input_split({n['net']:sorted(n['endpoints']) for n in corrected['nets']})
assert {n['net']:sorted(n['endpoints']) for n in m['nets']}==expected, 'Unregistered change after R39 correction'
assert m['native_pin_crosswalk']==old['native_pin_crosswalk']==read('evidence/pin_crosswalk.json')
def inventory(model):
    return {c['ref']:{k:c.get(k) for k in ['value','proposed_value','value_evidence','value_proposal','population','pins','library_symbol','footprint']} for c in model['components']}
expected_inventory=inventory(old)
assert expected_inventory['D2']['library_symbol']=='Connector_Generic:Conn_01x03'
expected_inventory['D2']['library_symbol']='Device:D_Dual_Series_KAC'
assert inventory(m)==expected_inventory,'Only D2 measured-equivalent representation may change; values/population/pad mapping stay fixed'
assert m['intentional_no_connects']==old['intentional_no_connects']
xml=ET.parse(R/'output/PetSafe_netlist.xml')
members={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
def native(ep):return members[m['native_pin_crosswalk'].get(ep,ep)]
for group in [['R39.1','TP16.1','Q2.S','U4.21'],['Q2.R','R38.2'],['R39.2','VDD.1']]:
    assert len({native(ep) for ep in group})==1,group
assert native('R39.1')!=native('Q2.R')
native_physical={}
for ep,target in m['native_pin_crosswalk'].items():
    if ep=='R39.1' or ep in m['unresolved_pins'] or ep in {x['endpoint'] for x in m['intentional_no_connects']}:continue
    if target in members:native_physical.setdefault(members[target],[]).append(ep)
assert sorted(sorted(pads) for pads in native_physical.values())==partitions(m,['R39.1']), 'Exported physical partitions differ from bounded live model'
assert hashlib.sha256((R/record['photo']).read_bytes()).hexdigest()==record['photo_sha256']
def erc_types(data):return sorted(v['type'] for s in data['sheets'] for v in s['violations'])
assert erc_types(json.loads(baseline('output/erc.json')))==['pin_to_pin']
verify_receiver_open_erc(read('output/erc.json'))
result=dict(result='PASS',revision=m['revision'],baseline_commit=record['baseline_commit'],historical_correction_commit='891d69c',moved_endpoint='R39.1',before='PIR_BASE',after='H_PIR_SIG',all_other_normalized_physical_partitions_at_correction='IDENTICAL',subsequent_bounded_correction='evidence/receiver_input_correction_v0946.json',native_endpoint_checks='PASS',values_population_symbols_crosswalk='UNCHANGED',photo_sha256='MATCH',erc_types='Original U6/U106 conflict retained; receiver destinations checked by bounded v0.9.48 correction',net_count_before=len(old['nets']),net_count_at_r39_correction=len(corrected['nets']),live_net_count=len(m['nets']))
(R/'evidence/r39_correction_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: historical R39-only correction and live endpoints; subsequent receiver split explicitly checked; values/crosswalk/photo/ERC retained.')
