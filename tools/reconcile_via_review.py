"""Overlay the user's v0.9 review without changing stable site IDs.

`net` is the reviewed site assignment; `modeled_nets` is descriptive only and
may contain an older unverified hypothesis. Neither expands to the whole net.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json,csv
R=Path(__file__).resolve().parents[1]
def apply(out):
    review=json.loads((R/'evidence/via_user_review.json').read_text())
    model=json.loads((R/'evidence/reconstruction.json').read_text())
    by=defaultdict(list)
    for r in review['reports']:by[r['id']].append(r)
    original_ids=set(by)
    for correction in review.get('followup_corrections',[]):
        for r in correction['assignments']:by[r['id']]=[r]
    current_ids=set(by)
    membership={e:n['net'] for n in model['nets'] for e in n['endpoints']}
    sites={s['id']:s for s in out['sites']}
    conflicts={
        'V073':'User number duplicated: GND and R19. R19 photo endpoint appears at V075. Do not ground R19 from this duplicate.',
        'V113':'User GND conflicts with Q8 outer joined-pad/output model. Check direct resistance to GND; component-net merge held.',
        'V115':'User GND conflicts with Q8 outer joined-pad/output model. Check direct resistance to GND; component-net merge held.'}
    def annotate(ids,ends,note,net=None):
        for i in ids:
            s=sites[f'V{i:03d}'];s['endpoints']=ends;s['component_crosscheck']=note
            if net:s['net']=net
    for s in out['sites']:
        s.pop('conflict',None)
        s.update(active=s['id']!='V050',user_reports=by[s['id']],review_status='USER_REPORTED' if by[s['id']] else 'NOT_IN_USER_LIST')
        kinds={r['kind'] for r in by[s['id']]}
        if 'ground' in kinds:s['net']='H_GND';s['confidence']='User GND report; no per-site ohms supplied'
        if any('MX512' in r['claim'] or (r['kind']=='motor_supply') for r in by[s['id']]):
            s['net']='H_VBAT';s['confidence']='User common-net report to MX512H pin4; no per-site ohms supplied'
        if s['id'] in conflicts:
            s['review_status']='CONFLICT';s['conflict']=conflicts[s['id']]
            if s['id']!='V025':s['net']=None
        if not s['active']:
            s.update(review_status='REJECTED_NOT_VIA',net=None,endpoints=[],note='User rejects V050 as a recognition error. ID retained as a tombstone; excluded from active markers.')
    annotate([1,2],['U5.4'],'MX512H motor VDD, distinct from logic VCC pin1.','H_VBAT')
    annotate([3,4],['C27.1'],'C27 left photo pad on user motor-supply island.','H_VBAT')
    annotate([8,9,10],['C27.2'],'C27 right photo pad on user GND island.','H_GND')
    annotate([11,12,13,14],['Q1.L','R43.2'],'Photo common island to Q1 left pad and R43 lower pad; transistor pin function still a candidate.','Q1_EMITTER')
    annotate([21],['Q9.R'],'Q9 DNP lower-right pad; stock pin2.','H_GND')
    annotate([22],['U4.15'],'User RC4 association; hidden onward destination unknown.')
    annotate([23],['U4.16'],'User RC5 association; hidden onward destination unknown.')
    annotate([24],['R32.1'],'R32 upper photo pad. Old PIR assignment withdrawn.','H_GND')
    annotate([26],['U4.21'],'User correction: V026 goes to PIC21/RB0; remote destination remains unknown.')
    annotate([31],['U4.2','C25.1'],'User RA0/C25 association corroborates existing local signal node.','PIC_RA0_FILTER')
    annotate([35],['U4.4','C39.1'],'Visible local C39 signal-pad route to PIC RA2; remote net unverified.','PIC_RA2_FILTER')
    for i,p in [(36,5),(37,6),(39,7),(47,11),(49,13)]:
        sites[f'V{i:03d}']['candidate_endpoints']=[f'U4.{p}']
        sites[f'V{i:03d}']['component_crosscheck']='Alignment hypothesis under PIC body only; requires continuity. Not a traced connection or NC.'
    annotate([53],['U4.12','VREF.1'],'Visible trace reaches VREF board pad. This local pad connection does not identify an onward buried net.','PIC_RC1_VREF')
    annotate([57,58],['R2.1','C4.1'],'DNP option free pads in the front ground copper.','H_GND')
    annotate([63],['R37.1','R39.2'],'Common lower ends in IMG_2435. Feed voltage/source unknown; old separate VDD/GND guesses withdrawn.','AUX_FEED_V063')
    annotate([64],['R1.1','C3.1','VDD.1','U1.R1'],'Regulated board VDD island. Do not equate this use of VDD with MX512H motor pin4.','H_VDD')
    annotate([67],['U6A.R1'],'Unpopulated U6A upper-right pad to via; remote destination unknown.')
    annotate([70],['R18.1'],'R18 free end; former supply assignment remains an inference, not established by component association alone.')
    annotate([71],['R21.2'],'R21 left/free end in receiver photo; shared bias hypothesis not confirmed by this via report.')
    annotate([72],['R22.2'],'R22 left/free end in receiver photo; shared bias hypothesis not confirmed by this via report.')
    annotate([75],['R19.2'],'R19 right/free end visibly reaches this site. Likely correction of duplicated V073; awaiting user confirmation.')
    annotate([76],['R22.1'],'R22 opposite/right photo pad; user GND corroborates return.','H_GND')
    annotate([82],[],'User associates D3; exact terminal on three-lead package still requires local confirmation.')
    for i,q in [(89,'Q11'),(94,'Q6'),(99,'Q5'),(104,'Q4')]:
        annotate([i],[q+'.L'],'Photo left transistor pad to user GND via; assumed emitter role not confirmed.','H_GND')
    annotate([87,88],[c+'.1' for c in ['C47','C44','C29','C14','C11']],'Shared lower front-capacitor band; old antenna rail assumption withdrawn.','H_GND')
    for i,c in [(93,'C48'),(96,'C45'),(101,'C38'),(105,'C15')]:
        annotate([i],[c+'.1'],'Rear capacitor ground-side land; other pad joins local tuning midpoint.','H_GND')
    for i,n,cs in [(90,5,['C46','C47','C48']),(95,4,['C43','C44','C45']),(100,3,['C16','C29','C38']),(103,2,['C13','C14','C15']),(107,1,['C10','C11','C12'])]:
        annotate([i],[c+'.2' for c in cs],'User front-pair junction plus rear-land photo pairing; onward hidden connection to antenna remains unknown.',f'TUNE_{n}_MID')
    annotate([113,115],['Q8.B1','Q8.B3'],'Outer joined Q8 pads appear on this front island; GND report conflicts with old output hypothesis. No GND merge applied.')
    annotate([116],['R10.2'],'R10 free end; no longer singleton monitor hypothesis.','H_GND')
    for s in out['sites']:
        s['modeled_nets']=sorted({membership[e] for e in s['endpoints'] if e in membership})
        if s['user_reports'] and s['net'] and s['review_status']!='CONFLICT':s['review_status']='ASSIGNED'
        elif not s['user_reports'] and s['net']:s['review_status']='PHOTO_LOCAL'
    out.update(revision='v0.9',user_review_source='evidence/via_user_review.json',
        user_review_method=review['method'],supply_naming=review['supply_naming'],
        review_summary=dict(catalogued_ids=len(sites),active_sites=sum(s['active'] for s in sites.values()),user_reported_ids=len(current_ids),original_user_reported_ids=len(original_ids),
            omitted_from_user_list=sorted(set(sites)-current_ids),rejected=['V050'],conflicts=list(conflicts),
            statuses=dict(Counter(s['review_status'] for s in sites.values()))),
        new_model_connections=json.loads((R/'evidence/v09_net_changes.json').read_text())['changes'])
    return out

if __name__=='__main__':
    p=R/'evidence/via_audit.json';out=apply(json.loads(p.read_text()))
    p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    fields=['id','active','rear_x','rear_y','front_x','front_y','rear_appearance','front_match','review_status','user_claims','endpoints','net','modeled_nets','component_crosscheck','conflict']
    with (R/'evidence/via_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for s in out['sites']:
            w.writerow(dict(id=s['id'],active=s['active'],rear_x=s['rear_xy'][0],rear_y=s['rear_xy'][1],front_x=s['front_xy'][0],front_y=s['front_xy'][1],
                rear_appearance=s['rear_appearance'],front_match=s['front_match'],review_status=s['review_status'],user_claims='; '.join(r['claim'] for r in s['user_reports']),
                endpoints=';'.join(s['endpoints']),net=s['net'] or '',modeled_nets=';'.join(s['modeled_nets']),component_crosscheck=s.get('component_crosscheck',''),conflict=s.get('conflict','')))
    print(out['review_summary'])
