import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import streamlit as st


def compare_performance(all_cities, full_df, analyze_func):
    start_time = time.time()
    sequential_results = [analyze_func(city, full_df) for city in all_cities]
    sequential_time = time.time() - start_time

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        parallel_results = list(executor.map(lambda city: analyze_func(city, full_df), all_cities))
    parallel_time = time.time() - start_time

    return sequential_time, parallel_time