"""Number real PIC pads on an untouched user photo and list unresolved GPIOs."""
from pathlib import Path
import csv, hashlib, json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

R=Path(__file__).resolve().parents[1]
PHOTO=R/'photos/user/2026-10-08/pic_closeup.png'
OUT=R/'output/pdf/PetSafe_PIC_GPIO_pin_map.pdf'
SOURCE='https://ww1.microchip.com/downloads/en/DeviceDoc/40001802G.pdf'
audit=json.loads((R/'evidence/pic_trace_audit.json').read_text())
model=json.loads((R/'evidence/reconstruction.json').read_text())
pins={p['pin']:p for p in audit['pins']}
missing=sorted(int(ep.split('.')[1]) for ep in model['unresolved_pins'] if ep.startswith('U4.'))
assert all(1 <= n <= 28 for n in missing)
user=json.loads((R/'evidence/pic_gpio_user_mapping.json').read_text())
reported={p['pin']:p for p in user['pins']}
# Coordinates are on the 1469 x 1958 original, not its resized chat preview.
left_y=[84,128,173,217,260,304,348,392,437,480,525,570,614,659]
right_y=[65,111,154,199,245,290,335,380,425,471,516,562,608,653]
xy={n:[452,y] for n,y in zip(range(15,29),left_y)}
xy.update({n:[833,y] for n,y in zip(range(14,0,-1),right_y)})
rows=[]
for n in missing:
 rows.append(dict(pin=n,gpio=pins[n]['function'],photo_side='right' if n<=14 else 'left',
   position=('from bottom: '+str(n)) if n<=14 else ('from top: '+str(n-14)),
   destination_reference=reported.get(n,{}).get('via',''),destination_pad_or_pin='onward destination unknown',resistance_ohms='',method='User pin-to-via report; no new numeric reading',notes=reported.get(n,{}).get('user_destination','')))
with (R/'evidence/PIC_GPIO_missing.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
photo_manifest=[]
for p in sorted(PHOTO.parent.glob('*.png')):
 photo_manifest.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,
    sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
request=dict(date='2026-10-08',basis_revision=model['revision'],status='AWAITING_ONWARD_DESTINATIONS',
 source_photos=photo_manifest,annotation_photo=PHOTO.relative_to(R).as_posix(),
 source_pixels=[1469,1958],crop=[320,0,990,725],
 pin_number_source=SOURCE+'#page=4',orientation='Top view; pin-1 dot lower right. Right bottom-to-top 1..14; left top-to-bottom 15..28.',
 missing_gpio_pins=missing,missing_count=len(missing),
 definition='These six GPIOs have user-identified local vias but no modeled onward component connection. They are not unused pins. Other modeled nets may still be partial or inferred.',
 targets=[dict(pin=n,gpio=pins[n]['function'],xy=xy[n]) for n in missing],
 all_pad_targets=[dict(pin=n,function=pins[n]['function'],xy=xy[n],missing=n in missing) for n in range(1,29)],
 reply_format='U4.<pin> -> <component reference> <exact pad/pin> -> <ohms or visual trace>. List every destination found.',
 measurements=rows,
 supplementary_local_nets={str(n):('Direct to TP17; prior onward R13 guess withdrawn' if n==18 else pins[n]['evidence']) for n in [1,2,4,14,18,24,26,27,28]},
 notes=['No guessed destination is presented as a measurement.',
        'All 28 pads are visible in the close-up although the top of the plastic body is cropped.',
        'v0.9.4: six highlighted GPIOs have unknown onward destinations. PIC15/RC4 -> U5.2 INA via V022-V016; PIC16/RC5 -> U5.3 INB via V023-V019 are now resolved. RC1/pin12 reaches VREF/V053 separately.'])
(R/'evidence/pic_gpio_request.json').write_text(json.dumps(request,indent=2)+'\n',encoding='utf-8')

W,H=1191,842
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle(f'PetSafe - {len(missing)} unresolved PIC GPIOs and physical pin map')
c.setAuthor('PetSafe PCB reverse-engineering project')
ink=HexColor('#173C3A');muted=HexColor('#5A706E');accent=HexColor('#BF402E')
gray=HexColor('#EDF1F1');paper=HexColor('#F5F7F5')
def text(x,y,s,size=12,bold=False,color=ink):
 c.setFillColor(color);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def paragraph(x,y,s,width,size=12,leading=17):
 line=''
 for word in s.split():
  new=(line+' '+word).strip()
  if stringWidth(new,'Helvetica',size)>width:
   text(x,y,line,size);y-=leading;line=word
  else:line=new
 if line:text(x,y,line,size);y-=leading
 return y
c.setFillColor(paper);c.rect(0,0,W,H,fill=1,stroke=0)
text(30,798,f'PIC GPIO: {len(missing)} destinations still missing',29,True)
text(30,773,'U4 / PIC16F18855 / 28-pin SOIC | Pin numbers are physical package numbers, not schematic drawing order.',13)
c.setFillColor(accent);c.roundRect(30,739,16,16,3,fill=1,stroke=0)
text(54,742,'Orange = onward destination unknown',12,True)
c.setFillColor(gray);c.setStrokeColor(muted);c.roundRect(352,739,16,16,3,fill=1,stroke=1)
text(376,742,'Grey = already represented, sometimes still inferred',12)

# Embed original PNG bytes with a PDF clipping path. Only vector leaders overlay it.
bx,by=155,169;x1,y1,x2,y2=request['crop'];scale=500/(x2-x1)
dw=(x2-x1)*scale;dh=(y2-y1)*scale
im=ImageReader(str(PHOTO));iw,ih=im.getSize();assert (iw,ih)==(1469,1958)
c.saveState();p=c.beginPath();p.rect(bx,by,dw,dh);c.clipPath(p,stroke=0,fill=0)
c.drawImage(im,bx-x1*scale,by-(ih-y2)*scale,iw*scale,ih*scale)
c.restoreState()
def transform(pt):return bx+(pt[0]-x1)*scale,by+dh-(pt[1]-y1)*scale
short={1:'RE3/MCLR',9:'RA7/OSC1',10:'RA6/OSC2',27:'RB6/CLK',28:'RB7/DAT'}
for n in range(1,29):
 x,y=transform(xy[n]);is_missing=n in missing
 lx=30 if n>=15 else 671;lw=113
 end=lx+lw if n>=15 else lx
 c.setLineWidth(3.4);c.setStrokeColor(white);c.line(end,y,x,y)
 c.setLineWidth(1.3 if is_missing else .7);c.setStrokeColor(accent if is_missing else muted);c.line(end,y,x,y)
 c.setFillColor(accent if is_missing else gray);c.setStrokeColor(white)
 c.circle(x,y,3.3 if is_missing else 2.5,fill=1,stroke=1)
 c.setFillColor(accent if is_missing else gray);c.roundRect(lx,y-10,lw,20,4,fill=1,stroke=0)
 text(lx+8,y-4,f'{n:02d}   {short.get(n,pins[n]["function"])}',11,True,white if is_missing else ink)

dx,dy=transform([723,616]);c.setStrokeColor(HexColor('#3DB9E9'));c.setLineWidth(1.7);c.circle(dx,dy,14,stroke=1,fill=0)
text(30,143,'Orientation: pin 1 is at the lower right, beside the round moulded dot (blue ring).',12,True)
text(30,124,'Right row: bottom to top 1-14. Left row: top to bottom 15-28. Do not mirror the image.',12)

tx=815;tw=346
text(tx,705,'Connection checklist',20,True)
text(tx,684,'Six local vias known; onward destinations missing.',10)
c.setFillColor(ink);c.rect(tx,651,tw,23,fill=1,stroke=0)
text(tx+8,658,'Pin',11,True,white);text(tx+46,658,'GPIO',11,True,white);text(tx+100,658,'Current observation',11,True,white)
for i,r in enumerate(rows):
 y=651-(i+1)*29
 c.setFillColor(white if i%2==0 else HexColor('#E9EFEC'));c.rect(tx,y,tw,29,fill=1,stroke=0)
 text(tx+9,y+10,str(r['pin']),13,True,accent);text(tx+47,y+10,r['gpio'],12,True)
 c.setStrokeColor(HexColor('#B2C1BC'));c.setLineWidth(.45);c.line(tx+102,y+7,tx+tw-8,y+7)
 text(tx+102,y+11,(reported[r['pin']]['via']+'; onward unknown'),10)
y=420
y=paragraph(tx,y,'Motor controls resolved: 15/RC4 -> U5.2 INA (V022-V016); 16/RC5 -> U5.3 INB (V023-V019). User-reported connections.',tw,11,15)
y=paragraph(tx,y,'User meter + visual trace: 3-R28/R29/TP7; 17-R13; 22-TP2; 23-TP1; 25-TP4. 26-TP10 corroborated. Numerical ohms not supplied.',tw,11,15)
y=paragraph(tx,y-4,'12: VREF/V053 | 2: C25 | 4: C39 | 14: TP11 | 18: TP17 | 24: R4 | 26: TP10/R35 | 27/28: ICSP nodes.',tw,11,15)
paragraph(tx,y-5,'These are not included in the orange pins. No visible route is not proof of NC. No no-connect flags were added. RP7 wording interpreted as photographed TP7.',tw,10,14)

c.setStrokeColor(HexColor('#C2D1CB'));c.line(30,108,1161,108)
text(30,87,'Unpowered checks: disconnect battery and programmer. Compare low readings with your shorted-probe baseline (about 0.5 ohm).',12,True)
text(30,67,'Reply example: U4.3 -> Rxx, left pad -> 0.7 ohm. A visual trace is useful too. Give exact pads and actual ohms, rather than only a beep.',11)
text(30,48,'Orange lines are callout leaders, not traced copper. Source: your new close-up; original photograph pixels retained.',10,color=muted)
text(30,27,'Pinout: Microchip DS40001802G, page 4. Current schematic: v0.9.4. Date: 2026-10-08. Full details: evidence/pic_gpio_request.json.',10,color=muted)
c.linkURL(SOURCE+'#page=4',(30,23,290,38),relative=0)
c.showPage();c.save()
print(f'{OUT}: 1 page, {len(missing)} unresolved GPIOs, all 28 physical pads numbered')
