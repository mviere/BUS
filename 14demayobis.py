import time
import random
import numpy as np
import pandas as pd

def command_processing (command_queue: list) -> None:
    
    # Acá tiene que juntar comando con tiempo y variable e imprimir por pantalla. Por ahora, es solo tiempo y variable.
    for cmd in command_queue:
        print(cmd)
    
    return

def mode_management (df_mode: pd.DataFrame, deftable_filename: str, cant_T: int, dT: int) -> list:

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
    resto = cant_T*dT - len(command_queue)
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

def event_handling (event: bool, regist_filename: str) -> list:

    commmand_queue = []
    commmand_queue = ["estos", "son", "comandos", "que se", "ejecutan", "por", "occurencia", "de un", "evento wow"]

    new_row = {'Descripcion': event, 'Cualk': 0.7}
    df_evento = pd.DataFrame(new_row, index=False, header=False)
    DF2CSV(df_evento, regist_filename, 'append')

    return commmand_queue

def CSV2DF (filename: str) -> pd.DataFrame:

    """
    Requiere: 
    - `import pandas as pd`

    @brief

    @param filename (str):                 Nombre del archivo 

    @return df pandas.DataFrame):          DataFrame de los datos
    """
    
    df = pd.read_csv(filename, header=[0])
    return df

def DF2CSV (df: pd.DataFrame, filename: str, estilo: str):

    """
    Requiere: 
    - `import pandas as pd`

    @brief

    @param filename (str):                 Nombre del archivo 
    @param df (pandas.DataFrame):          DataFrame de los datos
    @param estilo (str):                   'append' para agregar fila, 'write' para crear tabla

    @return None          
    """
    if estilo == 'append':
        df.to_csv(filename, mode='a', index=False, header=False)
    if estilo == 'write':
        df.to_csv(filename, mode='w', index=False)
    return

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
    dT = 10
    dt = 1

    # Defino rutas y creo archivo de registro de eventos
    deftable_filename = "deftable_modos.csv"
    regist_filename = "event_register.csv"
    df_evento1 = pd.DataFrame(columns=['Descripcion', 'Cualk'])
    DF2CSV(df_evento1, regist_filename, 'write')

    GoProgram = True
    while GoProgram:
        
        # Itero el archivo escenario.
        for index, cols in df_escenario.iterrows(): # While de nico
            
            # Defino el DataFrame modo. En él está la información del modo y la cantidad de ciclos que permanece en ese modo.
            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]
            
            # Defino la secuencia de comandos a ejecutar para transicionar al modo y quedarme allí la cantidad de ciclos que disponga el archivo "escenario.csv"
            command_queue = mode_management(df_mode, deftable_filename, ciclos, dT)

            # Si ocurrió un evento, obtengo la secuencia de comandos para manejarlo.
            event = bool(random.getrandbits(1))
            if event:
                event = random.choice(["Perdida de SMA por drag", "Perturbaciones por gravedad"])
                command_queue = event_handling(event, regist_filename)

            # Ejecuto secuencia de comandos
            command_processing(command_queue)

        GoProgram = False 
    return
                

if __name__ == "__main__":
    main()
