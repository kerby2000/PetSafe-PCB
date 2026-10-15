"""Separate value, package and routing gaps for the next hardware checks."""
from pathlib import Path
from collections import Counter
import json, csv, html
from current_state import current_state, value_is_known, component_summary

R=Path(__file__).resolve().parents[1]
m=json.loads((R/'evidence/reconstruction.json').read_text(encoding='utf-8'))
status=current_state()
cap_candidates={c['ref']:c for c in json.loads((R/'evidence/capacitor_value_review_20261015.json').read_text(encoding='utf-8'))['components']}
queue=json.loads((R/'evidence/finishing_measurements.json').read_text(encoding='utf-8'))
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
        candidate=cap_candidates[ref]
        gap='Original capacitance not recovered. Separate design candidate: '+candidate['proposal']+', '+str(candidate['voltage_rating_v'])+' V '+candidate['dielectric']+'. '+candidate['confidence']+'.'
        method=['See CAPACITOR_VALUE_REVIEW.html for the assumption and network validation. No new individual LCR measurement requested; keep fitted.']
    elif kind=='R':
        gap='Nominal resistance recovered from marking; tolerance and exact maker not established'
    elif kind=='L':
        gap='Inductor versus ferrite bead and value unresolved';method=['LCR at stated frequency; DC resistance; photo cannot establish RF impedance']
    elif kind=='TP':
        gap='Board pad: no component value required'
    else:
        gap=component_summary(c)
        issue_id={'D2':'I01','D3':'I01','D4':'I01','D5':'I01','D6':'E10','LED1':'M01'}.get(ref)
        if issue_id:
            method=[next(i['next_action'] for i in status['items'] if i['id']==issue_id)]
    if ref=='S1':method=['Electrical contacts verified; no repeat requested. Exact pad fit and 6 mm housing remain later PCB qualifications.']
    if ref=='D2':
        issue=next(i for i in status['items'] if i['id']=='I01')
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
    issue_cards.append(f'<article id="{e(i["id"])}"><h3>{e(i["id"])} - {e(i["area"])}</h3><p><b>Category:</b> {e(i["category"])}</p><p><b>Known:</b> {e(i["known"])}</p><p><b>Unresolved claim:</b> {e(i["unknown"])}</p><p><b>Next Codex action:</b> {e(i["codex_action"])}</p><p><b>Owner input:</b> {e(i["owner_input"])}</p><p><b>Closure evidence:</b> {e(i["closed_when"])}</p></article>')
work=json.loads((R/'evidence/remaining_work.json').read_text())
md=['# Remaining open items', '', f'Current schematic **{status["revision"]}**. Generated from [the authoritative register](../evidence/remaining_work.json); edit that source, not this view.', '',
    '[Schematic and PCB photographs](../README.md) | [HTML checklist](FINISHING_CHECKLIST.html) | [History and closed findings](history/README.md)', '',
    '**No owner measurement requested now.** Scope work and component lifting remain deferred. Supported copper, device interpretation and operating validation are distinct claims.', '',
    '| ID | Area | Category |', '|---|---|---|']
for i in status['items']:md.append(f'| [{i["id"]}](#{i["id"].lower()}) | {i["area"]} | {i["category"]} |')
for i in status['items']:
    md.extend(['',f'<a id="{i["id"].lower()}"></a>',f'## {i["id"]} - {i["area"]}', '', '| Field | Current position |','|---|---|'])
    for label,key in [('Category','category'),('Known','known'),('Unresolved claim','unknown'),('Next Codex action','codex_action'),('Owner input','owner_input'),('Closure evidence','closed_when')]:
        md.append('| '+label+' | '+i[key].replace('|','/').replace('\n',' ')+' |')
    md.extend(['','Evidence: '+', '.join('['+Path(p).name+'](../'+p+')' for p in i.get('supporting_evidence',[]))+'.'])
md.extend(['','## Accepted reconstruction boundaries','', 'These are acknowledged limits, not closed physical findings.'])
for i in status['reconstruction_limitations']:
    md.extend(['',f'### {i["id"]} - {i["area"]}', '', '**Disposition:** '+i['disposition'], '',i['known'],'','**Not established:** '+i['unknown'],'','**Reopen when:** '+i['reopen_when']])
md.extend(['',work['accepted_option_limitations'],'','## Reproduction requirements','','No routed reproduction PCB exists.'])
for i in work['reproduction_requirements']:md.extend(['','- **'+i['item']+':** '+i['remaining']])
(R/'docs/OPEN_ITEMS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
limitations=''.join('<article id="'+e(i['id'])+'"><h3>'+e(i['id']+' - '+i['area'])+'</h3><p><b>'+e(i['disposition'])+'</b></p><p>'+e(i['known'])+'</p><p><b>Unproved:</b> '+e(i['unknown'])+'</p><p><b>Next:</b> '+e(i['next_action'])+'</p><p><b>Reopen if:</b> '+e(i['reopen_when'])+'</p><a href="../'+e(i['evidence'])+'">Evidence and disposition</a></article>' for i in status['reconstruction_limitations'])
consistency=work.get('consistency_review',{})
consistency_rows=''.join('<tr><td><a href="#'+e(i['issue'])+'">'+e(i['issue'])+'</a></td><td><b>'+e(i['title'])+'</b><br>'+e(i['reasoning'])+'</td><td>'+e(i['next_action'])+'</td></tr>' for i in consistency.get('findings',[]))
reproduction=''.join('<tr><td><b>'+e(r['item'])+'</b></td><td>'+e(r['remaining'])+'</td><td>'+e(r['agent_work'])+'</td><td>'+e(r['owner_input'])+'</td></tr>' for r in work['reproduction_requirements'])
plan=''.join('<li><b>'+e(g['title'])+'</b> - '+e(g['summary'])+'</li>' for g in status['finish_plan'])
auditpath=R/'evidence/finalization_audit.json'
audit=json.loads(auditpath.read_text()) if auditpath.exists() else {}
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe remaining work</title>
<style>body{{font:16px/1.55 system-ui;background:#edf3ef;color:#193e36;max-width:1120px;margin:28px auto;padding:0 22px}}a{{color:#006e62}}h1{{font-size:36px}}article,.card{{background:white;border:1px solid #bfd0c6;border-radius:9px;padding:20px;margin:16px 0}}article p{{margin:9px 0}}.metrics{{display:flex;gap:15px;flex-wrap:wrap}}.metrics div{{background:#173e36;color:white;padding:16px;border-radius:8px}}.metrics strong{{font-size:27px;display:block}}li{{margin:8px 0}}table{{border-collapse:collapse;background:white;width:100%;font-size:14px}}th,td{{padding:12px;vertical-align:top;text-align:left;border-bottom:1px solid #bfd0c6}}th{{background:#dce9e1}}</style>
<a href="../index.html">Schematic overview</a> | <a href="CAPACITOR_VALUE_REVIEW.html">Capacitor values by function</a> | <a href="FINISHING_MEASUREMENTS.html">Current measurement screen</a> | <a href="../output/pdf/PetSafe_completion_status.pdf">Printable remaining work</a> | <a href="history/README.md">History and resolved items</a>
<h1>What remains to finish</h1><p>{e(status['revision'])} | {len(status['items'])} active issues. Each card states what is established, the specific gap and its closure criterion.</p>
<div class="metrics"><div><strong>{len(status['current_fitted_open_pads'])}</strong>unassigned fitted pads</div><div><strong>{audit.get('dangling_wire_ends','pending')}</strong>dangling wire ends</div><div><strong>{status['erc_total']}</strong>retained ERC conflict</div><div><strong>{len(status['unknown_ceramic_values'])}</strong>unknown ceramic values</div></div>
<div class="card"><b>{e(queue["batch_title"])}</b> <a href="FINISHING_MEASUREMENTS.html">Open measurement screen</a>. {e(queue["instructions"])} Q3 stays fitted. Other listed tests are staged, not requested together.</div>
<h2>Consistency checks: where a remaining error could hide</h2><p>These findings refer to existing issues; they are not additional issue groups or newly measured faults. <a href="../evidence/circuit_consistency_v0942.json">Evidence and checks</a>.</p><table><tr><th>Issue</th><th>Finding</th><th>Next useful action</th></tr>{consistency_rows}</table>
<h2>Finish in this order</h2><ol>{plan}</ol>
<p><b>Audit boundary:</b> {status['modeled_nets']} modeled net partitions agree with KiCad. Zero open pads or wire tails does not establish hidden copper or circuit operation. The supported RC3/TP11 and RC7/TP17 routes are complete as drawn; E06 is retained below as a hidden-layer reconstruction limitation, not a pending measurement. RA0/C25-to-TP6 is resolved by B59 = 1.5 ohm. Q3 device identity remains under E04. <a href="../evidence/finalization_audit.json">Detailed audit</a>.</p>
<h2>Documented reconstruction limitations</h2>{limitations}
<h2>Remaining questions</h2>{''.join(issue_cards)}
<div class="card"><h2>Unrecovered ceramic values</h2><p>{e(', '.join(status['unknown_ceramic_values']))}</p><p>Values belong to V01; package geometry cannot determine capacitance. C5 and L1/L2 readings are already retained in the inventory.</p></div>
<h2 id="reproduction">Can we reproduce the original PCB?</h2><p>Not yet. The items below are additional manufacturing and system requirements, separate from the {len(status['items'])} active main-board electrical/value/package issues. A replacement can target the same function and fit; exact inner-layer geometry is not recoverable from continuity alone.</p><div style="overflow:auto"><table><thead><tr><th>Area</th><th>Still required</th><th>Agent work</th><th>Owner input</th></tr></thead><tbody>{reproduction}</tbody></table></div>
<h2>Scope and accepted limitations</h2><p>{e(json.loads((R/'evidence/remaining_work.json').read_text())['scope_note'])}</p><p>{e(json.loads((R/'evidence/remaining_work.json').read_text())['accepted_option_limitations'])}</p>
<p>The library is registered for KiCad 10. Open the project .kicad_pro to load its project library table; an already-open editor may need reopening. {len(audit.get('source_flags', []))} stock PWR_FLAG annotations describe existing source paths. They do not certify measured voltages or Q7/Q8 operation. The U6/U106 regulator conflict remains visible at your request.</p>
<p><a href="../evidence/completion_audit.csv">Full component audit</a> | <a href="../evidence/remaining_work.json">Active register</a> | <a href="../evidence/finalization_review_v0931.json">Disposition of every previous item</a> | <a href="../evidence/proposed_nets.csv">Modeled nets</a></p></html>'''
(R/'docs/FINISHING_CHECKLIST.html').write_text(page,encoding='utf-8')
print('Remaining-only checklist: '+str(len(status['items']))+' issues.')
