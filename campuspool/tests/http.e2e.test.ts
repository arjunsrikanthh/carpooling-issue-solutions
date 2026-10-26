import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { api, dayAndWindow, DEMO_PASSWORD, expectError, futureIso, json, login, BASE_URL } from './http';

const enabled = process.env.RUN_CAMPUSPOOL_E2E === '1';
const runRaces = enabled && process.env.RUN_CAMPUSPOOL_RACES !== '0';
const password = DEMO_PASSWORD;
const adminEmail = 'admin@campuspool.test';
const suffix=crypto.randomUUID();
const driverEmail = `driver-${suffix}@campuspool.test`;
const riderEmail = `rider-${suffix}@campuspool.test`;
const rider2Email = `rider2-${suffix}@campuspool.test`;

describe.skipIf(!enabled)('CampusPool HTTP E2E (real MySQL + Mongo)', () => {
  let admin = '';
  let driver = '';
  let rider = '';
  let rider2 = '';
  let catalog: { stops: Array<{ id: number; name: string }> };
  let vehicleId = 0;
  let offerId = 0;
  let rideId = 0;
  let quoteToken = '';

  beforeAll(async () => {
    const health = await api('/api/auth/me');
    expect(health.response.status, `CampusPool is not reachable at ${BASE_URL}`).toBeLessThan(500);
    admin = await login(adminEmail);
    for(const [email,role] of [[driverEmail,'DRIVER'],[riderEmail,'RIDER'],[rider2Email,'RIDER']]) {
      const registered=await api<{id:number}>('/api/auth/register',json('POST',{name:'HTTP Test Member',email,password,role},`register-${email}`));
      expect(registered.response.status,JSON.stringify(registered.body)).toBe(201);
      const approved=await api(`/api/admin/members/${registered.body.data!.id}/approve`,json('POST',{status:'APPROVED'},`approve-${email}`),admin);
      expect(approved.response.status,JSON.stringify(approved.body)).toBe(200);
    }
    driver = await login(driverEmail);
    rider = await login(riderEmail);
    rider2 = await login(rider2Email);
    const catalogResult = await api<typeof catalog>('/api/catalog', {}, rider);
    expect(catalogResult.response.status, JSON.stringify(catalogResult.body)).toBe(200);
    catalog = catalogResult.body.data!;
    expect(catalog.stops.length).toBeGreaterThanOrEqual(2);
  });

  afterAll(async () => {
    // Fixtures are deliberately not deleted: the seed owns their database and
    // the API's cancellation/history paths are part of the acceptance evidence.
    if (driver && offerId) {
      await api(`/api/offers/${offerId}/cancel`, json('POST', { reason: 'e2e cleanup' }, `cleanup-${offerId}`), driver);
    }
  });

  it('exposes authenticated roles and protects all four role boundaries', async () => {
    for (const [cookie, role] of [[admin, 'ADMIN'], [driver, 'DRIVER'], [rider, 'RIDER'], [rider2, 'RIDER']] as const) {
      const me = await api<{ id: number; role: string; status: string }>('/api/auth/me', {}, cookie);
      expect(me.response.status).toBe(200);
      expect(me.body.data?.role).toBe(role);
      expect(me.body.data?.status).toBe('APPROVED');
    }
    const riderAdmin = await api('/api/admin/members', {}, rider);
    await expectError(riderAdmin, [403]);
    const riderEvidence = await api('/api/admin/database-evidence', {}, rider);
    await expectError(riderEvidence, [403]);
    const driverApprove = await api('/api/admin/members/1/approve', json('POST', { status: 'APPROVED' }, `bad-approve-${Date.now()}`), driver);
    await expectError(driverApprove, [403]);
    const riderSync = await api('/api/activity/sync', json('POST', {}, `bad-sync-${Date.now()}`), rider);
    await expectError(riderSync, [403]);
  });

  it('registers a pending student and lets only admin approve it', async () => {
    const email = `e2e-${Date.now()}@campuspool.test`;
    const registration = await api('/api/auth/register', json('POST', {
      name: 'E2E Pending Student', email, password, role: 'RIDER',
    }, `register-${email}`));
    expect(registration.response.status).toBe(201);
    const pendingLogin = await api('/api/auth/login', json('POST', { email, password }, `pending-login-${email}`));
    expect(pendingLogin.response.status).toBe(200);
    expect(pendingLogin.cookie).toBeTruthy();
    const pendingVehicles = await api('/api/vehicles', {}, pendingLogin.cookie);
    await expectError(pendingVehicles, [403]);
    const members = await api<Array<{ id: number; email: string; status: string }>>('/api/admin/members', {}, admin);
    expect(members.response.status).toBe(200);
    const pending = members.body.data?.find((member) => member.email === email);
    expect(pending?.status).toBe('PENDING');
    const approve = await api(`/api/admin/members/${pending!.id}/approve`, json('POST',{status:'APPROVED'},`approve-${email}`), admin);
    expect(approve.response.status, JSON.stringify(approve.body)).toBe(200);
  });

  it('enforces vehicle kind/capacity validation and admin approval', async () => {
    const invalidBike = await api('/api/vehicles', json('POST', {
      kind: 'BIKE', registration: `E2E-BIKE-${Date.now()}`, model: 'Test Bike', passengerCapacity: 2,
    }, `invalid-bike-${Date.now()}`), driver);
    await expectError(invalidBike, [422, 400]);
    const invalidCar = await api('/api/vehicles', json('POST', {
      kind: 'CAR', registration: `E2E-CAR-${Date.now()}`, model: 'Test Car', passengerCapacity: 6,
    }, `invalid-car-${Date.now()}`), driver);
    await expectError(invalidCar, [422, 400]);
    const vehicle = await api<{ id: number; status: string }>('/api/vehicles', json('POST', {
      kind: 'CAR', registration: `E2E-${Date.now()}`, model: 'Test Car', passengerCapacity: 2,
    }, `vehicle-${Date.now()}`), driver);
    expect(vehicle.response.status).toBe(201);
    vehicleId = vehicle.body.data!.id;
    expect(vehicle.body.data!.status).toBe('PENDING');
    const selfReview = await api(`/api/vehicles/${vehicleId}/review`, json('POST', { status: 'APPROVED' }, `self-review-${vehicleId}`), driver);
    await expectError(selfReview, [403]);
    const review = await api(`/api/vehicles/${vehicleId}/review`, json('POST', { status: 'APPROVED' }, `review-${vehicleId}`), admin);
    expect(review.response.status).toBe(200);
  });

  it('publishes an offer, rejects invalid data, and enforces idempotency', async () => {
    const [origin, destination] = catalog.stops;
    const departureAt = futureIso(180);
    const payload = { vehicleId, originStopId: origin.id, destinationStopId: destination.id, departureAt, totalSeats: 2, creditPrice: 25 };
    const invalid = await api('/api/offers', json('POST', { ...payload, totalSeats: 3 }, `invalid-offer-${Date.now()}`), driver);
    await expectError(invalid, [422, 400]);
    const key = `offer-${Date.now()}`;
    const created = await api<{ id: number; seatsAvailable: number }>('/api/offers', json('POST', payload, key), driver);
    expect(created.response.status,JSON.stringify(created.body)).toBe(201);
    offerId = created.body.data!.id;
    rideId = offerId;
    expect(created.body.data!.seatsAvailable).toBe(2);
    const replay = await api<{ id: number }>('/api/offers', json('POST', payload, key), driver);
    expect(replay.response.status).toBe(201);
    expect(replay.body.data?.id).toBe(offerId);
    const conflict = await api('/api/offers', json('POST', { ...payload, creditPrice: 26 }, key), driver);
    await expectError(conflict, [409]);
  });

  it('searches by bounded campus-time windows and issues a quote', async () => {
    const window = dayAndWindow(180);
    const query = new URLSearchParams({ originStopId: String(catalog.stops[0].id), destinationStopId: String(catalog.stops[1].id), ...window });
    const result = await api<Array<{ id: number; quoteToken: string; seatsAvailable: number }>>(`/api/rides?${query}`, {}, rider);
    expect(result.response.status).toBe(200);
    const match = result.body.data?.find((ride) => ride.id === rideId);
    expect(match).toBeTruthy();
    quoteToken = match!.quoteToken;
    expect(quoteToken).toEqual(expect.any(String));
    const malformed = await api('/api/rides?date=not-a-date&startTime=99:99', {}, rider);
    await expectError(malformed, [400, 422]);
    const detail = await api<{ id: number; quoteToken: string }>(`/api/rides/${rideId}`, {}, rider);
    expect(detail.response.status).toBe(200);
    expect(detail.body.data?.quoteToken).toEqual(expect.any(String));
  });

  it('prevents self/duplicate requests, accepts by owner, and rejects foreign decisions', async () => {
    const self = await api('/api/bookings', json('POST', { rideId, quoteToken }, `self-${Date.now()}`), driver);
    await expectError(self, [403, 409]);
    const request = await api<{ id: number; status: string }>('/api/bookings', json('POST', { rideId, quoteToken }, `request-${Date.now()}`), rider);
    expect(request.response.status,JSON.stringify(request.body)).toBe(201);
    const bookingId = request.body.data!.id;
    const duplicate = await api('/api/bookings', json('POST', { rideId, quoteToken }, `duplicate-${Date.now()}`), rider);
    await expectError(duplicate, [409]);
    const foreign = await api(`/api/bookings/${bookingId}/decision`, json('POST', { decision: 'ACCEPT' }, `foreign-${bookingId}`), rider2);
    await expectError(foreign, [403]);
    const accepted = await api<{ status: string }>(`/api/bookings/${bookingId}/decision`, json('POST', { decision: 'ACCEPT' }, `accept-${bookingId}`), driver);
    expect(accepted.response.status,JSON.stringify(accepted.body)).toBe(200);
    expect(accepted.body.data?.status).toBe('ACCEPTED');
    const stale = await api('/api/bookings', json('POST', { rideId, quoteToken: `${quoteToken}.tampered` }, `stale-${Date.now()}`), rider2);
    await expectError(stale, [409, 422]);
  });

  it.skipIf(!runRaces)('runs twelve parallel one-seat acceptance races with no overbooking', async () => {
    for (let trial = 0; trial < Number(process.env.RACE_TRIALS ?? 12); trial += 1) {
      const [origin, destination] = catalog.stops;
      const created = await api<{ id: number }>('/api/offers', json('POST', {
        vehicleId, originStopId: origin.id, destinationStopId: destination.id,
        // Keep each driver's fixture outside the contract's 60-minute overlap guard.
        departureAt: futureIso(360 + trial * 90), totalSeats: 1, creditPrice: 10,
      }, `race-offer-${Date.now()}-${trial}`), driver);
      expect(created.response.status,JSON.stringify(created.body)).toBe(201);
      const raceRide = created.body.data!.id;
      const found = await api<{ id: number; quoteToken: string }>(`/api/rides/${raceRide}`, {}, rider);
      const found2 = await api<{ quoteToken: string }>(`/api/rides/${raceRide}`, {}, rider2);
      const [one, two] = await Promise.all([
        api<{ id: number }>('/api/bookings', json('POST', { rideId: raceRide, quoteToken: found.body.data!.quoteToken }, `race-r1-${raceRide}`), rider),
        api<{ id: number }>('/api/bookings', json('POST', { rideId: raceRide, quoteToken: found2.body.data!.quoteToken }, `race-r2-${raceRide}`), rider2),
      ]);
      const accepted = await Promise.all([one, two].filter((r) => r.response.status === 201).map((r) => api(`/api/bookings/${r.body.data!.id}/decision`, json('POST', { decision: 'ACCEPT' }, `race-accept-${r.body.data!.id}`), driver)));
      expect(accepted.filter((r) => r.response.status === 200)).toHaveLength(1);
      expect(accepted.filter((r) => r.response.status !== 200)).toHaveLength(1);
    }
  });

  it.skipIf(!runRaces)('runs configurable parallel cancellation races with one refund path per booking', async () => {
    const trials = Number(process.env.CANCEL_RACE_TRIALS ?? 6);
    for (let trial = 0; trial < trials; trial += 1) {
      const [origin, destination] = catalog.stops;
      const created = await api<{ id: number }>('/api/offers', json('POST', {
        vehicleId, originStopId: origin.id, destinationStopId: destination.id,
        departureAt: futureIso(1800 + trial * 90), totalSeats: 1, creditPrice: 11,
      }, `cancel-race-offer-${Date.now()}-${trial}`), driver);
      expect(created.response.status,JSON.stringify(created.body)).toBe(201);
      const cancelRide = created.body.data!.id;
      const detail = await api<{ quoteToken: string }>(`/api/rides/${cancelRide}`, {}, rider);
      expect(detail.response.status).toBe(200);
      const requested = await api<{ id: number }>('/api/bookings', json('POST', {
        rideId: cancelRide, quoteToken: detail.body.data!.quoteToken,
      }, `cancel-race-request-${cancelRide}`), rider);
      expect(requested.response.status).toBe(201);
      const bookingId = requested.body.data!.id;
      const accepted = await api(`/api/bookings/${bookingId}/decision`, json('POST', { decision: 'ACCEPT' }, `cancel-race-accept-${bookingId}`), driver);
      expect(accepted.response.status,JSON.stringify(accepted.body)).toBe(200);
      const [first, second] = await Promise.all([
        api(`/api/bookings/${bookingId}/cancel`, json('POST', { reason: 'parallel cancellation' }, `cancel-race-a-${bookingId}`), rider),
        api(`/api/bookings/${bookingId}/cancel`, json('POST', { reason: 'parallel cancellation' }, `cancel-race-b-${bookingId}`), rider),
      ]);
      expect([first.response.status, second.response.status].filter((status) => status === 200)).toHaveLength(1);
      expect([first.response.status, second.response.status].filter((status) => status !== 200)).toHaveLength(1);
      const history = await api<Array<{ id: number; status: string }>>('/api/bookings', {}, rider);
      expect(history.body.data?.find((booking) => booking.id === bookingId)?.status).toBe('CANCELLED');
    }
  });

  it('cancels accepted history idempotently and exposes activity/database evidence', async () => {
    const bookings = await api<Array<{ id: number; status: string }>>('/api/bookings', {}, rider);
    const accepted = bookings.body.data?.find((booking) => booking.status === 'ACCEPTED');
    expect(accepted).toBeTruthy();
    const first = await api(`/api/bookings/${accepted!.id}/cancel`, json('POST', { reason: 'e2e cancellation' }, `cancel-${accepted!.id}`), rider);
    expect(first.response.status).toBe(200);
    const replay = await api(`/api/bookings/${accepted!.id}/cancel`, json('POST', { reason: 'e2e cancellation' }, `cancel-${accepted!.id}`), rider);
    expect(replay.response.status).toBe(200);
    expect(replay.body).toEqual(first.body);
    const conflictReplay = await api(`/api/bookings/${accepted!.id}/cancel`, json('POST', { reason: 'different reason' }, `cancel-conflict-${accepted!.id}`), rider);
    await expectError(conflictReplay, [409]);
    const activity = await api<{ events: unknown[]; summary: unknown; pendingCount: number }>('/api/activity', {}, rider);
    expect(activity.response.status).toBe(200);
    expect(activity.body.data?.events).toEqual(expect.any(Array));
    const sync = await api('/api/activity/sync', json('POST', {}, `sync-${Date.now()}`), admin);
    expect(sync.response.status).toBe(200);
    const evidence = await api<{ sql: { views: unknown[]; routines: unknown[]; triggers: unknown[]; indexes: unknown[] }; mongo: { indexes: unknown[] } }>('/api/admin/database-evidence', {}, admin);
    expect(evidence.response.status).toBe(200);
    expect(evidence.body.data?.sql).toBeTruthy();
    expect(evidence.body.data?.sql.views).toEqual(expect.arrayContaining([expect.objectContaining({ table_name: 'driver_ride_summary' })]));
    expect(evidence.body.data?.sql.routines).toEqual(expect.arrayContaining([expect.objectContaining({ routine_name: 'ride_capacity_report' })]));
    expect(evidence.body.data?.sql.triggers).toEqual(expect.any(Array));
    expect(evidence.body.data?.sql.indexes).toEqual(expect.any(Array));
    expect(evidence.body.data?.mongo).toBeTruthy();
    expect(evidence.body.data?.mongo.indexes).toEqual(expect.arrayContaining([
      expect.objectContaining({ name: 'activity_event_id_unique', unique: true }),
      expect.objectContaining({ name: 'activity_audience_created' }),
    ]));
  });
});

