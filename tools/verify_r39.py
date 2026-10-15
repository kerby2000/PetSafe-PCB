"""Bound the v0.9.45 R39 correction by physical memberships, not net counts."""
from pathlib import Path
import json, hashlib, subprocess, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
def read(path):return json.loads((R/path).read_text(encoding='utf-8'))
record=read('evidence/r39_endpoint_correction_v0945.json')
def baseline(path):return subprocess.check_output(['git','show',record['baseline_commit']+':'+path],cwd=R)
m=read('evidence/reconstruction.json');old=json.loads(baseline('evidence/reconstruction.json'))
def partitions(model,omit=()):
    return sorted(sorted(set(n['endpoints'])-set(omit)) for n in model['nets'] if set(n['endpoints'])-set(omit))
assert partitions(m,['R39.1'])==partitions(old,['R39.1']), 'Unexpected physical membership change outside R39.1'
assert m['native_pin_crosswalk']==old['native_pin_crosswalk']==read('evidence/pin_crosswalk.json')
def inventory(model):
    return {c['ref']:{k:c.get(k) for k in ['value','proposed_value','value_evidence','value_proposal','population','pins','library_symbol','footprint']} for c in model['components']}
assert inventory(m)==inventory(old),'Value, population, device symbol or physical inventory changed'
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
assert sorted(sorted(pads) for pads in native_physical.values())==partitions(old,['R39.1']), 'Exported physical partitions changed'
assert hashlib.sha256((R/record['photo']).read_bytes()).hexdigest()==record['photo_sha256']
def erc_types(data):return sorted(v['type'] for s in data['sheets'] for v in s['violations'])
assert erc_types(read('output/erc.json'))==erc_types(json.loads(baseline('output/erc.json')))
result=dict(result='PASS',revision=m['revision'],baseline_commit=record['baseline_commit'],moved_endpoint='R39.1',before='PIR_BASE',after='H_PIR_SIG',all_other_normalized_physical_partitions='IDENTICAL',native_endpoint_checks='PASS',values_population_symbols_crosswalk='UNCHANGED',photo_sha256='MATCH',erc_types='UNCHANGED',net_count_before=len(old['nets']),net_count_after=len(m['nets']))
(R/'evidence/r39_correction_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: only R39.1 moves; native physical memberships, values, crosswalk, photo and retained ERC checked.')
