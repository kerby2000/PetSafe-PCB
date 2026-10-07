"""Structural/data checks only. This does not replace native KiCad load/ERC."""
from pathlib import Path
import re,json,collections
R=Path(__file__).resolve().parents[1];D=R/'schematic'
def parse(text):
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',text)
 stack=[];roots=[]
 for token in tokens:
  if token=='(':
   a=[]
   if stack:stack[-1].append(a)
   else:roots.append(a)
   stack.append(a)
  elif token==')':
   if not stack:raise ValueError('Extra closing parenthesis')
   stack.pop()
  else:
   if not stack:raise ValueError('Atom outside expression: '+token)
   stack[-1].append(json.loads(token) if token.startswith('"') else token)
 if stack:raise ValueError(f'{len(stack)} unclosed expressions')
 if len(roots)!=1:raise ValueError(f'{len(roots)} root expressions')
 return roots[0]
def children(node,name):return [x for x in node if isinstance(x,list) and x and x[0]==name]
def one(node,name):
 xs=children(node,name);assert len(xs)==1,(name,len(xs));return xs[0]
model=json.loads((R/'evidence/reconstruction.json').read_text());byref={c['ref']:c for c in model['components']};seen={};reports=[]
for file in sorted(D.glob('*.kicad_sch')):
 tree=parse(file.read_text());assert tree[0]=='kicad_sch'
 lib={s[1]:s for s in children(one(tree,'lib_symbols'),'symbol')}
 refs=[]
 for sym in children(tree,'symbol'):
  lid=one(sym,'lib_id')[1];assert lid in lib,lid
  props={p[1]:p[2] for p in children(sym,'property')};ref=props['Reference']
  assert ref not in seen,ref;seen[ref]=file.name;refs.append(ref)
  pins=[p[1] for p in children(sym,'pin')]
  assert set(pins)==set(byref[ref]['pins']),ref
  libpins=[]
  for unit in children(lib[lid],'symbol'):
   libpins += [one(p,'number')[1] for p in children(unit,'pin')]
  assert set(libpins)==set(pins),(ref,libpins,pins)
 for sh in children(tree,'sheet'):
  props={p[1]:p[2] for p in children(sh,'property')}
  assert (D/props['Sheetfile']).is_file(),props
 assert not children(tree,'no_connect'),'Unknowns must not be suppressed as NC'
 reports.append({'file':file.name,'symbol_count':len(refs),'parse':'PASS','symbol_definitions_and_pins':'PASS','no_nc_flags':'PASS'})
assert set(seen)==set(byref),('inventory mismatch',set(byref)-set(seen))
for file in D.glob('*.kicad_sym'):parse(file.read_text())
parse((D/'sym-lib-table').read_text())
known={}
for net in model['nets']:
 assert len(net['endpoints'])>=2
 for ep in net['endpoints']:
  ref,p=ep.rsplit('.',1);assert ref in byref and p in byref[ref]['pins'];assert ep not in known,ep;known[ep]=net['net']
report={'scope':'STRUCTURAL_AND_MODEL_CHECKS_ONLY','native_kicad_available':False,'native_kicad_open_test':'NOT_RUN','erc':'NOT_RUN','physical_continuity_checks':'NONE_RECEIVED','sheet_results':reports,'catalog_entries':len(seen),'local_net_fragments':len(model['nets']),'electrically_measured_nets':0,'unresolved_pads':sum(len(c['pins']) for c in model['components'])-len(known)}
(R/'evidence/validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
