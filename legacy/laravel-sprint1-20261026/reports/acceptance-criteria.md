# Final acceptance-criterion classification

26 October 2026. This refines the engineering audit with issue-level manual/external limits. `IMPLEMENTED AND VERIFIED` below applies to the stated synthetic scope and selected tests. It never implies official issue closure or faculty approval. Actual private CI counts and run are in [VERIFICATION](../VERIFICATION.md).

| Issue | Criterion | Classification | Evidence / remaining gap |
|---|---|---|---|
| 12 | Register vehicle type, identifier and model | IMPLEMENTED AND VERIFIED | Existing owned-car API/manager and onboarding tests; proposed capacity/UI changes |
| 12 | Store and validate passenger capacity | IMPLEMENTED AND VERIFIED | Bike exactly 1, car 1–5, request/database tests |
| 12 | Show vehicle before confirmation while minimizing licence information | IMPLEMENTED AND VERIFIED in HTTP/native UI tests | Fingerprint-bound approved DTO, masked registration and mounted UI tests; visible browser demonstration unverified |
| 12 | Present truthful verification status | IMPLEMENTED AND VERIFIED | Current approval/onboarding required; synthetic fallback remains unverified/null |
| 12 | Obtain real document/licence approval | BLOCKED BY AN EXTERNAL DEPENDENCY | Human/document authority acceptance not established by fixtures |
| 12 | Reviewed owner contribution and demonstration evidence | PARTIALLY IMPLEMENTED | Proposed patch/tests exist; new real UI recording and genuine owner-reviewed PR absent |
| 21 | Record route, vehicle, future departure and seat limit | IMPLEMENTED AND VERIFIED for demo actors | Saved route/profile, date/time, one-seat API/UI tests |
| 21 | Never exceed vehicle capacity | IMPLEMENTED AND VERIFIED for bounded one-seat model | Publication is limited to 1; onboarding's minimum legal configured capacity is 1; multi-party routing not claimed |
| 21 | Eligible verified host checks in synthetic model | IMPLEMENTED AND VERIFIED | Approved cohort checks and explicit demo actor authorization; negative tests |
| 21 | Non-demo verified student can publish through campus commute endpoint | MISSING | Endpoint still requires a testing/demo actor; do not describe this as production/non-demo hosting |
| 21 | Duplicate publish, helpful errors and map-independent summaries | IMPLEMENTED AND VERIFIED in automated tests | Idempotency/product/native UI checks; fresh visual acceptance unverified |
| 21 | Preserve start_time/end_time contract | IMPLEMENTED AND VERIFIED | Existing official contract retained and search regressions run |
| 21 | Reviewed owner PR | MISSING | Not authorized/performed in official repositories |
| 22 | Direction/vehicle/future/window search | IMPLEMENTED AND VERIFIED | Official implementation plus boundary/malformed regression suite |
| 22 | Exclude full, cancelled and unpublished rides | IMPLEMENTED AND VERIFIED | Search regression/product checks |
| 22 | Provider failure and stale quote handling | IMPLEMENTED AND VERIFIED with deterministic providers | Does not establish live provider quality/availability |
| 23 | Reject own ride and duplicate pending/confirmed booking | IMPLEMENTED AND VERIFIED | Adapted attributed correctness suite, 6 tests/124 assertions |
| 23 | Owner-only accept/reject and participant status | IMPLEMENTED AND VERIFIED | Authorization and state tests plus HTTP journey |
| 23 | Atomic capacity, no overbooking on sampled last-seat contention | IMPLEMENTED AND VERIFIED for tested interleavings | 12 overlapping-client trials with durable row/capacity assertions; not universal proof |
| 23 | Failed/rejected operations preserve capacity | IMPLEMENTED AND VERIFIED | Focused correctness/product checks |
| 23 | Reviewed teammate contribution | PARTIALLY IMPLEMENTED | Genuine existing PR #47 retained; proposed adaptations need human review |
| 24 | Authorized cancellation updates booking/seats atomically | IMPLEMENTED AND VERIFIED | Product, dedicated endpoint and lifecycle/financial tests |
| 24 | Cancelled history and correct provenance retained | IMPLEMENTED AND VERIFIED | Rider/driver cancellation fields, canonical state and event assertions |
| 24 | Repeat cancellation/refund safe | IMPLEMENTED AND VERIFIED | Idempotency and unique ledger assertions |
| 24 | Concurrent cancellation consistent | IMPLEMENTED AND VERIFIED for tested interleavings | Six overlapping-client trials; one refund/ledger effect and restored capacity |
| 24 | Waitlist ordering and rematching | MISSING — SPRINT 2 | Explicitly outside Sprint 1 cancellation slice |
| 37 | FKs, unique/CHECK/indexes and restrictive deletion behavior | IMPLEMENTED AND VERIFIED | Hardening migration and 5 focused tests/23 assertions on MySQL 8 |
| 37 | Booking/cancellation transactions prevent sampled overbooking | IMPLEMENTED AND VERIFIED | Runtime transaction tests and both probes |
| 37 | No self-booking, valid seat/state and financial effects | IMPLEMENTED AND VERIFIED | Raw-SQL scoped triggers/checks, ledger unique key and focused tests |
| 37 | Empty migration and populated rollback/reapply | IMPLEMENTED AND VERIFIED | Fresh disposable MySQL and actual rollback/reapply log |
| 39 | Automated planning/application/source checks where available | IMPLEMENTED AND VERIFIED | Proposed additive checks and actual private baseline reconstruction Actions |
| 39 | Fresh-clone deterministic verification | IMPLEMENTED AND VERIFIED | New remote-source local checkout and independent CI jobs |
| 39 | Production npm build | BLOCKED BY AN EXTERNAL DEPENDENCY | Inherited Vite resources/lockfile absent; actual native frontend tests run instead |
| 39 | Real contributors create reviewed feature-branch PRs | MISSING | Human contribution/review not performed by this private-package task |
| 39 | Contribution workflow, artifacts and issue linking documented | IMPLEMENTED AND VERIFIED by document inspection | Runbook/contribution guidance, proposed scope and attribution |
| 43 | Registration/booking/capacity/cancellation/authorization tests | IMPLEMENTED AND VERIFIED | Actual selected combined suite and per-issue runs |
| 43 | Search/window/incompatibility/provider/stale-quote regressions | IMPLEMENTED AND VERIFIED | Product/search/segment suites and deterministic failure fixtures |
| 43 | Record real reproducible results | IMPLEMENTED AND VERIFIED | JUnit, logs, race JSON, fresh reconstruction, actual Actions artifacts |
| 43 | Trace to submitted/approved Test Plan | BLOCKED BY AN EXTERNAL DEPENDENCY | No approved team document located; proposed IDs and RTM remain provisional |
| 44 | Setup, DB initialization and scope documentation | IMPLEMENTED AND VERIFIED for disposable synthetic setup | Fresh-clone run, source patch and runbook |
| 44 | One-minute script and recording checklist | IMPLEMENTED AND VERIFIED by document inspection | New runbook/media review |
| 44 | Real continuous Sprint 1 working-product video uploaded/reviewed | MISSING | Existing clip rejected; fresh browser unavailable, no new video/upload |
| 44 | Sprint 2 two-minute video | MISSING — SPRINT 2 | Not part of this Sprint 1 delivery |
| 44 | Full DBMS schema/advanced-feature and required application evidence | PARTIALLY IMPLEMENTED | MySQL integrity evidence and reconciliation provided; Next.js/second paradigm/course-originality gates unmet |
| 44 | Approved SRS/SAD/STP and faculty acceptance | BLOCKED BY AN EXTERNAL DEPENDENCY | Drafts created; no historical approval fabricated |
| 44 | Genuine attribution and documented deviations | IMPLEMENTED AND VERIFIED by source/document inspection | Source map, contributions, provisional RTM and final report |
