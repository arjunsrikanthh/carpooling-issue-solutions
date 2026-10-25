# Attribution and review ownership

This repository contains **AI-assisted proposed implementations and verification material**. It is a distribution/verification repository; the official source repository remains authoritative. No teammate authorship or faculty approval is asserted.

- Upstream Carpoolear: retain the official package's LICENSE and existing SOURCE_MAP entries. Upstream source pin is `6ba3d8913a8f77e664e848a526f196690a03c1e8`. The inherited GPL text/MIT Composer metadata discrepancy is documented upstream and is not resolved by these patches.
- Imported CampusPool/MobilityPlatform extension: existing attribution and implementation remain credited as imported baseline material, not newly authored student work.
- Nikhil Suhas Joshi: official commit history includes departure windows and ranking (`b640be5`, `073454d`, `11f683b`, `65f3612`, `c0b0f83`). These contracts are preserved.
- Zayaan Ahmed: historical workspace feature branch `feature/add-commute-mjs` contains genuine commit `d77b0e317aee0ca211abf3146be0600e80ed35a4`. Its 22-line commute UI change was inspected. It removes the current departure-window parameters, so importing that older branch would regress Nikhil's contract; the proposed patches preserve official main instead. This existing work is distinct from new AI-assisted proposals.
- Arjun's existing PR #47: booking tests, race-probe structure and Compose override are derived from commits `7e17476` and `c240b581`. The package adapts the newer time-window contract and adds confirmed-duplicate coverage. PR #47 remains open and untouched.
- New proposed work: masked vehicle summaries, persisted passenger capacity, publication validation/UI, cancellation provenance and whole-ride cancellation, relational constraints, additional tests, verification scripts, course drafts and CI checks were generated with Codex assistance in this task. Commits use the authenticated owner's genuine identity; none impersonates a teammate.

Review allocation: Zayaan reviews `12/` and `21/`; Arjun reviews `23/`, `39/`, `44/`; Nithesh reviews `24/`, `37/`; Nikhil reviews `43/` and the closed #22 regression behavior. Each teammate should understand, test and adapt the proposed changes before independently submitting a real contribution branch and reviewed PR. That human workflow has not been performed by this task.

Source patches retain upstream notices. Newly generated package scripts and prose are provided for this private review; no upstream licensing notice is replaced. Academic originality/reuse acceptance must be resolved with the instructor rather than inferred from technical tests.

Issue #43 also reconciles the already attributed `driver-profile-integration.patch` and `routing-integration.patch` with the actual running Carpoolear application source. The underlying imported integration design is not represented as newly invented algorithmic work; this task adds the missing integration and exercises it through the expanded suites.
