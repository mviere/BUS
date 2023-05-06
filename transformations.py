"""
\brief 

\authors 

\version 0

\date 06/05/2023
"""
# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constantes import *

# %% 
def DefTableCSV2DF (filename: str) -> pd.DataFrame:
    """
    Requiere: 
    - `import pandas as pd`

    @brief Recibe el nombre 
    

       | Name  | gggggggg   | gggggggg|ggggggggg| gg   |   ggg    |  ggg                  |
       |:------|:----------:|:--------|:--------|:-----:|:--------:|:----------------------|
       | S1    |(value)     |(value)  |(value)  |(value)| (value)  |                       |
       | S2    |(value)     |(value)  |(value)  |(value)| (value)  |-                      |
       | ...   |...         |...      |...      | ...   |  ...     |  ...                  |
       | Sn    |(value)     |(value)  |(value)  |(value)| (value)  | Lbbbbbbbbbbbbbbb      |

    y lo convierte en un DataFrame.

    @param filename (str):    Nombre del archivo 

    @return df_swaths   (pandas.DataFrame):       DataFrame de tabla de definición
    """
    df_deftable = pd.read_csv(filename, header=[0], index_col=0)

    return df_deftable


# Si el archivo ejecutándose como main es este mismo, llamar a la función menu()
if __name__ == "__main__":
    DefTableCSV2DF()