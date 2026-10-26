# Issue #24 — Cancellation — Sprint 1 slice

## Requirement and existing implementation

Booking cancellation/refund service and cancelled history already exist; whole-ride commute cancellation was blocked.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds cancellation provenance and waiting-payment handling; atomically cancels an entire owned ride, refunds held demo credits once, updates canonical state/event and preserves history. Adds six sampled cancellation races.

Official files changed:

- `prototype/campuspool-extension/Mobility/Commute/CommuteController.php`
- `prototype/campuspool-extension/Mobility/Commute/CommuteService.php`
- `prototype/campuspool-extension/tests/MobilityCommuteProductTest.php`
- `prototype/reproduction/cancellation-concurrency-probe.php`
- `prototype/tests/extension/MobilityCommuteCancellationTest.php`
- `prototype/tests/extension/MobilityCommuteProductTest.php`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 24 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 24 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: 23. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: MobilityCommuteCancellationTest; cancellation case in MobilityCommuteProductTest; financial/lifecycle tests; cancellation HTTP race probe.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed. Waitlist/rematching remains Sprint 2.

## Demonstration to the teacher

Cancel a paid synthetic booking, inspect retained history, restored seat and one refund. Repeat cancellation. Demonstrate owner-only whole-ride cancellation through the commute transition endpoint and inspect the lifecycle event.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
