"""Verify stock-footprint existence and logical pad coverage; does not validate physical fit."""
from pathlib import Path
import argparse, os, json, hashlib, xml.etree.ElementTree as ET
import sexpdata as sx
from inventory_contracts import verify_bridge_asset_bytes
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--footprints',default=os.environ.get('KICAD10_FOOTPRINT_DIR'),help='KiCad 10 footprint directory; defaults to KICAD10_FOOTPRINT_DIR')
args=parser.parse_args()
if not args.footprints:parser.error('Set KICAD10_FOOTPRINT_DIR or pass --footprints; see docs/REBUILD.md')
F=Path(args.footprints).resolve()
m=json.loads((R/'evidence/reconstruction.json').read_text())
net=ET.parse(R/'output/PetSafe_netlist.xml')
report=[]
for c in m['components']:
    ref=m['reference_map'].get(c['ref'],c['ref'])
    comp=net.find(f'./components/comp[@ref="{ref}"]')
    assert (comp.findtext('footprint') or '')==c['footprint'],ref
    if not c['footprint']:continue
    lib,name=c['footprint'].split(':');p=F/(lib+'.pretty')/(name+'.kicad_mod')
    assert p.is_file(),p
    t=sx.loads(p.read_text());pads={str(e[1]) for e in t if isinstance(e,list) and str(e[0])=='pad' and str(e[1])}
    part=comp.find('libsource');l=net.find(f'./libparts/libpart[@lib="{part.attrib["lib"]}"][@part="{part.attrib["part"]}"]')
    pins={e.attrib['num'] for e in l.findall('./pins/pin')}
    assert pins<=pads,(ref,pins,pads)
    if ref=='J1':
        numbered={str(e[1]):e for e in t if isinstance(e,list) and str(e[0])=='pad' and str(e[1])}
        assert str(numbered['1'][3])=='rect', 'J1 pin 1 must mark the photographed square-pad VPP end'
        positions={n:next(e[1:3] for e in p if isinstance(e,list) and str(e[0])=='at') for n,p in numbered.items()}
        assert set(positions)=={'1','2','3','4','5'}
        assert len({xy[0] for xy in positions.values()})==1, 'J1 must have one sequential row'
        ys=[float(positions[str(n)][1]) for n in range(1,6)]
        assert all(abs(ys[n]-ys[n-1]-2.54)<1e-6 for n in range(1,5)), 'J1 sequential pad order/pitch mismatch'
    report.append(dict(ref=c['ref'],native_ref=ref,footprint=c['footprint'],symbol_pins=sorted(pins),footprint_pads=sorted(pads),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len(report)==sum(bool(c['footprint']) for c in m['components'])
for ref in ['R29','R44']:assert net.find(f'./components/comp[@ref="{ref}"]').findtext('value')=='15k'
out=dict(revision=m['revision'],result='PASS: file existence, native/model agreement, symbol-pin coverage',physical_fit='NOT VERIFIED: photo-based candidates',assigned=len(report),unassigned=[c['ref'] for c in m['components'] if not c['footprint']],components=report)
external=[]
for c in m.get('external_button_bridge',{}).get('components',[]):
    lib,name=c['footprint'].split(':')
    source=(R/'schematic' if lib=='TrailCurrentFootprints' else F)/(lib+'.pretty')/(name+'.kicad_mod')
    t=sx.loads(source.read_text(encoding='utf-8'))
    pads={str(e[1]) for e in t if isinstance(e,list) and str(e[0])=='pad' and str(e[1])}
    comp=net.find('./components/comp[@ref="'+c['reference']+'"]');part=comp.find('libsource')
    symbol=net.find('./libparts/libpart[@lib="'+part.attrib['lib']+'"][@part="'+part.attrib['part']+'"]')
    assert {p.attrib['num'] for p in symbol.findall('./pins/pin')}<=pads
    if c['reference']=='Q201':assert pads=={'1','2','3'}  # Stock E/B/C mapping verified in native check.
    if c['reference']=='U201':
        assert pads=={str(p) for p in range(1,21)}
        verify_bridge_asset_bytes(source.read_bytes(),m['external_button_bridge']['library_files'],'footprint_sha256')
        models=[e for e in t if isinstance(e,list) and str(e[0])=='model']
        assert len(models)==1 and models[0][1]=='${KIPRJMOD}/ButtonBridge.3dshapes/ESP32-C6-SuperMini-owner.step'
        model_path=R/'schematic/ButtonBridge.3dshapes/ESP32-C6-SuperMini-owner.step'
        verify_bridge_asset_bytes(model_path.read_bytes(),m['external_button_bridge']['library_files'],'owner_step_sha256')
    external.append(dict(reference=c['reference'],footprint=c['footprint'],pins_covered=True,physical_fit='PENDING: owned-part lead order / module geometry'))
out['external_button_bridge']=external
(R/'evidence/footprint_validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(out['result'],out['assigned'])
