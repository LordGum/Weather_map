import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

CITIES = [
    {"name": "Москва", "lat": 55.7558, "lon": 37.6173},
    {"name": "Лондон", "lat": 51.5074, "lon": -0.1278},
    {"name": "Нью-Йорк", "lat": 40.7128, "lon": -74.0060},
    {"name": "Токио", "lat": 35.6762, "lon": 139.6503},
    {"name": "Париж", "lat": 48.8566, "lon": 2.3522},
    {"name": "Сидней", "lat": -33.8688, "lon": 151.2093},
]

@st.cache_data(ttl=300)
def get_weather(api_key):
    data = []
    for city in CITIES:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"lat": city["lat"], "lon": city["lon"], "appid": api_key, "units": "metric"}
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 200:
                d = r.json()
                data.append({
                    "city": city["name"],
                    "temp": d["main"]["temp"],
                    "humidity": d["main"]["humidity"],
                    "lat": city["lat"],
                    "lon": city["lon"]
                })
        except:
            pass
    return data

def render_weather_heatmap(apikey):
    st.header("Погода в мире")

    if not apikey:
        st.info("Введите API ключ для отображения текущей температуры")
        return
    else:
        with st.spinner("Загрузка..."):
            data = get_weather(apikey)

        if not data:
            st.error("Ошибка загрузки")
            return

    df = pd.DataFrame(data)

    value = st.selectbox(
        "Показать",
        ["temp", "humidity"],
        format_func=lambda x: "Температура" if x == "temp" else "Влажность"
    )

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        text=df["city"] + "<br>" + df[value].astype(str),
        mode="markers",
        marker=dict(size=15, color=df[value], colorscale="RdYlGn_r", colorbar=dict(title=value), showscale=True)
    ))
    fig.update_layout(geo=dict(projection_type="natural earth"), height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df[["city", "temp", "humidity"]].rename(columns={
            "city": "Город",
            "temp": "Температура",
            "humidity": "Влажность"}
        ))