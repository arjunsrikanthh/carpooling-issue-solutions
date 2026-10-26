# CampusPool Next shared implementation contract

Application root: campuspool/. New original TypeScript implementation; do not copy Laravel source. Old work is behavioral reference only. Parent owns package/config/core/auth/schema + booking23/cancel24 integration. Each worker owns only assigned paths.

## Foundation (#39)
Next App Router, mysql2/promise and mongodb drivers, zod. Pool lazy from DATABASE_URL, UTC dateStrings. Tables snake_case. Cookie `cp_session` opaque random token, SQL hash only. Roles RIDER/DRIVER/ADMIN; status PENDING/APPROVED/SUSPENDED; credits synthetic integer. New registrations pending, admins approve. Testing/demo seed explicit synthetic .test users.

Shared modules to import:
- `@/server/core`: `HttpError(status:number,code:string,message?:string)`, `api(request:Request,handler:()=>Promise<Response>):Promise<Response>` (error envelope + same-origin mutation guard), `json(data:unknown,status?:number):Response` wraps as `{data}`, `body<T>(request,schema:ZodType<T>):Promise<T>`, `id(value:string|number):number`, `requireUser(request,approved?:boolean):Promise<User>`, `key(request):string`, `idempotent<T>(actorId:number,key:string,scope:string,payload:unknown,fn:(cx:PoolConnection)=>Promise<T>):Promise<T>`, `emit(cx,event:EventInput):Promise<void>`.
- `@/server/db`: `pool():Pool`, `rows<T>(cx:Pool|PoolConnection,sql:string,values?:unknown[]):Promise<T[]>`, `exec(cx,...):Promise<ResultSetHeader>`, `transaction<T>(fn:(cx:PoolConnection)=>Promise<T>):Promise<T>`.
- `@/server/types`: User {id,name,email,role,status,credits}; VehicleRow {id,owner_id,kind:'CAR'|'BIKE',registration,model,passenger_capacity,status:'PENDING'|'APPROVED'|'REJECTED',reviewed_by?,created_at?}; RideRow {id,driver_id,vehicle_id,origin_stop_id,destination_stop_id,departure_at,total_seats,seats_available,credit_price,status,driver_name?,driver_status?,vehicle_kind?,vehicle_registration?,vehicle_model?,vehicle_capacity?,vehicle_status?,origin_name?,destination_name?}.
- `@/server/quote`: `issueQuote(userId:number,ride:RideRow):string`, `verifyQuote(token:string,userId:number,ride:RideRow):void`, `publicRide(ride:RideRow):Record<string,unknown>` masks plate and returns camelCase DTO.
- `@/components/AppShell`: client layout/context hook `useSession(): {user:User|null,features:string[],refresh:()=>Promise<void>,loading:boolean}`. Parent/UI worker coordinates. Shared `apiFetch<T>(url:string,options?:RequestInit):Promise<T>` returns .data, sets same-origin credentials, JSON, idempotency UUID for mutations except auth. Helper exported from `@/lib/client`.
- EventInput {type:string,actorId:number,audienceIds:number[],rideId?:number,bookingId?:number,data:Record<string,unknown>} emit writes SQL outbox in current transaction.

## SQL columns (schema parent owns)
users(id,name,email,password_hash,role,status,credits,created_at)
sessions(token_hash,user_id,expires_at,created_at)
auth_attempts(bucket_key,failures,expires_at)
stops(id,name,lat,lng)
vehicles(id,owner_id,kind,registration,model,passenger_capacity,status,reviewed_by,review_note,created_at)
rides(id,driver_id,vehicle_id,origin_stop_id,destination_stop_id,departure_at,total_seats,seats_available,credit_price,status,created_at)
bookings(id,ride_id,rider_id,status:REQUESTED|ACCEPTED|REJECTED|CANCELLED,cancelled_by,cancellation_reason,created_at,updated_at); active-rider generated uniqueness.
ledger(id,user_id,booking_id,kind:HOLD|REFUND,amount,created_at), unique(booking_id,kind), amount positive
idempotency_records(actor_id,key_hash,scope,payload_hash,response_json,created_at), unique(actor_id,key_hash)
outbox(event_id,type,actor_id,audience_ids JSON,ride_id,booking_id,data JSON,created_at,published_at,attempts)

Foundation SQL includes FKs/checks/indexes needed for safe app, but capacity changes are owned by booking/cancel service transaction. #37 adds database evidence view/procedure/guard triggers + Mongo activity/outbox worker. Don't create DB capacity-decrement triggers; services update available seats once.

## API contract
All success `{data:...}`; all failures `{error:{code,message,fields?}}`, no tokens/hashes/SQL text leaked. api() validates Origin for mutations. Header `Idempotency-Key` required for domain mutations. JSON body strict via zod. Use Node runtime.
Auth foundation: POST /api/auth/{register,login,logout}; GET /api/auth/me =>User|null. Admin foundation GET /api/admin/members, POST /api/admin/members/[id]/approve {status:'APPROVED'|'SUSPENDED'}.
GET /api/catalog => {stops:[{id,name}],vehicles:own approved Vehicle DTO[],features:string[]}. GET /api/dashboard => {ridesPublished,bookingsRequested,bookingsAccepted,credits}.

12 owns server/vehicles.ts + API /api/vehicles GET/POST {kind,registration,model,passengerCapacity}, /api/vehicles/[id]/review POST {status:'APPROVED'|'REJECTED',note?}. Admin sees all, owner sees own, approved members only. Kind BIKE capacity1, CAR1..5. Never self-approve. Return camelCase DTO {id,ownerId,ownerName?,kind,registration,model,passengerCapacity,status,reviewNote?}. Admin/manual approval truthful.
21 owns server/offers.ts + /api/offers GET own driver rides and POST {vehicleId,originStopId,destinationStopId,departureAt ISO withoffset,totalSeats,creditPrice}. Future15min..30days, own approved vehicle+approved DRIVER, seat limit<=capacity, stops distinct, integer price1..1000 syntheticcredits. Reject active overlapping driver ride within60min (fixed-route course model, no live routing). Lock driver row then validate/insert, idempotency. Return publicRide DTO.
43 owns server/search.ts + GET /api/rides?originStopId&destinationStopId&date=YYYY-MM-DD&startTime=HH:mm&endTime=HH:mm&vehicleKind=CAR|BIKE|ALL. Campus timezone Asia/Kolkata; inclusive windows, future, notown, published, free seats, approved driver/vehicle. DTO array each publicRide +quoteToken. GET /api/rides/[id] same eligibility/read +quote, no mutation. Tests can inject fixtures through SQL.
23 parent: GET /api/bookings list participant; POST {rideId,quoteToken}; POST /api/bookings/[id]/decision {decision:'ACCEPT'|'REJECT'}, owner only. Request self/duplicate checks; accept atomic seat decrement+credit hold+ledger. DTO camelCase booking/ride/host/rider/status/actions/credits.
24 parent: POST /api/bookings/[id]/cancel {reason?}; POST /api/offers/[id]/cancel {reason?}; owner/rider authorization, history, exact refund/capacity. UI can include separate cancellations page, bookings page checks features includes cancellations to show cancel actions. No static imports between feature UI modules.
37 worker: server/activity.ts, server/outbox.ts, scripts/activity-worker.ts, api/activity GET {events,summary,pendingCount}; api/activity/sync POST ADMIN; api/admin/database-evidence GET foractual SQL+Mongo evidence. Mongo writes use event_id unique upsert, audience access filter. Worker MySQL outbox ->Mongo ->published_at, retries safe. Mongo outage must not rollback booking. New advanced migration002 SQL allowed separate sql/migrations/002_evidence.sql (delimiter directives support parent migrator). View driver_ride_summary + storedprocedure ride_capacity_report; guard trigger ride immutable after active bookings, ledger append-only? protect audit history. Do not alter parent001 schema without coordination.

## UI ownership
One UI worker owns src/app pages/components/styles/lib/client. Feature modules independent file routes: vehicles12, offers21, bookings23, cancellations24, activity+database37, rides43. API modules no crossfeature imports; core types shared. Root shared layout/nav shows only enabled features basedsrc/features/enabled/*.json viafoundationcatalog. Foundation pages login/register/dashboard/admin membership only; no otherfeature UI imports.

## Issue handoff
39 is shared foundation (auth/schema/scaffold/CI). Others patch only own modules onfoundation. Fullrepo runnableallfeatures. Submit helper will use officialmain whenfoundationpresent; otherwise explicitofficialfoundationbranch codex/issue-39 whenleaderhas submittedit. No fake prerequisite commits/claimotherstudentauthorship. Neveractuallypushofficialfromagentturn.
