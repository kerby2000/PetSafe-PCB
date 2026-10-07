"""Package tracked project files (including the original evidence), excluding Git internals."""
from pathlib import Path
import json, subprocess, zipfile
R=Path(__file__).resolve().parents[1]
version=json.loads((R/'evidence/reconstruction.json').read_text())['revision']
out=R/'output'/f'PetSafe-PCB-{version}.zip'
files=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:
        if f and (R/f).is_file():z.write(R/f,'PetSafe-PCB/'+f)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert z.read('PetSafe-PCB/schematic/PetSafe_1001339.kicad_sch')==(R/'schematic/PetSafe_1001339.kicad_sch').read_bytes()
print(f'{out} ({out.stat().st_size/1024/1024:.1f} MiB); archive integrity PASS')
