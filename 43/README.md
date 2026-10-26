# Issue #43 — [N8] Testing against approved Test Plan

Assigned owner: `@NikhilJoshi441`.

Executable test-plan contribution, search regression and the cross-feature production HTTP journey. Approved Test Plan mapping remains provisional until human approval.

From a clone of the solutions repository:

```sh
python3 scripts/prepare-pr.py 43 --output work/issue43
python3 scripts/verify-prepared.py 43 work/issue43
# Read/edit the staged diff and PR body, then publish with your assigned account:
python3 scripts/submit-pr.py 43 --path work/issue43 --publish
```

The helper creates a separate official-repository checkout. Do not push the solutions repository to the official repo. This patch contains only the paths listed in `files.json`; it adds no legacy application source. Required tools: Node.js 24, Python 3, Git, GitHub CLI and Docker.

The shared foundation must exist on official main or official codex/issue-39 before preparation. Feature branches can be prepared in parallel; retarget/retest after the foundation merge.

Draft PRs and `Refs #N` preserve review and existing issue status. Teammates must explain their own changes and resolve review comments. The approved Test Plan, faculty acceptance and working-product video are separate outstanding deliverables.
