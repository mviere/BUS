import numpy as np
import matplotlib.pyplot as plt

# Definition Table
command_definition_table = {
    'command1': [],
    'command2': [],
    'command3': [],
    }

# Cola de Comandos
pending_commands = []

# Funcion para iniciar el procesamiento de comandos
def initialize_command_processing():
    print("Iniciando Procesamiento de Comandos...")

# Funcion para buscar el comando en el definition table
def find_command(command):
    if command in command_definition_table:
        return True
    else:
        return False
    
# Funcion para agregar el comando a la cola de comandos
def add_command(command): 
    pending_commands.append((command))
    print(f"Comando '{command}' agregado a la cola")

# Funcion para ejecutar los comandos pendientes en orden          
def execute_commands():
    for command in pending_commands:
        print(f"Ejecutando comando '{command}'")          
    
def process_commands():
    initialize_command_processing()
    while True:
        print("1. Agregar Comando a la Cola")
        print("2. Ejecutar Comandos")
        op = int(input("Seleccione una Opción: "))
        
        if op == 1:
            command = input("Ingrese un Comando: ")
            found = find_command(command)
            if found:
                add_command(command)
            else:
                print("Comando no encontrado en la tabla de definición")
        
        if op == 2:
            execute_commands()
            print("Todos los Comandos fueron ejecutados con éxito")
            break
        
              