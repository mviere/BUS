import numpy as np
import pandas as pd
import AlgoritmoC2A as ac
import FuncAux as fa
import Aplicacion as app

 
# %% Simulador
# ---------------------------------------------------------------------------- #

def main():
    
    # Información del archivo "escenario.csv".
    escenario_filename = "escenario.csv"                #Establece una intención de secuencia de modos y su permanencia
    df_escenario = fa.CSV2DF(escenario_filename)

    # Un tiempo determinado T se define a partir del número de ciclo N y el número de step dT,      T = N + dT
    # A su vez, un ciclo N está dividido en steps dT.
        # Duración de un ciclo N (cantidad de steps)
    dN = 13
        # Duración de un step dT (cantidad de segundos)
    #deltaT = 1

    # Rutas a archivos auxiliares
    deftable_modes = "deftable_modes.csv"                #Def. Table con Bloque de Comandos ID para cada modo
    deftable_transition = "deftable_transition.csv"      #Def. Table con Bloque de Comandos ID para la transición entre modos
    deftable_housekeeping = "deftable_housekeeping.csv"  #Def. Table con valores nominales de las variables del housekeeping
    deftable_block = "deftable_block_command.csv"        #Def. Table con Comandos para cada Bloque ID
    deftable_events = "deftable_events.csv"              #Def. Table con Bloque de Comandos ID para el manejo de eventos impredecibles
    event_register = "event_register.csv"              
    
    # Creación del DataFrame donde se almacenarán los eventos ocurridos
    df = pd.DataFrame(columns=['Descripcion', 'Tiempo'])
    fa.DF2CSV(df, event_register, 'write')
    
    endProgram = False

    while not endProgram:

        new_n = 0
        for index in range(len(df_escenario.index.values)-1):

            mode_name = df_escenario.loc[index,'Modo']
            N = int(df_escenario.loc[index,'N'])
            N_post = int(df_escenario.loc[index+1,'N'])

            transition = True
            
            for n in range(N, N_post):
                print("n del Simulador:", n)
                n = new_n + n
                print("n + new_n del Simulador:", n)
                
                df_commands, df_nominalvalues = ac.mode_management(mode_name, transition, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                SafeMode = ac.application_management('housekeeping', df_nominalvalues)
                df_event_commands = ac.event_handling(deftable_events, deftable_block, event_register)
                
                if SafeMode:
                    df_safemode, df_nominalvalues = ac.mode_management('Modo S', False, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                else:
                    df_safemode = pd.DataFrame({'A' : []})
                
                new_n = ac.command_processing(df_commands, df_safemode, df_event_commands, dN, n)
                transition = False

        endProgram = True

if __name__ == "__main__":
    main()
    
'''
def main2():
    
    # Información del archivo "escenario.csv".
    escenario_filename = "escenario.csv"                #Establece una intención de secuencia de modos y su permanencia
    df_escenario = fa.CSV2DF(escenario_filename)

    # Un tiempo determinado T se define a partir del número de ciclo N y el número de step dT,      T = N + dT
    # A su vez, un ciclo N está dividido en steps dT.
        # Duración de un ciclo N (cantidad de steps)
    deltaN = 13
        # Duración de un step dT (cantidad de segundos)
    deltaT = 1

    # Rutas a archivos auxiliares
    deftable_modos = "deftable_modos.csv"                #Def. Table con Bloque de Comandos para cada modo
    deftable_transicion = "deftable_transicion.csv"      #Def. Table con Bloque de Comandos para la transición entre modos
    deftable_housekeeping = "deftable_housekeeping.csv"  #Def. Table con Bloque de Comandos para el housekeeping de cada modo
    deftable_eventos = "deftable_eventos.csv"            #Def. Table con Bloque de Comandos para el manejo de eventos impredecibles
    event_register = "event_register.csv"              
    
    # Creación del DataFrame donde se almacenarán los eventos ocurridos
    df = pd.DataFrame(columns=['Descripcion', 'Tiempo'])
    fa.DF2CSV(df, event_register, 'write')
    
    endProgram = False
    previous_mode = None

    while not endProgram:
        
        T = 0

        for index, cols in df_escenario.iterrows():

            df_mode = df_escenario.loc[[index], :]
            cant_ciclos = df_mode['N'].values[0]
            mode_name = df_mode['Modo'].values[0]
            event_list = [None]       

            for ciclo in range(cant_ciclos):

                if all(value is None for value in event_list):

                    command_queue, df_nominalvalues, mode_name = ac.mode_management(mode_name, previous_mode, deltaN, deftable_modos, deftable_transicion, deftable_housekeeping)
            
                else:

                    command_queue = ac.event_handling(event_list, event_register, deftable_eventos, deltaN)
                    mode_name = 'Safe Mode'

                for dT in range(deltaN):

                    event_list.append(app.event_test())
                    
                    # Ejecuto la realización del housekeeping
                    SafeMode = ac.application_management('housekeeping', df_nominalvalues)
    
                    #Ejecuto la activación del Safe Mode de ser necesario
                    #if SafeMode:
                        #print('Activar Safe Mode')

                    ac.command_processing(command_queue, dT, T)
                    
                previous_mode = mode_name
                T += 1

        endProgram = True

if __name__ == "__main__":
    main2()
    
Empieza con event_handling y finaliza con anomaly_logger
'''