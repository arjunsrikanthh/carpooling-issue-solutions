import json, subprocess, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]; PREP=HERE/"scripts/prepare-pr.py"
def sh(*args,cwd): return subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def fixture():
    d=Path(tempfile.mkdtemp()); remote=d/"remote"; remote.mkdir(); sh("git","init","-b","main",cwd=remote); sh("git","config","user.email","test@example.com",cwd=remote); sh("git","config","user.name","Test",cwd=remote)
    (remote/"campuspool").mkdir(); (remote/"campuspool/package.json").write_text('{"scripts":{}}'); sh("git","add",".",cwd=remote); sh("git","commit","-m","baseline",cwd=remote); base=sh("git","rev-parse","HEAD",cwd=remote).stdout.strip()
    (remote/"campuspool/.foundation-version").write_text("next-v1\n"); (remote/"campuspool/foundation.txt").write_text("shared\n"); sh("git","add",".",cwd=remote); sh("git","commit","-m","foundation",cwd=remote); sh("git","branch","codex/issue-39",cwd=remote)
    return d,remote,base
def make_inputs(d,base):
    cfg=d/"handoff.json"; cfg.write_text(json.dumps({"baseline":base,"upstream":str(d/"remote"),"foundation":{"issue":"39","marker":"campuspool/.foundation-version","value":"next-v1","branch":"codex/issue-39"},"issues":{"23":{"owner":"arjunsrikanthh","branch":"codex/issue-23","patch":"23.patch","files":"23.json","body":"23.md","title":"x"}}}))
    (d/"23.patch").write_text("diff --git a/campuspool/feature.ts b/campuspool/feature.ts\nnew file mode 100644\n--- /dev/null\n+++ b/campuspool/feature.ts\n@@ -0,0 +1 @@\n+x\n"); (d/"23.json").write_text('["campuspool/feature.ts"]'); (d/"23.md").write_text('Refs #23'); return cfg
def test_missing_foundation_fails():
    d,remote,base=fixture(); cfg=make_inputs(d,base); data=json.loads(cfg.read_text()); data["foundation"]["branch"]="codex/issue-39-missing"; cfg.write_text(json.dumps(data)); sh("git","update-ref","-d","refs/heads/main",cwd=remote); sh("git","checkout","-B","main",base,cwd=remote)
    r=sh("python3",str(PREP),"23","--output",str(d/"work"),"--source",str(remote),"--config",str(cfg),cwd=HERE); assert r.returncode!=0 and "foundation" in r.stderr.lower()
def test_stacked_base_and_scope():
    d,remote,base=fixture(); cfg=make_inputs(d,base)
    r=sh("python3",str(PREP),"23","--output",str(d/"work"),"--source",str(remote),"--config",str(cfg),cwd=HERE); assert r.returncode==0,r.stderr
    w=d/"work"; assert (w/"campuspool/.foundation-version").read_text().strip()=="next-v1"; assert sh("git","diff","--cached","--name-only",cwd=w).stdout.strip()=="campuspool/feature.ts"

def test_wrong_source_head_rejected():
    d,remote,base=fixture(); cfg=make_inputs(d,base)
    sh("git","checkout","-B","main",cwd=remote)
    (remote/"unrelated.txt").write_text("wrong source\n"); sh("git","add",".",cwd=remote); sh("git","commit","-m","unrelated",cwd=remote)
    # The configured baseline remains an ancestor, but this must still use the
    # explicit origin/main ref rather than the clone's incidental HEAD.
    r=sh("python3",str(PREP),"23","--output",str(d/"work"),"--source",str(remote),"--config",str(cfg),cwd=HERE); assert r.returncode==0,r.stderr
    assert sh("git","rev-parse","HEAD",cwd=d/"work").stdout.strip()!=base

def test_forged_metadata_rejected_before_publish():
    d,remote,base=fixture(); cfg=make_inputs(d,base)
    r=sh("python3",str(PREP),"23","--output",str(d/"work"),"--source",str(remote),"--config",str(cfg),cwd=HERE); assert r.returncode==0,r.stderr
    w=d/"work"; meta=w/".git/campuspool-handoff.json"; value=json.loads(meta.read_text()); value["owner"]="noqtar"; meta.write_text(json.dumps(value))
    r=sh("python3",str(HERE/"scripts/submit-pr.py"),"23","--path",str(w),cwd=HERE); assert r.returncode!=0

def test_verify_helper_rejects_staged_scope_tamper():
    d,remote,base=fixture(); cfg=make_inputs(d,base)
    r=sh("python3",str(PREP),"23","--output",str(d/"work"),"--source",str(remote),"--config",str(cfg),cwd=HERE); assert r.returncode==0,r.stderr
    w=d/"work"; (w/"campuspool/extra.ts").write_text("tamper\n"); sh("git","add","campuspool/extra.ts",cwd=w)
    r=sh("python3",str(HERE/"scripts/verify-prepared.py"),"23",str(w),cwd=HERE); assert r.returncode!=0 and "scope" in r.stderr.lower()
