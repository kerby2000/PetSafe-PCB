"""Audit native wire ends and complete uncertainty coverage without inventing hardware evidence."""
from pathlib import Path
from collections import defaultdict
import json, hashlib, subprocess, gzip
import sexpdata as sx
from current_state import current_state, validate_issue_register
from validate_native import wire_graph
from inventory_contracts import verify_receiver_open_erc, with_receiver_input_split, with_r39_output_pullup, without_withdrawn_r33, retained_crosswalk, with_antenna_outer_rail, with_ra0_tp6, with_tp14_motor_output, with_u2_r5_topology
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def tag(e):return str(e[0]) if isinstance(e,list) and e else ''
def children(e,t):return [x for x in e if tag(x)==t]
def one(e,t):return next(x for x in e if tag(x)==t)
def xy(e):return tuple(round(float(x),5) for x in e)
m=read('evidence/reconstruction.json');w=read('evidence/remaining_work.json');s=current_state()
validate_issue_register(m,w)
tree=sx.loads((R/'schematic/PetSafe_1001339.kicad_sch').read_text())
layout=read('evidence/library_layout.json')
assert layout['authoring_mode']=='reviewed_native_layout'
redraw=read(layout['baseline_record'])
incoming=gzip.decompress((R/redraw['source_archive']).read_bytes())
assert hashlib.sha256(incoming).hexdigest()==redraw['source_sha256']
for path in ['schematic/PetSafe_1001339.kicad_sch','tools/templates/mcp_standard_placements.kicad_sch']:
    assert hashlib.sha256((R/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==redraw['reviewed_schematic_sha256'], (path,'Reviewed layout drift')
assert hashlib.sha256(json.dumps([m['pin_positions'],m['geometric_wires']],sort_keys=True).encode()).hexdigest()==redraw['model_geometry_sha256']
def poses(t):
    return {(next(p[2] for p in children(x,'property') if p[1]=='Reference'),one(x,'unit')[1]):(xy(one(x,'at')[1:3]),float(one(x,'at')[3])) for x in children(t,'symbol')}
before=poses(sx.loads(incoming.decode('utf-8')));after=poses(tree)
assert before.keys()==after.keys()
for k,(p,angle) in before.items():
    expected=(angle+180)%360 if k[0] in redraw['nonpolar_pin_mapping_restored'] else angle
    assert after[k]==(p,expected),(k,'Owner position/rotation was not preserved')
assert layout['pins']==m['pin_positions'] and layout['wires']==m['geometric_wires']
segments=[tuple(xy(p[1:]) for p in children(one(w,'pts'),'xy')) for w in children(tree,'wire')]
labels={xy(one(l,'at')[1:3]) for kind in ['label','global_label','hierarchical_label'] for l in children(tree,kind)}
pins={xy(p) for p in m['pin_positions'].values()}
flags=[i for i in children(tree,'symbol') if one(i,'lib_id')[1]=='power:PWR_FLAG']
flag_points={xy(one(i,'at')[1:3]) for i in flags}
decl=read('evidence/power_source_declarations.json')['declarations']
assert flag_points=={xy(d['position_mm']) for d in decl} and len(flags)==6
pins|=flag_points
junctions={xy(one(j,'at')[1:3]) for j in children(tree,'junction')}
# KiCad can save a T junction in the middle of an unsplit wire. The old
# generated layout split every segment first; manual layouts need this step.
edges=wire_graph(segments,junctions|pins|labels)
tails=sorted(p for p,n in edges.items() if len(n)==1 and p not in pins|labels)
assert not tails,('Unattached native wire tails',tails)
islands=[];seen=set()
for start in edges:
    if start in seen:continue
    todo=[start];group=set()
    while todo:
        p=todo.pop()
        if p in group:continue
        group.add(p);todo.extend(edges[p]-group)
    seen|=group
    if not group&pins:islands.append(sorted(group))
assert not islands,('Wire pieces without physical or power-symbol pin',islands)
baseline=json.loads(subprocess.check_output(['git','show','ecd683d:evidence/reconstruction.json'],cwd=R,text=True,encoding='utf-8'))
partitions=lambda model:{n['net']:sorted(n['endpoints']) for n in model['nets']}
assert partitions(m)==with_receiver_input_split(with_r39_output_pullup(with_u2_r5_topology(with_tp14_motor_output(with_ra0_tp6(with_antenna_outer_rail(without_withdrawn_r33(partitions(baseline)))))))), 'Only documented R33 withdrawal, front capacitor pad moves and B59 RA0-TP6 and TP14-OUTA plus U2/R5 corrections are permitted'
assert m['native_pin_crosswalk']==retained_crosswalk(baseline['native_pin_crosswalk'])
assert m['intentional_no_connects']==baseline['intentional_no_connects']
assert s['erc_by_type']==verify_receiver_open_erc(read('output/erc.json'))
erc=read('output/erc.json')
ignored={x['key'] for x in erc.get('ignored_checks',[])}
assert not ignored&{'pin_not_connected','wire_dangling','label_dangling','isolated_pin_label','unconnected_wire_endpoint','power_pin_not_driven'}
project=read('schematic/PetSafe_1001339.kicad_pro')
assert not project.get('erc',{}).get('erc_exclusions',[])
assert next(c for c in m['components'] if c['ref']=='U6A')['population']=='DNP'
coverage=[]
for c in m['components']:
    ref=c['ref'];issues=[i['id'] for i in w['issues'] if ref in i['refs']]
    if ref in s['unknown_ceramic_values']:issues.append('V01')
    if c['population']=='DNP':issues.append('accepted-DNP-scope')
    if ref in {'TP11','TP17'}:issues.append('E06-documented-reconstruction-limitation')
    if '?' in c.get('proposed_value','') and not issues:
        # Passive ratings remain V01; geometry/pin numbering remain M01.
        issues.append('V01' if c['kind'] in {'R','L','C'} else 'M01')
    coverage.append(dict(reference=ref,issues=sorted(set(issues)),population=c['population']))
for ref in s['unknown_ceramic_values']:
    assert 'V01' in next(c for c in coverage if c['reference']==ref)['issues']
assert all(any(ref in i['refs'] for i in w['issues']) for ref in s['footprints']['unassigned'])
audit=dict(revision=m['revision'],result='PASS',schematic_sha256=s['schematic_sha256'],physical_net_partitions=len(m['nets']),pad_membership_baseline='ecd683d',documented_pad_moves='evidence/antenna_outer_rail_correction_v0937.json',documented_net_merge='evidence/ra0_tp6_connection_v0938.json',documented_tp14_move='evidence/tp14_motor_output_correction_v0939.json',documented_rf_supply_output_correction='evidence/u2_r5_topology_correction_v0940.json',documented_r39_move='evidence/r39_endpoint_correction_v0945.json',documented_receiver_input_split='evidence/receiver_input_correction_v0946.json',documented_receiver_capacitor_separations='evidence/receiver_input_correction_v0947.json',documented_receiver_destinations='evidence/receiver_connections_v0948.json',withdrawn_catalog_entries=['R33'],retained_physical_pad_crosswalk_unchanged=True,intentional_nc_unchanged=['U6.L1 / native pin4'],dangling_wire_ends=len(tails),wire_islands_without_pins=len(islands),native_wire_segments=len(children(tree,'wire')),unassigned_model_pads=len(m['unresolved_pins']),isolated_modeled_nets=[n['net'] for n in m['nets'] if len(n['endpoints'])==1],erc=s['erc_by_type'],erc_exclusions=[],unchanged_default_ignored_checks=sorted(ignored),source_flags=decl,local_only_branches={net:'evidence/e06_disposition_v0941.json' for net in ['PIC_RC3','PIC_RC7_TP17']},current_device_gap='E04: Q3 in-circuit pattern disputes PNP pinout; isolated identification remains optional.',active_issue_count=len(w['issues']),uncertainty_coverage=coverage,unverified_footprint='LED1 / M01',unrecovered_ceramics=s['unknown_ceramic_values'],limit='Checks native geometry, catalog and registered evidence only. Does not prove unseen inner-layer continuity, fitted identities or powered behavior.')
(R/'evidence/finalization_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
print(f"Audit PASS: {len(tails)} wire tails, {len(islands)} pinless wire islands, {len(w['issues'])} active issues, only documented front-capacitor moves and B59 RA0-TP6 and TP14-OUTA and U2/R5 RF plus R39 and receiver-input split corrections; unsupported R33 withdrawn.")
