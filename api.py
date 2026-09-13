from fastapi import FastAPI

app = FastAPI()

@app.post("/events")
def receive_event(event: dict):
    validation_errors = []

    if "passengers" not in event:
        validation_errors.append("Missing passengers")
    elif not isinstance(event["passengers"], int):
        validation_errors.append("Passengers must be an integer")
    elif event["passengers"] < 0:
        validation_errors.append("Passengers must be non-negative")

    if "speed_kmh" not in event:
        validation_errors.append("Missing speed_kmh")
    elif not isinstance(event["speed_kmh"], int):
        validation_errors.append("Speed must be an integer")
    elif not 0 <= event["speed_kmh"] <= 120:
        validation_errors.append("Speed must be between 0 and 120")

    if "status" not in event:
        validation_errors.append("Missing status")
    elif event["status"] not in {"ON_ROUTE", "STOPPED"}:
        validation_errors.append("Status must be ON_ROUTE or STOPPED")

    if (
        event.get("status") == "STOPPED"
        and event.get("speed_kmh") != 0
    ):
        validation_errors.append("STOPPED event must have speed 0")

    if validation_errors:
        return {
            "accepted": False,
            "validation_errors": validation_errors,
            "occupancy_category": None
        }

    passengers = event["passengers"]

    if passengers <= 10:
        occupancy = "LOW"
    elif passengers <= 20:
        occupancy = "MEDIUM"
    elif passengers <= 30:
        occupancy = "HIGH"
    else:
        occupancy = "OVER_CAPACITY"

    return {
        "accepted": True,
        "validation_errors": [],
        "occupancy_category": occupancy
    }