#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

package = pathlib.Path(__file__).resolve().parent.parent
issue, target = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
config = json.loads((package / 'solutions.json').read_text())
if issue not in config['order']:
    raise SystemExit('Unknown issue: ' + issue)
def git(*args):
    return subprocess.check_output(['git', '-C', str(target), *args], text=True).strip()
if git('rev-parse', 'HEAD') != config['baseline']:
    raise SystemExit('Expected the exact pinned baseline HEAD. Use a new disposable clone; do not reset an existing project.')
marker = pathlib.Path(git('rev-parse', '--absolute-git-dir')) / 'campuspool-solutions.json'
done = json.loads(marker.read_text()) if marker.exists() else []
if issue in done:
    print('Already applied issue ' + issue)
    raise SystemExit(0)
for dep in config['issues'][issue]['dependencies']:
    if dep not in done:
        subprocess.run([sys.executable, __file__, dep, str(target)], check=True)
done = json.loads(marker.read_text()) if marker.exists() else []
for name in config['issues'][issue]['patches']:
    patch = package / issue / name
    subprocess.run(['git', '-C', str(target), 'apply', '--check', '--index', str(patch)], check=True)
    subprocess.run(['git', '-C', str(target), 'apply', '--index', str(patch)], check=True)
subprocess.run([sys.executable, str(package / 'scripts/refresh-integrity.py'), str(target)], check=True)
marker.write_text(json.dumps([*done, issue]) + '\n')
print('Applied issue ' + issue)
