# Final Sprint 1 solution handoff

26 October 2026 (Asia/Kolkata). These are AI-assisted proposed implementations for review. Original repositories were read only. **Engineering verification covers a bounded synthetic application; full academic issue acceptance is not complete.**

## A. Repository

[arjunsrikanthh/carpooling-issue-solutions](https://github.com/arjunsrikanthh/carpooling-issue-solutions) is **PRIVATE**, owned by the personal account `arjunsrikanthh`, outside CampusPool. All eight expected folders contain nonempty source patches, file lists, instructions and verification reports. No collaborators were invited or visibility changed after creation.

Tested distribution commit: `2c2efd278472650e2c32964cf541a05a52ee48c1`. Final reporting changes do not alter its source patches, scripts or workflow; [patch hashes](reports/patch-sha256.json) identify the tested payload.

## B. Baselines inspected

| Source | Exact revision |
|---|---|
| Official `CampusPool/carpooling:main` — compatibility authority | `0478ae0ba2549f8fba3bd44b590e91e067a46e0d` |
| Workspace `CampusPool/carpooling-workspace:main` | `f103f7bff32bcb24712e10d6747670aa06f8f24b` |
| Local MobilityPlatform `codex/software-workflows` | `faccb66ebb65512cfca41116109609a7120111de` |
| Local Carpooling `main` | `6aacafbb233598d88e3e10bc31d248839792272b` |
| Workspace Zayaan feature branch | `d77b0e317aee0ca211abf3146be0600e80ed35a4` |
| Workspace portable-demo fix | `3921b09161ff8887e429166b13a2d7e245b2b3a5` |
| Workspace import branch | `0f6b37aa4b59cf5c724c18b67527cb7319b9d3bf` |
| Existing open official PR #47 | `c240b5819c79f93f5a9ebb286c88ca754df68d2b` |

All 235 official extension files were compared by content: six differ from workspace and nine from local. The older Zayaan branch removes current departure-window parameters, so it was not imported. Nikhil's official window/ranking changes remain authoritative. See [baseline](BASELINE.md), [audit](AUDIT.md), [comparison](audit/source-comparison.json) and [attribution](CONTRIBUTIONS.md).

## C. Status

“VERIFIED engineering” means the proposed bounded implementation, patch application, focused tests and combined disposable runtime passed. It does not mean the official issue was closed, a teammate authored/reviewed the proposal, or faculty accepted it. Every official open issue remains open; #22 remains closed.

| Issue | Existing implementation | New solution | Tests | Integrated | Status |
|---|---|---|---|---|---|
| [12](12/README.md) | Canonical vehicle registration and manual review | Capacity persistence/validation, masked current-approved vehicle DTO and UI | Onboarding, car API/manager, product and mounted UI | Pass | **PARTIAL overall**; synthetic engineering verified; real approval/live visual acceptance missing |
| [21](21/README.md) | Synthetic publication, profiles and idempotency | Explicit one-seat form/API/service limit and eligibility guard | Product/publication negative and UI checks | Pass | **PARTIAL overall**; commute publication remains demo-gated; non-demo hosting missing |
| [23](23/README.md) | Booking locks, authorization and quoted requests | Adapt attributed PR #47 tests; confirmed-duplicate coverage and HTTP race probe | 6 focused / 124 assertions; 12 sampled races | Pass | **VERIFIED engineering** in the synthetic Sprint 1 slice; reviewed owner contribution remains a human gate |
| [24](24/README.md) | Booking cancellation and refund primitive | Provenance, waiting-payment state and whole-ride atomic cancellation/refund/history/event fixes | 1 dedicated / 27 assertions plus product/financial/lifecycle and 6 sampled races | Pass | **VERIFIED engineering for Sprint 1 cancellation**; waitlist/rematching remains Sprint 2 |
| [37](37/README.md) | Service transactions and partial relational rules | FKs, indexes, CHECK/unique rules, scoped raw-SQL triggers and safe rollback | 5 focused / 23 assertions, fresh migrations and populated rollback/reapply | Pass | **VERIFIED engineering** on MySQL 8 |
| [39](39/README.md) | Official CI already green | Additive proposed checks, deterministic setup and private 9-job verification | Actual private Actions and fresh-clone checks | Pass | **PARTIAL overall**; CI engineering verified; genuine reviewed contribution PRs not performed |
| [43](43/README.md) | Official matching/window tests | Search boundaries and missing canonical profile/segment integration, provisional RTM | Search 4/33, bridge 3/10, segment 12/265 and combined suites | Pass | **PARTIAL**; engineering verified, submitted/approved Test Plan unavailable |
| [44](44/README.md) | Historical setup/sprint docs | Runbook, one-minute script, SRS/SAD/STP/RTM drafts and academic gap reconciliation | Fresh setup/runtime and actual evidence | Pass | **PARTIAL academic acceptance**; real working-product recording/upload and course gates outstanding |
| #22 regression | Closed official search issue | Preserve current windows/ranking; no redundant package | Product + search regression | Pass | **VERIFIED engineering regression**; issue remains closed |

## D. Detailed results

Each folder's README identifies all changed official files, exact application/test commands, prior functionality, proposed changes and remaining limits. Complete file lists also appear below. Test counts overlap across issues and must not be summed.

- **#12:** Bike capacity is exactly one passenger; car onboarding accepts one to five. The database and request validation reject invalid capacities. Rider vehicle display uses the currently linked approved host application, matching vehicle fingerprint and approved onboarding; registration is masked. It no longer invents approval or picks an arbitrary car. Demo actors lacking those records correctly display unverified/null metadata. No real licensing authority was queried, and no new visual browser acceptance was established.
- **#21:** Publication accepts the explicit/default one passenger, rejects zero/multiple/malformed counts, retains future-departure and idempotency behavior, and preserves `start_time` / `end_time`. The one-passenger limit bounds the existing route/detour model even if the registered car has more capacity. The campus commute endpoint still calls `requireDemo`; this is not completed non-demo student hosting or multi-passenger dispatch.
- **#23:** Existing sound booking code was retained. Attributed PR #47 tests were adapted to the current API; self-booking, foreign-driver operations, duplicate pending/confirmed requests, rejection/capacity preservation and atomic last-seat behavior are exercised. Twelve sampled overlapping-client races each ended with one accepted and one pending booking; retry sees no seat. Client timestamp overlap does not prove every internal database-lock interleaving was sampled.
- **#24:** Rider/driver cancellation keeps history and records provenance; whole-ride cancellation now captures its injected service/idempotency context, updates both canonical trip and lifecycle, appends one event and refunds each held booking once. The dedicated endpoint test adds 27 assertions. Six sampled concurrent cancellation trials confirm one refund and ledger entry, wallet correctness, retained history and restored capacity. Waitlist storage/order/rematching is missing and outside this Sprint 1 slice.
- **#37:** Publication audience sentinel zero is normalized to nullable NULL before user FKs are introduced. Commute auxiliary tables receive FKs/indexes, ledger uniqueness and value constraints; scoped triggers reject raw-SQL self-booking and invalid passenger state without breaking conductor rows. Rollback drops supporting FKs before indexes. Fresh empty migrations and rollback/reapply with populated synthetic data passed. This does not certify the safety of arbitrary production data; a real migration requires normal review/backup planning.
- **#39:** Existing official green workflows were preserved as baseline. The proposed official patch adds relevant source/frontend/backend/integrity/smoke/race checks and fixes admin-only migration credentials. The private workflow reconstructs the pinned baseline separately for all eight issue packages with prerequisites and for the combined implementation. Inherited missing Vite resources/lockfile mean no npm production build is claimed; native-module checks cover the served frontend. Feature-branch review by real teammates remains outstanding.
- **#43:** Regression tests cover inclusive/malformed windows, incompatible direction/vehicle, full/cancelled/unpublished rides, provider failure and stale quote behavior. Running broader suites exposed already-shipped profile/routing patches absent from runtime source; focused integration now uses trusted vehicle/route context and canonical segment admission. Campus-local persisted schedule handling and a scoped internal recurrence context preserve existing tests and ordinary creation limits; no new Sprint 2 feature is claimed. Search 4 tests/33 assertions, profile bridge 3/10 and segment 12/265 passed. The RTM contains proposed IDs, not invented submitted test IDs.
- **#44:** Six proposed documentation files include requirements, architecture with two sequence diagrams, Test Plan, RTM, course reconciliation and a one-minute recording runbook. Gmail/Drive supplied actual faculty requirements/templates, not evidence of team submission/approval. The existing 60-second candidate recording was rejected after sampled frames showed chat/GitHub instead of the working journey; it and unrelated UI frames were not published. [Media review](44/MEDIA_REVIEW.md) records this.

## E. Integration and execution

Application order: **37 → 12 → 21 → 23 → 24 → 43 → 39 → 44**. `solutions.json` declares dependencies; individual verification automatically applies prerequisites. Issue packages are distinct review units, not all standalone without dependencies.

Conflicts resolved include the audience-zero FK mismatch, FK/index rollback order, approval metadata provenance, missing service/seat closure captures, whole-trip canonical lifecycle/event consistency, absent runtime profile/segment integration, timezone interpretation and non-writing Python syntax compilation. The first private run additionally exposed that the campus timezone setup was assigned to later package 39 even though 43 required it; it was moved to 43 without changing assertions or the final combined application bytes. Source metadata is regenerated centrally after each patch rather than restoring stale manifests.

Actual local fresh-remote-source result: **121 PHP tests, 1,083 assertions; 27 frontend tests; zero failures**, plus PHP syntax, integrity, fresh MySQL migrations and populated rollback/reapply. This is the selected relevant Sprint 1/integration suite, not every historical upstream test. [Exact suite counts](reports/suite-summary.json), [JUnit](reports/backend.junit.xml), [frontend](reports/frontend.log), [race results](reports/booking-races.json), [cancellation races](reports/cancellation-races.json), [rollback](reports/migration-rollback.log).

The synthetic HTTP journey passed: driver demo session → publish → rider search → request → host accept → rider confirmation → demo-credit hold → cancellation → retained history → restored capacity and exactly one refund. The served page and health endpoint returned 200. This is HTTP and native UI test evidence; a fresh visible browser journey and recording were not verified because browser automation returned “Local browser use is disabled in Work settings.” Real identity, real road routing, GPS and payments are not established.

The [initial private run failure](reports/initial-ci-failure.json) is retained: eight jobs passed, while standalone #43 exposed the timezone prerequisite-order defect. The setup hunk was moved to the package that needs it; no test assertion was removed or weakened. The [final source comparison](reports/final-source-comparison.json) records that runtime application bytes remain unchanged from the passing combined proof; three documentation files were then corrected.

**Private Actions:** **SUCCESS — all 9 jobs passed**, including combined reconstruction and all eight individual issue/prerequisite runs. [GitHub Actions run](https://github.com/arjunsrikanthh/carpooling-issue-solutions/actions/runs/40231726242), tested distribution commit `2c2efd278472650e2c32964cf541a05a52ee48c1`. [Actual per-job counts and JUnit evidence](reports/actions-summary.json).


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

Reproduce in a new disposable directory:

```sh
git clone https://github.com/arjunsrikanthh/carpooling-issue-solutions.git
cd carpooling-issue-solutions
sh scripts/verify-integrated.sh /absolute/path/to/new-output
sh scripts/verify-issue.sh 23 /absolute/path/to/another-new-output
```

Requires Docker Engine/Compose, Git, Python 3.9+, compatible Node, network dependency access and free loopback port 18180. Configure your own Docker context. Verification refuses an existing output path and cleans only its own generated runtime and Compose project. See [integration details](INTEGRATION.md).

## F. Team handoff

| Member | Review folders | Responsibility |
|---|---|---|
| Zayaan | `12/`, `21/` | Understand capacity, vehicle provenance/UI and demo publication limits; demonstrate the visible UI and address non-demo acceptance separately |
| Arjun | `23/`, `39/`, `44/` | Review existing PR #47 provenance, reproduce races/Actions, reconcile documentation and record the real video |
| Nithesh | `24/`, `37/` | Review cancellation/refunds, raw DB constraints and rollback; keep waitlist/rematching as Sprint 2 |
| Nikhil | `43/`, #22 regressions | Review window/ranking preservation, canonical integration and map proposed tests to the faculty-approved plan when available |

Teammates were not granted private repository access by this task. The owner must share the assigned packages through an approved channel or separately authorize repository access.

For private rehearsal, clone the solutions repo, use `verify-issue.sh` and inspect each real patch/file list and actual outputs. For an eventual genuine contribution, start a new personal feature branch from the agreed official baseline and apply/adapt only the assigned changes plus agreed prerequisites; shared files must be integrated serially in the documented order. The strict apply script requires HEAD exactly at the pinned baseline, so do not run it on an unrelated or advanced branch. It stages changes without resetting them. Review `git diff --cached`, understand the changes and produce your own meaningful test evidence. Only after separate owner authorization should anyone push a real contribution branch or open/review an official PR. No such official actions were performed here; these proposals do not establish individual student authorship.

## G. Academic and external caveats

- SE's Part-2 brief expects following submitted SRS/SAD/STP, genuine member contributions/review and a one-minute Sprint 1 working-product video; Sprint 2 has separate work and a two-minute video. Faculty templates from 31 August, the 6 October brief and DBMS 9 October reminder were inspected read-only.
- No team-submitted/approved SRS, SAD or Test Plan was found in the inspected Gmail/Drive/local sources. The Drive “SE+ DBMS” file is a proposal. New SRS/SAD/Test Plan/RTM files are drafts requiring team and faculty reconciliation; absence from this search is not proof no version exists elsewhere.
- Real document/driver approval, non-demo student hosting and visible UI/video acceptance remain missing or unverified. No fake approval, screenshot, video or test result is provided.
- DBMS Level 3 separately requires a Next.js web application, authenticated roles, two database paradigms, advanced database demonstrations, approved two-member eligibility, documentation and originality acceptance. This Laravel/native-JS/MySQL synthetic slice does not satisfy those requirements. A private solution repository is not the required public final academic submission; privacy has not been changed.
- Upstream Carpoolear/imported CampusPool code stays attributed. The inherited GPL text/MIT metadata discrepancy and instructor reuse/originality approval remain unresolved. Do not present imported/AI-assisted work as independently authored student implementation.
- Reviewed teammate PRs, final course uploads, both required videos and faculty acceptance have not been completed by this task. No official issue should be marked complete solely from this package.

## H. Protected resources

Final read-only snapshots confirm both original local checkouts retain their starting HEAD, branch, Git status and worktree inventory. Both CampusPool repositories retain their inspected settings, branch refs and PR selected state. All nine inspected issue states/bodies/labels/assignments/comments match the starting snapshots: eight remain open, #22 remains closed. No official push, merge, PR/issue edit, comment, setting change, invitation or visibility mutation was made. Original databases were never used for testing. [Sanitized protection evidence](reports/protected-resources.json).

Only task-owned isolated clones, disposable synthetic Compose projects and the new private personal repository were written. Generated database containers/volumes were removed; existing Docker profiles were preserved. A bounded tracked-file review found no selected credential signatures, database/media artifacts, original course attachments or raw mailbox dumps in the publication. [Review scope and result](reports/distribution-review.json). This is a bounded review, not a guarantee against every secret format.

## Complete changed-file index

### Issue #12 (10 files)

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

### Issue #21 (7 files)

- `prototype/campuspool-extension/Mobility/Commute/CommuteController.php`
- `prototype/campuspool-extension/Mobility/Commute/CommuteMatchingService.php`
- `prototype/campuspool-extension/tests/MobilityCommuteProductTest.php`
- `prototype/campuspool-extension/web/commute.mjs`
- `prototype/campuspool-extension/web/driver-onboarding-ui.test.mjs`
- `prototype/tests/extension/MobilityCommuteProductTest.php`
- `prototype/tests/frontend/test-commute-ui.mjs`

### Issue #23 (4 files)

- `prototype/campuspool-extension/tests/MobilityBookingCorrectnessTest.php`
- `prototype/reproduction/booking-concurrency-probe.php`
- `prototype/reproduction/compose.booking.yml`
- `prototype/tests/extension/MobilityBookingCorrectnessTest.php`

### Issue #24 (6 files)

- `prototype/campuspool-extension/Mobility/Commute/CommuteController.php`
- `prototype/campuspool-extension/Mobility/Commute/CommuteService.php`
- `prototype/campuspool-extension/tests/MobilityCommuteProductTest.php`
- `prototype/reproduction/cancellation-concurrency-probe.php`
- `prototype/tests/extension/MobilityCommuteCancellationTest.php`
- `prototype/tests/extension/MobilityCommuteProductTest.php`

### Issue #37 (4 files)

- `prototype/campuspool-extension/Mobility/Commute/CommuteMatchingService.php`
- `prototype/campuspool-extension/migrations/2026_10_26_000100_harden_commute_integrity.php`
- `prototype/reproduction/compose.yml`
- `prototype/tests/extension/MobilityCommuteIntegrityTest.php`

### Issue #39 (3 files)

- `.github/workflows/application.yml`
- `prototype/reproduction/smoke-booking.py`
- `prototype/reproduction/verify-package.sh`

### Issue #43 (11 files)

- `prototype/app/Repository/PassengersRepository.php`
- `prototype/app/Repository/TripRepository.php`
- `prototype/app/Services/Logic/PassengersManager.php`
- `prototype/app/Services/Logic/TripsManager.php`
- `prototype/campuspool-extension/Mobility/Admission/DriverReservationPolicy.php`
- `prototype/campuspool-extension/Mobility/Recurrence/ProgramService.php`
- `prototype/campuspool-extension/Mobility/Recurrence/RecurrenceCreationContext.php`
- `prototype/campuspool-extension/Mobility/Segments/MatchController.php`
- `prototype/campuspool-extension/Mobility/Segments/SegmentBookingService.php`
- `prototype/config/.env.example`
- `prototype/tests/extension/MobilitySearchRegressionTest.php`

### Issue #44 (6 files)

- `docs/COURSE_REQUIREMENTS_RECONCILIATION.md`
- `docs/RTM_DRAFT.md`
- `docs/SAD_DRAFT.md`
- `docs/SPRINT1_DEMO_RUNBOOK.md`
- `docs/SRS_DRAFT.md`
- `docs/TEST_PLAN_DRAFT.md`
