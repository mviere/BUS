import numpy as np
import pandas as pd
import threading
import time
import random
import Componentes as comp


# %% Application
# ---------------------------------------------------------------------------- #

def sensing_temperature (sensors_list):
    """
    Esta función genera el registro del estado de las variables representativas del housekeeping.
    """
    temp_list = []

    for sensor in sensors_list:
        temp = comp.temp_sensors(sensor)
        temp_list.append(temp)

    # Creo el DataFrame de Housekeeping
    index = pd.Index(sensors_list, name="Sensor")
    df_realvalues = pd.DataFrame({'Temperatura [C]': temp_list}, index=index)

    return df_realvalues