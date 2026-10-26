# Issue #39 — Bootstrap Next.js TypeScript foundation and CI

Assigned owner: `@arjunsrikanthh`.

Original Next.js/TypeScript stack migration foundation: shared auth/roles/approval, MySQL schema, fixed-stop search, API contracts, setup and CI. This deliberately includes shared bootstrap work beyond the CI-only issue title; review the migration before integration.

From a clone of the solutions repository:

```sh
python3 scripts/prepare-pr.py 39 --output work/issue39
python3 scripts/verify-prepared.py 39 work/issue39
# Read/edit the staged diff and PR body, then publish with your assigned account:
python3 scripts/submit-pr.py 39 --path work/issue39 --publish
```

The helper creates a separate official-repository checkout. Do not push the solutions repository to the official repo. This patch contains only the paths listed in `files.json`; it adds no legacy application source. Required tools: Node.js 24, Python 3, Git, GitHub CLI and Docker.

Prepare #39 first. Other teammates can prepare after its official branch exists.

Draft PRs and `Refs #N` preserve review and existing issue status. Teammates must explain their own changes and resolve review comments. The approved Test Plan, faculty acceptance and working-product video are separate outstanding deliverables.
