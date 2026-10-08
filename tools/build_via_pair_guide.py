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
c.setTitle('PetSafe - recovered RC1 receiver control route');c.setAuthor('PetSafe PCB reverse engineering')
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
text(32,800,'Confirmed: RC1 reaches R18 via V053-V070',29,True)
text(32,774,'PIC12/RC1 -> V053 -> V070 -> R18.1. V053-VREF explicitly rejected; RB0/VREF stays separate.',13)
para(32,742,'Recorded from your continuity report; no numerical ohms supplied. This page now locates the completed connection. No repeat measurement requested. V067 also reaches J3 pin 1/red wire, on H_PIR_VDD.',1120,12,17)
cols=[32,106,226,358,827];top=683;rh=29
c.setFillColor(ink);c.rect(32,top-29,1126,29,fill=1,stroke=0)
for x,t in zip(cols,['Test','Fixed probe','Moving probe','What this tests','Recorded result']):text(x+7,top-20,t,11,True,white)
reasons={'F1':'PIC12/RC1 to R18.1 control input','C5':'C43/C44 junction to C16/C29 junction','C6':'C43/C44 junction to C13/C14 junction','C7':'C43/C44 junction to C10/C11 junction','D2':'R18 input to PIC21/RB0 (unmeasured candidate)','C1':'C46/C47 junction to C43/C44 junction','C2':'C46/C47 junction to C16/C29 junction','C3':'C46/C47 junction to C13/C14 junction','C4':'C46/C47 junction to C10/C11 junction'}
for i,t in enumerate(p['tests']):
 y=top-29-(i+1)*rh;c.setFillColor(white if i%2==0 else gray);c.rect(32,y,1126,rh,fill=1,stroke=0)
 for x,s in zip(cols,[t['id'],t['left'],t['right'],reasons[t['id']],'Connected (user checked)']):text(x+7,y+10,s,11)
para(32,593,'What this resolves: RC1 supplies the R18 control input in the reconstructed circuit. The earlier photo-only RC1-to-VREF link was wrong and is withdrawn. RC2 now reaches TP3; RB0 reaches VREF (native TP104). All PIC pads have modeled local destinations; other circuit gaps remain.',1120,13,19)
text(32,486,'A - V053: PIC pin 12 / RC1',16,True,teal)
text(614,486,'B - V070: R18 control input',16,True,teal)
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
photo([4000,1230,5120,2150],(32,165,535,295),['V053'],{'V053':[4840,1470]})
photo([6040,270,7180,1190],(614,165,535,295),['V070'],{'V070':[6280,440]})
para(32,141,'Evidence limits: V053-V070 is user-confirmed. The existing local V070-to-R18.1 pad association is retained. Q7/R19 base-emitter topology remains a photo/resistance-supported reconstruction, not a powered functional test.',1120,12,17)
para(32,89,'Rear mosaic is already mirrored to match the front. Circles mark vias; leaders are annotations, not traces. Use board landmarks and the paired photo locator to zoom. The completed V064-V070 reading is resistive, not direct continuity.',1120,11,16)
text(32,39,'No GPIO batch pending. Remaining work includes other hidden continuations, candidate identities, values and package geometry.',11,True,teal)
text(32,19,f"PetSafe | 8 October 2026 | Basis {p['basis_revision']} | Completed result locator | V053-V070 confirmed; V053-VREF rejected",9)
c.showPage();c.save()
print('Built paired photo locator and '+p['pdf_path']+' (1 page).')
