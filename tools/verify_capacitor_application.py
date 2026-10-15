"""Verify live capacitor preservation; the v0.9.44 bounded application record stays frozen."""
from pathlib import Path
import argparse, hashlib, json
import sexpdata as sx
R=Path(__file__).resolve().parents[1]
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
def canonical_text_sha256(data):
 # Only CRLF/LF equivalence is allowed; no whitespace or semantic changes.
 return sha(data.replace(b'\r\n', b'\n'))

def matches_text_digest(data, expected):
 # Live records written before this fix may contain a Windows CRLF digest.
 # Compare the two deterministic encodings without rewriting those records.
 lf=data.replace(b'\r\n', b'\n')
 return expected in {sha(lf), sha(lf.replace(b'\n', b'\r\n'))}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
 p=read('evidence/capacitor_value_review_20261015.json');a=read('evidence/capacitor_application_v0944.json')
 changed=set(a['updated_references']);assert len(changed)==44
 m=read('evidence/reconstruction.json');model={c['ref']:c for c in m['components']}
 layout={x['original_ref']:x for x in read('evidence/library_layout.json')['catalog']}
 placements={x['reference']:x for x in read('evidence/library_placements.json')['components']}
 files=['schematic/PetSafe_1001339.kicad_sch','tools/templates/mcp_standard_placements.kicad_sch']
 for f in files:
  actual,symbols=inspect(R/f,changed)
  assert actual['unchanged_values_sha256']==a['baseline_invariants'][f]['unchanged_values_sha256'],(f,'Unrelated value or footprint changed')
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
 assert m['revision']==p['schematic_revision']
 hashes={f:canonical_text_sha256((R/f).read_bytes()) for f in files+['evidence/reconstruction.json']}
 if args.record:
  p['source_schematic_sha256']=hashes[files[0]];p['source_model_sha256']=hashes['evidence/reconstruction.json']
  save('evidence/capacitor_value_review_20261015.json',p)
 else:
  assert matches_text_digest((R/files[0]).read_bytes(), p['source_schematic_sha256']), files[0]
  assert matches_text_digest((R/'evidence/reconstruction.json').read_bytes(), p['source_model_sha256']), 'evidence/reconstruction.json'
 print('PASS: 44 starred estimates and proposed properties match native/template/model/layout; C5, DNP and other values preserved; topology checked separately by native and bounded correction audits; 500-uH report qualified.')

if __name__=='__main__':main()
