"""Protect measured evidence while checking the bounded original-photo correction."""
from pathlib import Path
import hashlib, json, subprocess
import xml.etree.ElementTree as ET
from inventory_contracts import without_withdrawn_r33, retained_crosswalk
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
record=read('evidence/architect_review_v0930.json');m=read('evidence/reconstruction.json')
baseline=json.loads(subprocess.check_output(['git','show',record['baseline_commit']+':evidence/reconstruction.json'],cwd=R,text=True,encoding='utf-8'))
actual={n['net']:sorted(n['endpoints']) for n in m['nets']}
before={n['net']:sorted(n['endpoints']) for n in baseline['nets']}
assert before==record['before'] and actual==without_withdrawn_r33(record['after'])
expected=dict(before)
expected['RF_MONITOR_PAD']=sorted(before['RF_MONITOR_PAD']+['R6.2','R7.1','D1.S'])
expected['H_RF_IN_A']=sorted((set(before['H_RF_IN_A'])-{'D1.S'})|{'D1.R'})
del expected['H_RF_CONTROL'];del expected['H_D1_FREE']
assert actual==without_withdrawn_r33(expected), 'Unreviewed change outside the RF correction and unsupported R33 withdrawal'
assert m['native_pin_crosswalk']==retained_crosswalk(baseline['native_pin_crosswalk']), 'Retained native pin mapping changed'
assert m['intentional_no_connects']==baseline['intentional_no_connects']
assert m['unresolved_pins']==baseline['unresolved_pins']
for path,digest in record['photos'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest
assert hashlib.sha256((R/record['review_file']).read_bytes()).hexdigest()==record['review_sha256']
xml=ET.parse(R/'output/PetSafe_netlist.xml');member={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
for group in [['U4.13','TP3.1','R10.1','R6.2','R7.1','D1.3'],['D1.2','R7.2','C9.1','U2.1'],['D1.1','R6.1','C8.1','U2.3']]:
 assert len({member[x] for x in group})==1,group
assert len({member['D1.'+str(n)] for n in [1,2,3]})==3
assert member['U106.1']==member['U4.8'] and member['U106.2']==member['J3.1'] and member['U106.3']==member['U6.2']
assert xml.find('./components/comp[@ref="U106"]/libsource').attrib['part']=='MCP1700x-330xxTT'
components={c['ref']:c for c in m['components']}
placements=read('evidence/library_placements.json')['components']
for ref in ['Q3','Q4','Q5','Q6','Q11','D1','R6','R7','TP3','Q8','C6','S1','LED1']:
 summary=components[ref]['current_summary']
 assert xml.findtext('./components/comp[@ref="'+ref+'"]/fields/field[@name="CurrentEvidence"]')==summary
 assert next(c for c in placements if c['reference']==ref)['properties']['CurrentEvidence']==summary
v=read('evidence/validation.json');assert v['erc_total']==1 and v['erc_by_type']=={'pin_to_pin':1}
assert len(read('evidence/power_source_declarations.json')['declarations'])==5
assert read('evidence/finalization_audit.json')['retained_pad_memberships_unchanged_from']=='ecd683d'
result=dict(result='PASS',revision=m['revision'],baseline_commit=record['baseline_commit'],bounded_rf_partition_change='PASS',retained_pad_partitions_unchanged='PASS',unsupported_r33_withdrawal='PASS',native_rf_paths='PASS',u6a_symbol_and_mapping_retained='PASS',review_file_and_photo_hashes='PASS',erc_total=v['erc_total'],power_declarations='Five existing supply paths; see power_source_declarations.json',nc_added=False,measurement_contracts='See live_evidence_verification.json')
(R/'evidence/architect_review_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
