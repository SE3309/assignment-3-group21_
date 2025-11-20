USE AeroDB;

-- 1: All columns, all rows (SELECT * pattern from slides)
-- List full details of all passengers.
SELECT *
FROM Passenger;


-- 2: Specific columns + for departures in or after 2025 + order by departure date time
-- List flights departing on or after a given date, ordered by departure time.
SELECT
    FlightNumber,
    DepartureDateTime,
    ArrivalDateTime,
    `Status`
FROM Flight
WHERE DepartureDateTime >= '2025-01-01'
ORDER BY DepartureDateTime;


-- 3: Use of DISTINCT
-- List distinct seat classes that appear in bookings.
SELECT DISTINCT
    SeatClass
FROM Booking
ORDER BY SeatClass;


-- 4: Pattern matching with LIKE TODO SIMILAR TO 2 STRUCT.
-- Find passengers whose email address contains 'gmail.com'.
SELECT
    PassengerID,
    FirstName,
    LastName,
    Email
FROM Passenger
WHERE Email LIKE '%example.com'
ORDER BY LastName, FirstName;


-- 5: Aggregate with COUNT and WHERE
-- How many baggage items are heavier than 20 kg?
SELECT
    COUNT(*) AS NumHeavyBags
FROM Baggage
WHERE WeightKG > 20.00;


-- 6: GROUP BY with aggregates
-- For each booking status, show number of bookings and average price.
SELECT
    `Status`,
    COUNT(*) AS NumBookings,
    AVG(Price) AS AvgPrice
FROM Booking
WHERE `Status` IS NOT NULL
GROUP BY `Status`
ORDER BY NumBookings DESC;


-- 7: GROUP BY + HAVING (restricted groupings)
-- For each seat class, show number of bookings and average price,
-- but only keep classes with average price > 500.
SELECT
    SeatClass,
    COUNT(*) AS NumBookings,
    AVG(Price) AS AvgPrice
FROM Booking
WHERE SeatClass IS NOT NULL
GROUP BY SeatClass
HAVING AVG(Price) > 500.00
ORDER BY AvgPrice DESC;