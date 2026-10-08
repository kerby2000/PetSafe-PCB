"""Build the current paired-photo page and compact remaining-check PDF."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidence/via_pair_plan.json').read_text(encoding='utf-8'))
a=json.loads((R/'evidence/via_audit.json').read_text(encoding='utf-8'));sites={s['id']:s for s in a['sites']}
html=(R/'tools/templates/via_pair_tests.html').read_text(encoding='utf-8').replace('PLAN_DATA',json.dumps(p).replace('</','<\\/')).replace('AUDIT_DATA',json.dumps(a).replace('</','<\\/'))
html=html.replace('SITE_COUNT',str(p['count_basis']['nonrail_candidate_sites'])).replace('GROUP_COUNT',str(p['count_basis']['local_candidate_groups'])).replace('BASIS_REV',p['basis_revision'])
(R/'docs/VIA_PAIR_TESTS.html').write_text(html,encoding='utf-8')
W,H=1191,842;c=canvas.Canvas(str(R/p['pdf_path']),pagesize=(W,H))
c.setTitle('PetSafe - trace the receiver control input');c.setAuthor('PetSafe PCB reverse engineering')
ink=HexColor('#173e35');teal=HexColor('#087767');amber=HexColor('#a34d18');paper=HexColor('#f3f7f3');gray=HexColor('#e3ece5')
def text(x,y,s,size=12,bold=False,color=ink):
 c.setFillColor(color);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width,size=12,lead=17):
 line=''
 for word in s.split():
  trial=(line+' '+word).strip()
  if stringWidth(trial,'Helvetica',size)>width:text(x,y,line,size);y-=lead;line=word
  else:line=trial
 if line:text(x,y,line,size);y-=lead
 return y
c.setFillColor(paper);c.rect(0,0,W,H,fill=1,stroke=0)
text(32,800,'Next check: does RC2 drive the Q7 input?',29,True)
text(32,774,'V064-V070 = 11.2 kohm, matching R18 1.2k + R19 10k. The direct VDD assumption is withdrawn.',13)
para(32,742,'Battery and programmer disconnected. Report actual resistance, OL or changing. Compare near-zero readings with your probe/contact baseline and reverse probes to check. A beep alone is not proof of a direct connection.',1120,12,17)
cols=[32,106,226,358,827];top=683;rh=29
c.setFillColor(ink);c.rect(32,top-29,1126,29,fill=1,stroke=0)
for x,t in zip(cols,['Test','Fixed probe','Moving probe','What this tests','Reading / reversed if low']):text(x+7,top-20,t,11,True,white)
reasons={'C5':'C43/C44 junction to C16/C29 junction','C6':'C43/C44 junction to C13/C14 junction','C7':'C43/C44 junction to C10/C11 junction','D1':'R18 input to PIC13/RC2 (unmeasured candidate)','C1':'C46/C47 junction to C43/C44 junction','C2':'C46/C47 junction to C16/C29 junction','C3':'C46/C47 junction to C13/C14 junction','C4':'C46/C47 junction to C10/C11 junction'}
for i,t in enumerate(p['tests']):
 y=top-29-(i+1)*rh;c.setFillColor(white if i%2==0 else gray);c.rect(32,y,1126,rh,fill=1,stroke=0)
 for x,s in zip(cols,[t['id'],t['left'],t['right'],reasons[t['id']],'________________________']):text(x+7,y+10,s,11)
para(32,593,'Why this pair: the photo and 11.2 kohm reading support R18 as a series input to Q7, with R19 pulling its base toward VDD. RC2 is one of two GPIOs without a mapped destination. This checks a plausible receiver-enable route; it is not a traced or proven connection.',1120,13,19)
text(32,486,'A - V070: R18 control-input candidate',16,True,teal)
text(614,486,'B - V049: PIC pin13 / RC2',16,True,teal)
rear=ImageReader(str(R/p['photos']['rear']));iw,ih=rear.getSize();assert (iw,ih)==(12000,2600)
def photo(box,rect,ids,labels):
 bx,by,bw,bh=rect;x1,y1,x2,y2=box;scale=min(bw/(x2-x1),bh/(y2-y1));dw=(x2-x1)*scale;dh=(y2-y1)*scale
 c.saveState();path=c.beginPath();path.rect(bx,by,dw,dh);c.clipPath(path,stroke=0,fill=0)
 c.drawImage(rear,bx-x1*scale,by-(ih-y2)*scale,iw*scale,ih*scale);c.restoreState()
 def tr(pt):return bx+(pt[0]-x1)*scale,by+dh-(pt[1]-y1)*scale
 for id in ids:
  x,y=tr(sites[id]['rear_xy']);lx,ly=tr(labels[id]);c.setStrokeColor(white);c.setLineWidth(3);c.line(x,y,lx,ly)
  c.setStrokeColor(amber);c.setLineWidth(1.1);c.line(x,y,lx,ly);c.setStrokeColor(white);c.setLineWidth(2);c.circle(x,y,6,stroke=1,fill=0)
  c.setFont('Helvetica-Bold',11);w=stringWidth(id,'Helvetica-Bold',11)+12;c.setFillColor(ink);c.roundRect(lx-w/2,ly-7,w,17,3,fill=1,stroke=0);c.setFillColor(white);c.drawCentredString(lx,ly-2,id)
photo([6040,270,7180,1190],(32,165,535,295),['V070'],{'V070':[6280,440]})
photo([3440,920,4560,1840],(614,165,535,295),['V049'],{'V049':[4270,1160]})
para(32,141,'A near-baseline reading would support RC2 as the control source. If not direct, the next alternative is V070 to V026 (PIC21/RB0). Neither pin is assigned by elimination. Report actual ohms, OL or a changing reading.',1120,12,17)
para(32,89,'Rear mosaic is already mirrored to match the front. Circles mark vias; leaders are annotations, not traces. Use board landmarks and the paired photo locator to zoom. The completed V064-V070 reading is resistive, not direct continuity.',1120,11,16)
text(32,39,'No more capacitor sweeps. Q7 local topology is inferred from photo + resistance; the remote control route is unmeasured.',11,True,teal)
text(32,19,f"PetSafe | 8 October 2026 | Basis {p['basis_revision']} | D1 is proposed only; no GPIO connection added",9)
c.showPage();c.save()
print('Built paired photo locator and '+p['pdf_path']+' (1 page).')
