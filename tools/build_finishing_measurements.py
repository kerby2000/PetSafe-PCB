"""Small current bench queue, with vector callouts over unchanged board photos."""
from pathlib import Path
import html,json,re,base64
from current_state import current_state

R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidence/finishing_measurements.json').read_text(encoding='utf-8'))
s=current_state();esc=html.escape
points={key:value for photo in p['photos'] for key,value in photo['points'].items()}
active={t[k] for t in p['tests'] for k in ['from','to']}
completed=''.join(f'<tr><td>{t["id"]}</td><td>{t["from"]} - {t["to"]}<br>{esc(points[t["from"]]["description"])} to {esc(points[t["to"]]["description"])}</td><td>{esc(t["result"])}</td></tr>' for t in p.get('completed_tests',[]))
def photo_svg(photo, prefix='../'):
    vb=' '.join(map(str,photo['view_box']));w,h=photo['coordinate_space'];out=[]
    shown=active|set(photo.get('context_points',[]))
    for key,v in photo['points'].items():
        if key not in shown:continue
        x,y=v['xy'];lx,ly=v['label'];color='#67766f' if key not in active else '#096eab' if v.get('role')=='reference' else '#d56900'
        out.append(f'<g><title>{esc(key+": "+v["description"])}</title><path d="M {lx} {ly} L {x} {y}" stroke="white" stroke-width="7"/><path d="M {lx} {ly} L {x} {y}" stroke="{color}" stroke-width="3"/><circle cx="{x}" cy="{y}" r="14" fill="none" stroke="white" stroke-width="5"/><circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{color}" stroke-width="3"/><circle cx="{lx}" cy="{ly}" r="26" fill="{color}" stroke="white" stroke-width="3"/><text x="{lx}" y="{ly+9}" text-anchor="middle" fill="white" font-size="29" font-weight="700">{key}</text></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{photo["view_box"][2]}" height="{photo["view_box"][3]}" viewBox="{vb}" role="img" aria-label="{esc(photo["title"])}" font-family="Arial, sans-serif"><image xlink:href="{prefix}{photo["source"]}" width="{w}" height="{h}"/>{"".join(out)}</svg>'
def test_rows(tests):
    return ''.join(f'<tr><td>{t["id"]}</td><td><b>{t["from"]} - {t["to"]}</b><br>{esc(points[t["from"]]["description"])}<br>to {esc(points[t["to"]]["description"])}</td><td>{esc(t["purpose"])}</td><td><input data-test="{t["id"]}" aria-label="{t["id"]} reading" placeholder="ohms / kohms / OL"></td></tr>' for t in tests)
def photo_panel(photo):
    shown=active|set(photo.get('context_points',[]))
    legend=''.join(f'<li><b>{k}</b> - {esc(v["description"])}'+(' (orientation only; no measurement)' if k not in active else '')+'</li>' for k,v in photo['points'].items() if k in shown)
    tests=[t for t in p['tests'] if t.get('group')==photo['id']]
    table=f'<div class="table"><table><thead><tr><th>ID</th><th>Measure between</th><th>Why</th><th>Your result</th></tr></thead><tbody>{test_rows(tests)}</tbody></table></div>' if tests else ''
    picture=f'<img class="probe-photo" src="measurement_screens/{photo["id"]}.svg" alt="{esc(photo["title"])}">' if tests else photo_svg(photo)
    return f'<article id="{photo["id"]}"><h2>{esc(photo["title"])}</h2><p>{esc(photo.get("instructions",""))}</p>{picture}<ul>{legend}</ul><a href="../{photo["source"]}" target="_blank">Open original photo</a>{table}<p><a href="#reply">Copy results into chat</a></p></article>'
rows=''.join(f'<tr><td>{t["id"]}</td><td><b>{t["from"]} - {t["to"]}</b><br>{esc(points[t["from"]]["description"])}<br>to {esc(points[t["to"]]["description"])}</td><td>{esc(t["purpose"])}</td><td><input data-test="{t["id"]}" aria-label="{t["id"]} reading" placeholder="ohms / kohms / OL"></td></tr>' for t in p['tests'])
roadmap=''.join(f'<li><b>{esc(stage["stage"])}</b><p>{esc(stage["work"])}</p></li>' for stage in p['next_stages'])
data=json.dumps(p['tests']).replace('</','<\\/')
page=r'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PetSafe - finishing measurements</title>
<style>*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui;color:#193d36;background:#edf3ef}main{max-width:1300px;margin:auto;padding:24px}h1{font-size:34px;margin-bottom:8px}h2{font-size:23px}a{color:#006d61}nav{display:flex;gap:20px;flex-wrap:wrap}.card,article{background:white;border:1px solid #bfd1c5;border-radius:10px;padding:20px;margin:18px 0}.note{border-left:5px solid #c87716;background:#fff2d7;padding:16px}.photos{display:grid;grid-template-columns:1fr 1fr;gap:18px}.photos article{min-width:0}.photos article:only-child{grid-column:1/-1;max-width:900px;width:100%;justify-self:center}svg{width:100%;height:auto;background:#143b2c}li{margin:7px 0}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #d0ded6;padding:12px}th{background:#e3eee7}input,textarea,button{font:inherit;border:1px solid #91afa1;border-radius:5px;padding:9px}input{max-width:100%;width:180px}textarea{width:100%;height:230px}button{background:#096d5e;color:white;cursor:pointer}.table{overflow:auto}.muted{color:#51675d;font-size:14px}.roadmap{list-style:none;padding:0}.roadmap p{margin-top:3px}@media(max-width:850px){.photos{grid-template-columns:1fr}main{padding:14px}}@media print{input,button,textarea{display:none}.photos{grid-template-columns:1fr 1fr}article{break-inside:avoid}}</style>
<main><nav><a href="../index.html">Schematic overview</a><a href="FINISHING_CHECKLIST.html">All remaining issues</a><a href="VIA_REVIEW.html">Via photos</a></nav>
<h1>Finish the schematic, one useful batch at a time</h1>
<p><b>The connections are not all resolved yet.</b> This page separates your next bench work from the later value and documentation work.</p>
<h2>BATCH_TITLE</h2><p class="note">SETUP</p><p>INSTRUCTIONS</p>
<div class="photos">PHOTOS</div>
<p class="muted">Circles identify probe contacts; coloured leaders are annotations, not copper traces. Photos retain their original orientation. Each letter names a physical contact, not a signal name. Candidate measurements are not assumed connections.</p><p>INTERPRETATION</p>
<div class="card table"><table><thead><tr><th>ID</th><th>Measure between</th><th>Why</th><th>Your result</th></tr></thead><tbody>ROWS</tbody></table></div>
<div class="card"><h2>Copy results into chat</h2><label>Shorted-probe baseline <input id="baseline" placeholder="e.g. 0.5 ohm"></label><p class="muted">Fields are only a worksheet. Nothing is sent automatically. Copy your results before closing this page.</p><textarea id="reply" readonly aria-label="Reply with readings"></textarea><button id="select">Select reply text</button></div>
<div class="card"><h2>Current picture</h2><p><b>ERC: ERC_TOTAL findings</b> = FITTED open populated-entry pads + DNP open pads on empty options + ISOLATED isolated labels + POWER_WARNINGS power-source warnings. Power-source declarations require established supply paths; empty pads require copper review before an NC decision.</p><p>FITTED populated-entry pads still have no modeled connection: <b>OPEN_LIST</b>. Of these, U6's two pads are candidate internal-NC pins whose external copper remains unverified. Another DNP pads are on empty options.</p><p>There are also incomplete routes despite wires already being drawn: receiver feedback/output, RF excitation and antenna continuations, R41/D1 and some PIC test-point branches. <b>Zero open PIC pads is not proof that every signal path is complete.</b></p><p>VALUES ceramic values and L1/L2 type/value remain unrecovered. FOOTPRINTS candidate footprints are assigned; C5, S1 and LED1 still need geometry. The <a href="FINISHING_CHECKLIST.html">complete checklist</a> preserves the details.</p></div>
<div class="card"><h2>Measurements recorded</h2><p>RESULT_SUMMARY</p><details><summary>All recorded readings</summary><table><thead><tr><th>ID</th><th>Previous contacts</th><th>Recorded result</th></tr></thead><tbody>COMPLETED</tbody></table></details></div><div class="card"><h2>What follows this batch</h2><ul class="roadmap">ROADMAP</ul><p>DEFERRED</p><p><b>Already done; do not repeat:</b> REPEATS.</p></div><p class="muted">Based on schematic REV, DATE. Completed measurements are recorded above; later checks depend on the new results. A fully measured original and a reconstruction with documented component assumptions are distinct results.</p></main>
<script>const tests=DATA;const fields=[...document.querySelectorAll('input')];function update(){const lines=['PetSafe finishing batch / REV','Shorted probes: '+(document.querySelector('#baseline').value||'')];for(const t of tests){const value=document.querySelector('[data-test="'+t.id+'"]').value;lines.push(t.id+' '+t.from+'-'+t.to+': '+value)}document.querySelector('#reply').value=lines.join('\n')}fields.forEach(e=>e.addEventListener('input',update));document.querySelector('#select').onclick=()=>{document.querySelector('#reply').focus();document.querySelector('#reply').select()};update();</script></html>'''
for k,v in {'ERC_TOTAL':s['erc_total'],'ISOLATED':s['erc_by_type'].get('isolated_pin_label',0),'POWER_WARNINGS':s['erc_by_type'].get('power_pin_not_driven',0),'FITTED':len(s['current_fitted_open_pads']),'OPEN_LIST':esc(', '.join(s['current_fitted_open_pads'])),'DNP':len(s['current_dnp_open_pads']),'VALUES':len(s['unknown_ceramic_values']),'FOOTPRINTS':str(s['footprints']['assigned'])+'/'+str(s['catalog_entries']),'SETUP':esc(p['setup']),'BATCH_TITLE':esc(p['batch_title']),'INSTRUCTIONS':esc(p['instructions']),'INTERPRETATION':esc(p['interpretation']),'RESULT_SUMMARY':esc(p['result_summary']),'COMPLETED':completed,'PHOTOS':''.join(photo_panel(photo) for photo in p['photos'] if active & set(photo['points'])),'ROWS':rows,'ROADMAP':roadmap,'DEFERRED':esc(p['deferred']),'REPEATS':esc('; '.join(p['do_not_repeat'])),'REV':esc(s['revision']),'DATE':esc(p['date']),'DATA':data}.items():page=re.sub(r'\b'+re.escape(k)+r'\b',lambda _:str(v),page)
if not p['tests']:
    # A completed queue must not still present an empty measurement form.
    page=re.sub(r'<p class="note">.*?</p>','',page,count=1,flags=re.S)
    page=re.sub(r'<div class="photos">.*?<div class="card"><h2>Current picture</h2>', '<div class="card"><h2>Current picture</h2>',page,count=1,flags=re.S)
    page=page.replace('<h2>What follows this batch</h2>','<h2>Remaining work</h2>')
    page=re.sub(r'<script>.*?</script>','',page,flags=re.S)
if p['tests'] and all(t.get('group') for t in p['tests']):
    # Each screen owns its reading fields; never duplicate input IDs below it.
    page=re.sub(r'<div class="card table"><table>.*?</table></div>','',page,count=1,flags=re.S)
    page=page.replace('</style>','.photos{display:block}.photos article{max-width:1000px;margin:24px auto}article{scroll-margin-top:18px}.jump{background:white;padding:14px;border:1px solid #bfd1c5;border-radius:8px}.photos svg,.probe-photo{display:block;width:100%;height:auto;max-height:80vh;object-fit:contain}ul{padding-left:22px}</style>')
    tabs=''.join(f'<a href="#{photo["id"]}">{esc(photo["title"])}</a>' for photo in p['photos'] if any(t.get('group')==photo['id'] for t in p['tests']))
    page=page.replace('<div class="photos">',f'<nav class="jump">{tabs}<a href="#tp9">TP9 location review</a></nav><div class="photos">',1)
    loc=p.get('location_review')
    if loc:
        note=f'<div class="card" id="tp9"><h2>TP9: no physical location established</h2><p>You reported: <b>{esc(loc["user_report"])}</b>.</p><p>{esc(loc["conclusion"])}</p><p>{esc(loc["action"])}</p></div>'
        page=page.replace('<div class="card"><h2>Current picture</h2>',note+'<div class="card"><h2>Current picture</h2>',1)
    if p.get('u6_annotation'):
        a=p['u6_annotation']
        note=f'<div class="card"><h2>Latest U6 evidence</h2><p><a href="../{a["source"]}">Your annotated U6 photo</a> replaces the proposed broad NC-pad checks. Pin 4 is reported unused; pin 5 reaches R37 and the single U6A pad. The only requested U6 check is pin 5 to pin 2.</p><p>{esc(p["candidate_datasheet_note"])} <a href="datasheets/S812C.pdf#page=11">Local datasheet, page 11</a>.</p><p>{esc(a["model_status"])}</p></div>'
        page=page.replace('<div class="card"><h2>Current picture</h2>',note+'<div class="card"><h2>Current picture</h2>',1)
    export=R/'docs/measurement_screens';export.mkdir(exist_ok=True)
    for photo in p['photos']:
        if active & set(photo['points']):
            # Embed the unchanged original bytes so standalone screens need no
            # external image fetch and render reliably in local SVG viewers.
            original=base64.b64encode((R/photo['source']).read_bytes()).decode('ascii')
            screen=photo_svg(photo,'../../').replace('../../'+photo['source'],'data:image/jpeg;base64,'+original)
            (export/(photo['id']+'.svg')).write_text(screen,encoding='utf-8')
page=page.replace("lines.join('\\\\n')", "lines.join('\\n')")
(R/'docs/FINISHING_MEASUREMENTS.html').write_text(page,encoding='utf-8')
print('Built current finishing batch: '+str(len(p['tests']))+' proposed measurements; no net changes.')
