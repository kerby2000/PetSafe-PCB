"""Build the offline review page and tabular working inventory (standard library)."""
from pathlib import Path
import json, csv, html, hashlib
from collections import Counter
from current_state import current_state, component_summary
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'evidence/reconstruction.json').read_text())
layout=json.loads((R/'evidence/library_layout.json').read_text())
baseline_record=layout['baseline_record']
paper=json.loads((R/baseline_record).read_text()).get('paper','A2')
v=json.loads((R/'evidence/validation.json').read_text())
# Keep the tabular net and gap views synchronized with the exported model.
with (R/'evidence/proposed_nets.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['net','status','endpoints','retained_original_fragments'])
    for n in sorted(m['nets'],key=lambda n:n['net']):w.writerow([n['net'],n['status'],';'.join(n['endpoints']),';'.join(n.get('original_fragments',[]))])
components={c['ref']:c for c in m['components']}
with (R/'evidence/unresolved_pins.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['original_ref','pin','reason'])
    for ep in m['unresolved_pins']:
        ref,pin=ep.rsplit('.',1);w.writerow([ref,pin,'Unpopulated footprint' if components[ref]['population']=='DNP' else 'Trace / function unresolved; no certified NC flag'])
status=current_state()
queue=json.loads((R/'evidence/finishing_measurements.json').read_text(encoding='utf-8'))
(R/'evidence/completion_status.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
rows=[]
with (R/'evidence/components.csv').open('w',newline='',encoding='utf-8') as f:
    fields=['original_ref','kicad_ref','observed_value','proposed_value','marking','population','source','hypothesis','unresolved_pin_count','library_symbol','footprint']
    wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader()
    for c in m['components']:
        d=dict(original_ref=c['ref'],kicad_ref=m['reference_map'].get(c['ref'],c['ref']),observed_value=c['value'],proposed_value=c.get('proposed_value',c['value']),marking=c.get('marking',''),population=c.get('population',''),source=c.get('source',''),hypothesis=component_summary(c),unresolved_pin_count=sum(e.startswith(c['ref']+'.') for e in m['unresolved_pins']))
        d['library_symbol']=c.get('library_symbol','');d['footprint']=c.get('footprint','');wr.writerow(d);photos=' '.join(f'<a href="photos/originals/{html.escape(p)}">{html.escape(p)}</a>' for p in d['source'].split(';') if p)
        rows.append('<tr>'+''.join('<td>'+html.escape(str(d[k]))+'</td>' for k in fields[:6])+f'<td>{photos}</td><td>{html.escape(d["hypothesis"])}</td></tr>')
esc=html.escape
railrows=''.join('<tr><td><b>'+esc(r['name'])+'</b></td><td>'+esc(r['board_label'])+'</td><td>'+esc(r['path'])+'</td></tr>' for r in status['rails'])
planrows=''.join('<tr><td><b>'+esc(g['title'])+'</b><br>'+esc(g['scope'])+'</td><td>'+esc(g['summary'])+'</td><td>'+esc(g['next_action'])+'<br>'+ ' '.join('<a href="docs/FINISHING_CHECKLIST.html#'+esc(i)+'">'+esc(i)+'</a>' for i in g['issues'])+'</td></tr>' for g in status['finish_plan'])
settled=''.join('<li>'+esc(t)+'</li>' for t in status['settled_summary'])
work=json.loads((R/'evidence/remaining_work.json').read_text())
openrows=''.join('<tr><td><a href="docs/OPEN_ITEMS.md#'+esc(i['id'].lower())+'">'+esc(i['id'])+'</a></td><td>'+esc(i['area'])+'</td><td>'+esc(i['category'])+'</td><td>'+esc(i['unknown'])+'</td></tr>' for i in status['items'])
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe PCB - current reconstruction</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#f4f5f3;color:#1c2e2c;font:16px/1.55 system-ui}}main{{max-width:1500px;margin:auto;padding:28px}}h1{{font-size:34px}}a{{color:#006d64}}nav,.toolbar{{display:flex;flex-wrap:wrap;gap:14px;margin:20px 0}}button{{padding:7px 14px}}.viewer{{overflow:auto;background:white;border:1px solid #bccdc7}}.viewer img{{display:block;width:100%;max-width:none}}.board{{width:100%;height:auto}}table{{border-collapse:collapse;background:white;width:100%;font-size:14px}}th,td{{padding:12px;border-bottom:1px solid #d5e0da;text-align:left;vertical-align:top}}th{{background:#e6ede8}}.scroll{{overflow:auto}}details{{padding:16px;background:#eaf0ec;margin:20px 0}}summary{{cursor:pointer}}input[type=search]{{padding:10px;width:100%;max-width:600px;margin:14px 0}}.note{{border-left:4px solid #b87516;padding:12px 18px;background:#fff6dd}}footer{{margin-top:30px}}</style>
<main><p>PetSafe PPA19-16811 | Main board 100-1339 R03 A | {esc(m['revision'])}</p><h1>PCB photographs and reconstructed schematic</h1>
<p>One {esc(paper)} sheet with {status['catalog_entries']} catalog entries. Connections and device qualifications remain under review. <b>No routed reproduction PCB exists.</b></p>
<nav><a href="README.md">Prototype overview</a><a href="#schematic">Schematic</a><a href="#pcb">Physical PCB</a><a href="#open">Open items</a><a href="#evidence">Evidence and rebuild</a></nav>
<h2 id="schematic">Current schematic</h2><p><a href="output/pdf/PetSafe_single_sheet.pdf">PDF</a> | <a href="schematic/PetSafe_1001339.kicad_pro">KiCad project</a> | <a href="schematic/PetSafe_1001339.kicad_sch">Editable schematic</a></p>
<div class="toolbar"><button id="fit">Fit sheet</button><label>Zoom <input id="zoom" type="range" min="100" max="500" value="100" step="25"></label><output id="zvalue">100%</output><a href="output/svg/PetSafe_1001339.svg">Full native preview</a></div><div class="viewer"><img id="drawing" src="output/svg/PetSafe_1001339.svg" alt="Current one-sheet native KiCad schematic"></div>
<p class="note">{status['modeled_nets']} model/native net partitions agree; {status['erc_total']} ERC findings: the deliberately retained U6/U6A conflict. The three reported receiver joins resolve the four previous receiver findings without exclusions. These are file checks, not proof of every hidden connection. All 44 starred capacitor values are estimates; original values remain unconfirmed.</p>
<h2 id="bridge">Working external button bridge</h2><p>The native drawing retains the USB-powered ESP32-C6 SuperMini: GPIO3 drives a 2N3904 through 4.7 kΩ, with 100 kΩ from base to emitter. Collector joins H_BUTTON/S1.2; emitter and ESP32 ground join GND/S1.1. The owner has assembled and tested the perfboard. Firmware v0.1.0 is flashed; web/API startup checks passed and the owner confirms remote motor/button action. The owner confirms installation and USB-C power into the ESP, its 5V pad to PetSafe battery-positive with cells removed and converter output disconnected. Power margins remain unverified; see the wiring guide. The dashed block is external to the factory board.</p><p><a href="docs/BUTTON_BRIDGE.md">Add-on BOM, physical wiring and assembly qualifications</a> · <a href="firmware/button_bridge/README.md">Firmware: local web control, HTTP API and flashing</a> · <a href="schematic/ButtonBridge.3dshapes/ESP32-C6-SuperMini-owner.step">Owner-supplied STEP model</a>. Brief HIGH toggles the button mode; this is not absolute OPEN/CLOSE control. Basic commissioning is complete; camera integration waits for the camera. TPL5111/PIR wake is deferred; no carrier PCB layout is included.</p>
<h2 id="pcb">Actual physical PCB</h2><a href="photos/two_sides_overview.jpg"><img class="board" src="photos/two_sides_overview.jpg" alt="Front and rear original-photo mosaics of the actual PCB"></a>
<p>Photographic mosaics use original pixels. The rear is mirrored and approximately registered for comparison; alignment does not establish buried copper or dimensions. <a href="photos/back_readable.jpg">Rear, readable orientation</a> | <a href="photo-atlas-v01.html">Original-photo atlas</a> | <a href="docs/VIA_REVIEW.html">Existing via/photo viewer</a></p>
<h2 id="open">Remaining open items</h2><p><a href="docs/OPEN_ITEMS.md">GitHub-readable register</a> | <a href="docs/FINISHING_CHECKLIST.html">Detailed HTML view</a>. Generated from <a href="evidence/remaining_work.json">one authoritative register</a>.</p>
<p>{esc(work['owner_action_summary'])} TP11/TP17 possible hidden continuations are an accepted reconstruction boundary, not proved intentional non-use. <a href="docs/TOPOLOGY_AUDIT.md">Independent connection audit</a>.</p>
<div class="scroll"><table><thead><tr><th>ID</th><th>Area</th><th>Category</th><th>Unresolved claim</th></tr></thead><tbody>{openrows}</tbody></table></div>
<h2 id="evidence">Evidence and rebuild</h2><p><a href="docs/RECONSTRUCTION.md">Current circuit interpretation</a> | <a href="docs/MEASUREMENTS.md">Recorded measurements</a> | <a href="docs/CAPACITOR_VALUE_REVIEW.html">Preserved capacitor estimates</a> | <a href="evidence/validation.json">Native validation</a> | <a href="docs/history/README.md">Investigation history</a></p>
<p><a href="docs/REBUILD.md">Native-project use and optional audit rebuild instructions</a> explain KiCad 10 library paths, Python requirements and the full-history requirement. Firmware setup is separate. <a href="docs/PUBLICATION.md">Publication preparation and licensing proposal</a>; no release or Pages deployment is enabled.</p>
<details><summary>Rail map</summary><table><thead><tr><th>Net</th><th>PCB label</th><th>Supported path</th></tr></thead><tbody>{railrows}</tbody></table></details>
<details><summary>Searchable component inventory and source photos</summary><input id="search" type="search" aria-label="Filter components" placeholder="Find U6, R39, DNP or a photo"><div class="scroll"><table id="inventory"><thead><tr><th>Original</th><th>KiCad</th><th>Observed value</th><th>Candidate</th><th>Marking</th><th>Population</th><th>Photos</th><th>Evidence / qualification</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>
<footer>Original photos, numeric measurements and negative results preserved. <a href="evidence/proposed_nets.csv">Modeled nets</a> | <a href="https://github.com/kerby2000/PetSafe-PCB/pull/1">Merged architect review PR #1</a></footer></main>
<script>const zoom=document.getElementById('zoom'),drawing=document.getElementById('drawing'),zvalue=document.getElementById('zvalue');function change(){{drawing.style.width=zoom.value+'%';zvalue.textContent=zoom.value+'%'}}zoom.addEventListener('input',change);document.getElementById('fit').onclick=()=>{{zoom.value=100;change()}};document.getElementById('search').oninput=e=>{{const q=e.target.value.toLowerCase();document.querySelectorAll('#inventory tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}};</script></html>'''
def md(text):return text.replace('|','/').replace('\n',' ')
summaryrows='\n'.join('| ['+i['id']+'](docs/OPEN_ITEMS.md#'+i['id'].lower()+') | '+md(i['area'])+' | '+md(i['category'])+' |' for i in status['items'])
readme=f'''# PetSafe microchip cat-flap reverse engineering and remote-button retrofit

[![Installed PetSafe flap with the working USB-powered retrofit](photos/publication/installed-flap.jpg)](docs/BUTTON_BRIDGE.md#installed-placement)

*Owner's installed prototype in a temporary cardboard fit-test insert. This is not a permanent weatherproof installation.*

An **ESP32-C6 SuperMini and one transistor operate the original PetSafe button remotely** from a local web page or authenticated HTTP API. The owner reports successful remote button/motor operation and installation. The original S1 button, PIC controller and motor driver remain in use.

**PetSafe PPA19-16811 · main board 100-1339 R03 A · firmware 0.1.0 · schematic {m['revision']}**

## What works and what remains

| Status | Scope |
|---|---|
| Demonstrated | Owner-reported remote button press, motor response/delayed return and installation; firmware flash/boot and authenticated HTTP status checks recorded. |
| Planned | Camera/prey recognition and automatic admission. Neither is implemented or demonstrated. |
| Unknown | Independent OPEN/CLOSE state and latch position; the API reports button-output status, not door state. Power margins, failure behavior and long-term reliability remain qualified. |
| Reconstruction | One {paper} schematic; {status['modeled_nets']} modeled factory net partitions agree with KiCad. All **44 starred capacitor values are estimates**. **No routed reproduction PCB exists.** |

This is a working prototype, not a finished prey detector, secure access-control product or exact factory schematic. A press can toggle the current mode; a lost response must not trigger a fresh automatic retry.

## Short demo

[Watch the silent bench excerpt](photos/publication/remote-button-bench-excerpt.mp4) — the final 11.7 seconds of the owner's bench demonstration, following an off-screen remote command. It shows the original mechanism, not AI recognition or the final installed power routing. The full clip stays local because it includes a private chat on the monitor; [media details and release preparation](docs/PUBLICATION.md#demo).

## Build the minimal retrofit

| Quantity | Part | Connection |
|---|---|---|
| 1 | ESP32-C6 SuperMini | GPIO3 drives the base resistor; GND joins PetSafe GND. |
| 1 | 2N3904 NPN | Collector → H_BUTTON/S1 pin 2; emitter → GND/S1 pin 1. Confirm the actual part's lead order. |
| 1 | 4.7 kΩ resistor | GPIO3 → transistor base. |
| 1 | 100 kΩ resistor | Base → emitter, on the transistor side of the 4.7 kΩ resistor. |
| As needed | Insulated wire, isolated-pad perfboard and mounting insulation | Preserve the original button and factory circuitry. |

[Wiring, transistor pin mapping and installation photos](docs/BUTTON_BRIDGE.md) · [Owner-confirmed USB power arrangement and its limits](docs/BUTTON_BRIDGE.md#current-wired-power-direction)

Installed power: USB-C into the ESP, its 5V header to PetSafe battery-positive, common ground, **AA cells removed**, external converter output disconnected. The ESP uses its onboard 3.3 V regulator. This records the owner's build; it does not qualify the header/trace for motor current or establish source isolation. The native schematic retains the separate-positive-supply reference drawing. Do not parallel external power with alkaline cells or two regulator outputs.

## Firmware setup and use

Follow the [ESP-IDF v6.0.2 configuration/build instructions](firmware/button_bridge/README.md#build-and-configure), then the [first-flash instructions](firmware/button_bridge/README.md#flash-or-update-a-prototype). Configure Wi-Fi and a private token locally; configured binaries contain credentials and must not be published.

The [local web page and HTTP API](firmware/button_bridge/README.md#http-api) issue an authenticated 200 ms GPIO3 pulse with duplicate protection and a five-second cooldown. HIGH presses, LOW releases. Keep this HTTP control service on a trusted local network; do not expose it to the internet. Camera decisions can later use the existing client, but there is no camera integration in this version. TPL5111/PIR wake is deferred.

## Reconstructed schematic and evidence

[PDF](output/pdf/PetSafe_single_sheet.pdf) · [Editable KiCad project](schematic/PetSafe_1001339.kicad_pro) · [Schematic](schematic/PetSafe_1001339.kicad_sch) · [Existing investigation viewer](index.html)

[![Current native schematic preview](output/svg/PetSafe_1001339.svg)](output/pdf/PetSafe_single_sheet.pdf)

The **U6/U6A regulator-output ERC conflict is deliberately retained**. File consistency is not proof of every physical connection. Capacitor estimates, observed values, original photographs, measurements and negative results remain distinct and preserved.

[Original-photo atlas](photo-atlas-v01.html) · [Front/rear PCB mosaics](photos/two_sides_overview.jpg) · [Via/photo viewer](docs/VIA_REVIEW.html) · [Physical-evidence audit](docs/TOPOLOGY_AUDIT.md) · [Current interpretation](docs/RECONSTRUCTION.md) · [Measurements](docs/MEASUREMENTS.md) · [Capacitor estimates](docs/CAPACITOR_VALUE_REVIEW.html)

## Remaining work

The [existing register](docs/OPEN_ITEMS.md) and [HTML checklist](docs/FINISHING_CHECKLIST.html) both use [remaining_work.json](evidence/remaining_work.json). There is no second checklist or completion PDF.

| ID | Area | Category |
|---|---|---|
{summaryrows}

{work['owner_action_summary']} TP11/TP17 hidden continuations remain an explicit reconstruction boundary. Package geometry, routing/stackup, external assemblies and original firmware remain prerequisites for a factory-board reproduction.

## Rebuild and publication

[Ordinary native-project use versus optional audit regeneration](docs/REBUILD.md) · [Native validation](evidence/validation.json) · [Source/provenance register](docs/SOURCES.md) · [Licensing proposal and draft prototype release](docs/PUBLICATION.md) · [Investigation history](docs/history/README.md)

There is no top-level project license yet; public visibility is not a uniform open-source license. Third-party notices and the STEP model's noncommercial terms remain in force. Licensing, any release tag and Pages hosting await owner approval. No release or hosted control service is published by this preparation.

**Unofficial independent project; not affiliated with or endorsed by PetSafe or Radio Systems Corporation.**
'''

(R/'README.md').write_text(readme,encoding='utf-8',newline='\n')
(R/'index.html').write_text(page,encoding='utf-8',newline='\n')
sources=[]
for p in sorted((R/'docs/datasheets').glob('*.pdf')):sources.append(dict(file=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(R/'evidence/datasheet_manifest.json').write_text(json.dumps(sources,indent=2),encoding='utf-8',newline='\n')
print('Offline review and working inventory generated.')
