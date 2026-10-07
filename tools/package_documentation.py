from pathlib import Path
import csv,json,shutil,hashlib,html
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'photos';E=R/'evidence';M=json.loads((E/'reconstruction.json').read_text())
# Full-size JPEG companions are convenient for browsing; the PNG mosaics remain the lossless outputs.
for name in ['front_registered','back_mirrored_registered','back_readable']:
 im=Image.open(P/(name+'.png')).convert('RGB');im.save(P/(name+'.jpg'),quality=97,subsampling=0)
O=P/'originals';O.mkdir(exist_ok=True)
nums=[2417,2418,2419,2420,2421,2422,2423,2424,2425,2427,2428]+list(range(2429,2444))
manifest=[]
for n in nums:
 src=Path(f'/mnt/data/IMG_{n}.jpg')
 if not src.exists():src=O/f'IMG_{n}.jpg'
 if src.exists():
  dest=O/src.name
  if src.resolve()!=dest.resolve():shutil.copyfile(src,dest)
  manifest.append({'file':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size})
(E/'original_photo_manifest.json').write_text(json.dumps(manifest,indent=2))
rows=[]
def meas(i,a,b,purpose,method='resistance',expected='UNVERIFIED — record actual reading'):
 rows.append(dict(id=i,from_point=a,to_point_or_search=b,method=method,purpose=purpose,expectation=expected,result_ohm='',matched_pin='',notes=''))
meas('M01','PCB GND','U4 pin 8','Ground reference')
meas('M02','PCB GND','U4 pin 19','Second PIC ground')
meas('M03','PCB GND','U5 pin 6','Driver ground')
meas('M04','U5 pin 6','U5 pin 7','Driver ground pair')
meas('M04b','PCB GND (central pad)','GND pad near C5 at RF end','Check the two separately captured physical ground pads')
meas('M05','PCB GND','BATTERY minus pad','Determine whether a protection element separates raw battery negative')
meas('M06','PCB VDD test point','U4 pin 20','PIC supply domain')
meas('M07','PCB VDD test point','U5 pin 1','Check logic-domain sharing; do not confuse U5 VCC and VDD')
meas('M08','BATTERY plus pad','U5 pin 4','Motor supply route')
for i,a,b in [(9,'CLK','27'),(10,'DAT','28'),(11,'GND','8'),(12,'VDD','20'),(13,'VPP','1')]:
 meas(f'M{i:02}',f'J1 pad labelled {a}',f'U4 pin {b}','Verify programming-header net, not a presumed UART')
meas('M14','U5 pin 5','TP15','Verify local photo trace and pin orientation')
meas('M15','U5 pin 5 then pin 8','Both J5 motor connector contacts','Identify both motor output contacts','find direct trace; record contact description')
sweep='U4 pins 2–7, 11–18 and 21–28; stop on a stable near-probe-resistance match. Record NONE if no match.'
meas('M16','U5 pin 2 (INA)',sweep,'Find first hidden PIC-to-driver connection','resistance search, not beep alone')
meas('M17','U5 pin 3 (INB)',sweep,'Find second hidden PIC-to-driver connection','resistance search, not beep alone')
meas('M18','U3 pin 8','PCB VDD test point','Op-amp positive supply domain')
meas('M19','U3 pin 4','PCB GND','Op-amp negative supply domain')
meas('M20','J3 pin 3 (black wire)','PCB GND','Sensor-cable ground candidate')
meas('M21','J3 pin 1 (red wire)','PCB VDD test point','Sensor-cable supply candidate')
meas('M22','U1 upper-right pad in IMG_2430','PCB VDD test point','Verify visible regulator-region fragment')
meas('M23','U1 middle-left pad in IMG_2430','PCB GND','Resolve unknown five-pin-device ground candidate')
with (E/'measurements_round1.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'docs/MEASUREMENTS.md').write_text('''# First continuity pass — no modifications

Use `evidence/measurements_round1.csv` to record results. No measurements have been prefilled.

Remove all four AA cells and disconnect any external supply. Check that the board has discharged before using resistance/continuity mode. Do not use the meter's resistance mode on a powered circuit. No component removal is required for this batch.

Touch the probes together and record their resistance first. A direct copper connection should be stable and close to that value. A beep alone is not proof: resistors and semiconductor paths can also beep. Record a resistance, or OL; reverse probes when a reading is ambiguous or polarity-dependent. An in-circuit result of several ohms or more is NOT automatically a same-net connection.

## Small first batch

M01–M08 establish ground and supply domains. M09–M13 verify the programming header. M14–M17 map the motor outputs and the two control inputs. Stop there initially if time is limited. M18–M23 extend the map into the analogue supply and sensor interface.

Use `photos/U4_probe_orientation.png` and `photos/U5_probe_orientation.png`. Pin names in a semiconductor datasheet describe the IC, not a confirmed connection elsewhere on this board.

For M16/M17, hold one fine probe on U5's indicated input and sweep the listed PIC pins carefully without bridging neighbours. Record the matching PIC pin and resistance. If there is no near-zero match, report that rather than assuming a connection; a series resistor or intermediate circuit may be present.

## What is deliberately deferred

Do not cut traces, lift IC pins, reprogram the PIC, connect ESP32 outputs, switch battery chemistry or remove the RFID capacitors for this continuity pass. These actions do not help identify the first hidden connections.

The next analogue pass will trace one complete switched-capacitor branch (Q3 with C10/C12/C11), then the two op-amp feedback/input networks. It will use the already established ground/supply nodes to avoid a large blind all-pairs search.

## Values versus connectivity

A connectivity-complete schematic can still contain UNKNOWN capacitor values. A multimeter can establish which pads are joined; it generally cannot uniquely identify an unmarked capacitor value inside a connected filter or resonant network. Later LCR measurements, and sometimes lifting one end, may be needed. Do not infer capacitance, dielectric or voltage rating from physical size.
''')
(R/'README.md').write_text(f'''# PetSafe 100-1339 R03 A — reverse engineering v0.1

## What this package is

A photographic atlas, a native KiCad **initial capture**, an observed-part inventory, and a targeted continuity worksheet for Sergey's PetSafe PPA19-16811. It is **not a complete or electrically verified schematic** and is not a manufacturable replacement-board design.

Open `index.html` for the photographs and searchable inventory. Open `schematic/PetSafe_1001339.kicad_pro` in KiCad (8 or later is the intended target), then the root schematic. Symbols are embedded and also supplied as a local symbol library. There are six child sheets. No external symbol library is required to display the captured symbols.

## Current evidence

- {len(M['components'])} catalog entries: observed designators, test points, named-pad aliases and empty footprints. This is NOT a count of {len(M['components'])} fitted electronic parts.
- {len(M['nets'])} short, locally visible net fragments encoded in the schematic.
- Zero continuity-confirmed nets; 290 modeled pads remain unresolved in this revision.
- Known ICs: U4 PIC16F18855; U5 MX512H; U3 SGM8542XS. U1/U2/U6 and several short-marked devices remain unidentified.
- Unmarked capacitor values are UNKNOWN. Empty footprints are DNP, not zero-ohm links.
- The separate PIR daughterboard is included in the source photographs but is **not reconstructed** yet.

## Photograph outputs

`front_registered.png` combines a perspective-rectified overview with registered detail photographs. Each output pixel is taken from a selected source; there is no inpainting or invented copper. Seams are visible where the selected source changes. `front_source_ids.png` and `front_registration.json` record provenance.

`back_unrectified.png` is the sequential rear mosaic. `back_mirrored_registered.png` aligns the rear to the front for comparison. This is approximate registration, NOT a dimensional or electrical measurement. `back_readable.png` restores readable rear orientation. Full-size JPEG companions support the browser atlas. The original JPEG uploads are included byte-for-byte under `photos/originals/` with SHA-256 checksums.

The compact ZIP omits the large PNG mosaics; full-resolution JPEG companions and original photos are included. Lossless PNG front/rear mosaics are provided separately in the chat. Stitching scripts regenerate PNG outputs from the original photos.

## Layer count

Unconfirmed. The rear looks like a broad copper plane and numerous signal routes disappear at vias without a visible rear track. This raises the possibility of inner routing layers, rather than establishing a two-layer stackup. It is not photographic proof of a four-layer stackup. Electrical endpoint reconstruction is possible without knowing the physical layer used by each net.

## How evidence is represented

`VISUAL_LOCAL`: a short trace is visible in a specific source photograph. This is weaker than continuity confirmation and can be corrected.

`CANDIDATE_NOT_CONNECTED` / `HYPOTHESIS`: plausible relationship recorded outside the schematic. No wire is drawn for it.

`UNRESOLVED_NOT_NC`: the symbol pin is left open because its connection is not known. There are no no-connect flags to make these uncertainties disappear.

Known package pins use datasheet numbering. Unknown ICs/transistors use physical pad IDs; their source-photo orientation is recorded. Passive pin 1 is left/top and pin 2 right/bottom in the cited upright detail photo; this is a reconstruction convention, not a verified PCB-footprint pad numbering system. Multiple photographic ground pads are not silently collapsed into one electrical node.

## Validation performed

`evidence/validation.json` records balanced/native-file structural parsing, existence of child sheets, unique catalog references, matching symbol pins, valid model endpoints and the absence of fabricated no-connect flags. **KiCad is not installed in the execution environment: the native editor has not opened the files, and native ERC/netlist export were not run.** SVG previews are independently generated from the same data; they are not KiCad renderings.

## Continue the work

Start with `docs/MEASUREMENTS.md` and fill `evidence/measurements_round1.csv`. `CODEX_TASK.md` gives the continuation task. The immediate goal is reconstructing the original board, not choosing an ESP32 retrofit circuit.

The generators run with Python 3. `build_reconstruction.py`, `generate_kicad.py` and `validate_structure.py` use the standard library. Photo tools additionally use Pillow, NumPy and OpenCV. Do not overwrite manual KiCad edits blindly: the JSON/CSV model and the generator must be updated in parallel before regenerating.
''')
(R/'AGENTS.md').write_text('''# Project-specific instructions

Reconstruct the AS-BUILT PetSafe 100-1339 R03 A. Do not design a similar generic RFID circuit.

Preserve original photos and their names. Image stitching may warp/register/crop source pixels, but must never inpaint or generate electrical detail. Inspect original sources when a seam affects a trace.

Distinguish visible copper, electrical measurements, datasheet pin definitions and circuit hypotheses. A datasheet proves a pin's function, not its PCB net. No fabricated component values, hidden power connections, net assignments, tests or measurements.

Treat open captured pins as unresolved, not NC. Do not populate empty footprints as zero-ohm links. Do not merge identically named supply pads without evidence. Layer count remains unconfirmed.

Keep the native KiCad project, evidence model and readable documentation in agreement. First validate that the generated project opens in an installed KiCad. Do not claim an ERC pass when checks were not run or suppress unresolved-input errors just to achieve a green report.

Hardware changes, firmware replacement and rechargeable-power redesign are outside this reconstruction task. Ask Sergey for small grouped continuity measurements at named physical pads rather than broad exploratory work.
''')
(R/'CODEX_TASK.md').write_text('''# Codex task: complete the PetSafe as-built schematic reconstruction

## Goal

Continue the attached `PetSafe_RE_v01` project into a complete, evidence-backed KiCad schematic of the existing **100-1339 R03 A** main PCB, then the **100-1398 R001** PIR daughterboard. Preserve original reference designators. This is NOT an ESP32 add-on design task.

## Starting point

Read README.md and AGENTS.md. Inspect the original photographs, not just stitched seams. Open `schematic/PetSafe_1001339.kicad_pro`. The current generated files have only structural validation; first establish that they open in native KiCad and fix any format issues without inventing electrical content. Then export a native netlist and SVG/PDF preview and record exactly which checks ran.

There are 150 catalog entries and 29 visual local net fragments, not a finished netlist. Pin identifiers for unknown packages are physical placeholders. The independent SVG preview is not evidence that KiCad accepted the project.

## Work autonomously where the evidence permits

1. Audit the photo-derived component inventory against all original images. Correct duplicated/missing aliases, reference-designator readings, marking transcription, population status and package pin orientation. Do not invent components merely because a reference number is skipped.
2. Use manufacturer datasheets to resolve IC identities. U3 is SGM8542XS, U4 PIC16F18855 (28-pin SOIC), U5 MX512H. U1 marking PPEK; U2 approximately C14R with six leads; U6 marking uncertain. Short marking matches with a different pin count/package are not acceptable identifications.
3. Expand only genuinely visible copper connections. Each electrical net must retain photo and/or measurement evidence. Update evidence/reconstruction.json, the generator/model and KiCad together. Do not populate a schematic by copying a datasheet application circuit.
4. Incorporate Sergey's measurements from measurements_round1.csv. Use actual resistance readings, not beeper-only guesses. Direct copper, semiconductor paths and resistance through another component are different findings.
5. Trace the full ground/supply domains, ICSP header, motor inputs/outputs, crystal, user switch/LED, PIR interface, receiver and antenna drive/tuning networks. Many apparently isolated vias may connect through hidden layers; the physical route need not be known if endpoint continuity is proven.
6. After the first measurement batch, request only the next small high-information batch with precise pin/pad names and annotated crop references. Complete one tuning branch (Q3, C10/C12/C11) before assuming the topology of the other four. Do not assume those three capacitors are simply parallel.
7. Move from the provisional component-grid capture to readable functional circuitry as nets become established. Keep an unresolved-pins register until every fitted component pin and intentional empty footprint is accounted for.
8. Add the daughterboard as its own hierarchical sheet, preserving its local designators without collisions. Request a clear opposite-side photograph only if needed; do not infer its three-wire protocol or logic level from wire colors.

## Deliverables

A native KiCad project that has actually been opened/exported; readable circuit sheets; an as-built BOM with unknown fields explicit; an evidence-linked netlist; the measurement history; an unresolved-items list; and an updated photo atlas. Capacitor values may require later LCR/isolated measurements. Connectivity completion and value completion must be reported separately.

## Acceptance conditions

No fabricated wires/values, no ambiguous part identified solely by a short code, no unverified ground merges, no NC flags used to hide unknowns. Native exports and ERC results must be reported honestly. Preserve factory firmware and physical hardware. Do not claim completion until every connection has evidence or is explicitly unresolved.
''')
# Browser atlas: all data inline, photos local; no server needed.
data=json.dumps(M).replace('</','<\\/')
page='''<!doctype html><html><head><meta charset="utf-8"><title>PetSafe PCB atlas</title><style>
:root{color-scheme:light}body{margin:0;font:15px system-ui;background:#eef2f5;color:#172b38}header{background:#153644;color:white;padding:24px 30px}h1{margin:0 0 8px;font-size:29px}header p{margin:0;max-width:1050px;line-height:1.5}main{padding:22px 30px}button,a.btn{background:white;border:1px solid #afbdc7;padding:9px 13px;border-radius:5px;color:#163c4c;cursor:pointer;font:inherit;display:inline-block;text-decoration:none;margin:3px}button.active{background:#d8eee9}nav{margin:10px 0}.viewport{height:560px;overflow:auto;background:#cad3d8;border:1px solid #b2c1ca}.viewport img{display:block;max-width:none}.notice{background:#fff5e8;border-left:4px solid #cc852f;padding:13px 18px;line-height:1.5;margin:15px 0}table{border-collapse:collapse;width:100%;background:white}td,th{padding:9px 12px;border-bottom:1px solid #dfe7eb;text-align:left;font-size:13px}th{position:sticky;top:0;background:#dce7ed}input{padding:11px;font:inherit;width:360px;max-width:90%;margin:8px 0}small{color:#4c6472}code{background:#e9eef0;padding:2px 5px}a{color:#17617a}.legend{display:flex;gap:22px;flex-wrap:wrap;margin:12px 0}.legend span{background:white;padding:12px 16px;border-radius:6px}summary{cursor:pointer;padding:14px;background:white;margin-top:14px}</style></head><body>
<header><h1>PetSafe 100-1339 R03 A</h1><p>Photographic atlas and schematic reconstruction • v0.1 • Original board, not an ESP32 redesign.</p></header><main>
<div class="notice"><b>Incomplete photo-led capture.</b> 29 local net fragments; zero continuity-confirmed nets. Unknown pins and values are retained explicitly. Layer count is unconfirmed. The separate PIR board has not yet been reconstructed.</div>
<nav><a class="btn" href="schematic/preview.html">Schematic capture preview</a><a class="btn" href="README.md">Project notes</a><a class="btn" href="evidence/measurements_round1.csv">Continuity worksheet</a><a class="btn" href="CODEX_TASK.md">Codex continuation task</a></nav>
<h2>Registered photographs</h2><nav id="views"><button data-file="front_registered.jpg">Front</button><button data-file="back_readable.jpg">Rear — readable</button><button data-file="back_mirrored_registered.jpg">Rear — aligned / mirrored</button><button onclick="fit()">Fit width</button><button onclick="zoom(.75)">−</button><button onclick="zoom(1.5)">+</button><span id="scale"></span></nav>
<p><small>Scroll horizontally/vertically after zooming. Source selection may create seams. Mirrored rear alignment is approximate, not a net-connectivity test.</small></p>
<div class="viewport" id="vp"><img id="board" src="photos/front_registered.jpg" alt="Stitched PCB photographs"></div>
<div class="legend"><span><b>150</b> catalog entries, including pads and DNPs</span><span><b>29</b> visible local fragments</span><span><b>290</b> unresolved modeled pads</span></div>
<h2>Find a component</h2><input id="query" placeholder="Reference, marking, value, photo or note…"><div style="overflow:auto;max-height:620px"><table><thead><tr><th>Reference</th><th>Value / marking</th><th>Status</th><th>Original photo</th><th>Notes</th></tr></thead><tbody id="inventory"></tbody></table></div>
<details><summary>Recorded local connections</summary><table><thead><tr><th>Net</th><th>Endpoints</th><th>Evidence</th></tr></thead><tbody id="nets"></tbody></table></details>
<p><small>Known pin functions are based on manufacturer documentation. A function does not prove a connection. See evidence/ and docs/ for scope and verification records.</small></p>
</main><script>const data=DATA;const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');const img=document.getElementById('board'),vp=document.getElementById('vp');function fit(){img.style.width=vp.clientWidth+'px';scale()}function scale(){document.getElementById('scale').textContent=Math.round(img.width/img.naturalWidth*100)+'% of mosaic pixels'}function zoom(f){img.style.width=Math.max(300,Math.min(18000,img.width*f))+'px';scale()}img.onload=fit;document.querySelectorAll('[data-file]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-file]').forEach(a=>a.classList.remove('active'));b.classList.add('active');img.src='photos/'+b.dataset.file});function inventory(){let q=document.getElementById('query').value.toLowerCase();document.getElementById('inventory').innerHTML=data.components.filter(c=>JSON.stringify(c).toLowerCase().includes(q)).map(c=>'<tr><td><b>'+esc(c.ref)+'</b></td><td>'+esc(c.value)+'<br><small>'+esc(c.marking)+'</small></td><td>'+esc(c.population)+'<br>'+c.traced_pin_count+'/'+c.pins.length+' pads traced locally</td><td>'+c.source.split(';').map(s=>'<a href="photos/originals/'+esc(s)+'">'+esc(s)+'</a>').join('<br>')+'</td><td>'+esc(c.note)+'</td></tr>').join('')}document.getElementById('query').oninput=inventory;inventory();document.getElementById('nets').innerHTML=data.nets.map(n=>'<tr><td>'+esc(n.net)+'</td><td>'+esc(n.endpoints.join(' — '))+'</td><td>'+esc(n.evidence)+'<br>'+esc(n.source)+'</td></tr>').join('');</script></body></html>'''.replace('DATA',data,1)
(R/'index.html').write_text(page)
print('Documentation, worksheet, browser atlas, full-size JPEGs and',len(manifest),'original photos saved.')
