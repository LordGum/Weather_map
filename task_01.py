import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

data = pd.read_csv('temperature_data.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])
data = data.sort_values(['city', 'timestamp'])

# 1. Скользящее среднее с окном 30 дней
data['rolling_mean'] = data.groupby('city')['temperature'].transform(
    lambda x: x.rolling(30, min_periods=1).mean()
)

# 2. Средняя температура и std по сезонам
season_stats = data.groupby(['city', 'season'])['temperature'].agg(['mean', 'std']).reset_index()
season_stats.columns = ['city', 'season', 'season_mean', 'season_std']
print("Сезонная статистика:")
print(season_stats.head())

# 3. Аномалии (mean ± 2σ)
data = data.merge(season_stats, on=['city', 'season'])
data['anomaly'] = (data['temperature'] < data['season_mean'] - 2*data['season_std']) | \
                  (data['temperature'] > data['season_mean'] + 2*data['season_std'])
print(f"\nВсего аномалий: {data['anomaly'].sum()}")

# 4. Сравнение скорости с распараллеливанием
def analyze_city(city):
    city_data = data[data['city'] == city]
    city_data['rolling'] = city_data['temperature'].rolling(30, min_periods=1).mean()
    return len(city_data)

cities = data['city'].unique()

# Последовательно
start = time.time()
for city in cities:
    analyze_city(city)
seq_time = time.time() - start

# Параллельно
start = time.time()
with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
    list(executor.map(analyze_city, cities))
par_time = time.time() - start

print(f"\nПоследовательно: {seq_time:.3f} сек")
print(f"Параллельно: {par_time:.3f} сек")
print(f"Ускорение: {seq_time/par_time:.2f}x")