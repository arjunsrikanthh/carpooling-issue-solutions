# Sprint 1 integration contract

The merge order is dependency-driven, not a hidden commit chain:

1. #39 establishes the shared Next.js App Router, TypeScript, SQL schema,
   authentication, core API helpers, and CI.
2. #12 vehicles, #21 offers, #23 bookings, #24 cancellation, and #37 advanced
   SQL integrity plus MongoDB activity/database evidence each change only their
   declared modules on top of the foundation. Search/common functionality is
   part of the rebuilt foundation; #43 is the approved-Test-Plan testing issue,
   with its own search/test-plan evidence only.
3. #44 supplies the Sprint 1 documentation and traceability package.

While #39 is open, feature PRs target `codex/issue-39` and explicitly document
that dependency. Once #39 is merged, the leader may recreate feature branches
from official `main`; no fake prerequisite commits are allowed. Every PR must
remain independently attributable to its assigned GitHub account and must be a
draft until reviewed.

The verifier requires the application `npm ci`, `npm run typecheck`,
`npm run build`, and `npm test` checks, plus an issue-scoped test file for each
feature/test-plan issue. Documentation #44 is checked for documentation
artifacts rather than a fake application test. If the disposable MySQL/Mongo compose file exists, it is started
for integration checks and removed afterward. A green foundation test suite is
not accepted as evidence for an untested feature.
