# Issue #44 — Documentation and demonstration evidence

## Requirement and existing implementation

Setup, requirements and attribution documents exist; no submitted/approved SRS/SAD/STP was found in inspected sources.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds a reproducible one-minute runbook and recording checklist plus faculty-template-aligned SRS, SAD, Test Plan and RTM drafts with course-gap reconciliation.

Official files changed:

- `docs/COURSE_REQUIREMENTS_RECONCILIATION.md`
- `docs/RTM_DRAFT.md`
- `docs/SAD_DRAFT.md`
- `docs/SPRINT1_DEMO_RUNBOOK.md`
- `docs/SRS_DRAFT.md`
- `docs/TEST_PLAN_DRAFT.md`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 44 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 44 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 39. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: Documentation/link/source checks and fresh-clone runbook verification.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed. The submitted/approved document versions are unconfirmed; all new document and test identifiers are proposed. Actual reviewed video upload, DBMS Next.js plus second database implementation, approved two-person eligibility and originality acceptance remain outstanding.

## Demonstration to the teacher

Use docs/SPRINT1_DEMO_RUNBOOK.md in the reconstructed application. Record a continuous real UI video after checking its actual verification labels. These drafts, logs and instructions do not establish video upload or faculty approval.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
