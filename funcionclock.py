# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:53:11 2023

@author: Milena
"""

import time


def clock(running, t, T):  
    'Mientras runnning sea True va a devolver T = 10t y t'
    
    while running:
        #print("t:", t,"T:", T)
        t += 1
        if t % 10 == 0:
            T += 1
        time.sleep(1)
        
    return T, t

'Prueba de que la funcion devuelve T y t cada un segundo'

import time
import threading

def clock(stop_event, counters):
    t, T = counters
    while not stop_event.is_set():
        print("T:", T)
        print("t:", t)
        t += 1
        if t % 10 == 0:
            T += 1
        time.sleep(1)
    counters[0], counters[1] = t, T

# Crear un objeto de bloqueo
stop_event = threading.Event()

# Variables para contar los segundos
counters = [0, 0]

# Llamada a la función clock() en un hilo separado
clock_thread = threading.Thread(target=clock, args=(stop_event, counters))
clock_thread.start()

# Ejemplo de ejecución del programa principal
time.sleep(5)  # Espera 5 segundos

# Detener la ejecución del reloj
stop_event.set()
clock_thread.join()  # Esperar a que el hilo del reloj termine

# Obtener los valores finales de T y t
t, T = counters

# Imprimir los valores finales de T y t
print("Valor final de T:", T)
print("Valor final de t:", t)


