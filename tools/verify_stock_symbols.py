"""Audit embedded graphical units/pins against the installed KiCad 10 libraries."""
from pathlib import Path
import sys, json, hashlib
import sexpdata as sx
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path.home()/'Documents/VS.Code.Projects/KiCAD-MCP-Server/python'))
from commands.dynamic_symbol_loader import DynamicSymbolLoader
def tag(e):return str(e[0]) if isinstance(e,list) and e else ''
def children(e,t):return [x for x in e if tag(x)==t]
def one(e,t):return next(x for x in e if tag(x)==t)
tree=sx.loads((R/'schematic/PetSafe_1001339.kicad_sch').read_text())
loader=DynamicSymbolLoader(project_path=R/'schematic')
audit=[]
for embedded in children(one(tree,'lib_symbols'),'symbol'):
    lid=embedded[1]; lib,name=lid.split(':')
    source=loader.find_library_file(lib)
    assert '/10.0/' in source.as_posix(),source
    stock=sx.loads(loader.extract_symbol_from_library(lib,name))
    # Root library-name prefix may differ, but every subunit and its pins must match.
    assert children(embedded,'symbol')==children(stock,'symbol'),lid
    audit.append(dict(symbol=lid,source_file=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),graphics_and_pins='IDENTICAL'))
(R/'evidence/stock_library_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8',newline='\n')
print(f'PASS: {len(audit)} embedded graphical/pin definitions identical to installed KiCad 10 stock libraries.')
