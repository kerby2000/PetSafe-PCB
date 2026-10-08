"""Vector callouts over untouched source photographs; no synthesized PCB detail."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

R=Path(__file__).resolve().parents[1]
OUT=R/'output/pdf/PetSafe_measurement_round1.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=842,595
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('PetSafe: targeted unpowered measurements')
ink=HexColor('#193C3A');accent=HexColor('#D33C69')
def txt(x,y,s,size=11,bold=False,color=ink):
    c.setFillColor(color);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width=280,size=11):
    words=s.split();line=''
    for word in words:
        trial=(line+' '+word).strip()
        if stringWidth(trial,'Helvetica',size)>width:
            txt(x,y,line,size);y-=size*1.4;line=word
        else:line=trial
    if line:txt(x,y,line,size);y-=size*1.4
    return y
def photo(source,box,rect,points):
    bx,by,bw,bh=rect;x1,y1,x2,y2=box
    image=ImageReader(str(R/source));iw,ih=image.getSize()
    scale=min(bw/(x2-x1),bh/(y2-y1));dw=(x2-x1)*scale;dh=(y2-y1)*scale
    def tr(p):return bx+(p[0]-x1)*scale,by+dh-(p[1]-y1)*scale
    c.saveState();path=c.beginPath();path.rect(bx,by,dw,dh);c.clipPath(path,stroke=0,fill=0)
    c.drawImage(image,bx-x1*scale,by-(ih-y2)*scale,iw*scale,ih*scale)
    c.restoreState()
    for label,d in points.items():
        x,y=tr(d['point']);lx,ly=tr(d['label'])
        c.setLineWidth(3);c.setStrokeColor(white);c.line(lx,ly,x,y)
        c.setLineWidth(1.3);c.setStrokeColor(accent);c.line(lx,ly,x,y)
        c.setLineWidth(2);c.setStrokeColor(white);c.circle(x,y,5,stroke=1,fill=0)
        c.setFillColor(accent);c.setStrokeColor(white);c.circle(lx,ly,10,stroke=1,fill=1)
        c.setFillColor(white);c.setFont('Helvetica-Bold',11);c.drawCentredString(lx,ly-4,label)
    return dw,dh
def header(title,sub):
    c.setFillColor(HexColor('#F4F7F5'));c.rect(0,0,W,H,fill=1,stroke=0)
    txt(30,554,title,23,True);txt(30,531,sub,11)
    txt(30,27,'Original photo pixels; vector callouts only. Board orientation is unchanged. Candidate identities are unconfirmed.',9)
    txt(30,12,'PetSafe 100-1339 R03 A | 2026-10-08 | v0.5 measurement plan',8)
pages=[
 {'id':'U6','source':'photos/originals/IMG_2435.jpg','crop':[300,1030,1320,1850],
  'points':{'A':{'point':[1025,1248],'label':[1180,1220]},'B':{'point':[1025,1305],'label':[1180,1320]},'C':{'point':[1025,1357],'label':[1170,1420]},'G':{'point':[404,1720],'label':[540,1800]}},
  'tests':[{'id':'U6-1','from':'G','to':'A'},{'id':'U6-2','from':'G','to':'B'},{'id':'U6-3','from':'G','to':'C'}]},
 {'id':'Q8','source':'photos/originals/IMG_2431.jpg','crop':[280,1040,1130,1930],
  'points':{'D':{'point':[540,1662],'label':[340,1630]},'E':{'point':[698,1662],'label':[770,1720]},'F':{'point':[990,1530],'label':[1040,1370]},'S':{'point':[618,1667],'label':[610,1840]},'P':{'point':[618,1440],'label':[820,1420]}},
  'tests':[{'id':'Q8-1','from':'D','to':'E'},{'id':'Q8-2','from':'E','to':'F'},{'id':'Q8-3','from':'S','to':'G (U6 photo)'},{'id':'Q8-4','from':'F','to':'P'},{'id':'Q8-5','from':'F','to':'G (U6 photo)'}]}
]
header('U6: your measurements recorded','C2NM supports S-812C33AMC, a 3.3 V regulator. Board remains unpowered for resistance tests.')
photo(pages[0]['source'],pages[0]['crop'],(30,105,465,390),pages[0]['points'])
y=492
for s,b in [('Meter setup',True),('Use resistance / ohms. First short the probes together and note the lead resistance.',False),('Keep the black probe on G, the plated hole labelled GND on the PCB. Touch only the circled solder pad with the red probe.',False),('Your readings; shorted tips = 0.5 ohm',True),('G to A = 4.2 kohms (reported)',False),('G to B = 34 kohms (reported)',False),('G to C = 2.7 ohms (reported)',False),('Wait for each reading to settle. Report changing readings too. If unclear, reverse the probes and give both readings.',False),('A beep alone is not enough: a 22-ohm resistor can also trigger continuity. A direct copper connection should be close to your shorted-probe reading.',False)]:
    y=para(525,y,s,285,11 if not b else 12);y-=9
txt(30,78,'A = original R1 / upper-right lead; B = R2 / middle-right; C = R3 / lower-right.',10)
txt(30,61,'S-812C33AMC predicts C = pin 1 / GND, B = pin 2 / VIN, A = pin 3 / VOUT. Ground is supported, not proven.',10)
c.showPage()
header('Q8 and C6: measured results','D-E and S-G read 2 ohms. E-F reads 400 kohms: the proposed direct C6 output tie is withdrawn.')
photo(pages[1]['source'],pages[1]['crop'],(30,85,465,415),pages[1]['points'])
y=492
for s,b in [('Recorded results',True),('D to E = 2 ohms. This supports joined drain pads.',False),('S to G = 2 ohms. This supports the N-channel source returning to ground.',False),('E to F = 400 kohms. F is not directly joined to the output. That proposed wire is removed.',False),('C6 follow-up results',True),('F to P = 10 ohms (reported)',True),('P is Q8\'s upper middle solder pad, the candidate P-channel source / supply. F is the upper end of C6.',False),('F to G = 300 kohms (reported)',True),('G is the same ground hole on page 1. F appears supply-related. The 10-ohm path is not yet established as direct copper.',False),('No more measurements requested in this round. C6.1 remains unresolved; contact or series resistance may explain the F-P reading.',False)]:
    y=para(525,y,s,285,11 if not b else 12);y-=9
txt(30,61,'C6 connection unresolved. The 400-kohm in-circuit result is not a measurement of a discrete resistor.',10)
c.showPage();c.save()
evidence_path=R/'evidence/measurement_plan.json'
previous=json.loads(evidence_path.read_text()) if evidence_path.exists() else {}
previous.update(date='2026-10-08',status='TARGETED_ROUND_COMPLETE_C6_ROUTE_UNRESOLVED',method='Unpowered resistance; compare with shorted-probe reading',photo_callouts=pages)
previous.setdefault('results',[])
evidence_path.write_text(json.dumps(previous,indent=2),encoding='utf-8',newline='\n')
print(OUT)
