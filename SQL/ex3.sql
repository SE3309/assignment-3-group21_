use aeroDB;

DROP TABLE IF EXISTS FlightCrewAssignment;
DROP TABLE IF EXISTS Baggage;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS CrewMember;
DROP TABLE IF EXISTS BaggageFee;
DROP TABLE IF EXISTS Passenger;
DROP TABLE IF EXISTS Route;

CREATE TABLE Route (
    RouteID INT NOT NULL AUTO_INCREMENT,
    OriginAirportCode CHAR(3) NOT NULL,
    DestinationAirportCode CHAR(3) NOT NULL,
    DistanceKM INT NOT NULL,
    DurationMin INT NOT NULL,
    PRIMARY KEY (RouteID)
);

-- Insert Method 1
INSERT INTO Route 
VALUES
(
	NULL,
	'YYZ',
	'YYC',
	5000,
	756
);
SELECT * FROM Route; -- Just to output

-- Insert Method 2
-- Multi insert
INSERT INTO Route(
	OriginAirportCode,
	DestinationAirportCode,
	DistanceKM,
    DurationMin
)
VALUES
	(
    'JFK',
    'LAX',
    '2000',
    '100'
    ),
    (
    'YVR',
    'YHZ',
    '2000',
    '100'
    );
SELECT * FROM Route;

-- Insert Method 3 (Insert 'return' flights from routes)
INSERT INTO Route(
	OriginAirportCode,
	DestinationAirportCode,
	DistanceKM,
    DurationMin
)
SELECT 
	DestinationAirportCode,
	OriginAirportCode,
	DistanceKM,
    DurationMin
FROM Route
WHERE OriginAirportCode <> DestinationAirportCode;
SELECT * FROM Route;