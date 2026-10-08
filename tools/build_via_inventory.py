from pathlib import Path
import json,hashlib,csv
R=Path(__file__).resolve().parents[1]
# Manually reviewed centres on a 6000 x 1300 rear preview. Excludes mounting,
# connector and named test-point holes; no net is inferred from hole position alone.
isolated=[(33,853),(33,914),(93,854),(89,253),(89,315),(341,897),(447,836),(446,913),(521,839),(523,913),(609,931),(616,760),(612,612),(651,556),(820,413),(979,438),(978,516),(1323,515),(1426,924),
 (1740,253),(1583,648),(1685,648),(1632,692),(1895,689),(2000,689),(1528,924),(2284,847),(2653,1035),(2688,291),
 (3181,351),(3264,483),(3375,417),(3270,589),(3682,648),(3731,563),(3945,945),(3077,951)]
plane=[(104,1048),(375,215),(375,290),(375,357),(645,420),(825,307),(985,199),(1067,445),(1380,131),(1344,261),(1453,671),(1455,806),(1368,966),(1366,1139),
 (1714,101),(1850,202),(2310,169),(2132,350),(1847,426),(1740,698),(1738,847),(1637,875),(1895,856),(2001,855),(2315,1137),(1864,1171),(2619,1137),(2528,478),(2584,712),(2220,557),(2530,420),(2585,227),
 (3016,269),(3016,341),(3334,164),(3561,167),(3784,164),(4005,167),(4006,411),(3440,574),(3325,681),(4011,661),(4016,802),(4019,944),(4018,1083),(3559,1129),(3177,1048),(3177,837)]
other=[(1514,40),(2384,84),(2584,292),
 (4197,116),(4353,116),(4515,116),(4670,116),
 (4075,247),(4233,247),(4395,247),(4550,248),(4197,399),(4353,400),(4844,477),
 (4198,730),(4328,730),(4464,730),(4596,730),
 (5056,718),(5173,635),(5250,382),(5306,674),(4851,838),(5305,864),
 (5487,1111),(5440,1195),(5352,1186),(5302,1195),(5220,1210),(5168,1210),(5800,1076),(5600,1051),(5699,1197),(5490,1260),(4740,1141),(4600,1141),(5817,124)]
rear_caps=[(4127,730),(4264,730),(4400,728),(4530,730),(4669,730)]
sites=[]
for group,pts in [('REAR_CLEARANCE',isolated),('MAIN_REAR_COPPER',plane),('OTHER_REAR_REGION',other),('REAR_COMPONENT_PAD',rear_caps)]:
 for x,y in pts:
  sites.append(dict(rear_xy=[x*2,y*2],front_xy=[x*2,y*2],rear_appearance=group,
   front_match='PROJECTED: inspect original front photo; may be under a component',
   endpoints=[],net=None,confidence='rear visible; global front projection approximate',
   note={'REAR_CLEARANCE':'Visible clearance separates this site from the surrounding rear copper; this alone does not identify an internal net.',
   'MAIN_REAR_COPPER':'No isolating rear clearance apparent. Main copper is associated with PIC VSS through the reviewed anchors. Individual front endpoint not yet assigned.',
   'OTHER_REAR_REGION':'Separate strip/antenna region or ambiguous copper boundary; do not assume GND.',
   'REAR_COMPONENT_PAD':'Rear via/pad joins a tuning-capacitor land; not a direct GND assignment.'}[group]))
sites.sort(key=lambda v:(v['rear_xy'][0],v['rear_xy'][1]))
for i,v in enumerate(sites,1):v['id']=f'V{i:03d}'
def match(x,y,front,ends,net,note):
 v=min(sites,key=lambda v:(v['rear_xy'][0]-2*x)**2+(v['rear_xy'][1]-2*y)**2)
 assert abs(v['rear_xy'][0]-2*x)<3 and abs(v['rear_xy'][1]-2*y)<3,(x,y,v)
 v.update(front_xy=front,endpoints=ends,net=net,note=note,front_match='MANUALLY MATCHED',confidence='photo-derived, not continuity measured')
 # Coordinates measured independently in the enlarged PIC front and rear crops.
 return v['id']
# Front crop coordinates used previously: original x=2100+2.5*u, y=2.5*v.
f=lambda x,y:[round(2100+2.5*x),round(2.5*y)]
ids={}
ids['D4']=match(1380,131,f(261,117),['D4.2'],'H_GND','D4 anode-side via matches a rear site without clearance in the main VSS-associated copper.')
ids['D5']=match(1344,261,f(234,217),['D5.2'],'H_GND','D5 anode-side via matches the same rear copper region as the PIC VSS anchors.')
ids['C41']=match(1067,445,f(10,360),['C41.2'],'H_GND','C41 left pad in front mosaic joins this via; rear side joins main VSS-associated copper. Opposite capacitor pad remains the TP4 net.')
ids['VSS19']=match(1850,202,f(646,173),['U4.19','C32.2'],'H_GND','Ground anchor: C32 pad visibly joins PIC VSS pin 19 and this non-isolated rear via.')
ids['VSS8']=match(1738,847,f(554,679),['U4.8'],'H_GND','Ground anchor: PIC VSS pin 8 visibly joins this non-isolated rear via.')
ids['VDD20']=match(1740,253,f(557,216),['U4.20','C32.1'],'H_VDD','Contrast anchor: PIC VDD pin 20 / C32 supply pad. Rear annular clearance is visible; the rear plane is not this supply net.')
ids['RC1']=match(2284,847,f(997,679),['U4.12'],None,'PIC RC1 pin 12 reaches this site. Rear clearance and no visible onward surface trace; hidden continuation remains unresolved. Do not call it GND or VDD.')
ids['C39']=match(1637,875,f(475,704),['C39.2'],'H_GND','C39 opposite pad via supports the existing GND estimate using the matching rear copper.')
ids['C26']=match(1366,1139,f(255,905),['C26.2'],'H_GND','C26 ground-side pad matches a rear plane site; does not resolve its other pad.')
ids['D6']=match(1323,515,f(223,422),[],None,'Via beside/under the PIC body near D6. Rear annular clearance is visible; external endpoints require more tracing.')
out=dict(date='2026-10-08',revision='v0.8',source_front='photos/front_registered.jpg',source_rear='photos/back_mirrored_registered.jpg',
 images_are_original_photographic_mosaics=True,coordinate_size=[12000,2600],
 coverage='Board-wide rear-visible site inventory; not an exhaustive count of every physical via. Sticker, components, solder, image edges and ambiguous tiny features hide sites. Projected front markers are not confirmed net matches.',
 layers='Four-layer construction is a plausible working hypothesis supplied by the user, not verified by the surface photos. Inner planes and signal layers cannot be distinguished by an isolated outer pad alone.',
 ground_basis='Two independent visible PIC VSS anchors (pins 8 and 19) join the main rear copper. Supply pin 20 has a contrasting isolated rear pad.',
 registration='Existing mirrored registration, max recorded control-point residual 5.77 pixels at 1500-pixel width (~46 pixels on this 12000-pixel canvas). Selected PIC endpoints corrected manually. No metric accuracy claimed.',
 categories={'MAIN_REAR_COPPER':'Main VSS-associated rear copper candidate','REAR_CLEARANCE':'Rear isolated pad; onward net unknown unless independently known','OTHER_REAR_REGION':'Other/ambiguous region; not automatically GND','REAR_COMPONENT_PAD':'Rear component land connection'},
 sites=sites,reviewed_anchors=ids,new_model_connections=['D4.2','D5.2','C41.2'],
 sources=['photos/originals/IMG_2436.jpg','photos/originals/IMG_2437.jpg','photos/originals/IMG_2439.jpg','photos/originals/IMG_2440.jpg','photos/originals/IMG_2441.jpg','photos/originals/IMG_2442.jpg','photos/originals/IMG_2443.jpg'],
 interpretation_source='https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/plane')
(R/'evidence/via_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
with (R/'evidence/via_inventory.csv').open('w',newline='',encoding='utf-8') as h:
 fields=['id','rear_x','rear_y','front_x','front_y','rear_appearance','front_match','endpoints','net','note']
 w=csv.DictWriter(h,fieldnames=fields);w.writeheader()
 for v in sites:w.writerow(dict(id=v['id'],rear_x=v['rear_xy'][0],rear_y=v['rear_xy'][1],front_x=v['front_xy'][0],front_y=v['front_xy'][1],rear_appearance=v['rear_appearance'],front_match=v['front_match'],endpoints=';'.join(v['endpoints']),net=v['net'] or '',note=v['note']))
print(len(sites),'rear-visible sites;',len(ids),'manually matched anchors;',ids)
