-- Drop database if exists to avoid warning, then create fresh
-- Dropping the database automatically drops all tables, so no need for individual DROP TABLE statements
DROP DATABASE IF EXISTS AeroDB;
CREATE DATABASE AeroDB;
USE AeroDB;

CREATE TABLE Route (
    RouteID INT NOT NULL AUTO_INCREMENT,
    OriginAirportCode CHAR(3) NOT NULL,
    DestinationAirportCode CHAR(3) NOT NULL,
    DistanceKM INT NOT NULL,
    DurationMin INT NOT NULL,
    PRIMARY KEY (RouteID),
    CONSTRAINT chk_route_different_airports
        CHECK (OriginAirportCode != DestinationAirportCode)
);

CREATE TABLE Aircraft (
    AircraftID INT NOT NULL AUTO_INCREMENT,
    Model VARCHAR(50) NOT NULL,
    Capacity INT NOT NULL,
    `Status` VARCHAR(20) NOT NULL, -- status is a keyword watch out!
    PRIMARY KEY (AircraftID)
);

CREATE TABLE Passenger (
    PassengerID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName  VARCHAR(50) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(100) NOT NULL,
    PassportNumber VARCHAR(20) UNIQUE NOT NULL,
    LoyaltyStatus INT DEFAULT 0,
    PRIMARY KEY (PassengerID)
);

CREATE TABLE Flight (
    FlightID INT NOT NULL AUTO_INCREMENT,
    FlightNumber VARCHAR(10) UNIQUE NOT NULL,
    DepartureDateTime DATETIME NOT NULL,
    ArrivalDateTime   DATETIME NOT NULL,
    `Status` VARCHAR(20) NOT NULL,
    RouteID INT NOT NULL, -- FK
    AircraftID INT NOT NULL, -- FK
    PRIMARY KEY (FlightID),
    CONSTRAINT fk_flight_route
        FOREIGN KEY (RouteID) REFERENCES Route(RouteID),
    CONSTRAINT fk_flight_aircraft
        FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID),
    CONSTRAINT chk_flight_arrival_after_departure
        CHECK (ArrivalDateTime > DepartureDateTime)
);

CREATE TABLE Seat (
    SeatID INT NOT NULL AUTO_INCREMENT,
    SeatNumber VARCHAR(5) NOT NULL,
    Class VARCHAR(20) NOT NULL,
    IsAvailable BOOLEAN NOT NULL DEFAULT TRUE,
    AircraftID INT NOT NULL,
    PRIMARY KEY (SeatID),
    UNIQUE KEY uq_aircraft_seat (AircraftID, SeatNumber),
    CONSTRAINT fk_seat_aircraft
        FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID)
);

CREATE TABLE Booking (
    BookingID INT NOT NULL AUTO_INCREMENT,
    BookingCode VARCHAR(20) NOT NULL,
    SeatClass VARCHAR(20) NOT NULL,
    BookingDate DATE NOT NULL,
    Price DECIMAL(7,2) NOT NULL,
    FlightID INT NOT NULL,
    PassengerID INT NOT NULL, -- NOTE: Assumption is each booking only is associated with one passenger
    SeatID INT, -- FK to Seat
    `Status` VARCHAR(20) NOT NULL,
    PRIMARY KEY (BookingID),
    UNIQUE KEY uq_bookingcode (BookingCode),
    CONSTRAINT fk_booking_flight
        FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
    CONSTRAINT fk_booking_passenger
        FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
    CONSTRAINT fk_booking_seat
        FOREIGN KEY (SeatID) REFERENCES Seat(SeatID)
    -- NOTE: BookingDate should be <= Flight.DepartureDateTime
    -- This requires a trigger or application-level validation
);

CREATE TABLE BaggageFee ( 
    FeeID INT NOT NULL AUTO_INCREMENT,
    `Type` VARCHAR(20) NOT NULL, 
    MinWeightKG DECIMAL(5,2) NOT NULL,
    MaxWeightKG DECIMAL(5,2) NOT NULL,
    Fee DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (FeeID),
    CONSTRAINT chk_baggagefee_weight_range
        CHECK (MaxWeightKG >= MinWeightKG)
);

CREATE TABLE Baggage (
    BaggageID INT NOT NULL AUTO_INCREMENT,
    BookingID INT NOT NULL,
    TagNumber INT NOT NULL,
    `Type` VARCHAR(20) NOT NULL,
    WeightKG DECIMAL(5,2) NOT NULL,
    FeeID INT NOT NULL, -- FK to BaggageFee
    `Status` VARCHAR(20) NOT NULL,
    PRIMARY KEY (BaggageID),
    UNIQUE KEY uq_baggage_tagnumber (TagNumber),
    CONSTRAINT fk_baggage_booking
        FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
    CONSTRAINT fk_baggage_fee
        FOREIGN KEY (FeeID) REFERENCES BaggageFee(FeeID),
    CONSTRAINT chk_baggage_weight_in_range
        CHECK (WeightKG > 0)
) ;

CREATE TABLE CrewMember (
    CrewID INT NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(100) NOT NULL,
    `Role` VARCHAR(20) NOT NULL, -- e.g. 'Pilot', 'FlightAttendant'
    Certification VARCHAR(50),
    Contact VARCHAR(100) NOT NULL,
    PRIMARY KEY (CrewID),
    UNIQUE KEY uq_crew_contact (Contact)
);

CREATE TABLE FlightCrewAssignment (
    AssignmentID INT NOT NULL AUTO_INCREMENT,
    FlightID INT NOT NULL,
    CrewID INT NOT NULL,
    PRIMARY KEY (AssignmentID),
    UNIQUE KEY uq_flight_crew (FlightID, CrewID), -- Prevent duplicate assignments
    CONSTRAINT fk_fca_flight
        FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
    CONSTRAINT fk_fca_crew
        FOREIGN KEY (CrewID) REFERENCES CrewMember(CrewID)
);

DESCRIBE Passenger;
DESCRIBE Booking;
DESCRIBE Baggage;
DESCRIBE BaggageFee;
DESCRIBE Flight;
DESCRIBE Route;
DESCRIBE Aircraft;
DESCRIBE Seat;
DESCRIBE CrewMember;
DESCRIBE FlightCrewAssignment;
