"""Record the latest user corrections without merging the two VDD rails."""
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
def read(p): return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,v): (R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')

m=read('evidence/reconstruction.json');l=read('evidence/library_layout.json')
v=read('evidence/via_user_review.json');placements=read('evidence/library_placements.json')
summary={
 'Q1':'v0.9.5: V011-V014 reach Q1.L and user reports VDD. Which VDD rail remains to be distinguished (V064 regulated versus V001 motor supply). R43.2/V015 remains explicitly separate. No transistor polarity inferred from the supply report.',
 'U2':'v0.9.5: V114 reaches U2.T2, not Q8.T2. Earlier user GND assignment retained; native U2 pin2 already GND. This resolves the via annotation conflict.',
 'Q8':'v0.9.5: V113/V115 reach centre B2/pin5 GND. V114 belongs to U2.T2 and supplies no evidence about Q8.T2. Existing Q8.T2 supply hypothesis and outer-drain join remain independently qualified.',
 'C5':'v0.9.5: V125/V126 reach C5 negative terminal, native pad2, GND. Confirms existing ground assignment; 470uF/16V value retained.',
 'LED1':'v0.9.5: V127 is GND and reaches LED1. IMG_2432 shows the common pair opposite the resistor-fed pads; these are the existing model BL/BR pair (stock pins3/4), now grounded. Physical orientation and internal colour/polarity mapping remain provisional.'}
assignments=[dict(id=f'V{i:03d}',claim='Q1.L, clearly VDD; regulated versus motor VDD not yet distinguished; not R43.2',kind='supply_unspecified') for i in [11,12,13,14]]
assignments += [dict(id='V114',claim='U2.T2, not Q8.T2; earlier GND report retained',kind='ground')]
assignments += [dict(id=f'V{i:03d}',claim='C5 negative terminal; earlier GND report retained',kind='ground') for i in [125,126]]
assignments += [dict(id='V127',claim='GND and LED1; common pair selected from existing photo/model',kind='ground')]
entry=dict(source='User incremental via review 2026-10-08',revision='v0.9.5',answer='V127 - GND and LED1\nV126,125 - C5(- terminal)\nV114 - U2.T2 not Q8.T2\nV011,V012,V013,V014 - Clearly VDD',assignments=assignments)
if not any(c.get('revision')=='v0.9.5' for c in v['followup_corrections']):v['followup_corrections'].append(entry)
v['remaining_model_conflicts']=[]
v['pending_supply_disambiguation']={'vias':['V011','V012','V013','V014'],'endpoint':'Q1.L','reported':'VDD','options':{'H_VDD':'V064 / regulated board VDD','H_VBAT':'V001 / MX512H motor VDD'},'status':'AWAITING_USER_CLARIFICATION'}
save('evidence/via_user_review.json',v)
changes=[]
for ep in ['LED1.BL','LED1.BR']:
 for n in m['nets']:
  if ep in n['endpoints']:
   if n['net']!='H_GND':changes.append(dict(endpoint=ep,old=n['net'],new='H_GND',basis=summary['LED1']))
   n['endpoints'].remove(ep)
 next(n for n in m['nets'] if n['net']=='H_GND')['endpoints'].append(ep)
m['nets']=[n for n in m['nets'] if n['endpoints']]
for n in m['nets']:n['endpoints']=sorted(set(n['endpoints']))
for c in m['components']:
 if c['ref'] in summary:
  c['via_evidence']=summary[c['ref']];c['v095_summary']=summary[c['ref']]
for c in placements['components']:
 if c['reference'] in summary:c.setdefault('properties',{})['ViaEvidence']=summary[c['reference']]
for w in l['wires']:
 if w['net']=='H_LED_COMMON':w['net']='H_GND'
for key in ['labels']:
 for item in l.get(key,[]):
  if item.get('net')=='H_LED_COMMON':item['net']='H_GND'
m['revision']='v0.9.5'
save('evidence/reconstruction.json',m);save('evidence/library_layout.json',l);save('evidence/library_placements.json',placements)
changefile=R/'evidence/v095_net_changes.json'
if not changefile.exists():
 save('evidence/v095_net_changes.json',dict(revision='v0.9.5',changes=changes,corrected_via_ids=[a['id'] for a in assignments],confirmed_existing_ground_pads=['U2.T2','C5.2'],resolved_conflicts=['V114'],pending_supply_disambiguation=v['pending_supply_disambiguation'],component_evidence=summary))
print('Applied v0.9.5 user reports; LED common grounded; V114 corrected to U2; Q1 rail choice pending.')
