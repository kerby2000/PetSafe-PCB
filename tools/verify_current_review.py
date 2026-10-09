"""Check review coverage, stale generated state, local links and source integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib, json, subprocess
from pypdf import PdfReader
from current_state import current_state, validate_issue_register, read, ROOT
import xml.etree.ElementTree as ET

s=current_state(); saved=read('evidence/completion_status.json')
assert s==saved, 'Generated status is stale; run refresh_review.ps1'
m=read('evidence/reconstruction.json'); work=read('evidence/remaining_work.json')
v=read('evidence/validation.json'); audit=read('evidence/completion_audit.json')
issues,covered,isolated=validate_issue_register(m,work); ids=[i['id'] for i in issues]
assert s['footprints']['unassigned']==audit['footprint_blank'] or set(s['footprints']['unassigned'])==set(audit['footprint_blank'])
assert s['schematic_sha256']==v['schematic_sha256'], 'Native validation is stale'
assert s['unresolved_physical_pins']==audit['unresolved_physical_pins']==v['unresolved_physical_pins']
assert s['unknown_ceramic_values']==audit['unknown_ceramic_values']
assert s['current_gpio_pins']==read('evidence/pic_gpio_status.json')['open_gpio_pins']
assert s['modeled_nets']==len(m['nets'])
erc=read('output/erc.json'); findings=[i for sheet in erc['sheets'] for i in sheet['violations']]
assert s['erc_total']==len(findings)
# Verify physical J1 numbers separately from logical signal destinations.
mapping=read('evidence/j1_physical_mapping.json')['signal_to_native_pin']
xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
members={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
destinations={'VPP':'U4.1','VDD':'U4.20','GND':'U4.8','DAT':'U4.28','CLK':'U4.27'}
assert mapping=={'VPP':1,'VDD':2,'GND':3,'DAT':4,'CLK':5}
for name,pin in mapping.items():
    assert m['native_pin_crosswalk']['J1.'+name]=='J1.'+str(pin)
    assert read('evidence/pin_crosswalk.json')['J1.'+name]=='J1.'+str(pin)
    assert members['J1.'+str(pin)]==members[destinations[name]],name
for row in read('evidence/original_photo_manifest.json'):
    assert hashlib.sha256((ROOT/'photos/originals'/row['file']).read_bytes()).hexdigest()==row['sha256']
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.scripts=[];self.inscript=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ('href','src'):
            if a.get(key):self.links.append(a[key])
        if tag=='script':self.inscript=True
    def handle_endtag(self,tag):
        if tag=='script':self.inscript=False
    def handle_data(self,data):
        if self.inscript:self.scripts.append(data)
for name in ['index.html','docs/FINISHING_CHECKLIST.html','docs/VIA_REVIEW.html','docs/FINISHING_MEASUREMENTS.html']:
    path=ROOT/name; text=path.read_text(encoding='utf-8'); parser=Links();parser.feed(text)
    for link in parser.links:
        u=urlparse(link)
        if u.scheme or u.netloc or not u.path:continue
        assert (path.parent/unquote(u.path)).exists(), (name,link)
    for js in parser.scripts:
        result=subprocess.run(['node','--check'],input=js,text=True,capture_output=True)
        assert result.returncode==0,result.stderr
    assert '2 remaining PIC' not in text and 'v0.9 HOLD' not in text and 'Control origin unknown' not in text
checklist=(ROOT/'docs/FINISHING_CHECKLIST.html').read_text(encoding='utf-8')
for i in ids:assert f'id="{i}"' in checklist
reader=PdfReader(ROOT/'output/pdf/PetSafe_completion_status.pdf')
pdftext='\n'.join(p.extract_text() for p in reader.pages)
for i in ids:assert i+' -' in pdftext,i
for i in s['closed_items']:
    assert i['id']+' -' in pdftext, 'Closed issue missing from PDF history'
    assert i['resolution']['result'] in checklist, 'Closed issue result missing from HTML history'
for p in s['current_fitted_open_pads']:assert p in pdftext,p
for ref in s['unknown_ceramic_values']:assert ref in pdftext,ref
assert f'{len(s["current_gpio_pins"])} open PIC pads' in ' '.join(pdftext.split())
assert 'No electrical measurements were supplied' not in (ROOT/'docs/MEASUREMENTS.md').read_text(encoding='utf-8')
report=dict(result='PASS',date=s['date'],schematic_revision=s['revision'],review_revision=s['review_revision'],
    schematic_sha256=s['schematic_sha256'],issue_groups=len(issues),closed_issue_groups=len(s['closed_items']),fitted_open_pads_covered=len(covered),
    isolated_labels_covered=len(isolated),ceramic_values_listed=len(s['unknown_ceramic_values']),
    pdf_pages=len(reader.pages),current_html_links='PASS',current_html_javascript_syntax='PASS',
    browser_interaction='NOT_TESTED: prior file:// automation restriction retained',
    original_photo_hashes='PASS',electrical_contracts='See live_evidence_verification.json',j1_physical_numbering='PASS')
(ROOT/'evidence/current_review_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
