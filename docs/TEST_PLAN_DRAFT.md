# Sprint 1 test plan — CampusPool (draft)

**Status:** Proposed test plan; not submitted or approved. The commands and results below are placeholders until the implementation and test fixtures exist. Do not report a pending row as passed.

## 1. Test levels

- Unit/domain: validation, quote, masking, role and state rules.
- API/integration: route handlers against disposable MySQL and MongoDB services with environment credentials.
- Concurrency/integrity: booking/cancellation races, idempotency retries, migration rollback/reapply, FK/check/ledger guards.
- UI/system: real Next.js forms, role-based navigation, search, offer, booking and cancellation journeys.
- Acceptance: requirements traceability, instructor review, genuine member review, and continuous working-product demonstration.

## 2. Proposed cases

| ID | Requirement | Test | Expected result | Status |
| --- | --- | --- | --- | --- |
| T39-01 | FR-01 | Register, log in, inspect `/api/auth/me`, log out | Pending user/session lifecycle; no token leakage | Not run |
| T39-02 | FR-02 | Admin approves/suspends member; non-admin attempts same | Admin succeeds; unauthorized request rejected | Not run |
| T12-01 | FR-03 | Register BIKE capacity 2 and CAR capacity 6; review | Invalid capacities rejected; approved DTO is correct | Not run |
| T21-01 | FR-04 | Publish valid and invalid future offers; retry same idempotency key | One valid ride; invalid/overlap/duplicate requests rejected | Not run |
| T43-01 | FR-05 | Execute the approved Test Plan's search/matching cases against the shared baseline, including closed #22 regression boundaries | Actual traceability and deviations recorded; no new search implementation is implied | Not run |
| T23-01 | FR-06/07 | Request, duplicate request, stale quote, owner accept/reject | Correct status/authorization; one seat and one hold | Not run |
| T23-02 | FR-06/07 | Concurrent last-seat requests | At most one accepted request; no negative capacity/duplicate hold | Not run |
| T24-01 | FR-08 | Rider/driver cancellation, repeated cancellation, owner offer cancellation | Authorized one-time refund/history/capacity transition | Not run |
| T37-01 | FR-09/10 | Commit event, run worker twice, inspect Mongo and SQL evidence | Unique projection, safe retry, view/procedure/guard output | Not run |
| T39-03 | FR-11 | Cross-origin mutation, missing idempotency, malformed body | Rejected with safe error envelope | Not run |
| ACC-01 | Course/SE | Run clean setup, capture real UI and link reviewed PRs | Evidence package complete | Pending manual evidence |

## 3. Execution record

When tests are run, record commit SHA, environment (disposable DB names only), exact command, timestamp, pass/fail count, and artifact path. A future CI run may attach output here; this draft intentionally invents no test result.

## 4. Exit criteria

All Must cases pass with reproducible output; no open severity-1 integrity/security issue; focused and full CI are green; each teammate explains their own changed files; SRS/SAD/STP are reviewed; and the working-product video is actually recorded and submitted. The #43 Test Plan approval/traceability gate is not complete merely because this draft exists. Faculty approval and video remain outside this draft until evidenced. Issue #40 and waitlist/rematching remain Sprint 2/pending official scope.
