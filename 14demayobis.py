import time
import random
import numpy as np
import pandas as pd

def command_processing (command_queue: list) -> None:
    
    # Acá tiene que juntar comando con tiempo y variable e imprimir por pantalla. Por ahora, es solo tiempo y variable.
    for cmd in command_queue:
        print(cmd)
    
    return

def mode_management (df_mode: pd.DataFrame, deftable_filename: str, cant_T: int, T: int) -> list:

    # Leo definition table de modos
    df_deftable = CSV2DF(deftable_filename)

    # Creo la futura fila de comandos
    command_queue = []

    # Busco los comandos de transición y los coloco primeros en la fila
    command_queue_trans = mode_transition("deftable_transicion.csv")
    for cmd in command_queue_trans:
        command_queue.append(cmd)
    
    # Obtengo secuencia de comandos del modo
    modo = df_mode["Modo"].values[0]
    commmand_queue2 = mode_processing(deftable_filename, modo)
    
    # Agrego los comandos del modo hasta completar el tiempo T
    resto = cant_T*T - len(command_queue)
    i = 0
    for k in range(resto):
        for cmd in commmand_queue2:
            if i < resto:
                command_queue.append(cmd)
                i += 1

    return command_queue

def mode_transition(deftable_filename: str):

    commmand_queue_trans = []
    df_deftable = CSV2DF(deftable_filename)

    for cmd in df_deftable.values.tolist():
        for c in cmd:
            commmand_queue_trans.append(c)

    return commmand_queue_trans

def mode_processing(deftable_filename: str, modo: str):

    commmand_queue = []

    df_deftable = CSV2DF(deftable_filename)
    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == modo), :]

    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)
        
    return commmand_queue

def CSV2DF (filename: str) -> pd.DataFrame:

    """
    Requiere: 
    - `import pandas as pd`

    @brief

    @param filename (str):                 Nombre del archivo 

    @return df   (pandas.DataFrame):       DataFrame de los datos
    """
    
    df = pd.read_csv(filename, header=[0])
    return df

# %% Función Main

def main() -> None:

    """
    Requiere:
    - `import pandas as pd`
    @brief
    @param None
    @return None
    """
    print("\nImportando librerías y scripts necesarios...\n")
    
    # Leo archivo escenario
    escenario_filename = "escenario.csv"
    df_escenario = CSV2DF(escenario_filename)

    # Defino granularidades temporales [segundos]
    T = 10
    t = 1

    endProgram = False
    while endProgram == False:
        
        # Itero el archivo escenario. Cada fila es un Tiempo que tiene asociado un Modo.
        for index, cols in df_escenario.iterrows():
            
            # Defino el DataFrame modo y premodo. En cada uno de ellos, está la información del modo y la cantidad de ciclos que permanece en ese modo.
            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]
            
            # Llamo a la función de gestión de modo
            deftable_filename = "deftable_modos.csv"
            command_queue = mode_management(df_mode, deftable_filename, ciclos, T)
            
            #tiempo = time_management(T,t)

            # Ejecuto secuencia de comandos
            command_processing(command_queue)   #command_processing(command_queue, algo del tiempo)

        endProgram = True 
    return
                

if __name__ == "__main__":
    main()

'''
t = 0
comando = ""

'Funcion contador'
def():
    ....
return contando, T, t, 

'Funcion ejecucion de escenario'
while ('parametro booleano de la funcion contador de tiempo'):
    t += 1 'potestad de funcion contador'
    if t % 1 == 0:
        comando = random.choice(["comando1", "comando2", "comando3"])
    print("t:", t, "comando:", comando)
    time.sleep(1)

def gestión del tiempo():
    contador
    return contando, T, t
'''