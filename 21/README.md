# Issue #21 — Offer a car or bike ride

## Requirement and existing implementation

Existing publication uses saved home/campus coordinates and departure times, eligible demo drivers and idempotency receipts.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds an explicit one-passenger seat field and backend/service limits, client eligibility guard, mounted UI assertions and invalid/duplicate publication regressions.

Official files changed:

- `prototype/campuspool-extension/Mobility/Commute/CommuteController.php`
- `prototype/campuspool-extension/Mobility/Commute/CommuteMatchingService.php`
- `prototype/campuspool-extension/tests/MobilityCommuteProductTest.php`
- `prototype/campuspool-extension/web/commute.mjs`
- `prototype/campuspool-extension/web/driver-onboarding-ui.test.mjs`
- `prototype/tests/extension/MobilityCommuteProductTest.php`
- `prototype/tests/frontend/test-commute-ui.mjs`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 21 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 21 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 37, 12. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: MobilityCommuteProductTest; mounted driver publication test.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed. Sprint 1 publication is deliberately limited to one passenger; onboarding capacity does not imply multi-party route support or official legal certification.

## Demonstration to the teacher

Sign in as a synthetic driver, set the saved route, publish a future car/bike offer with the displayed one-seat limit, and show the new ride. Invalid counts are rejected by API tests. The saved route remains readable without Maps.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
