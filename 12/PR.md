Refs #12

Vehicle registration and administrator review; car/bike capacity validation. Public ride details use the shared masked vehicle projection.

This is a proposed original TypeScript implementation. The owner must inspect, understand and adapt the prepared changes, run the checks, and request a genuine independent review. AI assistance is disclosed; preparing a branch does not establish individual authorship or course approval.

Validation: `python3 scripts/verify-prepared.py 12 work/issue12` from the solutions checkout runs typecheck, lint, production build, available unit tests and isolated MySQL/Mongo integration. Full HTTP testing runs once its feature dependencies are present. See the solutions verification report for integrated results.

Dependency: shared foundation #39; target codex/issue-39 until it is merged, then refresh against main. No automatic merge or issue closure is requested.
