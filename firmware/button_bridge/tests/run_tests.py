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
    linked = ['main/bridge_policy.c'] if name == 'output' else []
    subprocess.run([*compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', *extra, *linked, '-Imain',
                    f'main/{source}', f'tests/test_{name}.c', '-o', str(exe)], cwd=ROOT, check=True)
    scenarios = ['normal', 'count_fail', 'arm_fail', 'start_fail', 'start_failed_after_arm',
                 'assert_fail', 'assert_and_release_fail', 'alarm_at_start', 'alarm_at_assert', 'release_low_fail',
                 'stop_fail', 'shutdown', 'shutdown_during_arm'] if name == 'output' else [None]
    for scenario in scenarios:
        subprocess.run([str(exe), *([scenario] if scenario else [])], check=True)
subprocess.run([sys.executable, 'tests/test_tools.py'], cwd=ROOT, check=True)
subprocess.run(['node', 'tests/test_web.cjs'], cwd=ROOT, check=True)
