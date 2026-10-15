"""Render the separately qualified capacitor proposals; never alter the native BOM."""
from pathlib import Path
import json, html
from collections import Counter
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidence/capacitor_value_review_20261015.json').read_text(encoding='utf-8'))
esc=html.escape
sources={s['id']:s for s in p['sources']}
groups=[('REFERENCE_STARTING_VALUE','12 supply capacitors: provisional replacement values'),
        ('CONDITIONAL_CANDIDATE','4 crystal and feedback capacitors: constrained candidates'),
        ('NETWORK_CONSTRAINT','28 capacitors: solve the connected network first')]
sections=[]
for key,title in groups:
    rows=[]
    for c in p['components']:
        if c['category']!=key: continue
        links=' '.join('<a href="#src-'+esc(s)+'">'+esc(s)+'</a>' for s in c['sources'])
        rows.append('<tr><td><b>'+esc(c['ref'])+'</b><br><small>'+esc(c['footprint'].split(':')[-1])+'</small></td><td>'+esc(c['function'])+'<br><small>'+esc(' / '.join(c['nets']))+'</small></td><td><b>'+esc(c['proposal'])+'</b></td><td>'+esc(c['basis'])+'<br>'+links+'</td><td>'+esc(c['remaining'])+'</td></tr>')
    sections.append('<section><h2>'+esc(title)+'</h2><div class="scroll"><table><thead><tr><th>Part</th><th>Function / modeled nets</th><th>Proposal or constraint</th><th>Reason</th><th>Still to qualify</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></section>')
cal=p['calculations']
ant=''.join('<tr><td>'+str(a['inductance_uh'])+' uH</td><td>'+f'{a["equivalent_capacitance_nf"]:.2f}'+' nF</td></tr>' for a in cal['antenna_examples'])
source_html=''.join('<li id="src-'+esc(s['id'])+'"><a href="'+esc(s['url'],quote=True)+'">'+esc(s['title'])+'</a>: '+esc(s['finding'])+'</li>' for s in p['sources'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PetSafe capacitor values by function</title><style>
body{font:16px/1.5 system-ui;color:#193d35;background:#edf3ef;max-width:1400px;margin:24px auto;padding:0 20px}a{color:#006c61}section,.note{background:white;padding:20px;margin:20px 0;border:1px solid #bfd2c7;border-radius:9px}.note{border-left:5px solid #b87516}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #cbdad0}th{background:#e1ece5}.scroll{overflow-x:auto}small{color:#50685c}li{margin:8px 0}code{background:#e1ece5;padding:3px}h1{font-size:32px}.compact{max-width:650px}nav{display:flex;gap:20px;flex-wrap:wrap}@media print{body{background:white;font-size:11px}table{font-size:10px}section{padding:4px}tr{break-inside:avoid}}
</style><nav><a href="../index.html">Schematic overview</a><a href="FINISHING_CHECKLIST.html#V01">Remaining questions</a><a href="FINISHING_MEASUREMENTS.html">Recorded C21/C22 readings</a></nav>
<h1>Choose values from circuit function</h1>'''
page+='<p>'+esc(p['schematic_revision'])+' | Review '+esc(p['date'])+' | All 44 unknown ceramics covered</p>'
page+='<div class="note"><b>12 supply starting values, 4 conditional candidates, 28 network constraints.</b> No new measurements are requested now. This is a provisional reconstruction-value table, not a claim to have recovered the factory BOM. Native wiring and recorded values are unchanged.</div>'
page+='<section><h2>What we can infer now</h2><p>The marked resistors already give useful constraints. R24 and R26 are 120 kohm; R23 and R48 are 5.6 kohm. Their ratio is 21.43. A feedback capacitor of 220 pF gives an isolated feedback pole near 6.03 kHz; 270 pF gives 4.91 kHz; 330 pF gives 4.02 kHz. Those are useful receiver-analysis candidates, not the complete two-stage response.</p><p>The six auto-mode readings fall with frequency. Both 100-kHz readings were 240 pF. That makes a few-hundred-pF trial useful, but does not prove 220 pF, 240 pF, or any other nominal: equivalent mode and D are missing, and the op-amp and resistors remain connected.</p><p>Primary datasheets constrain ordinary bypass choices. For example, the candidate U1 accepts at least 100 nF with the specified ESR, while the SGM8542 example combines bulk and local bypass capacitors. These recommendations do not uniquely identify what PetSafe fitted.</p><p><a href="#src-S1200">ABLIC U1 conditions</a> | <a href="#src-SGM">SGMICRO receiver guidance</a> | <a href="#src-PIC">PIC bypass guidance</a></p></section>'
page+='<section><h2>Why RF frequency and physical size are not enough</h2><p>For a simple resonant circuit, <code>Ceq = 1 / ((2 pi f)^2 Lantenna)</code>. At the working hypothesis of 134.2 kHz, the same frequency could require:</p><table class="compact"><thead><tr><th>Example coil inductance (not measured)</th><th>Required equivalent capacitance</th></tr></thead><tbody>'+ant+'</tbody></table><p>The five switched branches contain 15 physical capacitors. Frequency and one coil inductance constrain an equivalent total, not 15 unique values or binary weights. The roughly 5-ohm winding resistance does not establish inductance. L1 and L2 are supply filters, not the antenna coil.</p><p>134.2 kHz is a product-family FDX-B hypothesis, not a measured carrier on this PCB. <a href="#src-PETSAFE">Product-family context</a> | <a href="#src-RF">Antenna design reference</a></p><p>Body size is a weak clue. C30/C31 have 0805 candidates but are crystal-load capacitors in the pF class; a larger tuning capacitor can still have a small capacitance when voltage, low loss or dielectric stability drives its size. Supply replacements must meet effective capacitance under bias, not just their printed nominal. <a href="#src-MURATA">Selection guide</a> | <a href="#src-BIAS">DC-bias effects</a></p></section>'
page+=''.join(sections)
page+='<section><h2>How to finish efficiently</h2><ol>'+''.join('<li>'+esc(x)+'</li>' for x in p['next_actions'])+'</ol><p>Only a reference/equivalent-value decision is available for the 12 supply parts today. The original-value count remains 44; assigning a plausible value does not turn it into a measurement. A fabricated replacement also needs the unresolved device, firmware and layout work already listed in the checklist.</p></section>'
page+='<section><h2>Scope of these proposals</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in p['principles'])+'</ul></section><section><h2>Primary references</h2><ul>'+source_html+'</ul></section><p><a href="../evidence/capacitor_value_review_20261015.json">Machine-readable proposals and calculations</a> | <a href="../evidence/receiver_capacitance_results_20261015.json">Raw readings and qualifications</a></p></html>'
(R/'docs/CAPACITOR_VALUE_REVIEW.html').write_text(page,encoding='utf-8')
print('Capacitor review:',dict(Counter(c['category'] for c in p['components'])))
