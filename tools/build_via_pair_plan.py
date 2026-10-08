"""Prioritize unpowered continuity work; proposals never alter the circuit model."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,csv
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,d):(R/p).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
a=read('evidence/via_audit.json');m=read('evidence/reconstruction.json')
sites={s['id']:s for s in a['sites']}
excluded={'BATTERY+','GND','VSYS','VDD','MOTOR_INA','MOTOR_INB','ICSP_DAT','H_TUNE_1','H_TUNE_2','H_TUNE_3','H_TUNE_4','H_TUNE_5','RF_MONITOR_PAD','VREF','H_RX_ENABLE_CTL','H_PIR_VDD','PIC_TP4_C41'}
groups=defaultdict(list)
for s in a['sites']:
 if s['active'] and s['net'] not in excluded:
  groups[tuple(s['endpoints']) if s['endpoints'] else (s['id'],)].append(s['id'])
tests=[]
def add(id,group,left,right,reason,confidence,positive,negative):
 assert sites[left]['active'] and sites[right]['active']
 tests.append(dict(id=id,group=group,left=left,right=right,left_endpoint=', '.join(sites[left]['endpoints']) or 'terminal unresolved',right_endpoint=', '.join(sites[right]['endpoints']) or 'terminal unresolved',reason=reason,confidence=confidence,positive_action=positive,negative_action=negative,status='PROPOSED_UNMEASURED',reading=''))
add('F1','Completed - RC1 to R18','V053','V070',
    'User checked V053-V070 and confirmed connection. Existing local mappings place PIC12/RC1 at V053 and R18.1 at V070. This completes the formerly open GPIO checklist.',
    'User continuity report; no numerical resistance supplied. Q7 local topology/function remains inferred.',
    'Recorded in the schematic as H_RX_ENABLE_CTL. No repeat measurement requested.',
    'V053-VREF was explicitly rejected; RC1 and RB0/VREF remain separate.')
tests[0].update(status='USER_CONFIRMED',reading='Connected; no numeric resistance supplied')
reported=read('evidence/v096_net_changes.json')
followup=read('evidence/via_pair_followup_20261008.json')
for key in ['confirmed_via_pairs','rejected_pairs']:reported[key]+=followup[key]
reported['via_only_followup']=followup
latest=read('evidence/v097_net_changes.json')
reported['rejected_pairs']+=latest['rejected_pairs']
reported['previous_schematic_update']=latest
reported['latest_schematic_update']=read('evidence/v098_net_changes.json')
reported['confirmed_via_pairs']+=reported['latest_schematic_update']['confirmed_via_pairs']
reported['rejected_pairs']+=reported['latest_schematic_update']['rejected_pairs']
variable=read('evidence/via_pair_followup_20261008_rc2.json')
reported['inconclusive_pairs']=variable['inconclusive_pairs']
reported['power_path_update']=read('evidence/v099_net_changes.json')
plan=dict(id='via-pairs-round-6-completed',pdf_path='output/pdf/PetSafe_via_pair_next_check.pdf',date='2026-10-08',basis_revision=m['revision'],schematic_sha256=hashlib.sha256((R/'schematic/PetSafe_1001339.kicad_sch').read_bytes()).hexdigest(),
 status='CURRENT_GPIO_BATCH_COMPLETE',scope='Completed result locator. No repeat measurement requested; no unmeasured pair is added to accepted connectivity.',
 count_basis=dict(active_via_sites=120,nonrail_candidate_sites=sum(map(len,groups.values())),local_candidate_groups=len(groups),dnp_group='V067/U6A now mapped to J3.1/PIR supply; excluded from search pool',qualification='Groups are local endpoint associations, not a count of proven missing nets. Some modeled local nets need no additional hidden connection. Four unmentioned IDs are already photo-matched; they are not the full work queue.'),
 local_groups=[dict(vias=ids,endpoints=list(key)) for key,ids in groups.items()],
 known_controls=[['V022','V016'],['V023','V019']],baseline='Short the probes, then check known V022-V016 once to establish actual pad-contact resistance. Prior shorted tips were about 0.5 ohm; use today\'s reading.',
 method=['Battery and programmer disconnected; use resistance mode.',
         'A stable reading close to the known connected-pair baseline supports a DC connection. Recheck near-zero hits with probes reversed; do not rely on a beep alone.',
         'Record actual ohms, kohms, OL, or a changing reading. Tens/hundreds of ohms, one-way conduction or a changing reading are not direct-copper confirmation.',
         'A very low-resistance path can include a zero-ohm link or an inductor; continuity maps electrical connectivity, not exact buried-layer track geometry.',
         'B3 V064-V070 returned 11.2 kohm: a resistive path, not a direct rail tie. D1 V070-V049 gave variable 200-300 kohm; no continuity demonstrated. RB0/V026 now reaches VREF; D2 was unmeasured and is withdrawn from this batch. E1 was resolved by the user: V053 is NOT connected to VREF. F1 V053-V070 is confirmed; V067-J3.1 also confirmed. All seven capacitor comparisons returned OL; broad capacitor-pair testing is retired.'],
 tests=tests,reported_results=reported,staged_followups=[
 dict(stage='Q7 and R18',action='The 11.2 kohm result matches R18+R19 nominal resistance. With V075 at VDD and IMG_2434, this supports R19 as a base-emitter pull-up and R18 as a series base-drive resistor. The native v0.9.8 reconstruction uses this qualified topology; in-circuit resistance alone does not uniquely prove it.'),
 dict(stage='PIC updates and reference',action='User confirms RC2/V049 to TP3, RB0/V026 to VREF (native TP104), and V071/R21.2 to VREF. RC1/PIC12 now reaches R18 via V053-V070; old V053-VREF link rejected. No PIC pads remain open in the model. Other inferred branches and remote roles still need review.'),
 dict(stage='Capacitor search stopped',action='The first sweep tested V090 against four nodes; the second tested whether the other four shared a separate node. Seven OL results weaken that repeated-cell common-node hypothesis. No more broad pairwise tests are queued. V100-V103, V100-V107 and V103-V107 remain untested; no mutual isolation is assumed. Any next capacitor check must follow a visible trace or a specific antenna/component endpoint.'),
 dict(stage='Remaining functional endpoints',action='Q1.L/V011-V014 now confirmed to motor VDD/U5 pin4; no further rail-disambiguation test requested. Q1 is an R1A/FMOS3401A-class PMOS candidate. Raw battery BATTERY+ is distinct from post-Q1 VSYS; TP14 is on the raw side by photo. V015/R43.2 now reaches TP14; V017/R42.1/R44.1 reaches TP4/PIC25. V082 now reaches TP103/logic VDD; identify the exact D3 terminal without merging H_RX_VDD. V075 has a confirmed rail and photo/resistance-supported Q7/R19 terminal assignments; Q7 identity, orientation and function remain qualified. V011-V015 is explicitly excluded.'),
 dict(stage='Low priority',action='V067 now connects J3.1/PIR supply to the earlier U6A pad association. U6A remains DNP; this does not identify an IC. Do not repeat established grounds, motor pairs, Q1 duplicate vias or V079/V080.')],
 photos=dict(front=a['source_front'],rear=a['source_rear'],orientation='Rear mosaic is already mirrored to match front orientation; compare using landmarks before probing.',marker_basis='Rear coordinates are the established via IDs. Front coordinates are mostly projections; no new trace route is claimed.'))
save('evidence/via_pair_plan.json',plan)
reading_path=R/'evidence/via_pair_readings.csv'
previous={}
if reading_path.exists():
 with reading_path.open(encoding='utf-8',newline='') as f:previous={r['test_id']:r for r in csv.DictReader(f)}
with reading_path.open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['test_id','probe_1','probe_2','reading','reverse_reading','notes'])
 for t in tests:
  row=previous.get(t['id'],{})
  if row:assert (row['probe_1'],row['probe_2'])==(t['left'],t['right']), 'Existing readings belong to a different pair; preserve them separately before changing the plan'
  w.writerow([t['id'],t['left'],t['right'],row.get('reading',t['reading']),row.get('reverse_reading',''),row.get('notes','')])
print(f"Plan: {len(groups)} local candidate groups / {sum(map(len,groups.values()))} sites; {sum(t['status']=='PROPOSED_UNMEASURED' for t in tests)} proposed tests; completed result locator retained.")
