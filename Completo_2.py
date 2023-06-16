import numpy as np
import pandas as pd
import threading
import time
import random
import FuncAux as fa
import datetime


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


# %% Componentes
# ---------------------------------------------------------------------------- #

def temp_sensor (sensor):
    """
    Esta función 
    """
    temp = random.uniform(-40, 80)

    return temp

def event_sensor ():
    """
    Esta función
    """
    
    variable = random.uniform(-150, 190)

    return variable


def actuators ():
    return


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


def anomaly_control (event_register: str):

    '''
    Esta funcion utiliza event_sensor, toma el valor de la variable, lo asocia a un evento
    y te devuelve ID, Descripcion y Tiempo
    '''
    
    variable = event_sensor()

    event_ID = 0
    event_description = None
    t_actual = datetime.datetime.now().strftime('%H:%M:%S')

    if variable not in range(-40, 80):

        event_ID = 1
        event_description = 'Fuga'
    
    df_event = pd.DataFrame({'Event ID': [event_ID], 'Description': [event_description], 'Time': [t_actual]})
        
    return df_event


# %% Algoritmo C2A
# ---------------------------------------------------------------------------- #

def mode_processing(deftable_modos: str, deftable_block: str, deftable_housekeeping: str, mode_name: str):
    
    # Creación del DataFrame con los comandos y su deploy time
    
    df_deftable_modos = fa.CSV2DF(deftable_modos)
    df_deftable_block = fa.CSV2DF(deftable_block)

    mode_ID = mode_name[-1]

    block_ID = df_deftable_modos.loc[(df_deftable_modos["Modo ID"] == mode_ID), :]['Block ID'].values[0]
    df_commands = df_deftable_block.loc[(df_deftable_block["Block ID"] == block_ID), :]
    
    commmand_queue = []
    deploy_time = []
    for cmd in df_commands['Command'].values.tolist():
        commmand_queue.append(cmd)
    for dT in df_commands['dT'].values.tolist():
        deploy_time.append(dT)
    
    df_modecommands = pd.DataFrame({'Command': commmand_queue, 'dT': deploy_time})
    
    # Creación del DataFrame con los valores nominales de las variables de housekeeping
    df_deftable_housekeeping = fa.CSV2DF(deftable_housekeeping)
    df_housekeeping = df_deftable_housekeeping.loc[(df_deftable_housekeeping["Modo"] == mode_name), :]   
    index = pd.Index(df_housekeeping["Sensor"].values, name="Sensor")
    df_nominalvalues = pd.DataFrame({'Temperatura min. [C]': df_housekeeping["Temperatura min [C]"].values, 'Temperatura max. [C]': df_housekeeping["Temperatura max [C]"].values}, index=index)

    return df_modecommands, df_nominalvalues


def mode_transition(deftable_transicion: str, deftable_block: str):

    df_deftable_trans = fa.CSV2DF(deftable_transicion)
    df_deftable_block = fa.CSV2DF(deftable_block)
    
    block_ID = df_deftable_trans.loc[(df_deftable_trans["Modo ID"] == "T"), :]['Block ID'].values[0]
    df_commands = df_deftable_block.loc[(df_deftable_block["Block ID"] == block_ID), :]

    commmand_queue = []
    deploy_time = []
    for cmd in df_commands['Command'].values.tolist():
        commmand_queue.append(cmd)
    for dT in df_commands['dT'].values.tolist():
        deploy_time.append(dT)
    
    df_transcommands = pd.DataFrame({'Command': commmand_queue, 'dT': deploy_time})

    return df_transcommands


def mode_management (mode_name: str, transition: bool, deftable_modos: str, deftable_transicion: str, deftable_housekeeping: str, deftable_block: str):
    """
    Esta función
    """
    df_modecommands, df_nominalvalues = mode_processing(deftable_modos, deftable_block, deftable_housekeeping, mode_name)
    
    if transition:
        df_transcommands = mode_transition(deftable_transicion, deftable_block)
        df_commands = pd.concat([df_transcommands, df_modecommands])
        return df_commands, df_nominalvalues
    else:
        return df_modecommands, df_nominalvalues
    

def application_management (option: str, df_nominalvalues: pd.DataFrame):
    ''"""''
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


def anomaly_logger(event_register: str):
    '''
    LLama a anomaly_control y con la info arma un csv con el registro de eventos
    '''
    
    df_event = anomaly_control()

    if df_event['Event ID'] == 0:        
        fa.DF2CSV(df_event, event_register, 'append')

    return


def event_handling(deftable_eventos: str, deftable_block_command: str, event_register: str) -> list:
    
    '''
    Revisa event_register
    '''
    
    df_register = fa.CSV2DF(event_register)
    df_deftable = fa.CSV2DF(deftable_eventos)
    df_blockcmd = fa.CSV2DF(deftable_block_command)
    
    if df_register.empty:
        df_eventcommands = pd.DataFrame({'A' : []})
   
    else:
        commmand_queue = []
        deploy_time = []

        for index, row in df_register.interrows():

            event_ID = row['Event_ID']
            block_ID = df_deftable.loc[(df_deftable["Event ID"] == event_ID), :]['Block ID'].values[0]
            df_commands = df_blockcmd.loc[(df_blockcmd["Block ID"] == block_ID), :]
        
            for cmd in df_commands['Command'].values.tolist():
                commmand_queue.append(cmd)
            for dT in df_commands['dT'].values.tolist():
                deploy_time.append(dT)
        
        df_eventcommands = pd.DataFrame({'Command': commmand_queue, 'dT': deploy_time})

    return df_eventcommands


def command_processing(df_commands: pd.DataFrame, df_safemode: pd.DataFrame, df_event_commands: pd.DataFrame, dN: int, n: int):

    if not df_safemode.empty and not df_event_commands.empty:

        n_plus = 2

        print(f"Safemode")
        for dT in range(dN):
            if dT in df_safemode['dT'].values.tolist():
                cmd = df_safemode.loc[(df_safemode['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)

        n = n + 1
        print(f"Event")
        for dT in range(dN):
            if dT in df_event_commands['dT'].values.tolist():
                cmd = df_event_commands.loc[(df_event_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)

        n = n + 1
        print(f"Mode")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)
        
    # ---------------------------------------------------------
    if not df_safemode.empty and df_event_commands.empty:

        n_plus = 1

        print(f"Safemode")
        for dT in range(dN):
            if dT in df_safemode['dT'].values.tolist():
                cmd = df_safemode.loc[(df_safemode['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)
    
        n = n + 1
        print(f"Mode")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)

    # ---------------------------------------------------------
    if df_safemode.empty and not df_event_commands.empty:

        n_plus = 1

        print(f"Event")
        for dT in range(dN):
            if dT in df_event_commands['dT'].values.tolist():
                cmd = df_event_commands.loc[(df_event_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)

        n = n + 1
        print(f"Mode")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)

    # ---------------------------------------------------------
    if df_safemode.empty and df_event_commands.empty:

        n_plus = 0

        print(f"Mode")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.5)
            
    return n_plus


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

        N_plus = 0
        n_plus = 0
        
        for index in range(len(df_escenario.index.values)-1):
            print("--------------------------------------------------")
            mode_name = df_escenario.loc[index,'Modo']
            N = int(df_escenario.loc[index,'N']) + N_plus
            N_post = int(df_escenario.loc[index+1,'N']) + N_plus
            print(f"Se cubriran los ciclos: [{N},{N_post}]")
            transition = True
            N_plus = 0
            for n in range(N, N_post):
                # Acá hay un problema con range. Con todos los n_plus dentro de este for, me voy más allá del N_post
                n = n_plus + n
                df_commands, df_nominalvalues = mode_management(mode_name, transition, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                SafeMode = application_management('housekeeping', df_nominalvalues)
                #df_event_commands = ac.event_handling(deftable_events, deftable_block, event_register)
                df_event_commands = pd.DataFrame({'A' : []})
                if SafeMode:
                    df_safemode, df_nominalvalues = mode_management('Modo S', False, deftable_modes, deftable_transition, deftable_housekeeping, deftable_block)
                else:
                    df_safemode = pd.DataFrame({'A' : []})
                
                n_plus = command_processing(df_commands, df_safemode, df_event_commands, dN, n)
                transition = False
                N_plus = N_plus + n_plus

        endProgram = True

if __name__ == "__main__":
    main()
