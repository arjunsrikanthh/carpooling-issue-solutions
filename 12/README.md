# Issue #12 — Driver and vehicle details

## Requirement and existing implementation

Existing canonical car registration, owned-vehicle validation and document review already exist.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds persisted passenger capacity (bike 1; car 1–5), database capacity checks and masked current approved vehicle summaries before a seat request.

Official files changed:

- `prototype/campuspool-extension/Mobility/Commute/CommuteMatchingService.php`
- `prototype/campuspool-extension/Mobility/Trust/DriverOnboardingController.php`
- `prototype/campuspool-extension/migrations/2026_10_26_000100_add_passenger_capacity_to_driver_onboarding.php`
- `prototype/campuspool-extension/tests/DriverOnboardingHttpTest.php`
- `prototype/campuspool-extension/tests/MobilityCommuteProductTest.php`
- `prototype/campuspool-extension/web/app.js`
- `prototype/campuspool-extension/web/commute.mjs`
- `prototype/campuspool-extension/web/driver-onboarding-ui.test.mjs`
- `prototype/tests/extension/DriverOnboardingHttpTest.php`
- `prototype/tests/extension/MobilityCommuteProductTest.php`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 12 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 12 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: none. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: DriverOnboardingHttpTest; MobilityCommuteProductTest; mounted onboarding/commute UI tests.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed. Sprint 1 publication is deliberately limited to one passenger; onboarding capacity does not imply multi-party route support or official legal certification.

## Demonstration to the teacher

Use /mobility-pilot to register a synthetic owned vehicle and submit its checklist. Compare pending vs current approved onboarding; inspect masked vehicle details before requesting a seat. Demo-session eligibility is distinct from real approval.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
