#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
exec sh "$root/scripts/verify-issue.sh" 37 "$@"
