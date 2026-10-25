# Issue 37 verification

Run `sh 37/tests/verify.sh /absolute/path/to/new-output-directory` from the solutions root. It reconstructs the pinned source plus declared prerequisites, then executes the focused tests.

MobilityCommuteIntegrityTest; financial/lifecycle/booking tests; fresh migration and rollback/reapply.

The test implementation is carried in the issue patches; it is not a detached mock of the application. Reports record actual results after execution.
