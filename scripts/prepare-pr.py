#!/usr/bin/env python3
"""Prepare one clean, foundation-aware issue checkout; never push or commit."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "handoff.json"

class HandoffError(RuntimeError): pass
def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode: raise HandoffError(f"{' '.join(cmd)}\n{p.stderr.strip()}")
    return p
def git(path, *args, check=True): return run(["git", *args], path, check)
def fail(msg): print(f"prepare-pr: {msg}", file=sys.stderr); return 2
def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def safe_rel(value):
    p = Path(value)
    return not p.is_absolute() and ".." not in p.parts and str(p) != "."
def patch_paths(patch):
    found=[]
    for line in patch.read_text().splitlines():
        if line.startswith("diff --git a/"):
            m=re.match(r"diff --git a/(.+) b/(.+)$", line)
            if not m or m.group(1)!=m.group(2): raise HandoffError("renames/copies are not allowed")
            found.append(m.group(1))
    if not found: raise HandoffError(f"patch has no git paths: {patch}")
    if any(not safe_rel(p) for p in found): raise HandoffError("unsafe patch path")
    return sorted(set(found))
def ancestry(path, base, descendant):
    return git(path,"merge-base","--is-ancestor",base,descendant,check=False).returncode==0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("issue"); ap.add_argument("--output",required=True)
    ap.add_argument("--source",default=None); ap.add_argument("--config",default=str(CONFIG)); a=ap.parse_args()
    config_path=Path(a.config).resolve(); cfg=json.loads(config_path.read_text()); issue=str(a.issue)
    spec=cfg.get("issues",{}).get(issue)
    if not spec: return fail(f"issue {issue} is not in handoff.json")
    out=Path(a.output).expanduser().resolve()
    if out.exists(): return fail(f"refusing existing output directory: {out} (use a new disposable work/issueN path)")
    source=a.source or cfg["upstream"]
    artifact_root=config_path.parent
    patch=(artifact_root/spec["patch"]).resolve(); files=(artifact_root/spec["files"]).resolve()
    if not patch.is_file() or not files.is_file(): return fail("patch/files manifest is missing; wait for the issue artifact")
    declared=json.loads(files.read_text())
    declared=set(declared if isinstance(declared,list) else declared.get("files",[]))
    paths=patch_paths(patch)
    if set(paths)!=declared: return fail(f"patch paths differ from manifest: patch={paths} manifest={sorted(declared)}")
    try:
        out.parent.mkdir(parents=True,exist_ok=True)
        run(["git","clone",source,str(out)])
        git(out,"remote","set-url","origin",cfg["upstream"])
        git(out,"fetch","origin","refs/heads/main:refs/remotes/origin/main")
        # A missing foundation branch is handled below with a friendly message.
        git(out,"fetch","origin",f"refs/heads/{cfg['foundation']['branch']}:refs/remotes/origin/{cfg['foundation']['branch']}",check=False)
        baseline=cfg["baseline"]
        remote_main=git(out,"rev-parse","origin/main").stdout.strip()
        if not ancestry(out,baseline,"origin/main"): raise HandoffError(f"origin/main is not a descendant of configured baseline {baseline}")
        marker=cfg["foundation"]["marker"]; expected=cfg["foundation"]["value"]
        main_marker=git(out,"show",f"origin/main:{marker}",check=False)
        main_marker=main_marker.stdout.strip() if main_marker.returncode==0 else None
        if issue==cfg["foundation"]["issue"]:
            base_ref="origin/main"; base_branch="main"; base_sha=remote_main
        elif main_marker==expected:
            base_ref="origin/main"; base_branch="main"; base_sha=remote_main
        else:
            fref=f"origin/{cfg['foundation']['branch']}"
            check=git(out,"rev-parse","--verify",fref,check=False)
            if check.returncode: raise HandoffError("foundation issue 39 is not merged and official codex/issue-39 is unavailable; leader must submit issue 39 first")
            fsha=check.stdout.strip(); fmarker=git(out,"show",f"{fsha}:{marker}",check=False)
            if fmarker.returncode or fmarker.stdout.strip()!=expected: raise HandoffError("official foundation branch exists but has no valid campuspool foundation marker")
            base_ref=fref; base_branch=cfg["foundation"]["branch"]; base_sha=fsha
        git(out,"checkout","-B",spec["branch"],base_ref)
        # Patch is applied from an explicit file, never from arbitrary working-tree state.
        git(out,"apply","--index",str(patch))
        staged=git(out,"diff","--cached","--name-only").stdout.splitlines()
        if sorted(staged)!=paths: raise HandoffError(f"staged paths are not exactly declared paths: {staged}")
        if not (out/marker).is_file() or (out/marker).read_text().strip()!=expected: raise HandoffError("prepared tree lost the required foundation marker")
        meta={"schema":1,"issue":issue,"owner":spec["owner"],"branch":spec["branch"],"verify":spec.get("verify","feature"),"base_branch":base_branch,"base_sha":base_sha,"foundation_branch":cfg["foundation"]["branch"],"foundation_marker":marker,"foundation_value":expected,"patch_sha256":sha256(patch),"declared_paths":paths,"staged_diff_sha256":hashlib.sha256(git(out,"diff","--cached").stdout.encode()).hexdigest()}
        (out/".git"/"campuspool-handoff.json").write_text(json.dumps(meta,indent=2)+"\n")
        print(json.dumps(meta,indent=2)); return 0
    except (HandoffError, OSError, subprocess.CalledProcessError) as e:
        return fail(f"{e}; preserved checkout for inspection: {out}")
if __name__=="__main__": sys.exit(main())
