"""Verify reported routes, negative evidence, and earlier independent contracts."""
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
 for x,y in old['required_same_net_pairs']:assert net(x)==net(y),(x,y)
 for x,y in old['required_separate_net_pairs']:
  if {x,y}=={'R37.1','U5.1'}:
   # This former unknown-feed isolation is explicitly superseded by V064-V063.
   assert ['V064','V063'] in ch['confirmed_via_pairs'] and net(x)==net(y)
  else:assert net(x)!=net(y),(x,y)
latest={}
for ver in ['09','091','092','094','095','096']:
 for c in read(f'evidence/v{ver}_net_changes.json')['changes']:latest[c['endpoint']]=c['new']
for ep,name in latest.items():
 if name is None:assert ep in m['unresolved_pins'],ep
 else:assert net(ep)==name,(ep,net(ep),name)
sites={s['id']:s for s in a['sites']}
for va,vb,pin,res,n in [(36,108,5,'R14',2),(37,102,6,'R15',3),(39,97,7,'R16',4),(47,91,11,'R11',5)]:
 assert net(f'U4.{pin}')==net(res+'.1')==f'H_TUNE_{n}'
 for i in [va,vb]:assert sites[f'V{i:03d}']['endpoints']==[f'U4.{pin}',res+'.1'] and sites[f'V{i:03d}']['net']==f'H_TUNE_{n}'
assert net('R37.1')==net('R39.2')==net('VDD.1')!=net('U5.4')
assert sites['V063']['net']==sites['V064']['net']=='H_VDD'
assert net('U4.12')!=net('R21.2')
assert sites['V053']['excluded_vias']==['V071']
assert len(ch['confirmed_via_pairs'])==5 and len(ch['rejected_pairs'])==5
for i in [95,100,103,107]:assert f'V{i:03d}' in sites['V090']['excluded_vias'] and 'V090' in sites[f'V{i:03d}']['excluded_vias']
assert sites['V114']['endpoints']==['U2.T2'] and sites['V114']['net']=='H_GND'
assert net('U2.T2')==net('C5.2')==net('LED1.BL')==net('LED1.BR')==net('U4.8')
assert net('Q8.T2')!=net('Q8.B2')
assert net('Q8.B1')==net('Q8.B3')!=net('Q8.B2')
assert net('TP6.1')==net('C18.2')!=net('U3.5')
assert net('U3.5')==net('C18.1')
assert len({net('TP6.1'),net('U3.5'),net('R22.2'),net('U4.8')})==4
assert net('Q1.L')!=net('R43.2') and {'Q1.L','R43.2'}<=set(m['unresolved_pins'])
assert all(sites[f'V{i:03d}']['net'] is None for i in [11,12,13,14]), 'Unanswered VDD rail question must not merge rails'
assert a==apply(copy.deepcopy(a)), 'Review replay revived old evidence'
assert not a['review_summary']['conflicts']
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
request=read('evidence/pic_gpio_request.json');assert gpio==request['missing_gpio_pins']==[13,21]
for entry in request['source_photos']:assert sha(entry['path'])==entry['sha256']
assert v['netlist_partition_comparison']=='PASS' and v['proposed_net_partitions']==87 and v['erc_total']==42
assert v['unresolved_physical_pins']==33 and v['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert v['retained_original_visual_fragments']==28 and v['withdrawn_original_visual_fragments']==['V_Q1_LEFT']
placements=read('evidence/library_placements.json')
for ref in ['U4','R11','R14','R15','R16','R37','R39','Q1','U2','Q8','C5','LED1']:
 expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['ViaEvidence']
 assert xml.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="ViaEvidence"]')==expected,ref
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':2,'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf':1}
for path,pages in pdfs.items():assert len(PdfReader(R/path).pages)==pages
out=dict(revision=m['revision'],result='PASS',schematic_sha256=v['schematic_sha256'],confirmed_pairs=ch['confirmed_via_pairs'],rejected_pairs=ch['rejected_pairs'],gpio_pins_still_open=gpio,modeled_nets=87,open_pads=33,erc_total=42,original_photo_checksums=v['original_photo_checksums'],prior_independent_electrical_contracts='PASS',review_replay='PASS',mcp_properties_match='PASS',pdfs={k:dict(pages=n,sha256=sha(k)) for k,n in pdfs.items()},pending='Q1.L reported VDD; regulated versus motor rail not yet answered. No numerical ohms supplied for positive pairs.',browser_interaction='NOT_TESTED')
(R/'evidence/v096_verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
pv=read('evidence/pic_gpio_map_validation.json');pv.update(revision=m['revision'],missing_gpio_count=2,schematic_sha256=v['schematic_sha256'],pdf_sha256=sha('output/pdf/PetSafe_PIC_GPIO_pin_map.pdf'),png_sha256=sha('output/PetSafe_PIC_GPIO_pin_map.png'),current_revision_check='v0.9.6: only RC2/pin13 and RB0/pin21 remain highlighted.',warning='Local or inferred nets may still lack remote connections; no NC assumed.',visual_review='PASS: all 28 physical leads numbered; only RC2/13 and RB0/21 orange. Original photographs preserved.')
(R/'evidence/pic_gpio_map_validation.json').write_text(json.dumps(pv,indent=2)+'\n',encoding='utf-8')
print('PASS: five positive via pairs, five rejected pairs, two remaining GPIOs, native/model consistency and prior independent connections.')
