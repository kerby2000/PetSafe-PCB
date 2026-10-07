from pathlib import Path
import cv2,numpy as np,json
PROJECT=Path(__file__).resolve().parents[1]; R=PROJECT/'photos/originals'; O=PROJECT/'photos'; cv2.setNumThreads(4)
files=[f'IMG_{n}.jpg' for n in range(2439,2444)]
imgs=[cv2.rotate(cv2.imread(str(R/f)),cv2.ROTATE_90_COUNTERCLOCKWISE) for f in files]
s=cv2.SIFT_create(nfeatures=14000,contrastThreshold=.01); fs=[s.detectAndCompute(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),None) for im in imgs]; bm=cv2.BFMatcher()
T=[np.eye(3)]; rec=[]
for i in range(1,len(files)):
 k,d=fs[i]; K,D=fs[i-1]; good=[m for m,n in bm.knnMatch(d,D,k=2) if m.distance<.72*n.distance]
 p=np.float32([k[m.queryIdx].pt for m in good]); q=np.float32([K[m.trainIdx].pt for m in good]); H,msk=cv2.findHomography(p,q,cv2.USAC_MAGSAC,3)
 if H is None or int(msk.sum())<12: raise RuntimeError(f'Cannot match {files[i]}: {0 if msk is None else msk.sum()}')
 T.append(T[-1]@H); err=np.linalg.norm(cv2.perspectiveTransform(p.reshape(-1,1,2),H).reshape(-1,2)-q,axis=1)[msk.ravel().astype(bool)]
 rec.append({'file':files[i],'matched_to':files[i-1],'inliers':int(msk.sum()),'median_error_px':float(np.median(err))})
 print(rec[-1],flush=True)
pts=[]
for a,t in zip(imgs,T):
 h,w=a.shape[:2]; pts.extend(cv2.perspectiveTransform(np.float32([[[0,0],[w,0],[w,h],[0,h]]]),t)[0])
pts=np.array(pts); lo=np.floor(pts.min(0)); hi=np.ceil(pts.max(0)); sz=np.int32(hi-lo)
shift=np.array([[1,0,-lo[0]],[0,1,-lo[1]],[0,0,1.]])
# Bound memory. Photograph-only mosaic; final rectification occurs separately.
scale=min(1,12000/sz[0],4000/sz[1]); S=np.diag([scale,scale,1]); ww,hh=np.ceil(sz*scale).astype(int)
out=np.full((hh,ww,3),235,np.uint8); scores=np.zeros((hh,ww),np.float32); ids=np.full((hh,ww),255,np.uint8)
trans=[]
for i,(a,t) in enumerate(zip(imgs,T)):
 h,w=a.shape[:2]; yy,xx=np.indices((h,w)); d=np.minimum.reduce([xx,yy,w-1-xx,h-1-yy]).astype(np.float32); d=np.minimum(d/200,1)
 x=S@shift@t; trans.append(x)
 v=cv2.warpPerspective(a,x,(ww,hh)); ds=cv2.warpPerspective(d,x,(ww,hh)); take=ds>scores; out[take]=v[take]; scores[take]=ds[take]; ids[take]=i
cv2.imwrite(str(O/'back_unrectified.png'),out); cv2.imwrite(str(O/'back_source_ids_unrectified.png'),ids)
cv2.imwrite(str(O/'back_unrectified_preview.jpg'),cv2.resize(out,(2400,round(2400*hh/ww))))
json.dump({'files':files,'sources_rotated_90ccw':True,'transforms_to_canvas':[x.tolist() for x in trans],'registration':rec,'width':int(ww),'height':int(hh)},open(O/'back_registration.json','w'),indent=2)
print('BACK COMPLETE',ww,hh,flush=True)
