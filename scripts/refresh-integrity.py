#!/usr/bin/env python3
"""Refresh package metadata after intentional patches; retain upstream attribution."""
import csv
import hashlib
import io
import json
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
root = repo / 'prototype'
source = root / 'SOURCE_MAP.tsv'
baseline = json.loads((pathlib.Path(__file__).resolve().parent.parent / 'solutions.json').read_text())['baseline']
original = subprocess.check_output(['git', '-C', str(repo), 'show', baseline + ':prototype/SOURCE_MAP.tsv'], text=True)
old = {r['path']: r for r in csv.DictReader(io.StringIO(original), delimiter='\t')}
tracked = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '-z', 'prototype'], text=True).split('\0')
rows = []
for name in sorted(n for n in tracked if n):
    rel = pathlib.Path(name).relative_to('prototype').as_posix()
    if rel == 'MANIFEST.sha256':
        continue
    path = root / rel
    if not path.is_file():
        raise SystemExit('Tracked package file missing: ' + rel)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    prior = old.get(rel)
    if rel == 'SOURCE_MAP.tsv':
        rows.append([rel, '-', 'package-authored', 'Self hash omitted; covered by MANIFEST.sha256'])
    elif prior and prior['sha256'] == digest:
        rows.append([rel, digest, prior['provenance'], prior['detail']])
    else:
        origin = (prior['provenance'] + ': ' + prior['detail']) if prior else 'new file'
        rows.append([rel, digest, 'ai-assisted-proposed-change', 'Sprint 1 issue solutions; prior: ' + origin])
with source.open('w', newline='') as out:
    writer = csv.writer(out, delimiter='\t', lineterminator='\n')
    writer.writerow(['path', 'sha256', 'provenance', 'detail'])
    writer.writerows(rows)
subprocess.run([sys.executable, str(root / 'scripts/check-package.py'), '--write'], check=True)
subprocess.run(['git', '-C', str(repo), 'add', 'prototype/SOURCE_MAP.tsv', 'prototype/MANIFEST.sha256'], check=True)
print('Source map and manifest regenerated from the staged source package.')
