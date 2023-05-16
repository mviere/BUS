#%%

# Definition Table (en base a los txt)
mode_A = []
with open("mode_A.txt") as fname:
    lineas = fname.readlines()
    for linea in lineas:
        mode_A.append(linea.strip('\n'))
        
mode_B = []
with open("mode_B.txt") as fname:
    lineas = fname.readlines()
    for linea in lineas:
        mode_B.append(linea.strip('\n'))
        
mode_C = []
with open("mode_C.txt") as fname:
    lineas = fname.readlines()
    for linea in lineas:
        mode_C.append(linea.strip('\n'))

#%%

# Modo actual
current_mode = "mode_A"

# Fila de Comandos
command_queue = []

# Fila de Modos
mode_queue = []

#%%

# Funcion para mostrar en pantalla la tabla de definicion
def information():
    
    print(f"mode_A = [{', '.join(mode_A)}]")
    print(f"mode_B = [{', '.join(mode_B)}]")
    print(f"mode_C = [{', '.join(mode_C)}]")

#%%

# Funcion para mostrar en pantalla el modo actual
def display_current_mode():
    
    global current_mode
    print(f"Estado Actual: '{current_mode}'")

#%%
           
# Funcion para buscar el modo en la definition table
def find_mode(mode):
    
    if mode == "mode_A" or mode == "mode_B" or mode == "mode_C":
        return True
    else:
        return False
    
#%%

# Funcion para checkear que los modos de la secuencia estan definidos en la tabla
def check_mode_sequence(mode_sequence):
    
    global mode_A, mode_B, mode_C
    
    errors = []
    for mode in mode_sequence:
        found = find_mode(mode)
        if not found:     
            errors.append(f"Error: el modo '{mode}' no está definido en la tabla de definición")
    return errors

#%%

# Funcion para agregar la secuencia de modos y mostrar la secuencia de comandos
def add_mode_sequence(): 
    
    global mode_queue, command_queue
    
    mode_queue.clear()
    command_queue.clear()
    
    mode_sequence = input("Ingrese una secuencia de modos separados por comas: ").split(",")
    errors = check_mode_sequence(mode_sequence)
    if errors:
        for error in errors:
            print(error)   
    else:
        mode_queue = mode_sequence
        for mode in mode_sequence:
            if mode == "mode_A":
                command_queue.extend(mode_A)
            elif mode == "mode_B":
                command_queue.extend(mode_B)
            elif mode == "mode_C":
                command_queue.extend(mode_C)              
        print("Secuencia añadida a la fila\n")
        print(f"Secuencia = [{', '.join(mode_queue)}]")
        print(f"Comandos = [{', '.join(command_queue)}]")
    
#%%

# Funcion para ejecutar la secuencia de comandos
def execute_mode_sequence():
      
    global current_mode, mode_queue, command_queue

    if len(mode_queue) == 0:
        print("No hay una secuencia establecida") 
    else:
        for mode in mode_queue:
            print(f"Ejecutando modo ´{mode}´")
            current_mode = mode
            for command in eval(mode):
                print(f"Ejecutando comando '{command}'")
                
    mode_queue.clear()
    command_queue.clear()
        
#%%

# Funcion principal
def process_commands(op):
        
    if op == 1:
        information()
             
    if op == 2:
        display_current_mode()
        
    if op == 3:
        add_mode_sequence()
            
    if op == 4:
        execute_mode_sequence()
        
    if op not in [1, 2, 3, 4]:
        print("Opción inválida")

#%%

# Main (ingresar por consola)
def main():
    
    while True:
        print("\n1. Mostrar Definition Table de Modos")
        print("2. Mostrar Estado Actual")
        print("3. Establecer Secuencia de Modos")
        print("4. Ejecutar Secuencia de Modos")
        print("5. Salir\n")
        op = int(input("Seleccione una Opción: "))
        print()
        
        if op != 5:
            process_commands(op)  
        else:
            break
    return
    