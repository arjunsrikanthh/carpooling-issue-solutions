# Issue #39 — GitHub Actions and PR workflow

## Requirement and existing implementation

Official main already has green documentation/application CI; rewriting it wholesale is unnecessary.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds JS/Python/PHP syntax checks without generated-file contamination, full Sprint 1 regressions, synthetic stateful smoke checks and sampled HTTP races. Private-repository CI reconstructs the pinned baseline.

Official files changed:

- `.github/workflows/application.yml`
- `prototype/config/.env.example`
- `prototype/reproduction/smoke-booking.py`
- `prototype/reproduction/verify-package.sh`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 39 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 39 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 43. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: Private actual Actions run; per-issue and integrated fresh-clone scripts; package/source-map integrity; runtime smoke and migrations.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed.

## Demonstration to the teacher

Open the private Actions run and its real artifacts; explain the pinned baseline, patch order and source checks. Teammates still need their own genuine contribution branches/PRs and human review.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
