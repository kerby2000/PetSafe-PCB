"""Host checks for the same C policy/output code and shipped web/client code. No board access."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cc', default=os.environ.get('CC', 'cc'), help='Host C compiler path, or zig executable')
args = parser.parse_args()
compiler = [args.cc]
if Path(args.cc).stem == 'zig':
    compiler.append('cc')
out = ROOT / '.test-build'
out.mkdir(exist_ok=True)
for name, source, extra in [('policy', 'bridge_policy.c', []),
                            ('output', 'button_output.c', ['-Itests/stubs'])]:
    exe = out / (f'test_{name}' + ('.exe' if os.name == 'nt' else ''))
    subprocess.run([*compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', *extra, '-Imain',
                    f'main/{source}', f'tests/test_{name}.c', '-o', str(exe)], cwd=ROOT, check=True)
    subprocess.run([str(exe)], check=True)
subprocess.run([sys.executable, 'tests/test_tools.py'], cwd=ROOT, check=True)
subprocess.run(['node', 'tests/test_web.cjs'], cwd=ROOT, check=True)
