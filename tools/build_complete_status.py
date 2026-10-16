"""Refresh status/GPIO data for the HTML report; no duplicate completion PDF."""
from pathlib import Path
from collections import Counter
import json,csv
from current_state import current_state

R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
m=read('evidence/reconstruction.json');v=read('evidence/validation.json');a=read('evidence/via_audit.json')
cs={c['ref']:c for c in m['components']};member={e:n['net'] for n in m['nets'] for e in n['endpoints']}
counts=Counter(cs[e.rsplit('.',1)[0]]['population'] for e in m['unresolved_pins'])
fitted=sorted(e for e in m['unresolved_pins'] if cs[e.rsplit('.',1)[0]]['population']!='DNP')
dnp=sorted(e for e in m['unresolved_pins'] if cs[e.rsplit('.',1)[0]]['population']=='DNP')
gpios=[int(e.split('.')[1]) for e in fitted if e.startswith('U4.')];gpios.sort()
func={p['pin']:p['function'] for p in read('evidence/pic_trace_audit.json')['pins']}
local={1:'J1.1/VPP plus D6 cathode; D6 W-VPP 1 ohm, forward 0.7V from GND',2:'C25 / V031 to TP6 / R27.1 / C18.2: B59 = 1.5 ohm; RX_A_FILTER',3:'C26 signal pad (user annotation); R28 + R29 + TP7 (earlier meter/trace)',4:'VREF TP via V035; user confirms via-to-TP; C39.1 local photo route',
5:'V036-V108 to R14; user continuity report',6:'V037-V102 to R15; user continuity report',7:'V039-V097 to R16; user continuity report',8:'GND / V041 photo anchor',9:'Y1 oscillator; photo-derived',10:'Y1 oscillator; photo-derived',
11:'V047-V091 to R11; user continuity report',12:'R18.1 via V053-V070; user-confirmed; VREF link explicitly rejected',13:'TP3 via V049 (user); R10/R6/R7/D1 midpoint from IMG_2431; excitation waveform unmeasured',14:'TP11; supported local route; hidden continuation/firmware purpose unproved (E06 limitation)',
15:'V022-V016 to U5 pin2 / INA; user-confirmed',16:'V023-V019 to U5 pin3 / INB; user-confirmed',17:'R13; user meter / visible trace',18:'TP17; supported local route; hidden continuation/firmware purpose unproved; R13 belongs to RC6',19:'GND / C32 / V045 photo anchor',20:'V042 to board VDD TP user-confirmed; C32.1 local photo route',
21:'TP16/Q2.S; user correction. Old VREF join rejected; TP16-VREF 800 kohm',22:'TP2 / R31 / green LED branch; user meter, visible trace and B42 colour',23:'TP1 / R30 / red LED branch; user meter, visible trace and B43 colour',24:'R4; photo-derived; sensing role remains inferred',25:'TP4 / V017 / R42.1 / R44.1; user continuity; C41 photo-derived',26:'TP10 / R35; user meter / visible trace',27:'ICSP CLK / D4 / R32; photo-derived',28:'ICSP DAT / D5 / R40; photo-derived'}
pins=[dict(pin=n,gpio=func[n],net=member.get(f'U4.{n}'),open_pad=n in gpios,evidence=local[n]) for n in range(1,29)]
status=current_state()
queue=read('evidence/finishing_measurements.json')
save('evidence/completion_status.json',status)
# Refresh the formerly stale v0.7 audit from the maintained per-pin register.
# Function names retain their manufacturer pinout source; recorded evidence is not upgraded.
pin_audit=read('evidence/pic_trace_audit.json')
save('evidence/pic_trace_audit.json',dict(revision=m['revision'],
    pin_number_source=pin_audit['pin_number_source'],source_url=pin_audit['source_url'],
    interpretation='Current modeled routes and evidence qualifications. No claim of exhaustive hidden-layer connectivity.',
    historical_source='docs/history/e06-v0941/pic_trace_audit.json',
    open_gpio_pins=gpios,
    pins=[dict(pin=p['pin'],function=p['gpio'],net=p['net'],status='LOCAL_ROUTE_MODELED',evidence=p['evidence']) for p in pins]))
save('evidence/pic_gpio_status.json',dict(revision=m['revision'],pins=pins,open_gpio_pins=gpios,qualification='A modeled local net does not certify its remote role or all attached inferred branches.'))
with (R/'evidence/pic_gpio_status.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(pins[0]));w.writeheader();w.writerows(pins)

print("Status and GPIO data refreshed; HTML checklist is the current report.")
