"""Deterministic photographic registration. No inpainting, synthesis, or content-aware fill."""
from pathlib import Path
import cv2, numpy as np, json, math
PROJECT=Path(__file__).resolve().parents[1]; ROOT=PROJECT/'photos/originals'; OUT=PROJECT/'photos'; OUT.mkdir(parents=True,exist_ok=True)
cv2.setNumThreads(4)
def load(name):
 a=cv2.imread(str(ROOT/name));
 if a is None: raise FileNotFoundError(name)
 return a
# Use original full front as reference. Rotation only; perspective rectification follows.
anchor=cv2.rotate(load('IMG_2419.jpg'),cv2.ROTATE_90_COUNTERCLOCKWISE)
# Corners from the supplied full-board photograph, in its rotated original pixels.
# Preserve a useful reference aspect, not a claim of measured physical dimensions.
s=anchor.shape[1]/933.
corners=np.float32([[42,338],[907,320],[891,507],[68,505]])*s
W,H=12000,2600
rect=cv2.getPerspectiveTransform(corners,np.float32([[0,0],[W-1,0],[W-1,H-1],[0,H-1]]))
files=['IMG_2419.jpg','IMG_2438.jpg','IMG_2437.jpg','IMG_2436.jpg','IMG_2435.jpg','IMG_2434.jpg','IMG_2433.jpg','IMG_2431.jpg','IMG_2432.jpg','IMG_2429.jpg','IMG_2430.jpg']
imgs={f:(anchor if i==0 else load(f)) for i,f in enumerate(files)}
sift=cv2.SIFT_create(nfeatures=14000,contrastThreshold=.016,edgeThreshold=12)
features={}
for f,a in imgs.items():
 g=cv2.cvtColor(a,cv2.COLOR_BGR2GRAY)
 if f==files[0]:
  mask=np.zeros(g.shape,np.uint8); cv2.fillConvexPoly(mask,np.int32(corners),255)
 else: mask=None
 k,d=sift.detectAndCompute(g,mask); features[f]=(k,d)
 print(f,len(k),flush=True)
matcher=cv2.BFMatcher(); edges=[]
for i,f in enumerate(files):
 for j in range(i+1,len(files)):
  g=files[j]; k1,d1=features[g]; k2,d2=features[f]
  good=[a for a,b in matcher.knnMatch(d1,d2,k=2) if a.distance<.70*b.distance]
  if len(good)<12: continue
  p=np.float32([k1[m.queryIdx].pt for m in good]); q=np.float32([k2[m.trainIdx].pt for m in good])
  h,mask=cv2.findHomography(p,q,cv2.USAC_MAGSAC,3.0)
  if h is None: continue
  n=int(mask.sum()); inliers=mask.ravel().astype(bool)
  if n<10 or n<len(good)*.32: continue
  pred=cv2.perspectiveTransform(p.reshape(-1,1,2),h).reshape(-1,2)
  err=float(np.median(np.linalg.norm(pred[inliers]-q[inliers],axis=1)))
  edges.append((f,g,h,n,err)); print('MATCH',f,g,n,round(err,2),flush=True)
# Maximum-weight spanning placement. Paths and image-level residuals retained.
Ts={files[0]:np.eye(3)}; records=[{'file':files[0],'reference':'front reference photograph','transform_to_reference':np.eye(3).tolist()}]
while len(Ts)<len(files):
 options=[]
 for f,g,h,n,e in edges:
  if f in Ts and g not in Ts: options.append((n,f,g,h,e))
  elif g in Ts and f not in Ts: options.append((n,g,f,np.linalg.inv(h),e))
 if not options: break
 n,f,g,h,e=max(options,key=lambda x:x[0]); Ts[g]=Ts[f]@h
 records.append({'file':g,'matched_to':f,'inliers':n,'median_error_px':e,'transform_to_reference':Ts[g].tolist()})
# Piecewise source selection, no cross-fading (avoids creating double edges).
result=cv2.warpPerspective(anchor,rect,(W,H),borderValue=(235,235,235)); score=np.full((H,W),.00001,np.float32)
source_map=np.zeros((H,W),np.uint8)
for idx,f in enumerate(files[1:],1):
 if f not in Ts: continue
 a=imgs[f]; ah,aw=a.shape[:2]; t=rect@Ts[f]
 # Score favouring source resolution, gently reduced near the image edges.
 yy,xx=np.indices((ah,aw)); distance=np.minimum.reduce([xx,yy,aw-1-xx,ah-1-yy]).astype(np.float32)
 fade=np.clip(distance/100.,0,1)
 center=np.array([[[aw/2,ah/2],[aw/2+10,ah/2],[aw/2,ah/2+10]]],np.float32)
 pts=cv2.perspectiveTransform(center,t)[0]
 area=abs(np.linalg.det(np.stack([pts[1]-pts[0],pts[2]-pts[0]])))/100
 quality=1/max(area,1e-5)
 ws=cv2.warpPerspective(fade*quality,t,(W,H)); warped=cv2.warpPerspective(a,t,(W,H),flags=cv2.INTER_LINEAR)
 take=ws>score; result[take]=warped[take]; score[take]=ws[take]; source_map[take]=idx
cv2.imwrite(str(OUT/'front_registered.png'),result)
cv2.imwrite(str(OUT/'front_source_ids.png'),source_map)
cv2.imwrite(str(OUT/'front_preview.jpg'),cv2.resize(result,(2400,520)))
json.dump({'canvas':{'width':W,'height':H,'metric_scale':False},'reference_rectification':rect.tolist(),'sources':files,'registration':records,'not_registered':[f for f in files if f not in Ts]},open(OUT/'front_registration.json','w'),indent=2)
print('FRONT COMPLETE',len(Ts),'of',len(files),flush=True)
