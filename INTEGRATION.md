# Reproduction and integration

Order: **37 → 12 → 21 → 23 → 24 → 43 → 39 → 44**. `solutions.json` is the machine-readable authority. Issue 12 also applies independently; issue 37 changes the publication audience sentinel before newer validation touches that method. Issue 21 needs vehicle DTO/UI changes from 12. Booking precedes cancellation. Regression fixes precede the CI package that executes the expanded suites; documentation follows both.

Each issue folder contains one consolidated `solution.patch`, derived from the verified integration order. The tests and fixes in #43 must precede the expanded CI checks in #39. The apply script uses Git's index checks and recursively applies declared prerequisites. It never resets a checkout. HEAD must equal the pinned baseline; use only a new disposable clone. Staged patches remain reviewable with `git diff --cached`.

```sh
sh scripts/verify-integrated.sh /absolute/path/to/new-output-directory
sh scripts/verify-issue.sh 23 /absolute/path/to/another-new-directory
```

Requirements: Git, Python 3.9+, Node.js supporting `node --test`, Docker Engine with Compose, internet access to public official baseline and pinned container/Composer dependencies, free loopback port 18180. On this Mac, set `DOCKER_CONTEXT=colima-campuspool-solutions`; this is a disposable profile created for this task. Other machines use their own Docker configuration.

`BASELINE_SOURCE=/path/to/read-only-clone` optionally selects a local Git source. The exact SHA is still checked out. No token or private dependency is embedded. If official baseline access becomes private, configure read-only checkout access externally; do not publish tokens or weaken privacy.

All databases are synthetic and disposable. The verifier creates a unique Compose project, checks health, runs source validation/frontend/PHP/MySQL suites, then tests booking/cancellation and sampled HTTP races. Cleanup removes only its own containers and volume plus generated files inside its disposable clone.

`SOURCE_MAP.tsv` and `MANIFEST.sha256` are regenerated centrally after every issue application. Issue patches never restore stale manifests. Existing attribution is retained; changed/new files are explicitly labelled AI-assisted proposals. The source map self hash is omitted and its bytes are covered by the manifest.

Integration conflicts found and addressed: publication `audience_id=0` was incompatible with a new FK, so the migration normalizes it to NULL; vehicle approval/capacity must derive from a current linked approved application; the new seat field required an updated mounted UI fixture; trip cancellation must update both canonical trip/lifecycle state and append an event; cancellation closures must capture injected services and idempotency keys. These defects are documented so a reviewer can inspect the final fixes.

The frontend is served as native JavaScript/CSS. The inherited Vite configuration points to absent resources and has no lockfile; an npm production build is not a verified delivery path. Native-module syntax and mounted UI tests cover the actual served application. Real road routing, production identity and real payments are not established by synthetic tests.
