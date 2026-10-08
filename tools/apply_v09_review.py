"""Apply the reviewed v0.9 endpoint corrections; safe to rerun.

This is a migration of explicit evidence, not an automatic via-to-net detector.
The companion review overlay preserves unresolved/conflicting user reports.
"""
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
m=read('evidence/reconstruction.json');l=read('evidence/library_layout.json')
before={e:n['net'] for n in m['nets'] for e in n['endpoints']}
changes=[]
def assign(net,ends,basis):
    target=next((n for n in m['nets'] if n['net']==net),None)
    if target is None:
        target=dict(net=net,endpoints=[],status='Local photo/user association; remote continuation unresolved',original_fragments=[])
        m['nets'].append(target)
    for ep in ends:
        for n in m['nets']:
            if ep in n['endpoints']:n['endpoints'].remove(ep)
        target['endpoints'].append(ep)
        if before.get(ep)!=net:changes.append(dict(endpoint=ep,old=before.get(ep),new=net,basis=basis))
        c=next(c for c in m['components'] if c['ref']==ep.rsplit('.',1)[0])
        c.setdefault('v09_evidence',{})[ep]=basis
    target.setdefault('v09_evidence',[])
    if basis not in target['v09_evidence']:target['v09_evidence'].append(basis)

assign('H_VBAT',['C27.1'],'C27 photo left pad to V003/V004; user ties these to MX512H pin4 motor VDD.')
assign('H_GND',['C27.2'],'C27 photo right pad to V008/V009/V010 user GND.')
assign('H_VDD',['R1.1','C3.1'],'DNP free pads via V064 to board VDD test point / U1 output. This is distinct from MX512H pin4 motor VDD.')
assign('H_GND',['R2.1','C4.1'],'DNP free pads lie on front ground copper shared with V057/V058.')
assign('AUX_FEED_V063',['R37.1','R39.2'],'User V063 joins R37 and R39; photo identifies their lower ends. Withdraw conflicting H_VDD and GND guesses. Remote feed unknown.')
assign('H_GND',['R10.2'],'R10 free end visibly joins V116, user GND.')
assign('H_GND',['R32.1'],'R32 photo upper pad to V024, user GND; withdraw earlier PIR-signal guess.')
assign('H_GND',['Q9.R'],'DNP Q9 lower-right pad to V021, user GND; pad mapping R=stock pin2.')
assign('PIC_RC1_VREF',['U4.12','VREF.1'],'PIC pin12 visible trace reaches V053, the VREF-labelled board pad. Remote continuation/function remains unknown.')
assign('H_GND',['Q11.L','Q6.L','Q5.L','Q4.L','Q3.L'],'First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established.')
assign('H_GND',[f'{c}.1' for c in ['C47','C44','C29','C14','C11']],'Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown.')
assign('H_GND',[f'{c}.1' for c in ['C48','C45','C38','C15','C12']],'Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping.')
m['nets']=[n for n in m['nets'] if n['endpoints']]
for n in m['nets']:n['endpoints']=sorted(set(n['endpoints']))
m['nets'].sort(key=lambda n:n['net'])
connected={e for n in m['nets'] for e in n['endpoints']}
m['unresolved_pins']=sorted(e for e in m['pin_positions'] if e not in connected)
m['revision']='v0.9'
save('evidence/reconstruction.json',m)
if changes:
    save('evidence/v09_net_changes.json',dict(revision='v0.9',changes=changes,
        held=['V073 GND / R19 duplicate number','V113/V115 GND conflicts with Q8 joined-output hypothesis'],
        qualification='User via claims plus component-pad photo cross-checks. No new individual resistance or voltage measurements supplied. Existing unrelated hypotheses retained.'))

# Route-bank buses: separate antenna pads from the now-grounded bank rails.
for w in l['wires']:
    if w['net']=='H_ANT_B' and w['a'][1]>=235 and w['b'][1]>=235:
        w['net']='H_GND'
        if w['a']==[17,235]:w['a']=[36,235]
    if w['net']=='H_ANT_A' and w['a'][1]>=278 and w['b'][1]>=278:
        w['net']='H_GND'
        if w['a']==[17,287]:w['a']=[42,287]
    if w['net']=='H_RF_MONITOR':w['net']='H_GND'
    if w['net']=='H_GND' and w['a']==[277,283] and w['b']==[274,283]:w['net']='AUX_FEED_V063'
l['wires']=[w for w in l['wires'] if not (w['net']=='H_PIR_SIG' and (w['a'][0]==301 or w['b'][0]==301))]
for lb in l['labels']:
    if lb['net']=='H_RF_MONITOR':lb['net']='H_GND'
    if lb['net']=='H_ANT_B' and lb['p']==[25,235]:lb.update(net='H_GND',p=[36,235])
    if lb['net']=='H_ANT_A' and lb['p']==[25,287]:lb.update(net='H_GND',p=[42,287])
save('evidence/library_layout.json',l)
print('Changed endpoints:',len(changes),'open pads:',len(m['unresolved_pins']))
