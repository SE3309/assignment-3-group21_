-- 1) Insert a lost baggage record for the latest booking of a passenger
INSERT INTO Baggage (BookingID, TagNumber, `Type`, WeightKG, FeeID, `Status`)
SELECT b.BookingID,
       900001 AS TagNumber,
       'Checked' AS `Type`,
       18.40 AS WeightKG,
       f.FeeID,
       'Missing' AS `Status`
FROM Booking b
JOIN Passenger p
  ON p.PassengerID = b.PassengerID
JOIN BaggageFee f
  ON f.`Type` = 'Standard'
 AND 18.40 BETWEEN f.MinWeightKG AND f.MaxWeightKG
WHERE p.PassportNumber = 'X1234567'     -- choose a real passport number from your data
  AND b.`Status` = 'Completed'
ORDER BY b.BookingDate DESC
LIMIT 1;

-- 2) Update loyalty status based on total completed booking spend
UPDATE Passenger p
JOIN (
    SELECT PassengerID,
           SUM(Price) AS total_spent
    FROM Booking
    WHERE `Status` = 'Completed'
    GROUP BY PassengerID
) AS x
  ON p.PassengerID = x.PassengerID
SET p.LoyaltyStatus = p.LoyaltyStatus + FLOOR(x.total_spent / 100);

-- 3) Delete baggage linked to old cancelled bookings only
DELETE b
FROM Baggage b
JOIN Booking bk
  ON b.BookingID = bk.BookingID
WHERE bk.`Status` = 'Cancelled'
  AND bk.BookingDate < '2024-01-01';
