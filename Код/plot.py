import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('laythe_flight_data_20251202_142317.csv')

times = data['Time']
orbital_vels = data['Orbital_Velocity']
surface_vels = data['Surface_Velocity']

plt.figure(figsize=(14, 7))
plt.plot(times, orbital_vels, label='Орбитальная скорость', color='blue', linewidth=2)
plt.plot(times, surface_vels, label='Поверхностная скорость', color='red', linewidth=2)
plt.xlabel('Время (секунды)', fontsize=12)
plt.ylabel('Скорость (м/с)', fontsize=12)
plt.title('Изменение скорости во время полёта на Laythe', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

total_time = times.iloc[-1]
max_orbital_vel = orbital_vels.max()
avg_orbital_vel = orbital_vels.mean()
final_body = data['Body'].iloc[-1]

stats_text = f'Время полёта: {total_time/60:.1f} мин ({total_time:.0f} сек)\n'
stats_text += f'Макс. орбитальная скорость: {max_orbital_vel:.0f} м/с\n'
stats_text += f'Средняя орбитальная скорость: {avg_orbital_vel:.0f} м/с\n'
stats_text += f'Финальное тело: {final_body}'

plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.tight_layout()

plt.savefig('laythe_velocity_plot.png', dpi=300, bbox_inches='tight')
print("График сохранён как: laythe_velocity_plot.png")

print("\n=== СТАТИСТИКА ПОЛЁТА НА LAYTHE ===")
print(f"Продолжительность: {total_time:.1f} сек ({total_time/60:.1f} мин)")
print(f"Максимальная орбитальная скорость: {max_orbital_vel:.1f} м/с")
print(f"Средняя орбитальная скорость: {avg_orbital_vel:.1f} м/с")
print(f"Минимальная орбитальная скорость: {orbital_vels.min():.1f} м/с")
print(f"Максимальная поверхностная скорость: {surface_vels.max():.1f} м/с")
print(f"Финальное небесное тело: {final_body}")
print(f"Всего точек данных: {len(data)}")

plt.show()