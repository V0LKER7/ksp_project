import krpc
import time
import csv
import matplotlib.pyplot as plt
from datetime import datetime

print("Подключение к Kerbal Space Program...")
conn = krpc.connect(name='Laythe Flight Monitor')
vessel = conn.space_center.active_vessel

orbit_ref = vessel.orbit.body.orbital_reference_frame
surface_ref = vessel.orbit.body.non_rotating_reference_frame

print(f"Подключено к кораблю: {vessel.name}")
print(f"Текущее небесное тело: {vessel.orbit.body.name}")
print("Начало записи данных...")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"laythe_flight_data_{timestamp}.csv"

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'Orbital_Velocity', 'Surface_Velocity', 
                     'Altitude', 'Body', 'Apoapsis', 'Periapsis'])

start_time = time.time()
data_points = []
update_interval = 1.0

print("\n=== МОНИТОРИНГ ПОЛЁТА НА LAYTHE ===\n")

try:
    while True:
        current_time = time.time() - start_time
        
        orbital_velocity = vessel.orbit.speed
        
        altitude = vessel.flight().mean_altitude
        body_name = vessel.orbit.body.name
        apoapsis = vessel.orbit.apoapsis_altitude
        periapsis = vessel.orbit.periapsis_altitude
        
        data_point = {
            'time': current_time,
            'orbital_vel': orbital_velocity,
            'altitude': altitude,
            'body': body_name,
            'apoapsis': apoapsis if apoapsis > 0 else 0,
            'periapsis': periapsis if periapsis > 0 else 0
        }
        data_points.append(data_point)
        
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                round(current_time, 2),
                round(orbital_velocity, 2),
                round(altitude, 2),
                body_name,
                round(apoapsis, 2) if apoapsis > 0 else 0,
                round(periapsis, 2) if periapsis > 0 else 0
            ])
        
        print(f"\rВремя: {current_time:.1f}с | "
              f"Тело: {body_name} | "
              f"Орб.скорость: {orbital_velocity:.1f} м/с | "
              f"Высота: {altitude/1000:.2f} км", end='')
        
        if body_name in ['Jool', 'Laythe'] and len(data_points) > 1:
            if data_points[-2]['body'] not in ['Jool', 'Laythe']:
                print(f"\n*** ДОСТИГНУТА СИСТЕМА JOOL! Текущее тело: {body_name} ***")
        
        if vessel.situation.name in ['landed', 'splashed']:
            print("\n\n=== ПОСАДКА ОБНАРУЖЕНА! ===")
            break
        
        time.sleep(update_interval)
        
except KeyboardInterrupt:
    print("\n\nМониторинг остановлен пользователем.")

print(f"\nДанные сохранены в файл: {filename}")
print(f"Всего записано точек данных: {len(data_points)}")

print("\nПостроение графика скорости...")

times = [d['time'] for d in data_points]
orbital_vels = [d['orbital_vel'] for d in data_points]
surface_vels = [d['surface_vel'] for d in data_points]

plt.figure(figsize=(12, 6))
plt.plot(times, orbital_vels, label='Орбитальная скорость', color='blue', linewidth=2)
plt.xlabel('Время (секунды)', fontsize=12)
plt.ylabel('Скорость (м/с)', fontsize=12)
plt.title(f'Изменение скорости во время полёта на Laythe - {vessel.name}', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

total_time = times[-1]
max_orbital_vel = max(orbital_vels)

stats_text = f'Время полёта: {total_time/60:.1f} мин\n'
stats_text += f'Макс. скорость: {max_orbital_vel:.0f} м/с\n'

plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.tight_layout()

plot_filename = f"laythe_flight_plot_{timestamp}.png"
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
print(f"График сохранён: {plot_filename}")

plt.show()

print("\n=== ИТОГОВАЯ СТАТИСТИКА ===")
print(f"Продолжительность полёта: {total_time:.1f} сек ({total_time/60:.1f} мин)")
print(f"Максимальная орбитальная скорость: {max_orbital_vel:.1f} м/с")
print(f"Средняя орбитальная скорость: {sum(orbital_vels)/len(orbital_vels):.1f} м/с")
print(f"\nВсе данные сохранены!")