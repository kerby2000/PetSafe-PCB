"""Overlay the user's current review without changing stable site IDs.

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
    conflicts={'V114':'User identifies the opposite centre pad, Q8.T2/package pin2. The follow-up repeats the pad location but does not settle the earlier GND claim versus the existing source-supply hypothesis. No supply-to-ground merge applied.'}
    rejected=['V033','V050','V117','V120','V121','V122','V124']
    def annotate(ids,ends,note,net=None):
        for i in ids:
            s=sites[f'V{i:03d}'];s['endpoints']=ends;s['component_crosscheck']=note
            if net:s['net']=net
    for s in out['sites']:
        s.pop('conflict',None)
        s.update(active=s['id'] not in rejected,user_reports=by[s['id']],review_status='USER_REPORTED' if by[s['id']] else 'NOT_IN_USER_LIST')
        kinds={r['kind'] for r in by[s['id']]}
        if 'ground' in kinds:s['net']='H_GND';s['confidence']='User GND report; no per-site ohms supplied'
        if any('MX512' in r['claim'] or (r['kind']=='motor_supply') for r in by[s['id']]):
            s['net']='H_VBAT';s['confidence']='User common-net report to MX512H pin4; no per-site ohms supplied'
        if s['id'] in conflicts:
            s['review_status']='CONFLICT';s['conflict']=conflicts[s['id']]
            if s['id']!='V025':s['net']=None
        if not s['active']:
            s.update(review_status='REJECTED_NOT_VIA',net=None,endpoints=[],note=f"User rejects {s['id']} as a recognition error. ID retained as a tombstone; excluded from active markers.")
    annotate([1,2],['U5.4'],'MX512H motor VDD, distinct from logic VCC pin1.','H_VBAT')
    annotate([3,4],['C27.1'],'C27 left photo pad on user motor-supply island.','H_VBAT')
    annotate([8,9,10],['C27.2'],'C27 right photo pad on user GND island.','H_GND')
    annotate([6],['C33.2'],'User adds C33 to earlier GND report; pad2 selected from photo/model.','H_GND')
    annotate([7],['C34.2'],'User adds C34 to earlier GND report; pad2 selected from photo/model.','H_GND')
    for i in [11,12,13,14]:
        s=sites[f'V{i:03d}'];s.update(net=None,endpoints=[],excluded_endpoints=['R43.2'],confidence='User explicitly excludes R43.2; island destination unresolved',component_crosscheck='Previous Q1.L/R43.2 island association withdrawn. Earlier user reference to a Q1 pin does not specify its terminal. The separate original local Q1.L-to-R43.2 fragment is retained at V015.')
    annotate([15],['R43.2','Q1.L'],'User identifies R43 lower pad2. Q1.L is the retained original local photo fragment, not an additional user measurement.','Q1_EMITTER')
    annotate([17],['R42.1','R44.1'],'User explicitly names R42.1 and R44; photo selects R44 free pad1. Literal R42 retained; old R42.1-to-ANT2 hypothesis withdrawn.','V017_CONTROL')
    annotate([18],['C35.2'],'User adds C35 to earlier GND report; pad2 selected from photo/model.','H_GND')
    annotate([20],['R40.1'],'User identifies R40; photo selects upper/free pad1 on the existing ICSP DAT node.','ICSP_DAT')
    annotate([21],['Q9.R'],'Q9 DNP lower-right pad; stock pin2.','H_GND')
    annotate([22],['U4.15'],'User RC4 association; hidden onward destination unknown.')
    annotate([23],['U4.16'],'User RC5 association; hidden onward destination unknown.')
    annotate([24],['R32.1'],'R32 upper photo pad. Old PIR assignment withdrawn.','H_GND')
    annotate([26],['U4.21'],'User correction: V026 goes to PIC21/RB0; remote destination remains unknown.')
    annotate([29],['C25.2','C26.2'],'User adds both capacitors to earlier GND report; return pads selected from photos/model. C26.1 remains unresolved.','H_GND')
    annotate([31],['U4.2','C25.1'],'User RA0/C25 association corroborates existing local signal node.','PIC_RA0_FILTER')
    annotate([35],['U4.4','C39.1'],'Visible local C39 signal-pad route to PIC RA2; remote net unverified.','PIC_RA2_FILTER')
    annotate([34],['R3.1'],'User VDD/R3, previously explicitly the same net as V001 and MX512H pin4. This is motor supply H_VBAT, not regulated H_VDD.','H_VBAT')
    annotate([40],['C28.2'],'User adds C28 to earlier GND report; return pad selected from photo/model.','H_GND')
    for i,p in [(36,5),(37,6),(39,7),(47,11),(49,13)]:
        s=sites[f'V{i:03d}'];s.pop('candidate_endpoints',None)
        s.update(endpoints=[f'U4.{p}'],net=None,confidence='User-confirmed PIC pin-to-via association; no new per-site ohms supplied',component_crosscheck='User confirms this PIC pin-to-via connection. Earlier under-body alignment hypothesis superseded. Onward destination remains unknown; not NC. Front marker coordinates remain projected.')
    annotate([53],['U4.12','VREF.1'],'Visible trace reaches VREF board pad. This local pad connection does not identify an onward buried net.','PIC_RC1_VREF')
    annotate([57,58],['R2.1','C4.1'],'DNP option free pads in the front ground copper.','H_GND')
    annotate([59,61],['L2.1'],'User adds L2 to the earlier common motor-supply report; source/right pad1 selected from photo/model.','H_VBAT')
    annotate([60],['Q2.L'],'User adds Q2 to earlier GND report; local ground-side pad selected from photo/model.','H_GND')
    annotate([63],['R37.1','R39.2'],'Common lower ends in IMG_2435. Feed voltage/source unknown; old separate VDD/GND guesses withdrawn.','AUX_FEED_V063')
    annotate([64],['R1.1','C3.1','VDD.1','U1.R1'],'Regulated board VDD island. Do not equate this use of VDD with MX512H motor pin4.','H_VDD')
    annotate([65],['C2.2'],'User adds C2 to earlier GND report; return pad selected from photo/model.','H_GND')
    annotate([68],['C37.2','C36.2'],'User adds both capacitors to earlier GND report; return pads selected from photos/model.','H_GND')
    annotate([67],['U6A.R1'],'Unpopulated U6A upper-right pad to via; remote destination unknown.')
    annotate([70],['R18.1'],'R18 free end; former supply assignment remains an inference, not established by component association alone.')
    annotate([71],['R21.2'],'R21 left/free end in receiver photo; shared bias hypothesis not confirmed by this via report.')
    sites['V072'].update(net='RX_A_FILTER',endpoints=['TP6.1'],excluded_endpoints=['R22.2'],confidence='User identifies TP6 and explicitly excludes R22.2',component_crosscheck='User identifies TP6. Existing C18.2/R27.1 branches on RX_A_FILTER remain hypotheses; the via report does not certify the whole modeled net. TP6 remains separate from U3.5 across C18.')
    sites['V073'].update(net='H_GND',endpoints=[],component_crosscheck='User correction: GND only. R19 association removed; no R19 ground merge. V075 is now user-associated with Q7; its exact terminal is unresolved.')
    sites['V075'].update(net=None,endpoints=[],component_refs=['Q7'],candidate_endpoints=['Q7.R','R19.2'],component_crosscheck='User identifies Q7 but not its terminal. Q7.R and the previous R19.2 continuation are photo candidates only; do not promote an inferred supply/control net to confirmed.')
    annotate([76],['R22.1'],'R22 opposite/right photo pad; user GND corroborates return.','H_GND')
    annotate([77],['C19.2','R29.2'],'User explicitly confirms the C19-R29 junction is GND. R29 opposite the PIC3/TP7 end is pad2; C19 pad2 is assigned to the upper photo pad beside the via. Earlier C19-to-clamp and R29-to-U3.5 guesses withdrawn.','H_GND')
    annotate([78],['C17.2'],'User adds C17 to earlier GND report; return pad selected from existing photo/model.','H_GND')
    annotate([79,80],['U3.5'],'User identifies SGM8542 pin5 for both vias. Existing original C18.1 local fragment retained on RX_B_PLUS; TP6 lies on the opposite side of C18 and is not merged.','RX_B_PLUS')
    for i in [79,80]:sites[f'V{i:03d}']['confidence']='User explicit U3 pin5 association; no new per-site ohms supplied'
    annotate([82],[],'User associates D3; exact terminal on three-lead package still requires local confirmation.')
    sites['V082']['component_refs']=['D3']
    annotate([83],['C40.2'],'User adds C40 to earlier GND report; return pad selected from existing photo/model.','H_GND')
    for i,r,n in [(91,'R11',5),(97,'R16',4),(102,'R15',3),(108,'R14',2)]:
        annotate([i],[r+'.1'],'User identifies resistor; free upper photo pad1 selected. Tuning control role remains a hypothesis and onward GPIO is not identified.',f'H_TUNE_{n}')
    for i,q in [(89,'Q11'),(94,'Q6'),(99,'Q5'),(104,'Q4')]:
        annotate([i],[q+'.L'],'Photo left transistor pad to user GND via; assumed emitter role not confirmed.','H_GND')
    annotate([87,88],[c+'.1' for c in ['C47','C44','C29','C14','C11']],'Shared lower front-capacitor band; old antenna rail assumption withdrawn.','H_GND')
    for i,c in [(93,'C48'),(96,'C45'),(101,'C38'),(105,'C15')]:
        annotate([i],[c+'.1'],'Rear capacitor ground-side land; other pad joins local tuning midpoint.','H_GND')
    for i,n,cs in [(90,5,['C46','C47','C48']),(95,4,['C43','C44','C45']),(100,3,['C16','C29','C38']),(103,2,['C13','C14','C15']),(107,1,['C10','C11','C12'])]:
        annotate([i],[c+'.2' for c in cs],'User front-pair junction plus rear-land photo pairing; onward hidden connection to antenna remains unknown.',f'TUNE_{n}_MID')
    annotate([112],['C8.2'],'User adds C8 to earlier GND report; lower photo return pad selected.','H_GND')
    annotate([113,115],['Q8.B2'],'User corrects island destination to the centre pad: B2/package pin5, already modeled as GND. Previous B1/B3 annotation was wrong. Independent earlier D-E low-resistance evidence for the outer-pad join is retained.','H_GND')
    for i in [113,115]:
        sites[f'V{i:03d}'].update(excluded_endpoints=['Q8.B1','Q8.B3'],confidence='User centre-pad/GND clarification; corroborates earlier S-G low resistance')
    annotate([114],['Q8.T2'],'User: second pin on the opposite side of the package, mapped as T2/package pin2. Follow-up does not establish GND versus source supply; existing supply hypothesis retained separately.')
    annotate([116],['R10.2'],'R10 free end; no longer singleton monitor hypothesis.','H_GND')
    annotate([118],['C7.2'],'User adds C7 to earlier GND report; lower photo return pad selected.','H_GND')
    annotate([119],['C9.2'],'User identifies C9; photo selects lower pad2. GND is retained as the existing photo/model inference, not a new user ground measurement.','H_GND')
    sites['V119']['confidence']='User component association; pad and GND inferred from photo/model'
    for s in out['sites']:
        s['modeled_nets']=sorted({membership[e] for e in s['endpoints'] if e in membership})
        if not s['active']:
            s.update(review_status='REJECTED_NOT_VIA',net=None,endpoints=[],modeled_nets=[],component_crosscheck='User rejects this detection as not a via. Stable ID retained; excluded from active markers.')
        elif s['user_reports'] and s['net'] and s['review_status']!='CONFLICT':s['review_status']='ASSIGNED'
        elif not s['user_reports'] and s['net']:s['review_status']='PHOTO_LOCAL'
    out.update(revision='v0.9.3',user_review_source='evidence/via_user_review.json',
        user_review_method=review['method'],supply_naming=review['supply_naming'],
        review_summary=dict(catalogued_ids=len(sites),active_sites=sum(s['active'] for s in sites.values()),user_reported_ids=len(current_ids),original_user_reported_ids=len(original_ids),
            omitted_from_user_list=sorted(set(sites)-current_ids),rejected=rejected,conflicts=list(conflicts),
            statuses=dict(Counter(s['review_status'] for s in sites.values()))),
        new_model_connections=json.loads((R/'evidence/v093_net_changes.json').read_text())['changes'])
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
