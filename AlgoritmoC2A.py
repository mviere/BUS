import numpy as np
import pandas as pd
import threading
import time
import random
import Aplicacion as app


# %% Algoritmo C2A
# ---------------------------------------------------------------------------- #

class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._current_time = -1
        self._current_cycle = 0
        self._is_running = False
        self._lock = threading.Lock()

    def run(self):
        self._is_running = True
        while self._is_running:
            with self._lock:
                self._current_time += 1
                if self._current_time % 5 == 0:
                    self._current_cycle += 1
            time.sleep(1)

    def stop(self):
        self._is_running = False

    def get_current_time(self):
        with self._lock:
            return self._current_time

    def get_current_cycle(self):
        with self._lock:
            return self._current_cycle

    def increment_time(self):
        with self._lock:
            self._current_time += 1
            if self._current_time % 5 == 0:
                self._current_cycle += 1


def CSV2DF(filename: str) -> pd.DataFrame:

    # Leo el archivo CSV y lo almaceno en un DataFrame
    df = pd.read_csv(filename, header=[0])
    return df


def DF2CSV (df: pd.DataFrame, filename: str, estilo: str):

    if estilo == 'append':
        df.to_csv(filename, mode='a', index=False, header=False)
    if estilo == 'write':
        df.to_csv(filename, mode='w', index=False)

    return


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


def mode_processing(deftable_filename: str, deftable_filename3: str, modo: str):
    
    commmand_queue = []
    duracion = []

    df_deftable = CSV2DF(deftable_filename)
    df_deftable3 = CSV2DF(deftable_filename3)

    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == modo), :]
    df_blockcmd3 = df_deftable3.loc[(df_deftable["Modo"] == modo), :]

    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)
    for t in df_blockcmd['Duracion'].values.tolist():
        duracion.append(t)
    
    ### TENGO PROBLEMAS ACÁ, NO PUEDO CREAR EL FUKIN DATAFRAME

    # PASO 1: Creo DataFrame con los valores nominales de las variables de housekeeping
    sensor_list = df_blockcmd3["Sensor"].values.tolist()
    temp_min_list = df_blockcmd3["Temperatura min [C]"].values.tolist()
    temp_max_list = df_blockcmd3["Temperatura max [C]"].values.tolist()
    
    index = pd.Index(sensor_list, name="Sensor")
    df_nominalvalues = pd.DataFrame({'Temperatura min. [C]': temp_min_list, 'Temperatura max. [C]': temp_max_list}, index=index)

    return commmand_queue, duracion, df_nominalvalues


def mode_management (df_mode: pd.DataFrame, deftable_filename: str, deftable_filename2: str, deftable_filename3: str, cant_T: int, dT: int) -> list:

    command_queue = []

    command_queue_trans = mode_transition(deftable_filename2, dT)
    command_queue.extend(command_queue_trans)
   
    modo = df_mode["Modo"].values[0]
    command_queue2, lista_duracion, df_nominalvalues = mode_processing(deftable_filename, deftable_filename3, modo)
    
    for ciclo in range(cant_T):
        for i in range(len(command_queue2)):
            for j in range(lista_duracion[i]):
                command_queue.append(command_queue2[i])
        while len(command_queue) % dT != 0:
            command_queue.append(None)

    return command_queue, df_nominalvalues


def command_processing (df_nominalvalues: pd.DataFrame, command_queue: list, timer) -> None:
    
    # PASO 3: le paso los valores nominales a application_management para ver en qué estado está el housekeeping
    df_housekeeping = application_management(housekeeping = df_nominalvalues)

    # PASO 7: imprimo el estado de housekeeping
    print("\nHouse Keeping State:\n", df_housekeeping)

    for cmd in command_queue:
        t = timer.get_current_time()
        T = timer.get_current_cycle()
        print(f"Ciclo: {T}, t: {t}, Comando: {cmd}")
        time.sleep(1)
    
    return


def event_handling(event: str, regist_filename: str, deftable_eventos: str, dT: int, timer) -> list:
    command_queue_event = []

    df_deftable = CSV2DF(deftable_eventos)
    df_blockcmd = df_deftable.loc[df_deftable["Evento"] == event]

    command_queue_event = df_blockcmd['Comandos'].values.tolist()

    t = timer.get_current_time()
    new_row = pd.DataFrame({'Descripcion': [df_blockcmd["Evento"].values[0]], 'Cualk': [t]})
    df_evento = pd.DataFrame(new_row)

    DF2CSV(df_evento, regist_filename, 'append')

    while len(command_queue_event) < dT:
        command_queue_event.append(None)

    return command_queue_event


def application_management (**kwargs):
    """
    Esta función ahora mismo solo reporta el estado de un sensor de temperatura, pero se debería ingresar con una opción y sus inputs
    para que realice más tareas que el housekeeping. Por ejemplo, si fuera a activar actuadores lo haría desde aquí.
    """
    if kwargs.get('housekeeping') != None:

        df_nominalvalues = kwargs.get('housekeeping')

        # PASO 4: obtengo los estados de las variables representativas del housekeeping
        df_realvalues = app.sensing_temperatures(df_nominalvalues["Sensor"].values.tolist())

        # PASO 5: comparo los valores nominales de las variables representativas con los estados de las variables
        state_list = []

        for sensor, cols in df_realvalues.iterrows():
            print("sensor:", sensor)
            print("cols:", cols)
            
        # PASO 6: creo el DataFrame que reporta el estado de un sensor: 'Out of range' o 'In range'
        index = pd.Index(sensors_list, name="Sensor")
        df_housekeeping = pd.DataFrame({'Estado': state_list}, index=index)
        
        return df_housekeeping
    else:
        return 