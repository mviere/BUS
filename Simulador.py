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
    df = pd.DataFrame(columns=['Event ID', 'Description', 'Time', 'Ciclo'])
    fa.DF2CSV(df, event_register, 'write')
    
    endProgram = False

    while not endProgram:
        
        N_plusplus = 0
        N_plus = 0
        n_plus = 0
        
        for index in range(len(df_escenario.index.values)-1):

            mode_name = df_escenario.loc[index,'Modo'] 
            N = int(df_escenario.loc[index,'N']) + N_plusplus # N es el N donde arranca del Modo A   N = 7 + 2 = 9
            N_post = int(df_escenario.loc[index+1,'N']) + N_plusplus # N_post es el N donde arranca del Modo B    N = 10 + 2 = 

            transition = True
            N_plus = 0
            
            for i in range(N, N_post): # (10,11)      # i = 11

                n = N_plus + i     # n = 12
                df_commands, df_nominalvalues = ac.mode_management(mode_name, transition, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                SafeMode = ac.application_management('housekeeping', df_nominalvalues)
                
                if n == 0:
                    df_event_commands = pd.DataFrame({'A' : []})
                else:
                    df_event_commands = ac.event_handling(deftable_events, deftable_block, event_register, n-1)
            
                if SafeMode:
                    df_safemode, df_nominalvalues = ac.mode_management('Modo S', False, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                else:
                    df_safemode = pd.DataFrame({'A' : []})
                #df_event_commands = pd.DataFrame({'A' : []})
                #df_safemode = pd.DataFrame({'A' : []})
                n_plus = ac.command_processing(df_commands, df_safemode, df_event_commands, dN, n, i)   # n_plus = 1
                transition = False
                N_plus = N_plus + n_plus      # N_plus = 2
                ac.anomaly_logger(event_register, n)
            N_plusplus = N_plusplus + N_plus
        endProgram = True

if __name__ == "__main__":
    main()
    