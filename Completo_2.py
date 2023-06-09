import numpy as np
import pandas as pd
import threading
import time
import random
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

    while len(command_queue) < dT:
        command_queue.append(None)

    return command_queue, df_nominalvalues, mode_name


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
        df_housekeeping = housekeeping(df_nominalvalues)
        
        # Ordeno cambiar a Safe Mode si el reporte lo indica
        SafeMode = False
        for state in df_housekeeping['Estado'].values:
            if state == 'Out of range':
                SafeMode = True
                break
        
        return SafeMode
    
    else:
        return


def event_handling(event_list: pd.DataFrame, event_register: str, deftable_eventos: str, dT: int) -> list:
    
    command_queue_event = []

    for df in event_list:

        if df is not None:

            df_deftable = fa.CSV2DF(deftable_eventos)
            df_blockcmd = df_deftable.loc[df_deftable["Evento"] == df['Evento'][0]]

            command_queue_event.extend(df_blockcmd['Comandos'].values.tolist())

            new_row = pd.DataFrame({'Descripcion': [df_blockcmd["Evento"].values[0]], 'Ciclo': df['Ciclo'][0], 'Tiempo': df['Tiempo'][0]})
            df_evento = pd.DataFrame(new_row)
            fa.DF2CSV(df_evento, event_register, 'append')

            while len(command_queue_event) < dT:
               command_queue_event.append(None)

    return command_queue_event


# %% Application
# ---------------------------------------------------------------------------- #

def sensing_temperature (sensors):
    """
    Esta función interactúa con Componentes para obtener las temperaturas en los sensores ingresados.
    """
    temp_list = []

    for sensor in sensors:
        temp = temp_sensor(sensor)
        temp_list.append(temp)

    index = pd.Index(sensors, name='Sensor')
    df_realvalues = pd.DataFrame({'Temperatura [C]': temp_list}, index=index)

    return df_realvalues


def housekeeping (df_nominalvalues: pd.DataFrame):
    """
    Esta función realiza las tareas de housekeeping y reporta su estado.
    """
    # Solicito estado de las variables representativas del housekeeping
    ## Hoy son las temepraturas de 3 sensores, pero podrían ser otras más como la carga de batería
    df_realvalues = sensing_temperature(df_nominalvalues.index.values)
    
    # Comparo el estado de las variables con sus valores nominales y reporto
    ## En este caso, verifico que las temperaturas sensadas esten dentro del rango [T min; T max]
    ## Reporto el estado de un sensor: 'Out of range' o 'In range'
    state_list = []
    i = 0
    for sensor, temp in df_realvalues.iterrows():
        if df_nominalvalues['Temperatura min. [C]'].values[i] < df_realvalues['Temperatura [C]'].values[i] < df_nominalvalues['Temperatura max. [C]'].values[i]:
            state_list.append('Out of range')
        else:
            state_list.append('In range')
        i = i + 1
                
    # Devuelvo la información en un DataFrame
    index = pd.Index(df_nominalvalues.index.values, name='Sensor')
    df_housekeeping = pd.DataFrame({'Estado': state_list}, index=index)

    return df_housekeeping


def event_test (T, t):
    
    df = None
    probability = 0.1

    if random.random() < probability:

        event = random.choice(["Evento E", "Evento F"])
        
        data = {'Ciclo': [T], 'Tiempo': [t], 'Evento': [event]}
        df = pd.DataFrame(data)

    return df


# %% Componentes
# ---------------------------------------------------------------------------- #

def temp_sensor (sensor):
    """
    Esta función 
    """
    temp = random.uniform(-40, 80)

    return temp

def actuators ():
    return


# %% Simulador
# ---------------------------------------------------------------------------- #

def main():
    
    # Información del archivo "escenario.csv".
    escenario_filename = "escenario.csv"                #Establece una intención de secuencia de modos y su permanencia
    df_escenario = fa.CSV2DF(escenario_filename)

    # Definición de granularidades temporales
    dT = 13
    
    # Rutas a archivos auxiliares
    deftable_modos = "deftable_modos.csv"                #Def. Table con Bloque de Comandos para cada modo
    deftable_transicion = "deftable_transicion.csv"      #Def. Table con Bloque de Comandos para la transición entre modos
    deftable_housekeeping = "deftable_housekeeping.csv"  #Def. Table con Bloque de Comandos para el housekeeping de cada modo
    deftable_eventos = "deftable_eventos.csv"            #Def. Table con Bloque de Comandos para el manejo de eventos impredecibles
    event_register = "event_register.csv"              
    
    # Creación del DataFrame donde se almacenarán los eventos ocurridos
    df = pd.DataFrame(columns=['Descripcion', 'Ciclo', 'Tiempo'])
    fa.DF2CSV(df, event_register, 'write')
    
    endProgram = False
    previous_mode = None

    while not endProgram:
        
        T = 0

        for index, cols in df_escenario.iterrows():

            df_mode = df_escenario.loc[[index], :]
            cant_ciclos = df_mode['Ciclos'].values[0]
            mode_name = df_mode['Modo'].values[0]
            event_list = []
            
            for ciclo in range(cant_ciclos):

                if len(event_list) == 0:

                    command_queue, df_nominalvalues, mode_name = mode_management(mode_name, previous_mode, dT, deftable_modos, deftable_transicion, deftable_housekeeping)
                
                else:

                    command_queue = event_handling(event_list, event_register, deftable_eventos, dT)
                    mode_name = 'Safe Mode'

                for t in range(dT):

                    event_list.append(event_test(T, t))
                    
                    # Ejecuto la realización del housekeeping
                    SafeMode = application_management('housekeeping', df_nominalvalues)
    
                    # Ejecuto la activación del Safe Mode de ser necesario
                    #if SafeMode:
                        #print('Activar Safe Mode')

                    cmd = command_queue[t]
                    print(f"Ciclo: {T}, t: {t}, Comando: {cmd}")
         
                previous_mode = mode_name
                T += 1

        endProgram = True

if __name__ == "__main__":
    main()
    