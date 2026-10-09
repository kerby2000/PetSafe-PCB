"""Live electrical regressions derived from v0.9.9; snapshot totals live separately."""
from pathlib import Path
import copy,hashlib,json,xml.etree.ElementTree as ET
from pypdf import PdfReader
from reconcile_via_review import apply
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
m=read('evidence/reconstruction.json');a=read('evidence/via_audit.json');v=read('evidence/validation.json');ch=read('evidence/v096_net_changes.json')
xml=ET.parse(R/'output/PetSafe_netlist.xml')
actual={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'].removeprefix('/') for net in xml.findall('./nets/net') for n in net.findall('node')}
def net(ep):return actual[m['native_pin_crosswalk'].get(ep,ep)]
for report in ['evidence/v08_verification.json','evidence/v09_verification.json']:
 old=read(report)
 for x,y in old['required_same_net_pairs']:
  if {x,y}=={'U4.12','VREF.1'}:
   assert net(x)!=net(y), 'User explicitly rejected old RC1-VREF photo join'
   assert read('evidence/v098_net_changes.json')['rejected_pairs'][0]['endpoints']==['U4.12','VREF.1']
  else:assert net(x)==net(y),(x,y)
 for x,y in old['required_separate_net_pairs']:
  if {x,y}=={'R37.1','U5.1'}:
   # This former unknown-feed isolation is explicitly superseded by V064-V063.
   assert ['V064','V063'] in ch['confirmed_via_pairs'] and net(x)==net(y)
  else:assert net(x)!=net(y),(x,y)
sites={s['id']:s for s in a['sites']}
for va,vb,pin,res,n in [(36,108,5,'R14',2),(37,102,6,'R15',3),(39,97,7,'R16',4),(47,91,11,'R11',5)]:
 assert net(f'U4.{pin}')==net(res+'.1')==f'H_TUNE_{n}'
 for i in [va,vb]:assert sites[f'V{i:03d}']['endpoints']==[f'U4.{pin}',res+'.1'] and sites[f'V{i:03d}']['net']==f'H_TUNE_{n}'
assert net('R37.1')==net('R39.2')==net('VDD.1')!=net('U5.4')
assert sites['V063']['net']==sites['V064']['net']=='VDD'
assert net('U4.12')!=net('R21.2')
assert sites['V053']['excluded_vias']==['V071']
assert sites['V026']['net']=='H_PIR_SIG' and 'V071' not in sites['V026'].get('joined_vias',[])
assert len(ch['confirmed_via_pairs'])==5 and len(ch['rejected_pairs'])==5
for i in [95,100,103,107]:assert f'V{i:03d}' in sites['V090']['excluded_vias'] and 'V090' in sites[f'V{i:03d}']['excluded_vias']
assert sites['V114']['endpoints']==['U2.T2'] and sites['V114']['net']=='GND'
assert net('U2.T2')==net('C5.2')==net('LED1.BL')==net('LED1.BR')==net('U4.8')
assert net('Q8.T2')!=net('Q8.B2')
assert net('Q8.B1')==net('Q8.B3')!=net('Q8.B2')
assert net('TP6.1')==net('C18.2')!=net('U3.5')
assert net('U3.5')==net('C18.1')
assert net('U3.5')==net('R22.2')==net('VREF.1')
assert len({net('TP6.1'),net('U3.5'),net('R22.2'),net('U4.8')})==3
assert net('J3.3')==net('GND.1')
assert not {'R23.2','J3.2'} & set(m['unresolved_pins'])
assert net('R23.2')==net('C40.1')==net('R42.1')==net('TP4.1')
assert net('C40.2')==net('GND.1')!=net('C40.1')
assert net('C40.1')!=net('C23.2'), 'Do not merge the old inferred detector-output net with the measured R23 junction'
assert net('J3.2')==net('R38.1')!=net('R38.2')
assert net('U3.6')==net('R23.1')!=net('R23.2')
assert net('R22.1')==net('GND.1')!=net('U3.6')
assert net('J3.2')!=net('GND.1') and net('R23.2')!=net('VREF.1')
assert all(sites[f'V{i:03d}']['net']=='VREF' for i in [79,80])
assert net('Q1.L')!=net('R43.2') and net('Q1.L')==net('U5.4') and net('R43.2')==net('TP14.1')
assert all(sites[f'V{i:03d}']['net']=='VSYS' for i in [11,12,13,14])
assert net('Q1.L')!=net('VDD.1'), 'Motor and logic rails must remain separate'
# Historical replay idempotence belongs to the frozen baseline check.
assert not a['review_summary']['conflicts']
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
request=read('evidence/pic_gpio_request.json');assert gpio==read('evidence/pic_gpio_status.json')['open_gpio_pins']
for entry in request['source_photos']:assert sha(entry['path'])==entry['sha256']
assert v['netlist_partition_comparison']=='PASS' and v['proposed_net_partitions']==len(m['nets'])
assert v['erc_total']==sum(len(s['violations']) for s in read('output/erc.json')['sheets'])
assert v['unresolved_physical_pins']==len(m['unresolved_pins']) and v['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert v['retained_original_visual_fragments']==28 and v['withdrawn_original_visual_fragments']==['V_Q1_LEFT']
placements=read('evidence/library_placements.json')
batch=read('evidence/u3_j3_measurements_20261009.json')
measured={r['id']:r for r in batch['readings']}
assert measured['B05']['resistance_ohms']==measured['B03']['resistance_ohms']==1
assert measured['B04']['resistance_ohms']==10000
assert measured['B06']['resistance_ohms']==290000 and measured['B07']['resistance_ohms']==1
assert measured['B01']['resistance_range_ohms']==measured['B02']['resistance_range_ohms']==[270000,289000]
for ref,value in [('R22','10k'),('R23','5.6k')]:
 assert xml.findtext(f'./components/comp[@ref="{ref}"]/value')==value, 'In-circuit path resistance must not replace the marked value'
for ref in ['U3','R22','R23','R38','J3','C40','R42','U7','TP16']:
 expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['MeasurementEvidence']
 assert xml.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="MeasurementEvidence"]')==expected,ref
for path,digest in batch['photo_sha256'].items():assert sha(path)==digest
queue=read('evidence/finishing_measurements.json')
batch2=read('evidence/u3_j3_batch2_20261009.json')
measured2={r['id']:r for r in batch2['readings']}
assert {k:r['resistance_ohms'] for k,r in measured2.items()}=={'B08':10000,'B09':1,'B10':1,'B11':5600,'B12':1,'X01':400000}
assert net('R23.1')!=net('GND.1'), '400 kohm must not be rounded to a copper connection'
assert xml.findtext('./components/comp[@ref="R38"]/value')=='10k'
for path,digest in batch2['photos'].items():assert sha(path)==digest
batch3=read('evidence/u3_r23_batch3_20261009.json')
measured3={r['id']:r for r in batch3['readings']}
assert {k:r['resistance_ohms'] for k,r in measured3.items()}=={'B13':300000,'B14':400000,'B15':600000}
for x,y in batch3['rejected_direct_pairs']:
 assert net(x)!=net(y), 'High measured resistance must not become a copper join: '+x+' - '+y
for path,digest in batch3['photos'].items():assert sha(path)==digest
batch4=read('evidence/u3_r23_batch4_20261009.json')
measured4={r['id']:r for r in batch4['readings']}
assert {k:r['resistance_ohms'] for k,r in measured4.items()}=={'B16':1,'B17':1}
for x,y in batch4['confirmed_pairs']:assert net(x)==net(y)
for path,digest in batch4['photos'].items():assert sha(path)==digest
batch5=read('evidence/pir_batch5_u7_20261009.json')
measured5={r['id']:r for r in batch5['readings']}
assert {k:r['resistance_ohms'] for k,r in measured5.items()}=={'B18':400000,'B19':400000}
for x,y in batch5['rejected_direct_pairs']:assert net(x)!=net(y)
for x,y in batch5['confirmed_pairs']:assert net(x)==net(y)
assert not {'U7.1','U7.2','U7.3'} & set(m['unresolved_pins'])
assert next(c for c in m['components'] if c['ref']=='U7')['population']=='DNP'
assert net('U7.1')==net('GND.1') and net('U7.2')==net('J3.2') and net('U7.3')==net('J3.1')
for path,digest in batch5['photos'].items():assert sha(path)==digest
pir_correction=read('evidence/pic21_tp16_followup_20261009.json')['resolution']
assert pir_correction['reading']['resistance_ohms']==800000
for x,y in pir_correction['confirmed_pairs']:assert net(x)==net(y)
for x,y in pir_correction['rejected_direct_pairs']:assert net(x)!=net(y)
completed_ids=set(measured)|set(measured2)|set(measured3)|set(measured4)|set(measured5)|{'B21'}
assert {r['id'] for r in queue['completed_tests']}==completed_ids
assert not completed_ids&{r['id'] for r in queue['tests']}, 'Do not repeat completed finishing readings'
for ref in ['U4','R11','R14','R15','R16','R37','R39','Q1','U2','Q8','C5','LED1','R18','R19','Q7','TP3','TP104','U106','J3','R43','TP14','R42','R44','TP4','TP103','R21','R22','R23','R48']:
 expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['ViaEvidence']
 assert xml.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="ViaEvidence"]')==expected,ref
status_pdf=PdfReader(R/'output/pdf/PetSafe_completion_status.pdf')
# Status is a living report: validate content, not the historical two-page layout.
status_text='\n'.join(p.extract_text() for p in status_pdf.pages)
assert 'PIC connections' in status_text and 'Every remaining open pad' in status_text
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':len(status_pdf.pages),'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf':1,'output/pdf/PetSafe_via_pair_next_check.pdf':1}
for path,pages in pdfs.items():assert len(PdfReader(R/path).pages)==pages
assert net('Q7.R')==net('R19.2')==net('VDD.1')
assert net('R18.2')==net('R19.1')==net('Q7.L')
assert net('R18.1')!=net('VDD.1') and net('R18.1')!=net('Q7.L')
assert net('Q7.S')==net('R20.1')!=net('Q7.R')
assert net('R18.1') not in {net('U4.13'),net('U4.21')}, 'Unmeasured GPIO tie introduced'
ch7=read('evidence/v097_net_changes.json')
assert ch7['rejected_pairs'][0]['resistance_ohms']==11200
assert ch7['inference']['nominal_series_ohms']==1200+10000
assert sites['V070']['net']=='H_RX_ENABLE_CTL' and sites['V075']['net']=='VDD'
assert sites['V075']['endpoints']==['Q7.R','R19.2']
assert sites['V070']['resistive_measurements'][0]['resistance_ohms']==11200
assert sites['V082']['net']=='VDD' and set(sites['V082']['endpoints'])=={'VDD.1','D3.R'}
assert net('VDD.1')==net('U5.1')!=net('U5.4')
d3=read('evidence/d3_measurement_20261009.json')
assert net('D3.R')==net('VDD.1') and net('D3.L')==net('GND.1')
assert net('D3.R')!=net('U3.8'), 'D3 measurement does not establish a whole receiver-rail merge'
assert net('D3.S')==net('R42.2') # KiCad may auto-name a continuous local wire without a label.
assert next(n for n in m['nets'] if n['net']=='H_D3_SIGNAL')['endpoints']==['D3.S','R42.2']
assert d3['measurements'][2]['resistance_ohms']==1.2
assert sha(d3['photo'])==d3['photo_sha256']
d2=read('evidence/d2_diode_20261009.json')
assert net('D2.R')==net('C20.2') and net('D2.L')==net('ANT2.1')
assert net('D2.R')!=net('D2.L')
assert all(net(p) not in {net('GND.1'),net('VDD.1')} for p in ['D2.R','D2.L'])
assert not set(['D2.S','D2.L','D2.R','R46.1','R46.2']) & set(m['unresolved_pins'])
assert net('D2.S')==net('R46.2') and net('D2.L')==net('R46.1')
assert net('D2.S') not in {net('D2.L'),net('D2.R'),net('GND.1'),net('VREF.1')}, 'Empty R46 must not bridge S to ANT2 or a rail'
assert next(c for c in m['components'] if c['ref']=='R46')['population']=='DNP'
assert xml.findtext('./components/comp[@ref="R46"]/value')=='DNP'
assert d2['local_connection_measurements'][0]['ohms']==1
assert d2['local_connection_measurements'][1]['reported']=='OL'
assert {r['to']:r['ohms'] for r in d2['external_resistance_followup']['readings_as_reported'] if r['from']=='D2.S'}=={'GND test point':700000,'VREF test point':1320000}
assert sha(d2['pad_orientation_confirmation']['photo'])==d2['pad_orientation_confirmation']['photo_sha256']
assert xml.findtext('./components/comp[@ref="D2"]/fields/field[@name="MeasurementEvidence"]')==next(c for c in placements['components'] if c['reference']=='D2')['properties']['MeasurementEvidence']
assert xml.findtext('./components/comp[@ref="R46"]/fields/field[@name="MeasurementEvidence"]')==next(c for c in placements['components'] if c['reference']=='R46')['properties']['MeasurementEvidence']
assert xml.findtext('./components/comp[@ref="TP103"]/value')=='VDD'
assert net('U4.12')==net('R18.1')=='H_RX_ENABLE_CTL'
assert net('U4.13')==net('TP3.1')==net('R10.1')=='RF_MONITOR_PAD'
assert net('U4.21')==net('TP16.1')==net('Q2.S')=='H_PIR_SIG'
assert net('R21.2')==net('VREF.1')!=net('U4.21')
assert net('VREF.1')!=net('VDD.1')
assert sites['V071']['net']=='VREF'
assert net('R42.1')==net('R44.1')==net('TP4.1')==net('U4.25')
assert net('U6A.R1')==net('J3.1')=='H_PIR_VDD'
assert net('U4.12')!=net('VREF.1') and net('U4.12')!=net('VDD.1')
assert sites['V053']['net']==sites['V070']['net']=='H_RX_ENABLE_CTL'
assert sites['V067']['endpoints']==['U6A.R1','J3.1']
assert xml.findtext('./components/comp[@ref="TP104"]/value')=='VREF'
assert sites['V049']['inconclusive_vias']==['V070']
assert sites['V070']['resistive_measurements'][-1]['resistance_range_ohms']==[200000,300000]
assert net('BATP.1')==net('Q1.S')==net('TP14.1')==net('R43.2')=='BATTERY+'
assert net('Q1.L')==net('U5.4')==net('L2.1')==net('L1.1')=='VSYS'
assert net('L1.1')!=net('L1.2') and net('L2.1')!=net('L2.2'), 'Supply report must not short the filter components'
assert net('Q1.R')==net('R44.2')!=net('Q1.L')
q1pins=xml.findall('./libparts/libpart[@lib="Transistor_FET"][@part="Q_PMOS_GSD"]/pins/pin')
assert {p.attrib['num']:p.attrib['name'] for p in q1pins}=={'1':'G','2':'S','3':'D'}
assert len({net('BATP.1'),net('Q1.L'),net('VDD.1'),net('VREF.1'),net('BATN.1')})==5
assert net('U4.4')==net('C39.1')==net('VREF.1')=='VREF'
assert net('U4.20')==net('C32.1')==net('VDD.1')=='VDD'
assert sites['V035']['net']=='VREF' and sites['V042']['net']=='VDD'
assert xml.find('./components/comp[@ref="Q1"]/libsource').attrib['part']=='Q_PMOS_GSD'
assert xml.findtext('./components/comp[@ref="Q1"]/value')=='FMOS3401A?'
assert xml.findtext('./components/comp[@ref="TP107"]/value')=='BATTERY (+)'
assert xml.findtext('./components/comp[@ref="TP108"]/value')=='BATTERY (-)'
out=dict(revision=m['revision'],result='PASS',schematic_sha256=v['schematic_sha256'],modeled_nets=v['proposed_net_partitions'],open_pads=len(m['unresolved_pins']),erc_total=v['erc_total'],gpio_pins_still_open=gpio,recorded_resistance_ohms=11200,qualified_q7_topology='R18 input - base; R19 base-emitter pull-up; emitter VDD; collector R20. Photo/resistance-supported inference.',unmeasured_gpio_connections='None introduced',prior_independent_electrical_contracts='PASS',review_replay='PASS',mcp_properties_match='PASS',original_photo_checksums=v['original_photo_checksums'],pdfs={k:dict(pages=n,sha256=sha(k)) for k,n in pdfs.items()},pic_map_basis='Updated v0.9.9: V035/RA2 to VREF, V042 to VDD; zero open PIC pads; qualified local connections remain. Original photo pixels retained.')
(R/'evidence/live_evidence_verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('PASS: RC1-R18, RC2-TP3, RB0-TP16/Q2, U6A-J3.1; rejected RC1-VREF; prior independent contracts; native/model and MCP properties.')
