from verify_capacitor_application import matches_text_digest
"""Check review coverage, stale generated state, local links and source integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib, json, subprocess, math
from pypdf import PdfReader
from current_state import current_state, validate_issue_register, read, ROOT
import xml.etree.ElementTree as ET
from inventory_contracts import with_r39_output_pullup, with_receiver_input_split

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
# E06 is a documented limitation, never a claim that absent hidden copper was proved.
consistency=read('evidence/circuit_consistency_v0942.json')
assert consistency['electrical_change'] is False and consistency['new_measurements']==['B83']
assert consistency['followup_measurements']==['B84','B85']
assert next(f for f in consistency['findings'] if f['id']=='C01')['status']=='RESOLVED_BY_RECHECK'
assert all(f['id']!='C01' for f in work['consistency_review']['findings'])
assert 'E09' in ids, 'Resolving one reading conflict must not falsely close Q1 behavior'
assert {n['net']:sorted(n['endpoints']) for n in m['nets']}==with_receiver_input_split(with_r39_output_pullup(consistency['unchanged_net_partitions']))
assert set(next(n['endpoints'] for n in m['nets'] if n['net']=='Q1_GATE'))=={'Q1.R','R44.2'}
for ref,value in [('R44','15k'),('R26','120k'),('R24','120k'),('R21','10k'),('R22','10k')]:
    assert next(c for c in m['components'] if c['ref']==ref)['value']==value
epnet={e:n['net'] for n in m['nets'] for e in n['endpoints']}
for group in [['U3.1','R26.1'],['U3.2','R26.2'],['U3.7','R24.1'],['U3.6','R24.2'],['TP5.1','R21.1'],['R21.2','R22.2','VREF.1'],['R22.1','U3.4']]:
    assert len({epnet[e] for e in group})==1
assert epnet['U3.1']!=epnet['U3.2'] and epnet['U3.7']!=epnet['U3.6']
assert next(c for c in m['components'] if c['ref']=='D6')['proposed_value']=='G3 / Vbr TBD'
e06=read('evidence/e06_disposition_v0941.json')
assert e06['electrical_change'] is False and e06['new_measurements']==[]
assert {n['net']:sorted(n['endpoints']) for n in m['nets']}==with_receiver_input_split(with_r39_output_pullup(e06['unchanged_net_partitions']))
assert 'E06' not in ids and 'E06' not in planned
limitation=next(i for i in work['reconstruction_limitations'] if i['id']=='E06')
assert limitation['disposition']=='Drawing resolved; physical completeness unproved'
assert 'test-only use is not asserted' in limitation['unknown']
for path,digest in {**e06['photos'],**e06['archived_sha256']}.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
pin_audit=read('evidence/pic_trace_audit.json')
assert pin_audit['revision']==m['revision'] and pin_audit['open_gpio_pins']==[]
erc=read('output/erc.json'); findings=[i for sheet in erc['sheets'] for i in sheet['violations']]
assert s['erc_total']==len(findings)
# Verify physical J1 numbers separately from logical signal destinations.
mapping=read('evidence/j1_physical_mapping.json')['signal_to_native_pin']
xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
members={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
for branch in e06['retained_branches']:
    endpoint_set=set(branch['endpoints'])
    netname=members[next(iter(endpoint_set))]
    assert {e for e,n in members.items() if n==netname}==endpoint_set
assert members['U4.17']==members['R13.1']!=members['U4.18']
for pin in pin_audit['pins']:
    model_net=next(n for n in m['nets'] if n['net']==pin['net'])
    expected={m['native_pin_crosswalk'].get(e,e) for e in model_net['endpoints']}
    native_net=members['U4.'+str(pin['pin'])]
    actual={e for e,n in members.items() if n==native_net and not e.startswith('#FLG')}
    assert actual==expected, (pin['pin'], actual, expected)
for ref in ['TP11','TP17']:
    summary=next(c for c in m['components'] if c['ref']==ref)['current_summary']
    assert xml.findtext('./components/comp[@ref="'+ref+'"]/fields/field[@name="CurrentEvidence"]')==summary
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
for name in ['index.html','docs/FINISHING_CHECKLIST.html','docs/VIA_REVIEW.html','docs/FINISHING_MEASUREMENTS.html','docs/RF_TRACE_REVIEW.html','docs/CAPACITOR_VALUE_REVIEW.html']:
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
cap_review=read('evidence/capacitor_value_review_20261015.json')
assert {r['ref'] for r in cap_review['components']}==set(s['unknown_ceramic_values'])
assert len(cap_review['components'])==44 and len({r['ref'] for r in cap_review['components']})==44
assert matches_text_digest((ROOT/'schematic/PetSafe_1001339.kicad_sch').read_bytes(), cap_review['source_schematic_sha256'])
assert matches_text_digest((ROOT/'evidence/reconstruction.json').read_bytes(), cap_review['source_model_sha256'])
assert cap_review['electrical_change'] is True and cap_review['topology_change'] is False and cap_review['individual_values_closed']==[]
assert all(r['applied_to_native'] and r['native_value']==r['proposal'].replace(' ','')+'*' for r in cap_review['components'])
assert all(r['selection_pf']>0 and r['voltage_rating_v']>0 and r['dielectric'] and r['confidence'] for r in cap_review['components'])
assert {r['ref'] for r in cap_review['known_capacitors']}=={'C5'}
assert {r['ref'] for r in cap_review['unpopulated_capacitors']}=={c['ref'] for c in m['components'] if c['kind']=='C' and c['population']=='DNP'}
assert len(cap_review['components'])+len(cap_review['known_capacitors'])+len(cap_review['unpopulated_capacitors'])==51
bank=cap_review['antenna_design_example']
assert bank['status']=='DELIBERATE_DESIGN_SEED_NOT_RECOVERED_VALUES'
assert bank['design_inductance_uh']==500 and bank['target_hz']==134200
assert read(bank['measurement_source'])['inductance_uh']==500
cap_by_ref={c['ref']:c for c in cap_review['components']}
model_net={ep:n['net'] for n in m['nets'] for ep in n['endpoints']}
for branch in bank['branches']:
    # Qualify the ideal-switch equation against the actual traced three-cap network.
    ca,cg,cs=(branch[k] for k in ['antenna_cap','ground_cap','switched_cap'])
    midpoint='TUNE_'+str(branch['branch'])+'_MID'
    assert {model_net[ca+'.1'],model_net[ca+'.2']}=={'H_ANT_B',midpoint}
    assert {model_net[cg+'.1'],model_net[cg+'.2']}=={'GND',midpoint}
    assert {model_net[cs+'.1'],model_net[cs+'.2']}=={'TUNE_'+str(branch['branch'])+'_SW',midpoint}
    assert model_net[branch['switch']+'.S']=='TUNE_'+str(branch['branch'])+'_SW'
    assert model_net[branch['switch']+'.L']=='GND'
    for ref,key in [(ca,'antenna_pf'),(cg,'ground_pf'),(cs,'switched_pf')]: assert cap_by_ref[ref]['selection_pf']==branch[key]
assert [s['mask'] for s in bank['states']]==list(range(32))
for state in bank['states']:
    ceq=0
    for i,branch in enumerate(bank['branches']):
        ca=branch['antenna_pf']; grounded=branch['ground_pf']+(branch['switched_pf'] if state['mask']&(1<<i) else 0)
        ceq+=1/(1/ca+1/grounded)
    assert math.isclose(ceq,state['equivalent_pf'],rel_tol=1e-12)
    assert math.isclose(1/(2*math.pi*math.sqrt(500e-6*ceq*1e-12))/1000,state['frequency_khz'],rel_tol=1e-12)
assert bank['nearest_state']==min(bank['states'],key=lambda s:abs(s['frequency_khz']-134.2))
cap_results=read('evidence/receiver_capacitance_results_20261015.json')
assert [t['capacitance_pf'] for t in cap_results['measurements']]==[680,340,240,680,320,240]
assert all(t['capacitance_model'] is None and t['dissipation_factor'] is None for t in cap_results['measurements'])
assert all(t in measurements['completed_tests'] for t in cap_results['measurements'])
for src in cap_results['sources']:
    assert hashlib.sha256((ROOT/src['file']).read_bytes()).hexdigest()==src['sha256']
ra0=read('evidence/ra0_tp6_connection_v0938.json')
b59=ra0['measurement']
assert (b59['id'],b59['from'],b59['to'],b59['resistance_ohms'])==('B59','A0','T6',1.5)
assert b59['shorted_probe_ohms'] is None and b59['stability'] is None
assert b59 in measurements['completed_tests'] and all(t['id']!='B59' for t in measurements['tests'])
assert len({members[e] for e in ['C25.1','U4.2','TP6.1','R27.1','C18.2']})==1
assert len({members[e] for e in ['TP6.1','U3.1','C18.1','C25.2','C26.1']})==5
assert members['U3.1']==members['R27.2']
assert 'PIC_RA0_FILTER' not in {n['net'] for n in m['nets']}
assert members['C20.2']==members['D2.2']==members['R28.2']!=members['U3.3']
assert members['C20.2']!=members['TP7.1']
for site in read('evidence/via_audit.json')['sites']:
    if site['id'] in {'V031','V072'}:
        assert site['net']=='RX_A_FILTER' and site['joined_vias']==['V031','V072']
for path,digest in ra0['source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
supply=read('evidence/supply_baseline_results_20261014.json')
assert supply['electrical_change'] is False
assert supply['measurements'][0]['native_endpoint']=='TP14.1'
assert 'DISPUTED' in supply['measurements'][0]['net_assignment_status']
assert all(r in measurements['completed_tests'] for r in supply['measurements'])
assert not {r['id'] for r in supply['measurements']}&{r['id'] for r in measurements['tests']}
tp14=read('evidence/tp14_motor_output_correction_v0939.json')
assert tp14['measured_pair']==['TP14.1','U5.8'] and tp14['measured_ohms']==1.5
assert tp14['measurement'] in measurements['completed_tests']
assert members['TP14.1']==members['R43.2']==members['U5.8']==members['J5.1']
assert len({members[e] for e in ['TP14.1','Q1.1','Q1.2','Q1.3','U4.8']})==5
assert next(s for s in read('evidence/via_audit.json')['sites'] if s['id']=='V015')['net']=='H_MOTOR_A'
rx=read('evidence/receiver_supply_results_20261014.json')
assert rx['electrical_change'] is False and rx['measurements'][0] in measurements['completed_tests']
assert members['TP5.1']==members['U3.8']==members['R20.2']
assert len({members[e] for e in ['TP5.1','R19.1','R19.2','U4.8']})==4
for path,digest in rx['photo_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
q7_voltage=read('evidence/q7_r19_voltage_results_20261014.json')
assert q7_voltage['status']=='Q7_R19_JOINS_CONFIRMED_DEVICE_BEHAVIOR_OPEN'
q7_joins=read('evidence/q7_r19_join_results_20261014.json')
assert q7_joins['electrical_change'] is False
assert all(row in measurements['completed_tests'] for row in q7_joins['measurements'])
assert members['Q7.1']==members['R19.1'] and members['Q7.2']==members['R19.2']
assert not q7_voltage['contested_pairs']
assert all(r in measurements['completed_tests'] for r in q7_voltage['measurements'])
for path,digest in q7_voltage['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
q7_diode=read('evidence/q7_diode_results_20261014.json')
assert q7_diode['electrical_change'] is False
assert all(row in measurements['completed_tests'] for row in q7_diode['measurements'])
assert hashlib.sha256((ROOT/'photos/originals/IMG_2434.jpg').read_bytes()).hexdigest()==q7_diode['photo_sha256']
manual=read('evidence/product_manual_led_review_20261014.json')
assert manual['model']=='PPA19-16811'
pack=manual['model_evidence'];assert hashlib.sha256((ROOT/pack['file']).read_bytes()).hexdigest()==pack['sha256']
antenna=read('evidence/antenna_outer_rail_results_20261014.json')
outer=read('evidence/antenna_outer_rail_correction_v0937.json')
assert antenna['status']=='C11_ANT2_CONNECTION_SUPPORTED'
by_id={t['id']:t for t in antenna['measurements']}
assert (by_id['B50']['from'],by_id['B50']['to'],by_id['B50']['resistance_ohms'])==('B','G',414000)
assert by_id['B50']['from_original_request']=='N' and by_id['B50']['to_original_request']=='B'
assert (by_id['B52']['from'],by_id['B52']['to'],by_id['B52']['resistance_ohms'])==('N','B',1.4)
for row in antenna['measurements']:
    assert row in measurements['completed_tests']
    assert not any(t['id']==row['id'] for t in measurements['tests'])
ant1=members['TP105.1'];ant2=members['TP106.1'];ground=members['U4.8']
assert len({ant1,ant2,ground})==3, 'Do not merge antenna terminals or ground through the fitted loop'
for front,rear in [('C11','C12'),('C14','C15'),('C29','C38'),('C44','C45'),('C47','C48')]:
    assert members[front+'.1']==ant2 and members[rear+'.1']==ground
    assert members[front+'.2']==members[rear+'.2'] not in {ant1,ant2,ground}
for site in read('evidence/via_audit.json')['sites']:
    if site['id'] in {'V087','V088'}:
        assert site['net']=='GND' and site['endpoints']==[]
for path,digest in outer['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
led=read('evidence/led1_colour_results_20261009.json')
for test_id,red,colour,pin,resistor in [('B42','A','green','2','R31'),('B43','B','red','1','R30')]:
    recorded=next(t for t in led['measurements'] if t['id']==test_id)
    assert (recorded['from'],recorded['to'],recorded['colour'])==(red,'K',colour)
    assert recorded in measurements['completed_tests']
    assert not any(t['id']==test_id for t in measurements['tests']), 'Completed LED colour test re-entered queue'
    assert members['LED1.'+pin]==members[resistor+'.2']
assert members['R30.1']==members['U4.23']!=members['R31.1']==members['U4.22']
assert members['LED1.3']==members['LED1.4']==members['U4.8']
assert xml.findtext('./components/comp[@ref="LED1"]/fields/field[@name="ColourMapping"]')=='Native pin1 / R30 / PIC23 = RED; native pin2 / R31 / PIC22 = GREEN'
j5=read('evidence/j5_photo_review_20261009.json')
assert not any(i['id']=='I02' for i in work['issues'])
assert j5['closed_issue']['state']=='closed' and j5['electrical_change'] is False
assert members['J5.1']==members['U5.8']!=members['J5.2']==members['U5.5']==members['TP15.1']
assert next(c for c in m['components'] if c['ref']=='J5')['side']=='back'
for path,digest in j5['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
for path,digest in led['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
s1=read('evidence/s1_contact_results_20261009.json')
expected_s1={'B38':('A','B','Released','1 ohm'),'B39':('C','D','Released','1 ohm'),
             'B40':('B','D','Released','OL'),'B41':('B','D','Held pressed','1 ohm'),
             'X02':('A','C','Not separately stated','OL')}
for test_id,expected in expected_s1.items():
    recorded=next(t for t in s1['measurements'] if t['id']==test_id)
    assert tuple(recorded[k] for k in ['from','to','state','result'])==expected
    assert recorded in measurements['completed_tests']
    assert not any(t['id']==test_id for t in measurements['tests'])
assert s1['closed_issue']['id']=='E05' and s1['closed_issue']['state']=='closed'
assert s1['closed_issue']['resolution']['evidence']==['evidence/s1_contact_results_20261009.json']
assert not any(i['id']=='E05' for i in work['issues']), 'Closed S1 issue still in active register'
assert members['S1.1']==members['C35.2']!=members['S1.2']==members['R41.2']
for path,digest in s1['photos'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
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
    assert '<input ' not in measurement_page, 'Completed queue still requests readings'
    assert '<textarea id="reply" aria-label="Results to share" readonly>' in measurement_page, 'Completed results export must remain read-only'
assert measurements['u6_annotation']['pending_check'] is None, 'Completed U6 pin5-pin2 check re-entered queue'
audit_rows={c['ref']:c for c in audit['components']}
assert '6.33' in audit_rows['C5']['value_or_identity'] and '16 mm' in audit_rows['C5']['value_or_identity']
assert 'pin5' in audit_rows['U6']['value_or_identity'].lower() and '1 ohm' in audit_rows['U6']['value_or_identity']
assert '1.4' in audit_rows['L1']['value_or_identity'] and '2.2' in audit_rows['L2']['value_or_identity']
assert 'TP9' not in audit_rows and 'R33' not in audit_rows, 'Removed unsupported entry has returned'
assert members['R41.1']==members['J1.1'] and members['U4.21']==members['TP16.1']!=members['TP104.1']
for name in ['docs/FINISHING_CHECKLIST.html','docs/FINISHING_MEASUREMENTS.html']:
    body=(ROOT/name).read_text(encoding='utf-8')
    for group in work['finish_plan']:
        assert group['title'] in body, (name,group['id'],'Missing shared finishing stage')
landing=(ROOT/'index.html').read_text(encoding='utf-8')
assert 'docs/FINISHING_CHECKLIST.html' in landing and 'docs/OPEN_ITEMS.md' in landing
for issue in issues:
    assert 'docs/OPEN_ITEMS.md#'+issue['id'].lower() in landing, (issue['id'],'Missing compact current issue link')
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

# Generated Markdown and HTML must expose the same authoritative open-item fields.
markdown=(ROOT/'docs/OPEN_ITEMS.md').read_text(encoding='utf-8')
for issue in issues:
    assert f'## {issue["id"]} - {issue["area"]}' in markdown
    for key in ['category','known','unknown','codex_action','owner_input','closed_when']:
        assert issue[key].replace('|','/').replace('\n',' ') in markdown
        assert __import__('html').escape(issue[key]) in checklist
assert m['revision'] in (ROOT/'README.md').read_text() and m['revision'] in markdown
assert 'physical switch common pairs remain inferred' not in next(c for c in m['components'] if c['ref']=='R40')['current_summary']
assert 'R33 branch remains' not in next(n for n in m['nets'] if n['net']=='H_PIR_RAW')['status']
for file in ['README.md','docs/OPEN_ITEMS.md','docs/TOPOLOGY_AUDIT.md']:
    import re
    for target in re.findall(r'\]\(([^)]+)\)', (ROOT/file).read_text()):
        url=urlparse(target)
        if not url.scheme and url.path:assert (ROOT/file).parent.joinpath(url.path).exists(),(file,target)
physical=read('evidence/topology_closure_audit.json')
assert physical['revision']==m['revision'] and physical['result']=='PASS_WITH_EVIDENCE_GAPS'
assert not physical['split_findings'] and not physical['incorrect_merge_findings']
assert not physical['unmapped_observed_pads']
assert any(i['id']=='E11' and 'RX-3' in i['owner_input'] and 'TP7' in i['owner_input'] for i in issues)
assert {t['id'] for t in measurements['tests']}=={'RX-3'}
assert {'RX-1','RX-2'} <= {t['id'] for t in measurements['completed_tests']}
assert work['owner_action_summary'] in (ROOT/'README.md').read_text(encoding='utf-8')
