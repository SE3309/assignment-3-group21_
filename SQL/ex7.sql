USE AeroDB;

CREATE OR REPLACE VIEW FlightDetailsView AS
SELECT 
    f.FlightID,
    f.FlightNumber,
    f.DepartureDateTime,
    f.ArrivalDateTime,
    f.Status AS FlightStatus,
    r.OriginAirportCode,
    r.DestinationAirportCode,
    r.DistanceKM,
    r.DurationMin AS RouteDurationMin,
    a.Model AS AircraftModel,
    a.Capacity AS AircraftCapacity
FROM 
    Flight f
    INNER JOIN Route r ON f.RouteID = r.RouteID
    INNER JOIN Aircraft a ON f.AircraftID = a.AircraftID;

CREATE OR REPLACE VIEW BookingSummaryView AS
SELECT 
    b.BookingID,
    b.BookingCode,
    b.BookingDate,
    b.Price,
    b.SeatClass,
    b.Status AS BookingStatus,
    p.FirstName,
    p.LastName,
    p.Email,
    p.PassportNumber,
    f.FlightNumber,
    f.DepartureDateTime,
    f.ArrivalDateTime,
    s.SeatNumber,
    s.Class AS SeatClassType
FROM 
    Booking b
    INNER JOIN Passenger p ON b.PassengerID = p.PassengerID
    INNER JOIN Flight f ON b.FlightID = f.FlightID
    LEFT JOIN Seat s ON b.SeatID = s.SeatID;

SELECT 
    FlightNumber,
    OriginAirportCode,
    DestinationAirportCode,
    DepartureDateTime,
    AircraftModel,
    DistanceKM,
    FlightStatus
FROM 
    FlightDetailsView
WHERE 
    OriginAirportCode = 'YYZ'
ORDER BY 
    DepartureDateTime
LIMIT 10;

SELECT 
    BookingCode,
    FirstName,
    LastName,
    Email,
    FlightNumber,
    SeatNumber,
    SeatClass,
    Price,
    BookingDate
FROM 
    BookingSummaryView
WHERE 
    BookingStatus = 'Confirmed'
ORDER BY 
    BookingDate DESC
LIMIT 10;

SHOW CREATE VIEW FlightDetailsView;
SHOW CREATE VIEW BookingSummaryView;

SELECT 
    TABLE_NAME AS ViewName,
    VIEW_DEFINITION
FROM 
    INFORMATION_SCHEMA.VIEWS
WHERE 
    TABLE_SCHEMA = 'AeroDB';

