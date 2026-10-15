"""Verify the bounded v0.9.44 value application in native/template/model sources."""
from pathlib import Path
import argparse, hashlib, json
import sexpdata as sx
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
def read(f):return json.loads((R/f).read_text(encoding='utf-8'))
def save(f,x):(R/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(data):return hashlib.sha256(data).hexdigest()
def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
def one(x,t):return next((a for a in x if tag(a)==t),None)
def inspect(path,changed):
 tree=sx.loads(path.read_text(encoding='utf-8'));symbols={};invariants=[];unchanged=[]
 for item in tree:
  t=tag(item)
  if t=='symbol':
   props={a[1]:a[2] for a in item if tag(a)=='property'}
   ref=props['Reference'];symbols.setdefault(ref,[]).append(props)
   invariants.append(sx.dumps([a for a in item if tag(a)!='property']))
   if ref not in changed:unchanged.append((ref,one(item,'unit')[1],props['Value'],props['Footprint']))
  elif t in {'lib_symbols','wire','junction','label','no_connect','polyline','bus','bus_entry','global_label','hierarchical_label','sheet'}:
   invariants.append(sx.dumps(item))
 return dict(geometry_and_library_sha256=sha('\n'.join(sorted(invariants)).encode()),unchanged_values_sha256=sha(json.dumps(sorted(unchanged)).encode())),symbols
p=read('evidence/capacitor_value_review_20261015.json');a=read('evidence/capacitor_application_v0944.json')
changed=set(a['updated_references']);assert len(changed)==44
m=read('evidence/reconstruction.json');model={c['ref']:c for c in m['components']}
layout={x['original_ref']:x for x in read('evidence/library_layout.json')['catalog']}
placements={x['reference']:x for x in read('evidence/library_placements.json')['components']}
files=['schematic/PetSafe_1001339.kicad_sch','tools/templates/mcp_standard_placements.kicad_sch']
if 'baseline_invariants' not in a:
 assert args.record,'Initialize immutable baseline invariants with --record'
 a['baseline_invariants']={}
 for f in files:
  baseline=R/'.cache/v0944-before'/f
  assert sha(baseline.read_bytes())==a['baseline_sha256'][f]
  a['baseline_invariants'][f]=inspect(baseline,changed)[0]
before_model=read('.cache/v0944-before/evidence/reconstruction.json') if (R/'.cache/v0944-before/evidence/reconstruction.json').exists() else None
if 'baseline_nets_sha256' not in a:
 assert args.record and before_model is not None
 a['baseline_nets_sha256']=sha(json.dumps(before_model['nets'],sort_keys=True).encode())
assert sha(json.dumps(m['nets'],sort_keys=True).encode())==a['baseline_nets_sha256'],'Model nets changed during value-only application'
for f in files:
 actual,symbols=inspect(R/f,changed)
 assert actual==a['baseline_invariants'][f],(f,'Geometry, library, or unrelated component value changed')
 for c in p['components']:
  ref=c['ref'];expected=c['proposal'].replace(' ','')+'*'
  assert c['applied_to_native'] and c['native_value']==expected
  assert model[ref]['value']=='UNKNOWN' and model[ref]['value_evidence']['state']=='estimated'
  assert model[ref]['proposed_value']==layout[ref]['placement']['value']==layout[ref]['legacy']['value']==placements[ref]['value']==expected
  props=symbols[ref];assert len(props)==1
  props=props[0];assert props['Value']==expected and props['NominalEstimate']==c['proposal']
  assert props['ValueStatus']=='ESTIMATED - not factory verified'
  assert props['Voltage']==str(c['voltage_rating_v'])+' V (proposed)'
  assert props['Dielectric']==c['dielectric']+' (proposed)'
  assert props['Tolerance']==str(c['tolerance_percent'])+'% (proposed)'
  assert props['ValueBasis']==c['basis'] and props['ValueQualification']==c['remaining']
  for key in ['ValueStatus','Voltage','Dielectric','Tolerance','ValueBasis','ValueQualification','ValueSource','NominalEstimate','DesignSeed']:
   assert props[key]==layout[ref]['placement']['properties'][key]==placements[ref]['properties'][key]
antenna=read('evidence/antenna_inductance_results_20261015.json')
assert antenna['inductance_uh']==p['antenna_design_example']['design_inductance_uh']==m['external_antenna']['inductance_uh']==500
assert antenna['measurement_frequency_hz'] is None and antenna['isolation_state'] is None
assert p['topology_change'] is False and p['electrical_change'] is True and p['individual_values_closed']==[]
assert m['revision']==p['schematic_revision']=='v0.9.44'
hashes={f:sha((R/f).read_bytes()) for f in files+['evidence/reconstruction.json']}
if args.record:
 p['source_schematic_sha256']=hashes[files[0]];p['source_model_sha256']=hashes['evidence/reconstruction.json']
 save('evidence/capacitor_value_review_20261015.json',p)
 a['current_sha256']=hashes;a['validation']={'result':'PASS','capacitor_candidates_applied':44,'native_and_template_properties':'MATCH_MODEL_AND_LAYOUT','topology_and_symbol_geometry':'UNCHANGED','other_values_including_C5_and_DNP':'UNCHANGED','factory_values_newly_confirmed':0,'antenna_inductance_uh_user_reported':500}
 save('evidence/capacitor_application_v0944.json',a)
else:
 assert a['current_sha256']==hashes,'Application audit hashes stale'
 assert p['source_schematic_sha256']==hashes[files[0]] and p['source_model_sha256']==hashes['evidence/reconstruction.json']
print('PASS: 44 starred estimates and proposed properties match native/template/model/layout; geometry, nets, C5, DNP and all other values unchanged; 500-uH report qualified.')
