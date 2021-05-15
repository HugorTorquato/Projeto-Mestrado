# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    print("""Autor: Hugo Torquato \nData: 24/01/2020 \nE-mail: hugortorquato@gmail.com \n""")

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    sqlalchemyVersion()

    Rede = DSS("C:\\Users\hugo1\Desktop\Rede_03\_trafo3\Master.dss")

    Version(Rede), Compila_DSS(Rede), Inicializa(Rede)

    if Salva_Dados:
        Salvar_Dados_Rede(Rede)

    if Calc_HC:
        HC(Rede)
    else:
        Solve_Hora_por_Hora(Rede)

    #print DF_Tensao_A.head()
    #from FunctionsSecond import Colunas_DF_Horas

    #print DF_Tensao_A.set_index('Barras').head()

    #plt.figure(1)
    #[DF_Tensao_A.set_index('Barras')[coll].plot(figsize=(16, 8), kind='bar', color='black') for coll in ['48']]
    #plt.xticks(rotation=45), plt.ylim([0.9, 1.05]), plt.grid()

    #plt.figure(2)
    #print 'hugo'
    #print DF_Tensao_A.set_index('Barras').iloc[3:5]
    #DF_Tensao_A.set_index('Barras').iloc[4].plot(figsize=(16, 8), linewidth=4)
    #plt.ylim([0.9, 1.05]), plt.grid()

    #plt.show()