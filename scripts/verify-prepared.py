#!/usr/bin/env python3
"""Run bounded checks against a prepared checkout; no network writes."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(cmd,cwd,allow=False):
    print("$ "+" ".join(cmd),flush=True)
    p=subprocess.run(cmd,cwd=cwd)
    if p.returncode and not allow: raise SystemExit(p.returncode)
    return p.returncode
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("issue"); ap.add_argument("path"); a=ap.parse_args()
    root=Path(a.path).resolve(); meta=root/".git/campuspool-handoff.json"
    if not meta.is_file(): print("verify-prepared: missing preparation metadata",file=sys.stderr); return 2
    m=json.loads(meta.read_text())
    if str(m["issue"])!=str(a.issue) or m.get("owner","").lower()=="noqtar": return 2
    marker=root/m["foundation_marker"]
    if not marker.is_file() or marker.read_text().strip()!=m["foundation_value"]: print("verify-prepared: invalid foundation marker",file=sys.stderr); return 2
    status=subprocess.run(["git","status","--porcelain"],cwd=root,text=True,stdout=subprocess.PIPE).stdout.splitlines()
    # The issue files are intentionally staged; metadata lives in .git.
    if any(not line.startswith(("A ","M ","D ","R ")) for line in status): print("verify-prepared: unexpected working-tree state",file=sys.stderr); return 2
    staged=subprocess.run(["git","diff","--cached","--name-only"],cwd=root,text=True,stdout=subprocess.PIPE).stdout.splitlines()
    if not staged and m.get("published_commit"):
        head=subprocess.run(["git","rev-parse","HEAD"],cwd=root,text=True,stdout=subprocess.PIPE).stdout.strip()
        parent=subprocess.run(["git","rev-parse",f"{head}^"],cwd=root,text=True,stdout=subprocess.PIPE).stdout.strip()
        if head!=m["published_commit"] or parent!=m["base_sha"]:
            print("verify-prepared: retry commit does not match recorded base",file=sys.stderr); return 2
        staged=subprocess.run(["git","diff","--name-only",m["base_sha"],head],cwd=root,text=True,stdout=subprocess.PIPE).stdout.splitlines()
    if sorted(staged)!=sorted(m["declared_paths"]): print("verify-prepared: staged scope mismatch",file=sys.stderr); return 2
    app=root/"campuspool"
    if not (app/"package.json").is_file(): print("verify-prepared: campuspool/package.json missing",file=sys.stderr); return 2
    if (app/"package-lock.json").is_file(): run(["npm","ci"],app)
    scripts=json.loads((app/"package.json").read_text()).get("scripts",{})
    missing=[name for name in ("typecheck","lint","build","test") if name not in scripts]
    if missing:
        print("verify-prepared: required npm scripts missing: "+", ".join(missing),file=sys.stderr); return 2
    for name in ("typecheck","lint","build","test"): run(["npm","run",name],app)
    if m.get("verify") in ("feature","testplan"):
        candidates=[app/"tests"/f"issue-{a.issue}.test.ts",app/"tests"/f"issue-{a.issue}.test.tsx",app/"tests"/"features"/f"issue-{a.issue}.test.ts"]
        if not any(p.is_file() for p in candidates):
            print(f"verify-prepared: feature issue {a.issue} has no issue-scoped test file",file=sys.stderr); return 2
    if m.get("verify")=="docs":
        docs=[root/"campuspool/docs",root/"README.md",root/"INTEGRATION.md",root/"TEAM_START_HERE.md",root/"docs"]
        if not any(p.exists() for p in docs):
            print("verify-prepared: documentation issue has no documentation artifact",file=sys.stderr); return 2
    compose=app/"docker-compose.verify.yml"
    if compose.is_file():
        run(["docker","compose","-f",str(compose),"up","-d","--wait"],app)
        try:
            if "test:integration" not in scripts:
                print("verify-prepared: docker compose exists but test:integration script is missing",file=sys.stderr); return 2
            run(["npm","run","test:integration"],app)
        finally: run(["docker","compose","-f",str(compose),"down","-v"],app)
    integration=ROOT/"scripts"/"test-integration.sh"
    if integration.is_file(): run([str(integration),str(a.issue),str(root)],ROOT)
    print(f"verify-prepared: issue {a.issue} passed available checks"); return 0
if __name__=="__main__": sys.exit(main())
