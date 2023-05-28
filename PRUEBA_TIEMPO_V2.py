import numpy as np
import pandas as pd
import threading
import time


class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._current_time = 0
        self._is_running = False
        self._lock = threading.Lock()

    def run(self):
        self._is_running = True
        while self._is_running:
            with self._lock:
                self._current_time += 1
            time.sleep(1)

    def stop(self):
        self._is_running = False

    def get_current_time(self):
        with self._lock:
            return self._current_time

    def increment_time(self):
        with self._lock:
            self._current_time += 1


def CSV2DF(filename: str) -> pd.DataFrame:
    # Leo el archivo CSV y lo almaceno en un DataFrame
    df = pd.read_csv(filename, header=[0])
    return df


def mode_transition(deftable_filename: str):
    # Inicializo la fila de comandos de transicion
    commmand_queue_trans = []

    # Creo un DataFrame con la informacion contenida en la definition table de transicion
    df_deftable = CSV2DF(deftable_filename)

    # Agrego los comandos definidos en el DataFrame a la lista de comandos de transicion
    for cmd in df_deftable.values.tolist():
        for c in cmd:
            commmand_queue_trans.append(c)

    return commmand_queue_trans


def mode_processing(deftable_filename: str, modo: str):
    # Inicializo la fila de comandos
    commmand_queue = []

    # Creo un DataFrame con la informacion contenida en la definition table de transicion
    # Se filtra el DataFrame para obtener las filas donde la columna "Modo" es igual al modo especificado
    # Creo un DataFrame que contiene solo las filas del modo especificado
    df_deftable = CSV2DF(deftable_filename)
    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == modo), :]

    # Obtengo los comandos del nuevo DataFrame y los agrego a la fila de comandos
    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)

    return commmand_queue


def mode_management(df_mode: pd.DataFrame, deftable_filename: str, cant_T: int, T: int) -> list:
    # Creo un DataFrame con la informacion contenida en la definition table
    df_deftable = CSV2DF(deftable_filename)

    # Inicializo la fila de comandos
    command_queue = []

    # Busco los comandos de transición y los agrego en la fila de comandos
    command_queue_trans = mode_transition("deftable_transicion.csv")
    for cmd in command_queue_trans:
        command_queue.append(cmd)

    # Obtengo la secuencia de comandos del modo
    modo = df_mode["Modo"].values[0]
    commmand_queue2 = mode_processing(deftable_filename, modo)

    # Agrego los comandos del modo hasta completar el tiempo T
    resto = cant_T * T - len(command_queue)
    i = 0
    for k in range(resto):
        for cmd in commmand_queue2:
            if i < resto:
                command_queue.append(cmd)
                i += 1

    return command_queue


def command_processing(command_queue: list, timer):
    # Ejecuto (imprimo) los comandos de la fila junto con el valor de tiempo asociado
    for cmd in command_queue:
        t = timer.get_current_time()
        print("t:", t, cmd)
        time.sleep(1)


def main():
    print("\nImportando librerías y scripts necesarios...\n")

    # Leo el archivo 'escenario'
    escenario_filename = "escenario.csv"
    df_escenario = CSV2DF(escenario_filename)

    # Defino granularidades temporales [segundos]
    T = 10

    # Creo el objeto TimerThread
    timer = TimerThread()
    timer.start()

    endProgram = False
    while not endProgram:
        # Itero el archivo escenario. Cada fila es un Modo asociado a un numero de ciclos de tiempo
        for index, cols in df_escenario.iterrows():
            # Para cada fila, extraigo la informacion del modo y numero de ciclos y lo guardo en un DataFrame
            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]

            # Llamo a la función de gestión de modo y obtengo la fila de comandos
            deftable_filename = "deftable_modos.csv"
            command_queue = mode_management(df_mode, deftable_filename, ciclos, T)

            # Ejecuto secuencia de comandos con el tiempo
            command_processing(command_queue, timer)

        endProgram = True

    timer.stop()
    timer.join()

if __name__ == "__main__":
    main()




