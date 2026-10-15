"""Read-only check of the frozen documentation-cleanup milestone, not current state."""
import hashlib, json, subprocess
BASE='522d235bfc9cd1973c41746033a9c38277aa4736'
def blob(path):return subprocess.check_output(['git','show',BASE+':'+path])
def read(path):return json.loads(blob(path))
m=read('evidence/reconstruction.json'); v=read('evidence/validation.json')
w=read('evidence/remaining_work.json'); s=read('evidence/completion_status.json')
assert len(m['nets'])==v['proposed_net_partitions']==83
assert len(m['unresolved_pins'])==v['unresolved_physical_pins']==28
assert v['erc_total']==36
assert all(i['state']=='open' for i in w['issues'])
assert len(s['unknown_ceramic_values'])==44
assert s['current_gpio_pins']==[]
assert hashlib.sha256(blob('schematic/PetSafe_1001339.kicad_sch')).hexdigest()==v['schematic_sha256']
assert len(m['unresolved_pins'])==read('docs/history/pre_cleanup_20261008/evidence/completion_status.json')['unresolved_physical_pins']
print('PASS: frozen 522d235 cleanup snapshot; current completion is not constrained by these totals.')
