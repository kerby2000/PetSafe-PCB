"""Check the new receiver grounds and distinguish Q8 centre pins from drains."""
from pathlib import Path
import copy,json,hashlib,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader
from reconcile_via_review import apply
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
m=read('evidence/reconstruction.json');v=read('evidence/validation.json');a=read('evidence/via_audit.json');changes=read('evidence/v092_net_changes.json')
native=ET.parse(R/'output/PetSafe_netlist.xml')
actual={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'].removeprefix('/') for net in native.findall('./nets/net') for n in net.findall('node')}
def net(ep):return actual[m['native_pin_crosswalk'].get(ep,ep)]
for report in ['evidence/v08_verification.json','evidence/v09_verification.json']:
    old=read(report)
    for x,y in old['required_same_net_pairs']:assert net(x)==net(y),(x,y)
    for x,y in old['required_separate_net_pairs']:assert net(x)!=net(y),(x,y)
for report in ['evidence/v09_net_changes.json','evidence/v091_net_changes.json','evidence/v092_net_changes.json']:
    for c in read(report)['changes']:assert net(c['endpoint'])==c['new'],c
assert net('C19.2')==net('R29.2')==net('U4.8')
assert net('R29.1')==net('U4.3')!=net('U4.8')
assert net('U3.5')==net('C18.1')!=net('U4.8')
assert net('R42.2')==net('D3.S')!=net('C19.2')
assert net('Q8.B2')==net('U4.8')
assert net('Q8.B1')==net('Q8.B3')!=net('Q8.B2')
assert net('Q8.T2')!=net('Q8.B2')
assert m['native_pin_crosswalk']['Q8.B2']=='Q8.5' and m['native_pin_crosswalk']['Q8.T2']=='Q8.2'
assert net('R42.1')==net('R44.1')!=net('ANT2.1')
assert net('Q1.L')==net('R43.2') and net('R22.2')=='H_RX_BIAS'
sites={s['id']:s for s in a['sites']}
assert len(sites)==127 and sum(s['active'] for s in sites.values())==120
assert {s['id'] for s in sites.values() if not s['active']}=={'V033','V050','V117','V120','V121','V122','V124'}
assert a['review_summary']['user_reported_ids']==111 and len(a['review_summary']['omitted_from_user_list'])==16
assert {s['id'] for s in sites.values() if s['review_status']=='CONFLICT'}=={'V114'}
assert sites['V114']['endpoints']==['Q8.T2'] and sites['V114']['net'] is None
for i in [113,115]:
    s=sites[f'V{i:03d}'];assert s['endpoints']==['Q8.B2'] and s['net']=='H_GND' and 'conflict' not in s
    assert set(s['excluded_endpoints'])=={'Q8.B1','Q8.B3'}
assert sites['V077']['endpoints']==['C19.2','R29.2'] and sites['V077']['net']=='H_GND'
assert sites['V075']['component_refs']==['Q7'] and not sites['V075']['endpoints'] and sites['V075']['net'] is None
for i,ref in [(91,'R11'),(97,'R16'),(102,'R15'),(108,'R14'),(78,'C17'),(83,'C40'),(112,'C8'),(118,'C7'),(119,'C9')]:
    assert sites[f'V{i:03d}']['endpoints']==[ref+('.1' if ref.startswith('R') else '.2')]
for i,ep in [(11,'R43.2'),(12,'R43.2'),(13,'R43.2'),(14,'R43.2'),(72,'R22.2')]:
    s=sites[f'V{i:03d}'];assert not s['net'] and not s['endpoints'] and ep in s['excluded_endpoints']
assert a==apply(copy.deepcopy(a)),'Via reconciliation must not revive withdrawn associations'
assert len(changes['corrected_via_ids'])==19 and len(changes['changes'])==2
placements=read('evidence/library_placements.json')
for ref in ['Q8','C19','R29','Q7','R11','R16','R15','R14','C17','C40','C8','C7','C9']:
    expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['ViaEvidence']
    assert native.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="ViaEvidence"]')==expected,ref
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
assert gpio==read('evidence/pic_gpio_request.json')['missing_gpio_pins']==[5,6,7,11,13,15,16,21]
assert v['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert v['netlist_partition_comparison']=='PASS' and v['proposed_net_partitions']==90 and v['erc_total']==55
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':2}
for p,pages in pdfs.items():assert len(PdfReader(R/p).pages)==pages
js=re.search(r'<script>(.*?)</script>',(R/'docs/VIA_REVIEW.html').read_text(encoding='utf-8'),re.S).group(1)
tmp=R/'.cache/v092/viewer.js';tmp.parent.mkdir(parents=True,exist_ok=True);tmp.write_text(js,encoding='utf-8')
subprocess.run(['node','--check',str(tmp)],check=True)
save('evidence/v092_verification.json',dict(revision=m['revision'],result='PASS',native_schematic_sha256=v['schematic_sha256'],corrected_sites=19,changed_endpoint_checks=2,
    prior_electrical_contracts='PASS',new_receiver_grounds='PASS',q8_ground_drain_supply_separation='PASS',reconciliation_idempotent='PASS',
    mcp_properties_match_placement_replay='PASS',via_summary=a['review_summary'],missing_gpio_pins=gpio,
    pdfs={p:dict(pages=n,sha256=sha(p)) for p,n in pdfs.items()},
    visual_review='PASS: latest schematic full page, receiver ground branches and Q8 note; both status pages.',
    html_review='Embedded JavaScript syntax PASS; browser interaction not tested (prior file navigation denied; no workaround).',
    hardware_limit='V077 GND is user-confirmed. Terminal selections qualified. V114 net and V075 Q7 terminal remain unresolved; no new numerical resistance supplied.'))
pv=read('evidence/pic_gpio_map_validation.json');pv.update(revision=m['revision'],schematic_sha256=v['schematic_sha256'],current_revision_check='GPIO destinations unchanged in v0.9.2; original v0.9 numbered map retained and missing-pin list cross-checked.')
assert pv['pdf_sha256']==sha('output/pdf/PetSafe_PIC_GPIO_pin_map.pdf')
save('evidence/pic_gpio_map_validation.json',pv)
print('PASS: V077 grounds, Q8 centre/drain separation, 19 site corrections, earlier net contracts, MCP metadata, PDF and JavaScript checks.')
