"""Verify the incremental via corrections against the exported KiCad netlist."""
from pathlib import Path
import copy,json,hashlib,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader
from reconcile_via_review import apply
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
m=read('evidence/reconstruction.json');v=read('evidence/validation.json');a=read('evidence/via_audit.json');changes=read('evidence/v091_net_changes.json')
native=ET.parse(R/'output/PetSafe_netlist.xml')
actual={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'].removeprefix('/') for net in native.findall('./nets/net') for n in net.findall('node')}
def net(ep):return actual[m['native_pin_crosswalk'].get(ep,ep)]
for report in ['evidence/v08_verification.json','evidence/v09_verification.json']:
    old=read(report)
    for x,y in old['required_same_net_pairs']:assert net(x)==net(y),(x,y)
    for x,y in old['required_separate_net_pairs']:assert net(x)!=net(y),(x,y)
for c in read('evidence/v09_net_changes.json')['changes']+changes['changes']:assert net(c['endpoint'])==c['new'],c
assert net('R42.1')==net('R44.1')=='V017_CONTROL'
assert net('R42.1')!=net('ANT2.1')
assert net('Q1.L')==net('R43.2')
assert net('R22.2')=='H_RX_BIAS'
assert net('R19.2')!=net('U4.8')
sites={s['id']:s for s in a['sites']}
assert len(sites)==127 and sum(s['active'] for s in sites.values())==125
assert {s['id'] for s in sites.values() if not s['active']}=={'V033','V050'}
assert a['review_summary']['user_reported_ids']==101
assert len(a['review_summary']['omitted_from_user_list'])==26
assert {s['id'] for s in sites.values() if s['review_status']=='CONFLICT'}=={'V113','V115'}
assert sites['V073']['net']=='H_GND' and sites['V073']['endpoints']==[] and 'conflict' not in sites['V073']
for i,ep in [(11,'R43.2'),(12,'R43.2'),(13,'R43.2'),(14,'R43.2'),(72,'R22.2')]:
    s=sites[f'V{i:03d}'];assert not s['net'] and not s['endpoints'] and not s['modeled_nets'] and ep in s['excluded_endpoints']
expected={6:['C33.2'],7:['C34.2'],15:['R43.2','Q1.L'],17:['R42.1','R44.1'],18:['C35.2'],20:['R40.1'],29:['C25.2','C26.2'],34:['R3.1'],40:['C28.2'],59:['L2.1'],60:['Q2.L'],61:['L2.1'],65:['C2.2'],68:['C37.2','C36.2']}
for i,eps in expected.items():
    s=sites[f'V{i:03d}'];assert s['endpoints']==eps,(i,s['endpoints'])
    modeled={e:n['net'] for n in m['nets'] for e in n['endpoints']}
    assert all(modeled[ep]==s['net'] for ep in eps),(i,s['net'])
    assert len({net(ep) for ep in eps})==1,(i,eps)
assert a==apply(copy.deepcopy(a)),'Via reconciliation must be repeatable without stale annotations'
assert len(changes['corrected_via_ids'])==21 and len(changes['changes'])==2
placements=read('evidence/library_placements.json')
for ref in ['R42','R44','R43','R22']:
    expected=next(c for c in placements['components'] if c['reference']==ref)['properties']['ViaEvidence']
    assert native.findtext(f'./components/comp[@ref="{ref}"]/fields/field[@name="ViaEvidence"]')==expected
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
assert gpio==read('evidence/pic_gpio_request.json')['missing_gpio_pins']==[5,6,7,11,13,15,16,21]
assert v['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert v['netlist_partition_comparison']=='PASS' and v['proposed_net_partitions']==90 and v['erc_total']==55
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':2}
for p,pages in pdfs.items():assert len(PdfReader(R/p).pages)==pages
js=re.search(r'<script>(.*?)</script>',(R/'docs/VIA_REVIEW.html').read_text(encoding='utf-8'),re.S).group(1)
tmp=R/'.cache/v091/viewer.js';tmp.parent.mkdir(parents=True,exist_ok=True);tmp.write_text(js,encoding='utf-8')
subprocess.run(['node','--check',str(tmp)],check=True)
save('evidence/v091_verification.json',dict(revision=m['revision'],result='PASS',native_schematic_sha256=v['schematic_sha256'],corrected_sites=21,changed_endpoint_checks=2,
    prior_v08_v09_electrical_contracts='PASS',corrected_component_via_associations='PASS',negative_associations_removed='PASS',reconciliation_idempotent='PASS',
    mcp_properties_match_placement_replay='PASS',via_summary=a['review_summary'],missing_gpio_pins=gpio,
    pdfs={p:dict(pages=n,sha256=sha(p)) for p,n in pdfs.items()},
    visual_review='PASS: rendered latest one-page schematic and both status pages; enlarged R42/R44 label spacing inspected.',
    html_review='Embedded JavaScript syntax PASS; browser interaction not tested (prior file navigation denied; no workaround).',
    hardware_limit='User reports and photo-selected pads; no new resistance or functional measurements. V113/V115 held for later review.'))
pv=read('evidence/pic_gpio_map_validation.json');pv.update(revision=m['revision'],schematic_sha256=v['schematic_sha256'],current_revision_check='GPIO destinations unchanged in v0.9.1; original v0.9 numbered map retained and missing-pin list cross-checked.')
assert pv['pdf_sha256']==sha('output/pdf/PetSafe_PIC_GPIO_pin_map.pdf')
save('evidence/pic_gpio_map_validation.json',pv)
print('PASS: 21-site corrections, V017 native connection, preserved prior net contracts, via overlay, MCP metadata, unchanged GPIO map and PDF/JS checks.')
