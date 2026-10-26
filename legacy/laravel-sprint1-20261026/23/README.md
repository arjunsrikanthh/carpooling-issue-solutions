# Issue #23 — Request and confirm a seat

## Requirement and existing implementation

Quote-bound requests, authorization, row locks and owner accept/reject already exist. PR #47 contains genuine proposed booking verification.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adapts attributed PR #47 tests/probe to the current time-window contract and adds confirmed-duplicate verification. No redundant rewrite of working application code.

Official files changed:

- `prototype/campuspool-extension/tests/MobilityBookingCorrectnessTest.php`
- `prototype/reproduction/booking-concurrency-probe.php`
- `prototype/reproduction/compose.booking.yml`
- `prototype/tests/extension/MobilityBookingCorrectnessTest.php`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 23 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 23 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 21. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: MobilityBookingCorrectnessTest; MobilityCommuteProductTest; 12-trial HTTP/MySQL last-seat probe.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed.

## Demonstration to the teacher

Use separate synthetic accounts: search with an explicit departure window, request a quote-bound seat, accept as the owner, inspect the rider confirmation, and show the concurrency report. No real identity or payment verification is implied.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
