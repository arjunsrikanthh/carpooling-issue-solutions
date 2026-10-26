#!/usr/bin/env python3
"""Regenerate disjoint issue patches from the original app, preserving the legacy archive."""
from pathlib import Path
import fnmatch,hashlib,json,os,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'campuspool'
RULES={
 '12':['src/server/vehicles.ts','src/app/api/vehicles/**','src/app/vehicles/**','src/features/enabled/12.json','tests/issue-12.test.ts'],
 '21':['src/server/offers.ts','src/app/api/offers/route.ts','src/app/offers/**','src/features/enabled/21.json','tests/issue-21.test.ts'],
 '23':['src/server/bookings.ts','src/app/api/bookings/route.ts','src/app/api/bookings/*/decision/**','src/app/bookings/**','src/features/enabled/23.json','tests/issue-23.test.ts'],
 '24':['src/server/cancellations.ts','src/app/api/cancellations/**','src/app/api/bookings/*/cancel/**','src/app/api/offers/*/cancel/**','src/app/cancellations/**','src/features/enabled/24.json','tests/issue-24.test.ts'],
 '37':['src/server/activity.ts','src/server/mongo.ts','src/server/outbox.ts','src/app/api/activity/**','src/app/api/admin/database-evidence/**','src/app/activity/**','src/app/admin/database-evidence/**','src/features/enabled/37.json','sql/migrations/002_evidence.sql','sql/migrations/003_course_evidence.sql','scripts/activity-worker.ts','tests/issue-37.test.ts','tests/database-evidence.ts','tests/outbox-recovery.ts'],
 '43':['tests/issue-43.test.ts','tests/http.e2e.test.ts','tests/http.ts','docs/TEST_TRACEABILITY.md']}
SCOPES={
 '12':'Vehicle registration and administrator review; car/bike capacity validation. Public ride details use the shared masked vehicle projection.',
 '21':'Publish and list approved-driver offers, capacity/date validation, and driver time-conflict protection.',
 '23':'Quote-bound requests and host decisions, atomic final-seat confirmation and synthetic credit holds.',
 '24':'Sprint 1 booking and whole-ride cancellation, retained history, exact refunds and race coverage. Sprint 2 waitlist/rematching remains pending.',
 '37':'Advanced SQL integrity guards, view/procedure/index evidence, and audience-protected Mongo activity delivered through a retryable SQL outbox.',
 '39':'Original Next.js/TypeScript stack migration foundation: shared auth/roles/approval, MySQL schema, fixed-stop search, API contracts, setup and CI. This deliberately includes shared bootstrap work beyond the CI-only issue title; review the migration before integration.',
 '43':'Executable test-plan contribution, search regression and the cross-feature production HTTP journey. Approved Test Plan mapping remains provisional until human approval.',
 '44':'Draft SRS/SAD/Test Plan/ERD, DBMS evidence instructions, course mapping and ownership guidance. Actual video, instructor approvals and genuine teammate reviews remain outstanding.'}

def appfiles():
 for p in APP.rglob('*'):
  if not p.is_file():continue
  parts=p.relative_to(APP).parts
  if any(x in {'.next','node_modules','coverage','.git'} for x in parts):continue
  if p.name in {'.env','tsconfig.tsbuildinfo','.DS_Store'} or p.name.startswith('.env.') and p.name!='.env.example':continue
  yield p

def mappings():
 result={i:{} for i in [*RULES,'39','44']}
 for p in sorted(appfiles()):
  rel=p.relative_to(APP).as_posix();owners=[i for i,rules in RULES.items() if any(fnmatch.fnmatch(rel,r) for r in rules)]
  if len(owners)>1:raise ValueError(f'Overlapping ownership: {rel}: {owners}')
  owner=owners[0] if owners else '39';result[owner]['campuspool/'+rel]=p
 result['39']['.github/workflows/campuspool-next.yml']=ROOT/'campuspool/ci/campuspool-next.yml'
 for p in sorted((ROOT/'docs').rglob('*')):
  if p.is_file():result['44']['campuspool/docs/'+p.relative_to(ROOT/'docs').as_posix()]=p
 return result

def main():
 cfg=json.loads((ROOT/'handoff.json').read_text());mapping=mappings();report={'baseline':cfg['baseline'],'issues':{},'path_owners':{}}
 for issue,files in mapping.items():
  for path in files:
   if path in report['path_owners']:raise ValueError('Duplicate patch path '+path)
   report['path_owners'][path]=issue
  folder=ROOT/issue;folder.mkdir(exist_ok=True)
  with tempfile.TemporaryDirectory(prefix='cp-patch-') as temp:
   base=Path(temp);subprocess.run(['git','init','-q'],cwd=base,check=True)
   for rel,source in files.items():
    target=base/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
   subprocess.run(['git','add','--all'],cwd=base,check=True)
   patch=subprocess.check_output(['git','diff','--cached','--binary','--full-index','--no-renames'],cwd=base)
   (folder/'solution.patch').write_bytes(patch)
  (folder/'files.json').write_text(json.dumps(sorted(files),indent=2)+'\n')
  spec=cfg['issues'][issue]
  text=f'''Refs #{issue}

{SCOPES[issue]}

This is a proposed original TypeScript implementation. The owner must inspect, understand and adapt the prepared changes, run the checks, and request a genuine independent review. AI assistance is disclosed; preparing a branch does not establish individual authorship or course approval.

Validation: `python3 scripts/verify-prepared.py {issue} work/issue{issue}` from the solutions checkout runs typecheck, lint, production build, available unit tests and isolated MySQL/Mongo integration. Full HTTP testing runs once its feature dependencies are present. See the solutions verification report for integrated results.

Dependency: {'official main; supplies the shared foundation' if issue=='39' else 'shared foundation #39; target codex/issue-39 until it is merged, then refresh against main'}. No automatic merge or issue closure is requested.
'''
  (folder/'PR.md').write_text(text)
  (folder/'README.md').write_text(f'''# Issue #{issue} — {spec['title']}

Assigned owner: `@{spec['owner']}`.

{SCOPES[issue]}

From a clone of the solutions repository:

```sh
python3 scripts/prepare-pr.py {issue} --output work/issue{issue}
python3 scripts/verify-prepared.py {issue} work/issue{issue}
# Read/edit the staged diff and PR body, then publish with your assigned account:
python3 scripts/submit-pr.py {issue} --path work/issue{issue} --publish
```

The helper creates a separate official-repository checkout. Do not push the solutions repository to the official repo. This patch contains only the paths listed in `files.json`; it adds no legacy application source. Required tools: Node.js 24, Python 3, Git, GitHub CLI and Docker.

{'Prepare #39 first. Other teammates can prepare after its official branch exists.' if issue=='39' else 'The shared foundation must exist on official main or official codex/issue-39 before preparation. Feature branches can be prepared in parallel; retarget/retest after the foundation merge.'}

Draft PRs and `Refs #N` preserve review and existing issue status. Teammates must explain their own changes and resolve review comments. The approved Test Plan, faculty acceptance and working-product video are separate outstanding deliverables.
''')
  report['issues'][issue]={'owner':spec['owner'],'files':len(files),'patch_sha256':hashlib.sha256(patch).hexdigest(),'source_sha256':{rel:hashlib.sha256(p.read_bytes()).hexdigest() for rel,p in files.items()}}
 (ROOT/'reports/handoff-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Generated disjoint patches:',', '.join(f'{i}: {len(v)} paths' for i,v in mapping.items()))
if __name__=='__main__':main()
