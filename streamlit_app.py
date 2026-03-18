import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.main_content import (
    render_descriptive_stats,
    render_time_series,
    render_seasonal_profiles,
    render_performance_comparison,
    render_current_temperature
)
from utils.data_processor import load_and_prepare_data, calculate_rolling_stats, get_season_stats

st.set_page_config(layout="wide")
st.title("Анализ температурных данных")

uploaded_file = st.file_uploader("Загрузите CSV файл с историческими данными", type="csv")
if uploaded_file is None:
    st.info("Пожалуйста, загрузите файл temperature_data.csv")
    st.stop()

df = pd.read_csv(uploaded_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

cities = df['city'].unique()
selected_city = st.selectbox("Выберите город", cities)

api_key = st.text_input("Введите API ключ OpenWeatherMap", type="password")

city_df = load_and_prepare_data(df, selected_city)
city_df = calculate_rolling_stats(city_df)
season_stats = get_season_stats(city_df)

st.header(f"Анализ для города {selected_city}")
render_descriptive_stats(city_df)
render_time_series(city_df, selected_city)
render_seasonal_profiles(city_df, selected_city, season_stats)
render_performance_comparison(df, cities)
render_current_temperature(api_key, selected_city, season_stats)

render_sidebar()