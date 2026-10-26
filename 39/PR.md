Refs #39

Original Next.js/TypeScript stack migration foundation: shared auth/roles/approval, MySQL schema, fixed-stop search, API contracts, setup and CI. This deliberately includes shared bootstrap work beyond the CI-only issue title; review the migration before integration.

This is a proposed original TypeScript implementation. The owner must inspect, understand and adapt the prepared changes, run the checks, and request a genuine independent review. AI assistance is disclosed; preparing a branch does not establish individual authorship or course approval.

Validation: `python3 scripts/verify-prepared.py 39 work/issue39` from the solutions checkout runs typecheck, lint, production build, available unit tests and isolated MySQL/Mongo integration. Full HTTP testing runs once its feature dependencies are present. See the solutions verification report for integrated results.

Dependency: official main; supplies the shared foundation. No automatic merge or issue closure is requested.
