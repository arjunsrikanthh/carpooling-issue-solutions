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
| Private Actions | All 9 jobs succeeded: [actual run](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242) at `2c2efd278472650e2c32964cf541a05a52ee48c1` |

Commands: `sh scripts/verify-integrated.sh NEW_DIRECTORY`; per issue: `sh scripts/verify-issue.sh ISSUE NEW_DIRECTORY`. Docker context is machine-specific. Both commands clone read-only source and refuse to reuse existing output directories. Runtime cleanup is limited to their own disposable clones/projects/volumes.

The selected suites are relevant Sprint 1 and integration regressions, not an assertion that every upstream historical test or every production dependency was exercised. See [exact suite counts](reports/suite-summary.json). No synthetic fixture establishes production authentication, live road routing, payments, GPS or faculty approval.

Issue #43 remains partial for approved submitted Test Plan traceability. #44 engineering preparation is complete but academic submission is incomplete. Teammate review and real contribution PRs are human workflow gates, and no official issues were closed.

Current overall acceptance is detailed in [FINAL_REPORT.md](FINAL_REPORT.md) and [criterion classifications](reports/acceptance-criteria.md). #12, #21 and #39 remain partial overall for real approval/non-demo hosting/visible demonstration or human reviewed-PR criteria. This final report supersedes pending CI text in the earlier engineering audit.

## Actual private Actions results

Independent runs include their declared prerequisites. Counts overlap and must not be summed. The isolated #37 run passes the 25 baseline frontend tests; the other eight runs pass 27 frontend tests including the two added UI checks. Frontend failures are zero. Backend failures/errors/skips were zero in all nine jobs.

| Scope | Backend tests | Assertions | Frontend tests | Result |
|---|---:|---:|---:|---|
| [integrated](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692145) | 121 | 1083 | 27 | PASS |
| [12](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692380) | 46 | 381 | 27 | PASS |
| [21](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692369) | 47 | 391 | 27 | PASS |
| [23](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692351) | 19 | 367 | 27 | PASS |
| [24](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692365) | 40 | 537 | 27 | PASS |
| [37](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692394) | 35 | 370 | 25 | PASS |
| [39](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692328) | 121 | 1083 | 27 | PASS |
| [43](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692337) | 121 | 1083 | 27 | PASS |
| [44](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242/job/121284692346) | 121 | 1083 | 27 | PASS |
