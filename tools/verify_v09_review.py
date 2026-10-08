"""Check critical electrical separations and via-review provenance after export."""
from pathlib import Path
import json,hashlib,csv,xml.etree.ElementTree as ET
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
m=read('evidence/reconstruction.json');v=read('evidence/validation.json');a=read('evidence/via_audit.json');x=read('evidence/v09_net_changes.json')
native=ET.parse(R/'output/PetSafe_netlist.xml')
actual={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in native.findall('./nets/net') for n in net.findall('node')}
def net(ep):return actual[m['native_pin_crosswalk'].get(ep,ep)].removeprefix('/')
same=[['R37.1','R39.2'],['C27.1','U5.4'],['C27.2','U4.8'],['R1.1','U1.R1'],['C3.1','U1.R1'],['R2.1','U4.8'],['C4.1','U4.8'],['R10.2','U4.8'],['R32.1','U4.8'],['Q9.R','U4.8'],['U4.12','VREF.1']]
separate=[['U5.4','U5.1'],['U5.4','U4.8'],['U5.1','U4.8'],['R37.1','U5.1'],['R37.1','U4.8'],['Q8.B1','U4.8'],['Q8.B3','U4.8'],['R32.1','Q2.S'],['ANT1.1','U4.8'],['ANT2.1','U4.8']]
old=read('evidence/v08_verification.json')
for p in same+old['required_same_net_pairs']:assert net(p[0])==net(p[1]),p
for p in separate+old['required_separate_net_pairs']:assert net(p[0])!=net(p[1]),p
for c in x['changes']:assert net(c['endpoint'])==c['new'],c
request=read('evidence/pic_gpio_request.json')
gpio=sorted(int(e.split('.')[1]) for e in m['unresolved_pins'] if e.startswith('U4.'))
assert request['missing_gpio_pins']==gpio==[5,6,7,11,13,15,16,21]
assert len(request['all_pad_targets'])==28
assert sorted(int(r['pin']) for r in csv.DictReader((R/'evidence/PIC_GPIO_missing.csv').open()))==gpio
for im in request['source_photos']:assert sha(im['path'])==im['sha256']
sites={s['id']:s for s in a['sites']};assert len(sites)==127 and sum(s['active'] for s in sites.values())==126
assert not sites['V050']['active'] and sites['V025']['net']=='H_GND' and sites['V026']['endpoints']==['U4.21']
assert sites['V025']['review_status']!='CONFLICT'
assert {s['id'] for s in sites.values() if s['review_status']=='CONFLICT'}=={'V073','V113','V115'}
assert a['review_summary']['user_reported_ids']==98 and len(a['review_summary']['omitted_from_user_list'])==29
pdfs={'output/pdf/PetSafe_single_sheet.pdf':1,'output/pdf/PetSafe_completion_status.pdf':2,'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf':1}
for p,n in pdfs.items():assert len(PdfReader(R/p).pages)==n,(p,n)
assert sha('schematic/PetSafe_1001339.kicad_sch')==v['schematic_sha256']
report=dict(revision=m['revision'],result='PASS',native_schematic_sha256=v['schematic_sha256'],changed_endpoint_checks=len(x['changes']),
    required_same_net_pairs=same,required_separate_net_pairs=separate,retained_v08_contracts='PASS',
    via_summary=a['review_summary'],missing_gpio_pins=gpio,original_attachment_hashes='PASS',
    pdfs={p:dict(pages=n,sha256=sha(p)) for p,n in pdfs.items()},
    visual_review='PASS: latest schematic full page and modified power/PIC/PIR/bank regions; both status pages; all 28 PIC callouts.',
    html_review='Embedded JavaScript syntax checked with node --check; browser interaction not tested because file navigation was policy-denied earlier. No workaround used.',
    hardware_limit='Electrical assignments remain evidence-qualified; V073 and Q8 conflicts held. No new voltage or functional measurements.')
save('evidence/v09_verification.json',report)
save('evidence/pic_gpio_map_validation.json',dict(date='2026-10-08',revision=m['revision'],missing_gpio_count=len(gpio),
    pin_list_matches_native_netlist='PASS',original_photo_bytes_preserved='PASS',schematic_sha256=v['schematic_sha256'],
    pdf_sha256=sha('output/pdf/PetSafe_PIC_GPIO_pin_map.pdf'),png_sha256=sha('output/PetSafe_PIC_GPIO_pin_map.png'),
    visual_review='PASS: 28 real pad callouts, eight orange targets; V022/V023/V026 associations and RC1/VREF update shown.',
    warning='Eight GPIO onward destinations unresolved; five have no visible exit. No NC inferred. Local modeled nets can still have hidden or inferred continuations.'))
print('PASS: 28 revised native endpoints, critical net separations, retained v0.8 contracts, via corrections, GPIO lists, photo hashes and PDF page counts.')
