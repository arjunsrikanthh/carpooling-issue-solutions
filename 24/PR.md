Refs #24

Sprint 1 booking and whole-ride cancellation, retained history, exact refunds and race coverage. Sprint 2 waitlist/rematching remains pending.

This is a proposed original TypeScript implementation. The owner must inspect, understand and adapt the prepared changes, run the checks, and request a genuine independent review. AI assistance is disclosed; preparing a branch does not establish individual authorship or course approval.

Validation: `python3 scripts/verify-prepared.py 24 work/issue24` from the solutions checkout runs typecheck, lint, production build, available unit tests and isolated MySQL/Mongo integration. Full HTTP testing runs once its feature dependencies are present. See the solutions verification report for integrated results.

Dependency: shared foundation #39; target codex/issue-39 until it is merged, then refresh against main. No automatic merge or issue closure is requested.
