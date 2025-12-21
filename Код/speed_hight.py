import krpc
import matplotlib.pyplot as plt
import time as t
import json

def main():
    conn = krpc.connect(name='speed_hight_checker')
    vessel = conn.space_center.active_vessel

    time_values = []
    height_values = []
    speed_values = []
    time = 0

    while True:
        height = vessel.flight().surface_altitude
        speed = vessel.flight(
            vessel.orbit.body.reference_frame
        ).speed

        time_values.append(time)
        height_values.append(height)
        speed_values.append(speed)

        print(
            f"Время: {time} s | "
            f"Высота: {height:.1f} m | "
            f"Скорость: {speed:.1f} m/s"
        )

        if height > 90_000:
            print("Достигнута высота 90 км. Сбор данных остановлен.")
            break

        t.sleep(1)
        time += 1

    height_data = {
        "time": time_values,
        "altitude": height_values
    }

    speed_data = {
        "time": time_values,
        "speed": speed_values
    }

    with open("height_data.json", "w") as f:
        json.dump(height_data, f, indent=4)

    with open("speed_data.json", "w") as f:
        json.dump(speed_data, f, indent=4)

    print("Данные сохранены в JSON файлы.")

    plt.figure()
    plt.plot(time_values, height_values)
    plt.title("Зависимость высоты от времени")
    plt.xlabel("Время, s")
    plt.ylabel("Высота, m")
    plt.grid()
    plt.savefig("./graphics/height_graph.png", dpi=300, bbox_inches="tight")
    plt.show()

    plt.figure()
    plt.plot(time_values, speed_values)
    plt.title("Зависимость скорости от времени")
    plt.xlabel("Время, s")
    plt.ylabel("Скорость, m/s")
    plt.grid()
    plt.savefig("./graphics/speed_graph.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
