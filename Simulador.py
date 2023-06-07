import numpy as np
import pandas as pd
import threading
import time
import random
import AlgoritmoC2A as ac
import FuncAux as fa


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
    
    previous_mode = None

    endProgram = False
    while not endProgram:
        
        T = 0
        for index, cols in df_escenario.iterrows():

            df_mode = df_escenario.loc[[index], :]
            cant_ciclos = df_mode['Ciclos'].values[0]
            mode_name = df_mode['Modo'].values[0]
            
            for ciclo in range(cant_ciclos):

                time_queue = list(range(dT))
                
                command_queue, df_nominalvalues, mode_name = ac.mode_management(mode_name, previous_mode, dT, deftable_modos, deftable_transicion, deftable_housekeeping)
                
                event_time = None
                for t in range(dT):

                    probability = 0.2
                    if random.random() < probability:
                        event = True
                        event_cycle = T
                        event_time = t

                    else:
                        event = False
                    
                if event:
                    event = random.choice(["Evento E", "Evento F"])
                    command_queue = ac.event_handling(event, event_register, deftable_eventos, dT, event_time, event_cycle)
                    ac.command_processing(df_nominalvalues, command_queue, time_queue, T)
                    mode_name = 'Safe'
                
                else:
                    ac.command_processing(df_nominalvalues, command_queue, time_queue, T)
            
                previous_mode = mode_name
                T += 1

        endProgram = True

if __name__ == "__main__":
    main()
    