"""Check review coverage, stale generated state, local links and source integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib, json, subprocess
from pypdf import PdfReader
from current_state import current_state, read, ROOT

s=current_state(); saved=read('evidence/completion_status.json')
assert s==saved, 'Generated status is stale; run refresh_review.ps1'
m=read('evidence/reconstruction.json'); work=read('evidence/remaining_work.json')
v=read('evidence/validation.json'); audit=read('evidence/completion_audit.json')
issues=work['issues']; ids=[i['id'] for i in issues]
assert len(ids)==len(set(ids))
for issue in issues:
    for key in ['known','unknown','next_action','closed_when']:
        assert issue[key].strip(), (issue['id'],key)
    assert issue['state']=='open'
covered={p for i in issues for p in i['open_pads']}
assert set(s['current_fitted_open_pads'])<=covered, 'A fitted open pad has no next action'
assert covered<=set(m['unresolved_pins']), 'Resolved/nonexistent pad still called open'
netnames={n['net'] for n in m['nets']}
assert {n for i in issues for n in i['nets']}<=netnames, 'Question register references a nonexistent net'
assert {'H_ANT_B','H_D1_FREE','H_BUTTON_MCU'}<={n for i in issues for n in i['nets']}
assert s['footprints']['unassigned']==audit['footprint_blank'] or set(s['footprints']['unassigned'])==set(audit['footprint_blank'])
assert set(s['footprints']['unassigned'])<=set(next(i for i in issues if i['id']=='M01')['refs'])
assert s['schematic_sha256']==v['schematic_sha256'], 'Native validation is stale'
assert s['unresolved_physical_pins']==audit['unresolved_physical_pins']==v['unresolved_physical_pins']
assert len(s['unknown_ceramic_values'])==audit['fitted_capacitors']-1
assert s['current_gpio_pins']==read('evidence/pic_gpio_status.json')['open_gpio_pins']==[]
assert s['modeled_nets']==83 and s['erc_total']==36
# Documentation cleanup must not alter the electrical source or any photo bytes.
prior=json.loads((ROOT/'docs/history/pre_cleanup_20261008/evidence/completion_status.json').read_text(encoding='utf-8'))
assert prior['unresolved_physical_pins']==s['unresolved_physical_pins']
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
for name in ['index.html','docs/FINISHING_CHECKLIST.html']:
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
for p in s['current_fitted_open_pads']:assert p in pdftext,p
for ref in s['unknown_ceramic_values']:assert ref in pdftext,ref
assert '0 open PIC pads' in ' '.join(pdftext.split())
assert 'No electrical measurements were supplied' not in (ROOT/'docs/MEASUREMENTS.md').read_text(encoding='utf-8')
report=dict(result='PASS',date=s['date'],schematic_revision=s['revision'],review_revision=s['review_revision'],
    schematic_sha256=s['schematic_sha256'],issue_groups=len(issues),fitted_open_pads_covered=len(covered),
    isolated_labels_covered=3,ceramic_values_listed=len(s['unknown_ceramic_values']),
    pdf_pages=len(reader.pages),current_html_links='PASS',current_html_javascript_syntax='PASS',
    browser_interaction='NOT_TESTED: prior file:// automation restriction retained',
    original_photo_hashes='PASS',electrical_contracts='See v099_verification.json')
(ROOT/'evidence/cleanup_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
