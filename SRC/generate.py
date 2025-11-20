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
    # OUTPUT
    # -------------------
    with open("aerodb_data.sql", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"Generated aerodb_data.sql with {len(lines)} INSERT statements.")
    print(f"File saved to: aerodb_data.sql")


if __name__ == "__main__":
    main()
