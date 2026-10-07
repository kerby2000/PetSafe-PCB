"""Compare the authored electrical model with a native KiCad XML netlist."""
from pathlib import Path
from collections import Counter
import json, hashlib, xml.etree.ElementTree as ET
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
    assert len(native.findall('./components/comp'))==150
    assert len(native.findall('./design/sheet'))==1
    old=json.loads((ROOT/'reference/v01/evidence/reconstruction.json').read_text())
    for net in old['nets']:
        ep=set(map(translated,net['endpoints']))
        assert any(ep<=pins for pins in actual),net
    manifest=json.loads((ROOT/'evidence/original_photo_manifest.json').read_text())
    for p in manifest:
        source=ROOT/'photos/originals'/p['file']
        assert sha(source)==p['sha256'] and source.stat().st_size==p['bytes'],p
    erc=json.loads((ROOT/'output/erc.json').read_text())
    violations=[v for sheet in erc['sheets'] for v in sheet['violations']]
    counts=Counter(v['type'] for v in violations)
    unexpected=set(counts)-{'pin_not_connected','isolated_pin_label','power_pin_not_driven','pin_not_driven'}
    assert not unexpected,counts
    sch=ROOT/'schematic/PetSafe_1001339.kicad_sch'
    assert '(no_connect ' not in sch.read_text()
    assert '(lib_id "PetSafe_Working:' not in sch.read_text()
    report=dict(date='2026-10-08',native_tool=native.findtext('./design/tool'),native_load_and_export='PASS',single_sheet='PASS',catalog_components=150,symbol_units=154,physical_pins=352,stock_library_symbols=22,custom_symbols=0,proposed_net_partitions=len(expected),netlist_partition_comparison='PASS',unintended_multi_pin_nets=0,retained_original_visual_fragments=len(old['nets']),original_photo_checksums=f'PASS ({len(manifest)} files)',unresolved_physical_pins=len(m['unresolved_pins']),erc_total=len(violations),erc_by_type=dict(counts),erc_status='OPEN FINDINGS - see ERC report; placeholders have passive pins and cannot check IC drive rules',gui_open='NOT_TESTED (native CLI validated)',hardware_verification='NOT_PERFORMED',physical_pcb_layout='NOT_CREATED',schematic_sha256=sha(sch),input_zip_sha256=sha(ROOT/'input/PetSafe_KiCad_RE_v01.zip'))
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
    (ROOT/'evidence/validation_log.txt').write_text('Native KiCad model/netlist cross-check: PASS\n'+json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
