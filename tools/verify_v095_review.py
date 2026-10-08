"""Validate corrected U2/C5/LED grounds while preserving Q1 rail ambiguity and prior nets."""
from pathlib import Path
import copy, hashlib, json, re, subprocess, xml.etree.ElementTree as ET
from pypdf import PdfReader
from reconcile_via_review import apply
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def save(p,d):(R/p).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
m=read('evidence/reconstruction.json');a=read('evidence/via_audit.json');v=read('evidence/validation.json')
native=ET.parse(R/'output/PetSafe_netlist.xml')
actual={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'].removeprefix('/') for net in native.findall('./nets/net') for n in net.findall('node')}
def net(ep):return actual[m['native_pin_crosswalk'].get(ep,ep)]
for report in ['evidence/v08_verification.json','evidence/v09_verification.json']:
    old=read(report)
    for x,y in old['required_same_net_pairs']:assert net(x)==net(y),(x,y)
    for x,y in old['required_separate_net_pairs']:assert net(x)!=net(y),(x,y)
for report in ['evidence/v09_net_changes.json','evidence/v091_net_changes.json','evidence/v092_net_changes.json']:
    for c in read(report)['changes']:assert net(c['endpoint'])==c['new'],c
assert net('TP6.1')==net('C18.2')
assert net('U3.5')==net('C18.1')
# KiCad auto-names unlabeled local nets; compare their pad partitions and
# separately check the evidence-model names used by the via viewer.
membership={ep:n['net'] for n in m['nets'] for ep in n['endpoints']}
assert membership['TP6.1']==membership['C18.2']=='RX_A_FILTER'
assert membership['U3.5']==membership['C18.1']=='RX_B_PLUS'
assert len({net('TP6.1'),net('U3.5'),net('R22.2'),net('U4.8')})==4
assert net('C19.2')==net('R29.2')==net('Q8.B2')==net('U4.8')
assert net('R29.1')==net('U4.3')!=net('U4.8')
assert net('Q8.B1')==net('Q8.B3')!=net('Q8.B2')
assert net('Q8.T2')!=net('Q8.B2')
assert net('R42.1')==net('R44.1')!=net('ANT2.1')
assert net('Q1.L')!=net('R43.2')
assert {'Q1.L','R43.2'} <= set(m['unresolved_pins'])
assert net('U4.15')==net('U5.2')=='MOTOR_INA'
assert net('U4.16')==net('U5.3')=='MOTOR_INB'
assert net('U4.15')!=net('U4.16')
assert v['retained_original_visual_fragments']==28 and v['withdrawn_original_visual_fragments']==['V_Q1_LEFT']
sites={s['id']:s for s in a['sites']}
assert len(sites)==127 and sum(s['active'] for s in sites.values())==120
assert {s['id'] for s in sites.values() if not s['active']}=={'V033','V050','V117','V120','V121','V122','V124'}
assert a['review_summary']['user_reported_ids']==120
assert a['review_summary']['omitted_from_user_list']==['V027','V028','V030','V035','V038','V042','V053']
assert not a['review_summary']['conflicts']
assert not any(s['review_status']=='CONFLICT' for s in sites.values())
assert sites['V114']['endpoints']==['U2.T2'] and sites['V114']['net']=='H_GND'
assert sites['V114']['excluded_endpoints']==['Q8.T2']
assert net('U2.T2')==net('C5.2')==net('LED1.BL')==net('LED1.BR')==net('U4.8')
for i in [125,126]:assert sites[f'V{i:03d}']['endpoints']==['C5.2'] and sites[f'V{i:03d}']['net']=='H_GND'
assert sites['V127']['endpoints']==['LED1.BL','LED1.BR'] and sites['V127']['net']=='H_GND'
for i in [113,115]:assert sites[f'V{i:03d}']['endpoints']==['Q8.B2'] and sites[f'V{i:03d}']['net']=='H_GND'
assert sites['V075']['component_refs']==['Q7'] and not sites['V075']['endpoints']
assert sites['V077']['endpoints']==['C19.2','R29.2'] and sites['V077']['net']=='H_GND'
via_pins={36:5,37:6,39:7,47:11,49:13,26:21}
for i in [11,12,13,14]:
    s=sites[f'V{i:03d}'];assert s['endpoints']==['Q1.L'] and s['net'] is None and s['excluded_endpoints']==['R43.2']
assert all(sites[f'V{i:03d}']['reported_supply'].startswith('VDD') for i in [11,12,13,14])
assert sites['V015']['endpoints']==['R43.2'] and sites['V015']['net'] is None
for ids,ends,name in [([16,22],['U5.2','U4.15'],'MOTOR_INA'),([19,23],['U5.3','U4.16'],'MOTOR_INB')]:
    for i in ids:
        s=sites[f'V{i:03d}'];assert s['endpoints']==ends and s['net']==name and s['review_status']=='ASSIGNED'
for i,pin in via_pins.items():
    s=sites[f'V{i:03d}']
    assert s['endpoints']==[f'U4.{pin}'] and s['net'] is None
    assert s['user_reports'] and s['review_status']=='USER_REPORTED'
    assert not s.get('candidate_endpoints')
assert sites['V072']['endpoints']==['TP6.1'] and sites['V072']['net']=='RX_A_FILTER'
assert 'R22.2' in sites['V072']['excluded_endpoints']
for i in [79,80]:
    s=sites[f'V{i:03d}'];assert s['endpoints']==['U3.5'] and s['net']=='RX_B_PLUS' and s['user_reports']
assert a==apply(copy.deepcopy(a)),'Reconciliation revived a superseded association'
changes=read('evidence/v095_net_changes.json')
assert len(changes['corrected_via_ids'])==8 and len(changes['changes'])==2
for c in changes['changes']:
    if c['new'] is None:assert c['endpoint'] in m['unresolved_pins']
    else:assert net(c['endpoint'])==c['new']
placements=read('evidence/library_placements.json')
for ref in ['U4','U5','Q1','R43','U3','TP6','R22','Q8','C19','R29','U2','C5','LED1']:
    expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['ViaEvidence']
    assert native.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="ViaEvidence"]')==expected,ref
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
request=read('evidence/pic_gpio_request.json')
assert gpio==request['missing_gpio_pins']==[5,6,7,11,13,21]
assert {r['pin']:r['destination_reference'] for r in request['measurements']}=={p:f'V{i:03d}' for i,p in via_pins.items()}
for entry in request['source_photos']:assert sha(entry['path'])==entry['sha256']
assert v['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert v['netlist_partition_comparison']=='PASS' and v['proposed_net_partitions']==88 and v['erc_total']==50
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':2,'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf':1}
for p,pages in pdfs.items():assert len(PdfReader(R/p).pages)==pages
pic_text=' '.join(p.extract_text() for p in PdfReader(R/'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf').pages)
for i in via_pins:assert f'V{i:03d}; onward unknown' in pic_text
assert 'Hidden route or unused?' not in pic_text
js=re.search(r'<script>(.*?)</script>',(R/'docs/VIA_REVIEW.html').read_text(encoding='utf-8'),re.S).group(1)
tmp=R/'.cache/v095/viewer.js';tmp.parent.mkdir(parents=True,exist_ok=True);tmp.write_text(js,encoding='utf-8')
subprocess.run(['node','--check',str(tmp)],check=True)
save('evidence/v095_verification.json',dict(revision=m['revision'],result='PASS',native_schematic_sha256=v['schematic_sha256'],corrected_sites=8,changed_component_net_endpoints=2,confirmed_motor_control_pairs=[["U4.15","U5.2"],["U4.16","U5.3"]],withdrawn_original_fragment="V_Q1_LEFT",
    prior_electrical_contracts='PASS',receiver_filter_input_bias_ground_separation='PASS',q8_ground_drain_supply_separation='PASS',reconciliation_idempotent='PASS',
    mcp_properties_match_placement_replay='PASS',via_summary=a['review_summary'],missing_onward_gpio_destinations=gpio,
    pdfs={p:dict(pages=n,sha256=sha(p)) for p,n in pdfs.items()},
    visual_review='PASS: final single sheet, both status pages, numbered PIC photo map. Original source photographs preserved.',
    html_review='Embedded JavaScript syntax PASS; browser interaction not tested (prior file navigation denied; no workaround).',
    hardware_limit='PIC RC4/RC5 to motor INA/INB confirmed by user via reports; no numerical resistance supplied. Q1/R43 connection explicitly rejected. Q1 reported VDD but rail choice pending. V114 corrected to U2 ground; LED common selected from photo and grounded by user report.'))
pv=read('evidence/pic_gpio_map_validation.json')
pv.update(revision=m['revision'],missing_gpio_count=6,schematic_sha256=v['schematic_sha256'],pdf_sha256=sha('output/pdf/PetSafe_PIC_GPIO_pin_map.pdf'),png_sha256=sha('output/PetSafe_PIC_GPIO_pin_map.png'),
    current_revision_check='v0.9.5: map regenerated with six unresolved GPIOs; pins15/16 are now grey and map to motor INA/INB.',
    warning='Six GPIO onward destinations unresolved; each has an identified local via. PIC15/16 reach motor INA/INB. No NC inferred. Local modeled nets can still have inferred continuations.',
    visual_review='PASS: all 28 physical leads numbered; six orange GPIOs with their confirmed local via identifiers. Original source photographs preserved.')
save('evidence/pic_gpio_map_validation.json',pv)
print('PASS: U2/C5/LED ground corrections, pending Q1 rail choice, eight via cross-checks, prior independent nets, MCP metadata, photos, PDFs and HTML syntax.')
