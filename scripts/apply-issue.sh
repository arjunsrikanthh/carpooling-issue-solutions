#!/bin/sh
set -eu
test "$#" -eq 2 || { echo 'Usage: apply-issue.sh ISSUE DISPOSABLE_OFFICIAL_CHECKOUT' >&2; exit 2; }
solutions=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
exec python3 "$solutions/scripts/apply-issue.py" "$1" "$2"
