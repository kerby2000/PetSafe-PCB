"""Compare the authored electrical model with a native KiCad XML netlist."""
from pathlib import Path
from collections import Counter
import json, hashlib, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((ROOT/'evidence/reconstruction.json').read_text())
    native=ET.parse(ROOT/'output/PetSafe_netlist.xml')
    def translated(ep):
        if 'native_pin_crosswalk' in m:return m['native_pin_crosswalk'][ep]
        r,p=ep.rsplit('.',1)
        return m['reference_map'].get(r,r)+'.'+p
    actual={frozenset(n.attrib['ref']+'.'+n.attrib['pin'] for n in net.findall('node')):net.attrib['name'] for net in native.findall('./nets/net')}
    expected={frozenset(map(translated,n['endpoints'])):n['net'] for n in m['nets']}
    differences=[dict(net=n,pins=sorted(p)) for p,n in expected.items() if p not in actual]
    extras=[dict(net=n,pins=sorted(p)) for p,n in actual.items() if len(p)>1 and p not in expected]
    assert not differences and not extras,(differences,extras)
    assert len(native.findall('./components/comp'))==len(m['components'])
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
    report=dict(date=m.get('review_date','2026-10-08'),native_tool=native.findtext('./design/tool'),native_load_and_export='PASS',single_sheet='PASS',catalog_components=len(m['components']),symbol_units=len(json.loads((ROOT/'evidence/library_layout.json').read_text())['catalog']),physical_pins=sum(len(c['pins']) for c in m['components']),stock_library_symbols=len(definitions)-custom,custom_symbols=custom,proposed_net_partitions=len(expected),netlist_partition_comparison='PASS',unintended_multi_pin_nets=0,retained_original_visual_fragments=len(old['nets'])-len(withdrawn),withdrawn_original_visual_fragments=sorted(withdrawn),original_photo_checksums=f'PASS ({len(manifest)} files)',unresolved_physical_pins=len(m['unresolved_pins']),erc_total=len(violations),erc_by_type=dict(counts),erc_status='OPEN FINDINGS - candidate IC pin types checked; unknown board routing remains',gui_open='NOT_TESTED (native CLI validated)',hardware_verification='PARTIAL: recorded U6/Q8 resistance and selected PIC meter/visual routes; user via reports plus photo cross-checks; circuit hypotheses remain; no functional or voltage test',physical_pcb_layout='NOT_CREATED',schematic_sha256=sha(sch),input_zip_sha256=sha(ROOT/'input/PetSafe_KiCad_RE_v01.zip'))
    report['datasheet_symbol_pin_contracts']='PASS (U1: 5 pins; U5: 8 pins; U6: 5 pins; Q8: 6 pins; types, footprints and source properties)'
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
    (ROOT/'evidence/validation_log.txt').write_text('Native KiCad model/netlist cross-check: PASS\n'+json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
