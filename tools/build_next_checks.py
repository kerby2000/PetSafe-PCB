"""Non-destructive photo clipping and vector measurement callouts in ReportLab."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
R=Path(__file__).resolve().parents[1]
out=R/'output/pdf/PetSafe_next_checks.pdf'
c=canvas.Canvas(str(out),pagesize=(842,595));c.setTitle('PetSafe - next measurements: D2, C5 and package scale')
ink=HexColor('#193c3a');accent=HexColor('#b82055')
def text(x,y,s,size=11,bold=False):
    c.setFillColor(ink);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width,size=11):
    line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if stringWidth(trial,'Helvetica',size)>width:text(x,y,line,size);y-=15;line=word
        else:line=trial
    if line:text(x,y,line,size);y-=15
    return y
c.setFillColor(HexColor('#f3f6f4'));c.rect(0,0,842,595,fill=1,stroke=0)
text(28,558,'D2: identify the junction pattern',24,True)
text(28,533,'Battery and programmer disconnected. Use diode-test mode; report volts or OL.',12)
# Clip source photograph; no source pixels retouched or synthesized.
source='photos/originals/IMG_2434.jpg';box=(650,1360,1469,1958);bx,by=28,200;scale=445/(box[2]-box[0]);dh=(box[3]-box[1])*scale
im=ImageReader(str(R/source));iw,ih=im.getSize()
c.saveState();clip=c.beginPath();clip.rect(bx,by,445,dh);c.clipPath(clip,stroke=0,fill=0)
c.drawImage(im,bx-box[0]*scale,by-(ih-box[3])*scale,iw*scale,ih*scale);c.restoreState()
points={'X':{'point':[1110,1710],'label':[1000,1610]},'Y':{'point':[1236,1710],'label':[1370,1610]},'Z':{'point':[1176,1840],'label':[1370,1890]}}
def tr(p):return bx+(p[0]-box[0])*scale,by+dh-(p[1]-box[1])*scale
for label,d in points.items():
    x,y=tr(d['point']);lx,ly=tr(d['label'])
    c.setStrokeColor(white);c.setLineWidth(3);c.line(lx,ly,x,y)
    c.setStrokeColor(accent);c.setLineWidth(1.3);c.line(lx,ly,x,y)
    c.setStrokeColor(white);c.setLineWidth(2);c.circle(x,y,5,stroke=1,fill=0)
    c.setFillColor(accent);c.circle(lx,ly,12,stroke=1,fill=1);c.setFillColor(white);c.setFont('Helvetica-Bold',12);c.drawCentredString(lx,ly-4,label)
text(500,493,'Record these six readings',15,True)
text(500,469,'RED probe     BLACK probe        Reading',11,True)
for i,(a,b) in enumerate([('X','Y'),('Y','X'),('X','Z'),('Z','X'),('Y','Z'),('Z','Y')]):
    y=441-i*29;text(523,y,a,13,True);text(630,y,b,13,True);text(716,y,'________',12)
para(500,246,'X/Y/Z identify physical solder pads only. They do not assume pin numbers or internal functions.',306)
para(28,178,'D2 is the three-terminal part below D3 in this photo. Touch the circled metal pads, not the black body. Report a changing reading too. No desoldering is requested in this round.',445)
para(500,186,'In-circuit results can include other paths. This test narrows the candidates; it does not by itself prove a transistor versus a dual-diode package.',306)
text(28,106,'Two extra observations',14,True)
para(28,83,'C5: read/photo the sleeve value and voltage; report can diameter and lead-centre spacing if accessible. R8: measure body length and width, excluding solder, to check the 0805 estimate.',772)
text(28,29,'PetSafe 100-1339 R03 A | v0.6 | Original photo pixels with vector callouts | 2026-10-08',9)
c.showPage();c.save()
(R/'evidence/next_measurements.json').write_text(json.dumps(dict(revision='v0.6',instruments=['LCR meter','multimeter'],status='AWAITING_READINGS',photo=source,crop=box,points=points,mode='Unpowered diode mode, volts or OL',tests=['red X black Y','red Y black X','red X black Z','red Z black X','red Y black Z','red Z black Y']),indent=2),encoding='utf-8')
print(out)
