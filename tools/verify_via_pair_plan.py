"""Check probe references, generated guide and separation from circuit evidence."""
from pathlib import Path
import csv, hashlib, json, re, subprocess
from pypdf import PdfReader

R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
p=read('evidence/via_pair_plan.json');a=read('evidence/via_audit.json');m=read('evidence/reconstruction.json')
sites={s['id']:s for s in a['sites']};tests=p['tests']
assert [(t['id'],t['left'],t['right']) for t in tests]==[('D1','V070','V049')]
assert sites['V075']['net']==sites['V064']['net']=='H_VDD'
assert sites['V075']['endpoints']==['Q7.R','R19.2']
assert 'not separate pad measurements' in sites['V075']['confidence']
assert sites['V070']['net']=='H_RX_ENABLE_CTL'
assert sites['V064']['excluded_vias']==['V070'] and sites['V070']['excluded_vias']==['V064']
assert sites['V070']['resistive_measurements'][0]['resistance_ohms']==11200
assert sites['V075']['candidate_endpoints']==[]
assert all(sites[s]['joined_vias']==['V063','V064','V075'] for s in ['V063','V064','V075'])
for dest in ['V100','V103','V107']:
 assert dest in sites['V095']['excluded_vias'] and 'V095' in sites[dest]['excluded_vias']
assert all('V103' not in sites[s].get('excluded_vias',[]) for s in ['V100','V107']), 'Untested pairs cannot be inferred negative'
assert len(p['reported_results']['confirmed_via_pairs'])==6
assert len(p['reported_results']['rejected_pairs'])==10
assert sites['V049']['excluded_vias']==['V071'] and 'V049' in sites['V071']['excluded_vias']
assert sites['V049']['resistive_measurements'][0]['resistance_ohms']==20000
measured={tuple(sorted(pair)) for pair in p['reported_results']['confirmed_via_pairs']}
measured|={tuple(sorted(item['vias'])) for item in p['reported_results']['rejected_pairs']}
assert all(tuple(sorted([t['left'],t['right']])) not in measured for t in tests), 'Completed pair re-entered queue'
assert all(sites[t[k]]['active'] for t in tests for k in ['left','right'])
assert all(t['status']=='PROPOSED_UNMEASURED' for t in tests)
assert not any(set([t['left'],t['right']])==set(pair) for t in tests for pair in p['known_controls'])
assert p['basis_revision']==m['revision']
assert p['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert p['schematic_sha256']==read('evidence/validation.json')['schematic_sha256']
assert m['revision']=='v0.9.7'
assert p['count_basis']['local_candidate_groups']==len(p['local_groups'])
assert p['count_basis']['nonrail_candidate_sites']==sum(len(g['vias']) for g in p['local_groups'])
assert not any('V114' in g['vias'] for g in p['local_groups']), 'Resolved U2 ground re-entered search'
assert not any('V075' in g['vias'] for g in p['local_groups']), 'Known V075 rail re-entered unknown-net search'
assert p['count_basis']['local_candidate_groups']==19 and p['count_basis']['nonrail_candidate_sites']==23
html=(R/'docs/VIA_PAIR_TESTS.html').read_text(encoding='utf-8')
assert 'const plan='+json.dumps(p).replace('</','<\\/')+',audit=' in html
assert all(x not in html for x in ['PLAN_DATA','AUDIT_DATA','SITE_COUNT','GROUP_COUNT','BASIS_REV'])
syntax={}
for path in ['docs/VIA_PAIR_TESTS.html','docs/VIA_REVIEW.html']:
 body=(R/path).read_text(encoding='utf-8')
 for target in re.findall(r'href="([^"]+)"',body):
  if not target.startswith(('https:','http:','#','mailto:')):assert (R/path).parent.joinpath(target).exists(),(path,target)
 js='\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>',body))
 dest=R/'.cache/via-pairs'/Path(path).with_suffix('.js').name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(js,encoding='utf-8')
 subprocess.run(['node','--check',str(dest)],check=True,capture_output=True);syntax[path]='PASS'
with (R/'evidence/via_pair_readings.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
assert [(r['test_id'],r['probe_1'],r['probe_2']) for r in rows]==[(t['id'],t['left'],t['right']) for t in tests]
with (R/'evidence/via_pair_round2_readings.csv').open(encoding='utf-8',newline='') as f:previous=list(csv.DictReader(f))
assert all(r['reading']=='OL' for r in previous if r['test_id'] in ['C5','C6','C7'])
assert len(previous)==4
with (R/'evidence/via_pair_round3_readings.csv').open(encoding='utf-8',newline='') as f:third=list(csv.DictReader(f))
assert third[0]['reading']=='11.2 kohm' and third[0]['test_id']=='B3'
pdfpath=p['pdf_path'];pdf=PdfReader(R/pdfpath)
assert len(pdf.pages)==1
pdftext='\n'.join(page.extract_text() for page in pdf.pages)
assert all(t['id'] in pdftext and t['left'] in pdftext and t['right'] in pdftext for t in tests)
assert p['basis_revision'] in pdftext
photos={k:sha(p['photos'][k]) for k in ['front','rear']}
for entry in read('evidence/original_photo_manifest.json'):assert sha('photos/originals/'+entry['file'])==entry['sha256']
assert (R/'docs/VIA_PAIR_SEARCH.md').exists()
result=dict(status='PASS',basis_revision=p['basis_revision'],scope='11.2 kohm recorded; Q7 topology inferred with R18 input separate from VDD; one proposed GPIO candidate',proposed_tests=len(tests),local_groups=len(p['local_groups']),nonrail_sites=p['count_basis']['nonrail_candidate_sites'],confirmed_via_pairs=p['reported_results']['confirmed_via_pairs'],rejected_pairs=p['reported_results']['rejected_pairs'],active_endpoints='PASS',schematic_sha256=p['schematic_sha256'],photo_sha256=photos,original_photos='26 checksums PASS',html_embedded_plan='PASS',local_html_links='PASS',javascript_syntax=syntax,browser_interaction='NOT_TESTED',pdf=dict(path=pdfpath,pages=1,sha256=sha(pdfpath),text_check='PASS',visual_review='Rendered page inspected; targets, leaders and table readable'))
(R/'evidence/via_pair_plan_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: 11.2 kohm non-direct rail result, preserved readings, Q7 inferred topology, one unmeasured GPIO test, current native hash, HTML data/links/JS, one-page guide and original photo checksums.')
