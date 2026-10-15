"""Render only the active measurement queue; raw completed evidence stays archived."""
from pathlib import Path
import json, html, base64, mimetypes
from current_state import current_state
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidence/finishing_measurements.json').read_text(encoding='utf-8'))
s=current_state();esc=html.escape
active={t[k] for t in p['tests'] for k in ['from','to']}
latest=[t for t in p['completed_tests'] if t['id'] in p.get('last_completed_test_ids', ['B31','B32','B33','B34','B35','B36'])]
displayed=p['tests'] or latest
shown_contacts={t[k] for t in displayed for k in ['from','to']}
contact_labels=p.get('contact_labels',['red probe','black probe'])
steps='<ol>'+''.join('<li>'+esc(step)+'</li>' for step in p.get('setup_steps',[]))+'</ol>' if p.get('setup_steps') else ''
source_links=' | '.join('<a href="'+esc(src['url'],quote=True)+'">'+esc(src['title'])+'</a>' for src in p.get('measurement_sources',[]))
sources='<p><small>Settings and method: '+source_links+'</small></p>' if source_links else ''
def photo_svg(photo, prefix='../'):
    vb=' '.join(map(str,photo['view_box']));w,h=photo['coordinate_space'];out=[]
    shown=shown_contacts|set(photo.get('context_points',[]))
    for key,v in photo['points'].items():
        if key not in shown:continue
        x,y=v['xy'];lx,ly=v['label'];color='#096eab' if v.get('role')=='reference' else '#d56900'
        out.append(f'<g><title>{esc(key+": "+v["description"])}</title><path d="M {lx} {ly} L {x} {y}" stroke="white" stroke-width="7"/><path d="M {lx} {ly} L {x} {y}" stroke="{color}" stroke-width="3"/><circle cx="{x}" cy="{y}" r="14" fill="none" stroke="white" stroke-width="5"/><circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{color}" stroke-width="3"/><circle cx="{lx}" cy="{ly}" r="26" fill="{color}" stroke="white" stroke-width="3"/><text x="{lx}" y="{ly+9}" text-anchor="middle" fill="white" font-size="29" font-weight="700">{key}</text></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{photo["view_box"][2]}" height="{photo["view_box"][3]}" viewBox="{vb}" role="img" aria-label="{esc(photo["title"])}" font-family="Arial, sans-serif"><image xlink:href="{prefix}{photo["source"]}" width="{w}" height="{h}"/>{"".join(out)}</svg>'

out=R/'docs/measurement_screens';out.mkdir(exist_ok=True)
panels=[]
for photo in p['photos']:
    tests=[t for t in displayed if t['group']==photo['id']]
    reference_panel=bool(set(photo.get('reference_for',[])) & {t['group'] for t in displayed})
    if not tests and not reference_panel:continue
    raw=base64.b64encode((R/photo['source']).read_bytes()).decode('ascii')
    mime=mimetypes.guess_type(photo['source'])[0] or 'application/octet-stream'
    svg=photo_svg(photo,'../../').replace('../../'+photo['source'],'data:'+mime+';base64,'+raw)
    (out/(photo['id']+'.svg')).write_text(svg,encoding='utf-8')
    def reading(t):
        if p['tests']:return f'<input data-id="{t["id"]}" aria-label="{t["id"]}" placeholder="{esc(t.get("unit","V or OL"))}">'
        return esc(t['result'])+(' (latest; earlier '+esc(t['earlier_reading'])+')' if t.get('earlier_reading') else '')
    rows=''.join(f'<tr><td>{t["id"]}</td><td>{t["from"]}</td><td>{t["to"]}</td><td>{esc(t.get("state", "As described"))}</td><td>{reading(t)}</td></tr>' for t in tests)
    legend=''.join(f'<li><b>{k}</b>: {esc(v["description"])}</li>' for k,v in photo['points'].items() if k in shown_contacts)
    result_table=f'<div class="table-scroll"><table><tr><th>ID</th><th>{esc(contact_labels[0].capitalize())}</th><th>{esc(contact_labels[1].capitalize())}</th><th>Condition</th><th>Reading</th></tr>{rows}</table></div>' if tests else '<p>Other probe location for the same reading above; no additional test.</p>'
    panels.append(f'<article><h2>{esc(photo["title"])}</h2><img src="measurement_screens/{photo["id"]}.svg" alt="{esc(photo["title"])}"><ul>{legend}</ul>{result_table}</article>')
roadmap=''.join('<li><b>'+esc(g['title'])+'</b> - '+esc(g['summary'])+'</li>' for g in s['finish_plan'])
result_path=esc(p.get('last_result_evidence','evidence/q3_diode_results_20261009.json'))
reply=('<h2>Results to share</h2><p>Nothing is sent automatically. Copy and paste into the chat, or download a text file.</p><p id="draft-status" role="status"></p><textarea id="reply" aria-label="Results to share" readonly></textarea><p><button id="copy" type="button">Copy results</button> <button id="select" type="button">Select text</button> <button id="download" type="button">Download text</button></p><p id="result-status" role="status" aria-live="polite"></p>') if displayed else ''
if not p['tests']:
    reply=f'<p>No new readings requested here. <a href="../{result_path}">Recorded result and interpretation</a>.</p>'+reply
review_link='<p><a href="'+esc(p['review_link'],quote=True)+'">Function-based capacitor review and provisional values</a></p>' if p.get('review_link') else ''
form_config=dict(tests=displayed,active=bool(p['tests']),title=p['batch_title'],revision=s['revision'],contacts=contact_labels,batch=p['batch_id'])
form_script=(R/'tools/measurement_form.js').read_text(encoding='utf-8')+'\ninitializeMeasurementForm('+json.dumps(form_config)+');'
baseline='<p><label>Shorted-probe baseline (ohms): <input id="baseline" aria-label="Shorted-probe baseline" placeholder="ohms"></label></p>' if p.get('request_probe_baseline') and p['tests'] else ''
batch_status=f'{len(p["tests"])} requested readings' if p['tests'] else 'In-circuit batch completed; no active measurement form'
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe next measurement</title>
<style>body{{font:16px/1.5 system-ui;background:#edf3ef;color:#183d36;max-width:1000px;margin:24px auto;padding:0 20px}}a{{color:#006c61}}article,.note{{background:white;border:1px solid #bccfc4;border-radius:10px;padding:20px;margin:20px 0}}.note{{border-left:5px solid #cb7c20}}img{{display:block;width:100%;max-height:680px;object-fit:contain}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #ccdcd2;text-align:left}}input,textarea,button{{font:inherit;padding:10px}}input{{width:230px;box-sizing:border-box}}.table-scroll{{overflow-x:auto}}li{{margin:8px 0}}textarea{{width:95%;height:190px}}button{{background:#006c61;color:white;border:0}}</style>
<a href="FINISHING_CHECKLIST.html">All remaining issues</a> | <a href="../index.html">Schematic</a> | <a href="history/README.md">Completed investigation</a>
<h1>{esc(p['batch_title'])}</h1><p>{s['revision']} | {batch_status}</p><p class="note">{esc(p['setup'])}</p><p>{esc(p['instructions'])}</p>{review_link}{steps}{sources}{baseline}{''.join(panels)}<p>{esc(p['interpretation'])}</p>{reply}
<h2>What follows</h2><ul>{roadmap}</ul><p>ERC: {s['erc_total']} retained U6/U6A output conflict. U6A is DNP; its regulator symbol remains by your request. Other source and library findings are resolved.</p>
<script>{form_script}</script></html>'''
(R/'docs/FINISHING_MEASUREMENTS.html').write_text(page,encoding='utf-8')
print('Active measurement page: '+str(len(p['tests']))+' tests; history omitted.')
