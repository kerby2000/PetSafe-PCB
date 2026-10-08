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
c.setTitle('PetSafe - four next via-pair checks');c.setAuthor('PetSafe PCB reverse engineering')
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
text(32,800,'Four next checks after your results',29,True)
text(32,774,'Controls and V064-V063 confirmed. V053-V071 rejected. V090 to V095/V100/V103/V107: all OL.',13)
para(32,742,'Battery and programmer disconnected. Report actual resistance, OL or changing. Compare near-zero readings with your probe/contact baseline and reverse probes to check. A beep alone is not proof of a direct connection.',1120,12,17)
cols=[32,106,226,358,827];top=683;rh=29
c.setFillColor(ink);c.rect(32,top-29,1126,29,fill=1,stroke=0)
for x,t in zip(cols,['Test','Fixed probe','Moving probe','What this tests','Reading / reversed if low']):text(x+7,top-20,t,11,True,white)
reasons={'C5':'C43/C44 junction to C16/C29 junction','C6':'C43/C44 junction to C13/C14 junction','C7':'C43/C44 junction to C10/C11 junction','B3':'Regulated VDD to R18 receiver feed','C1':'C46/C47 junction to C43/C44 junction','C2':'C46/C47 junction to C16/C29 junction','C3':'C46/C47 junction to C13/C14 junction','C4':'C46/C47 junction to C10/C11 junction'}
for i,t in enumerate(p['tests']):
 y=top-29-(i+1)*rh;c.setFillColor(white if i%2==0 else gray);c.rect(32,y,1126,rh,fill=1,stroke=0)
 for x,s in zip(cols,[t['id'],t['left'],t['right'],reasons[t['id']],'________________________']):text(x+7,y+10,s,11)
text(32,479,'B3  Is the receiver feed also on regulated VDD?',16,True,teal)
text(545,479,'C5-C7  Do the other four junctions share a node?',16,True,teal)
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
photo([4950,250,6770,1430],(32,135,475,315),['V064','V070'],{'V064':[5620,460],'V070':[6500,530]})
photo([8020,1150,9560,1810],(545,171,610,270),['V095','V100','V103','V107'],{'V090':[8230,1270],'V095':[8510,1690],'V100':[8800,1270],'V103':[9080,1690],'V107':[9340,1270]})
para(545,145,'Keep one probe on V095 for all three new C readings. If all are OL, stop broad pairwise testing; we will trace toward antenna/component endpoints instead.',610,12,17)
para(32,104,'Photographs: rear mosaic already mirrored to match the front. Circles mark vias; leaders are annotations, not traces. Use the paired photo locator for zoomed views. Near-zero can also include an inductor or zero-ohm link.',1120,11,16)
text(32,43,'Next: choose antenna/group tests and remaining RC2/RB0 candidates from these results. Q1 VDD rail choice is still pending.',11,True,teal)
text(32,20,f"PetSafe | 8 October 2026 | Basis {p['basis_revision']} | Proposed pairs only; no unmeasured connection added",9)
c.showPage();c.save()
print('Built paired photo locator and '+p['pdf_path']+' (1 page).')
