#!/usr/bin/env python3
"""Commit and create a draft PR only after local verification and identity checks."""
from __future__ import annotations
import argparse, json, subprocess, sys
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(cmd,cwd=None,check=True):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode: raise RuntimeError(p.stderr.strip() or "command failed")
    return p
def out(cmd,cwd): return run(cmd,cwd).stdout.strip()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("issue"); ap.add_argument("--path",required=True); ap.add_argument("--publish",action="store_true"); ap.add_argument("--ready",action="store_true"); a=ap.parse_args()
    cfg=json.loads((ROOT/"handoff.json").read_text()); issue=str(a.issue); spec=cfg["issues"].get(issue); root=Path(a.path).resolve()
    if not spec: print("submit-pr: unknown issue",file=sys.stderr); return 2
    meta=root/".git/campuspool-handoff.json"
    if not meta.is_file(): print("submit-pr: run prepare-pr.py first",file=sys.stderr); return 2
    m=json.loads(meta.read_text())
    if m.get("issue")!=issue or m.get("owner","").lower()!=spec.get("owner","").lower() or m.get("branch")!=spec.get("branch"):
        print("submit-pr: preparation metadata does not match handoff.json",file=sys.stderr); return 2
    if m["owner"].lower()=="noqtar": return 2
    if not a.publish: print("Prepared safely. Re-run with --publish to commit, push, and create a draft PR."); return 0
    try:
        who=run(["gh","api","user","--jq",".login"]).stdout.strip()
        uid=run(["gh","api","user","--jq",".id"]).stdout.strip()
        if who.lower()!=m["owner"].lower(): raise RuntimeError(f"GitHub identity is {who!r}; assigned owner is {m['owner']!r}")
        if who.lower()=="noqtar": raise RuntimeError("noqtar is never allowed")
        origin=run(["git","remote","get-url","origin"],root).stdout.strip().lower().rstrip("/")
        if origin not in {cfg["upstream"].lower().rstrip("/"),"git@github.com:campuspool/carpooling.git"}: raise RuntimeError("origin is not the official CampusPool repository")
        head=out(["git","rev-parse","HEAD"],root)
        staged=run(["git","diff","--cached"],root).stdout
        staged_hash=hashlib.sha256(staged.encode()).hexdigest()
        if staged:
            if head!=m["base_sha"]: raise RuntimeError("staged preparation must still have HEAD exactly at base SHA")
            if staged_hash!=m.get("staged_diff_sha256"): raise RuntimeError("staged diff changed since preparation")
        else:
            if m.get("published_commit")!=head or out(["git","rev-parse",f"{head}^"],root)!=m["base_sha"]: raise RuntimeError("no staged changes and no recorded prepared commit to retry")
            if out(["git","status","--porcelain"],root): raise RuntimeError("retry requires a clean working tree")
            actual=hashlib.sha256(run(["git","diff",m["base_sha"],head],root).stdout.encode()).hexdigest()
            if actual!=m.get("published_diff_sha256"): raise RuntimeError("recorded commit diff changed since publication")
        body=ROOT/spec["body"]; text=body.read_text() if body.is_file() else f"Refs #{issue}\n\nCampusPool TypeScript implementation."
        if any(x in text.lower() for x in ("closes #","fixes #","resolves #")): raise RuntimeError("PR body must use Refs #, never closing language")
        # Run all local checks before any commit or push; output is streamed by
        # verify-prepared.py so failures retain their command diagnostics.
        if subprocess.run([sys.executable,str(ROOT/"scripts/verify-prepared.py"),issue,str(root)]).returncode:
            raise RuntimeError("Prepared checkout verification failed; nothing was published")
        existing=run(["gh","pr","list","--repo",cfg["repository"],"--head",m["branch"],"--json","url,headRefOid","--jq",".[0]"],root,False).stdout.strip()
        if existing:
            try:
                pr=json.loads(existing)
                if pr.get("headRefOid")!=out(["git","rev-parse","HEAD"],root): raise RuntimeError("existing PR uses a different head commit")
                print(pr["url"]); return 0
            except json.JSONDecodeError: raise RuntimeError("could not inspect existing PR head")
        if staged:
            run(["git","config","user.name",who],root); run(["git","config","user.email",f"{uid}+{who}@users.noreply.github.com"],root)
            run(["git","commit","-m",f"Implement CampusPool issue #{issue}"],root)
            head=out(["git","rev-parse","HEAD"],root)
            m["published_commit"]=head; m["published_diff_sha256"]=hashlib.sha256(run(["git","diff",m["base_sha"],head],root).stdout.encode()).hexdigest()
            meta.write_text(json.dumps(m,indent=2)+"\n")
        run(["git","-c","credential.helper=","-c","credential.helper=!gh auth git-credential","push","--set-upstream","origin",m["branch"]],root)
        cmd=["gh","pr","create","--repo",cfg["repository"],"--base",m["base_branch"],"--head",m["branch"],"--title",spec["title"],"--body-file",str(body)]
        if not a.ready: cmd.append("--draft")
        print(run(cmd,root).stdout.strip()); return 0
    except RuntimeError as e: print(f"submit-pr: {e}",file=sys.stderr); return 2
if __name__=="__main__": sys.exit(main())
