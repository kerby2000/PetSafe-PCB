"""Prepare MCP placement requests; reuse the reviewed topology, never its symbols."""
from pathlib import Path
import importlib.util, json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('legacy', ROOT/'reference/v02/single_sheet.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
for fn in ['power','controller','motor_ui','rf','receiver','tuning','pir_options','legend']:
    getattr(old,fn)()

def write(path, data):
    path.write_text(json.dumps(data, indent=2), encoding='utf-8', newline='\n')

symbols = {
    'U1':'Connector_Generic:Conn_01x05',
    'U2':'74xGxx:74LVC2G14',
    'U3':'Amplifier_Operational:Opamp_Dual',
    'U4':'MCU_Microchip_PIC16:PIC16F18855-xSO',
    'U5':'Connector_Generic:Conn_02x04_Counter_Clockwise',
    'U6':'Connector_Generic:Conn_01x05',
    'Q1':'Transistor_BJT:MMBT3904', 'Q2':'Transistor_BJT:BC847',
    'Q7':'Transistor_BJT:BC857',
    'Q8':'Connector_Generic:Conn_02x03_Counter_Clockwise',
    'LED1':'Device:LED_Dual_AAKK', 'S1':'Switch:SW_Push_Dual',
    'J1':'Connector_Generic:Conn_01x05', 'J3':'Connector_Generic:Conn_01x03',
    'J5':'Connector_Generic:Conn_01x02', 'J6':'Connector_Generic:Conn_01x02',
    'U6A':'Connector_Generic:Conn_01x03', 'U7':'Connector_Generic:Conn_01x03',
    'Q9':'Connector_Generic:Conn_01x03',
}
maps = {
    'U1':dict(L1='1',L2='2',L3='3',R2='4',R1='5'),
    'U2':dict(T3='1',T2='2',T1='3',B1='4',B2='5',B3='6'),
    'U6':dict(R1='1',R2='2',R3='3',L2='4',L1='5'),
    'Q8':dict(T1='1',T2='2',T3='3',B3='4',B2='5',B1='6'),
    'LED1':dict(TL='1',TR='2',BL='3',BR='4'),
    'S1':dict(TL='1',TR='2',BL='3',BR='4'),
    'J1':dict(CLK='1',DAT='2',VPP='3',VDD='4',GND='5'),
    'J5':dict(A='1',B='2'),
}
placements=[]; extra=[]; crosswalk={}; catalog=[]
for i in old.INST:
    ref=i['ref']; c=old.C[ref]; k=i['kind']; angle=0
    symbol=symbols.get(ref)
    if not symbol:
        symbol={'R':'Device:R','C':'Device:C','L':'Device:L','Y':'Device:Crystal',
                'TP':'Connector:TestPoint','PNP':'Transistor_BJT:Q_PNP_BEC',
                'DUALD':'Diode:BAV99','D2':'Device:D'}.get(k)
    assert symbol, (ref,k)
    pinmap=maps.get(ref, {})
    if k in ['PNP','NPN']:
        bce=c.get('bce',dict(B='R',E='L',C='S'))
        pinmap={bce['B']:'1',bce['E']:'2',bce['C']:'3'}
    elif k=='DUALD':pinmap=dict(L='1',R='2',S='3')
    elif ref in ['U6A','U7','Q9','J6']:
        pinmap={p:str(n+1) for n,p in enumerate(c['pins'])}
    for p in i['pins']:
        pn=pinmap.get(p['p'],p['p'])
        crosswalk[ref+'.'+p['p']]=i['actual']+'.'+pn
    x,y=i['x'],i['y']
    if k in ['R','C','L']:
        p1=next(p for p in i['pins'] if p['p']=='1')
        angle=(90 if p1['x']<0 else 270) if p1['x'] else (0 if p1['y']<0 else 180)
    if k=='TP': x-=2; angle=270
    if ref=='C5':symbol='Device:C_Polarized'
    if ref=='U3' and i['unit']==3:x+=2
    # The standard PIC places oscillator pins on the right and RC3 on the left.
    if ref=='Y1':x,y=246,89
    if ref=='C30':x,y=238,98
    if ref=='C31':x,y=254,98; angle=180
    if ref=='TP11':x,y=182,70;angle=90
    value=i['value']
    if ref=='U2':value='SN74LVC2G14DBV?'
    if ref=='U1':value='S-1200B45? [pins]'
    if ref=='U5':value='MX512H [pins]'
    if ref=='U6':value='WN23? [pins]'
    if ref=='Q8':value='372A? [pads]'
    args=dict(symbol=symbol,reference=i['actual'],value=value,
              position=dict(x=round(x*1.27,4),y=round(y*1.27,4)),rotation=angle,includePins=True)
    footprints={'U2':'Package_TO_SOT_SMD:SOT-23-6','U3':'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
                'U4':'Package_SO:SOIC-28W_7.5x17.9mm_P1.27mm',
                'U1':'Package_TO_SOT_SMD:SOT-23-5', 'U5':'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm'}
    if k in ['PNP','NPN','DUALD']:args['footprint']='Package_TO_SOT_SMD:SOT-23'
    if ref in footprints:args['footprint']=footprints[ref]
    if i['unit']==1:placements.append(args)
    else:
        args['angle']=args.pop('rotation');args.pop('includePins');args['unit']=i['unit'];extra.append(args)
    catalog.append(dict(original_ref=ref,reference=i['actual'],unit=i['unit'],symbol=symbol,
                        footprint=args.get('footprint',''),legacy=i,placement=args))

stage=ROOT/'.cache/v03';stage.mkdir(parents=True,exist_ok=True)
write(stage/'placements.json',placements);write(stage/'extra_units.json',extra)
write(stage/'layout.json',dict(catalog=catalog,crosswalk=crosswalk,notes=old.NOTES,
                            wires=old.WIRES,labels=old.LABELS,pins=old.PINS,graphics=old.GRAPH))
(ROOT/'evidence/library_layout.json').write_text((stage/'layout.json').read_text(),encoding='utf-8',newline='\n')
write(ROOT/'evidence/library_placements.json',dict(components=placements,extra_units=extra))
write(ROOT/'evidence/pin_crosswalk.json',crosswalk)
print(f'Prepared {len(placements)} components and {len(extra)} additional units; {len(crosswalk)} physical pads.')
