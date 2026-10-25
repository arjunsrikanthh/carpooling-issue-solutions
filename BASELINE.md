# Pinned baselines

Official compatibility baseline: `CampusPool/carpooling:main` at **0478ae0ba2549f8fba3bd44b590e91e067a46e0d**.

Historical workspace: `CampusPool/carpooling-workspace:main` at **f103f7bff32bcb24712e10d6747670aa06f8f24b**.

Local MobilityPlatform: `codex/software-workflows` at **faccb66ebb65512cfca41116109609a7120111de**. Local coursework checkout: `main` at **6aacafbb233598d88e3e10bc31d248839792272b**, with existing modified/untracked files preserved.

Official main already includes Nikhil's departure-window/ranking changes and #52 CI repair. Existing open PR #47 at `c240b5819c79f93f5a9ebb286c88ca754df68d2b` supplies attributed booking-test material; it was inspected and remains untouched.

The original directories were read only throughout this task. Implementation, test databases and generated files belong to isolated clones. No original developer database was used.

The official fresh-clone baseline verifier passed 25 frontend tests, 23 upstream tests / 67 assertions and 11 commute tests / 223 assertions on 26 October 2026. It verified Laravel startup, MySQL migrations, health and `/mobility/` HTTP 200. These are baseline results, distinct from proposed-solution results.

Snapshot comparison covers all 235 official extension files: 6 differ from historical workspace, 9 from local prototype. Source files were compared by content hashes and relevant differences inspected, not by filename alone. See `audit/source-comparison.json`.

Relevant historical workspace branches inspected: `feature/add-commute-mjs` at `d77b0e317aee0ca211abf3146be0600e80ed35a4`, `fix/portable-sprint1-demo-ci` at `3921b09161ff8887e429166b13a2d7e245b2b3a5`, and import branch `0f6b37aa4b59cf5c724c18b67527cb7319b9d3bf`. The UI feature branch rolls back `start_time`/`end_time`; the historical fix branch also has older service signatures. Neither is used to overwrite current official main.
