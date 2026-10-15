"""Bound the E11 receiver split against the independently reviewed PR head."""
from pathlib import Path
import json,subprocess,xml.etree.ElementTree as ET
import sexpdata as sx
from inventory_contracts import with_receiver_input_split, with_receiver_input_split_v0946, with_receiver_capacitor_separations
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
rec=read('evidence/receiver_input_correction_v0946.json')
def old(p):return subprocess.check_output(['git','show',rec['baseline_commit']+':'+p],cwd=R).decode('utf-8')
m=read('evidence/reconstruction.json');b=json.loads(old('evidence/reconstruction.json'))
parts=lambda x:{n['net']:sorted(n['endpoints']) for n in x['nets']}
assert parts(m)==with_receiver_input_split(parts(b))
for k in ['native_pin_crosswalk','pin_positions','intentional_no_connects','unresolved_pins']:assert m[k]==b[k],k
keys=['value','proposed_value','value_evidence','value_proposal','population','pins','library_symbol','footprint']
inventory=lambda x:{c['ref']:{k:c.get(k) for k in keys} for c in x['components']}
assert inventory(m)==inventory(b),'Value, population, symbol or footprint changed'
def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
def one(x,t):return next((a for a in x if tag(a)==t),None)
def wire(x):return frozenset(tuple(float(v) for v in a[1:]) for a in one(x,'pts') if tag(a)=='xy')
def key(x):return sx.dumps([a for a in x if tag(a)!='uuid'])
path='schematic/PetSafe_1001339.kicad_sch'
before=sx.loads(old(path))
caprec=read('evidence/receiver_input_correction_v0947.json')
frozen=lambda p:subprocess.check_output(['git','show',caprec['baseline_commit']+':'+p],cwd=R).decode('utf-8')
after=sx.loads(frozen(path))
live=sx.loads((R/path).read_text(encoding='utf-8'))
assert parts(json.loads(frozen('evidence/reconstruction.json')))==with_receiver_input_split_v0946(parts(b))
removed={frozenset(tuple(p) for p in w) for w in rec['native_removed_wire_segments']}
assert {wire(x) for x in after if tag(x)=='wire'}=={wire(x) for x in before if tag(x)=='wire'}-removed
for t in ['lib_symbols','symbol','no_connect','polyline']:
    def invariant(tree):
        return sorted(key([a for a in x if tag(a)!='property']) if t=='symbol' else key(x) for x in tree if tag(x)==t)
    assert invariant(before)==invariant(after),t
before_labels={key(x) for x in before if tag(x)=='label'}
new_labels=[x for x in after if tag(x)=='label' and key(x) not in before_labels]
assert before_labels <= {key(x) for x in after if tag(x)=='label'}
assert sorted((x[1],one(x,'at')[1:3]) for x in new_labels)==sorted((x['net'],x['position']) for x in rec['new_labels'])
for tree in [before,after]:
    assert all(x[1]!='D2_C20' for x in tree if tag(x)=='global_label')
points=lambda tree:{tuple(one(x,'at')[1:3]) for x in tree if tag(x)=='junction'}
assert points(after)==points(before)-{tuple(p) for p in rec['native_removed_junctions']}
# Live geometry proof is bounded independently of the frozen v0.9.46 split.
cap_removed={frozenset(tuple(p) for p in w) for w in caprec['native_removed_wire_segments']}
assert {wire(x) for x in live if tag(x)=='wire'}=={wire(x) for x in after if tag(x)=='wire'}-cap_removed
for t in ['lib_symbols','symbol','no_connect','polyline']:assert invariant(after)==invariant(live),t
assert points(live)==points(after)
label_positions=lambda tree:{(x[1],tuple(one(x,'at')[1:3])) for x in tree if tag(x)=='label'}
added={(x['net'],tuple(x['position'])) for x in caprec['native_added_labels']}
removed_labels={(x['net'],tuple(x['position'])) for x in caprec['native_removed_labels']}
assert label_positions(live)==(label_positions(after)-removed_labels)|added
xml=ET.parse(R/'output/PetSafe_netlist.xml')
members={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
native=lambda e:members[m['native_pin_crosswalk'].get(e,e)]
assert native('C20.2')==native('D2.R')==native('R28.2')
assert native('C20.2')!=native('U3.3') and native('C20.2')!=native('TP7.1')
assert native('R28.1')==native('TP7.1')==native('U4.3')
assert native('C19.1')!=native('U3.3')
assert native('C20.1')!=native('GND.1')
for endpoint in ['C19.1','C20.1','U3.3']:
    assert [p for p,n in members.items() if n==native(endpoint)]==[m['native_pin_crosswalk'].get(endpoint,endpoint)]
result=dict(result='PASS',revision=m['revision'],baseline_commit=rec['baseline_commit'],allowed_split=rec['after'],all_other_partitions='UNCHANGED',native_geometry='Frozen v0.9.46 split preserved; live RX-1/RX-2 change removes four segments and relabels three isolated endpoints',live_allowed_split=caprec['after'],values_pin_maps_population='UNCHANGED',new_resistors=0,remaining='U3.3, C19.1 and C20.1 onward destinations unresolved; no intentional NC declaration')
(R/'evidence/receiver_input_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: frozen D2/C20/R28 split and live RX-1/RX-2 separations; native singleton endpoints and TP7 resistor path; other partitions/values/mappings unchanged.')
