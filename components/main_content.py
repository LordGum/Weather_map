import streamlit as st
from utils.visualization import create_time_series_plot, create_seasonal_boxplot
from utils.api_client import get_temp_sync, get_temp_async, check_temperature_anomaly
from utils.performance import compare_performance
from utils.data_processor import analyze_city
from utils.heatmap import render_weather_heatmap
import asyncio
import time


def render_descriptive_stats(city_df):
    st.subheader("Описательная статистика")
    st.dataframe(city_df['temperature'].describe())


def render_time_series(city_df, selected_city):
    st.subheader("Временной ряд с аномалиями")
    fig = create_time_series_plot(city_df, selected_city)
    st.plotly_chart(fig, use_container_width=True)


def render_seasonal_profiles(city_df, selected_city, season_stats):
    st.subheader("Сезонные профили")
    fig = create_seasonal_boxplot(city_df, selected_city)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(season_stats)


def render_performance_comparison(df, cities):
    st.subheader("⚡ Сравнение производительности анализа")
    if st.button("Запустить сравнение производительности"):
        sequential_time, parallel_time = compare_performance(list(cities), df, analyze_city)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Последовательный анализ", f"{sequential_time:.2f} сек")
        with col2:
            st.metric("Параллельный анализ", f"{parallel_time:.2f} сек")

        st.write(f"Ускорение: {sequential_time / parallel_time:.2f}x")


def render_current_temperature(api_key, selected_city, season_stats):
    if not api_key:
        st.info("Введите API ключ для отображения текущей температуры")
        return

    st.header("Текущая температура")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Синхронный запрос")
        start_time = time.time()
        try:
            current_temp_sync = get_temp_sync(selected_city, api_key)
            sync_time = time.time() - start_time

            if current_temp_sync:
                st.metric("Температура", f"{current_temp_sync}°C")
                st.write(f"Время: {sync_time:.2f} сек")

                is_normal, current_season = check_temperature_anomaly(current_temp_sync, season_stats)

                if is_normal:
                    st.success(f"Текущая температура в норме для сезона {current_season.capitalize()}")
                else:
                    st.error(f"Текущая температура аномальна для сезона {current_season.capitalize()}")
            else:
                st.error("Ошибка API: Неверный ключ или город")
        except Exception as e:
            st.error(f"Ошибка: {e}")

    with col2:
        st.subheader("Асинхронный запрос")
        start_time = time.time()
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            current_temp_async = loop.run_until_complete(get_temp_async(selected_city, api_key))
            async_time = time.time() - start_time

            if current_temp_async:
                st.metric("Температура", f"{current_temp_async}°C")
                st.write(f"Время: {async_time:.2f} сек")
            else:
                st.error("Ошибка API: Неверный ключ или город")
        except Exception as e:
            st.error(f"Ошибка: {e}")


def render_heatmap(apikey):
    render_weather_heatmap(apikey)