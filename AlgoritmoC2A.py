import numpy as np
import pandas as pd
import FuncAux as fa
import Aplicacion as app
import time
 
 
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
        df_housekeeping = app.housekeeping(df_nominalvalues)
        
        # Ordeno cambiar a Safe Mode si el reporte lo indica
        SafeMode = False
        for state in df_housekeeping['Estado'].values:
            if state == 'Out of range':
                SafeMode = True
                break
        
        return SafeMode
    
    else:
        return


def anomaly_logger(event_register: str, N: int):
    '''
    LLama a anomaly_control y con la info arma un csv con el registro de eventos
    '''
    
    df_event = app.anomaly_control(N)

    if df_event['Event ID'].values[0] != 0:        
        fa.DF2CSV(df_event, event_register, 'append')

    return


def event_handling(deftable_eventos: str, deftable_block_command: str, event_register: str, n: int) -> list:
    
    '''
    Revisa event_register
    '''
    
    df_register = fa.CSV2DF(event_register) 
    df_deftable = fa.CSV2DF(deftable_eventos)
    df_blockcmd = fa.CSV2DF(deftable_block_command)
    
    if df_register.empty:
        df_eventcommands = pd.DataFrame({'A' : []})
   
    else:
        
        df_register2 = df_register.loc[df_register['Ciclo'] == n]
        commmand_queue = []
        deploy_time = []

        for index, row in df_register2.iterrows():

            event_ID = df_register2.loc[index,'Event ID']
            block_ID = df_deftable.loc[(df_deftable["Event ID"] == event_ID), :]['Block ID'].values[0]
            df_commands = df_blockcmd.loc[(df_blockcmd["Block ID"] == block_ID), :]

            for cmd in df_commands['Command'].values.tolist():
                commmand_queue.append(cmd)
            for dT in df_commands['dT'].values.tolist():
                deploy_time.append(dT)
        
        df_eventcommands = pd.DataFrame({'Command': commmand_queue, 'dT': deploy_time})

    return df_eventcommands


def command_processing(df_commands: pd.DataFrame, df_safemode: pd.DataFrame, df_event_commands: pd.DataFrame, dN: int, n: int, i:int):

    if not df_safemode.empty and not df_event_commands.empty:

        n_plus = 2

        print(f"\n\t\tTurning to Safemode")
        for dT in range(dN):
            if dT in df_safemode['dT'].values.tolist():
                cmd = df_safemode.loc[(df_safemode['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)

        n = n + 1
        print(f"\n\t\tEvent Handling")
        for dT in range(dN):
            if dT in df_event_commands['dT'].values.tolist():
                cmd = df_event_commands.loc[(df_event_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)

        n = n + 1
        print(f"\n\t\tMode Processing")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)
        
    # ---------------------------------------------------------
    elif not df_safemode.empty and df_event_commands.empty:

        n_plus = 1

        print(f"\n\t\tTurning to Safemode")
        for dT in range(dN):
            if dT in df_safemode['dT'].values.tolist():
                cmd = df_safemode.loc[(df_safemode['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}") # n = 2
            time.sleep(0.25)
    
        n = n + 1 # n = 3
        print(f"\n\t\tMode Processing")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)

    # ---------------------------------------------------------
    elif df_safemode.empty and not df_event_commands.empty:

        n_plus = 1

        print(f"\n\t\tEvent Handling")
        for dT in range(dN):
            if dT in df_event_commands['dT'].values.tolist():
                cmd = df_event_commands.loc[(df_event_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)

        n = n + 1
        print(f"\n\t\tMode Processing")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)

    # ---------------------------------------------------------
    elif df_safemode.empty and df_event_commands.empty:

        n_plus = 0

        print(f"\n\t\tMode Processing")
        for dT in range(dN):
            if dT in df_commands['dT'].values.tolist():
                cmd = df_commands.loc[(df_commands['dT'] == dT), :]['Command'].values[0]
            else:
                cmd = ''
            print(f"Ciclo: {n}, dT: {dT}, Comando: {cmd}")
            time.sleep(0.25)
            
    return n_plus
