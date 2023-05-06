"""
\authors 

\brief 

\version 0

\date 06/05/2023
"""
# %%

print("\nImportando librerías y scripts necesarios...")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constantes import *
import transformations as tr

# %% Solve deprecation warnings

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

# %% Funciones esenciales

def ModeManagement (mode: str) -> None:
    """
    Requiere: 
    - `import pandas as pd`

    @brief blblb
    

       | nnnn  | gggggggg   | gggggggg|ggggggggg| gg   |   ggg    |  ggg                  |
       |:------|:----------:|:--------|:--------|:-----:|:--------:|:----------------------|
       | S1    |(value)     |(value)  |(value)  |(value)| (value)  |                       |
       | S2    |(value)     |(value)  |(value)  |(value)| (value)  |-                      |
       | ...   |...         |...      |...      | ...   |  ...     |  ...                  |
       | Sn    |(value)     |(value)  |(value)  |(value)| (value)  | Lbbbbbbbbbbbbbbb      |


    @param timeline (list):    grrr
    @param block (pandas.DataFrame):       DataFrame de tabla de definición

    @return    
    """
    ModeProcessing()
    TransitionMode()
    return

def CommandProcessing (timeline: list, block:: pd.DataFrame) -> None:
    """
    Requiere: 
    - `import pandas as pd`

    @brief asocia comando con tiempo?
    

       | nnnn  | gggggggg   | gggggggg|ggggggggg| gg   |   ggg    |  ggg                  |
       |:------|:----------:|:--------|:--------|:-----:|:--------:|:----------------------|
       | S1    |(value)     |(value)  |(value)  |(value)| (value)  |                       |
       | S2    |(value)     |(value)  |(value)  |(value)| (value)  |-                      |
       | ...   |...         |...      |...      | ...   |  ...     |  ...                  |
       | Sn    |(value)     |(value)  |(value)  |(value)| (value)  | Lbbbbbbbbbbbbbbb      |


    @param timeline (list):    grrr
    @param block (pandas.DataFrame):       DataFrame de tabla de definición

    @return    
    """
    #según el tipo de ejecución y tiempo de ejecución, llamará a distintas funciones.
    #sino podría enlazar comando con tiempo y ejecutar
    #podría crear un diccionario o lista de tuplas con (Tiempo, Comando)
    #cada vez que se ejecuta el command processing, esta función vuelve a generar su línea de tiempo
    #y dónde se ubica cada commando
    # y luego llamar a la función Execture Command o Aplication comannd
    ExecuteCommand()
    return

# %% Menú principal

def menu() -> None:
    """
    Requiere:
    - `import pandas as pd`
    - `import matplotlib.pyplot as plt`
    - `import numpy as np`

    @brief Éj:

       | Name  | gggggggg   | gggggggg|ggggggggg| gg   |   ggg    |  ggg                  |
       |:------|:----------:|:--------|:--------|:-----:|:--------:|:----------------------|
       | S1    |(value)     |(value)  |(value)  |(value)| (value)  |                       |
       | S2    |(value)     |(value)  |(value)  |(value)| (value)  |-                      |
       | ...   |...         |...      |...      | ...   |  ...     |  ...                  |
       | Sn    |(value)     |(value)  |(value)  |(value)| (value)  | Lbbbbbbbbbbbbbbb      |

    Y l

    @param None
    @return None
    """
    endProgram = False
    while endProgram == False:
        print("\nIntroducir:")
        print("\n\t1) Cambio de modo\n\t\t(cambia el modo de operación aleatoriamente)")
        print("\t2) Evento impredecible\n\t\t()")
        print("\t3) Desviación de órbita\n\t\t()")
        print("\n\tPresione 0 para abandonar")

        backtoMenu = False
        menu_option = 7
        while menu_option not in [0, 1, 2, 3]:
            menu_option = input("\nIngrese la opción a ejecutar:\t\t\t")
            if menu_option == "":
                menu_option = 0
            else:
                menu_option = int(menu_option)
            if menu_option not in [0, 1, 2, 3]:
                print("{} no es una opción válida. Inténtelo de nuevo.\n".format(
                    menu_option))

        if menu_option == 1:
            print("\n\n> > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >\n")
            print("\nOpción 1")
            print("\n\n< < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <\n")

        elif opt == 2:
            print("\n\n> > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >\n")
            print("\nOpción 2")
            print("\n\n< < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <\n")

        elif opt == 3:
            print("\n\n> > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >\n")
            print("\nOpción 3")
            print("\n\n< < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <\n")
                
        elif menu_option == 0:
            print("\n¡Saludos!\n")
            endProgram = True

    return

if __name__ == "__main__":
    outputs = menu()