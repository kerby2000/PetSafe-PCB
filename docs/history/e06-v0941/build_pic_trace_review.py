"""Photo trace evidence: original pixels, clipped in PDF, with vector endpoint markers."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
R=Path(__file__).resolve().parents[1]
c=canvas.Canvas(str(R/'output/pdf/PetSafe_PIC_trace_review.pdf'),pagesize=(842,595))
c.setTitle('PetSafe PIC photo tracing - v0.7')
ink=HexColor('#193c3a');accent=HexColor('#b62058')
def text(x,y,s,size=11,bold=False):
 c.setFillColor(ink);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width=310,size=11):
 line=''
 for word in s.split():
  trial=(line+' '+word).strip()
  if stringWidth(trial,'Helvetica',size)>width:text(x,y,line,size);y-=15;line=word
  else:line=trial
 if line:text(x,y,line,size);y-=15
 return y
def header(title,subtitle,page):
 c.setFillColor(HexColor('#f3f6f4'));c.rect(0,0,842,595,fill=1,stroke=0)
 text(26,560,title,23,True);text(26,537,subtitle,11)
 text(26,16,f'PetSafe v0.7 | 2026-10-08 | Photo evidence, not continuity verification | Page {page}/2',9)
def photo(source,box,rect,marks=None):
 bx,by,bw,bh=rect;x1,y1,x2,y2=box
 im=ImageReader(str(R/source));iw,ih=im.getSize();s=min(bw/(x2-x1),bh/(y2-y1));dh=(y2-y1)*s
 c.saveState();p=c.beginPath();p.rect(bx,by,(x2-x1)*s,dh);c.clipPath(p,stroke=0,fill=0)
 c.drawImage(im,bx-x1*s,by-(ih-y2)*s,iw*s,ih*s);c.restoreState()
 def tr(p):return bx+(p[0]-x1)*s,by+dh-(p[1]-y1)*s
 for label,points,anchor in marks or []:
  lx,ly=tr(anchor)
  for p in points:
   x,y=tr(p);c.setStrokeColor(white);c.setLineWidth(2.5);c.line(lx,ly,x,y)
   c.setStrokeColor(accent);c.setLineWidth(.8);c.line(lx,ly,x,y)
   c.setStrokeColor(white);c.setLineWidth(1.3);c.circle(x,y,3,stroke=1,fill=0)
  c.setFillColor(accent);c.circle(lx,ly,8,stroke=0,fill=1);c.setFillColor(white);c.setFont('Helvetica-Bold',9);c.drawCentredString(lx,ly-3,label)
header('PIC: connections recovered from existing photos','Callouts mark endpoints; the straight leaders are annotations, not fabricated copper tracks.',1)
marks=[('A',[[350,460],[350,242]],[430,300]),('B',[[816,470],[1095,176]],[970,310]),('C',[[653,460],[653,365],[732,460],[732,365]],[566,283]),('D',[[104,1100],[104,1250]],[152,1370]),('E',[[263,1100],[272,1250]],[385,1370])]
photo('photos/originals/IMG_2436.jpg',(0,0,1180,1430),(26,57,432,461),marks)
y=503
items=[('A - pin 24 / RB3 to R4 lower pad','Direct visible copper. R4 was incorrectly tied to ground; that tie is removed.'),('B - pin 18 / RC7 to TP17','Direct local trace. The lowest top-edge continuation to R13 is probable across overlapping photos; retained as a qualified inference.'),('C - C32 across pins 20 and 19','VDD and VSS respectively. C32 moved from the PIR block to the PIC supply. Its 100 nF value remains an estimate.'),('D - pin 2 / RA0 to C25 right pad','The old VDD connection and generic 100 nF value are withdrawn.'),('E - pin 4 / RA2 to C39 left pad','The old VDD connection and generic 100 nF value are withdrawn.')]
for title,body in items:
 text(455,y,title,12,True);y=para(455,y-18,body,357)-15
para(455,y,'C26: the old VDD tie is also withdrawn. Its signal-side route is still unresolved. Opposite capacitor-pad ground assignments remain hypotheses.',357,10)
c.showPage()
header('Programming lines and the empty option network','The same programming pins may serve other firmware functions during normal operation.',2)
photo('photos/originals/IMG_2437.jpg',(0,120,1469,860),(26,260,475,245))
photo('photos/originals/IMG_2438.jpg',(810,150,1469,655),(26,52,285,200))
y=500
for title,body in [
 ('Pin 27 / RB6 / ICSP clock','The lower pad of D4 and lower pad of R32 join this pin. The earlier R32-to-PIR-supply tie is removed.'),
 ('Pin 28 / RB7 / ICSP data','The lower pad of D5 and upper pad of R40 join this pin. The earlier R40-to-VDD tie is removed.'),
 ('Pin 26 / RB5 to TP10 and R35 upper','Follow the long loop outside D4, across the board edge and below Q9. It joins TP10. R35 lower instead joins Q9 lower-left; the empty resistor separates these nodes.'),
 ('C41 to TP4','The right capacitor pad joins TP4. The continuation disappears under U4, so the previous antenna-net assignment is withdrawn.'),
 ('What a clearer photo would help resolve','Take a straight-down, full-resolution PIC-area shot with both pin rows and nearby parts in focus. Also capture the top-edge tracks toward R11-R16 and LED1 in overlapping close-ups. Keep the actual board edge in frame.')]:
 text(525,y,title,11,True);y=para(525,y-17,body,288,10)-13
para(325,208,'The upper image is IMG_2437; the lower is IMG_2438. Both retain their original pixels and orientation.',176,10)
para(325,133,'Routes under the IC body or into vias may still require a few targeted continuity checks; a sharper photo cannot expose covered copper.',176,10)
c.showPage();c.save()
print('PIC trace review created')
