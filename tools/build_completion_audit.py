"""Separate value, package and routing gaps for the next hardware checks."""
from pathlib import Path
from collections import Counter
import json, csv, html
from current_state import current_state, value_is_known

R=Path(__file__).resolve().parents[1]
m=json.loads((R/'evidence/reconstruction.json').read_text(encoding='utf-8'))
status=current_state()
openpins=Counter(p.rsplit('.',1)[0] for p in m['unresolved_pins'])
rows=[]
for c in m['components']:
    ref=c['ref'];kind=c['kind'];pop=c['population'];method=[]
    if pop=='DNP':
        gap='Unpopulated option: no fitted value to recover'
    elif ref=='C5':
        gap='User sleeve reading: 470 uF / 16 V; exact can dimensions still needed'
        method=['Can diameter and lead-centre spacing for footprint']
    elif kind in ['C','L'] and value_is_known(c):
        gap='Individual value recovered: '+c['value']+'; '+c['value_evidence']['source']
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
    if ref=='D2':
        issue=next(i for i in status['items'] if i['id']=='E01')
        gap=issue['known']+' Remaining: '+issue['unknown']
        method=[issue['next_action']]
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
    unresolved_physical_pins=len(m['unresolved_pins']),unknown_ceramic_values=status['unknown_ceramic_values'],
    warning='Open-pad counts do not include every inferred route. Assigned footprints are candidates, not measured reproductions.',components=rows)
(R/'evidence/completion_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
with (R/'evidence/completion_audit.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
e=html.escape
body=[]
for r in rows:
    photos=' '.join(f'<a href="../photos/originals/{e(p)}">{e(p)}</a>' for p in r['photos'].split(';') if p)
    body.append('<tr>'+''.join('<td>'+e(str(r[k]))+'</td>' for k in ['ref','population','observed','displayed','value_or_identity','footprint','footprint_confidence','open_pads','next_method'])+'<td>'+photos+'</td></tr>')
issue_cards=[]
for i in status['items']:
    issue_cards.append(f'<article id="{e(i["id"])}"><h3>{e(i["id"])} - {e(i["area"])}</h3><p><b>Known:</b> {e(i["known"])}</p><p><b>Still uncertain:</b> {e(i["unknown"])}</p><p><b>Next useful check:</b> {e(i["next_action"])}</p><p><b>Finished when:</b> {e(i["closed_when"])}</p></article>')
closed_cards=''.join(f'<article id="{e(i["id"])}"><h3>{e(i["id"])} - closed</h3><p>{e(i["resolution"]["result"])}</p><p>Evidence: {e(str(i["resolution"]["evidence"]))}</p></article>' for i in status['closed_items'])
milestones=''.join(f'<p><b>{e(i["name"])}:</b> {e(i["criterion"])}</p>' for i in status['milestones'])
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe - current completion checklist</title>
<style>body{{font:15px/1.55 system-ui;background:#f3f6f4;color:#173b35;margin:30px auto;max-width:1200px;padding:0 20px}}a{{color:#006f64}}h1{{font-size:34px}}.cards{{display:flex;gap:12px;flex-wrap:wrap}}.cards div,article{{padding:18px;background:white;border:1px solid #bfd0c6;border-radius:8px;margin:12px 0}}.cards strong{{display:block;font-size:25px}}article p{{margin:8px 0}}.table{{overflow:auto;max-height:75vh;background:white}}table{{border-collapse:collapse;font-size:13px;min-width:1500px}}td,th{{padding:10px;border-bottom:1px solid #d5e0da;text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#dce8e1}}td:nth-child(5),td:nth-child(9){{min-width:270px}}input{{font:inherit;padding:12px;width:550px;max-width:90%;margin:20px 0}}.note{{background:#fff1cc;padding:15px}}li{{margin:8px 0}}</style>
<a href="../index.html">Schematic overview</a> | <a href="../output/pdf/PetSafe_completion_status.pdf">Printable status</a> | <a href="history/README.md">Investigation history</a>
<h1>What remains to finish</h1><p>{e(status['revision'])} schematic; review {e(status['review_revision'])}. All {status['catalog_entries']} catalog entries are on one sheet. This register covers known uncertainties; it does not certify unseen copper or operating behavior.</p>
<div class="cards"><div><strong>{status['footprints']['assigned']} / {status['catalog_entries']}</strong>candidate footprints assigned</div><div><strong>{len(status['unknown_ceramic_values'])}</strong>ceramic values unrecovered</div><div><strong>{len(status['current_fitted_open_pads'])}</strong>open pads on populated entries</div><div><strong>{len(status['current_gpio_pins'])}</strong>open PIC pads in the model</div></div>
<p class="note"><b>What the counts mean:</b> The {status['unresolved_physical_pins']} open pads include {len(status['current_dnp_open_pads'])} on empty options. A modeled wire can still be inferred. {status['erc_by_type'].get('isolated_pin_label',0)} isolated labels also need attention. No PIC pin has been assumed unused. There is no routed KiCad PCB.</p>
<h2>Recommended order</h2><ol><li>U7-J3 mapping resolved; TP16-TP11/TP17 rejected. PIC21-TP16/Q2 route resolved. PIC21-VREF explicitly withdrawn after TP16-VREF measured 800 kohm; C25-RA0 and C26-RA1 wiring resolved from user annotation. C6-C5 parallel wiring adopted from photos; Q8 source path remains qualified. Clear local copper remains agent photo work.</li><li>One complete Q3/C10/C11/C12 cell and remaining PIR supply details.</li><li>Specific R41, RF excitation and detector-output endpoints.</li><li>After routing, frequency-sensitive values and one powered scan session; footprint dimensions follow.</li></ol><p><a href="ARCHITECT_REVIEW_RESPONSE.md">Architect review response and specific checks</a></p><h2>Completion milestones</h2>{milestones}
<p><b>Open populated-entry pads:</b> {e(', '.join(status['current_fitted_open_pads']))}. TP9 remains an unlocated inventory entry. U6 pin 4 is unused by user/photo evidence; pin 5 is externally tied to pin 2/VIN (1 ohm), although internally NC in the candidate datasheet.</p>
<p><b>Unrecovered ceramic values ({len(status['unknown_ceramic_values'])}):</b> {e(', '.join(status['unknown_ceramic_values']))}. C5 is already 470 uF / 16 V. <b>Unrecovered magnetic values:</b> {e(', '.join(status['unknown_magnetic_values'])) or 'None'}. Photographs cannot determine ceramic capacitance or dielectric.</p>
<h2>Remaining questions and closure criteria</h2>{''.join(issue_cards)}
<details><summary>Closed issues retained as history</summary>{closed_cards}</details><h2>Every component: values, footprint confidence and open pads</h2><p>Question marks denote candidates; the tables identify the actual evidence needed. No generic request to remeasure every resistor is pending.</p>
<input id="q" type="search" placeholder="Filter by reference, LCR, continuity, footprint..." aria-label="Filter components"><div class="table"><table><thead><tr><th>Reference</th><th>Population</th><th>Observed</th><th>Proposed</th><th>Value / identity evidence</th><th>Stock footprint</th><th>Package confidence</th><th>Open pads</th><th>How to resolve</th><th>Photos</th></tr></thead><tbody>{''.join(body)}</tbody></table></div>
<p><a href="../evidence/completion_audit.csv">Component audit CSV</a> | <a href="../evidence/remaining_work.json">Maintained question register</a> | <a href="../evidence/proposed_nets.csv">All modeled net groups</a> | <a href="MEASUREMENTS.md">Recorded measurements</a></p>
<script>document.querySelector('#q').oninput=e=>{{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}}</script></html>'''
(R/'docs/FINISHING_CHECKLIST.html').write_text(page,encoding='utf-8')
print({k:v for k,v in report.items() if k!='components'})
