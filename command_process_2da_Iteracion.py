#%%

# Definition Table
command_definition_table = {
    'mode_A': ["command_1", "command_2", "command_3"],
    'mode_B': ["command_4", "command_5", "command_6"],
    'mode_C': ["command_7", "command_8", "command_9"]
    }

# Modo actual
current_mode = "mode_A"

# Cola de Comandos
pending_commands = []

#%%

# Funcion para cambiar de modo
def change_mode(new_mode):
    
    global current_mode
    
    for command in command_definition_table[new_mode]:
        pending_commands.append(command)
    print(f"Cambiando al modo ´{new_mode}´")
    current_mode = new_mode

#%%
          
# Funcion para ejecutar comandos
def execute_commands():
    
    global pending_commands
    
    for command in pending_commands:
        print(f"Ejecutando comando '{command}'")
    pending_commands.clear()

#%%
           
# Funcion para buscar el comando en la definition table
def find_command(command):
    for commands in command_definition_table.values():
        if command in commands:
            return True
    return False

#%%

# Funcion para agregar un comando a la cola de comandos
def add_command(command): 
    
    global pending_commands
    
    pending_commands.append(command)
    print(f"Comando '{command}' agregado a la cola")
        
#%%

# Main (ingresar por consola)
def process_commands():
    
    global current_mode
    global pending_commands
    
    pending_commands.clear()
    
    while True:
        print("\n1. Estado Actual")
        print("2. Cambiar Modo")
        print("3. Agregar Comando a la Cola")
        print("4. Ejecutar Comandos")
        print("5. Salir\n")
        op = int(input("Seleccione una Opción: "))
        print()
        
        if op == 1:
            print(f"Estado Actual: '{current_mode}'")
        
        if op == 2:
            new_mode = input("Ingrese un Nuevo Modo: ")
            print()
            if new_mode == current_mode:
                print(f"El Modo ya está establecido en ´{current_mode}´")       
            elif new_mode not in command_definition_table:
                print(f"Error: el modo ´{new_mode}´ no está definido en la tabla de definición")
            else:
                change_mode(new_mode)
                execute_commands()
                print("Cambio de Modo exitoso")
            
        if op == 3:
            command = input("Ingrese un Comando: ")
            print()
            found = find_command(command)
            if found:
                add_command(command)
            else:
                print("Comando no encontrado en la tabla de definición")
        
        if op == 4:
            if len(pending_commands) == 0:
                print("No hay Comandos en la cola")
            else:
                execute_commands()
                print("Todos los Comandos fueron ejecutados con éxito")
            
        if op == 5:
            break
        
        if op not in [1, 2, 3, 4, 5]:
            print("Opción inválida")
        

              