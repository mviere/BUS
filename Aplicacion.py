import numpy as np
import pandas as pd
import threading
import time
import random
import Componentes as comp


# %% Application
# ---------------------------------------------------------------------------- #

def sensing_temperature (sensors):
    """
    Esta función interactúa con Componentes para obtener las temperaturas en los sensores ingresados.
    """
    temp_list = []

    for sensor in sensors:
        temp = comp.temp_sensor(sensor)
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