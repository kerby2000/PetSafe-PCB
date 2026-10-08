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
    'V075 is now confirmed on regulated VDD. This DIFFERENT test checks the older assumption that V070, the free end of R18, is also on that rail. The Q7/R19 photo suggests a possible supply-switch arrangement in which R18 could instead carry a control signal.',
    'Diagnostic check of an older supply hypothesis, not a predicted hit. Q7 terminal functions and the R18 route remain provisional.',
    'Record V070 as regulated VDD after reviewing the resistance; re-evaluate the local Q7/R18 topology before merging device terminals.',
    'Withdraw the R18 supply hypothesis if a direct tie is excluded. Trace its local Q7 pad, then choose a remaining GPIO/control endpoint; do not launch another rail sweep.')
reported=read('evidence/v096_net_changes.json')
followup=read('evidence/via_pair_followup_20261008.json')
for key in ['confirmed_via_pairs','rejected_pairs']:reported[key]+=followup[key]
reported['latest_via_only_followup']=followup
plan=dict(id='via-pairs-round-3',pdf_path='output/pdf/PetSafe_via_pair_next_check.pdf',date='2026-10-08',basis_revision=m['revision'],schematic_sha256=hashlib.sha256((R/'schematic/PetSafe_1001339.kicad_sch').read_bytes()).hexdigest(),
 status='AWAITING_USER_READINGS',scope='Proposed continuity work only. No unmeasured pair is added to the native schematic or accepted connectivity.',
 count_basis=dict(active_via_sites=120,nonrail_candidate_sites=sum(map(len,groups.values())),local_candidate_groups=len(groups),dnp_group='V067 / U6A',qualification='Groups are local endpoint associations, not a count of proven missing nets. Some modeled local nets need no additional hidden connection. Seven unmentioned IDs are already photo-matched; they are not the full work queue.'),
 local_groups=[dict(vias=ids,endpoints=list(key)) for key,ids in groups.items()],
 known_controls=[['V022','V016'],['V023','V019']],baseline='Short the probes, then check known V022-V016 once to establish actual pad-contact resistance. Prior shorted tips were about 0.5 ohm; use today\'s reading.',
 method=['Battery and programmer disconnected; use resistance mode.',
         'A stable reading close to the known connected-pair baseline supports a DC connection. Recheck near-zero hits with probes reversed; do not rely on a beep alone.',
         'Record actual ohms, kohms, OL, or a changing reading. Tens/hundreds of ohms, one-way conduction or a changing reading are not direct-copper confirmation.',
         'A very low-resistance path can include a zero-ohm link or an inductor; continuity maps electrical connectivity, not exact buried-layer track geometry.',
         'Only B3 remains in this batch. V064-V075 is confirmed, but V064-V070 is unreported. All seven capacitor comparisons returned OL; broad capacitor-pair testing is retired.'],
 tests=tests,reported_results=reported,staged_followups=[
 dict(stage='Q7 and R18',action='V075 is on regulated VDD. IMG_2434 suggests its continuation to Q7.R/R19.2, with a possible PNP supply-switch role. The exact pad association and R18 supply/control role remain provisional. B3 tests the older R18 rail assignment. An OL result would favor investigating a control route, not prove one.'),
 dict(stage='Remaining GPIOs and reference',action='Only PIC13/RC2 via V049 and PIC21/RB0 via V026 remain open. After the local R18 route is checked, these are plausible control endpoints, not connections established by elimination. V053-V071 is rejected; V031/RA0 and V035/RA2 remain separate reference/filter candidates.'),
 dict(stage='Capacitor search stopped',action='The first sweep tested V090 against four nodes; the second tested whether the other four shared a separate node. Seven OL results weaken that repeated-cell common-node hypothesis. No more broad pairwise tests are queued. V100-V103, V100-V107 and V103-V107 remain untested; no mutual isolation is assumed. Any next capacitor check must follow a visible trace or a specific antenna/component endpoint.'),
 dict(stage='Remaining functional endpoints',action='Distinguish Q1.L/V011 user-reported VDD between regulated V064 and motor V001 when the user answers the pending question. Target R43.2/V015, V017 and V082/D3 after narrowing their roles. V075 has a known rail but an unresolved device terminal, so removal from the unknown-net pool does not mean Q7 is solved. V011-V015 is explicitly excluded.'),
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
