import numpy as np
import pandas as pd
import threading
import time
import random
import AlgoritmoC2A as ac


# %% Simulador
# ---------------------------------------------------------------------------- #


def main():
    
    print("\nImportando librerías y scripts necesarios...\n")

    escenario_filename = "escenario.csv"
    df_escenario = ac.CSV2DF(escenario_filename)

    dT = 5
    dt = 1
    
    deftable_filename = "deftable_modos.csv"
    deftable_filename2 = "deftable_transicion.csv"
    deftable_filename3 = "deftable_housekeeping.csv"

    deftable_eventos = "deftable_eventos.csv"
    regist_filename = "event_register.csv"
    df_evento1 = pd.DataFrame(columns=['Descripcion', 'Cualk'])
    ac.DF2CSV(df_evento1, regist_filename, 'write')

    timer = ac.TimerThread()
    timer.start()


    
    endProgram = False
    while not endProgram:
        
        for index, cols in df_escenario.iterrows():
            
            df_mode = df_escenario.loc[[index], :]
            ciclos = df_mode['Ciclos'].values[0]
            # PASO 1: obtengo los valores nominales de las variables representativas de housekeeping del modo
            command_queue, df_nominalvalues = ac.mode_management(df_mode, deftable_filename, deftable_filename2, deftable_filename3, ciclos, dT)
            
            event = bool(random.getrandbits(1))
            if event:
                event = random.choice(["Perdida de SMA por drag", "Perturbaciones por gravedad"])

                command_queue = ac.event_handling(event, regist_filename, deftable_eventos, dT, timer)

                ac.command_processing(df_nominalvalues, command_queue, timer)

            # PASO 2: paso los valores nominales a commando processing para obtener el estado de housekeeping allí
            ac.command_processing(df_nominalvalues, command_queue, timer)

        endProgram = True

    timer.stop()
    timer.join()

if __name__ == "__main__":
    main()

