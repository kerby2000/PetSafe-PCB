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
local={1:'J1.1/VPP at square-pad end; position photo-supported; D6 route missing',2:'C25 signal pad / V031; onward destination unknown',3:'R28 + R29 + TP7; user meter / visible trace',4:'VREF TP via V035; user confirms via-to-TP; C39.1 local photo route',
5:'V036-V108 to R14; user continuity report',6:'V037-V102 to R15; user continuity report',7:'V039-V097 to R16; user continuity report',8:'GND / V041 photo anchor',9:'Y1 oscillator; photo-derived',10:'Y1 oscillator; photo-derived',
11:'V047-V091 to R11; user continuity report',12:'R18.1 via V053-V070; user-confirmed; VREF link explicitly rejected',13:'TP3 via V049; user-confirmed; existing R10 branch photo-derived',14:'TP11; visible route; onward destination unknown',
15:'V022-V016 to U5 pin2 / INA; user-confirmed',16:'V023-V019 to U5 pin3 / INB; user-confirmed',17:'R13; user meter / visible trace',18:'TP17; visible route; old R13 guess withdrawn',19:'GND / C32 / V045 photo anchor',20:'V042 to board VDD TP user-confirmed; C32.1 local photo route',
21:'VREF (TP104), V026 and V071/R21.2; user-confirmed',22:'TP2 / R31; user meter / visible trace',23:'TP1 / R30; user meter / visible trace',24:'R4; photo-derived; sensing role remains inferred',25:'TP4 / V017 / R42.1 / R44.1; user continuity; C41 photo-derived',26:'TP10 / R35; user meter / visible trace',27:'ICSP CLK / D4 / R32; photo-derived',28:'ICSP DAT / D5 / R40; photo-derived'}
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
story=[P('Schematic completion status','TitlePS'),P(f'PetSafe 100-1339 R03 A | {m["revision"]} | {status["date"]}'),
P('<b>All catalog entries are drawn on one sheet.</b> The remaining questions are listed explicitly below. This is a partially verified reconstruction, not a completed hardware validation or a routed PCB.'),
table([['Coverage','Open connections','Values / packages'],[f'{status["catalog_entries"]} entries; 1 A2 sheet; 20 stock + 4 custom symbol definitions.',f'{len(fitted)} populated-entry pads + {len(dnp)} DNP pads. {len(gpios)} open PIC pads in the model.',f'{len(status["unknown_ceramic_values"])} ceramic and {len(status["unknown_magnetic_values"])} magnetic values unknown; {status["footprints"]["assigned"]}/{status["catalog_entries"]} footprints assigned.']],[W/3]*3),
P('Power rails - current names','HeadPS'),table([['Name','Known path']]+[[r['name'],r['path']] for r in status['rails']],[80,W-80]),
P('L1/L2 share the VSYS supply side. Their opposite ends are not shorted together. H_RF_VDD, H_LDO_IN, H_RX_VDD and H_PIR_VDD describe local branches; these are not additional confirmed independent supplies. Rail voltages have not been measured.'),
P('Recommended next checks','HeadPS'),P('1. D3 rails resolved; next U3.5 DC-bias return, preserving separation across C18.<br/>2. J3 ground/signal and one complete Q3/C10/C11/C12 tuning cell.<br/>3. Specific R41, RF excitation and receiver-output destinations.<br/>4. After routing: frequency-sensitive values and one powered idle/scan session; footprints follow.'),
P('Validation and limits','HeadPS'),P(f'{v["proposed_net_partitions"]} modeled net partitions match KiCad 10.0.5. ERC retains {v["erc_total"]} findings: {v["erc_by_type"].get("pin_not_connected",0)} open pins, {v["erc_by_type"].get("isolated_pin_label",0)} isolated labels and {v["erc_by_type"].get("power_pin_not_driven",0)} undriven power checks. No artificial NC/power flags hide gaps. Original photo hashes are unchanged. This proves file consistency, not all physical connections.'),
P('Isolated modeled nodes: '+escape(', '.join(n['net'] for n in m['nets'] if len(n['endpoints'])==1))+'. A PIC pin can have a local net and still lack an onward destination.'),
P('Completion milestones','HeadPS')]+[P('<b>'+escape(i['name'])+':</b> '+escape(i['criterion'])) for i in status['milestones']]+[PageBreak()]
for title,ids in [('Supply and diode gaps',['E01','E02','E03']),('Tuning and local endpoints',['E04','E05','E06']),('Other routing and identity gaps',['E07','E08','E09','E10','I01','I02']),('Values, mechanics and scope',['V01','M01','D01','F01'])]:
    story.append(P(title,'TitlePS'))
    for i in status['items']:
        if i['id'] not in ids:continue
        story.append(KeepTogether([P(escape(i['id']+' - '+i['area']),'HeadPS'),P('<b>Known:</b> '+escape(i['known'])),P('<b>Uncertain:</b> '+escape(i['unknown'])),P('<b>Next:</b> '+escape(i['next_action']))]))
    if 'V01' in ids:
        story.extend([P('Every unrecovered ceramic value','HeadPS'),P(escape(', '.join(status['unknown_ceramic_values']))),P('C5 is already 470 uF / 16 V. In-circuit LCR readings may include parallel components and semiconductor paths; record frequency, mode and whether a lead was isolated. Geometry cannot establish capacitance, dielectric or voltage rating.')])
        if status['closed_items']:
            story.append(P('Closed issues retained as history','HeadPS'))
            story.extend(P(escape(i['id']+' - '+i['resolution']['result'])) for i in status['closed_items'])
    story.append(PageBreak())
story.extend([P('PIC connections','TitlePS'),P('Physical package pins. All have modeled local nets; the evidence column distinguishes confirmed endpoints from photo-derived or incomplete branches. Use the separate numbered photo guide for physical locations.'),
table([['Pin','Function','Local destination / evidence']]+[[p['pin'],{27:'RB6/CLK',28:'RB7/DAT'}.get(p['pin'],p['gpio']),p['evidence']] for p in pins],[30,64,W-94]),
P('Every remaining open pad','HeadPS'),P('<b>Populated entries:</b> '+escape(', '.join(fitted))+'.<br/><b>Empty options:</b> '+escape(', '.join(dnp))+'.','SmallPS'),
P('U6.L1/L2 are candidate internal NC pins 4/5; external ties remain unknown. Photo pad S means single pad, not necessarily source. Current completion checklist includes closure criteria and the full per-component audit. Sources: reconstruction.json, remaining_work.json, via_audit.json, v099_net_changes.json, native validation and the preserved earlier measurement records.','SmallPS')])
def footer(c,d):
    c.setFillColor(ink);c.setFont('Helvetica',8);c.drawString(32,17,'PetSafe | Evidence-qualified reconstruction | '+m['revision']);c.drawRightString(A4[0]-32,17,str(d.page))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
