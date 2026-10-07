"""Generate a functional, single-sheet KiCad working reconstruction.
Coordinate unit = 2.54 mm. All circuit routes are explicitly authored.
"""
from pathlib import Path
from collections import defaultdict
import json, uuid, math, csv
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'schematic'
BASE=json.loads((ROOT/'reference/v01/evidence/reconstruction.json').read_text())
C={c['ref']:dict(c) for c in BASE['components']}
NS=uuid.UUID('c5ee9f10-9018-4456-81b4-a963cfead728')
def uid(s):return str(uuid.uuid5(NS,s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def mm(x):return f'{x*2.54:.4f}'.rstrip('0').rstrip('.') if x else '0'
def eff(size=.5,just='',hide=False):return f'(effects (font (size {mm(size)} {mm(size)})){" (justify "+just+")" if just else ""}{" hide" if hide else ""})'
RID=uid('sheet');PROJECT='PetSafe_1001339'
GRAPH=[];LIB={};INST=[];PINS={};LOC={};WIRES=[];LABELS=[];NOTES=[];USED=set();NETINFO={}
REF_MAP={'C1A':'C101','C2A':'C102','U6A':'U106'}
for i,r in enumerate(['GND','GND_RF','VDD','VREF','ANT1','ANT2','BATP','BATN'],101):REF_MAP[r]=f'TP{i}'
def text(t,x,y,size=.6):
    NOTES.append(dict(text=t,x=x,y=y,size=size))
    GRAPH.append(f'(text {q(t)} (at {mm(x)} {mm(y)} 0) {eff(size,"left")} (uuid {uid("text:"+str((t,x,y)))}))')
def block(title,x,y,w,h,subtitle):
    for a,b in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:
        GRAPH.append(f'(polyline (pts (xy {mm(a[0])} {mm(a[1])}) (xy {mm(b[0])} {mm(b[1])})) (stroke (width .254) (type default)) (fill (type none)) (uuid {uid(str((title,a,b)))}))')
    text(title,x+3,y+4,1);text(subtitle,x+3,y+8,.52)
def line(pts,fill='none'):
    return '(polyline (pts '+' '.join(f'(xy {mm(x)} {mm(-y)})' for x,y in pts)+f') (stroke (width .254) (type default)) (fill (type {fill})))'
def rect(x1,y1,x2,y2):return f'(rectangle (start {mm(x1)} {mm(-y1)}) (end {mm(x2)} {mm(-y2)} ) (stroke (width .254) (type default)) (fill (type background)))'
def circle(x,y,r,fill='none'):return f'(circle (center {mm(x)} {mm(-y)}) (radius {mm(r)}) (stroke (width .254) (type default)) (fill (type {fill})))'
def pin(p,name,x,y,side,typ='passive',length=2):return dict(p=str(p),name=name,x=x,y=y,side=side,typ=typ,length=length)
def part(ref,x,y,kind=None,value=None,orientation='h',unit=1,pins=None,body=None,size=(8,6),hyp='',reverse=False):
    c=C[ref];USED.add(ref);key=ref if unit==1 else f'{ref}:{unit}'
    if value is not None:c['proposed_value']=value
    if hyp:c['hypothesis']=hyp
    val=c.get('proposed_value',c['value']);val='?' if val=='UNKNOWN' else val
    if ref in REF_MAP:val=f'{ref} / {val}'
    k=kind or c['kind'];g=[]
    if pins is None:
        if k in ['R','C','Y','L','D2']:
            v=orientation=='v'
            pins=[pin('1','~',0,-3,270,length=1.6),pin('2','~',0,3,90,length=1.6)] if v else [pin('1','~',-3,0,0,length=1.6),pin('2','~',3,0,180,length=1.6)]
            if k=='R':paths=[[(-1.4,-.5),(1.4,-.5),(1.4,.5),(-1.4,.5),(-1.4,-.5)]]
            elif k=='C':paths=[[(-1.4,0),(-.4,0)],[(-.4,-1),(-.4,1)],[(.4,-1),(.4,1)],[(.4,0),(1.4,0)]]
            elif k=='Y':paths=[[(-1,-1),(1,-1),(1,1),(-1,1),(-1,-1)],[(-1.4,-1.5),(-1.4,1.5)],[(1.4,-1.5),(1.4,1.5)]]
            elif k=='L':paths=[[(cen+.35*math.cos(math.pi-j*math.pi/10),-.7*math.sin(math.pi-j*math.pi/10)) for j in range(11)] for cen in [-1.05,-.35,.35,1.05]]
            else:paths=[[(-1.4,-.7),(1.4,-.7),(1.4,.7),(-1.4,.7),(-1.4,-.7)]]
            g=[line([(-b,a) for a,b in path] if v else path) for path in paths];size=(2,2)
        elif k=='TP':pins=[pin('1','~',-2,0,0,length=1.3)];g=[circle(0,0,.7)];size=(1,1)
        elif k in ['NPN','PNP']:
            m=c.get('bce',{'B':'R','E':'L','C':'S'})
            pins=[pin(m['B'],'B?',-4,0,0),pin(m['C'],'C?',2,-4,270),pin(m['E'],'E?',2,4,90)]
            g=[line([(-2,-1.5),(-2,1.5)]),line([(-2,-.6),(2,-2)]),line([(-2,.6),(2,2)])]
            arrow=[(.1,1.35),(1.8,1.9),(.8,.65),(.1,1.35)] if k=='NPN' else [(-1.3,.85),(.4,.9),(-.3,2),(-1.3,.85)]
            g.append(line(arrow,'outline'));size=(4,4)
        elif k=='DUALD':
            pins=[pin('L','A1?',-6,0,0),pin('R','K2?',6,0,180),pin('S','K1/A2?',0,4,90)]
            g=[line([(-4,0),(-3,0),(-3,-1),(-1,0),(-3,1),(-3,0)]),line([(-1,-1),(-1,1)]),line([(-1,0),(1,0),(1,-1),(3,0),(1,1),(1,0)]),line([(3,-1),(3,1)]),line([(3,0),(4,0)]),line([(0,0),(0,2)])];size=(6,3)
        elif k=='SW':
            pins=[pin('TL','TL',-5,-2,0),pin('BL','BL',-5,2,0),pin('TR','TR',5,-2,180),pin('BR','BR',5,2,180)]
            g=[line([(-3,-2),(-3,2)]),line([(3,-2),(3,2)]),line([(-3,0),(2,-1)]),line([(0,-1),(0,-2)])];size=(5,3)
        else:
            pp=c['pins'];half=math.ceil(len(pp)/2)
            pins=[pin(p,p,-size[0]-2,(i-(half-1)/2)*2,0) for i,p in enumerate(pp[:half])]
            pins += [pin(p,p,size[0]+2,(i-(len(pp)-half-1)/2)*2,180) for i,p in enumerate(pp[half:])]
            g=[rect(-size[0],-size[1],size[0],size[1])]
    else:g=body or [rect(-size[0],-size[1],size[0],size[1])]
    if reverse:
        assert len(pins)==2
        pins[0]['p'],pins[1]['p']=pins[1]['p'],pins[0]['p']
    lid='PetSafe_Working:RE_'+ref
    LIB.setdefault(ref,dict(lid=lid,units={}));assert unit not in LIB[ref]['units']
    LIB[ref]['units'][unit]=(g,pins)
    if k in ['R','C','L','Y','D2'] and orientation=='v':rx,ry,vx,vy,just=x+2,y-.7,x+2,y+.9,'left'
    else:rx,ry,vx,vy,just=x,y-size[1]-2.5,x,y-size[1]-1,''
    if ref in ['U2','U3'] and unit==3:rx,ry,vx,vy,just=x-9,y-1,x-9,y+.5,'right'
    if ref=='U4':rx,ry,vx,vy=x+12,y-28,x+12,y-26.5
    if ref=='U5':rx,ry,vx,vy=x+12,y-14,x+12,y-12.5
    if k in ['NPN','PNP']:rx=vx=x-2
    if ref=='R43':ry,vy=y+2.5,y+4
    if ref=='R48':rx=vx=x+4
    if ref=='GND_RF':rx=vx=x-6
    INST.append(dict(ref=ref,actual=REF_MAP.get(ref,ref),x=x,y=y,unit=unit,lid=lid,value=val,rx=rx,ry=ry,vx=vx,vy=vy,just=just,pins=pins,kind=k))
    LOC[key]=dict(x=x,y=y,kind=k,unit=unit,size=size)
    for p in pins:
        ep=ref+'.'+p['p'];assert ep not in PINS,ep;PINS[ep]=(x+p['x'],y+p['y'])
def pos(p):return PINS[p] if isinstance(p,str) else tuple(p)
def wire(name,*points):
    pp=[pos(p) for p in points]
    for a,b in zip(pp,pp[1:]):
        if a==b:continue
        assert a[0]==b[0] or a[1]==b[1],('NONORTHOGONAL',name,a,b)
        WIRES.append(dict(net=name,a=a,b=b))
def label(name,p):LABELS.append(dict(net=name,p=pos(p)))
def stub(name,ep,dx=0,dy=0):
    if dx<0 and dy==0:dx=-max(abs(dx),math.ceil((len(name)*.32+1.2)*2)/2)
    a=pos(ep);b=(a[0]+dx,a[1]+dy);wire(name,a,b);label(name,b)
def bus(name,y,eps,x1=None,x2=None):
    pp=[pos(p) for p in eps];xs=[p[0] for p in pp]
    x1=min(xs) if x1 is None else x1;x2=max(xs) if x2 is None else x2
    wire(name,(x1,y),(x2,y));label(name,(x1,y))
    for ep,(x,_) in zip(eps,pp):wire(name,ep,(x,y))

def power():
    block('01  POWER / INPUT FILTER',10,20,135,88,'H01: likely S-1200B45 LDO. Nominal 4.5 V is a candidate, not a measured rail.')
    part('BATP',18,42,value='BATTERY +');part('L2',33,42,value='bead / L ?')
    part('C1',44,52,orientation='v',value='1u?');part('C1A',33,52,orientation='v')
    pp=[pin('L1','VIN (1)?',-9,-4,0,'power_in'),pin('L2','GND (2)?',0,9,90,'power_in',length=3),pin('L3','EN (3)?',-9,3,0,'input'),pin('R1','OUT (5)?',9,-4,180,'power_out'),pin('R2','NC/ALT (4)?',9,3,180)]
    part('U1',66,46,value='S-1200B45?',pins=pp,size=(7,6),hyp='H01: ABLIC S1200 Rev6 page23 maps PPE to S-1200B45-M5T1x and fourth character to lot. Strong identity candidate; board-wide connections remain inferred.')
    part('C2',90,52,orientation='v',value='4.7u?');part('C2A',106,52,orientation='v');part('VDD',117,42,value='VDD pad');part('GND',119,64,value='GND pad')
    wire('H_VBAT','BATP.1','L2.1');label('H_VBAT',(23,42))
    wire('H_LDO_IN','L2.2','U1.L1');wire('H_LDO_IN','C1.1',(44,42));wire('H_LDO_IN','C1A.1',(38,49),(38,42));wire('H_LDO_IN','U1.L3',(52,49),(52,42))
    wire('H_VDD','U1.R1','VDD.1');wire('H_VDD','C2.1',(90,42));wire('H_VDD','C2A.1',(106,42));label('H_VDD',(101,42))
    bus('H_GND',64,['C1.2','C1A.2','U1.L2','C2.2','C2A.2','GND.1'])
    text('Original pad IDs on U1. Candidate datasheet pin numbers in parentheses.',17,72,.55)
    part('R1',42,87);part('C3',65,87);part('R2',90,87);part('C4',112,87)
    wire('U1_ALT_PAD','U1.R2',(80,49),(80,81),(115,81),'C4.2')
    wire('U1_ALT_PAD','R1.2',(48,87),(48,81),(80,81));wire('U1_ALT_PAD','C3.2',(72,87),(72,81));wire('U1_ALT_PAD','R2.2',(97,87),(97,81));label('U1_ALT_PAD',(80,81))
    text('Optional R1/R2/C3/C4 network: empty footprints; free ends unresolved.',17,99,.55)

def controller():
    block('02  PIC CONTROLLER / CLOCK / ICSP',151,20,160,88,'H02: programming and decoupling inferred. Unassigned GPIOs stay open; PPS prevents a unique functional pin guess.')
    names=['MCLR/VPP','RA0','RA1','RA2','RA3','RA4','RA5','VSS','OSC1/RA7','OSC2/RA6','RC0','RC1','RC2','RC3','RC4','RC5','RC6','RC7','VSS','VDD','RB0','RB1','RB2','RB3','RB4','RB5','ICSPCLK/RB6','ICSPDAT/RB7']
    pp=[pin('20','VDD',0,-25,270,'power_in'),pin('8','VSS',-3,25,90,'power_in'),pin('19','VSS',3,25,90,'power_in')]
    for pn,y in [(1,-17),(2,-11),(3,-8),(4,-5),(5,-2),(6,1),(7,4),(9,13),(10,17)]:pp.append(pin(pn,names[pn-1],-13,y,0,'input' if pn in(1,9) else 'bidirectional'))
    for i,pn in enumerate(list(range(11,19))+list(range(21,29))):pp.append(pin(pn,names[pn-1],13,-20+i*2.5,180,'bidirectional'))
    part('U4',207,62,pins=pp,size=(11,23))
    part('J1',271,47,value='ICSP',pins=[pin(p,p,-5,(i-2)*3,0) for i,p in enumerate(['CLK','DAT','VPP','VDD','GND'])],size=(3,8))
    part('C25',166,38,orientation='v',value='100n?');part('C26',177,38,orientation='v',value='100n?');part('C39',188,38,orientation='v',value='100n?')
    bus('H_VDD',32,['U4.20','C25.1','C26.1','C39.1']);bus('H_GND',44,['C25.2','C26.2','C39.2'])
    wire('ICSP_CLK','U4.27',(228,77),(228,47),(253,47),(253,41),'J1.CLK');label('ICSP_CLK',(230,47))
    wire('ICSP_DAT','U4.28',(231,79.5),(231,50),(257,50),(257,44),'J1.DAT');label('ICSP_DAT',(233,50))
    stub('MCLR_VPP','U4.1',-7,0);stub('MCLR_VPP','J1.VPP',-5,0);stub('H_VDD','J1.VDD',-3,0)
    wire('H_GND','J1.GND',(263,53),(263,91));bus('H_GND',91,['U4.8','U4.19'],204,263)
    part('Y1',172,77,value='20 MHz');part('C30',164,88,orientation='v',value='18p?');part('C31',180,88,orientation='v',value='18p?')
    wire('OSC1','U4.9',(188,75),(188,71),(164,71),(164,77),'Y1.1');wire('OSC1','C30.1',(164,77));label('OSC1',(177,71))
    wire('OSC2','U4.10',(188,79),(188,81),(180,81),(180,77),'Y1.2');wire('OSC2','C31.2',(180,96),(190,96),(190,81),(180,81))
    wire('H_GND','C30.2',(164,98),(175,98),(175,85),'C31.1');label('H_GND',(164,98))
    part('TP11',225,49.5);wire('PIC_RC3','U4.14','TP11.1')
    part('R3',280,68,orientation='v');part('R4',280,83,orientation='v');part('C28',296,83,orientation='v',value='100n?');part('TP17',301,75)
    stub('H_VBAT','R3.1',0,-4);wire('H_BAT_SENSE','R3.2',(280,75),'R4.1');wire('H_BAT_SENSE',(280,75),'TP17.1');wire('H_BAT_SENSE','C28.1',(296,75));label('H_BAT_SENSE',(284,75));bus('H_GND',94,['R4.2','C28.2'])
    text('H03: R3/R4 divider candidate: 1/2 VBAT. Capacitor values estimated.',239,101,.5)

def motor_ui():
    block('03  MOTOR / BUTTON / BATTERY INTERFACE',317,20,139,88,'H04: MX512H typical supply/output topology. Motor A/B and MCU control assignments remain hypotheses.')
    pp=[pin('1','VCC logic',-10,-5,0,'power_in'),pin('2','INA',-10,0,0,'input'),pin('3','INB',-10,5,0,'input'),pin('4','VDD motor',0,-12,270,'power_in'),pin('5','OUTB',10,5,180,'output'),pin('8','OUTA',10,-5,180,'output'),pin('6','GND',-2,12,90,'power_in'),pin('7','GND',2,12,90,'power_in')]
    part('U5',361,48,pins=pp,size=(8,10));part('C33',339,39,orientation='v',value='1u?');part('C34',330,54,orientation='v',value='100n?')
    part('J5',393,49,value='MOTOR',pins=[pin('A','A',-5,-6,0),pin('B','B',-5,4,0)],size=(3,7));part('TP15',383,61);part('BATN',381,69,value='BATTERY -')
    bus('H_VBAT',33,['U5.4','C33.1']);wire('H_VDD','U5.1',(330,43),'C34.1');label('H_VDD',(330,43));wire('H_GND','C33.2',(339,69));bus('H_GND',69,['C34.2','U5.6','U5.7','BATN.1'])
    wire('H_MOTOR_A','U5.8','J5.A');wire('H_MOTOR_B','U5.5','J5.B');wire('H_MOTOR_B','TP15.1',(381,53))
    stub('H_MOTOR_INA','U5.2',-8,0);stub('H_MOTOR_INB','U5.3',-8,0)
    part('S1',423,48);part('C35',440,59,orientation='v',value='100n?');part('R40',440,40,orientation='v');part('R41',410,40,value='mark 33...?');part('C27',403,63,orientation='v')
    stub('H_VDD','R40.1',0,-3);wire('H_BUTTON','R40.2',(440,46),'C35.1');wire('H_BUTTON',(440,46),'S1.TR');wire('H_BUTTON','S1.BR',(432,50),(432,46))
    wire('H_BUTTON','R41.2',(414,40),(414,31),(448,31),(448,46),(440,46));label('H_BUTTON',(440,46))
    wire('H_GND','S1.TL',(416,46),(416,50),'S1.BL');wire('H_GND',(416,50),(416,69));wire('H_GND','C35.2',(440,69),(416,69));wire('H_GND',(379,69),(416,69));stub('H_BUTTON_MCU','R41.1',-3,0)
    text('C27 role unresolved',403,75,.5)
    part('Q1',357,88,'NPN',value='MMBT3904?',hyp='H05: R1A mark suggests MMBT3904; B=R, E=L, C=S inferred from SOT23 orientation.')
    part('R44',340,88,value='15k?');part('R43',364,98);part('TP14',385,82)
    wire('Q1_BASE','R44.2','Q1.R');wire('Q1_EMITTER','Q1.L',(359,94),(370,94),(370,98),'R43.2');wire('H_BAT_DETECT','Q1.S',(359,82),'TP14.1');stub('H_Q1_BIAS','R44.1',-3,0);stub('H_GND','R43.1',-2,0)
    text('H05: NPN interface candidate; bias destination unresolved.',397,87,.5)
    text('H06: S1 pairs and RC debounce inferred.',397,94,.5)

def rf():
    block('04  ANTENNA EXCITATION / LOGIC / INDICATOR',10,114,210,95,'H07: U2 matches SN74LVC2G14 (C14R, 6 pins). Q8 probably contains two switching devices; exact type unresolved.')
    tri=[line([(-4,-3),(-4,3),(3,0),(-4,-3)]),circle(3.6,0,.6),line([(-2,-1),(-1,-1),(-1,1),(0,1),(0,-1),(1,-1)])]
    part('U2',69,146,value='74LVC2G14?',unit=1,pins=[pin('T3','~',-6,0,0,'input'),pin('B3','~',6,0,180,'output')],body=tri,size=(5,4),hyp='H07: exact TI C14R marking and 6-pin DBV package match. Photo top row left to right = 3,2,1; bottom = 4,5,6.')
    part('U2',69,171,unit=2,pins=[pin('T1','~',-6,0,0,'input'),pin('B1','~',6,0,180,'output')],body=tri,size=(5,4))
    part('U2',133,141,unit=3,pins=[pin('B2','VCC',0,-5,270,'power_in'),pin('T2','GND',0,5,90,'power_in')],body=[rect(-5,-3,5,3)],size=(5,3))
    part('C7',150,141,orientation='v',value='100n?');part('C8',53,181,orientation='v');part('C9',53,156,orientation='v')
    part('R8',91,171);part('R9',91,146);part('R6',30,175,orientation='v');part('R7',30,140,orientation='v');part('D1',39,158,'DUALD',value='BAV99?',hyp='H08: A7 mark + SOT23 fits BAV99 series dual diode. Photo pad mapping is provisional.')
    pp=[pin('T3','drive A?',-7,-5,0),pin('T1','drive B?',-7,2,0),pin('T2','T2',7,-5,180),pin('B1','B1',-3,9,90),pin('B2','B2',1,9,90),pin('B3','B3',7,5,180)]
    part('Q8',118,169,value='dual switch? / 372A',pins=pp,size=(5,7),hyp='H09: paired 220-ohm inputs from U2 suggest complementary RF switching device; exact type and supply-pad assignment unknown.')
    wire('U2_DRIVE_A','U2.B3','R9.1');wire('Q8_DRIVE_A','R9.2',(102,146),(102,164),'Q8.T3')
    wire('U2_DRIVE_B','U2.B1','R8.1');wire('Q8_DRIVE_B','R8.2','Q8.T1')
    wire('H_RF_IN_A','U2.T3',(53,146),'C9.1');wire('H_RF_IN_A',(53,146),(39,146),(30,146),'R7.2');wire('H_RF_IN_A','D1.S',(39,165),(46,165),(46,146))
    wire('H_RF_IN_B','U2.T1',(53,171),'C8.1');wire('H_RF_IN_B',(53,171),(30,171),'R6.1');wire('H_RF_IN_B','D1.L',(24,158),(24,171),(30,171))
    stub('H_RF_CONTROL','R7.1',-6,0);stub('H_RF_CONTROL','R6.2',-6,0);stub('H_D1_FREE','D1.R',3,0)
    # Separate capacitor returns are joined below the two gates.
    wire('H_GND','C9.2',(57,159),(57,190));wire('H_GND','C8.2',(53,190),(57,190));label('H_GND',(53,190))
    bus('H_VDD',131,['U2.B2','C7.1']);bus('H_GND',152,['U2.T2','C7.2'])
    part('L1',174,132,value='bead / L ?');part('C5',187,143,orientation='v',value='electrolytic ?');part('C6',204,143,orientation='v');part('GND_RF',204,156,value='GND pad');part('TP2',200,132)
    stub('H_VBAT','L1.1',-6,0);wire('H_RF_VDD','L1.2',(204,132));wire('H_RF_VDD','C5.1',(187,132));wire('H_RF_VDD','C6.1',(204,132));label('H_RF_VDD',(183,132));bus('H_GND',156,['C5.2','C6.2','GND_RF.1'])
    part('R5',157,174);wire('H_RF_OUT_CAND','Q8.B3','R5.1');stub('H_ANT_A','R5.2',6,0)
    text('H09: B3 = RF output is low-confidence.',96,193,.5);text('Q8 T2/B1/B2 power assignments open.',96,198,.5)
    part('R10',27,198);part('TP3',43,198);stub('H_RF_MONITOR','R10.2',0,4);wire('RF_MONITOR_PAD','R10.1',(19,198),(19,204),(41,204),'TP3.1')
    part('LED1',182,187,value='2-colour LED?',size=(5,5));part('R30',161,184);part('R31',161,191);part('TP1',211,187)
    wire('H_LED_A','R30.2',(174,184),(174,186),'LED1.TL')
    wire('H_LED_B','R31.2',(172,191),(172,188),'LED1.TR')
    stub('H_LED_CTL_A','R30.1',-5,0);stub('H_LED_CTL_B','R31.1',-5,0)
    wire('H_LED_COMMON','LED1.BL',(199,186),(199,187),'TP1.1');wire('H_LED_COMMON','LED1.BR',(199,188),(199,187));label('H_LED_COMMON',(200,187))

def receiver():
    block('05  RF RECEIVE / GAIN / ENVELOPE',226,114,230,95,'H10-H12: working topology around photographed 120k feedback resistors. Filters, bias, and interstage routes inferred.')
    tri=[line([(-5,-5),(-5,5),(5,0),(-5,-5)])]
    part('U3',300,158,value='SGM8542XS',unit=1,pins=[pin('3','+',-7,-2,0,'input'),pin('2','-',-7,2,0,'input'),pin('1','OUT',7,0,180,'output')],body=tri,size=(5,5))
    part('U3',382,158,unit=2,pins=[pin('5','+',-7,-2,0,'input'),pin('6','-',-7,2,0,'input'),pin('7','OUT',7,0,180,'output')],body=tri,size=(5,5))
    part('U3',437,146,unit=3,pins=[pin('8','VS+',0,-5,270,'power_in'),pin('4','VS-',0,5,90,'power_in')],body=[rect(-5,-3,5,3)],size=(5,3))
    part('C24',449,146,orientation='v',value='100n?');bus('H_RX_VDD',136,['U3.8','C24.1']);bus('H_GND',157,['U3.4','C24.2'])
    part('R26',300,142,reverse=True);part('C22',300,133,reverse=True);part('R48',281,176,orientation='v');part('R27',324,158,reverse=True);part('TP6',337,158)
    wire('RX_A_FB','U3.2',(286,160),(286,142),'R26.2');wire('RX_A_FB',(286,142),(286,133),'C22.2');wire('RX_A_FB','R48.1',(281,160),(286,160))
    wire('RX_A_OUT','U3.1','R27.2');wire('RX_A_OUT',(314,158),(314,142),'R26.1');wire('RX_A_OUT','C22.1',(314,133),(314,142))
    wire('RX_A_FILTER','R27.1','TP6.1');wire('H_RX_BIAS','R48.2',(279,179),(279,183));label('H_RX_BIAS',(279,183))
    part('R24',382,142,reverse=True);part('C21',382,133,reverse=True);part('R23',363,176,orientation='v');part('C18',363,156,reverse=True)
    wire('RX_B_FB','U3.6',(370,160),(370,142),'R24.2');wire('RX_B_FB',(370,142),(370,133),'C21.2');wire('RX_B_FB','R23.1',(363,160),(370,160))
    wire('RX_B_OUT','U3.7',(396,158),(396,142),'R24.1');wire('RX_B_OUT','C21.1',(396,133),(396,142))
    wire('RX_B_PLUS','U3.5','C18.1');wire('RX_A_FILTER','C18.2',(344,156),(344,158),'TP6.1');stub('H_RX_BIAS','R23.2',0,4)
    part('C23',403,158);part('R25',415,170,orientation='v');part('C40',427,170,orientation='v');part('R42',403,187)
    part('D3',438,184,'DUALD',value='clamp?');part('D2',438,198,'DUALD',value='clamp?');part('R29',357,145,orientation='v',value='15k?');part('R28',273,174,orientation='v',value='1M');part('C19',367,197);part('C20',351,190,orientation='v');part('TP7',337,184)
    wire('RX_B_OUT',(396,158),'C23.1');wire('H_RX_DETECT','C23.2',(415,158),'R25.1');wire('H_RX_DETECT',(415,158),(427,158),'C40.1');bus('H_GND',179,['R25.2','C40.2'])
    wire('H_RX_RF_SENSE','D3.S',(438,191),(424,191),(424,187),'R42.2');wire('H_RX_RF_SENSE','C19.2',(420,197),(420,187),(424,187))
    stub('H_RX_BIAS','R29.1',0,-4);wire('RX_B_PLUS','R29.2',(357,151),(373,151),(373,156),'U3.5')
    stub('H_ANT_B','R42.1',-4,0);stub('H_GND','D3.L',-3,0);stub('H_RX_VDD','D3.R',3,0);stub('H_GND','D2.L',-3,0);stub('H_RX_VDD','D2.R',3,0)
    wire('H_RX_DETECT','D2.S',(438,205),(452,205),(452,163),(427,163),(427,158));wire('H_RX_DETECT','TP7.1',(330,184),(330,205),(438,205));label('H_RX_DETECT',(391,205))
    wire('RX_A_PLUS','C19.1',(351,197),'C20.2');wire('RX_A_PLUS',(351,197),(346,197),(346,186),(284,186),(284,156),'U3.3');stub('H_GND','C20.1',-4,0)
    stub('H_RX_BIAS','R28.1',0,-4);wire('RX_A_PLUS','R28.2',(273,181),(278,181),(278,156),(284,156))
    C['Q7']['bce']={'B':'L','E':'R','C':'S'}
    part('Q7',247,144,'PNP',value='BC857C?',hyp='H11: 3GW fits BC857C. Physical B=L E=R C=S orientation and switched supply role inferred.')
    part('R19',237,157,orientation='v');part('R18',257,134);part('R20',268,144);part('C17',268,158,orientation='v',value='100n?');part('TP5',282,144)
    wire('RX_SUPPLY_SERIES','Q7.S',(249,137),(264,137),(264,144),'R20.1');wire('H_RX_VDD','R20.2','TP5.1');wire('H_RX_VDD','C17.1',(275,155),(275,144));label('H_RX_VDD',(275,144));stub('H_GND','C17.2',0,4)
    wire('H_RX_ENABLE','R19.1',(237,144),'Q7.L');stub('H_RX_ENABLE_CTL','R19.2',0,4)
    wire('H_RX_SUPPLY_FEED','Q7.R',(249,151),(260,151),'R18.2');stub('H_VDD','R18.1',-4,0)
    part('R21',242,181,orientation='v');part('R22',257,181,orientation='v')
    stub('H_RX_VDD','R21.1',0,-5);wire('H_RX_BIAS','R21.2',(242,188),(257,188),'R22.2');label('H_RX_BIAS',(247,188));stub('H_GND','R22.1',0,-4)
    part('C42',289,196);part('R47',309,196);part('R46',325,196)
    text('C42 / R47 / R46: DNP options, exact pads unresolved.',238,204,.5)

def tuning():
    block('06  SWITCHED ANTENNA CAPACITANCE',10,215,215,98,'H13: 2H devices are probably PNP BJTs (MMBTA55 family; PBSS5140T is an alternative). Capacitor values unknown.')
    part('ANT2',19,235,value='ANTENNA B');part('ANT1',19,287,value='ANTENNA A');part('TP4',217,287)
    wire('H_ANT_B','ANT2.1',(216,235));label('H_ANT_B',(25,235));wire('H_ANT_A','ANT1.1',(215,287));label('H_ANT_A',(25,287))
    for i,(qr,rr,ct,cf,cr) in enumerate([('Q3','R13','C10','C11','C12'),('Q4','R14','C13','C14','C15'),('Q5','R15','C16','C29','C38'),('Q6','R16','C43','C44','C45'),('Q11','R11','C46','C47','C48')]):
        x=40+i*42
        part(qr,x,274,'PNP',value='MMBTA55?',hyp='H13: 2H marking suggests PNP MMBTA55/FMMTA55 family; PBSS5140T alternative. B=R E=L C=S assumed.')
        part(rr,x-12,274);part(ct,x+2,262,orientation='v',reverse=True);part(cf,x-4,247,orientation='v');part(cr,x+8,247,orientation='v',value='? (rear)')
        wire(f'TUNE_{i+1}_BASE',rr+'.2',qr+'.R');stub(f'H_TUNE_{i+1}',rr+'.1',-4,0)
        wire(f'TUNE_{i+1}_SW',qr+'.S',ct+'.1');wire('H_ANT_A',qr+'.L',(x+2,287))
        wire(f'TUNE_{i+1}_MID',ct+'.2',(x+2,254),(x-4,254),cf+'.2');wire(f'TUNE_{i+1}_MID',(x+2,254),(x+8,254),cr+'.2')
        wire('H_ANT_B',cf+'.1',(x-4,235));wire('H_ANT_B',cr+'.1',(x+8,235))
    text('Selected working hypothesis: Ctop in series with (Cfront || Crear). Rear-bank vias suggest paired lower capacitors.',17,298,.58)
    text('Ceff = Ctop * (Cfront + Crear) / (Ctop + Cfront + Crear). Equal values give 2C/3 per enabled branch.',17,303,.58)
    text('All-parallel and all-series banks remain alternatives. Emitter rail / collector orientation is provisional.',17,308,.58)

def pir_options():
    block('07  PIR / AUXILIARY RAIL',231,215,100,73,'H14-H15: J3 pin order and U6 LDO topology are low-confidence.')
    part('U6',260,244,value='LDO? / WN23',pins=[pin('R1','VIN? (1)',-7,-3,0,'power_in'),pin('R2','GND? (2)',0,7,90,'power_in'),pin('R3','EN? (3)',-7,3,0,'input'),pin('L1','OUT? (5)',7,-3,180,'power_out'),pin('L2','NC? (4)',7,3,180)],size=(5,5),hyp='H14: selected SOT23-5 LDO topology from two adjacent capacitors; WN can also identify RT9818 supervisor, so all role assignments remain provisional.')
    part('R37',244,233);part('C36',237,246,orientation='v',value='1u?');part('C37',280,246,orientation='v',value='1u?');part('C32',313,241,orientation='v',value='100n?');part('J3',319,258,value='PIR BOARD',pins=[pin('1','1 / V+?',-4,-4,0),pin('2','2 / GND?',-4,0,0),pin('3','3 / SIG?',-4,4,0)],size=(2,6))
    stub('H_VDD','R37.1',-4,0);wire('H_AUX_IN','R37.2',(249,233),(249,241),'U6.R1');wire('H_AUX_IN','C36.1',(237,241),(249,241));wire('H_AUX_IN','U6.R3',(249,247),(249,241))
    wire('H_PIR_VDD','U6.L1',(280,241),'C37.1');wire('H_PIR_VDD',(280,241),(290,241),(290,232),(313,232),'C32.1');wire('H_PIR_VDD',(290,241),(290,254),'J3.1');label('H_PIR_VDD',(290,232))
    bus('H_GND',257,['C36.2','U6.R2','C37.2']);wire('H_GND','C32.2',(323,244),(323,269),(309,269),(309,258),'J3.2');label('H_GND',(309,269))
    part('Q2',288,272,'NPN',value='BC847B?',hyp='H15: 1FW suggests BC847B. B=R E=L C=S. PIR interface role and J3 order inferred.')
    part('R38',269,272);part('R39',277,280,orientation='v');part('R32',301,270,orientation='v');part('R33',310,278,orientation='v');part('TP16',301,264)
    wire('PIR_BASE','R38.2','Q2.R');wire('PIR_BASE','R39.1',(277,272));stub('H_GND','R39.2',-3,0);stub('H_GND','Q2.L',0,7)
    wire('H_PIR_RAW','J3.3',(306,262),(306,265),(262,265),(262,272),'R38.1');wire('H_PIR_RAW','R33.1',(306,275),(306,265));stub('H_PIR_VDD','R33.2',3,0)
    wire('H_PIR_SIG','Q2.S',(290,264),'TP16.1');wire('H_PIR_SIG','R32.1',(301,264),(299,264))
    stub('H_PIR_VDD','R32.2',2,0);label('H_PIR_SIG',(290,264))
    block('08  UNRESOLVED / UNPOPULATED OPTIONS',231,293,100,20,'No invented ties on untraced spare pads; original reference aliases retained.')
    for ref,x in [('R35',241),('R36',254),('C41',267),('C49',280),('D4',293),('D5',306),('D6',319)]:part(ref,x,308)

def legend():
    block('READING THIS WORKING RECONSTRUCTION',337,215,119,98,'One sheet. Functional wiring is proposed; this is not a verified production circuit.')
    for i,t in enumerate([
        '150 original main-board catalog entries, including DNP footprints and named pads.',
        'H_* = inferred inter-block net. Other net names do not imply measurement.',
        '? on a part value or pin function means an estimate or candidate identity.',
        'Original photographed pad names remain on ambiguous packages (L/R/S etc.).',
        'U2 and U3 use multiple symbol units on this same sheet, including supply units.',
        '29 original local visual fragments are retained; added connections are hypotheses.',
        'PIC GPIOs are intentionally unassigned where photographs cannot support a map.',
        'DNP = unpopulated. An open pin means unresolved, not a certified no-connect.',
        'PIR daughterboard internals are not yet traced; J3 represents its interface.',
        'No capacitor value or rail voltage in this drawing was electrically measured.',
        'See docs/RECONSTRUCTION.md for evidence, alternatives, and calculations.',
    ]):text(t,341,229+i*4,.58)
    part('U6A',347,285,size=(3,3));part('U7',363,285,size=(3,3));part('Q9',381,285,size=(3,3));part('J6',397,285,size=(3,3))
    part('TP9',345,301);part('TP10',361,301);part('VREF',379,301,value='VREF pad / net ?')
    text('Spare footprints / unassigned test pads',405,284,.5)
    text('v0.2  |  2026-10-07',405,301,.65)

def on(p,w):
    a,b=w['a'],w['b']
    return ((a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0])))

def lib_entry(ref,embedded=True):
    d=LIB[ref];name=d['lid'] if embedded else d['lid'].split(':')[1];actual=REF_MAP.get(ref,ref)
    hide=next(i['kind'] for i in INST if i['ref']==ref) in ['NPN','PNP','DUALD']
    out=[f'(symbol {q(name)} (pin_names (offset 0.635){" hide" if hide else ""}) (in_bom yes) (on_board yes)',f'(property "Reference" {q(actual.rstrip("0123456789"))} (at 0 0 0) {eff(.5)})',f'(property "Value" {q(C[ref].get("proposed_value",C[ref]["value"]))} (at 0 0 0) {eff(.5)})']
    for unit,(g,pins) in d['units'].items():
        out.append(f'(symbol {q("RE_"+ref+"_"+str(unit)+"_1")}');out.extend(g)
        for p in pins:
            out.append(f'(pin {p["typ"]} line (at {mm(p["x"])} {mm(-p["y"])} {p["side"]}) (length {mm(p["length"])}) (name {q(p["name"])} {eff(.42)}) (number {q(p["p"])} {eff(.4)}))')
        out.append(')')
    return '\n'.join(out+[')'])

def finish():
    assert USED==set(C),('missing',set(C)-USED)
    expected={r+'.'+p for r,c in C.items() for p in c['pins']}
    assert set(PINS)==expected,('pins',expected-set(PINS),set(PINS)-expected)
    member={};clashes=[]
    for ep,p in PINS.items():
        nn={w['net'] for w in WIRES if on(p,w)}|{l['net'] for l in LABELS if l['p']==p}
        if len(nn)>1:clashes.append((ep,p,sorted(nn)))
        if nn:member[ep]=sorted(nn)[0]
    # Unlike a plain crossing, a T-junction or wire endpoint creates a real native join.
    for w in WIRES:
        for p in [w['a'],w['b']]:
            nn={v['net'] for v in WIRES if on(p,v)}
            if len(nn)>1:clashes.append(('wire endpoint',p,sorted(nn)))
    for l in LABELS:
        nn={w['net'] for w in WIRES if on(l['p'],w)}
        assert nn=={l['net']},('label not attached to its intended wire',l,nn)
    if clashes:raise ValueError(json.dumps(sorted(set(map(str,clashes))),indent=2))
    for n in BASE['nets']:
        assert len({member.get(e,'UNRESOLVED:'+e) for e in n['endpoints']})==1,('original fragment lost',n)
    # Split every wire at same-net pins/endpoints, then de-duplicate segments and mark junctions.
    pts=defaultdict(set)
    for w in WIRES:pts[w['net']].update([w['a'],w['b']])
    for e,n in member.items():pts[n].add(PINS[e])
    for l in LABELS:pts[l['net']].add(l['p'])
    segments=set()
    for w in WIRES:
        ordered=sorted(p for p in pts[w['net']] if on(p,w))
        for a,b in zip(ordered,ordered[1:]):segments.add((w['net'],a,b))
    # Label only geometric pieces that need name-based connectivity. Local continuous circuits use wires alone.
    ad=defaultdict(lambda:defaultdict(set))
    for n,a,b in segments:ad[n][a].add(b);ad[n][b].add(a)
    all_labels=[dict(l,hidden=False) for l in LABELS]
    for n,edges in ad.items():
        seen=set();groups=[]
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
                if not any(l['net']==n and l['p'] in group for l in LABELS):all_labels.append(dict(net=n,p=sorted(group)[0],hidden=False))
    out=['(kicad_sch (version 20231120) (generator "eeschema")',f'(uuid {RID}) (paper "A0")', '(title_block (title "PetSafe 100-1339 R03 A - functional working reconstruction") (date "2026-10-07") (rev "0.2 - inferred") (company "PPA19-16811 microchip cat flap") (comment 1 "One sheet / photo evidence plus explicit hypotheses / not continuity verified"))', '(lib_symbols']
    out.extend(lib_entry(r) for r in LIB);out.append(')');out.extend(GRAPH)
    for n,a,b in sorted(segments):out.append(f'(wire (pts (xy {mm(a[0])} {mm(a[1])}) (xy {mm(b[0])} {mm(b[1])})) (stroke (width 0) (type default)) (uuid {uid("wire:"+str((n,a,b)))}))')
    for n,edges in ad.items():
        for p,neighbours in edges.items():
            if len(neighbours)>=3:out.append(f'(junction (at {mm(p[0])} {mm(p[1])}) (diameter 0) (color 0 0 0 0) (uuid {uid("junction:"+str((n,p)))}))')
    for i,l in enumerate(all_labels):
        x,y=l['p'];out.append(f'(label {q(l["net"])} (at {mm(x)} {mm(y)} 0) {eff(.48,"left bottom",l["hidden"])} (uuid {uid("label:"+str((i,l)))}))')
    for d in INST:
        ref,x,y,u=d['ref'],d['x'],d['y'],d['unit'];iid=uid('instance:'+ref+':'+str(u))
        out.append(f'(symbol (lib_id {q(d["lid"])}) (at {mm(x)} {mm(y)} 0) (unit {u}) (in_bom yes) (on_board yes) (dnp {"yes" if C[ref]["value"]=="DNP" else "no"}) (uuid {iid})')
        display=d['actual']+('ABC'[u-1] if len(LIB[ref]['units'])>1 else '')
        out.append(f'(property "Reference" {q(d["actual"])} (at {mm(d["rx"])} {mm(d["ry"])} 0) {eff(.55,d["just"])})')
        out.append(f'(property "Value" {q(d["value"])} (at {mm(d["vx"])} {mm(d["vy"])} 0) {eff(.48,d["just"])})')
        for key,val in [('OriginalReference',ref),('Evidence','Photo-based working reconstruction; inferred links are unverified'),('Hypothesis',C[ref].get('hypothesis','See docs/RECONSTRUCTION.md'))]:out.append(f'(property {q(key)} {q(val)} (at {mm(x)} {mm(y)} 0) {eff(.5,hide=True)})')
        for p in d['pins']:out.append(f'(pin {q(p["p"])} (uuid {uid(iid+":"+p["p"])}))')
        out.append(f'(instances (project {q(PROJECT)} (path "/{RID}" (reference {q(d["actual"])}) (unit {u})))) )')
    out.append('(sheet_instances (path "/" (page "1"))) )')
    OUT.mkdir(exist_ok=True)
    (OUT/(PROJECT+'.kicad_sch')).write_text('\n'.join(out),encoding='utf-8',newline='\n')
    (OUT/'PetSafe_Working.kicad_sym').write_text('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+'\n'.join(lib_entry(r,False) for r in LIB)+'\n)',encoding='utf-8',newline='\n')
    (OUT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "PetSafe_Working") (type "KiCad") (uri "${KIPRJMOD}/PetSafe_Working.kicad_sym") (options "") (descr "Photo-based working symbols; physical pad identifiers retained")))',encoding='utf-8',newline='\n')
    (OUT/(PROJECT+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':PROJECT+'.kicad_pro','version':1}},indent=2),encoding='utf-8',newline='\n')
    nets=[dict(net=n,endpoints=sorted(e for e,v in member.items() if v==n),status='HYPOTHESIS / retains visual fragments where listed',original_fragments=[v['net'] for v in BASE['nets'] if all(member.get(e)==n for e in v['endpoints'])]) for n in sorted(set(member.values()))]
    unresolved=sorted(set(PINS)-set(member))
    model=dict(board=BASE['board'],revision='v0.2',status='INFERRED WORKING CIRCUIT / NOT CONTINUITY VERIFIED',components=list(C.values()),nets=nets,original_visual_fragments=BASE['nets'],unresolved_pins=unresolved,reference_map=REF_MAP,geometric_wires=[dict(net=n,a=a,b=b) for n,a,b in sorted(segments)],pin_positions=PINS,sources=BASE['sources'])
    (ROOT/'evidence/reconstruction.json').write_text(json.dumps(model,indent=2),encoding='utf-8',newline='\n')
    with (ROOT/'evidence/proposed_nets.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(['net','status','endpoints','retained_original_fragments'])
        for n in nets:wr.writerow([n['net'],n['status'],';'.join(n['endpoints']),';'.join(n['original_fragments'])])
    with (ROOT/'evidence/unresolved_pins.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(['original_ref','pin','reason'])
        for ep in unresolved:
            r,p=ep.split('.');wr.writerow([r,p,'Unpopulated footprint' if C[r]['value']=='DNP' else 'Trace / function unresolved; no certified NC flag'])
    print(json.dumps(dict(components=len(C),symbol_units=len(INST),physical_pins=len(PINS),proposed_nets=len(nets),unresolved_pins=len(unresolved),preserved_visual_fragments=len(BASE['nets']),schematic=str(OUT/(PROJECT+'.kicad_sch'))),indent=2))

if __name__=='__main__':
    power();controller();motor_ui();rf();receiver();tuning();pir_options();legend();finish()
