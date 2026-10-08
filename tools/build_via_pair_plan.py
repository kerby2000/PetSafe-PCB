"""Prioritize unpowered continuity work; proposals never alter the circuit model."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,csv
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,d):(R/p).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
a=read('evidence/via_audit.json');m=read('evidence/reconstruction.json')
sites={s['id']:s for s in a['sites']}
excluded={'H_GND','H_VBAT','H_VDD','MOTOR_INA','MOTOR_INB','ICSP_DAT','H_TUNE_1','H_TUNE_2','H_TUNE_3','H_TUNE_4','H_TUNE_5'}
groups=defaultdict(list)
for s in a['sites']:
 if s['active'] and s['net'] not in excluded:
  groups[tuple(s['endpoints']) if s['endpoints'] else (s['id'],)].append(s['id'])
tests=[]
def add(id,group,left,right,reason,confidence,positive,negative):
 assert sites[left]['active'] and sites[right]['active']
 tests.append(dict(id=id,group=group,left=left,right=right,left_endpoint=', '.join(sites[left]['endpoints']) or 'terminal unresolved',right_endpoint=', '.join(sites[right]['endpoints']) or 'terminal unresolved',reason=reason,confidence=confidence,positive_action=positive,negative_action=negative,status='PROPOSED_UNMEASURED',reading=''))
add('B3','B - reference and supply feeds','V064','V070',
    'V070 reaches the free end of R18 feeding the Q7/receiver region. Regulated VDD at V064 is the current plausible supply source.',
    'Moderate supply hypothesis; Q7 role remains provisional.',
    'Record this feed association after reviewing resistance. Q7 terminal functions and receiver bias remain separate questions.',
    'Next round compare V070 with V059 or a switched supply endpoint; select from the first-round results.')
for i,target in enumerate([100,103,107],5):
 add(f'C{i}','C - compare the remaining capacitor junctions','V095',f'V{target:03d}',
     'V090 gave OL to all four other junctions. These three tests check whether the remaining four share a different node; the repeated-cell hypothesis is weaker after the first results. No common antenna node is assumed.',
     'Moderate repeated-circuit hypothesis; no assumed antenna assignment.',
     'Add this junction to the V095 group after review. Continue all three C tests; later measure one group representative to ANT1/ANT2.',
     'Leave this junction outside the V095 group. Continue the other C tests; nonmatching junctions may still form another group.')
plan=dict(id='via-pairs-round-2',pdf_path='output/pdf/PetSafe_via_pair_round2.pdf',date='2026-10-08',basis_revision=m['revision'],schematic_sha256=hashlib.sha256((R/'schematic/PetSafe_1001339.kicad_sch').read_bytes()).hexdigest(),
 status='AWAITING_USER_READINGS',scope='Proposed continuity work only. No unmeasured pair is added to the native schematic or accepted connectivity.',
 count_basis=dict(active_via_sites=120,nonrail_candidate_sites=sum(map(len,groups.values())),local_candidate_groups=len(groups),dnp_group='V067 / U6A',qualification='Groups are local endpoint associations, not a count of proven missing nets. Some modeled local nets need no additional hidden connection. Seven unmentioned IDs are already photo-matched; they are not the full work queue.'),
 local_groups=[dict(vias=ids,endpoints=list(key)) for key,ids in groups.items()],
 known_controls=[['V022','V016'],['V023','V019']],baseline='Short the probes, then check known V022-V016 once to establish actual pad-contact resistance. Prior shorted tips were about 0.5 ohm; use today\'s reading.',
 method=['Battery and programmer disconnected; use resistance mode.',
         'A stable reading close to the known connected-pair baseline supports a DC connection. Recheck near-zero hits with probes reversed; do not rely on a beep alone.',
         'Record actual ohms, kohms, OL, or a changing reading. Tens/hundreds of ohms, one-way conduction or a changing reading are not direct-copper confirmation.',
         'A very low-resistance path can include a zero-ohm link or an inductor; continuity maps electrical connectivity, not exact buried-layer track geometry.',
         'Complete B3 and the three new C comparisons. V090-to-other-midpoint tests all returned OL. Prior tuning controls and V064-V063 are resolved; V053-V071 is explicitly rejected.'],
 tests=tests,reported_results=read('evidence/v096_net_changes.json'),staged_followups=[
 dict(stage='After the remaining supply test',action='If V064-V070 is not direct, compare V070 with motor supply V059 or a switched feed. V064-V063 is already confirmed.'),
 dict(stage='Remaining GPIOs and reference',action='Only PIC13/RC2 via V049 and PIC21/RB0 via V026 remain open. Prioritize receiver/PIR/button endpoints once the remaining group checks return. V053-V071 is rejected; consider V071-V031 or V071-V035 as separate reference/filter hypotheses, not new assignments.'),
 dict(stage='Capacitor bank after C',action='Partition any confirmed groups. If the new C sweep is also all OL, stop broad pairwise testing and trace a junction toward antenna/component endpoints. Check local probe contact against its known capacitor junction before interpreting repeated OL as topology. The four original OL readings exclude V090 direct ties; they do not prove all other junctions isolated.'),
 dict(stage='Remaining functional endpoints',action='Distinguish Q1.L/V011 user-reported VDD between regulated V064 and motor V001 when the user answers the pending question. Target R43.2/V015, V017, V075/Q7 and V082/D3 after narrowing their roles. V114 is now resolved as U2 ground and is excluded. Use TP16/PIR, the receiver output and button pad where no catalogued via is known. V011-V015 is already explicitly excluded; do not repeat it.'),
 dict(stage='Low priority',action='V067 belongs to empty U6A; defer unless it helps another live route. Do not repeat established grounds, motor pairs, Q1 duplicate vias or V079/V080.')],
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
  w.writerow([t['id'],t['left'],t['right'],row.get('reading',''),row.get('reverse_reading',''),row.get('notes','')])
print(f'Plan: {len(groups)} local candidate groups / {sum(map(len,groups.values()))} sites; {len(tests)} next-round candidate tests. No proposed pair added as a circuit connection.')
