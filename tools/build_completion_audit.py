"""Separate value, package and routing gaps for the next hardware checks."""
from pathlib import Path
from collections import Counter
import json, csv, html

R=Path(__file__).resolve().parents[1]
m=json.loads((R/'evidence/reconstruction.json').read_text())
openpins=Counter(p.rsplit('.',1)[0] for p in m['unresolved_pins'])
rows=[]
for c in m['components']:
    ref=c['ref'];kind=c['kind'];pop=c['population'];method=[]
    if pop=='DNP':
        gap='Unpopulated option: no fitted value to recover'
    elif ref=='C5':
        gap='User sleeve reading: 470 uF / 16 V; exact can dimensions still needed'
        method=['Can diameter and lead-centre spacing for footprint']
    elif kind=='C':
        gap='Capacitance not recovered; displayed numerical values are estimates'
        method=['Read sleeve and measure can/lead spacing' if ref=='C5' else 'LCR: in-circuit screening first; isolate one terminal if an individual value is needed']
    elif kind=='R':
        gap='Nominal resistance recovered from marking; tolerance and exact maker not established'
    elif kind=='L':
        gap='Inductor versus ferrite bead and value unresolved';method=['LCR at stated frequency; DC resistance; photo cannot establish RF impedance']
    elif kind=='TP':
        gap='Board pad: no component value required'
    else:
        gap=c.get('hypothesis') or c.get('note') or 'See component identification evidence'
        if ref in ['D2','D3','D4','D5','D6','LED1']:method+=['Diode-mode readings and continuity; markings are already recorded; check PIC trace audit before requesting continuity']
        elif ref=='S1':method+=['Measure common leg pairs with switch released and pressed']
        elif '?' in c.get('proposed_value',c['value']):method+=['Candidate identity: confirm pin functions/routing; a short top code may not identify one manufacturer']
    if openpins[ref] and pop!='DNP':method+=['Targeted continuity for '+str(openpins[ref])+' open physical pads']
    if not c['footprint']:method+=['Photo with ruler/body and lead measurements for exact footprint']
    rows.append(dict(ref=ref,native_ref=m['reference_map'].get(ref,ref),population=pop,
        observed=c['value'],displayed=c.get('proposed_value',c['value']),marking=c.get('marking',''),
        value_or_identity=gap,footprint=c['footprint'],footprint_confidence=c['footprint_confidence'],
        footprint_basis=c['footprint_basis'],open_pads=openpins[ref],next_method='; '.join(method) or 'No immediate measurement requested',photos=c['source']))
report=dict(revision=m['revision'],instruments=['LCR meter','multimeter'],
    footprint_assigned=sum(bool(r['footprint']) for r in rows),footprint_blank=[r['ref'] for r in rows if not r['footprint']],
    fitted_capacitors=sum(c['kind']=='C' and c['population']=='populated' for c in m['components']),
    fitted_resistors=sum(c['kind']=='R' and c['population']=='populated' for c in m['components']),
    unresolved_physical_pins=len(m['unresolved_pins']),
    warning='Open-pad counts do not include every inferred route. Assigned footprints are candidates, not measured reproductions.',components=rows)
(R/'evidence/completion_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
with (R/'evidence/completion_audit.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
e=html.escape
body=[]
for r in rows:
    photos=' '.join(f'<a href="../photos/originals/{e(p)}">{e(p)}</a>' for p in r['photos'].split(';') if p)
    body.append('<tr>'+''.join('<td>'+e(str(r[k]))+'</td>' for k in ['ref','population','observed','displayed','value_or_identity','footprint','footprint_confidence','open_pads','next_method'])+'<td>'+photos+'</td></tr>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>PetSafe - finishing audit</title>
<style>body{font:15px/1.5 system-ui;background:#f3f6f4;color:#173b35;margin:30px}h1{font-size:32px}p{max-width:1100px}a{color:#006f64}.cards{display:flex;gap:15px;flex-wrap:wrap}.cards div{padding:18px;background:white;border:1px solid #b9ccc4;border-radius:8px;min-width:180px}.cards strong{display:block;font-size:26px}.table{overflow:auto;max-height:70vh;background:white}table{border-collapse:collapse;font-size:13px;min-width:1600px}td,th{padding:10px;border-bottom:1px solid #d5e0da;text-align:left;vertical-align:top}th{position:sticky;top:0;background:#dce8e1}td:nth-child(5),td:nth-child(9){min-width:280px}input{font:inherit;padding:12px;width:550px;max-width:90%;margin:20px 0}.note{background:#fff1cc;padding:15px}li{margin-bottom:9px}</style>
<h1>What remains to finish the main-board schematic</h1><p>v0.9.2 | One sheet, 150 catalog entries. Each question mark needs a specific kind of evidence. A package assignment does not establish capacitance or verify a wire.</p>
<div class="cards"><div><strong>147 / 150</strong>footprints assigned</div><div><strong>3</strong>blank: C5, S1, LED1</div><div><strong>44</strong>fitted capacitor values unrecovered</div><div><strong>8</strong>PIC pins still open</div></div>
<p><b>v0.7 update:</b> C5 is 470uF / 16V from the user. C11 3.2 x 1.5 mm supports 1206; R8 1.6 x 0.77 mm supports 0603. Fitted resistor family estimates revised to 0603; other resistor bodies are not individually measured. <a href="../output/pdf/PetSafe_PIC_trace_review.pdf">PIC photo tracing</a> recovers five GPIO local routes and corrects earlier supply assumptions.</p><p><b>Previous v0.6 work:</b> 126 stock footprint assignments through KiCad MCP. R29 and R44 both read 18C in the existing photos: nominal 15 kohm. All 38 fitted resistors now have a nominal value from their markings. Their exact tolerance/maker is not recovered.</p>
<p><b>Footprints:</b> fitted resistors now use 0603 candidates (1.6 x 0.8 mm), based on the user R8 measurement; larger tuning capacitors appear 1206 (3.2 x 1.6 mm). These are photo-based families. Connector pitches, test-pad drills and J5's XH-like housing are lower confidence. J1's square-pad/VPP orientation still needs reconciliation with the present logical numbering.</p>
<p class="note"><b>Electrical gaps:</b> 37 open pads = 18 on populated entries (including test pads and two internal NC pins) + 19 on empty options. Existing drawn wires also include hypotheses. The native KiCad check validates file connectivity against the model; it does not prove the board.</p>
<h2>v0.9.2 via review</h2><p>111 distinct via IDs reviewed; 120 active sites / 127 stable IDs. The latest 19-site batch excludes V117/V120/V121/V122/V124 without renumbering. V113/V115 now correctly point to Q8 centre B2/pin5, GND; the old outer-pad annotation is withdrawn. V077 confirms C19.2/R29.2 are GND, replacing the earlier clamp/op-amp-input guesses. V091/R11, V097/R16, V102/R15 and V108/R14 identify tuning-control resistor ends, with onward GPIOs unknown. V114 reaches the opposite centre T2/pin2, but its earlier GND assignment versus source-supply hypothesis remains unresolved. V075 identifies Q7; exact terminal remains unspecified. <a href="VIA_REVIEW.html">Via viewer</a> · <a href="../output/pdf/PetSafe_completion_status.pdf">Complete status</a>.</p><h2>Current PIC tracing request</h2><p>Eight GPIO pads remain open: 5, 6, 7, 11, 13, 15, 16, 21. RC1/pin12 now reaches VREF/V053, with its onward net unresolved. RC4/15 reaches V022; RC5/16 reaches V023; RB0/21 reaches V026 (user correction); V025 is GND. <a href="../output/pdf/PetSafe_PIC_GPIO_pin_map.pdf">Updated numbered close-up</a> and <a href="../evidence/pic_gpio_status.csv">complete pin status CSV</a>. Under-body candidates V036/V037/V039/V047/V049 are alignment hypotheses only, not confirmed routes.</p><h2>Other outstanding checks</h2><ol><li><a href="../output/pdf/PetSafe_next_checks.pdf">D2 annotated guide:</a> six diode-mode readings, swapping probe direction for each pair. Battery and programmer disconnected. No desoldering requested.</li><li><b>C5:</b> 470uF / 16V is recorded; only can diameter and lead-centre spacing remain for its footprint.</li><li><b>Package scale:</b> R8 and C11 dimensions are recorded. The user confirms R8 included both metal end caps: its 0603 size match is resolved. Other resistor bodies remain individually unmeasured.</li></ol>
<p><b>Next LCR round:</b> start with C6 and one tuning cell (C10/C11/C12), recording meter frequency and mode. In-circuit values can include several capacitors and semiconductor paths; treat them as network readings. Only lift one end later if a specific individual value cannot otherwise be recovered. Do not remove all capacitors. The RF values deserve priority over ordinary bypass estimates.</p>
<p><b>Photos versus measurement:</b> photos help with sleeve text, markings, dimensions and visible traces. They cannot reveal an unmarked ceramic's capacitance, voltage rating or dielectric. Continuity is needed for hidden GPIO destinations; a typical PIC application cannot determine the board's GPIO assignments.</p>
<p><b>Remaining identity work:</b> D2/4P is unidentified. D4/D5/5U and D6/G3 are marking-based candidates; diode mode alone cannot establish a Zener voltage. U6/Q8 pin-map candidates are implemented; external wiring and exact fitted manufacturer remain partly uncertain. S1 common pairs and LED1 polarity are also provisional.</p>
<input id="q" type="search" placeholder="Filter by reference, LCR, continuity, footprint, photo..." aria-label="Filter audit"><div class="table"><table><thead><tr><th>Reference</th><th>Population</th><th>Observed</th><th>Proposed</th><th>Value / identity evidence</th><th>Stock footprint</th><th>Package confidence</th><th>Open pads</th><th>How to resolve</th><th>Photos</th></tr></thead><tbody>ROWS</tbody></table></div>
<p><a href="../index.html">Schematic review</a> | <a href="../evidence/completion_audit.csv">Full audit CSV</a> | <a href="../evidence/footprint_evidence.json">Package evidence and caveats</a></p>
<script>document.querySelector('#q').oninput=e=>{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}</script></html>'''
(R/'docs/FINISHING_CHECKLIST.html').write_text(page.replace('ROWS','\n'.join(body)),encoding='utf-8')
print({k:v for k,v in report.items() if k!='components'})
