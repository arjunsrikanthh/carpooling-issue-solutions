# CampusPool Sprint 1 issue solutions

Private, AI-assisted proposed patches and reproducible verification on official commit `0478ae0ba2549f8fba3bd44b590e91e067a46e0d`. This is a review/distribution repository, not a replacement application repository or proof of individual student authorship.

Start with [BASELINE.md](BASELINE.md), [AUDIT.md](AUDIT.md), [INTEGRATION.md](INTEGRATION.md) and [CONTRIBUTIONS.md](CONTRIBUTIONS.md). The eight issue folders contain actual source/test/document patches. Closed #22 is verified as a dependency in `43/`.

```sh
sh scripts/verify-integrated.sh
# Or one issue with its declared prerequisites:
sh scripts/verify-issue.sh 23
```

Use Docker Compose, Git, Node.js and Python. Output directories must be new. Review changes in the reconstructed app with `git diff --cached`. Do not run these scripts against an existing developer checkout.

Verification reports distinguish code/test completion from human PR review, approved course documents and actual video submission. Course drafts are new drafts and have not been submitted or approved. Waitlist/rematching and Sprint 2 implementation remain outside this package.

Neither CampusPool repository, nor any existing issue, PR, branch, setting or original local checkout is an authorized write destination for this task.
