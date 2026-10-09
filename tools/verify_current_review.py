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
planned=[i for group in work['finish_plan'] for i in group['issues']]
assert sorted(planned)==sorted(ids), 'Finishing plan must cover each active issue once, without closed issues'
assert s['footprints']['unassigned']==audit['footprint_blank'] or set(s['footprints']['unassigned'])==set(audit['footprint_blank'])
assert s['schematic_sha256']==v['schematic_sha256'], 'Native validation is stale'
assert s['unresolved_physical_pins']==audit['unresolved_physical_pins']==v['unresolved_physical_pins']
assert s['unknown_ceramic_values']==audit['unknown_ceramic_values']
assert s['current_gpio_pins']==read('evidence/pic_gpio_status.json')['open_gpio_pins']
assert s['modeled_nets']==len(m['nets'])
assert 'PIC21' not in next(r for r in work['rails'] if r['name']=='VREF')['path'], 'Removed RB0/VREF assignment remains in the rail summary'
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
for name in ['index.html','docs/FINISHING_CHECKLIST.html','docs/VIA_REVIEW.html','docs/FINISHING_MEASUREMENTS.html','docs/RF_TRACE_REVIEW.html']:
    path=ROOT/name; text=path.read_text(encoding='utf-8'); parser=Links();parser.feed(text)
    for link in parser.links:
        u=urlparse(link)
        if u.scheme or u.netloc or not u.path:continue
        assert (path.parent/unquote(u.path)).exists(), (name,link)
    for js in parser.scripts:
        result=subprocess.run(['node','--check'],input=js,text=True,capture_output=True)
        assert result.returncode==0,result.stderr
    assert '2 remaining PIC' not in text and 'v0.9 HOLD' not in text and 'Control origin unknown' not in text
via_intro=(ROOT/'docs/VIA_REVIEW.html').read_text(encoding='utf-8').split('<script>')[0]
assert 'RB0/V026 to VREF.' not in via_intro and 'TP104, V026/PIC21' not in via_intro
checklist=(ROOT/'docs/FINISHING_CHECKLIST.html').read_text(encoding='utf-8')
for i in ids:assert f'id="{i}"' in checklist
measurements=read('evidence/finishing_measurements.json')
q8=read('evidence/q8_supply_result_20261009.json')
q8_test=q8['measurements'][0]
assert q8_test['id']=='B37' and q8_test['raw_user_statement']=='P-F 1Ohm'
assert q8_test['result']=='1 ohm' and q8_test['resistance_ohms']==1
assert q8_test['shorted_probe_ohms'] is None and q8_test['stability'] is None
assert q8_test['earlier_reading']=='10 ohm' and q8_test in measurements['completed_tests']
assert not any(t['id']=='B37' for t in measurements['tests']), 'Completed Q8 check re-entered queue'
assert members['Q8.2']==members['C6.1']==members['C5.1']
assert members['Q8.2']!=members['Q8.5'] and members['Q8.2']!=members['TP103.1']
for path,digest in q8['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
q3=read('evidence/q3_diode_results_20261009.json')
expected_diode={'B31':('QL','QR','2.3 V'),'B32':('QR','QL','OL'),'B33':('QL','QS','0.48 V'),'B34':('QS','QL','OL'),'B35':('QR','QS','OL'),'B36':('QS','QR','OL')}
for test_id,(red,black,result) in expected_diode.items():
    recorded=next(t for t in q3['measurements'] if t['id']==test_id)
    assert (recorded['from'],recorded['to'],recorded['result'])==(red,black,result)
    assert recorded in measurements['completed_tests']
    assert not any(t['id']==test_id for t in measurements['tests']), 'Completed test re-entered the queue'
assert next(t for t in q3['measurements'] if t['id']=='B33')['earlier_reading']=='0.35 V'
assert xml.find('./components/comp[@ref="R33"]') is None
assert not any(ep.startswith('R33.') for net in m['nets'] for ep in net['endpoints'])
assert members['J3.2']==members['R38.1']==members['U7.2']!=members['J3.1']
measurement_page=(ROOT/'docs/FINISHING_MEASUREMENTS.html').read_text(encoding='utf-8')
assert 'U6A is DNP' in measurement_page and 'U6A is 0' not in measurement_page, 'Population text replaced by numeric placeholder'
if not measurements['tests']:
    assert '<input ' not in measurement_page and '<textarea ' not in measurement_page, 'Completed queue still requests readings'
assert measurements['u6_annotation']['pending_check'] is None, 'Completed U6 pin5-pin2 check re-entered queue'
audit_rows={c['ref']:c for c in audit['components']}
assert '6.33' in audit_rows['C5']['value_or_identity'] and '16 mm' in audit_rows['C5']['value_or_identity']
assert 'pin5' in audit_rows['U6']['value_or_identity'].lower() and '1 ohm' in audit_rows['U6']['value_or_identity']
assert '1.4' in audit_rows['L1']['value_or_identity'] and '2.2' in audit_rows['L2']['value_or_identity']
assert 'TP9' not in audit_rows and 'R33' not in audit_rows, 'Removed unsupported entry has returned'
assert members['R41.1']==members['J1.1'] and members['U4.21']==members['TP16.1']!=members['TP104.1']
for name in ['index.html','docs/FINISHING_CHECKLIST.html','docs/FINISHING_MEASUREMENTS.html']:
    body=(ROOT/name).read_text(encoding='utf-8')
    for group in work['finish_plan']:
        assert group['title'] in body, (name,group['id'],'Missing shared finishing stage')
# Preserve source evidence while replacing obsolete current summaries.
cleanup=read('evidence/cleanup_v0929.json')
for name,expected in cleanup['archived_sha256'].items():
    assert hashlib.sha256((ROOT/cleanup['archived_root']/name).read_bytes()).hexdigest()==expected, name
previous=read(cleanup['archived_root']+'/evidence/finishing_measurements.json')
for key in ['completed_tests','cancelled_tests','photo_updates','photos']:
    assert all(entry in measurements[key] for entry in previous[key]), (key,'Cleanup altered recorded observations')
reader=PdfReader(ROOT/'output/pdf/PetSafe_completion_status.pdf')
pdftext='\n'.join(p.extract_text() for p in reader.pages)
for i in ids:assert i+' -' in pdftext,i
assert not s['closed_items'], 'Resolved groups belong in history, not the active register'
assert 'history/README.md' in checklist
archive=read('evidence/cleanup_v0931.json')
for name,digest in archive['archived_sha256'].items():
    assert hashlib.sha256((ROOT/archive['archived_root']/name).read_bytes()).hexdigest()==digest
assert 'Already resolved' not in checklist and 'Closed issues retained' not in checklist
for p in s['current_fitted_open_pads']:assert p in pdftext,p
for ref in s['unknown_ceramic_values']:assert ref in pdftext,ref
assert f'{len(s["current_gpio_pins"])} open PIC pads' in ' '.join(pdftext.split())
assert 'No electrical measurements were supplied' not in (ROOT/'docs/MEASUREMENTS.md').read_text(encoding='utf-8')
report=dict(result='PASS',date=s['date'],schematic_revision=s['revision'],review_revision=s['review_revision'],
    schematic_sha256=s['schematic_sha256'],issue_groups=len(issues),closed_issue_groups=len(s['closed_items']),fitted_open_pads_covered=len(covered),
    isolated_labels_covered=len(isolated),ceramic_values_listed=len(s['unknown_ceramic_values']),
    pdf_pages=len(reader.pages),current_html_links='PASS',current_html_javascript_syntax='PASS',
    browser_interaction='NOT_TESTED: file:// blocked by browser policy; HTML links, data and JavaScript checked statically',
    original_photo_hashes='PASS',electrical_contracts='See live_evidence_verification.json',j1_physical_numbering='PASS')
(ROOT/'evidence/current_review_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
