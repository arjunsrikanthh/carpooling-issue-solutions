# Issue #43 — Testing and closed #22 regression

## Requirement and existing implementation

Official matching already implements direction/vehicle/time windows and Nikhil ranking. Existing package contains integration patches that were missing from running source.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds malformed/state/boundary/provider regression coverage and reconciles trusted approved-driver/profile/routing integration with the actual application. Preserves guards for ordinary untrusted trips.

Official files changed:

- `prototype/app/Repository/PassengersRepository.php`
- `prototype/app/Repository/TripRepository.php`
- `prototype/app/Services/Logic/PassengersManager.php`
- `prototype/app/Services/Logic/TripsManager.php`
- `prototype/campuspool-extension/Mobility/Admission/DriverReservationPolicy.php`
- `prototype/campuspool-extension/Mobility/Recurrence/ProgramService.php`
- `prototype/campuspool-extension/Mobility/Recurrence/RecurrenceCreationContext.php`
- `prototype/campuspool-extension/Mobility/Segments/MatchController.php`
- `prototype/campuspool-extension/Mobility/Segments/SegmentBookingService.php`
- `prototype/tests/extension/MobilitySearchRegressionTest.php`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 43 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 43 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 24. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: MobilitySearchRegressionTest; MobilityDriverProfileBridgeTest; MobilitySegmentBookingTest; all integrated Sprint 1 suites.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed. The submitted/approved document versions are unconfirmed; all new document and test identifiers are proposed.

## Demonstration to the teacher

Run the focused search and canonical booking suites; demonstrate inclusive windows, unavailable/full/cancelled rides and fail-closed provider behavior. Compare the proposed RTM with the faculty template. #22 stays closed and is not duplicated.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
