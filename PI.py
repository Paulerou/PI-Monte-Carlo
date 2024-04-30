import random
import math
from multiprocessing import Pool
import threading
import time
from tkinter import Tk, Button, Label, Entry, StringVar

# Função para calcular o número de pontos dentro de um círculo usando o método de Monte Carlo.
# Gera n pontos aleatórios dentro de um quadrado de lado 2 e conta quantos desses pontos estão dentro de um círculo de raio 1.
# O valor de Pi pode ser aproximado pela razão entre os pontos dentro do círculo e o total de pontos gerados.
def monte_carlo_circle(n):
    inside = 0 # Inicializa o contador de pontos dentro do círculo
    for _ in range(n):
        x = random.random() # Gera um número aleatório para a coordenada x
        y = random.random() # Gera um número aleatório para a coordenada y
        if math.sqrt(x**2 + y**2) <= 1: # Verifica se o ponto está dentro do círculo
            inside += 1 # Incrementa o contador se o ponto estiver dentro do círculo
    return inside       

def calculate_pi_multiprocessing(n_points, n_processes):
    with Pool(n_processes) as p:
        results = p.map(monte_carlo_circle, [n_points // n_processes] * n_processes)
    return sum(results) / n_points

# Função para calcular o valor de Pi usando multiprocessamento.
# Divide o trabalho entre vários processos para calcular o número de pontos dentro de um círculo em paralelo.
# A soma dos resultados de cada processo é então usada para calcular o valor aproximado de Pi.
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

# Função para calcular o valor de Pi usando threading.
# Cria várias threads para calcular o número de pontos dentro de um círculo em paralelo.
# Usa uma lista compartilhada para contar os pontos dentro do círculo, permitindo que as threads atualizem o contador simultaneamente.

from concurrent.futures import ThreadPoolExecutor

def calculate_pi_concurrent_futures(n_points, n_threads):
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        results = list(executor.map(monte_carlo_circle, [n_points // n_threads] * n_threads))
    return sum(results) / n_points

from threading import Semaphore

# Função para calcular o valor de Pi usando ThreadPoolExecutor.
# Utiliza um executor de threads para gerenciar a execução de várias tarefas em paralelo.
# Cada tarefa é uma chamada à função monte_carlo_circle, que é mapeada para cada thread.
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
    n_points = int(entry_points.get()) # Obtém o número de pontos do campo de entrada
    n_processes = int(entry_processes.get()) # Obtém o número de processos do campo de entrada
    start = time.time() # Registra o tempo de início
    pi_multiprocessing = calculate_pi_multiprocessing(n_points, n_processes) # Calcula Pi usando multiprocessamento
    label_result.config(text=f"Pi (multiprocessing): {pi_multiprocessing}, Time: {time.time() - start}") # Atualiza o rótulo com o resultado e o tempo de cálculo
    root.update_idletasks() # Força a atualização da interface gráfica

# Funções semelhantes para threading, ThreadPoolExecutor e threading com semáforo
# Funções para a interface gráfica
def start_multiprocessing():
    n_points = int(entry_points.get())
    n_processes = int(entry_processes.get())
    start = time.time()
    pi_multiprocessing = calculate_pi_multiprocessing(n_points, n_processes) # Calcula Pi usando multiprocessamento
    label_result.config(text=f"Pi (multiprocessing): {pi_multiprocessing}, Time: {time.time() - start}")
    root.update_idletasks() # Força a atualização da interface gráfica

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
root = Tk() # Cria a janela principal
root.title("Monte Carlo Pi Calculator") # Define o título da janela

label_points = Label(root, text="Number of Points:") # Cria um rótulo para o número de pontos
label_points.pack() # Adiciona o rótulo à janela
entry_points = Entry(root) # Cria um campo de entrada para o número de pontos
entry_points.pack() # Adiciona o campo de entrada à janela

label_processes = Label(root, text="Number of Processes:") # Cria um rótulo para o número de processos
label_processes.pack() # Adiciona o rótulo à janela
entry_processes = Entry(root) # Cria um campo de entrada para o número de processos
entry_processes.pack() # Adiciona o campo de entrada à janela

label_threads = Label(root, text="Number of Threads:") # Cria um rótulo para o número de threads
label_threads.pack() # Adiciona o rótulo à janela
entry_threads = Entry(root) # Cria um campo de entrada para o número de threads
entry_threads.pack() # Adiciona o campo de entrada à janela

button_multiprocessing = Button(root, text="Calculate Pi (Multiprocessing)", command=start_multiprocessing) # Cria um botão para calcular Pi usando multiprocessamento
button_multiprocessing.pack() # Adiciona o botão à janela
button_threading = Button(root, text="Calculate Pi (Threading)", command=start_threading) # Cria um botão para calcular Pi usando threading
button_threading.pack() # Adiciona o botão à janela

button_concurrent_futures = Button(root, text="Calculate Pi (Concurrent Futures)", command=start_concurrent_futures) # Cria um botão para calcular Pi usando ThreadPoolExecutor
button_concurrent_futures.pack() # Adiciona o botão à janela

button_threading_with_semaphore = Button(root, text="Calculate Pi (Threading with Semaphore)", command=start_threading_with_semaphore) # Cria um botão para calcular Pi usando threading com semáforo
button_threading_with_semaphore.pack() # Adiciona o botão à janela

label_result = Label(root, text="")
label_result.pack()

root.mainloop()
