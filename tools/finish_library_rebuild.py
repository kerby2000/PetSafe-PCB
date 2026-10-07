"""Route the MCP-placed stock symbols, keeping the physical-pad crosswalk explicit.

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
instances=children(tree,'symbol'); assert len(instances)==154
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
            xx=x+px*math.cos(rad)-py*math.sin(rad)
            yy=y-(px*math.sin(rad)+py*math.cos(rad))
            ALL_NATIVE[ref+'.'+pn]=xy((xx,yy))
            PIN_ANGLE[ref+'.'+pn]=int((angle+rot)%360)
    # Use legible, horizontal 1 mm fields; retaining library definitions intact.
    props={p[1]:p for p in children(inst,'property')}
    rx,ry,vx,vy=(old[k]*1.27 for k in ['rx','ry','vx','vy'])
    # Standard symbol bodies have different extents from the earlier sketches.
    if ref=='U4':rx=vx=x;ry=y-29.21;vy=y-27.305
    if ref in ['U2','U3'] and unit==3:rx=vx=x-12.7;ry=y-1.27;vy=y+0.635
    if ref=='U2' and unit in [1,2]:rx=vx=x;ry=y-12.065;vy=y-10.16
    if ref in ['U1','U5','U6','Q8']:rx=vx=x;ry=y-10.16;vy=y-8.255
    if ref in ['J1','J3','J5']:rx=vx=x+2.54;ry=y-3.81;vy=y-1.905
    if ref=='Y1':rx=vx=x;ry=y-5.08;vy=y-3.175
    if ref in ['C30','C31']:rx=vx=x+2.54;ry=y-0.635;vy=y+1.27
    if ref=='TP11':rx=vx=x-1.27;ry=y-5.08;vy=y-3.175
    if ref=='S1':rx=vx=x;ry=y-10.16;vy=y-8.255
    if ref=='C18':rx=vx=x-6.35;ry=y+3.81;vy=y+5.715
    if ref in ['TP9','TP10','TP104']:ry-=24*1.27;vy-=24*1.27
    if rot==180:rx=vx=x+4.445
    for name,px,py in [('Reference',rx,ry),('Value',vx,vy)]:
        prop=props[name];one(prop,'at')[1:]=[rnd(px),rnd(py),int(rot)%180]
        effects=one(prop,'effects')
        if effects:prop.remove(effects)
        just=old.get('just','')
        if ref in ['J1','J3','J5','C30','C31']:just='left'
        if rot==180:just=''
        prop.append(expr(f'(effects (font (size 1.016 1.016)){" (justify "+just+")" if just else ""})'))
    pop=next(cc['value'] for cc in model['components'] if cc['ref']==old['ref'])
    one(inst,'dnp')[1]=S('yes' if pop=='DNP' else 'no')
    for name,val in [('OriginalReference',old['ref']),('Evidence','Photo reconstruction; topology inferred'),
                     ('LibraryPolicy','Unmodified KiCad 10 stock symbol'),
                     ('PinMapping','See evidence/pin_crosswalk.json; physical orientation may be provisional')]:
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
    if w['net']=='H_GND' and (w['a']==[57,159] or w['b']==[57,159] or w['a']==[57,190] or w['b']==[57,190]):continue
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
    w=dict(a=l['p'],b=l['p'])
    if not excluded(w):L.append(dict(net=l['net'],p=oldpoints.get(mm(l['p']),mm(l['p']))))
wire('H_GND','C9.2',(49,159),(49,190),(53,190))

# U1 remains a numbered, explicitly temporary stock placeholder.
wire('H_VBAT','BATP.1','L2.1');label('H_VBAT',(23,42))
wire('H_LDO_IN','L2.2','U1.L1');wire('H_LDO_IN','C1.1',(44,42))
wire('H_LDO_IN','C1A.1',(38,49),(38,42));wire('H_LDO_IN','U1.L3',(52,46),(52,42))
wire('H_GND','U1.L2',(50,44),(50,64));bus('H_GND',64,['C1.2','C1A.2','C2.2','C2A.2','GND.1'])
wire('H_VDD','U1.R1',(56,50),(56,60),(82,60),(82,42),'VDD.1')
wire('H_VDD','C2.1',(90,42));wire('H_VDD','C2A.1',(106,42));label('H_VDD',(101,42))
wire('U1_ALT_PAD','U1.R2',(54,48),(54,81),(115,81),'C4.2')
wire('U1_ALT_PAD','R1.2',(48,87),(48,81),(54,81));wire('U1_ALT_PAD','C3.2',(72,87),(72,81));wire('U1_ALT_PAD','R2.2',(97,87),(97,81))
label('U1_ALT_PAD',(80,81))

# PIC: official SOIC symbol; both ground pins share the library endpoint.
bus('H_VDD',32,['U4.20','C25.1','C26.1','C39.1']);bus('H_GND',44,['C25.2','C26.2','C39.2'])
wire('ICSP_CLK','U4.27',(228,76),(228,43),'J1.CLK');label('ICSP_CLK',(230,43))
wire('ICSP_DAT','U4.28',(231,78),(231,45),'J1.DAT');label('ICSP_DAT',(233,45))
stub('MCLR_VPP','U4.1',-12);stub('MCLR_VPP','J1.VPP',-12)
stub('H_VDD','J1.VDD',-8)
wire('H_GND','J1.GND',(263,51),(263,104));wire('H_GND','U4.8',(207,104),(263,104));label('H_GND',(207,104))
wire('OSC1','U4.9',(233,60),(233,85),(238,85),(238,89),'Y1.1');wire('OSC1','C30.1',(238,89))
wire('OSC2','U4.10',(235,58),(235,83),(254,83),(254,89),'Y1.2');wire('OSC2','C31.2',(254,89))
wire('H_GND','C30.2',(238,104));wire('H_GND','C31.1',(254,104));wire('PIC_RC3','U4.14','TP11.1')
stub('H_VBAT','R3.1',0,-4);wire('H_BAT_SENSE','R3.2',(280,75),'R4.1');wire('H_BAT_SENSE',(280,75),'TP17.1');wire('H_BAT_SENSE','C28.1',(296,75));label('H_BAT_SENSE',(284,75));bus('H_GND',94,['R4.2','C28.2'])

# MX512H physical pin numbering, not a DRV8837 pin substitution.
wire('H_VBAT','C33.1',(339,33),(350,33),(350,52),'U5.4');label('H_VBAT',(339,33))
wire('H_VDD','U5.1',(345,46),(345,43),(330,43),'C34.1');label('H_VDD',(330,43))
wire('H_GND','C33.2',(339,69));bus('H_GND',69,['C34.2','BATN.1'])
wire('H_GND','U5.6',(376,50),(376,69));wire('H_GND','U5.7',(378,48),(378,69))
wire('H_MOTOR_A','U5.8',(372,46),(372,43),(384,43),(384,49),'J5.A')
wire('H_MOTOR_B','U5.5',(370,52),(370,55),(386,55),(386,51),'J5.B');wire('H_MOTOR_B','TP15.1',(381,55))
stub('H_MOTOR_INA','U5.2',-10);stub('H_MOTOR_INB','U5.3',-10)

# WN23 unidentified five-pin package; provisional functional roles remain explicit.
stub('H_VDD','R37.1',-4)
wire('H_AUX_IN','R37.2',(249,233),(249,240),'U6.R1')
wire('H_AUX_IN','C36.1',(237,240),(249,240));wire('H_AUX_IN','U6.R3',(249,244),(249,240))
wire('H_GND','U6.R2',(247,242),(247,257));bus('H_GND',257,['C36.2','C37.2'])
wire('H_PIR_VDD','U6.L1',(252,248))
wire('H_PIR_VDD',(252,248),(252,250),(284,250),(284,241),(280,241),'C37.1')
wire('H_PIR_VDD',(280,241),(290,241),(290,232),(313,232),'C32.1')
wire('H_PIR_VDD',(290,241),(290,256),'J3.1');label('H_PIR_VDD',(290,232))
wire('H_GND','C32.2',(323,244))

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
        t='U1 stock placeholder: 1 VIN, 2 GND, 3 EN, 4 NC, 5 OUT. Exact symbol pending.'
    if 'Original photographed pad names remain' in t:
        t='Library pin numbers are mapped to photo pads in evidence/pin_crosswalk.json.'
    if t.startswith('v0.2'):t='v0.3 | KiCad 10.0.5 | 2026-10-08';n['y']=292
    if t.startswith('H03:'):n['y']=106
    text(t,n['x'],n['y'],1.27 if n['size']>=1 else max(.762,n['size']*1.27))
text('U5 placeholder: 1 VCC, 2 INA, 3 INB, 4 VDD, 5 OUTB, 6/7 GND, 8 OUTA.',320,77,.762)
text('U3 alternative: MCP6002-I/SN; same pin roles, electrical suitability to verify.',288,208,.762)
text('U5 alternative: DRV8212PDSGR. Different package/pins; redesign required.',320,81,.762)
text('U6 placeholder: 1 VIN?, 2 GND?, 3 EN?, 4 NC?, 5 OUT?.',234,284,.762)
text('Q8 indices: 1=T1, 2=T2, 3=T3, 4=B3, 5=B2, 6=B1. Identity open.',90,202,.762)

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
tree.append(expr('(title_block (title "PetSafe 100-1339 R03 A | single-sheet reconstruction") (date "2026-10-08") (rev "0.3") (company "KiCad 10 standard libraries | MCP authoring") (comment 1 "Inferred circuit. Numbered placeholders pending vendor symbols; not hardware verified."))'))
# Canonical pretty printer supplied by the installed MCP server.
sys.path.insert(0,str(Path.home()/'Documents/VS.Code.Projects/KiCAD-MCP-Server/python'))
from utils.sexpr_format import prettify
out=R/'schematic/PetSafe_1001339.kicad_sch'
out.write_text(prettify(sx.dumps(tree)),encoding='utf-8',newline='\n')
model.update(revision='v0.3',coordinate_units='mm',native_pin_crosswalk=layout['crosswalk'],pin_positions={e:list(p) for e,p in P.items()},
             geometric_wires=[dict(net=n,a=a,b=b) for n,a,b in segments],library_policy='KiCad 10 stock symbols, MCP placed; no custom symbol definitions')
for c in model['components']:
    entry=next(x for x in layout['catalog'] if x['original_ref']==c['ref'])
    c['library_symbol']=entry['symbol'];c['footprint']=entry['footprint']
(R/'evidence/reconstruction.json').write_text(json.dumps(model,indent=2),encoding='utf-8',newline='\n')
print(f'Routed {len(segments)} segments. Preserved {len(expected)} connected pads, {len(P)-len(expected)} unresolved pads. {len(libs)} stock symbols, zero custom symbols.')
