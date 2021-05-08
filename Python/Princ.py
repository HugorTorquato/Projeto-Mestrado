# coding: utf-8
from Definitions import *
import pandas as pd
import matplotlib.pyplot as plt



if __name__ == "__main__":
    print u"""Autor: Hugo Torquato \nData: 24/01/2020 \nE-mail: hugortorquato@gmail.com \n"""

    Rede = DSS("C:\Users\hugo1\Desktop\Rede_03\_trafo3\Master.dss")

    from SistemFunctions import *
    Version(Rede), Compila_DSS(Rede)

    from SistemFunctions import Inicializa
    Inicializa(Rede)

    if Salva_Dados:
        from LevantarDados import *
        Salvar_Dados_Rede(Rede)

    if Criar_GD:
        from Geradores import *
        Adicionar_GDs(Rede)

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



