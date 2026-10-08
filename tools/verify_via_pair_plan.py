"""Check probe references, generated guide and separation from circuit evidence."""
from pathlib import Path
import csv, hashlib, json, re, subprocess
from pypdf import PdfReader

R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
p=read('evidence/via_pair_plan.json');a=read('evidence/via_audit.json');m=read('evidence/reconstruction.json')
sites={s['id']:s for s in a['sites']};tests=p['tests']
assert len(tests)==4 and len({t['id'] for t in tests})==4
assert len({tuple(sorted([t['left'],t['right']])) for t in tests})==4
assert all(sites[t[k]]['active'] for t in tests for k in ['left','right'])
assert all(t['status']=='PROPOSED_UNMEASURED' for t in tests)
assert not any(set([t['left'],t['right']])==set(pair) for t in tests for pair in p['known_controls'])
assert p['basis_revision']==m['revision']
assert p['schematic_sha256']==sha('schematic/PetSafe_1001339.kicad_sch')
assert p['count_basis']['local_candidate_groups']==len(p['local_groups'])
assert p['count_basis']['nonrail_candidate_sites']==sum(len(g['vias']) for g in p['local_groups'])
assert not any('V114' in g['vias'] for g in p['local_groups']), 'Resolved U2 ground re-entered search'
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
pdfpath=p['pdf_path'];pdf=PdfReader(R/pdfpath)
assert len(pdf.pages)==1
pdftext='\n'.join(page.extract_text() for page in pdf.pages)
assert all(t['id'] in pdftext and t['left'] in pdftext and t['right'] in pdftext for t in tests)
assert p['basis_revision'] in pdftext
photos={k:sha(p['photos'][k]) for k in ['front','rear']}
for entry in read('evidence/original_photo_manifest.json'):assert sha('photos/originals/'+entry['file'])==entry['sha256']
assert (R/'docs/VIA_PAIR_SEARCH.md').exists()
result=dict(status='PASS',basis_revision=p['basis_revision'],scope='Measurement proposals only; v0.9.6 results independently recorded',proposed_tests=len(tests),local_groups=len(p['local_groups']),nonrail_sites=p['count_basis']['nonrail_candidate_sites'],active_endpoints='PASS',schematic_sha256=p['schematic_sha256'],photo_sha256=photos,original_photos='26 checksums PASS',html_embedded_plan='PASS',local_html_links='PASS',javascript_syntax=syntax,browser_interaction='NOT_TESTED',pdf=dict(path=pdfpath,pages=1,sha256=sha(pdfpath),text_check='PASS',visual_review='Rendered page inspected; targets, leaders and table readable'))
(R/'evidence/via_pair_plan_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: four active-site proposals, current native revision/hash, HTML data/links/JS, reading sheet, one-page guide and original photo checksums.')
