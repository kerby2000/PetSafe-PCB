"""Reproduce the approximate cross-side registration using recorded control points.
The reflection aligns corresponding holes; it does not establish electrical nets.
"""
from pathlib import Path
import cv2, numpy as np, json
R=Path(__file__).resolve().parents[1];P=R/'photos'
front=cv2.imread(str(P/'front_registered.png'));back=cv2.imread(str(P/'back_unrectified.png'))
if front is None or back is None:raise FileNotFoundError('Run stitch_evidence.py and stitch_back.py first.')
meta=json.loads((P/'cross_side_alignment.json').read_text())
f=np.float32(meta['front_preview_points']);b=np.float32(meta['back_preview_points'])
h,_=cv2.findHomography(b,f)
x=np.diag([front.shape[1]/1500,front.shape[1]/1500,1])@h@np.diag([1500/back.shape[1],1500/back.shape[1],1])
a=cv2.warpPerspective(back,x,(front.shape[1],front.shape[0]),borderValue=(235,235,235))
for name,img in [('back_mirrored_registered.png',a),('back_readable.png',cv2.flip(a,1))]:
 if not cv2.imwrite(str(P/name),img):raise OSError(f'Could not write {name}')
print('Aligned rear outputs regenerated; approximate only.')
