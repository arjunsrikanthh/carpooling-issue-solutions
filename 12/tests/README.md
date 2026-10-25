# Issue 12 verification

Run `sh 12/tests/verify.sh /absolute/path/to/new-output-directory` from the solutions root. It reconstructs the pinned source plus declared prerequisites, then executes the focused tests.

DriverOnboardingHttpTest; MobilityCommuteProductTest; mounted onboarding/commute UI tests.

The test implementation is carried in the issue patches; it is not a detached mock of the application. Reports record actual results after execution.
