import krpc
import time as t
import json


def main():
    conn = krpc.connect(name="full_flight_logger")
    vessel = conn.space_center.active_vessel

    start_ut = conn.space_center.ut

    time_data = []
    height_data = []
    speed_data = []
    apoapsis_data = []
    periapsis_data = []
    time = 0

    print("Начат лог всего полёта...")

    while True:
        current_ut = conn.space_center.ut

        flight = vessel.flight()
        orbit = vessel.orbit

        height = flight.surface_altitude
        speed = vessel.flight(
            orbit.body.reference_frame
        ).speed

        time_data.append(time)
        height_data.append(height)
        speed_data.append(speed)
        apoapsis_data.append(orbit.apoapsis_altitude)
        periapsis_data.append(orbit.periapsis_altitude)

        print(
            f"t={time}s | "
            f"h={height:.1f}m | "
            f"v={speed:.1f}m/s"
        )

        if vessel.situation == vessel.situation.landed:
            print("Полёт завершён.")
            break

        t.sleep(1)
        time += 1

    data = {
        "time": time_data,
        "height": height_data,
        "speed": speed_data,
        "apoapsis": apoapsis_data,
        "periapsis": periapsis_data,
        "body": orbit.body.name
    }

    with open("flight_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Данные сохранены в flight_data.json")

if __name__ == "__main__":
    main()
