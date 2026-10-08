"""Route MCP-placed library symbols, keeping the physical-pad crosswalk explicit.

Requires sexpdata (available in the KiCad MCP virtual environment). Symbol artwork,
pin definitions and numbering are never generated or changed by this script.
"""
from pathlib import Path
from collections import defaultdict
import json, math, uuid, sys
import sexpdata as sx

R=Path(__file__).resolve().parents[1]; STAGE=R/'.cache/v03'
S=sx.Symbol
def tag(e):return str(e[0]) if isinstance(e,list) and e else ''
def children(e,t):return [x for x in e if tag(x)==t]
def one(e,t):return next((x for x in e if tag(x)==t),None)
def q(s):return json.dumps(str(s),ensure_ascii=False)
def uid():return str(uuid.uuid4())
def expr(s):return sx.loads(s)
def rnd(v):return round(float(v),5)
def xy(p):return tuple(rnd(v) for v in p)
def mm(p):return tuple(rnd(round(v)*1.27) for v in p)

STAGE.mkdir(parents=True,exist_ok=True)
layout=json.loads((R/'evidence/library_layout.json').read_text())
model=json.loads((R/'evidence/reconstruction.json').read_text())
template=R/'tools/templates/mcp_standard_placements.kicad_sch'
if not template.exists():
    template.parent.mkdir(parents=True,exist_ok=True)
    template.write_text((STAGE/'PetSafe_1001339.kicad_sch').read_text(),encoding='utf-8',newline='\n')
tree=sx.loads(template.read_text())
one(tree,'paper')[1]='A2'
libs={x[1]:x for x in children(one(tree,'lib_symbols'),'symbol')}
instances=children(tree,'symbol'); assert len(instances)==155
catalog={(i['reference'],i['unit']):i for i in layout['catalog']}
P={}; PIN_ANGLE={}; BYREF={}; ALL_NATIVE={}
for inst in instances:
    ref=next(p[2] for p in children(inst,'property') if p[1]=='Reference')
    unit=int(one(inst,'unit')[1]); c=catalog[(ref,unit)]; old=c['legacy']; lid=one(inst,'lib_id')[1]
    x,y,rot=map(float,one(inst,'at')[1:]); rad=math.radians(rot)
    if ref in ['TP9','TP10','TP104']:
        y=277*1.27;one(inst,'at')[2]=y
    BYREF[ref]=inst
    for sub in children(libs[lid],'symbol'):
        u,style=map(int,sub[1].rsplit('_',2)[1:])
        if u not in (0,unit) or style not in (0,1):continue
        for p in children(sub,'pin'):
            pn=str(one(p,'number')[1]);px,py,angle=map(float,one(p,'at')[1:])
            mirror=one(inst,'mirror')
            if mirror:
                if str(mirror[1])=='x':py=-py
                if str(mirror[1])=='y':px=-px
            xx=x+px*math.cos(rad)-py*math.sin(rad)
            yy=y-(px*math.sin(rad)+py*math.cos(rad))
            ALL_NATIVE[ref+'.'+pn]=xy((xx,yy))
            PIN_ANGLE[ref+'.'+pn]=int((angle+rot)%360)
    # Use legible, horizontal 1 mm fields; retaining library definitions intact.
    props={p[1]:p for p in children(inst,'property')}
    props['Value'][2]=c['placement']['value']
    props['Footprint'][2]=c['footprint']
    if ref in ['U1','U5','U6','Q8','D2','D3','D4','D5','D6','R41']:
        props['Value'][2]=c['placement']['value']
        props['Footprint'][2]=c['footprint']
        library_properties={p[1]:p[2] for p in children(libs[lid],'property')}
        for name in ['Datasheet','Description']:
            props[name][2]=c.get(name.lower(),library_properties[name])
    rx,ry,vx,vy=(old[k]*1.27 for k in ['rx','ry','vx','vy'])
    # Standard symbol bodies have different extents from the earlier sketches.
    if ref=='U4':rx=vx=x;ry=y-29.21;vy=y-27.305
    if ref in ['U2','U3'] and unit==3:rx=vx=x-12.7;ry=y-1.27;vy=y+0.635
    if ref=='U2' and unit in [1,2]:rx=vx=x;ry=y-12.065;vy=y-10.16
    if ref in ['U1','U5','U6','Q8']:rx=vx=x;ry=y-10.16;vy=y-8.255
    if ref=='U1':ry=y-12.7;vy=y-10.795
    if ref=='U5':ry=y-22.86;vy=y-20.955
    if ref=='U6':rx=vx=x+15.24;ry=y-8.89;vy=y-6.985
    if ref=='Q8':rx=vx=x+12.7;ry=y-1.27;vy=y+0.635
    if ref in ['J1','J3','J5']:rx=vx=x+2.54;ry=y-3.81;vy=y-1.905
    if ref=='Q1':rx=vx=x+11.43;ry=y-5.08;vy=y-3.175;just='left'
    if ref=='Y1':rx=vx=x;ry=y-5.08;vy=y-3.175
    if ref in ['C30','C31']:rx=vx=x+2.54;ry=y-0.635;vy=y+1.27
    if ref=='TP11':rx=vx=x-12.7;ry=y-1.27;vy=y+0.635
    if ref=='R32':rx=vx=x+4.445;ry=y-0.635;vy=y+1.27
    if ref in ['TP1','TP2']:rx=vx=x+7.62;ry=y-1.27;vy=y+0.635
    if ref=='S1':rx=vx=x;ry=y-10.16;vy=y-8.255
    if ref=='C18':rx=vx=x-6.35;ry=y+3.81;vy=y+5.715
    if ref in ['TP9','TP10','TP104']:ry-=24*1.27;vy-=24*1.27
    if rot==180:rx=vx=x+4.445
    for name,px,py in [('Reference',rx,ry),('Value',vx,vy)]:
        prop=props[name];one(prop,'at')[1:]=[rnd(px),rnd(py),int(rot)%180]
        effects=one(prop,'effects')
        if effects:prop.remove(effects)
        just=old.get('just','')
        if ref in ['J1','J3','J5','C30','C31','Q8','U6','Q1','TP1','TP2']:just='left'
        if rot==180:just=''
        prop.append(expr(f'(effects (font (size 1.016 1.016)){" (justify "+just+")" if just else ""})'))
    evidence=next(cc for cc in model['components'] if cc['ref']==old['ref'])
    pop=evidence['value']
    one(inst,'dnp')[1]=S('yes' if pop=='DNP' else 'no')
    policy='User-authorized datasheet symbol created through KiCad MCP' if lid.startswith('PetSafe_Datasheet:') else 'Unmodified KiCad 10 stock symbol'
    for name,val in [('OriginalReference',old['ref']),('Evidence','Photo reconstruction; topology inferred'),
                     ('LibraryPolicy',policy),
                     ('FootprintConfidence',evidence.get('footprint_confidence','unresolved')),
                     ('FootprintBasis',evidence.get('footprint_basis','')),
                     ('PinMapping','See evidence/pin_crosswalk.json; physical orientation may be provisional')]:
        for existing in children(inst,'property'):
            if existing[1]==name:inst.remove(existing)
        inst.append(expr(f'(property {q(name)} {q(val)} (at {x} {y} 0) (effects (font (size 1 1)) hide))'))
for ep,target in layout['crosswalk'].items():P[ep]=ALL_NATIVE[target]
assert len(P)==352
oldpoints={mm(v):P[e] for e,v in layout['pins'].items()}

W=[]; L=[]; G=[]
def pt(p):return P[p] if isinstance(p,str) else mm(p)
def wire(net,*pts):
    pp=[pt(p) for p in pts]
    for a,b in zip(pp,pp[1:]):
        if a==b:continue
        assert a[0]==b[0] or a[1]==b[1],(net,a,b)
        W.append(dict(net=net,a=a,b=b))
def label(net,p):L.append(dict(net=net,p=pt(p)))
def bus(net,y,eps):
    ps=[pt(p) for p in eps];xx=[p[0]/1.27 for p in ps]
    wire(net,(min(xx),y),(max(xx),y))
    for e,p in zip(eps,ps):wire(net,e,(p[0]/1.27,y))
    label(net,(min(xx),y))
def stub(net,e,dx=0,dy=0):
    p=P[e];end=(p[0]/1.27+dx,p[1]/1.27+dy)
    wire(net,e,end);label(net,end)
def text(t,x,y,size=1.016,bold=False):
    G.append(expr(f'(text {q(t)} (at {x*1.27} {y*1.27} 0) (effects (font (size {size} {size}){" (bold yes)" if bold else ""}) (justify left)) (uuid {q(uid())}))'))
def excluded(w):
    a,b=w['a'],w['b']
    # Redesigned around library pin arrangements: power, PIC, motor IC, AUX IC.
    return (a[0]<146 and b[0]<146 and a[1]<109 and b[1]<109
        or 151<=a[0]<=311 and 151<=b[0]<=311 and a[1]<109 and b[1]<109
        or 317<=a[0]<=395 and 317<=b[0]<=395 and a[1]<=69 and b[1]<=69
        or 230<=a[0]<=331 and 230<=b[0]<=331 and 215<=a[1]<=257 and 215<=b[1]<=257)
for w in layout['wires']:
    if excluded(w):continue
    if w['net'] in ['Q8_DRIVE_A','Q8_DRIVE_B','H_RF_OUT_CAND','H_RF_VDD']:continue
    if w['net']=='GND' and (w['a']==[57,159] or w['b']==[57,159] or w['a']==[57,190] or w['b']==[57,190]):continue
    a,b=mm(w['a']),mm(w['b']); aa=oldpoints.get(a,a);bb=oldpoints.get(b,b)
    # Adapt short symbol leads; preserve authored route corridors.
    path=[aa]
    if aa[0]!=bb[0] and aa[1]!=bb[1]:
        if a[1]==b[1]:
            mx=round((aa[0]+bb[0])/2/1.27)*1.27;path.extend([(mx,aa[1]),(mx,bb[1])])
        else:
            my=round((aa[1]+bb[1])/2/1.27)*1.27;path.extend([(aa[0],my),(bb[0],my)])
    path.append(bb)
    for aa,bb in zip(path,path[1:]):
        if aa!=bb:W.append(dict(net=w['net'],a=xy(aa),b=xy(bb)))
for l in layout['labels']:
    if l['net'] in ['Q8_DRIVE_A','Q8_DRIVE_B','H_RF_OUT_CAND','H_RF_VDD']:continue
    w=dict(a=l['p'],b=l['p'])
    if not excluded(w):L.append(dict(net=l['net'],p=oldpoints.get(mm(l['p']),mm(l['p']))))
# Give the button-control label enough room before the horizontal resistor body.
for l in L:
    if l['net']=='H_BUTTON_MCU':
        x,y=l['p'];start=(rnd(x-3.81),y)
        W.append(dict(net=l['net'],a=start,b=l['p']));l['p']=start
wire('GND','C9.2',(49,159),(49,190),(53,190))

# Datasheet S-1200B45 symbol: input/enable left, output/NC right, ground below.
stub('BATTERY+','BATP.1',0,7)
stub('VSYS','L2.1',-7,0) # Post-Q1 feed; BATP is on the other side of Q1.
wire('H_LDO_IN','L2.2','U1.L1');wire('H_LDO_IN','C1.1',(44,42))
wire('H_LDO_IN','C1A.1',(38,49),(38,42));wire('H_LDO_IN','U1.L3',(52,48),(52,42))
wire('GND','U1.L2',(66,64));bus('GND',64,['C1.2','C1A.2','C2.2','C2A.2','GND.1'])
wire('VDD','U1.R1',(82,42),'VDD.1')
wire('VDD','C2.1',(90,42));wire('VDD','C2A.1',(106,42));label('VDD',(101,42))
wire('U1_ALT_PAD','U1.R2',(80,48),(80,81),(115,81),'C4.2')
wire('U1_ALT_PAD','R1.2',(48,87),(48,81),(80,81));wire('U1_ALT_PAD','C3.2',(72,87),(72,81));wire('U1_ALT_PAD','R2.2',(97,87),(97,81))
label('U1_ALT_PAD',(80,81))
stub('VDD','R1.1',0,5);stub('VDD','C3.1',0,5)
stub('GND','R2.1',0,5);stub('GND','C4.1',0,5)

# PIC: official SOIC symbol; both ground pins share the library endpoint.
bus('VDD',32,['U4.20','C32.1']);bus('GND',44,['C32.2','C26.2'])
# IMG_2436: RA0/C25 and RA2/C39 are signal nodes, not supply bypasses.
wire('PIC_RA0_FILTER','U4.2','C25.1')
wire('VREF','U4.4','C39.1');label('VREF','C39.1') # User V035-VREF
bus('GND',66,['C25.2','C39.2'])
wire('PIC_TP4_C41','TP4.1','C41.1');stub('GND','C41.2',4)
stub('PIC_RA1_RX_REF','U4.3',4)
stub('H_TUNE_2','U4.5',4)
stub('H_TUNE_3','U4.6',4)
stub('H_TUNE_4','U4.7',4)
stub('H_TUNE_5','U4.11',-12)
stub('H_RX_ENABLE_CTL','U4.12',-12) # User V053-V070; old VREF join rejected.
stub('RF_MONITOR_PAD','U4.13',-12)
stub('VREF','VREF.1',0,4)
stub('VREF','U4.21',4)
stub('MOTOR_INA','U4.15',-12)
stub('MOTOR_INB','U4.16',-12)
stub('H_TUNE_1','U4.17',-12)
stub('H_LED_CTL_B','U4.22',4)
stub('H_LED_CTL_A','U4.23',4)
stub('PIC_TP4_C41','U4.25',4)
wire('ICSP_CLK','U4.27',(228,76),(228,43),'J1.CLK');label('ICSP_CLK',(230,43))
wire('ICSP_DAT','U4.28',(231,78),(231,45),'J1.DAT');label('ICSP_DAT',(233,45))
stub('MCLR_VPP','U4.1',-12);stub('MCLR_VPP','J1.VPP',-12)
stub('VDD','J1.VDD',-8)
wire('GND','J1.GND',(263,51),(263,104));wire('GND','U4.8',(207,104),(263,104));label('GND',(207,104))
wire('OSC1','U4.9',(233,60),(233,85),(238,85),(238,89),'Y1.1');wire('OSC1','C30.1',(238,89))
wire('OSC2','U4.10',(235,58),(235,83),(254,83),(254,89),'Y1.2');wire('OSC2','C31.2',(254,89))
wire('GND','C30.2',(238,104));wire('GND','C31.1',(254,104));wire('PIC_RC3','U4.14','TP11.1')
stub('VSYS','R3.1',0,-4);wire('H_BAT_SENSE','R3.2',(280,75),'R4.1');wire('H_BAT_SENSE','C28.1',(296,75));label('H_BAT_SENSE',(284,75));stub('GND','C28.2',0,6)
stub('PIC_RB3_RETURN','U4.24',14);stub('PIC_RB3_RETURN','R4.2',0,6)
wire('PIC_RC7_TP17','U4.18','TP17.1');label('PIC_RC7_TP17','TP17.1')
stub('ICSP_CLK','D4.1',-4);stub('ICSP_CLK','R32.2',3)
stub('ICSP_DAT','D5.1',-4);stub('ICSP_DAT','R40.1',0,-5)
stub('GND','D4.2',0,4);stub('GND','D5.2',0,4)
wire('H_LED_CTL_A','TP1.1',(151,184),'R30.1')
wire('H_LED_CTL_B','TP2.1',(151,191),'R31.1')
label('GND',(199,187))
stub('RB5_OPT','U4.26',14);stub('RB5_OPT','TP10.1',0,4)
stub('RB5_OPT','R35.1',-3);stub('R35_Q9','R35.2',0,4)
stub('R35_Q9','Q9.L',-4)
stub('GND','Q9.R',4)
stub('GND','R32.1',3)

wire('VSYS','Q1.L',(359,94),(352,94));label('VSYS',(352,94));label('BATTERY+',(359,82)) # User post-Q1 supply; keep its label clear of R43 ground.
wire('BATTERY+','R43.2',(367,102),(379,102),(379,82),'TP14.1') # V015-TP14
# MX512H physical pin numbering, not a DRV8837 pin substitution.
wire('VSYS','C33.1',(339,33),(361,33),'U5.4');label('VSYS',(339,33))
wire('VDD','U5.1',(345,44),(345,43),(330,43),'C34.1');label('VDD',(330,43))
wire('GND','C33.2',(339,69));bus('GND',69,['C34.2','BATN.1'])
wire('GND','U5.6',(359,69));wire('GND','U5.7',(363,69));wire('GND',(359,69),(363,69))
wire('H_MOTOR_A','U5.8',(384,44),(384,49),'J5.A')
wire('H_MOTOR_B','U5.5',(381,52),(381,55),(386,55),(386,51),'J5.B');wire('H_MOTOR_B','TP15.1',(381,55))
stub('MOTOR_INA','U5.2',-10);stub('MOTOR_INB','U5.3',-10)
stub('VSYS','C27.1',0,-4);stub('GND','C27.2',0,4)

# S-812C33AMC candidate: C2N code and measured ground support pin assignment.
wire('VDD','R37.1',(235,233),(235,227));label('VDD',(235,227))
wire('H_AUX_IN','R37.2',(248,233),(248,240),'U6.R2')
wire('H_AUX_IN','C36.1',(237,238),(248,238));label('H_AUX_IN',(237,238))
wire('GND','U6.R3',(260,257));bus('GND',257,['C36.2','C37.2'])
stub('H_PIR_VDD','U6A.R1',-10) # V067-J3.1 confirmed; option remains DNP.
wire('H_PIR_VDD','U6.R1',(280,240),'C37.1')
wire('H_PIR_VDD',(280,240),(280,241))
wire('H_PIR_VDD',(280,241),(290,241),(290,232))
wire('H_PIR_VDD',(290,241),(290,256),'J3.1');label('H_PIR_VDD',(290,232))

# Q8: 3724A marking supports SIL3724A pinout; manufacturer and routing provisional.
wire('Q8_DRIVE_A','R9.2',(111,146),(111,182),'Q8.T3')
wire('Q8_DRIVE_B','R8.2',(106,171),(106,163),'Q8.T1')
wire('H_RF_OUT_CAND','Q8.B1',(130,174),'Q8.B3')
wire('H_RF_OUT_CAND',(130,174),'R5.1')
wire('GND','Q8.B2',(130,188),(134,188));label('GND',(134,188))
wire('H_RF_VDD','Q8.T2',(177,159),(177,132),'L1.2')
wire('H_RF_VDD','L1.2',(187,132),'C5.1')
label('H_RF_VDD',(181,132))
# C6.1 to output was refuted by 400 kohm E-F; leave its destination unresolved.
stub('H_ANT_A','ANT1.1',5);stub('H_ANT_B','ANT2.1',5)

# Preserve original frame geometry at half scale, using normal readable text sizes.
for g in layout['graphics']:
    e=sx.loads(g)
    if tag(e)!='polyline':continue
    for p in children(one(e,'pts'),'xy'):p[1:]=[rnd(v/2) for v in p[1:]]
    if all(p[1]>=337*1.27 for p in children(one(e,'pts'),'xy')):
        for p in children(one(e,'pts'),'xy'):
            if p[2]==313*1.27:p[2]=295*1.27
    G.append(e)
for n in layout['notes']:
    t=n['text']
    if t.startswith('Original pad IDs on U1.'):
        t='U1 datasheet symbol: S-1200B45 SOT-23-5. Pin 4 is internally open; option pads retained.'
    if 'Original photographed pad names remain' in t:
        t='Library pin numbers are mapped to photo pads in evidence/pin_crosswalk.json.'
    if t.startswith('v0.2'):t='v0.9.9 | KiCad 10.0.5 | 2026-10-08';n['y']=292
    if t.startswith('H14-H15:'):t='H14-H15: C2N supports S-812C33AMC 3.3V LDO. C/R3 ground supported by resistance.'
    if t.startswith('H09:'):t='H09: 3724A matches SIL3724A N/P MOSFET pair. Both units share one package.'
    if t.startswith('Q8 T2/B1/B2'):t='V113/V115: Q8 centre pin5 GND. V114 is U2 pin2 GND, not Q8 pin2.'
    if t.startswith('H07:'):t='H07: C14R inverter candidate. Q8 source rail inferred; C6 destination unresolved.'
    if t.startswith('No invented ties'):t='D4/D5 opposite vias join rear GND copper. D6 type and routes remain uncertain.'
    if t.startswith('H02:'):t='User: RA3/R14, RA4/R15, RA5/R16, RC0/R11, RC6/R13. RC2 -> TP3; RB0 -> VREF. RC1 -> R18 via V053-V070.'
    if t.startswith('Selected working hypothesis:'):t='v0.9: user-reviewed GND returns replace previous antenna rails on this capacitor bank.'
    if t.startswith('Ceff ='):t='Local three-capacitor junctions retained. Hidden links from these midpoints to antenna remain unknown.'
    if t.startswith('All-parallel'):t='Do not infer complete tuning topology from local connections. Transistor identity/orientation remains provisional.'
    if t.startswith('C27 role unresolved'):t='C27: motor-supply bypass; value unmeasured.'
    if t.startswith('Optional R1/R2/C3/C4'):t='Empty options: R1/C3 free ends join regulated VDD; R2/C4 free ends join GND.'
    if t.startswith('H04:'):t='User: PIC15/RC4 -> INA pin2; PIC16/RC5 -> INB pin3. Motor output polarity remains inferred.'
    if t.startswith('H05:'):t='Q1: R1A -> FMOS3401A PMOS candidate. Battery+ at D3; post-Q1 supply at S2; G1 via R44.'
    if t.startswith('29 original local'):t='28 original local photo fragments retained; Q1.L-R43.2 withdrawn by user.'
    if t.startswith('H03:'):t='R3/R4 sensing candidate; R4 returns to RB3. C28 value estimated.';n['y']=106
    text(t,n['x'],n['y'],1.27 if n['size']>=1 else max(.762,n['size']*1.27))
text('BATTERY+ -> Q1 -> VSYS / U5 pin4. Board VDD / TP103 = VDD -> U5 pin1.',320,77,.762)
text('VDD / TP103: regulated logic supply VDD; candidate 4.5V, not measured. V082 confirmed here.',13,76,.762)
text('V082 -> VDD / TP103. D3 terminal unresolved; existing H_RX_VDD branch remains inferred.',330,126,.762)
text('D2: 4P unidentified; old BAV99 clamp ties withdrawn.',350,201,.762)
text('User: V072 = TP6, not R22.2. V079/V080 = U3 pin5; separate from TP6 across C18.',288,211,.762)
text('U3 alternative: MCP6002-I/SN; same pin roles, electrical suitability to verify.',288,208,.762)
text('U5 alternative: DRV8212PDSGR. Different package/pins; redesign required.',320,81,.762)
text('U6: 3.3V is the candidate rating, not a voltage measurement. NC4/5 board ties unresolved.',234,284,.762)
text('C6: F-P 10 ohm, F-G 300 kohm suggests a supply-related node; exact path unresolved.',90,202,.762)
text('User: V063-V064 confirms R37/R39 feed on regulated VDD.',234,287,.762)
text('Q7: 11.2 kohm V064-V070 fits R18+R19. Supply-switch topology inferred; RC1 drives R18 via V053-V070.',229,126,.762)

def on(p,w):
    a,b=w['a'],w['b']
    return ((a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or
            (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0])))
member={};clashes=[]
for ep,p in P.items():
    ns={w['net'] for w in W if on(p,w)}
    if len(ns)>1:clashes.append([ep,p,sorted(ns)])
    if ns:member[ep]=sorted(ns)[0]
for w in W:
    for p in [w['a'],w['b']]:
        ns={v['net'] for v in W if on(p,v)}
        if len(ns)>1:clashes.append(['endpoint',p,sorted(ns)])
expected={e:n['net'] for n in model['nets'] for e in n['endpoints']}
delta={e:[expected.get(e),member.get(e)] for e in set(expected)|set(member) if expected.get(e)!=member.get(e)}
if clashes or delta:
    (STAGE/'routing_issues.json').write_text(json.dumps(dict(clashes=clashes,changed=delta),indent=2))
    print(json.dumps(dict(clashes=clashes,changed=delta),indent=2));sys.exit(1)

# Split only at same-net joins, de-duplicate, and label disconnected pieces.
pts=defaultdict(set)
for w in W:pts[w['net']].update([w['a'],w['b']])
for e,n in member.items():pts[n].add(P[e])
L=[l for l in L if any(on(l['p'],w) and w['net']==l['net'] for w in W)]
for l in L:pts[l['net']].add(l['p'])
segments=set()
for w in W:
    ordered=sorted(p for p in pts[w['net']] if on(p,w))
    for a,b in zip(ordered,ordered[1:]):segments.add((w['net'],a,b))
adj=defaultdict(lambda:defaultdict(set))
for net,a,b in segments:adj[net][a].add(b);adj[net][b].add(a)
for net,edges in adj.items():
    groups=[];seen=set()
    for start in sorted(edges):
        if start in seen:continue
        todo=[start];group=set()
        while todo:
            p=todo.pop()
            if p in group:continue
            group.add(p);todo.extend(edges[p]-group)
        seen|=group;groups.append(group)
    if len(groups)>1:
        for group in groups:
            if not any(l['net']==net and l['p'] in group for l in L):L.append(dict(net=net,p=sorted(group)[0]))
for net,a,b in sorted(segments):
    G.append(expr(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid {q(uid())}))'))
for net,edges in adj.items():
    for p,neighbors in edges.items():
        if len(neighbors)>=3:G.append(expr(f'(junction (at {p[0]} {p[1]}) (diameter 0) (color 0 0 0 0) (uuid {q(uid())}))'))
for l in L:
    x,y=l['p'];G.append(expr(f'(label {q(l["net"])} (at {x} {y} 0) (effects (font (size .762 .762)) (justify left bottom)) (uuid {q(uid())}))'))
tree.extend(G)
tree.append(expr('(title_block (title "PetSafe 100-1339 R03 A | single-sheet reconstruction") (date "2026-10-08") (rev "0.9.9") (company "KiCad 10 libraries + four datasheet symbols | MCP authoring") (comment 1 "Raw battery separated from post-Q1 supply; R1A PMOS candidate. GPIO routes retained."))'))
# Canonical pretty printer supplied by the installed MCP server.
sys.path.insert(0,str(Path.home()/'Documents/VS.Code.Projects/KiCAD-MCP-Server/python'))
from utils.sexpr_format import prettify
out=R/'schematic/PetSafe_1001339.kicad_sch'
out.write_text(prettify(sx.dumps(tree)),encoding='utf-8',newline='\n')
model.update(revision='v0.9.9',coordinate_units='mm',native_pin_crosswalk=layout['crosswalk'],pin_positions={e:list(p) for e,p in P.items()},
             geometric_wires=[dict(net=n,a=a,b=b) for n,a,b in segments],library_policy='KiCad 10 stock symbols plus four explicitly authorized MCP-authored datasheet symbols for U1/U5/U6/Q8')
for c in model['components']:
    entry=next(x for x in layout['catalog'] if x['original_ref']==c['ref'])
    c['library_symbol']=entry['symbol'];c['footprint']=entry['footprint']
(R/'evidence/reconstruction.json').write_text(json.dumps(model,indent=2),encoding='utf-8',newline='\n')
print(f'Routed {len(segments)} segments. Model has {len(expected)} connected pads, {len(P)-len(expected)} unresolved pads. {len(libs)} library definitions including four MCP-authored datasheet symbols.')
