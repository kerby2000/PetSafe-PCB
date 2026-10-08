"""Current board-wide completion picture; native connectivity is not proof of hardware."""
from pathlib import Path
from collections import Counter
import json,csv
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4

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
local={1:'J1 VPP; mapping inferred; D6 route missing',2:'C25 signal pad / V031; onward destination unknown',3:'R28 + R29 + TP7; user meter / visible trace',4:'C39 signal pad / V035; onward destination unknown',
5:'No visible exit; V036 under-body alignment candidate only',6:'No visible exit; V037 under-body alignment candidate only',7:'No visible exit; V039 under-body alignment candidate only',8:'GND / V041 photo anchor',9:'Y1 oscillator; photo-derived',10:'Y1 oscillator; photo-derived',
11:'No visible exit; V047 under-body alignment candidate only',12:'VREF board pad / V053; visible local route, remote net unknown',13:'No visible exit; V049 under-body alignment candidate only',14:'TP11; visible route; onward destination unknown',
15:'V022 user association; remote destination unknown',16:'V023 user association; remote destination unknown',17:'R13; user meter / visible trace',18:'TP17; visible route; old R13 guess withdrawn',19:'GND / C32 / V045 photo anchor',20:'Regulated VDD / C32 / V042 photo anchor',
21:'V026; user correction. Onward destination unknown',22:'TP2 / R31; user meter / visible trace',23:'TP1 / R30; user meter / visible trace',24:'R4; photo-derived; sensing role remains inferred',25:'TP4 / C41; user meter / visible trace',26:'TP10 / R35; user meter / visible trace',27:'ICSP CLK / D4 / R32; photo-derived',28:'ICSP DAT / D5 / R40; photo-derived'}
pins=[dict(pin=n,gpio=func[n],net=member.get(f'U4.{n}'),open_pad=n in gpios,evidence=local[n]) for n in range(1,29)]
gaps=[
('PIC / block interfaces',f'{len(gpios)} GPIO pads still open: '+', '.join(map(str,gpios))+'. Other pins have local nets but may lack remote continuations. Motor INA/INB origins remain inferred.', 'Continuity on the numbered PIC map; start with hidden via destinations.'),
('Q8 / RF output / C6','V113/V115 reported GND conflicts with the outer-pad output hypothesis. C6.1 path unresolved despite 10 ohm to P.', 'Clarify whether GND was measured; compare outer pads to the same GND hole.'),
('Tuning bank','Ground returns corrected. Five local capacitor midpoints are known; connections onward to the antenna are not established.', 'Check V090/V095/V100/V103/V107 to ANT1 and ANT2.'),
('Auxiliary / receiver','V063 feed unknown. V017 joins R42.1/R44.1; circuit role unknown. V011-V014 and V072 destinations are unresolved after rejected associations.', 'Identify these remote nets; R44.1 is a photo-selected pad. Receiver bias is still inferred.'),
('D2 / D6 / candidate parts','D2/4P identity and all three pad routes remain open. D6 has two open pads. U6/Q8 and small BJTs/diodes retain candidate identities/polarities.', 'D2 diode-mode guide; D6 continuity; targeted candidate pin checks.'),
('Other open fitted pads','C26.1 and TP9.1; U6 NC pins 4/5 have unknown external ties. LED common and S1 leg mapping are still provisional.', 'Targeted continuity; no need to identify chips on empty footprints.'),
('Component values','44 unmarked fitted capacitor values and L1/L2 type/value remain unrecovered. C5 = 470uF / 16V is recorded; 38 fitted resistors have decoded nominal values.', 'LCR first on RF/tuning parts, recording frequency; in-circuit results are network readings.'),
('Packages','147/150 footprints assigned. C5, S1 and LED1 still need exact geometry; other photo-based package assignments remain candidates.', 'C5 diameter/lead spacing; S1/LED1 body and pad spacing. R8/C11 sizes already recorded.'),
]
status=read('evidence/completion_status.json')
status.update(revision=m['revision'],unresolved_physical_pins=len(m['unresolved_pins']),unresolved_pins_by_population=dict(counts),
    current_gpio_pins=gpios,current_fitted_open_pads=fitted,current_dnp_open_pads=dnp,current_gaps=[dict(area=x,gap=y,method=z) for x,y,z in gaps],
    via_review=a['review_summary'],complete_symbols_for_selected_candidates=True)
status['completed']=[s.replace('Five additional PIC local routes from existing photos; 14 GPIO pins remain open','v0.7 historical: five additional PIC local routes recovered; current GPIO count below') for s in status['completed']]
entry='v0.9: 28 endpoint corrections from user via review and component-pad cross-checks; 37 open pads, eight GPIO pads'
if entry not in status['completed']:status['completed'].append(entry)
entry='v0.9.1: 21 via-site corrections; V017 joins R42.1/R44.1; V033 rejected; V073 GND-only conflict resolved'
if entry not in status['completed']:status['completed'].append(entry)
for item in status['items']:
    if item['refs']==['U6']:item['detail']+=' v0.9: R37/R39 share V063; remote feed unknown, previous rail assignments withdrawn.' if 'v0.9:' not in item['detail'] else ''
    if item['refs']==['Q8']:item['detail']+=' v0.9 HOLD: V113/V115 user GND conflicts with output hypothesis; no ground merge applied.' if 'v0.9 HOLD' not in item['detail'] else ''
    if 'U4' in item['refs']:item['detail']='Eight GPIO pads open: 5,6,7,11,13,15,16,21. RC1/pin12 now locally connected to VREF/V053; remote continuations are separately unresolved. See pic_gpio_status.json.'
save('evidence/completion_status.json',status)
save('evidence/pic_gpio_status.json',dict(revision=m['revision'],pins=pins,open_gpio_pins=gpios,qualification='A modeled local net does not certify its remote role or all attached inferred branches.'))
with (R/'evidence/pic_gpio_status.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(pins[0]));w.writeheader();w.writerows(pins)

styles=getSampleStyleSheet();ink=HexColor('#183F3B');teal=HexColor('#007D70');amber=HexColor('#AD512E')
styles.add(ParagraphStyle(name='TitlePS',fontName='Helvetica-Bold',fontSize=24,leading=28,textColor=ink,spaceAfter=9))
styles.add(ParagraphStyle(name='BodyPS',fontName='Helvetica',fontSize=9,leading=12,textColor=ink,spaceAfter=6))
styles.add(ParagraphStyle(name='SmallPS',fontName='Helvetica',fontSize=8,leading=10.5,textColor=ink))
styles.add(ParagraphStyle(name='HeadPS',fontName='Helvetica-Bold',fontSize=12,leading=15,textColor=teal,spaceBefore=8,spaceAfter=6))
styles.add(ParagraphStyle(name='TableHeadPS',fontName='Helvetica-Bold',fontSize=8,leading=10,textColor=white))
def P(s,style='BodyPS'):return Paragraph(s,styles[style])
def table(rows,widths):
    data=[[P(escape(str(x)),'TableHeadPS' if i==0 else 'SmallPS') for x in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#EDF3EF')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#CEDCD5'))]))
    return t
out=R/'output/pdf/PetSafe_completion_status.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=32,leftMargin=32,topMargin=30,bottomMargin=32,title=f'PetSafe {m["revision"]} - complete schematic status',author='PetSafe PCB reverse-engineering project')
W=A4[0]-64
story=[P('What remains to finish','TitlePS'),P(f'PetSafe 100-1339 R03 A | {m["revision"]} | 8 October 2026'),
P('<b>All 150 catalog entries are drawn on one KiCad sheet.</b> This includes empty options and test pads. The drawing is structurally complete; hidden wiring, candidate identities and component values still need evidence.'),
table([['Drawing / libraries','Electrical gaps','Packages / values'],['1 A2 sheet; 20 stock + 4 authorized custom symbol definitions; no missing library files for selected candidates.',f'{len(m["unresolved_pins"])} open pads = {counts["populated"]} populated-entry pads + {counts["DNP"]} DNP pads. {len(gpios)} GPIO pads open.','147/150 footprints; 44 capacitor values and 2 magnetic-part values unknown.']],[W/3]*3),
P('What your via review changed','HeadPS'),
P('101 IDs reviewed; 26 unmentioned, some photo-matched. V033/V050 rejected, leaving 125 active sites. Latest: V017 joins R42.1/R44.1; R43.2 belongs to V015, not V011-V014; V072-to-R22.2 withdrawn; V073 is GND only. Prior supply, tuning-ground and RC1/VREF corrections remain. Motor VDD stays separate from regulated board VDD.'),
table([['Remaining area','What is missing','How to resolve']]+gaps,[87,257,W-344]),
P('Remaining conflicts for later review','HeadPS'),
P('<b>Resolved:</b> V025=GND, V026=PIC21/RB0, V073=GND only. R19/V075 remains photo-derived. <b>V113/V115:</b> GND reports conflict with the apparent Q8 output connection; those merges remain held. The latest batch adds no resistance or functional measurements.'),
P(f'<b>Validation:</b> KiCad 10.0.5 exports pass; {v["proposed_net_partitions"]} modeled nets match the native file. {v["erc_total"]} ERC findings remain: 37 open pins, 10 isolated labels, 5 power and 3 input drive findings. This checks the file, not hardware correctness. No artificial NC or power flags were added.'),PageBreak(),
P('PIC connections: complete picture','TitlePS'),P('Physical package pins, top view. Use the separate numbered close-up to locate them. OPEN means no modeled pad connection; a local connection can still have an unknown onward destination.'),
table([['Pin','Function','State','Local destination / evidence']]+[[p['pin'],{27:'RB6/CLK',28:'RB7/DAT'}.get(p['pin'],p['gpio']),'OPEN' if p['open_pad'] else 'Local net',p['evidence']] for p in pins],[30,64,52,W-146]),
P('Every remaining open pad','HeadPS'),
P('<b>Populated entries (18):</b> '+escape(', '.join(fitted))+'.<br/><b>Empty options (19):</b> '+escape(', '.join(dnp))+'.','SmallPS'),
Spacer(1,6),P('Pad names above are photo-model names; U6.L1/L2 map to its internal NC pins 4/5. DNP pads do not block understanding of the fitted circuit. Vias with a component association do not automatically prove a connection to every other pad on a previously inferred net.','SmallPS'),
Spacer(1,6),P('Evidence: user via review and supplied MX512H diagram; original front/rear photographs; reconstruction.json, via_audit.json, v09_net_changes.json, v091_net_changes.json and native KiCad validation. Pin names follow the existing Microchip datasheet audit. The via viewer retains reports and conflicts.','SmallPS')]
def footer(c,d):
    c.setFillColor(ink);c.setFont('Helvetica',8);c.drawString(32,17,'PetSafe | Evidence-qualified reconstruction | '+m['revision']);c.drawRightString(A4[0]-32,17,str(d.page))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
