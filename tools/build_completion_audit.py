"""Separate value, package and routing gaps for the next hardware checks."""
from pathlib import Path
from collections import Counter
import json, csv, html
from current_state import current_state, value_is_known, component_summary

R=Path(__file__).resolve().parents[1]
m=json.loads((R/'evidence/reconstruction.json').read_text(encoding='utf-8'))
status=current_state()
openpins=Counter(p.rsplit('.',1)[0] for p in m['unresolved_pins'])
rows=[]
for c in m['components']:
    ref=c['ref'];kind=c['kind'];pop=c['population'];method=[]
    if pop=='DNP':
        gap='Unpopulated option: no fitted value to recover. '+component_summary(c)
    elif ref=='C5':
        gap='470 uF / 16 V; measured can diameter 6.33 mm and height 16 mm. Stock nominal 6.3 mm radial footprint assigned; 2.5 mm pitch remains inferred.'
        method=['No repeat can measurement. Verify lead pitch/drill fit only for PCB reproduction; use the measured 16 mm height.']
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
        gap=component_summary(c)
        issue_id={'D2':'E01','D3':'I01','D4':'I01','D5':'I01','D6':'E10','LED1':'I02','S1':'E05'}.get(ref)
        if issue_id:
            method=[next(i['next_action'] for i in status['items'] if i['id']==issue_id)]
    if ref=='D2':
        issue=next(i for i in status['items'] if i['id']=='E01')
        gap=issue['known']+' Remaining: '+issue['unknown']
        method=[issue['next_action']]
    if openpins[ref] and pop!='DNP':method+=['Targeted continuity for '+str(openpins[ref])+' open physical pads']
    if not c['footprint']:method+=['LED1 body is already measured at 1.5 x 1.5 mm. Obtain the pad geometry/numbering or matching vendor drawing; no repeat body-size request.']
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
plan=''.join('<li><b>'+e(g['title'])+'</b> - '+e(g['summary'])+' '+e(g['next_action'])+'</li>' for g in status['finish_plan'])
settled=''.join('<li>'+e(t)+'</li>' for t in status['settled_summary'])
milestones=''.join(f'<p><b>{e(i["name"])}:</b> {e(i["criterion"])}</p>' for i in status['milestones'])
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe - current completion checklist</title>
<style>body{{font:15px/1.55 system-ui;background:#f3f6f4;color:#173b35;margin:30px auto;max-width:1200px;padding:0 20px}}a{{color:#006f64}}h1{{font-size:34px}}.cards{{display:flex;gap:12px;flex-wrap:wrap}}.cards div,article{{padding:18px;background:white;border:1px solid #bfd0c6;border-radius:8px;margin:12px 0}}.cards strong{{display:block;font-size:25px}}article p{{margin:8px 0}}.table{{overflow:auto;max-height:75vh;background:white}}table{{border-collapse:collapse;font-size:13px;min-width:1500px}}td,th{{padding:10px;border-bottom:1px solid #d5e0da;text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#dce8e1}}td:nth-child(5),td:nth-child(9){{min-width:270px}}input{{font:inherit;padding:12px;width:550px;max-width:90%;margin:20px 0}}.note{{background:#fff1cc;padding:15px}}li{{margin:8px 0}}</style>
<a href="../index.html">Schematic overview</a> | <a href="../output/pdf/PetSafe_completion_status.pdf">Printable status</a> | <a href="history/README.md">Investigation history</a>
<h1>What remains to finish</h1><p>{e(status['revision'])} schematic; review {e(status['review_revision'])}. All {status['catalog_entries']} catalog entries are on one sheet. This register covers known uncertainties; it does not certify unseen copper or operating behavior.</p>
<div class="cards"><div><strong>{status['footprints']['assigned']} / {status['catalog_entries']}</strong>candidate footprints assigned</div><div><strong>{len(status['unknown_ceramic_values'])}</strong>ceramic values unrecovered</div><div><strong>{len(status['current_fitted_open_pads'])}</strong>open pads on populated entries</div><div><strong>{len(status['current_gpio_pins'])}</strong>open PIC pads in the model</div></div>
<p class="note"><b>What the counts mean:</b> The {status['unresolved_physical_pins']} open pads include {len(status['current_dnp_open_pads'])} on empty options. A modeled wire can still be inferred. {status['erc_by_type'].get('isolated_pin_label',0)} isolated labels also need attention. No PIC pin has been assumed unused. There is no routed KiCad PCB.</p>
<h2>Finish in this order</h2><ol>{plan}</ol><p>No active measurement batch is waiting for the owner. The entries below describe remaining work, not a request to perform every listed method now.</p>
<details><summary>Already resolved</summary><ul>{settled}</ul></details><h2>Completion milestones</h2>{milestones}
<p><b>Open populated-entry pads:</b> {e(', '.join(status['current_fitted_open_pads']) or 'None')}. <b>Open empty-option pads:</b> {e(', '.join(status['current_dnp_open_pads']) or 'None')}. TP9 was removed as unsupported; C49 is wired ANT2-to-GND. U6 pin4 is intentionally unused; pin5 externally joins VIN at 1 ohm.</p>
<p><b>Unrecovered ceramic values ({len(status['unknown_ceramic_values'])}):</b> {e(', '.join(status['unknown_ceramic_values']))}. C5 is 470 uF / 16 V. L1/L2 readings are 1.4/2.2 uH; conditions and exact type/ratings remain unreported. Package size does not establish ceramic capacitance or dielectric.</p>
<h2>Remaining questions and closure criteria</h2>{''.join(issue_cards)}
<details><summary>Closed issues retained as history</summary>{closed_cards}</details><h2>Every component: values, footprint confidence and open pads</h2><p>Question marks denote candidates; the tables identify the actual evidence needed. No generic request to remeasure every resistor is pending.</p>
<input id="q" type="search" placeholder="Filter by reference, LCR, continuity, footprint..." aria-label="Filter components"><div class="table"><table><thead><tr><th>Reference</th><th>Population</th><th>Observed</th><th>Proposed</th><th>Value / identity evidence</th><th>Stock footprint</th><th>Package confidence</th><th>Open pads</th><th>How to resolve</th><th>Photos</th></tr></thead><tbody>{''.join(body)}</tbody></table></div>
<p><a href="../evidence/completion_audit.csv">Component audit CSV</a> | <a href="../evidence/remaining_work.json">Maintained question register</a> | <a href="../evidence/proposed_nets.csv">All modeled net groups</a> | <a href="MEASUREMENTS.md">Recorded measurements</a></p>
<script>document.querySelector('#q').oninput=e=>{{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}}</script></html>'''
(R/'docs/FINISHING_CHECKLIST.html').write_text(page,encoding='utf-8')
print({k:v for k,v in report.items() if k!='components'})
