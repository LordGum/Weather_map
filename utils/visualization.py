import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


def create_time_series_plot(city_df, city_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=city_df['timestamp'],
        y=city_df['temperature'],
        mode='lines',
        name='Температура',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=city_df['timestamp'],
        y=city_df['rolling_mean'],
        mode='lines',
        name='Скользящее среднее (30 дней)',
        line=dict(color='red')
    ))

    anomalies = city_df[city_df['anomaly']]
    fig.add_trace(go.Scatter(
        x=anomalies['timestamp'],
        y=anomalies['temperature'],
        mode='markers',
        name='Аномалии',
        marker=dict(color='orange', size=8)
    ))

    fig.update_layout(
        title=f'Временной ряд температуры в {city_name}',
        xaxis_title='Дата',
        yaxis_title='Температура (°C)'
    )
    return fig


def create_seasonal_boxplot(city_df, city_name):
    fig = go.Figure()
    for season in city_df['season'].unique():
        season_data = city_df[city_df['season'] == season]
        fig.add_trace(go.Box(y=season_data['temperature'], name=season.capitalize()))

    fig.update_layout(
        title=f'Распределение температур по сезонам в {city_name}',
        yaxis_title='Температура (°C)'
    )
    return fig