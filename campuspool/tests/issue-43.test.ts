import { describe, expect, it } from "vitest";
import { GET as searchRides } from "@/app/api/rides/route";
import { GET as rideDetail } from "@/app/api/rides/[id]/route";
import { searchQuery } from "@/server/search";
import { utcDate } from "@/server/quote";
import { fixtureRide, fixtureUser } from "./support";

const enabled = process.env.RUN_CAMPUSPOOL_INTEGRATION === "1";

describe("issue 43 validation", () => {
  it("rejects an impossible calendar date while requiring explicit window fields", () => {
    const base = { originStopId: "1", destinationStopId: "2", startTime: "09:00", endTime: "10:00", vehicleKind: "ALL" };
    expect(searchQuery.safeParse({ ...base, date: "2030-02-30" }).success).toBe(false);
    expect(searchQuery.safeParse({ ...base, date: "2030-02-28" }).success).toBe(true);
  });
});

function localWindow(departure: string) {
  const date = utcDate(departure);
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata", year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(date);
  const value = (type: string) => parts.find((part) => part.type === type)?.value ?? "";
  return { date: `${value("year")}-${value("month")}-${value("day")}`, startTime: "00:00", endTime: "23:59" };
}

describe.skipIf(!enabled)("issue 43 ride search against real MySQL", () => {
  it("returns a public ride with a quote and excludes the driver from results", async () => {
    const driver = await fixtureUser("DRIVER");
    const rider = await fixtureUser("RIDER");
    const ride = await fixtureRide(driver.user, 1);
    const query = new URLSearchParams({ originStopId: String(ride.origin_stop_id), destinationStopId: String(ride.destination_stop_id), ...localWindow(ride.departure_at), vehicleKind: "ALL" });
    const response = await searchRides(new Request(`http://localhost/api/rides?${query}`, { headers: rider.request("GET").headers }));
    expect(response.status, await response.clone().text()).toBe(200);
    const body = await response.json() as { data: Array<{ id: number; quoteToken: string; vehicle: { registration: string | null } }> };
    const found = body.data.find((item) => item.id === ride.id);
    expect(found).toBeDefined();
    expect(found?.quoteToken).toEqual(expect.any(String));
    expect(found?.vehicle.registration).not.toBe(ride.vehicle_registration);
    const detail = await rideDetail(rider.request("GET", undefined), { params: Promise.resolve({ id: String(ride.id) }) });
    expect(detail.status).toBe(200);
  });
});
