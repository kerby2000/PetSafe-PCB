"""Current board-wide completion picture; native connectivity is not proof of hardware."""
from pathlib import Path
from collections import Counter
import json,csv
from current_state import current_state
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
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
local={1:'J1.1/VPP plus D6 cathode; D6 W-VPP 1 ohm, forward 0.7V from GND',2:'C25 signal pad / V031; onward destination unknown',3:'C26 signal pad (user annotation); R28 + R29 + TP7 (earlier meter/trace)',4:'VREF TP via V035; user confirms via-to-TP; C39.1 local photo route',
5:'V036-V108 to R14; user continuity report',6:'V037-V102 to R15; user continuity report',7:'V039-V097 to R16; user continuity report',8:'GND / V041 photo anchor',9:'Y1 oscillator; photo-derived',10:'Y1 oscillator; photo-derived',
11:'V047-V091 to R11; user continuity report',12:'R18.1 via V053-V070; user-confirmed; VREF link explicitly rejected',13:'TP3 via V049 (user); R10/R6/R7/D1 midpoint from IMG_2431; excitation waveform unmeasured',14:'TP11; visible route; onward destination unknown',
15:'V022-V016 to U5 pin2 / INA; user-confirmed',16:'V023-V019 to U5 pin3 / INB; user-confirmed',17:'R13; user meter / visible trace',18:'TP17; visible route; old R13 guess withdrawn',19:'GND / C32 / V045 photo anchor',20:'V042 to board VDD TP user-confirmed; C32.1 local photo route',
21:'TP16/Q2.S; user correction. Old VREF join rejected; TP16-VREF 800 kohm',22:'TP2 / R31 / green LED branch; user meter, visible trace and B42 colour',23:'TP1 / R30 / red LED branch; user meter, visible trace and B43 colour',24:'R4; photo-derived; sensing role remains inferred',25:'TP4 / V017 / R42.1 / R44.1; user continuity; C41 photo-derived',26:'TP10 / R35; user meter / visible trace',27:'ICSP CLK / D4 / R32; photo-derived',28:'ICSP DAT / D5 / R40; photo-derived'}
pins=[dict(pin=n,gpio=func[n],net=member.get(f'U4.{n}'),open_pad=n in gpios,evidence=local[n]) for n in range(1,29)]
status=current_state()
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
audit=read('evidence/finalization_audit.json')
story=[P('Remaining schematic work','TitlePS'),P(f'PetSafe 100-1339 | {m["revision"]} | {status["date"]}'),
P(f'<b>{len(status["items"])} active issues.</b> Completed steps are archived, not bench requests. S1 electrical contacts are verified; E05 is closed. Q3 stays fitted with identification deferred. LED colours are recorded: R30/PIC23 red; R31/PIC22 green. Package mapping remains separate.'),
table([['Drawing / connectivity','Remaining data','ERC'],[f'{len(fitted)} fitted open pads; {len(gpios)} open PIC pads; {audit["dangling_wire_ends"]} dangling wire ends. {len(m["nets"])} native/model net partitions match.',f'{len(status["unknown_ceramic_values"])} ceramic values; LED1 footprint blank. Three local-only PIC branches remain explicit; unsupported R33 withdrawn.',f'{status["erc_total"]} retained U6/U6A output conflict. Five stock power-source flags retained; no new copper joins.']],[W/3]*3),
P('Audit boundary','HeadPS'),P('Native wire geometry, library definitions, all catalog pad assignments and existing evidence were checked. Zero open pads does not establish hidden copper or functional behavior. U6A is DNP; its regulator symbol and visible conflict remain by user choice. No new NC markers, net merges or ERC exclusions.'),
P('Order of work','HeadPS')]
for group in status['finish_plan']:
    story.append(P('<b>'+escape(group['title'])+':</b> '+escape(group['summary'])+' '+escape(group['next_action'])))
story.append(PageBreak())
for group in status['finish_plan']:
    story.append(P(escape(group['title']),'TitlePS'))
    for i in status['items']:
        if i['id'] not in group['issues']:continue
        story.append(KeepTogether([P(escape(i['id']+' - '+i['area']),'HeadPS'),P('<b>Established:</b> '+escape(i['known'])),P('<b>Remaining:</b> '+escape(i['unknown'])),P('<b>Next:</b> '+escape(i['next_action'])),P('<b>Close when:</b> '+escape(i['closed_when']))]))
    if 'V01' in group['issues']:
        story.extend([P('All unrecovered ceramic values','HeadPS'),P(escape(', '.join(status['unknown_ceramic_values'])))])
    story.append(PageBreak())
story.extend([P('Scope and sources','TitlePS'),P(escape(read('evidence/remaining_work.json')['scope_note'])),P(escape(read('evidence/remaining_work.json')['accepted_option_limitations'])),P('All previous issue dispositions: evidence/finalization_review_v0931.json. Native geometry and uncertainty coverage: evidence/finalization_audit.json. Current register: evidence/remaining_work.json. Archived observations and old checklists: docs/history/README.md.'),P('Power-source flags describe supply paths through existing passive components; they do not prove voltage or transistor operation. Installed KiCad 10 libraries and project symbols match the embedded pin/graphic definitions. GUI library reload has not been verified.'),P('Reference rails','HeadPS'),table([['Rail','Existing modeled path']]+[[r['name'],r['path']] for r in status['rails']],[75,W-75])])

def footer(c,d):
    c.setFillColor(ink);c.setFont('Helvetica',8);c.drawString(32,17,'PetSafe | Evidence-qualified reconstruction | '+m['revision']);c.drawRightString(A4[0]-32,17,str(d.page))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
