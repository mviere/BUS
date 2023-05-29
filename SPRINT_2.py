import numpy as np
import pandas as pd
import threading
import time
import random


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


def mode_management (df_mode: pd.DataFrame, deftable_filename: str, cant_T: int, dT: int) -> list:

    command_queue = []

    command_queue_trans = mode_transition("deftable_transicion.csv", dT)
    command_queue.extend(command_queue_trans)
   
    modo = df_mode["Modo"].values[0]
    command_queue2, lista_duracion = mode_processing(deftable_filename, modo)
    
    for ciclo in range(cant_T):
        for i in range(len(command_queue2)):
            for j in range(lista_duracion[i]):
                command_queue.append(command_queue2[i])
        while len(command_queue) % dT != 0:
            command_queue.append(None)

    return command_queue


def command_processing (command_queue: list, timer) -> None:
  
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


def main():
    
    print("\nImportando librerías y scripts necesarios...\n")

    escenario_filename = "escenario.csv"
    df_escenario = CSV2DF(escenario_filename)

    dT = 5
    dt = 1
    
    deftable_filename = "deftable_modos.csv"
    regist_filename = "event_register.csv"
    df_evento1 = pd.DataFrame(columns=['Descripcion', 'Cualk'])
    DF2CSV(df_evento1, regist_filename, 'write')

    timer = TimerThread()
    timer.start()

    endProgram = False
    while not endProgram:
        
        for index, cols in df_escenario.iterrows():
            
            event = bool(random.getrandbits(1))
            if event:
                event = random.choice(["Perdida de SMA por drag", "Perturbaciones por gravedad"])

                deftable_eventos = "deftable_eventos.csv"
                command_queue = event_handling(event, regist_filename, deftable_eventos, dT, timer)

                command_processing(command_queue, timer)

            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]

            deftable_filename = "deftable_modos.csv"
            command_queue = mode_management(df_mode, deftable_filename, ciclos, dT)
            
            command_processing(command_queue, timer)

        endProgram = True

    timer.stop()
    timer.join()

if __name__ == "__main__":
    main()
