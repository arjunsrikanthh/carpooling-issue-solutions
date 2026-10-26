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

## Leader checklist after this audit

1. Submit the shared #39 foundation PR first. It is the only branch that changes the official application baseline.
2. Ask each owner to prepare one fresh official PR from this repository's helper. They must read the issue README, run the checks, explain their own diff, and request a teammate review.
3. Keep official PRs #47 and #51 separate from this Next.js work. #47 is old prototype booking evidence and is currently dirty; #51 has no net diff and includes commits authored under `noqtar`. Do not merge either into the new application.
4. Review the official PRs one at a time after CI passes. Confirm the issue scope, tests, screenshots/evidence and reviewer comments before merging.
5. Finish the course gates: compare these drafts with the submitted SRS/SAD/Test Plan, capture final UI/database screenshots, record the one-minute working-product video, and document any deviations. Engineering tests do not replace those gates.

The completed feature handoff was verified against merged foundation commit `f1314b1656ba939eb603e67e97dc8f24e0a7de92`. See [reports/FEATURE_HANDOFF_VERIFICATION.md](reports/FEATURE_HANDOFF_VERIFICATION.md). Teammates do not need to implement missing feature code; they need to prepare the completed scoped patch, understand it, run verification, submit it from the assigned account, and request review.
