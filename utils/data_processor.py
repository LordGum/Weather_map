import pandas as pd
import numpy as np

def load_and_prepare_data(df, city):
    city_df = df[df['city'] == city].copy()
    city_df = city_df.sort_values('timestamp')
    return city_df

def calculate_rolling_stats(df, window=30):
    df['rolling_mean'] = df['temperature'].rolling(window=window, center=True).mean()
    df['rolling_std'] = df['temperature'].rolling(window=window, center=True).std()
    df['upper_bound'] = df['rolling_mean'] + 2 * df['rolling_std']
    df['lower_bound'] = df['rolling_mean'] - 2 * df['rolling_std']
    df['anomaly'] = (df['temperature'] > df['upper_bound']) | (df['temperature'] < df['lower_bound'])
    return df

def get_season_stats(df):
    return df.groupby('season')['temperature'].agg(['mean', 'std']).reset_index()

def analyze_city(city_name, full_df):
    city_data = full_df[full_df['city'] == city_name].copy()
    city_data = city_data.sort_values('timestamp')
    city_data['rolling_mean'] = city_data['temperature'].rolling(window=30, center=True).mean()
    city_data['rolling_std'] = city_data['temperature'].rolling(window=30, center=True).std()
    city_data['anomaly'] = (city_data['temperature'] > city_data['rolling_mean'] + 2 * city_data['rolling_std']) | \
                           (city_data['temperature'] < city_data['rolling_mean'] - 2 * city_data['rolling_std'])
    return city_data