# Issue 39 verification

Run `sh 39/tests/verify.sh /absolute/path/to/new-output-directory` from the solutions root. It reconstructs the pinned source plus declared prerequisites, then executes the focused tests.

Private actual Actions run; per-issue and integrated fresh-clone scripts; package/source-map integrity; runtime smoke and migrations.

The test implementation is carried in the issue patches; it is not a detached mock of the application. Reports record actual results after execution.
