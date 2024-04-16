import random
import math
from multiprocessing import Pool
import threading

def monte_carlo_circle(n):
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if math.sqrt(x**2 + y**2) <= 1:
            inside += 1
    return inside

def calculate_pi_multiprocessing(n_points, n_processes):
    with Pool(n_processes) as p:
        results = p.map(monte_carlo_circle, [n_points // n_processes] * n_processes)
    return sum(results) / n_points

def calculate_pi_threading(n_points, n_threads):
    inside = [0]
    def worker():
        for _ in range(n_points // n_threads):
            x = random.random()
            y = random.random()
            if math.sqrt(x**2 + y**2) <= 1:
                inside[0] += 1
    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return inside[0] / n_points


from concurrent.futures import ThreadPoolExecutor

def calculate_pi_concurrent_futures(n_points, n_threads):
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        results = list(executor.map(monte_carlo_circle, [n_points // n_threads] * n_threads))
    return sum(results) / n_points

from threading import Semaphore

def calculate_pi_threading_with_semaphore(n_points, n_threads):
    sem = Semaphore()
    inside = [0]
    def worker():
        for _ in range(n_points // n_threads):
            x = random.random()
            y = random.random()
            if math.sqrt(x**2 + y**2) <= 1:
                with sem:
                    inside[0] += 1
    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return inside[0] / n_points


import time

if __name__ == '__main__':
    n_points = 1000000
    n_processes = 4
    n_threads = 4

    start = time.time()
    pi_multiprocessing = calculate_pi_multiprocessing(n_points, n_processes)
    print(f"Pi (multiprocessing): {pi_multiprocessing}, Time: {time.time() - start}")

    start = time.time()
    pi_threading = calculate_pi_threading(n_points, n_threads)
    print(f"Pi (threading): {pi_threading}, Time: {time.time() - start}")

    start = time.time()
    pi_concurrent_futures = calculate_pi_concurrent_futures(n_points, n_threads)
    print(f"Pi (concurrent.futures): {pi_concurrent_futures}, Time: {time.time() - start}")

    start = time.time()
    pi_threading_with_semaphore = calculate_pi_threading_with_semaphore(n_points, n_threads)
    print(f"Pi (threading with semaphore): {pi_threading_with_semaphore}, Time: {time.time() - start}")
