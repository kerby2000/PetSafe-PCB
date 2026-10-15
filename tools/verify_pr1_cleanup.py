"""Frozen PR1 cleanup/audit commits preserve the R39 correction's decisions.

Later electrical work is checked separately by its bounded live regression.
"""
from pathlib import Path
import hashlib, json, subprocess
import sexpdata as sx
R=Path(__file__).resolve().parents[1]
BASE='891d69c'
END='ed9824035b7c29f20bf0e995c0d1413727df3b93'
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode('utf-8')
def read(path):return json.loads((R/path).read_text(encoding='utf-8'))
def completed(path):return subprocess.check_output(['git','show',END+':'+path],cwd=R).decode('utf-8')
m=json.loads(completed('evidence/reconstruction.json'));b=json.loads(old('evidence/reconstruction.json'))
assert {n['net']:sorted(n['endpoints']) for n in m['nets']}=={n['net']:sorted(n['endpoints']) for n in b['nets']}
for key in ['native_pin_crosswalk','pin_positions','geometric_wires','intentional_no_connects','unresolved_pins']:assert m[key]==b[key],key
keys=['value','proposed_value','value_evidence','value_proposal','population','pins','library_symbol','footprint']
assert {c['ref']:{k:c.get(k) for k in keys} for c in m['components']}=={c['ref']:{k:c.get(k) for k in keys} for c in b['components']}
def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
def electrical(text):
    result=[]
    for x in sx.loads(text):
        if tag(x)=='symbol':x=[f for f in x if tag(f)!='property']
        if tag(x) not in ['text','title_block']:result.append(sx.dumps(x))
    return sorted(result)
for f in ['schematic/PetSafe_1001339.kicad_sch','tools/templates/mcp_standard_placements.kicad_sch']:
    assert electrical(completed(f))==electrical(old(f)),f
result=dict(result='PASS',baseline_commit=BASE,completed_commit=END,scope='Historical PR1 documentation/audit snapshot; later live corrections have separate regressions',physical_memberships='UNCHANGED',native_geometry_pin_mappings='UNCHANGED',values_population_choices='UNCHANGED')
(R/'evidence/pr1_cleanup_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: historical cleanup/audit commits changed no native electrical geometry, pad memberships, pin maps, values or population choices.')
