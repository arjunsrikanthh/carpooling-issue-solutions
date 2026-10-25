# Verification results

Pinned official baseline: **0478ae0ba2549f8fba3bd44b590e91e067a46e0d**. Execution date: 26 October 2026, Asia/Kolkata.

| Gate | Actual result |
|---|---|
| Baseline original verifier | 25 frontend; 23 upstream / 67 assertions; 11 commute / 223 assertions passed |
| Consolidated patch application | Eight nonempty issue patches applied in order without conflicts; reconstructed source bytes match the integrated candidate excluding regenerated metadata |
| Source validation | PHP syntax, Git whitespace and package integrity passed |
| Expanded backend | 121 tests, 1,083 assertions, zero failures |
| Frontend | 27 tests, zero failures |
| Synthetic HTTP workflow | Publish/search/request/accept/rider confirmation/hold/cancel/history/capacity/refund passed |
| Last-seat race | 12 overlapping-client trials passed, exactly one accepted row per one-seat trip |
| Cancellation race | 6 overlapping-client trials passed, exactly one refund per paid booking |
| Fresh database | Disposable MySQL migrations passed |
| Populated rollback/reapply | Integrity migration rolled back then reapplied successfully |
| Fresh remote-source reconstruction | Full verifier exited 0 on new checkout at the pinned SHA |
| Private Actions | Pending actual run after private push |

Commands: `sh scripts/verify-integrated.sh NEW_DIRECTORY`; per issue: `sh scripts/verify-issue.sh ISSUE NEW_DIRECTORY`. Docker context is machine-specific. Both commands clone read-only source and refuse to reuse existing output directories. Runtime cleanup is limited to their own disposable clones/projects/volumes.

The selected suites are relevant Sprint 1 and integration regressions, not an assertion that every upstream historical test or every production dependency was exercised. See [exact suite counts](reports/suite-summary.json). No synthetic fixture establishes production authentication, live road routing, payments, GPS or faculty approval.

Issue #43 remains partial for approved submitted Test Plan traceability. #44 engineering preparation is complete but academic submission is incomplete. Teammate review and real contribution PRs are human workflow gates, and no official issues were closed.
