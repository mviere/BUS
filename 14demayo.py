import time
import random
import numpy as np
import pandas as pd

def mode_management (df_mode: pd.DataFrame, df_premode: pd.DataFrame, deftable_filename: str, cant_T: int, T: int) -> list:

    # Leo definition table de modos
    df_deftable = CSV2DF(deftable_filename)

    # Creo la futura fila de comandos
    command_queue = []
    
    # Obtengo secuencia de comandos del modo
    modo = df_mode["Modo"].values[0]
    commmand_queue2 = mode_processing(deftable_filename, modo)

    # Si hay que transicionar de modo,
    if df_mode['Modo'].values[0] != df_premode['Modo'].values[0]:

        # Busco los comandos de transición y los coloco primeros en la fila
        command_queue_trans = mode_transition("deftable_transicion.csv")
        for cmd in command_queue_trans:
            command_queue.append(cmd)

        # Agrego los comandos del modo hasta completar el tiempo T
        resto = cant_T*T - len(command_queue)
        i = 0
        for k in range(resto):
            for cmd in commmand_queue2:
                if i < resto:
                    command_queue.append(cmd)
                    i += 1
    
    # Si me mantengo en el mismo modo que el T anterior,
    #else:
        # Observo en qué parte del bloque de comandos quedé en el T anterior
        
        # Agrego los comandos que siguen hasta completar el tiempo T
        

    return command_queue

def mode_transition(deftable_filename: str):

    commmand_queue_trans = []
    df_deftable = CSV2DF(deftable_filename)

    for cmd in df_deftable.values.tolist():
        for c in cmd:
            commmand_queue_trans.append(c)

    return commmand_queue_trans

def mode_processing(deftable_filename: str, modo: str):

    commmand_queue = []

    df_deftable = CSV2DF(deftable_filename)
    df_blockcmd = df_deftable.loc[(df_deftable["Modo"] == modo), :]

    for cmd in df_blockcmd['Comandos'].values.tolist():
        commmand_queue.append(cmd)
        
    return commmand_queue

def CSV2DF (filename: str) -> pd.DataFrame:

    """
    Requiere: 
    - `import pandas as pd`

    @brief

    @param filename (str):                 Nombre del archivo 

    @return df   (pandas.DataFrame):       DataFrame de los datos
    """
    
    df = pd.read_csv(filename, header=[0])
    return df

# %% Función Main

def main() -> None:

    """
    Requiere:
    - `import pandas as pd`
    @brief
    @param None
    @return None
    """
    print("\nImportando librerías y scripts necesarios...")
    
    # Leo archivo escenario
    escenario_filename = "escenario2.csv"
    df_escenario = CSV2DF(escenario_filename)

    # Defino granularidades temporales [segundos]
    T = 10
    t = 1

    endProgram = False
    while endProgram == False:

        # Itero el archivo escenario. Cada fila es un Tiempo que tiene asociado un Modo.
        for Tn, mode in df_escenario.iterrows():
            
            # Defino el DataFrame modo y premodo. En cada uno de ellos, está la información Tiempo y Modo.
            df_mode = df_escenario.loc[[Tn], :]
            if Tn == 0:
                df_premode = df_escenario.loc[[Tn], :]
            else:
                df_premode = df_escenario.loc[[Tn-1], :]
            
            # Llamo a la función de gestión de modo
            deftable_filename = "deftable_modos.csv"
            command_queue = mode_management(df_mode, df_premode, deftable_filename, cant_T, T)
            print(command_queue)

            #T = df_escenario['Tiempo']
            #tiempo = time_management(T,t)
            #command_processing(comandos, tiempo)
        
        endProgram = True 
    return
                

if __name__ == "__main__":
    main()

'''
def mode_management(modo):
    Lista_de_Cmd = []
    evalúa si debe ocurrir una transición, compara el ModoX con Modo anterior escenario[n-1]
    si hay transición:
        Lista_de_Cmd_Trans = función transición de modos()
        comandos.append(Lista_de_Cmd_Trans)
    Lista_de_Cmd = función procesamiento de modos(Modox)
    comandos.append(Lista_de_Cmd)
    return Lista_de_Cmd
'''
'''
def transición de modos():
    lee los comandos de la def table de trans.
    return Lista_de_Cmd_Trans

t = 0
comando = ""
'''
'''
'Funcion contador'
def():
    ....
return contando, T, t, 

'Funcion ejecucion de escenario'
while ('parametro booleano de la funcion contador de tiempo'):
    t += 1 'potestad de funcion contador'
    if t % 1 == 0:
        comando = random.choice(["comando1", "comando2", "comando3"])
    print("t:", t, "comando:", comando)
    time.sleep(1)
'''
'''
def main():
    es una función anidada en la que realiza las siguientes acciones:
        lee línea de archivo escenario
        interactua con función gestión de modos(ModoX)
        interactua con función gestión del tiempo()
        ejecuta escenario une comando con tiempo
    return

def gestión de modos(ModoX):
    Lista_de_Cmd = []
    evalúa si debe ocurrir una transición, compara el ModoX con Modo anterior escenario[n-1]
    si hay transición:
        Lista_de_Cmd_Trans = función transición de modos()
        comandos.append(Lista_de_Cmd_Trans)
    Lista_de_Cmd = función procesamiento de modos(Modox)
    comandos.append(Lista_de_Cmd)
    return Lista_de_Cmd

def transición de modos():
    lee los comandos de la def table de trans.
    return Lista_de_Cmd_Trans

def procesamiento de modos(ModoX):
    lee los comandos de las def table de modos.
    return Lista_de_Cmd

def gestión del tiempo():
    contador
    return contando, T, t
'''

''''''''''''