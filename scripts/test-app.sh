#!/bin/sh
set -eu
app=$1
out=$2
scope=${3:-integrated}
gitdir=$(git -C "$app" rev-parse --absolute-git-dir)
if [ ! -f "$gitdir/campuspool-solutions.json" ] && [ "${SOLUTIONS_DISPOSABLE_CHECKOUT:-}" != 1 ]; then
  echo 'Refusing runtime cleanup outside a checkout reconstructed by the solutions scripts.' >&2
  exit 2
fi
cd "$app/prototype"
command -v docker >/dev/null
docker compose version >/dev/null
python3 scripts/check-package.py
node --test tests/frontend/*.mjs campuspool-extension/web/driver-onboarding-ui.test.mjs campuspool-extension/web/tracking-state.test.mjs > "$out/frontend.log" 2>&1 || { cat "$out/frontend.log"; exit 1; }
cat "$out/frontend.log"
project="campuspool-solutions-$(date +%s)-$$"
export COMPOSE_PROJECT_NAME="$project"
if [ -n "${SOLUTIONS_COMPOSER_CACHE:-}" ]; then
  mkdir -p "$SOLUTIONS_COMPOSER_CACHE"
  python3 - "$SOLUTIONS_COMPOSER_CACHE" "$out/compose.cache.yml" <<'PY_CACHE'
import json,pathlib,sys
cache=str(pathlib.Path(sys.argv[1]).resolve())
pathlib.Path(sys.argv[2]).write_text(json.dumps({'services':{'deps':{'environment':{'COMPOSER_CACHE_DIR':'/tmp/composer-cache'},'volumes':[cache+':/tmp/composer-cache']}}}))
PY_CACHE
fi
python3 - "$out" <<'PY_ARTIFACTS'
import json,pathlib,sys
out=pathlib.Path(sys.argv[1]).resolve()
(out/'compose.verification.yml').write_text(json.dumps({'services':{'app':{'volumes':[str(out)+':/verification']}}}))
PY_ARTIFACTS
dc() {
  if [ -f reproduction/compose.booking.yml ]; then set -- -f reproduction/compose.booking.yml "$@"; fi
  if [ -f "$out/compose.cache.yml" ]; then set -- -f "$out/compose.cache.yml" "$@"; fi
  docker compose -f reproduction/compose.yml -f reproduction/compose.local.yml -f reproduction/compose.demo.yml -f "$out/compose.verification.yml" "$@"
}
cleanup() {
  status=$?
  trap - EXIT INT TERM
  if [ "$status" -ne 0 ]; then dc logs --no-color --tail=100 app migrate mysql > "$out/runtime-failure.log" 2>&1 || true; fi
  dc run --rm --no-deps --user 0 deps sh -c 'rm -rf /var/www/vendor /var/www/storage /var/www/bootstrap/cache/*' >/dev/null 2>&1 || true
  dc down -v --remove-orphans >/dev/null 2>&1 || true
  rm -f reproduction/package.env .env
  printf '{"scope":"%s","exit_code":%s,"checkout_head":"%s"}\n' "$scope" "$status" "$(git rev-parse HEAD)" > "$out/result.json"
  exit "$status"
}
trap cleanup EXIT INT TERM
python3 reproduction/configure-demo-env.py
mkdir -p storage/framework/cache/data storage/framework/sessions storage/framework/views storage/logs storage/suburbs storage/geojson bootstrap/cache
dc config --quiet
dc build deps > "$out/build.log" 2>&1 || { tail -80 "$out/build.log"; exit 1; }
dc run --rm --no-deps deps sh -c 'find . -type d \( -name vendor -o -name storage \) -prune -o -type f -name "*.php" -print0 > /tmp/campuspool-php-sources; test -s /tmp/campuspool-php-sources; xargs -0 -n 1 php -l < /tmp/campuspool-php-sources' > "$out/php-syntax.log" 2>&1 || { tail -80 "$out/php-syntax.log"; exit 1; }
dc up -d app > "$out/startup.log" 2>&1 || { tail -100 "$out/startup.log"; exit 1; }
attempt=0
until curl -fsS --max-time 2 http://127.0.0.1:18180/api/health > "$out/health.json"; do
  attempt=$((attempt + 1))
  test "$attempt" -lt 45 || { echo 'HTTP health did not become ready.' >&2; exit 1; }
  sleep 1
done
python3 - "$out/health.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); assert d['status']=='ok' and d['database']=='up',d
PY
curl -fsS http://127.0.0.1:18180/mobility/ > /dev/null
case "$scope" in
  12|21) tests='tests/extension/MobilityCommuteProductTest.php tests/extension/DriverOnboardingHttpTest.php tests/Feature/Http/CarApiTest.php tests/Unit/Services/Logic/CarsManagerTest.php' ;;
  23) tests='tests/extension/MobilityCommuteProductTest.php tests/extension/MobilityBookingCorrectnessTest.php' ;;
  24) tests='tests/extension/MobilityCommuteProductTest.php tests/extension/MobilityBookingCorrectnessTest.php tests/extension/MobilityCommuteCancellationTest.php tests/extension/MobilityFinancialInvariantsTest.php tests/extension/MobilityLifecycleTest.php' ;;
  37) tests='tests/extension/MobilityCommuteProductTest.php tests/extension/MobilityCommuteIntegrityTest.php tests/extension/MobilityFinancialInvariantsTest.php tests/extension/MobilityLifecycleTest.php' ;;
  *)
    tests='tests/Unit/Services/Logic/TripLiveShareManagerTest.php tests/Feature/Http/CarApiTest.php tests/Unit/Services/Logic/CarsManagerTest.php tests/extension/MobilityCommuteProductTest.php tests/extension/DriverOnboardingHttpTest.php tests/extension/MobilityDriverProfileBridgeTest.php tests/extension/MobilityLifecycleTest.php tests/extension/MobilityFinancialInvariantsTest.php tests/extension/MobilitySegmentBookingTest.php'
    for name in MobilityBookingCorrectnessTest MobilityCommuteIntegrityTest MobilitySearchRegressionTest MobilityCommuteCancellationTest; do
      test ! -f "tests/extension/$name.php" || tests="$tests tests/extension/$name.php"
    done ;;
esac
# Intentional word splitting: the list above contains only fixed repository paths.
dc exec -T -e DB_DATABASE=testing -e DB_USERNAME=root -e DB_PASSWORD=smoke-root-password app php artisan test --compact --log-junit /verification/backend.junit.xml $tests > "$out/backend.log" 2>&1 || { cat "$out/backend.log"; exit 1; }
cat "$out/backend.log"
python3 reproduction/smoke-booking.py > "$out/booking-smoke.log" 2>&1 || { cat "$out/booking-smoke.log"; exit 1; }
cat "$out/booking-smoke.log"
if [ -f reproduction/booking-concurrency-probe.php ]; then
  dc exec -T app php /var/www/reproduction/booking-concurrency-probe.php > "$out/booking-races.json" 2>&1 || { cat "$out/booking-races.json"; exit 1; }
  cat "$out/booking-races.json"
fi
if [ -f reproduction/cancellation-concurrency-probe.php ]; then
  dc exec -T app php /var/www/reproduction/cancellation-concurrency-probe.php > "$out/cancellation-races.json" 2>&1 || { cat "$out/cancellation-races.json"; exit 1; }
  cat "$out/cancellation-races.json"
fi
if [ -f campuspool-extension/migrations/2026_10_26_000100_harden_commute_integrity.php ]; then
  dc exec -T -e DB_USERNAME=root -e DB_PASSWORD=smoke-root-password app php artisan migrate:rollback --step=1 --force > "$out/migration-rollback.log" 2>&1 || { cat "$out/migration-rollback.log"; exit 1; }
  dc exec -T -e DB_USERNAME=root -e DB_PASSWORD=smoke-root-password app php artisan migrate --force >> "$out/migration-rollback.log" 2>&1 || { cat "$out/migration-rollback.log"; exit 1; }
  cat "$out/migration-rollback.log"
fi
printf '%s\n' 'All selected issue and integration checks passed.' 
