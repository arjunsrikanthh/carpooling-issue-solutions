# Issue #21 verification

Engineering status: **local integration verified; independent private Actions execution pending**.

Pinned official baseline: `0478ae0ba2549f8fba3bd44b590e91e067a46e0d`.
Application order: `37, 12, 21, 23, 24, 43, 39, 44`. Fresh reconstruction used only these source patches and centrally regenerated integrity metadata.

Executed 26 October 2026:

```sh
SOLUTIONS_COMPOSER_CACHE=/path/to/disposable/composer-cache DOCKER_CONTEXT=colima-campuspool-solutions sh scripts/verify-integrated.sh /path/to/new-output
```

Actual result: exit 0; **121 backend tests / 1,083 assertions; 27 frontend tests; 0 failures**. PHP source syntax checks, MySQL fresh migrations, health and `/mobility/` passed. Synthetic publication → search → request → acceptance → rider confirmation → payment hold → cancellation → retained history → restored seat/refund passed. Twelve sampled last-seat races and six sampled cancellation races passed; timestamp overlap establishes overlapping HTTP clients, not universal correctness under all interleavings. Populated-database rollback/reapply passed.

See [suite evidence](../reports/suite-summary.json), [backend JUnit](../reports/backend.junit.xml), [booking races](../reports/booking-races.json), [cancellation races](../reports/cancellation-races.json), and [rollback](../reports/migration-rollback.log). Counts overlap between issue coverage and must not be added across packages.

Run this package with prerequisites independently using `sh scripts/verify-issue.sh 21 /path/to/new-output`. Its actual private CI outcome will be recorded in [VERIFICATION.md](../VERIFICATION.md).

Acceptance of a genuine teammate PR and any required human review remains outside this proposed engineering verification.
