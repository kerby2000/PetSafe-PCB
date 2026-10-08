"""Apply the four measured tuning-control pairs and reject the VREF candidate."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
m=read('evidence/reconstruction.json');v=read('evidence/via_user_review.json');l=read('evidence/library_placements.json')
pairs=[(36,108,5,'R14',2),(37,102,6,'R15',3),(39,97,7,'R16',4),(47,91,11,'R11',5)]
changes=[];assignments=[];props={}
for va,vb,pin,res,n in pairs:
 ep=f'U4.{pin}';name=f'H_TUNE_{n}';basis=f'User reports working via pair V{va:03d}-V{vb:03d}: PIC pin{pin} to {res}.1; no numerical resistance supplied.'
 old=next((net['net'] for net in m['nets'] if ep in net['endpoints']),None)
 for net in m['nets']:
  if ep in net['endpoints']:net['endpoints'].remove(ep)
 target=next(net for net in m['nets'] if net['net']==name);target['endpoints'].append(ep);target['v096_evidence']=basis
 changes.append(dict(endpoint=ep,old=old,new=name,basis=basis))
 for i in [va,vb]:assignments.append(dict(id=f'V{i:03d}',kind='component_or_issue',claim=basis))
 props[res]=basis
props['U4']='v0.9.6 user working pairs: 5/RA3 V036-V108 R14; 6/RA4 V037-V102 R15; 7/RA5 V039-V097 R16; 11/RC0 V047-V091 R11. Existing RC6-R13 retained. Only 13/RC2 and 21/RB0 remain without modeled onward routes.'
for c in m['components']:
 if c['ref'] in props:c['v096_summary']=props[c['ref']];c['via_evidence']=props[c['ref']]
for c in l['components']:
 if c['reference'] in props:c.setdefault('properties',{})['ViaEvidence']=props[c['reference']]
m['nets']=[n for n in m['nets'] if n['endpoints']]
for n in m['nets']:n['endpoints']=sorted(set(n['endpoints']))
connected={e for n in m['nets'] for e in n['endpoints']}
m['unresolved_pins']=sorted(e for e in m['pin_positions'] if e not in connected)
m['revision']='v0.9.6'
entry=dict(source='User continuity results 2026-10-08',revision='v0.9.6',answer='Working: V036-V108, V037-V102, V039-V097, V047-V091. Not working: V053-V071.',assignments=assignments,rejected_pairs=[dict(vias=['V053','V071'],status='USER_REJECTED_DIRECT_CONNECTION',reading=None)])
if not any(c.get('revision')=='v0.9.6' for c in v['followup_corrections']):v['followup_corrections'].append(entry)
save('evidence/reconstruction.json',m);save('evidence/library_placements.json',l);save('evidence/via_user_review.json',v)
if not (R/'evidence/v096_net_changes.json').exists():save('evidence/v096_net_changes.json',dict(revision='v0.9.6',changes=changes,confirmed_via_pairs=[[f'V{a:03d}',f'V{b:03d}'] for a,b,_,_,_ in pairs],rejected_pairs=entry['rejected_pairs'],component_evidence=props))
# Preserve the first plan and its reading sheet as historical proposals/results.
if not (R/'evidence/via_pair_round1_plan.json').exists():
 p=read('evidence/via_pair_plan.json');p['status']='USER_RESULTS_RECEIVED';p['reported_results']=entry
 save('evidence/via_pair_round1_plan.json',p)
 (R/'evidence/via_pair_round1_readings.csv').write_bytes((R/'evidence/via_pair_readings.csv').read_bytes())
print('Four tuning-control routes applied; V053-V071 rejected; two open GPIO pads remain.')
