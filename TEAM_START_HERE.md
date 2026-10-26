# CampusPool Sprint 1 teammate handoff

The new implementation is under `campuspool/`. The Laravel prototype is
preserved under `legacy/` for reference only. Each teammate works from a fresh
clone of this solutions repository and prepares exactly one assigned issue.

```sh
python3 scripts/prepare-pr.py 39 --output work/issue39
python3 scripts/verify-prepared.py 39 work/issue39
python3 scripts/submit-pr.py 39 --path work/issue39 --publish
```

Issue 39 is the shared Next.js/TypeScript/MySQL foundation. Until its PR is
merged, feature preparation intentionally requires the official
`codex/issue-39` branch and targets that branch. After the marker
`campuspool/.foundation-version` is on official `main`, fresh feature clones
target `main`.

The current eight-issue handoff is intentionally scoped: #12 vehicles, #21
offers, #23 bookings, #24 cancellation, #37 advanced SQL integrity plus Mongo
activity evidence, #39 the rebuilt foundation, #43 `[N8] Testing against
approved Test Plan` (search is foundation functionality, not this issue), and
#44 documentation. Sprint 2 waitlist work and the remaining advanced features
are not claimed as complete.

Use only the GitHub account assigned in `handoff.json`. The helper is draft by
default, uses `Refs #N`, and never merges, closes issues, force-pushes, or uses
the `noqtar` account. Do not reuse a work directory or copy files from the
legacy application.
