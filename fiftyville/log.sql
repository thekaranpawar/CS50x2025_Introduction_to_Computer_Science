-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. Find the crime scene report for July 28, 2024 on Humphrey Street
SELECT * FROM crime_scene_reports
WHERE year = 2024 AND month = 7 AND day = 28
  AND street = 'Humphrey Street';

-- 2. Look up witness interviews from that day for leads
SELECT * FROM interviews
WHERE year = 2024 AND month = 7 AND day = 28;

-- 3. Check ATM transactions on that date for suspicious withdrawals
SELECT * FROM atm_transactions
WHERE year = 2024 AND month = 7 AND day = 28
ORDER BY hour, minute;

-- 4. Look at bakery security logs near Humphrey Street around the time
--    for vehicles leaving town after the theft
SELECT * FROM bakery_security_logs
WHERE date = '2024-07-28'
ORDER BY time;

-- 5. Narrow to suspect person via license plates or descriptions
--    (if plates link to owner in `vehicle_owners`)
SELECT * FROM vehicle_owners
WHERE license_plate = '[SUSPICIOUS PLATE]';

-- 6. Query phone calls around that time to identify accomplice
SELECT * FROM phone_calls
WHERE date = '2024-07-28'
  AND from_person_id IN (
      /* suspect’s person_id */
  );

-- 7. Identify the first flight out of Fiftyville after the theft
SELECT f.id AS flight_id,
       a.city AS destination_city,
       f.year, f.month, f.day, f.hour, f.minute
FROM flights f
JOIN airports a ON f.destination_airport_id = a.id
WHERE f.year = 2024
  AND DATE(f.year || '-' || f.month || '-' || f.day) >= '2024-07-28'
ORDER BY f.year, f.month, f.day, f.hour, f.minute
LIMIT 1;

-- 8. List passengers on that flight to find the thief and accomplice
SELECT p.person_id, persons.name
FROM passengers p
JOIN persons ON p.person_id = persons.id
WHERE p.flight_id = [flight_id from previous query];

-- 9. Cross-check if those passengers had suspicious transactions or calls
SELECT * FROM phone_calls
WHERE (from_person_id = [thief_id] OR to_person_id = [thief_id])
  AND date BETWEEN '2024-07-27' AND '2024-07-29';

SELECT * FROM phone_calls
WHERE (from_person_id = [accomplice_id] OR to_person_id = [accomplice_id])
  AND date BETWEEN '2024-07-27' AND '2024-07-29';

-- 10. Summarize conclusion (not a query but a note)
-- Based on witness reports, ATM withdrawal matching thief, flight passenger list,
-- and phone call connection between suspect and accomplice, we've identified:
-- thief as [Name], accomplice as [Name], city escaped to: [Destination City].
