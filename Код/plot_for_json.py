import json
import matplotlib.pyplot as plt


JSON_PATH = "flight_data.json"

def plot_from_json():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    time = data["time"]
    height = data["height"]
    speed = data["speed"]

    plt.figure(figsize=(14, 7))
    plt.plot(time, height)
    plt.title("Высота от времени")
    plt.xlabel("Время, s")
    plt.ylabel("Высота, m")
    plt.grid()
    plt.savefig("./graphics/full_flight_height.png", dpi=300, bbox_inches="tight")
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(time, speed)
    plt.title("Орбитальная скорость от времени")
    plt.xlabel("Время, s")
    plt.ylabel("Скорость, m/s")
    plt.grid()
    plt.savefig("./graphics/full_flight_speed.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_from_json()
