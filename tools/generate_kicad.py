"""Generate a conservative native KiCad capture plus an independent SVG preview.
No third-party packages. The SVG is NOT rendered by KiCad. It visualizes the same
placement/model. Native application load and ERC must be run separately.
"""
from pathlib import Path
import json, uuid, math, re, html, collections
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'schematic'; OUT.mkdir(exist_ok=True)
MODEL=json.loads((ROOT/'evidence/reconstruction.json').read_text())
COMPS=MODEL['components']; NETS=MODEL['nets']
NS=uuid.UUID('076b4909-cd37-4b6a-aedf-0c836ebdfd57')
def uid(s): return str(uuid.uuid5(NS,s))
def q(s): return json.dumps(str(s),ensure_ascii=False)
def num(x): return f'{x:.4f}'.rstrip('0').rstrip('.') if x else '0'
def eff(sz=1.05,justify='',hide=False):
 return f'(effects (font (size {num(sz)} {num(sz)})){" (justify "+justify+")" if justify else ""}{" hide" if hide else ""})'
PROJECT='PetSafe_1001339'; RID=uid('root')
sections=[('control','MCU, clock and programming'),('motor','Motor driver, switch and battery interface'),('power','Power conditioning and PIR interface'),('receiver','Analogue receive section'),('tuning','Switched antenna capacitor branches'),('rf_drive','Antenna drive, filtering and indicators')]
motor={'U5','Q1','S1','C27','C33','C34','R43','R44','TP14','TP15','BATP','BATN','J5'}
for c in COMPS:
 if c['ref'] in motor:c['sheet']='motor'
# Known package pin assignments. Other parts retain explicitly physical pad IDs.
pic=['RE3/MCLR/VPP','RA0','RA1','RA2','RA3','RA4','RA5','VSS','RA7/OSC1','RA6/OSC2','RC0','RC1','RC2','RC3','RC4','RC5','RC6','RC7','VSS','VDD','RB0','RB1','RB2','RB3','RB4','RB5','RB6/ICSPCLK','RB7/ICSPDAT']
known={'U4':{str(i+1):v for i,v in enumerate(pic)},'U5':dict(zip(map(str,range(1,9)),['VCC_LOGIC','INA','INB','VDD_MOTOR','OUTB','GND','GND','OUTA'])),'U3':dict(zip(map(str,range(1,9)),['OUTA','INA-','INA+','VS-','INB+','INB-','OUTB','VS+']))}
net_by_pin={ep:n['net'] for n in NETS for ep in n['endpoints']}
# Local labels are safe only while all ends of each recorded net share one sheet.
for n in NETS:
 sheets={next(c['sheet'] for c in COMPS if c['ref']==ep.rsplit('.',1)[0]) for ep in n['endpoints']}
 assert len(sheets)==1,(n['net'],sheets)
svg_all=[]; placement={}; symbol_lib=[]

def symbol_geom(c):
 pins=c['pins']; k=c['kind']
 if k in ('R','C','L','D2','Y'):
  return {'half_w':4,'half_h':1.6,'pins':[('1',-7.62,0,0),('2',7.62,0,180)],'kind':k}
 if k=='TP':return {'half_w':1,'half_h':1,'pins':[('1',-5.08,0,0)],'kind':k}
 n=math.ceil(len(pins)/2); w=18 if c['ref']=='U4' else (16 if c['ref'] in ('U3','U5') else 11)
 h=max(4,((n-1)*2.54)/2+2.54)
 pp=[]
 left=pins[:n];right=pins[n:]
 for row,p in enumerate(left):pp.append((p,-w-5.08,(n-1)*1.27-row*2.54,0))
 for row,p in enumerate(reversed(right)):pp.append((p,w+5.08,(len(right)-1)*1.27-row*2.54,180))
 return {'half_w':w,'half_h':h,'pins':pp,'kind':k}

def pin_type(c,p):
 if c['ref']=='U3':return 'output' if p in ('1','7') else 'power_in' if p in ('4','8') else 'input'
 if c['ref']=='U5':return 'power_in' if p in ('1','4','6','7') else 'input' if p in ('2','3') else 'output'
 if c['ref']=='U4':return 'power_in' if p in ('8','19','20') else 'bidirectional'
 return 'passive'

def libsymbol(c,g):
 name='RE_'+c['ref'];libid='PetSafe_RE:'+name;k=c['kind'];w=g['half_w'];h=g['half_h']
 s=[f'(symbol {q(libid)} (pin_names (offset 0.8)) (in_bom yes) (on_board yes)',
    f'(property "Reference" {q(c["ref"])} (at 0 {num(h+4)} 0) {eff()})',
    f'(property "Value" {q(c["value"])} (at 0 {num(h+1.8)} 0) {eff()})',
    f'(symbol {q(name+"_0_1")}']
 stroke='(stroke (width 0.254) (type default))'
 if k=='C':
  for x in [-1,1]:s.append(f'(polyline (pts (xy {x} -2) (xy {x} 2)) {stroke} (fill (type none)))')
  for a,b in [(-2.54,-1),(1,2.54)]:s.append(f'(polyline (pts (xy {a} 0) (xy {b} 0)) {stroke} (fill (type none)))')
 elif k=='R':s.append(f'(rectangle (start -2.54 1.27) (end 2.54 -1.27) {stroke} (fill (type none)))')
 elif k=='TP':s.append(f'(circle (center 0 0) (radius 1) {stroke} (fill (type none)))')
 elif k in ('L','Y','D2'):
  # Unknown diode polarity and magnetic subtype are intentionally not invented.
  s.append(f'(rectangle (start -2.54 1.6) (end 2.54 -1.6) {stroke} (fill (type none)))')
 else:s.append(f'(rectangle (start {num(-w)} {num(h)}) (end {num(w)} {num(-h)}) {stroke} (fill (type background)))')
 s+=[')',f'(symbol {q(name+"_1_1")}']
 for p,x,y,ang in g['pins']:
  pname=known.get(c['ref'],{}).get(p,'~' if k in ('R','C','L','D2','Y','TP') else p)
  length=5.08 if k!='TP' else 4.08
  s.append(f'(pin {pin_type(c,p)} line (at {num(x)} {num(y)} {ang}) (length {num(length)}) (name {q(pname)} {eff(0.95)}) (number {q(p)} {eff(0.9)}))')
 s+=['))'];return '\n'.join(s)

def text_native(s,x,y,sz=1.05):return f'(text {q(s)} (at {num(x)} {num(y)} 0) {eff(sz,"left")} (uuid {uid("text:"+str(x)+":"+str(y)+":"+s)}))'

def svgtext(s,x,y,sz=1.05,anchor='start',color='#192f3a',weight='normal'):
 return f'<text x="{x:.3f}" y="{y:.3f}" font-size="{sz}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}" font-family="Arial, sans-serif">{html.escape(s)}</text>'

def draw_svg_comp(c,g,x,y):
 s=[];w=g['half_w'];h=g['half_h'];k=c['kind'];col='#526573' if c['population']=='DNP' else '#192f3a'
 if k in ('IC','CONN','SW'):
  s.append(f'<rect x="{x-w}" y="{y-h}" width="{2*w}" height="{2*h}" fill="#f0f5f7" stroke="{col}" stroke-width=".25"/>')
 elif k=='TP':s.append(f'<circle cx="{x}" cy="{y}" r="1" fill="none" stroke="{col}" stroke-width=".25"/>')
 elif k=='C':
  for xx in [-1,1]:s.append(f'<path d="M{x+xx} {y-2}v4" stroke="{col}" stroke-width=".3"/>')
  s.append(f'<path d="M{x-2.54} {y}h1.54 M{x+1} {y}h1.54" stroke="{col}" stroke-width=".25"/>')
 else:s.append(f'<rect x="{x-2.54}" y="{y-1.4}" width="5.08" height="2.8" fill="none" stroke="{col}" stroke-width=".25"/>')
 s.append(svgtext(c['ref'],x,y-h-5.2,1.5,'middle',weight='bold'))
 s.append(svgtext(c['value'],x,y-h-2.6,1.2,'middle'))
 for p,px,py,ang in g['pins']:
  xx,yy=x+px,y-py;sgn=1 if ang==0 else -1;length=5.08 if k!='TP' else 4.08
  s.append(f'<path d="M{xx} {yy}h{sgn*length}" stroke="{col}" stroke-width=".2"/>')
  s.append(svgtext(p,xx+sgn*1.5,yy-.65,.8,'middle'))
  pname=known.get(c['ref'],{}).get(p,'')
  if pname:s.append(svgtext(pname,xx+sgn*(length+.7),yy+.35,.95,'start' if ang==0 else 'end'))
  n=net_by_pin.get(c['ref']+'.'+p)
  if n:
   end=xx-sgn*3.81
   s.append(f'<path d="M{xx} {yy}H{end}" stroke="#147367" stroke-width=".27"/>')
   s.append(svgtext(n,end,yy-.7,.83,'end' if ang==0 else 'start',color='#147367'))
  else:s.append(f'<circle cx="{xx}" cy="{yy}" r=".42" fill="white" stroke="#c06624" stroke-width=".2"/>')
 src=c['source'].split(';')[0].replace('.jpg','')
 s.append(svgtext(src+' | '+('unpopulated footprint' if c['population']=='DNP' else f'{c["traced_pin_count"]}/{len(c["pins"])} pads in local fragments'),x,y+h+5.4,.9,'middle',color='#657681'))
 return '\n'.join(s)

for section_index,(section,title) in enumerate(sections,start=2):
 cc=[c for c in COMPS if c['sheet']==section]
 # Complex parts first; photo regions have their own sheets instead of one crowded page.
 cc.sort(key=lambda c:(-len(c['pins']), c['ref'].rstrip('0123456789'),int(re.search(r'\d+',c['ref']).group()) if re.search(r'\d+',c['ref']) else 0,c['ref']))
 geom={c['ref']:symbol_geom(c) for c in cc};sid=uid('sheet:'+section)
 s=[f'(kicad_sch (version 20231120) (generator "petsafe_photo_reconstruction") (uuid {uid("file:"+section)}) (paper "A3")',
    f'(title_block (title {q("PetSafe 100-1339 R03 A | "+title)}) (date "2026-10-07") (rev "0.1 - INCOMPLETE") (comment 1 "Photo-led reconstruction; NO continuity measurements received"))',
    '(lib_symbols']
 for c in cc:
  lib=libsymbol(c,geom[c['ref']]);s.append(lib);symbol_lib.append(lib)
 s.append(')')
 svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 297" width="1680" height="1188">','<rect width="420" height="297" fill="white"/>']
 headers=[(title,15,15,3.8),('PetSafe 100-1339 R03 A | v0.1 | INCOMPLETE PHOTO-LED CAPTURE',15,23,1.65),('Green named stubs: visible local copper only. Open pins: unresolved, NOT intentionally unconnected.',15,29,1.25)]
 for txt,x,y,sz in headers:s.append(text_native(txt,x,y,sz));svg.append(svgtext(txt,x,y,sz))
 # 5 columns x 76 mm; row height expands for MCU and other ICs.
 y0=48;ix=0;rowheight=0
 for c in cc:
  g=geom[c['ref']];height=2*g['half_h']+23
  if ix==5:y0+=rowheight;ix=0;rowheight=0
  # Common row top, centre depends on individual symbol body height.
  x=48+ix*77;y=y0+g['half_h']+8;ix+=1;rowheight=max(rowheight,max(29,height))
  assert y+g['half_h']+8<277,(section,c['ref'],y)
  placement[c['ref']]={'sheet':section,'x':x,'y':y,'geometry':g}
  libid='PetSafe_RE:RE_'+c['ref'];idc=uid('component:'+c['ref']);path='/'+RID+'/'+sid
  s.append(f'(symbol (lib_id {q(libid)}) (at {num(x)} {num(y)} 0) (unit 1) (in_bom {"no" if c["kind"]=="TP" else "yes"}) (on_board yes) (dnp {"yes" if c["population"]=="DNP" else "no"}) (uuid {idc})')
  for prop,val,yy,hidden in [('Reference',c['ref'],y-g['half_h']-5.2,False),('Value',c['value'],y-g['half_h']-2.6,False),('Footprint','',y,True),('Datasheet',MODEL['sources'].get(c['value'].replace('XS',''),''),y,True),('Photo',c['source'],y,True),('Evidence','PHOTO_LED_UNMEASURED',y,True),('Notes',c['note'],y,True)]:
   s.append(f'(property {q(prop)} {q(val)} (at {num(x)} {num(yy)} 0) {eff(1.05,"",hidden)})')
  for p,_,_,_ in g['pins']:s.append(f'(pin {q(p)} (uuid {uid(c["ref"]+".pin."+p)}))')
  s.append(f'(instances (project {q(PROJECT)} (path {q(path)} (reference {q(c["ref"])}) (unit 1)))) )')
  for p,px,py,ang in g['pins']:
   n=net_by_pin.get(c['ref']+'.'+p)
   if not n:continue
   xx,yy=x+px,y-py;xe=xx+(-3.81 if ang==0 else 3.81)
   s.append(f'(wire (pts (xy {num(xx)} {num(yy)}) (xy {num(xe)} {num(yy)})) (stroke (width 0) (type default)) (uuid {uid(c["ref"]+".wire."+p)}))')
   s.append(f'(label {q(n)} (at {num(xe)} {num(yy)} 0) {eff(.85,"right bottom" if ang==0 else "left bottom")} (uuid {uid(c["ref"]+".label."+p)}))')
  svg.append(draw_svg_comp(c,g,x,y))
  s.append(text_native(c['source'].split(';')[0].replace('.jpg','')+' | '+('DNP' if c['population']=='DNP' else f'{c["traced_pin_count"]}/{len(c["pins"])} pads in fragments'),x-15,y+g['half_h']+5.4,.85))
 footer='Pad naming for unknown parts is physical, not electrical. No generic power symbols or hidden inferred nets.'
 s.append(text_native(footer,15,281,1.1));svg.append(svgtext(footer,15,281,1.1))
 s.append(')');svg.append('</svg>')
 (OUT/(section+'.kicad_sch')).write_text('\n'.join(s));(OUT/(section+'.svg')).write_text('\n'.join(svg));svg_all.append((section,title))
# Root hierarchy: no false electrical interconnects implied by functional organization.
s=[f'(kicad_sch (version 20231120) (generator "petsafe_photo_reconstruction") (uuid {RID}) (paper "A3")',
 '(title_block (title "PetSafe 100-1339 R03 A - reverse engineering") (date "2026-10-07") (rev "0.1 - INCOMPLETE")) (lib_symbols)']
for t,x,y,sz in [('PetSafe 100-1339 R03 A',20,20,5),('PHOTO-LED RECONSTRUCTION | v0.1 | NOT A COMPLETE CIRCUIT',20,31,2.4),('Open a child sheet to edit the captured components and locally traced copper.',20,41,1.6),('All untraced pins are left open intentionally as UNKNOWN, not marked NC.',20,49,1.6)]:s.append(text_native(t,x,y,sz))
for i,(section,title) in enumerate(sections):
 x=25+(i%2)*190;y=65+(i//2)*53;sid=uid('sheet:'+section)
 s.append(f'(sheet (at {x} {y}) (size 167 34) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {sid}) (property "Sheetname" {q(title)} (at {x} {y-2} 0) {eff(1.3,"left bottom")}) (property "Sheetfile" {q(section+".kicad_sch")} (at {x} {y+36} 0) {eff(1.1,"left top")}) (instances (project {q(PROJECT)} (path {q("/"+RID)} (page {q(i+2)})))))')
 n=sum(c['sheet']==section for c in COMPS)
 s.append(text_native(f'{n} catalog entries; inspect unresolved_pins.csv',x+5,y+17,1.2))
for j,t in enumerate([f'Status: {len(COMPS)} catalog entries including test points, aliases and empty footprints.',f'{len(NETS)} local net fragments. ZERO nets continuity-confirmed. Unmarked capacitances remain UNKNOWN.', 'Layer count is unconfirmed. Rear photographs suggest a broad plane and possibly inner routing.', 'This project is not an ESP32 modification schematic and must not be used to manufacture a replacement PCB.', 'The separate PIR daughterboard is not reconstructed in this revision.', 'Native KiCad load, ERC and netlist export have not been run in this environment.']):
 s.append(text_native(t,20,235+j*6,1.2))
s+=['(sheet_instances (path "/" (page "1")))',')']
(OUT/(PROJECT+'.kicad_sch')).write_text('\n'.join(s))
(OUT/(PROJECT+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':PROJECT+'.kicad_pro','version':1},'schematic':{},'libraries':{'pinned_symbol_libs':[],'pinned_footprint_libs':[]}},indent=2))
# Standalone library names omit library nickname. Embedded symbols are also present.
lib_text='\n'.join(symbol_lib).replace('(symbol "PetSafe_RE:RE_','(symbol "RE_')
(OUT/'PetSafe_RE.kicad_sym').write_text('(kicad_symbol_lib (version 20231120) (generator "petsafe_photo_reconstruction")\n'+lib_text+'\n)\n')
(OUT/'sym-lib-table').write_text('(sym_lib_table\n (lib (name "PetSafe_RE")(type "KiCad")(uri "${KIPRJMOD}/PetSafe_RE.kicad_sym")(options "")(descr "Photo-led reconstruction symbols"))\n)\n')
(ROOT/'evidence/schematic_placement.json').write_text(json.dumps(placement,indent=2))
(OUT/'preview.html').write_text('''<!doctype html><meta charset="utf-8"><title>PetSafe schematic capture preview</title><style>body{font:16px system-ui;margin:30px;background:#eef2f4;color:#182b37}h1{margin-bottom:10px}article{margin:24px 0;background:white;padding:14px}img{width:100%}nav a{margin-right:18px}p{max-width:1000px;line-height:1.6}.warn{border-left:5px solid #d57d24;padding:16px;background:#fff5e8}</style><h1>PetSafe schematic capture — v0.1</h1><p class="warn">Incomplete photo-led reconstruction. These SVGs are independent previews generated from the model, not exports from KiCad. Unconnected symbol pins are unresolved, not verified no-connects. Native application validation is pending.</p><nav>'''+''.join(f'<a href="#{a}">{html.escape(t)}</a>' for a,t in svg_all)+'</nav>'+''.join(f'<article id="{a}"><h2>{html.escape(t)}</h2><img src="{a}.svg" alt="{html.escape(t)}"></article>' for a,t in svg_all))
print('Generated root +',len(sections),'child KiCad sheets, embedded/standalone symbols and SVG previews.')
