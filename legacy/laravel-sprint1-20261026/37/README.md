# Issue #37 — Database integrity

## Requirement and existing implementation

Canonical lifecycle/seat authority and some existing constraints already exist; commute auxiliary tables lacked referential integrity.

Live upstream acceptance criteria were captured on 26 October 2026. See [AUDIT.md](../AUDIT.md) for the criterion-by-criterion gap analysis and [BASELINE.md](../BASELINE.md) for exact source revisions.

## Proposed change

Adds reversible foreign keys, indexes, value/state checks and unique booking/kind ledger identity. Normalizes publication audience sentinel 0 to NULL so new FKs remain compatible.

Official files changed:

- `prototype/campuspool-extension/Mobility/Commute/CommuteMatchingService.php`
- `prototype/campuspool-extension/migrations/2026_10_26_000100_harden_commute_integrity.php`
- `prototype/reproduction/compose.yml`
- `prototype/tests/extension/MobilityCommuteIntegrityTest.php`

## Apply and verify

Use a new disposable clone at the pinned official SHA. From this solutions repository:

```sh
sh scripts/apply-issue.sh 37 /absolute/path/to/new-official-clone
sh scripts/verify-issue.sh 37 /absolute/path/to/new-verification-directory
```

Direct prerequisite issue packages: none. The application script resolves prerequisites recursively. Patch: `solution.patch`. Source map and manifest regeneration is centralized in the application script.

Tests/evidence: MobilityCommuteIntegrityTest; financial/lifecycle/booking tests; fresh migration and rollback/reapply.

Actual execution results are recorded in [verification.md](verification.md). Worker static inspection alone does not satisfy the runtime gate.

## Limitations

Synthetic routing/authentication/demo-credit evidence only; production identity, road routing, GPS and real payments are not verified. Human review and academic acceptance are not claimed.

## Demonstration to the teacher

Show MySQL named FKs/CHECKs/indexes, a rejected orphan/negative hold, the preserved valid publication, rollback/reapply evidence and last-seat/refund race results. Use disposable databases only.

Attribution is documented in [CONTRIBUTIONS.md](../CONTRIBUTIONS.md). This is an AI-assisted proposal for teammate review, not a claim that the assigned student authored this patch.
