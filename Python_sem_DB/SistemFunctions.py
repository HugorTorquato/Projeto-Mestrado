# coding: utf-8
import numpy as np
from Definitions import *
from Geradores import *
from DB_Rede import *
from FunctionsSecond import *

def Inicializa(Rede):
    # Essa função é responsável por inicializar alguns os dataframes utilizados ( Acho quenão preciso )

    # Features:
    # Daria para colocar uma coluna para diferênciar a simulação diária ( primeira, segunda....)( ID da simulação)

    # Dataframe de tensão
    DF_Tensao_A.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_A.insert(i+1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_B.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_B.insert(i+1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_C.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_C.insert(i+1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    # Defnição das barras em que os geradores vão estar inseridos no sistema
    #FindBusGD(Num_GDs)


def Version(Rede):
    print(Rede.dssObj.Version)

def Compila_DSS(Rede):
    Rede.dssObj.ClearALL()
    Rede.dssText.Command = "compile " + Rede.Modelo_Barras

    Rede.dssSolution.Solve()

def Nome_Barras(Rede):
    return Rede.dssCircuit.AllBusNames
    #Rede.dssText.Command = "Show power kva elements"
    #Rede.dssText.Command = 'Buscoords BusCoords.csv'
    #Rede.dssText.Command = 'Set NodeWidth=4'
    #Rede.dssText.Command = 'plot circuit Power Max=20 dots=y labels=n subs=n C1=$00FF0000'
    #Rede.dssText.Command = 'Plot type=circuit quantity=1 Max=.001  dots=no  labels=no Object=BusCoords.CSV'

def Tamanho_pmult(Rede):
    Rede.dssLoadShapes.Name = Rede.dssLoadShapes.AllNames[1]
    return len(Rede.dssLoadShapes.pmult)

def Solve_Hora_por_Hora(Rede):
    # Essa função é o coração do código, aqui que são feitos todos os comandos e designações para os calculos durante
    # a simulação diária

    # Feature:
    # -> Limitar a simulação diária somente ao pico de geração fotovoltaica ( algumas horas ) = sim. mais rápida
    # -> Salvar no banco os valores obtidos
    #       -> Função para salvar os dados em cada iteração ( Salvar_Dados_Tensao )

    Rede.dssSolution.Number = 1

    #print 'originalsteps : ' + str(originalSteps)
    from FunctionsSecond import Tensao_Barras, originalSteps

    for itera in range(0, originalSteps(Rede)):

        Rede.dssSolution.SolveSnap()
        Tensao_Barras(Rede, itera)

        Rede.dssSolution.FinishTimeStep()


        # Adicionar uma função para salvar o DF e depois zerar ele para a próxima simulação

    #print DF_Tensao_A['0'], DF_Tensao_B['0'], DF_Tensao_C['0']

def HC(Rede):
    # Essa função é o pulmão do código, aqui que é feito o cálculo do HC
    from FunctionsSecond import Colunas_DF_Horas, Limpar_DF, Max_and_Min_Voltage_DF
    coll = Colunas_DF_Horas(Rede)

    for Simulation in range(1, Num_Simulations + 1):
        print(Num_GDs)

        Nummero_Simulacoes = 0
        Pot_GD = 0

        Compila_DSS(Rede), Limpar_DF(DF_Geradores)  # Resetar os valores dos DF

        while Nummero_Simulacoes == 0 or \
                (float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]) <= 1.05 and
                float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]) >= 0.92):

            # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
            # valores para fazer o código funcionar
            if Criar_GD and Nummero_Simulacoes > 0:
                Compila_DSS(Rede), Limpar_DF(DF_Geradores), Adicionar_GDs(Rede, Pot_GD, Simulation)
            else:
                Adicionar_GDs(Rede, Pot_GD, Simulation)

            Solve_Hora_por_Hora(Rede)        # Chamada da função que levanta o perfil diário

            Nummero_Simulacoes += 1
            Pot_GD += 1
            #print('-----------------------------------------------------')
            #print(max(DF_Tensao_A.set_index('Barras').max().values))
            #print(min(DF_Tensao_A.set_index('Barras').min().values))
            #print('-----------------------------------------------------')

        #print(DF_Tensao_C)
        Save_General_Data(Simulation)
        Save_Data(Simulation)
        print('Número da Simulação : ' + str(Simulation) + ' Pot GDs : ' + str(Pot_GD))

    # Feature:
    # -> Colocar o cálculo da pertinência triangular aqui, para acontecer logo depois que tiver a violação

def Save_General_Data(Simulation):

    Limpar_DF(DF_General)
    DF_General.loc[0, 'Voltage_Max'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]
    DF_General.loc[0, 'Voltage_Min'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]
    DF_General.loc[0, 'GD_Config'] = str(DF_Geradores.set_index('Name').values)