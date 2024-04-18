import random
import math
from multiprocessing import Pool
import threading
import time
from tkinter import Tk, Button, Label, Entry, StringVar

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

# Funções para a interface gráfica
def start_multiprocessing():
    n_points = int(entry_points.get())
    n_processes = int(entry_processes.get())
    start = time.time()
    pi_multiprocessing = calculate_pi_multiprocessing(n_points, n_processes)
    label_result.config(text=f"Pi (multiprocessing): {pi_multiprocessing}, Time: {time.time() - start}")

def start_threading():
    n_points = int(entry_points.get())
    n_threads = int(entry_threads.get())
    start = time.time()
    pi_threading = calculate_pi_threading(n_points, n_threads)
    label_result.config(text=f"Pi (threading): {pi_threading}, Time: {time.time() - start}")

def start_concurrent_futures():
    n_points = int(entry_points.get())
    n_threads = int(entry_threads.get())
    start = time.time()
    pi_concurrent_futures = calculate_pi_concurrent_futures(n_points, n_threads)
    label_result.config(text=f"Pi (concurrent.futures): {pi_concurrent_futures}, Time: {time.time() - start}")

def start_threading_with_semaphore():
    n_points = int(entry_points.get())
    n_threads = int(entry_threads.get())
    start = time.time()
    pi_threading_with_semaphore = calculate_pi_threading_with_semaphore(n_points, n_threads)
    label_result.config(text=f"Pi (threading with semaphore): {pi_threading_with_semaphore}, Time: {time.time() - start}")

# Criação da interface gráfica
root = Tk()
root.title("Monte Carlo Pi Calculator")

label_points = Label(root, text="Number of Points:")
label_points.pack()
entry_points = Entry(root)
entry_points.pack()

label_processes = Label(root, text="Number of Processes:")
label_processes.pack()
entry_processes = Entry(root)
entry_processes.pack()

label_threads = Label(root, text="Number of Threads:")
label_threads.pack()
entry_threads = Entry(root)
entry_threads.pack()

button_multiprocessing = Button(root, text="Calculate Pi (Multiprocessing)", command=start_multiprocessing)
button_multiprocessing.pack()

button_threading = Button(root, text="Calculate Pi (Threading)", command=start_threading)
button_threading.pack()

button_concurrent_futures = Button(root, text="Calculate Pi (Concurrent Futures)", command=start_concurrent_futures)
button_concurrent_futures.pack()

button_threading_with_semaphore = Button(root, text="Calculate Pi (Threading with Semaphore)", command=start_threading_with_semaphore)
button_threading_with_semaphore.pack()

label_result = Label(root, text="")
label_result.pack()

root.mainloop()
