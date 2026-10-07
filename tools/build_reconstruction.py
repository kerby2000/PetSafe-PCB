"""Photo-led PetSafe reconstruction. Unresolved pins remain OPEN, not marked NC.
No plausible circuit is silently substituted for a measured/visible connection.
Python 3; standard library only. Native KiCad application validation remains pending.
"""
from pathlib import Path
import json,csv,uuid,re,html,collections
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'evidence'; S=ROOT/'schematic'; E.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
NS=uuid.UUID('6d19bd1d-a0ac-498a-bbe4-a1d6324fe3c9')
def uid(s):return str(uuid.uuid5(NS,s))
comp=[]
def add(ref,kind,value='UNKNOWN',mark='',status='populated',sheet='receiver',source='',pins=None,note='',side='front'):
 if pins is None: pins=['1','2'] if kind in ['R','C','L','D2','Y'] else ['1']
 comp.append(dict(ref=ref,kind=kind,value=value,marking=mark,population=status,sheet=sheet,source=source,pins=pins,note=note,side=side))
# Only designators actually observed. Missing numbers are not invented components.
rv={3:('334','330k'),4:('334','330k'),5:('220','22'),6:('122','1.2k'),7:('182','1.8k'),8:('221','220'),9:('221','220'),10:('01C','10k'),11:('182','1.8k'),13:('182','1.8k'),14:('182','1.8k'),15:('182','1.8k'),16:('182','1.8k'),18:('122','1.2k'),19:('01C','10k'),20:('220','22'),21:('01C','10k'),22:('01C','10k'),23:('562','5.6k'),24:('124','120k'),25:('122','1.2k'),26:('124','120k'),27:('01C','10k'),28:('1004','1M'),29:('18C?','UNKNOWN'),30:('221','220'),31:('221','220'),32:('01C','10k'),33:('01C','10k'),37:('220','22'),38:('01C','10k'),39:('01C','10k'),40:('01C','10k'),41:('33?','UNKNOWN'),42:('122','1.2k'),43:('682','6.8k'),44:('18C?','UNKNOWN'),48:('562','5.6k')}
rsheets={**{i:'control' for i in [3,4,32,40,41,43,44]},**{i:'power' for i in [33,37,38,39]},**{i:'tuning' for i in [11,13,14,15,16]},**{i:'rf_drive' for i in range(5,11)},30:'rf_drive',31:'rf_drive'}
for n,(mark,value) in rv.items():
 sh=rsheets.get(n,'receiver');source={'control':'IMG_2436.jpg;IMG_2437.jpg;IMG_2438.jpg','power':'IMG_2435.jpg','tuning':'IMG_2433.jpg','rf_drive':'IMG_2431.jpg;IMG_2432.jpg','receiver':'IMG_2429.jpg;IMG_2434.jpg'}[sh]
 add('R'+str(n),'R',value,mark,sheet=sh,source=source,note='Value decoded from visible marking, not measured.' if value!='UNKNOWN' else 'Ambiguous printed code; do not choose a nominal value yet.')
for n in [1,2,35,36,46,47]:add('R'+str(n),'R','DNP',status='DNP',sheet={1:'power',2:'power',35:'control',36:'control',46:'receiver',47:'receiver'}[n],source='IMG_2430.jpg;IMG_2434.jpg;IMG_2438.jpg',note='Empty footprint photographed; do not treat as a jumper.')
cdnp={3,4,42,49}; cback={12,15,38,45,48}
csheets={**{i:'control' for i in [25,26,27,28,30,31,32,33,34,35,39,41]},**{i:'power' for i in [1,2,3,4,36,37]},**{i:'rf_drive' for i in [5,6,7,8,9]},**{i:'tuning' for i in [10,11,12,13,14,15,16,29,38,43,44,45,46,47,48,49]}}
for n in range(1,50):
 sh=csheets.get(n,'receiver');src={'control':'IMG_2436.jpg;IMG_2437.jpg;IMG_2438.jpg','power':'IMG_2430.jpg;IMG_2435.jpg','tuning':'IMG_2433.jpg;IMG_2442.jpg','rf_drive':'IMG_2431.jpg;IMG_2432.jpg','receiver':'IMG_2434.jpg'}[sh]
 add('C'+str(n),'C','DNP' if n in cdnp else 'UNKNOWN',status='DNP' if n in cdnp else 'populated',sheet=sh,source=src,side='back' if n in cback or n==49 else 'front',note='Unmarked ceramic: capacitance unknown; no default 100nF assigned.' if n!=5 else 'Electrolytic: body value and voltage not readable; polarity + is printed on PCB.')
for r in ['C1A','C2A']:add(r,'C','DNP',status='DNP',sheet='power',source='IMG_2430.jpg')
for r in ['L1','L2']:add(r,'L','UNKNOWN',sheet='rf_drive' if r=='L1' else 'power',source='IMG_2432.jpg' if r=='L1' else 'IMG_2430.jpg',note='Series two-terminal magnetic component; ferrite bead versus inductor and value not verified.')
add('Y1','Y','20MHz','JH20.000',sheet='control',source='IMG_2436.jpg',note='Nominal frequency from marking; two active terminals. Case connections not inferred.')
add('U4','IC','PIC16F18855','PIC16F18855 /SO',sheet='control',source='IMG_2424.jpg',pins=[str(i) for i in range(1,29)],note='Microchip 28-pin SOIC pinout. Factory firmware unchanged.')
add('U5','IC','MX512H','MX512H',sheet='control',source='IMG_2424.jpg;IMG_2438.jpg',pins=[str(i) for i in range(1,9)],note='Motor driver pinout from manufacturer document; logic and motor supply nets kept distinct.')
add('U3','IC','SGM8542XS','SGM8542XS / 2531C',sheet='receiver',source='IMG_2429.jpg',pins=[str(i) for i in range(1,9)],note='Dual op amp. Standard SOIC-8 mapping verified against manufacturer pin diagram.')
add('U1','IC','UNKNOWN_5PIN','PPEK',sheet='power',source='IMG_2430.jpg',pins=['L1','L2','L3','R1','R2'],note='Physical pads in IMG_2430 upright: left top/middle/bottom, right top/bottom. No assumed LDO pinout.')
add('U2','IC','UNKNOWN_6PIN','C14R?',sheet='rf_drive',source='IMG_2431.jpg',pins=['T1','T2','T3','B1','B2','B3'],note='Physical top/bottom rows, left to right in IMG_2431. Short marking alone is not a unique identification.')
add('U6','IC','UNKNOWN_5PIN','WN23?',sheet='power',source='IMG_2435.jpg',pins=['L1','L2','R1','R2','R3'],note='Physical pads as viewed in IMG_2435; pin functions unresolved.')
add('U6A','IC','DNP',status='DNP',sheet='power',source='IMG_2435.jpg',pins=['L','R1','R2'],note='Alternative three-pad footprint; do not presume electrical equivalence to U6.')
add('U7','CONN','DNP',status='DNP',sheet='power',source='IMG_2441.jpg',pins=['1','2','3'],side='back',note='Three-hole unpopulated footprint; square pad is local pin 1.')
qmark={1:'R1A',2:'1FW / 56',3:'2H',4:'2H',5:'2H',6:'2H',7:'3GW / 54',8:'372A',9:'' ,11:'2H'}
for n,m in qmark.items():
 sh='tuning' if n in [3,4,5,6,11] else 'control' if n in [1,9] else 'power' if n==2 else 'rf_drive' if n==8 else 'receiver'
 add('Q'+str(n),'IC','DNP' if n==9 else 'UNKNOWN',m,'DNP' if n==9 else 'populated',sh,source={'tuning':'IMG_2433.jpg','control':'IMG_2438.jpg','power':'IMG_2435.jpg','rf_drive':'IMG_2431.jpg','receiver':'IMG_2434.jpg'}[sh],pins=['L','R','S'] if n!=8 else ['T1','T2','T3','B1','B2','B3'],note='Physical-pad symbol, not transistor pin-function assignment. L/R = upper pair, S = lower single pad in upright detail photograph.' if n!=8 else 'Six-pad device. Identity and polarity not proven.')
for n in [1,2,3]:add('D'+str(n),'IC','UNKNOWN',mark='A7' if n==1 else '',sheet='rf_drive' if n==1 else 'receiver',source='IMG_2431.jpg' if n==1 else 'IMG_2434.jpg',pins=['L','R','S'],note='Three-terminal diode-designated part. L/R/S are photo pad identifiers, not assumed anodes/cathodes.')
for n in [4,5,6]:add('D'+str(n),'D2','UNKNOWN',sheet='control',source='IMG_2437.jpg',note='Two-terminal diode-designated component; type/polarity not resolved.')
add('S1','SW','pushbutton',sheet='control',source='IMG_2438.jpg',pins=['TL','TR','BL','BR'],note='Four physical leads retained. Internal common pairs require meter check; no invented terminal shorting.')
add('J1','CONN','ICSP header',sheet='control',source='IMG_2437.jpg',pins=['CLK','DAT','GND','VDD','VPP'],note='Pin identifiers use the printed names, not an assumed numeric connector order.')
add('J3','CONN','PIR daughterboard',sheet='power',source='IMG_2435.jpg;IMG_2441.jpg',pins=['1','2','3'],note='1 red, 2 blue, 3 black from rear photo. Electrical meaning still to verify.')
add('J5','CONN','motor connector',sheet='control',source='IMG_2439.jpg',pins=['A','B'],note='Two physical contacts; A/B must be related to red/black motor leads by continuity.')
add('J6','CONN','DNP',status='DNP',sheet='control',source='IMG_2438.jpg',pins=['1','2'])
add('LED1','IC','UNKNOWN_4PAD',sheet='rf_drive',source='IMG_2432.jpg',pins=['TL','TR','BL','BR'],note='Physical four-pad LED package. Number/polarity of internal emitters to measure.')
for n in [1,2,3,4,5,6,7,9,10,11,14,15,16,17]:
 sh='control' if n in[4,9,10,11,14,15,17] else 'power' if n==16 else 'rf_drive' if n in[1,2,3] else 'receiver'
 add('TP'+str(n),'TP','test point',sheet=sh,source={'control':'IMG_2436.jpg;IMG_2437.jpg;IMG_2438.jpg','power':'IMG_2435.jpg','rf_drive':'IMG_2431.jpg;IMG_2432.jpg','receiver':'IMG_2434.jpg'}[sh])
for r,sh in [('GND','power'),('GND_RF','rf_drive'),('VDD','power'),('VREF','power'),('ANT1','tuning'),('ANT2','tuning'),('BATP','control'),('BATN','control')]:
 add(r,'TP',r,sheet=sh,source='IMG_2430.jpg;IMG_2433.jpg;IMG_2435.jpg;IMG_2438.jpg',note='Photo-derived pad alias, not an added part. Label names alone do not connect this pad to IC pins.')
for c in comp:
 if c['ref']=='GND_RF':
  c['source']='IMG_2432.jpg';c['value']='GND (RF end)';c['note']='Second physical pad printed GND near C5. Not merged with the central GND pad until continuity is checked.'
# Schematic electrical connections are intentionally limited to locally visible copper.
# For R/C: pin 1 is left (horizontal part) or top (vertical part) in upright detail source.
# This is a reconstruction convention, not a claim of manufacturer pad numbering.
nets=[]
def net(name,ends,source,note=''):
 nets.append(dict(net=name,endpoints=ends.split(),evidence='VISUAL_LOCAL',source=source,note=note))
# Main control and motor fragments
net('V_MOTOR_OUTB','U5.5 TP15.1','IMG_2438.jpg','Visible trace; J5 contact assignment remains open.')
net('V_U5_LOGIC_CAP','U5.1 C34.1','IMG_2438.jpg')
net('V_U5_MOTOR_CAP','U5.4 C33.1','IMG_2438.jpg')
net('V_U4_RC3','U4.14 TP11.1','IMG_2436.jpg')
net('V_XTAL_LEFT','U4.9 Y1.1 C30.1','IMG_2436.jpg')
net('V_XTAL_RIGHT','U4.10 Y1.2 C31.2','IMG_2436.jpg')
net('V_XTAL_CAP_COMMON','C30.2 C31.1','IMG_2436.jpg','Ground assignment not assumed from capacitor position.')
net('V_Q1_LEFT','Q1.L R43.2','IMG_2438.jpg')
net('V_Q1_RIGHT','Q1.R R44.2','IMG_2438.jpg')
net('V_J6_Q9','J6.1 Q9.S','IMG_2438.jpg','Q9 and J6 not populated. S is single pad above in this particular footprint; see unresolved pad-orientation note.')
# Power region physical pin labels match IMG_2430.
net('V_U1_LEFT_TOP','U1.L1 C1.1','IMG_2430.jpg')
net('V_U1_LEFT_MID','U1.L2 C1.2','IMG_2430.jpg')
net('V_U1_RIGHT_TOP','U1.R1 C2.1 VDD.1','IMG_2430.jpg')
net('V_U1_RIGHT_BOTTOM','U1.R2 R1.2 C3.2','IMG_2430.jpg','Empty R1/C3 pads retained; verify especially before assigning regulator type.')
net('V_Q2_SINGLE','Q2.S TP16.1','IMG_2435.jpg')
# Repeated antenna-switch rows: directly exposed short links only.
for q,r,c in [(11,11,46),(6,16,43),(5,15,16),(4,14,13),(3,13,10)]:
 net(f'V_TUNE_Q{q}_DRIVE',f'R{r}.2 Q{q}.R','IMG_2433.jpg')
 net(f'V_TUNE_Q{q}_CAP',f'Q{q}.S C{c}.1','IMG_2433.jpg')
# Receiver: unequivocal short local leads. Do not infer feedback hidden under body.
net('V_U3_SUPPLY_LOCAL','U3.8 C24.1','IMG_2429.jpg')
net('V_U3_OUTA_LOCAL','U3.1 R27.2','IMG_2429.jpg;IMG_2434.jpg')
net('V_TP6_LOCAL','TP6.1 R27.1 R21.1','IMG_2434.jpg')
net('V_U3_INA_MINUS_LOCAL','U3.2 R26.2','IMG_2429.jpg')
net('V_Q7_BASE_LOCAL','Q7.L R19.1','IMG_2434.jpg')
net('V_Q7_SINGLE_LOCAL','Q7.S R18.1','IMG_2434.jpg')
# Driver discrete short links. Physical D1 S is upper single pad in IMG_2431.
net('V_D1_SINGLE_LOCAL','D1.S R7.1','IMG_2431.jpg')
net('V_U2_T1_LOCAL','U2.T1 D1.L','IMG_2431.jpg')
net('V_U2_B1_LOCAL','U2.B1 R8.1','IMG_2431.jpg')
net('V_U2_B3_LOCAL','U2.B3 R9.1','IMG_2431.jpg')
net('V_Q8_T1_LOCAL','Q8.T1 R8.2','IMG_2431.jpg')
net('V_Q8_T3_LOCAL','Q8.T3 R9.2','IMG_2431.jpg')
net('V_U3_OUTB_LOCAL','U3.7 R24.1','IMG_2429.jpg','Short exposed lead to feedback resistor pad; no hidden-node continuation inferred.')
net('V_U3_INB_MINUS_LOCAL','U3.6 R24.2','IMG_2429.jpg')
net('V_U3_INB_PLUS_LOCAL','U3.5 C18.1','IMG_2429.jpg')
# Prune any link whose orientation cannot yet be mapped safely. Keep as candidate, not copper.
prune={'V_J6_Q9','V_U1_LEFT_MID','V_Q7_BASE_LOCAL','V_Q7_SINGLE_LOCAL','V_D1_SINGLE_LOCAL','V_U2_T1_LOCAL','V_U2_B1_LOCAL','V_U2_B3_LOCAL','V_Q8_T1_LOCAL','V_Q8_T3_LOCAL','V_TP6_LOCAL'}
candidates=[n for n in nets if n['net'] in prune]
nets=[n for n in nets if n['net'] not in prune]
for n in candidates:n['evidence']='CANDIDATE_NOT_CONNECTED'
# Candidate complete tuning strings. Series order is NOT encoded as a fact.
for q,cs in [(3,[10,12,11]),(4,[13,15,14]),(5,[16,38,29]),(6,[43,45,44]),(11,[46,48,47])]:
 candidates.append(dict(net=f'H_TUNE_Q{q}_CHAIN',endpoints=[f'Q{q}.S']+[f'C{c}' for c in cs],evidence='HYPOTHESIS',source='IMG_2433.jpg;IMG_2442.jpg',note='Likely one switched 3-capacitor branch. Determine actual series/parallel topology and antenna endpoint with meter.'))
for c in comp:
 if c['ref'] in {'U5','Q1','S1','C27','C33','C34','R43','R44','TP14','TP15','BATP','BATN','J5'}:c['sheet']='motor'
byref={c['ref']:c for c in comp};seen={}
for n in nets:
 for ep in n['endpoints']:
  ref,pin=ep.rsplit('.',1)
  assert ref in byref and pin in byref[ref]['pins'],ep
  assert ep not in seen,(ep,seen.get(ep),n['net'])
  seen[ep]=n['net']
for c in comp:c['traced_pin_count']=sum(f"{c['ref']}.{p}" in seen for p in c['pins'])
for c in comp:
 if c['ref'] in ['Q7','Q9','D1','D3']:
  c['note']='Physical L/R identify the paired pads, S the single pad. The single pad is ABOVE the pair in the referenced detail image; no function/polarity is implied.'
cols=['ref','kind','value','marking','population','sheet','side','source','note','traced_pin_count']
with open(E/'components.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows({k:c[k] for k in cols} for c in comp)
with open(E/'connections.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['net','endpoints','evidence','source','note']);w.writeheader();w.writerows({**n,'endpoints':' ; '.join(n['endpoints'])} for n in nets)
with open(E/'candidate_connections_NOT_WIRED.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['net','endpoints','evidence','source','note']);w.writeheader();w.writerows({**n,'endpoints':' ; '.join(n['endpoints'])} for n in candidates)
openpins=[]
for c in comp:
 for p in c['pins']:
  if f"{c['ref']}.{p}" not in seen:openpins.append({'ref':c['ref'],'pin':p,'population':c['population'],'status':'UNRESOLVED_NOT_NC','source':c['source']})
with open(E/'unresolved_pins.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(openpins[0]));w.writeheader();w.writerows(openpins)
# Data used by native-file generator, browser viewer, and the continuation task.
model=dict(board='100-1339 R03 A',revision='0.1',status='INCOMPLETE_PHOTO_LED_RECONSTRUCTION',components=comp,nets=nets,candidates=candidates,
           sources={'SGM8542':'https://www.sg-micro.com/product/SGM8542','PIC16F18855':'https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/PIC16%28L%29F18855-75-Data-Sheet-40001802H.pdf','MX512H':'https://jlcpcb.com/partdetail/Mixic-MX512H/C5119047'},
           pin_mapping_note='R/C pin1 = left or top in upright referenced detail photo; verify with atlas. Unknown ICs retain physical pad IDs. No capacitor values were assumed. No board connection has been continuity measured.')
(E/'reconstruction.json').write_text(json.dumps(model,indent=2))
print('Inventory',len(comp),'references,',sum(c['population']=='populated' for c in comp),'populated;',len(nets),'local net fragments;',len(openpins),'unresolved pads')
