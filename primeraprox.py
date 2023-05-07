"""
\authors 

\brief 

\version 0 hola PI3

\date 06/05/2023
"""
# %%


import numpy as np
import pandas as pd
import transformations as tr

# crear funciones que ingresando parámetros de entrada, ejemplo, cambiar de modo, vaya a la deftable e imprima x pantalla algo.

file_deftable = input(
    "\nIngrese el nombre del archivo de Def. Table de Modos de Operación o presione Enter para archivo default (deftable_modos.csv):  ")
if file_deftable == "":
    file_deftable = "deftable_modos.csv"

df_deftable = tr.DefTableCSV2DF(file_deftable)
print(df_deftable)