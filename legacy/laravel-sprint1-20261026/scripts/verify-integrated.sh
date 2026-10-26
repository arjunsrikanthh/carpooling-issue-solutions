#!/bin/sh
set -eu
solutions=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
if [ "$#" -gt 0 ]; then
  output=$1
  test ! -e "$output" || { echo 'Output path must not exist. Existing directories are never reset.' >&2; exit 2; }
  mkdir -p "$output"
else
  output=$(mktemp -d "${TMPDIR:-/tmp}/campuspool-solutions.XXXXXX")
fi
output=$(CDPATH= cd -- "$output" && pwd)
echo "Verification artifacts: $output"
baseline=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline"])' "$solutions/solutions.json")
git clone --no-hardlinks "${BASELINE_SOURCE:-https://github.com/CampusPool/carpooling.git}" "$output/app"
git -C "$output/app" checkout --detach "$baseline"
git -C "$output/app" remote set-url --push origin DISABLED
if [ -n "${VERIFY_ISSUE:-}" ]; then
  sh "$solutions/scripts/apply-issue.sh" "$VERIFY_ISSUE" "$output/app"
else
  for issue in $(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1]))["order"]))' "$solutions/solutions.json"); do
    sh "$solutions/scripts/apply-issue.sh" "$issue" "$output/app"
  done
fi
git -C "$output/app" diff --cached --check
sh "$solutions/scripts/test-app.sh" "$output/app" "$output" "${VERIFY_ISSUE:-integrated}"
