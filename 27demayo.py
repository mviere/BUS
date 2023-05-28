import time
import random
import numpy as np
import pandas as pd






def command_processing (command_queue: list, dT: int) -> None:
    
    # Acá tiene que juntar comando con tiempo y variable e imprimir por pantalla. Por ahora, es solo tiempo y variable.
    t = 0
    ciclo = 0
    
    for cmd in command_queue:
        print(f"Ciclo: {ciclo}, t: {t}, Comando: {cmd}")
        time.sleep(1)
        t += 1
        
        if t%dT == 0:
            ciclo += 1
    
    return

def mode_management (df_mode: pd.DataFrame, deftable_filename: str, cant_T: int, dT: int) -> list:


    # Creo la futura fila de comandos
    command_queue = []

    # Busco los comandos de transición y los coloco primeros en la fila
    command_queue_trans = mode_transition("deftable_transicion.csv", dT)
   
    #Agrego el ciclo de transicion a la fila de comandos
    command_queue.extend(command_queue_trans)
   
    # Obtengo secuencia de comandos del modo
    modo = df_mode["Modo"].values[0]
    command_queue2, lista_duracion = mode_processing(deftable_filename, modo)
    
    for ciclo in range(cant_T):
        for i in range(len(command_queue2)):
            for j in range(lista_duracion[i]):
                command_queue.append(command_queue2[i])
        while len(command_queue) % dT != 0:
            command_queue.append(None)


    return command_queue

def mode_transition(deftable_filename: str, dT: int):
    command_queue_trans = []
    df_deftable = CSV2DF(deftable_filename)

    for cmd in df_deftable.values.tolist():
        for c in cmd:
            if len(command_queue_trans) < dT:
                command_queue_trans.append(c)
            else:
                break

    while len(command_queue_trans) < dT:
        command_queue_trans.append(None)

    return command_queue_trans

def mode_processing(deftable_filename: str, modo: str):

    commmand_queue = []
    duracion = []

    df_deftable = CSV2DF(deftable_filename)
    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == modo), :]

    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)
    for t in df_blockcmd['Duracion'].values.tolist():
        duracion.append(t)
        
    return commmand_queue, duracion

def event_handling (event: str, regist_filename: str, deftable_eventos: str) -> list:

    # Segun el evento que ocurrió, obtengo la lista de comandos a ejecutar
    commmand_queue = []
    df_deftable = CSV2DF(deftable_eventos)
    df_blockcmd = df_deftable.loc[(df_deftable["Evento"] == event), :]
    commmand_queue = df_blockcmd['Comandos'].values

    # Registro el evento que ocurrió con el tiempo
    '''new_row = {'Descripcion': event, 'Cualk': 0.7}
    df_evento = pd.DataFrame(new_row, index=False, header=False)
    DF2CSV(df_evento, regist_filename, 'append')'''

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
    dT = 5
    dt = 1

    # Defino rutas y creo archivo de registro de eventos
    deftable_filename = "deftable_modos.csv"
    #regist_filename = "event_register.csv"
    #df_evento1 = pd.DataFrame(columns=['Descripcion', 'Cualk'])
    #DF2CSV(df_evento1, regist_filename, 'write')

    GoProgram = True
    while GoProgram:
        
        # Itero el archivo escenario.
        for index, cols in df_escenario.iterrows(): # While de nico
            
            # Defino el DataFrame modo. En él está la información del modo y la cantidad de ciclos que permanece en ese modo.
            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]
            
            # Defino la secuencia de comandos a ejecutar para transicionar al modo y quedarme allí la cantidad de ciclos que disponga el archivo "escenario.csv"
            command_queue = mode_management(df_mode, deftable_filename, ciclos, dT)
            
            '''
            # Si ocurrió un evento, obtengo la secuencia de comandos para manejarlo.
            event = bool(random.getrandbits(1))
            if event:
                event = random.choice(["Perdida de SMA por drag", "Perturbaciones por gravedad"])
                deftable_eventos = "deftable_eventos.csv"
                command_queue = event_handling(event, regist_filename, deftable_eventos)'''

            # Ejecuto secuencia de comandos
            command_processing(command_queue,dT)

        GoProgram = False 
    return
                

if __name__ == "__main__":
    main()