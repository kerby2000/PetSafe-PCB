"""Compare the authored electrical model with a native KiCad XML netlist."""
from pathlib import Path
from collections import Counter
import json, hashlib, re, math, xml.etree.ElementTree as ET
import sexpdata as sx
ROOT=Path(__file__).resolve().parents[1]

def board_net_partitions(native, model):
    """Validate the explicit off-board winding, then compare main-board copper only."""
    ext=model.get('external_antenna',{}).get('native_reference')
    nodes={n.attrib['ref']+'.'+n.attrib['pin']:net.attrib['name'] for net in native.findall('./nets/net') for n in net.findall('node')}
    if ext:
        assert ext=='L101' and model['external_antenna']['inductance_uh']==500
        comp=native.find('./components/comp[@ref="L101"]')
        assert comp is not None and comp.findtext('value')=='500uH'
        assert comp.find('libsource').attrib=={'lib':'Device','part':'L','description':'Inductor'}
        assert comp.find('property[@name="exclude_from_bom"]') is not None
        assert comp.find('property[@name="exclude_from_board"]') is not None
        assert not comp.findtext('footprint')
        assert nodes['L101.1']==nodes['TP105.1']!=nodes['TP106.1']==nodes['L101.2']
        assert {p.attrib['num'] for p in comp.findall('./units/unit/pins/pin')}=={'1','2'}
    actual={frozenset(n.attrib['ref']+'.'+n.attrib['pin'] for n in net.findall('node') if n.attrib['ref']!=ext):net.attrib['name'] for net in native.findall('./nets/net')}
    return actual
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def wire_graph(wires, connection_points=()):
    """Join wire ends/T-junctions; do not join a plain interior X crossing."""
    from collections import defaultdict
    points=set(connection_points)|{p for pair in wires for p in pair}
    graph=defaultdict(set)
    for a,b in wires:
        def on(p):
            cross=(p[0]-a[0])*(b[1]-a[1])-(p[1]-a[1])*(b[0]-a[0])
            return abs(cross)<1e-7 and all(min(a[i],b[i])-1e-7<=p[i]<=max(a[i],b[i])+1e-7 for i in [0,1])
        ordered=sorted(p for p in points if on(p))
        for p,q in zip(ordered,ordered[1:]):graph[p].add(q);graph[q].add(p)
    return graph

def native_pin_positions(tree):
    """Resolve embedded pin coordinates independently of the evidence model."""
    def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
    def children(x,t):return [a for a in x if tag(a)==t]
    def one(x,t):return next((a for a in x if tag(a)==t),None)
    libs={x[1]:x for x in children(one(tree,'lib_symbols'),'symbol')};result={}
    for inst in children(tree,'symbol'):
        ref=next(p[2] for p in children(inst,'property') if p[1]=='Reference')
        x,y,rot=map(float,one(inst,'at')[1:]);r=math.radians(rot)
        unit=int(one(inst,'unit')[1]);mirror=one(inst,'mirror')
        for sub in children(libs[one(inst,'lib_id')[1]],'symbol'):
            u,style=map(int,sub[1].rsplit('_',2)[1:])
            if u not in (0,unit) or style not in (0,1):continue
            for pin in children(sub,'pin'):
                px,py,_=map(float,one(pin,'at')[1:])
                if mirror:
                    if str(mirror[1])=='x':py=-py
                    if str(mirror[1])=='y':px=-px
                result[ref+'.'+str(one(pin,'number')[1])]=[round(x+px*math.cos(r)-py*math.sin(r),5),round(y-px*math.sin(r)-py*math.cos(r),5)]
    return result
def main():
    m=json.loads((ROOT/'evidence/reconstruction.json').read_text())
    native=ET.parse(ROOT/'output/PetSafe_netlist.xml')
    def translated(ep):
        if 'native_pin_crosswalk' in m:return m['native_pin_crosswalk'][ep]
        r,p=ep.rsplit('.',1)
        return m['reference_map'].get(r,r)+'.'+p
    actual=board_net_partitions(native,m)
    expected={frozenset(map(translated,n['endpoints'])):n['net'] for n in m['nets']}
    differences=[dict(net=n,pins=sorted(p)) for p,n in expected.items() if p not in actual]
    extras=[dict(net=n,pins=sorted(p)) for p,n in actual.items() if len(p)>1 and p not in expected]
    assert not differences and not extras,(differences,extras)
    assert len(native.findall('./components/comp'))==len(m['components'])+bool(m.get('external_antenna',{}).get('native_reference'))
    assert len(native.findall('./design/sheet'))==1
    old=json.loads((ROOT/'reference/v01/evidence/reconstruction.json').read_text())
    withdrawn={f['net']:f for f in m.get('withdrawn_original_fragments',[])}
    assert set(withdrawn)=={'V_Q1_LEFT'}, 'Only the explicitly user-refuted original fragment may be skipped'
    assert withdrawn['V_Q1_LEFT']['user_authorization']=='Remove Q1.L–R43.2 connection'
    for net in old['nets']:
        ep=set(map(translated,net['endpoints']))
        if net['net'] in withdrawn:
            assert set(net['endpoints'])==set(withdrawn[net['net']]['endpoints'])
            assert not any(ep<=pins for pins in actual), 'Withdrawn Q1/R43 tie revived'
            continue
        assert any(ep<=pins for pins in actual),net
    manifest=json.loads((ROOT/'evidence/original_photo_manifest.json').read_text())
    for p in manifest:
        source=ROOT/'photos/originals'/p['file']
        assert sha(source)==p['sha256'] and source.stat().st_size==p['bytes'],p
    erc=json.loads((ROOT/'output/erc.json').read_text())
    violations=[v for sheet in erc['sheets'] for v in sheet['violations']]
    counts=Counter(v['type'] for v in violations)
    # Keep the DNP regulator-option warning visible in native ERC. Accept only
    # this documented pair, never a blanket waiver for output conflicts.
    option_conflicts=[v for v in violations if v['type']=='pin_to_pin']
    for warning in option_conflicts:
        assert {i['description'] for i in warning['items']}=={
            'Symbol U6 Pin 3 [VOUT, Power output, Line]',
            'Symbol U106 Pin 2 [VO, Power output, Line]'},warning
        assert next(c for c in m['components'] if c['ref']=='U6A')['population']=='DNP'
        assert any({'U6.3','U106.2'}<=pins and name=='H_PIR_VDD' for pins,name in expected.items())
        assert (ROOT/'evidence/options_reorganization_20261009.json').exists()
    unexpected=set(counts)-{'pin_not_connected','isolated_pin_label','power_pin_not_driven','pin_not_driven','pin_to_pin'}
    assert not unexpected,counts
    sch=ROOT/'schematic/PetSafe_1001339.kicad_sch'
    positions=native_pin_positions(sx.loads(sch.read_text(encoding='utf-8')))
    assert m['pin_positions']=={ep:positions[target] for ep,target in m['native_pin_crosswalk'].items()}, 'Model/native pad coordinate mismatch'
    # Permit only evidence-backed intentional NCs; never blanket-suppress opens.
    nc=m.get('intentional_no_connects',[])
    marked={tuple(round(float(v),5) for v in xy) for xy in re.findall(r'\(no_connect\s+\(at\s+([-\d.]+)\s+([-\d.]+)\)',sch.read_text())}
    assert marked=={tuple(m['pin_positions'][c['endpoint']]) for c in nc}
    for c in nc:
        assert c['basis'] and (ROOT/c['evidence']).exists()
        assert c['endpoint'] not in m['unresolved_pins']
        assert not any(translated(c['endpoint']) in pins and len(pins)>1 for pins in actual)
    assert '(lib_id "PetSafe_Working:' not in sch.read_text()
    definitions={(p.attrib['lib'],p.attrib['part']) for p in native.findall('./libparts/libpart')}
    custom=sum(lib=='PetSafe_Datasheet' for lib,part in definitions)
    expected_definitions={tuple(c['symbol'].split(':',1)) for c in json.loads((ROOT/'evidence/library_layout.json').read_text())['catalog']}
    assert custom==4 and definitions==expected_definitions,(definitions,expected_definitions)
    # D2 is a measured equivalent, not an inferred manufacturer replacement.
    d2=native.find('./components/comp[@ref="D2"]')
    assert d2.find('libsource').attrib['part']=='D_Dual_Series_KAC'
    d2lib=native.find('./libparts/libpart[@lib="Device"][@part="D_Dual_Series_KAC"]')
    assert {p.attrib['num']:p.attrib['name'] for p in d2lib.findall('./pins/pin')}=={'1':'K','2':'A','3':'common'}
    assert {p:m['native_pin_crosswalk']['D2.'+p] for p in ['L','R','S']}=={'L':'D2.1','R':'D2.2','S':'D2.3'}
    assert 'equivalent' in d2.findtext('./fields/field[@name="Representation"]')
    # Independent manufacturer pin-table contracts, checked in native KiCad output.
    contracts={
        'U1':('S-1200B45-M5T1','Package_TO_SOT_SMD:SOT-23-5',
              [('VIN','power_in'),('VSS','power_in'),('ON/OFF','input'),('NC','passive'),('VOUT','power_out')]),
        'U5':('MX512H','Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
              [('VCC','power_in'),('INA','input'),('INB','input'),('VDD','power_in'),('OUTB','tri_state'),('GND','power_in'),('GND','power_in'),('OUTA','tri_state')]),
        'U6':('S-812C33AMC','Package_TO_SOT_SMD:SOT-23-5',
              [('VSS','power_in'),('VIN','power_in'),('VOUT','power_out'),('NC','passive'),('NC','passive')]),
        'Q8':('SIL3724A','Package_TO_SOT_SMD:SOT-23-6',
              [('G','input'),('S','passive'),('G','input'),('D','passive'),('S','passive'),('D','passive')])}
    for ref,(part,footprint,pins) in contracts.items():
        lib=native.find(f'./libparts/libpart[@lib="PetSafe_Datasheet"][@part="{part}"]')
        actual_pins={p.attrib['num']:(p.attrib['name'],p.attrib['type']) for p in lib.findall('./pins/pin')}
        assert actual_pins=={str(i):p for i,p in enumerate(pins,1)},(ref,actual_pins)
        comp=native.find(f'./components/comp[@ref="{ref}"]')
        assert comp.findtext('footprint')==footprint
        assert comp.findtext('datasheet')==lib.findtext('docs')
        assert comp.findtext('description')==lib.findtext('description')
    report=dict(date=m.get('review_date','2026-10-08'),native_tool=native.findtext('./design/tool'),native_load_and_export='PASS',single_sheet='PASS',catalog_components=len(m['components']),symbol_units=len(json.loads((ROOT/'evidence/library_layout.json').read_text())['catalog']),physical_pins=sum(len(c['pins']) for c in m['components']),stock_library_symbols=len(definitions)-custom,custom_symbols=custom,proposed_net_partitions=len(expected),netlist_partition_comparison='PASS',unintended_multi_pin_nets=0,retained_original_visual_fragments=len(old['nets'])-len(withdrawn),withdrawn_original_visual_fragments=sorted(withdrawn),original_photo_checksums=f'PASS ({len(manifest)} files)',unresolved_physical_pins=len(m['unresolved_pins']),erc_total=len(violations),erc_by_type=dict(counts),erc_status='OPEN FINDINGS - candidate IC pin types checked; unknown board routing remains',gui_open='NOT_TESTED (native CLI validated)',hardware_verification='PARTIAL: recorded U6/Q8 resistance and selected PIC meter/visual routes; user via reports plus photo cross-checks; six powered DC levels and TP14 follow-ups recorded; circuit behavior and transient operation remain unverified',physical_pcb_layout='NOT_CREATED',schematic_sha256=sha(sch),input_zip_sha256=sha(ROOT/'input/PetSafe_KiCad_RE_v01.zip'))
    report['datasheet_symbol_pin_contracts']='PASS (U1: 5 pins; U5: 8 pins; U6: 5 pins; Q8: 6 pins; types, footprints and source properties)'
    report['external_antenna']='L101: 500uH, ANT1 to ANT2, excluded from main-board BOM and PCB; endpoints verified separately'
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
    (ROOT/'evidence/validation_log.txt').write_text('Native KiCad model/netlist cross-check: PASS\n'+json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
