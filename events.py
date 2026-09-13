import pandas as pd

df = pd.DataFrame([
    {
        "Timestamp": "08:00",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 18,
        "Speed_kmh": 31,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:01",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 22,
        "Speed_kmh": 28,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:02",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 21,
        "Speed_kmh": 29,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:03",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 25,
        "Speed_kmh": 27,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:04",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 24,
        "Speed_kmh": 0,
        "Status": "STOPPED"
    },
    {
        "Timestamp": "08:05",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 26,
        "Speed_kmh": 30,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:06",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 23,
        "Speed_kmh": 32,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:07",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 28,
        "Speed_kmh": 26,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:08",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 27,
        "Speed_kmh": 25,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:09",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 30,
        "Speed_kmh": 24,
        "Status": "ON_ROUTE"
    }
])

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%H:%M"
)

df["Passengers"] = df["Passengers"].astype(int)
df["Speed_kmh"] = df["Speed_kmh"].astype(int)

VALID_STATUSES = {"ON_ROUTE", "STOPPED"}


def validate_event(event: dict) -> dict:
    required_fields = [
        "Timestamp",
        "Route",
        "Bus",
        "Passengers",
        "Speed_kmh",
        "Status"
    ]

    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(event["Timestamp"], pd.Timestamp):
        raise ValueError("Timestamp must be a pandas Timestamp")

    if not isinstance(event["Passengers"], int):
        raise ValueError("Passengers must be an integer")

    if event["Passengers"] < 0:
        raise ValueError("Passengers must be non-negative")

    if not isinstance(event["Speed_kmh"], int):
        raise ValueError("Speed_kmh must be an integer")

    if not 0 <= event["Speed_kmh"] <= 120:
        raise ValueError("Speed_kmh must be between 0 and 120")

    if event["Status"] not in VALID_STATUSES:
        raise ValueError(
            "Status must be ON_ROUTE or STOPPED"
        )

    if (event["Status"] == "STOPPED" and event["Speed_kmh"] != 0):
        raise ValueError(
            "A STOPPED bus must have speed 0"
        )

    return event


def event_generator(dataframe):
    for _, row in dataframe.iterrows():
        event = row.to_dict()
        yield validate_event(event)


def process_stream(stream):
    processed_count = 0

    for event in stream:
        processed_count += 1

        print(
            f"Event {processed_count}: "
            f"{event['Timestamp'].strftime('%H:%M')} | "
            f"Bus {event['Bus']} | "
            f"Passengers: {event['Passengers']} | "
            f"Speed: {event['Speed_kmh']} | "
            f"Status: {event['Status']}"
        )

    return processed_count


def dataframe_to_json(dataframe, filename="events.json"):
    json_data = dataframe.copy()
    json_data = json_data.rename(columns={
        "Timestamp": "timestamp",
        "Route": "route",
        "Bus": "bus",
        "Passengers": "passengers",
        "Speed_kmh": "speed_kmh",
        "Status": "status"
    })
    json_data["timestamp"] = json_data["timestamp"].dt.strftime("%H:%M")
    json_data.to_json(filename, orient="records", indent=4, force_ascii=False)

def get_occupancy_category(passengers: int) -> str:
    if 0 <= passengers <= 10:
        return "LOW"
    elif 11 <= passengers <= 20:
        return "MEDIUM"
    elif 21 <= passengers <= 30:
        return "HIGH"
    else:
        return "OVER_CAPACITY"


def analyze_dataframe(dataframe):
    average_passengers = dataframe[
        "Passengers"
    ].mean()

    maximum_passengers = dataframe[
        "Passengers"
    ].max()

    stopped_events = (
        dataframe["Status"] == "STOPPED"
    ).sum()

    busiest_index = dataframe[
        "Passengers"
    ].idxmax()

    busiest_event = dataframe.loc[busiest_index]

    busiest_minute = busiest_event[
        "Timestamp"
    ].strftime("%H:%M")

    busiest_bus = busiest_event["Bus"]

    return {
        "average_passengers": average_passengers,
        "maximum_passengers": maximum_passengers,
        "stopped_events": stopped_events,
        "busiest_minute": busiest_minute,
        "busiest_bus": busiest_bus
    }


if __name__ == "__main__":
    stream = event_generator(df)
    process_stream(stream)
    dataframe_to_json(df)

    results = analyze_dataframe(df)

    for key, value in results.items():
        print(f"{key}: {value}")