#!/bin/sh
set -eu
test "$#" -ge 1 || { echo 'Usage: verify-issue.sh ISSUE [NEW_OUTPUT_DIRECTORY]' >&2; exit 2; }
solutions=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
issue=$1
shift
VERIFY_ISSUE="$issue" exec sh "$solutions/scripts/verify-integrated.sh" "$@"
