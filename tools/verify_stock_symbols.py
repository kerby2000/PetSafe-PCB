"""Audit embedded graphical units/pins against the installed KiCad 10 libraries."""
from pathlib import Path
import argparse, copy, os, json, hashlib
from functools import lru_cache
import sexpdata as sx
from inventory_contracts import verify_bridge_asset_bytes
R=Path(__file__).resolve().parents[1]
def tag(e):return str(e[0]) if isinstance(e,list) and e else ''
def children(e,t):return [x for x in e if tag(x)==t]
def one(e,t):return next(x for x in e if tag(x)==t)
@lru_cache(maxsize=None)
def library_symbols(path):
    return {e[1]: e for e in children(sx.loads(path.read_text(encoding='utf-8')), 'symbol')}

def graphical_units(symbols, name, chain=()):
    """Resolve KiCad extends for the graphics/pins actually checked here.

    Do not import an external symbol loader or silently drop a missing parent.
    Properties are intentionally outside this audit, as in the original check.
    """
    if name in chain:
        raise ValueError('Cyclic symbol inheritance: ' + ' -> '.join((*chain, name)))
    if name not in symbols:
        raise ValueError('Missing symbol/parent: ' + name)
    symbol = symbols[name]
    parents = children(symbol, 'extends')
    if len(parents) > 1:
        raise ValueError('Multiple symbol parents: ' + name)
    units = {}
    if parents:
        parent = str(parents[0][1])
        for unit in graphical_units(symbols, parent, (*chain, name)):
            unit = copy.deepcopy(unit)
            assert str(unit[1]).startswith(parent + '_'), unit[1]
            suffix = str(unit[1])[len(parent):]
            unit[1] = name + suffix
            units[suffix] = unit
    for unit in children(symbol, 'symbol'):
        assert str(unit[1]).startswith(name + '_'), unit[1]
        units[str(unit[1])[len(name):]] = unit
    return list(units.values())

def verify(symbol_dir):
    tree=sx.loads((R/'schematic/PetSafe_1001339.kicad_sch').read_text(encoding='utf-8'))
    table=sx.loads((R/'schematic/sym-lib-table').read_text(encoding='utf-8'))
    registered={one(entry,'name')[1]: entry for entry in children(table,'lib')}
    assert len(registered)==len(children(table,'lib')), 'Duplicate library registration'
    audit=[]
    for embedded in children(one(tree,'lib_symbols'),'symbol'):
        lid=embedded[1]; lib,name=lid.split(':')
        custom=lib=='PetSafe_Datasheet'
        vendor=lib=='TrailCurrentSymbolLibrary'
        # Keep checking the project's actual registration, not just a same-named file.
        expected_uri=('${KIPRJMOD}/' if custom or vendor else '${KICAD10_SYMBOL_DIR}/')+lib+'.kicad_sym'
        assert lib in registered, f'Unregistered library: {lib}'
        assert one(registered[lib],'type')[1]=='KiCad', lib
        assert one(registered[lib],'uri')[1]==expected_uri, f'Unexpected library source: {lib}'
        source=(R/'schematic' if custom or vendor else symbol_dir)/(lib+'.kicad_sym')
        if not source.is_file():
            raise FileNotFoundError(f'{source}: install the packed KiCad 10 symbol libraries; see docs/REBUILD.md')
        if vendor:
            assert name=='ESP32-C6-SuperMini'
            bridge=json.loads((R/'evidence/reconstruction.json').read_text())['external_button_bridge']
            verify_bridge_asset_bytes(source.read_bytes(),bridge['library_files'],'symbol_sha256')
        # Root library-name prefix may differ, but every subunit and its pins must match.
        assert children(embedded,'symbol')==graphical_units(library_symbols(source),name),lid
        portable_source=('schematic/' if custom or vendor else '${KICAD10_SYMBOL_DIR}/')+source.name
        audit.append(dict(symbol=lid,source_type='Owner-selected TrailCurrent library' if vendor else 'MCP-created datasheet symbol' if custom else 'KiCad 10 stock',source_file=portable_source,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),graphics_and_pins='IDENTICAL'))
    (R/'evidence/stock_library_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8',newline='\n')
    print(f'PASS: {len(audit)} embedded definitions match registered stock, authorized datasheet or owner-selected vendor libraries.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--symbols',default=os.environ.get('KICAD10_SYMBOL_DIR'),help='Packed KiCad 10 symbol directory; defaults to KICAD10_SYMBOL_DIR')
    args=parser.parse_args()
    if not args.symbols:parser.error('Set KICAD10_SYMBOL_DIR or pass --symbols; see docs/REBUILD.md')
    verify(Path(args.symbols).resolve())
