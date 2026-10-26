# Database evidence examples — draft

These examples are taken from the new implementation's direct SQL and MongoDB source. They illustrate what the team should demonstrate; they are not recorded execution results.

## SQL: relational operations

Source: `campuspool/sql/migrations/001_schema.sql`.

```sql
-- DDL source: campuspool/sql/migrations/001_schema.sql
-- The source creates users, sessions, stops, vehicles, rides, bookings,
-- ledger, idempotency_records, and outbox with FKs/checks/indexes.
-- Example of a source-defined integrity rule:
CONSTRAINT ck_rides_stops CHECK (origin_stop_id <> destination_stop_id)

-- DML/query example used by a future evidence run
SELECT r.id, s.name AS origin, d.name AS destination,
       r.departure_at, r.seats_available
FROM rides r
JOIN stops s ON s.id = r.origin_stop_id
JOIN stops d ON d.id = r.destination_stop_id
WHERE r.status = 'PUBLISHED'
  AND r.seats_available > 0
ORDER BY r.departure_at, r.id;
```

The exact schema source defines the actual columns, FKs, checks, and indexes. Do not replace the source with a made-up screenshot or claim the query passed before running it against a disposable database.

## SQL: advanced features

Source: `campuspool/sql/migrations/002_evidence.sql`.

```sql
SELECT * FROM driver_ride_summary;
CALL ride_capacity_report('2026-10-26');

-- The source migration also creates:
--   idx_rides_driver_departure_status
--   idx_bookings_ride_status
--   idx_outbox_pending_created
-- and guards active ride edits plus ledger UPDATE/DELETE.
```

These demonstrate a view, stored procedure, indexes, and triggers in the planned DBMS evidence. Transactions and foreign-key/check enforcement are implemented through the application/schema contract and require an actual run record.

## MongoDB: activity projection

Source: `campuspool/src/server/mongo.ts`.

```javascript
db.activity_events.createIndex({ eventId: 1 }, { unique: true });
db.activity_events.createIndex({ audienceIds: 1, createdAt: -1 });

db.activity_events.aggregate([
  { $match: { audienceIds: USER_ID } },
  { $facet: {
      events: [ { $sort: { createdAt: -1, eventId: -1 } }, { $limit: 50 } ],
      summary: [
        { $group: { _id: '$type', count: { $sum: 1 } } },
        { $project: { _id: 0, type: '$_id', count: 1 } }
      ]
  } }
]);
```

The worker uses an `updateOne({eventId}, {$setOnInsert: event}, {upsert: true})` pattern, so retrying an outbox event does not duplicate the projection. MongoDB outage handling and actual index/aggregation output remain pending evidence.
