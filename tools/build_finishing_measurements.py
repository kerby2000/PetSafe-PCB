"""Render only the active measurement queue; raw completed evidence stays archived."""
from pathlib import Path
import json, html, base64
from current_state import current_state
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidence/finishing_measurements.json').read_text(encoding='utf-8'))
s=current_state();esc=html.escape
active={t[k] for t in p['tests'] for k in ['from','to']}
latest=[t for t in p['completed_tests'] if t['id'] in {'B31','B32','B33','B34','B35','B36'}]
displayed=p['tests'] or latest
shown_contacts={t[k] for t in displayed for k in ['from','to']}
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
    if not tests:continue
    raw=base64.b64encode((R/photo['source']).read_bytes()).decode('ascii')
    svg=photo_svg(photo,'../../').replace('../../'+photo['source'],'data:image/jpeg;base64,'+raw)
    (out/(photo['id']+'.svg')).write_text(svg,encoding='utf-8')
    def reading(t):
        if p['tests']:return f'<input data-id="{t["id"]}" aria-label="{t["id"]}" placeholder="V or OL">'
        return esc(t['result'])+(' (latest; earlier '+esc(t['earlier_reading'])+')' if t.get('earlier_reading') else '')
    rows=''.join(f'<tr><td>{t["id"]}</td><td>{t["from"]}</td><td>{t["to"]}</td><td>{reading(t)}</td></tr>' for t in tests)
    legend=''.join(f'<li><b>{k}</b>: {esc(v["description"])}</li>' for k,v in photo['points'].items() if k in shown_contacts)
    panels.append(f'<article><h2>{esc(photo["title"])}</h2><img src="measurement_screens/{photo["id"]}.svg" alt="Labelled Q3 probe contacts"><ul>{legend}</ul><table><tr><th>ID</th><th>Red probe</th><th>Black probe</th><th>Reading</th></tr>{rows}</table></article>')
roadmap=''.join('<li><b>'+esc(g['title'])+'</b> - '+esc(g['summary'])+'</li>' for g in s['finish_plan'])
reply='<h2>Copy results</h2><p>Worksheet only; nothing is sent automatically. Copy before closing.</p><textarea id="reply" readonly></textarea><button id="copy">Select results</button>' if p['tests'] else '<p>No new readings requested here. <a href="../evidence/q3_diode_results_20261009.json">Recorded result and interpretation</a>.</p>'
batch_status=f'{len(p["tests"])} requested readings' if p['tests'] else 'In-circuit batch completed; no active measurement form'
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe next measurement</title>
<style>body{{font:16px/1.5 system-ui;background:#edf3ef;color:#183d36;max-width:1000px;margin:24px auto;padding:0 20px}}a{{color:#006c61}}article,.note{{background:white;border:1px solid #bccfc4;border-radius:10px;padding:20px;margin:20px 0}}.note{{border-left:5px solid #cb7c20}}img{{display:block;width:100%;max-height:680px;object-fit:contain}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #ccdcd2;text-align:left}}input,textarea,button{{font:inherit;padding:10px}}input{{width:130px}}textarea{{width:95%;height:190px}}button{{background:#006c61;color:white;border:0}}</style>
<a href="FINISHING_CHECKLIST.html">All remaining issues</a> | <a href="../index.html">Schematic</a> | <a href="history/README.md">Completed investigation</a>
<h1>{esc(p['batch_title'])}</h1><p>{s['revision']} · {batch_status}</p><p class="note">{esc(p['setup'])}</p><p>{esc(p['instructions'])}</p>{''.join(panels)}<p>{esc(p['interpretation'])}</p>{reply}
<h2>What follows</h2><ul>{roadmap}</ul><p>ERC: {s['erc_total']} retained U6/U6A output conflict. U6A is DNP; its regulator symbol remains by your request. Other source and library findings are resolved.</p>
<script>const data={json.dumps(p['tests'])};function update(){{document.querySelector('#reply').value='PetSafe Q3 diode batch / {s['revision']}'+String.fromCharCode(10)+data.map(t=>t.id+' red '+t.from+' / black '+t.to+': '+document.querySelector('[data-id="'+t.id+'"]').value).join(String.fromCharCode(10))}}if(data.length){{document.querySelectorAll('input').forEach(e=>e.oninput=update);document.querySelector('#copy').onclick=()=>document.querySelector('#reply').select();update();}}</script></html>'''
(R/'docs/FINISHING_MEASUREMENTS.html').write_text(page,encoding='utf-8')
print('Active measurement page: '+str(len(p['tests']))+' diode tests; history omitted.')
