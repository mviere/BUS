import numpy as np
import pandas as pd
import threading
import time
import random
import Aplicacion as app
import FuncAux as fa


# %% Algoritmo C2A
# ---------------------------------------------------------------------------- #

def mode_processing(deftable_modos: str, deftable_housekeeping: str, mode_name: str):
    
    commmand_queue = []
    duracion = []

    df_deftable = fa.CSV2DF(deftable_modos)
    df_deftable3 = fa.CSV2DF(deftable_housekeeping)

    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == mode_name), :]
    df_blockcmd3 = df_deftable3.loc[(df_deftable3["Modo"] == mode_name), :]

    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)
    for t in df_blockcmd['Duracion'].values.tolist():
        duracion.append(t)
    
    # Creación del DataFrame con los valores nominales de las variables de housekeeping   
    index = pd.Index(df_blockcmd3["Sensor"].values, name="Sensor")
    df_nominalvalues = pd.DataFrame({'Temperatura min. [C]': df_blockcmd3["Temperatura min [C]"].values, 'Temperatura max. [C]': df_blockcmd3["Temperatura max [C]"].values}, index=index)

    return commmand_queue, duracion, df_nominalvalues


def mode_transition(deftable_filename: str, dT: int):

    command_queue_trans = []

    df_deftable = fa.CSV2DF(deftable_filename)
    
    for cmd in df_deftable.values.tolist():
        for c in cmd:
            if len(command_queue_trans) < dT:
                command_queue_trans.append(c)
            else:
                break

    return command_queue_trans


def mode_management (mode_name: str, previous_mode: str, dT: int, deftable_modos: str, deftable_transicion: str, deftable_housekeeping: str) -> list:
    """
    Esta función
    """
    command_queue = []

    if mode_name != previous_mode:

        command_queue_trans = mode_transition(deftable_transicion, dT)
        command_queue.extend(command_queue_trans)
   
    command_queue2, lista_duracion, df_nominalvalues = mode_processing(deftable_modos, deftable_housekeeping, mode_name)
    
    for i in range(len(command_queue2)):
        for j in range(lista_duracion[i]):
            command_queue.append(command_queue2[i])

    while len(command_queue) % dT != 0:
        command_queue.append(None)

    return command_queue, df_nominalvalues, mode_name


def command_processing (df_nominalvalues: pd.DataFrame, command_queue: list, time_queue: list, T: int) -> None:
    
    # Ejecuto la realización del housekeeping
    SafeMode = application_management('housekeeping', df_nominalvalues)
    
    # Ejecuto la activación del Safe Mode de ser necesario
    if SafeMode:
        print('Activar Safe Mode')

    i = 0
    for cmd in command_queue:
        print(f"Ciclo: {T}, t: {time_queue[i]}, Comando: {cmd}")
        time.sleep(1)
        i+=1
    return


def event_handling(event: str, event_register: str, deftable_eventos: str, dT: int, t: int, T: int) -> list:
    command_queue_event = []

    df_deftable = fa.CSV2DF(deftable_eventos)
    df_blockcmd = df_deftable.loc[df_deftable["Evento"] == event]

    command_queue_event = df_blockcmd['Comandos'].values.tolist()

    new_row = pd.DataFrame({'Descripcion': [df_blockcmd["Evento"].values[0]], 'Ciclo': [T], 'Tiempo': [t]})
    df_evento = pd.DataFrame(new_row)
    fa.DF2CSV(df_evento, event_register, 'append')

    while len(command_queue_event) < dT:
        command_queue_event.append(None)

    return command_queue_event


def application_management (option: str, df_nominalvalues: pd.DataFrame):
    """
    Esta función interactúa con Aplicación a través de comandos.
    Realiza diversas interacciones, entre ellas:

        - Housekeeping
          Para esta opción debe ingresar el DataFrame con los valores nominales
          de las variables representativas del housekeeping.

        - Despliegue 
    """
    if option == 'housekeeping':
        
        # Ordeno tareas de housekeeping y obtengo el reporte
        df_housekeeping = app.housekeeping(df_nominalvalues)
        
        # Ordeno cambiar a Safe Mode si el reporte lo indica
        SafeMode = False
        for state in df_housekeeping['Estado'].values:
            if state == 'Out of range':
                SafeMode = True
                break
        
        return SafeMode
    
    else:
        return