import requests
import aiohttp
import pandas as pd
import asyncio
import time
import streamlit as st

month_to_season = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}


def get_temp_sync(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['main']['temp']
    return None


async def get_temp_async(city, api_key):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['main']['temp']
            return None


def check_temperature_anomaly(current_temp, season_stats):
    current_season = month_to_season[pd.Timestamp.now().month]
    season_mean = season_stats[season_stats['season'] == current_season]['mean'].values[0]
    season_std = season_stats[season_stats['season'] == current_season]['std'].values[0]

    is_normal = (current_temp >= season_mean - 2 * season_std) and (current_temp <= season_mean + 2 * season_std)
    return is_normal, current_season