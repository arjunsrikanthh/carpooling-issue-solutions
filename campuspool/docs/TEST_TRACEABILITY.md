# Sprint 1 executable test mapping

This is a proposed mapping to the new application contract; no instructor-approved Test Plan was located. Approval and video evidence remain pending.

| Requirement | Executable evidence |
| --- | --- |
| Authentication, opaque sessions, pending approval, cross-origin protection | `tests/issue-39.test.ts` |
| Car/bike capacity, registration, administrator review | `tests/issue-12.test.ts` |
| Eligible host, future departure, vehicle capacity and time conflict | `tests/issue-21.test.ts` |
| Private vehicle details, explicit Kolkata search window, signed quote | `tests/issue-43.test.ts` |
| Self/duplicate/foreign decision, stale quote, insufficient credit, final-seat race | `tests/issue-23.test.ts` |
| Cancellation, exact-once refund, rider/host/whole-ride races, history | `tests/issue-24.test.ts` |
| Real SQL constraints, view/procedure/triggers/index and Mongo failure/recovery | `tests/issue-37.test.ts` and its helper suites |
| Full production HTTP journey, role boundaries, 12 final-seat and 6 cancellation races | `tests/http.e2e.test.ts` |

Every feature carries its own tests. #43 owns this cross-feature mapping and the full HTTP suite. A partial feature checkout can run its available SQL tests; the complete HTTP journey requires the remaining feature PRs. A skipped test is not a passing integration test.
