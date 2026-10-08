"""Verify stock-footprint existence and logical pad coverage; does not validate physical fit."""
from pathlib import Path
import json, hashlib, xml.etree.ElementTree as ET
import sexpdata as sx
R=Path(__file__).resolve().parents[1]
F=Path.home()/'AppData/Local/Programs/KiCad/10.0/share/kicad/footprints'
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
    report.append(dict(ref=c['ref'],native_ref=ref,footprint=c['footprint'],symbol_pins=sorted(pins),footprint_pads=sorted(pads),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len(report)==147
for ref in ['R29','R44']:assert net.find(f'./components/comp[@ref="{ref}"]').findtext('value')=='15k'
out=dict(revision=m['revision'],result='PASS: file existence, native/model agreement, symbol-pin coverage',physical_fit='NOT VERIFIED: photo-based candidates',assigned=len(report),unassigned=['C5','S1','LED1'],components=report)
(R/'evidence/footprint_validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(out['result'],out['assigned'])
