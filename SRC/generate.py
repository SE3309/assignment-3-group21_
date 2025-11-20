import random
from datetime import datetime, timedelta

# -------------------
# CONFIG
# -------------------
NUM_ROUTES = 40
NUM_AIRCRAFT = 40
NUM_PASSENGERS = 2500
NUM_FLIGHTS = 200
NUM_BOOKINGS = 1000
NUM_CREW = 200
NUM_BAGGAGE = 2500

random.seed(3309)

airports = ["YYZ", "YVR", "YYC", "YUL", "YOW", "YHZ", "JFK", "LAX", "SFO", "ORD"]
aircraft_models = ["Boeing 737", "Airbus A320", "Boeing 787", "Airbus A350", "Embraer E190"]
aircraft_statuses = ["Active", "Maintenance", "Retired"]
flight_statuses = ["Scheduled", "On Time", "Delayed", "Cancelled"]
booking_statuses = ["Confirmed", "Pending", "Cancelled"]
seat_classes = ["Economy", "Premium Economy", "Business"]
baggage_types = ["CarryOn", "Checked", "Oversized"]
crew_roles = ["Pilot", "CoPilot", "FlightAttendant"]


def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def main():
    lines = []

    # Use the AeroDB database
    lines.append("USE AeroDB;")

    # -------------------
    # ROUTES
    # -------------------
    route_id = 1
    route_pairs = set()
    while len(route_pairs) < NUM_ROUTES:
        o, d = random.sample(airports, 2)
        if (o, d) not in route_pairs:
            route_pairs.add((o, d))

    for (o, d) in route_pairs:
        distance = random.randint(300, 8000)
        duration = random.randint(45, 800)
        lines.append(
            f"INSERT INTO Route (RouteID, OriginAirportCode, DestinationAirportCode, DistanceKM, DurationMin) "
            f"VALUES ({route_id}, '{o}', '{d}', {distance}, {duration});"
        )
        route_id += 1
    max_route_id = route_id - 1

    # -------------------
    # AIRCRAFT
    # -------------------
    aircraft_id = 1
    for _ in range(NUM_AIRCRAFT):
        model = random.choice(aircraft_models)
        capacity = random.randint(120, 300)
        status = random.choice(aircraft_statuses)
        lines.append(
            "INSERT INTO Aircraft (AircraftID, Model, Capacity, `Status`) "
            f"VALUES ({aircraft_id}, '{model}', {capacity}, '{status}');"
        )
        aircraft_id += 1
    max_aircraft_id = aircraft_id - 1

    # -------------------
    # PASSENGERS
    # -------------------
    first_names = ["Alex", "Jordan", "Taylor", "Chris", "Sam", "Jamie", "Morgan", "Riley", "Casey", "Drew"]
    last_names = ["Smith", "Johnson", "Lee", "Patel", "Wong", "Brown", "Garcia", "Martin", "Kim", "Singh"]

    passenger_id = 1
    for i in range(NUM_PASSENGERS):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        phone = f"+1-416-{random.randint(200,999)}-{random.randint(1000,9999)}"
        email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
        passport = f"P{1000000 + i}"
        loyalty = random.randint(0, 5)  # stored as VARCHAR but numeric text is fine
        lines.append(
            "INSERT INTO Passenger (PassengerID, FirstName, LastName, Phone, Email, PassportNumber, LoyaltyStatus) "
            f"VALUES ({passenger_id}, '{fn}', '{ln}', '{phone}', '{email}', '{passport}', '{loyalty}');"
        )
        passenger_id += 1
    max_passenger_id = passenger_id - 1

    # -------------------
    # BAGGAGE FEE (range-based)
    # -------------------
    baggage_fee_ranges = {
        "CarryOn": [
            (0.00, 10.00, 0.00),
            (10.01, 23.00, 30.00),
        ],
        "Checked": [
            (0.00, 23.00, 35.00),
            (23.01, 32.00, 75.00),
            (32.01, 45.00, 150.00),
        ],
        "Oversized": [
            (0.00, 32.00, 200.00),
            (32.01, 45.00, 250.00),
        ],
    }

    baggage_fee_id = 1
    baggage_fee_rows = []  # (BaggageFeeID, Type, MinWeight, MaxWeight)
    for btype, ranges in baggage_fee_ranges.items():
        for (min_w, max_w, fee) in ranges:
            lines.append(
                "INSERT INTO BaggageFee (FeeID, `Type`, MinWeightKG, MaxWeightKG, Fee) "
                f"VALUES ({baggage_fee_id}, '{btype}', {min_w:.2f}, {max_w:.2f}, {fee:.2f});"
            )
            baggage_fee_rows.append((baggage_fee_id, btype, min_w, max_w))
            baggage_fee_id += 1

    # -------------------
    # FLIGHTS
    # -------------------
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    flight_id = 1
    flight_to_aircraft = {}   # FlightID -> AircraftID
    flight_departure = {}     # FlightID -> DepartureDateTime

    used_flight_numbers = set()  # to keep FlightNumber UNIQUE

    for _ in range(NUM_FLIGHTS):
        # generate a unique flight number like AC123
        while True:
            flight_num = f"AC{random.randint(100, 999)}"
            if flight_num not in used_flight_numbers:
                used_flight_numbers.add(flight_num)
                break

        dep = random_date(start_date, end_date)
        duration_min = random.randint(45, 800)
        arr = dep + timedelta(minutes=duration_min)
        status = random.choice(flight_statuses)
        rid = random.randint(1, max_route_id)
        aid = random.randint(1, max_aircraft_id)

        lines.append(
            "INSERT INTO Flight (FlightID, FlightNumber, DepartureDateTime, ArrivalDateTime, `Status`, RouteID, AircraftID) "
            f"VALUES ({flight_id}, '{flight_num}', '{dep.strftime('%Y-%m-%d %H:%M:%S')}', "
            f"'{arr.strftime('%Y-%m-%d %H:%M:%S')}', '{status}', {rid}, {aid});"
        )

        flight_to_aircraft[flight_id] = aid
        flight_departure[flight_id] = dep  # save departure time for bookings
        flight_id += 1

    max_flight_id = flight_id - 1

    # -------------------
    # SEATS (per aircraft) + map aircraft -> seat IDs
    # -------------------
    seat_id = 1
    aircraft_seats = {}  # AircraftID -> list of SeatIDs
    for aid in range(1, max_aircraft_id + 1):
        capacity = random.randint(120, 300)
        seat_letters = ["A", "B", "C", "D", "E", "F"]
        count = 0
        row = 1
        aircraft_seats[aid] = []
        while count < capacity:
            for letter in seat_letters:
                if count >= capacity:
                    break
                seat_number = f"{row}{letter}"
                seat_class = "Economy"
                if row <= 3:
                    seat_class = "Business"
                elif row <= 10:
                    seat_class = "Premium Economy"
                lines.append(
                    "INSERT INTO Seat (SeatID, SeatNumber, Class, IsAvailable, AircraftID) "
                    f"VALUES ({seat_id}, '{seat_number}', '{seat_class}', TRUE, {aid});"
                )
                aircraft_seats[aid].append(seat_id)
                seat_id += 1
                count += 1
            row += 1

    # -------------------
    # CREW MEMBERS
    # -------------------
    crew_id = 1
    for i in range(NUM_CREW):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{fn} {ln}"
        role = random.choice(crew_roles)
        if role in ["Pilot", "CoPilot"]:
            cert = f"ATPL-{random.randint(1000,9999)}"
        else:
            cert = f"FA-{random.randint(1000,9999)}"
        contact = f"{fn.lower()}.{ln.lower()}{i}@airlinecrew.com"
        lines.append(
            "INSERT INTO CrewMember (CrewID, `Name`, `Role`, Certification, Contact) "
            f"VALUES ({crew_id}, '{name}', '{role}', '{cert}', '{contact}');"
        )
        crew_id += 1
    max_crew_id = crew_id - 1

    # -------------------
    # BOOKINGS (assign SeatID and valid BookingDate)
    # -------------------
    booking_id = 1
    used_flight_seats = {}  # FlightID -> set of SeatIDs already used on that flight

    for i in range(NUM_BOOKINGS):
        code = f"BK{100000 + i}"
        seat_class = random.choice(seat_classes)

        # pick a flight first
        fid = random.randint(1, max_flight_id)
        dep_dt = flight_departure[fid]

        # choose booking date between global start_date and that flight's departure
        # (ensures BookingDate <= DepartureDateTime, satisfying the trigger)
        bdate = random_date(start_date, dep_dt).date()

        price = round(random.uniform(100, 2000), 2)
        pid = random.randint(1, max_passenger_id)
        status = random.choice(booking_statuses)

        # Determine Aircraft for this Flight
        aircraft_id_for_flight = flight_to_aircraft[fid]
        seats_for_aircraft = aircraft_seats[aircraft_id_for_flight]

        if fid not in used_flight_seats:
            used_flight_seats[fid] = set()

        seat_id_sql = "NULL"
        available_seats = list(set(seats_for_aircraft) - used_flight_seats[fid])
        if available_seats:
            chosen_seat_id = random.choice(available_seats)
            used_flight_seats[fid].add(chosen_seat_id)
            seat_id_sql = str(chosen_seat_id)
        # else: no seats left → SeatID stays NULL, which is allowed

        lines.append(
            "INSERT INTO Booking (BookingID, BookingCode, SeatClass, BookingDate, Price, FlightID, PassengerID, SeatID, `Status`) "
            f"VALUES ({booking_id}, '{code}', '{seat_class}', '{bdate}', {price}, {fid}, {pid}, {seat_id_sql}, '{status}');"
        )
        booking_id += 1
    max_booking_id = booking_id - 1

    # -------------------
    # FLIGHT CREW ASSIGNMENTS
    # -------------------
    assignment_id = 1
    for fid in range(1, max_flight_id + 1):
        # For each flight, assign 5 distinct crew members
        assigned_crew = random.sample(range(1, max_crew_id + 1), k=5)
        for cid in assigned_crew:
            lines.append(
                "INSERT INTO FlightCrewAssignment (AssignmentID, FlightID, CrewID) "
                f"VALUES ({assignment_id}, {fid}, {cid});"
            )
            assignment_id += 1

    # -------------------
    # BAGGAGE (now uses BaggageFeeID + Type + WeightKG)
    # -------------------
    baggage_id = 1
    tag_number = 100000
    for _ in range(NUM_BAGGAGE):
        bid = random.randint(1, max_booking_id)
        # choose a random fee row and generate weight within its range
        fee_row = random.choice(baggage_fee_rows)
        fee_id, btype, min_w, max_w = fee_row
        # Ensure weight is always > 0 to satisfy check constraint (WeightKG > 0)
        effective_min = 0.01 if min_w == 0.0 else min_w
        weight = round(random.uniform(effective_min, max_w), 2)
        # Safety check: ensure weight is never exactly 0
        if weight <= 0.0:
            weight = 0.01
        status = random.choice(["CheckedIn", "Loaded", "InTransit", "Delivered"])
        lines.append(
            "INSERT INTO Baggage (BaggageID, BookingID, TagNumber, FeeID, `Type`, WeightKG, `Status`) "
            f"VALUES ({baggage_id}, {bid}, {tag_number}, {fee_id}, '{btype}', {weight:.2f}, '{status}');"
        )
        baggage_id += 1
        tag_number += 1

    # -------------------
    # OUTPUT
    # -------------------
    with open("aerodb_data.sql", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"Generated aerodb_data.sql with {len(lines)} INSERT statements.")
    print(f"File saved to: aerodb_data.sql")


if __name__ == "__main__":
    main()
