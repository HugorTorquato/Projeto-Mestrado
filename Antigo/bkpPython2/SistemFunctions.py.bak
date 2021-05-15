# coding: utf-8
import numpy as np
from Definitions import *
from Geradores import *

def Inicializa(Rede):
    # Essa função é responsável por inicializar alguns os dataframes utilizados

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
    FindBusGD(Num_GDs)


def Version(Rede):
    print Rede.dssObj.Version

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
    from FunctionsSecond import Colunas_DF_Horas, Salvar_e_Limpar_DF
    coll = Colunas_DF_Horas(Rede)
    Nummero_Simulacoes = 0
    Pot_GD = 0

    while (max(DF_Tensao_A.set_index('Barras').max().values) <= 1.05 and
            min(DF_Tensao_A.set_index('Barras').min().values) >= 0.92) or\
            Nummero_Simulacoes == 0:

        # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
        # valores para fazer o código funcionar
        if Criar_GD and Nummero_Simulacoes > 0:
            Compila_DSS(Rede), Salvar_e_Limpar_DF(DF_Geradores), Adicionar_GDs(Rede, Pot_GD)
        else:
            Adicionar_GDs(Rede, Pot_GD)

        Solve_Hora_por_Hora(Rede)        # Chamada da função que levanta o perfil diário

        Nummero_Simulacoes += 1
        Pot_GD += 2
        print '-----------------------------------------------------'
        print max(DF_Tensao_A.set_index('Barras').max().values)
        print min(DF_Tensao_A.set_index('Barras').min().values)
        print '-----------------------------------------------------'

    print DF_Tensao_A
    print 'Número de Simulações : ' + str(Nummero_Simulacoes) + ' Pot GDs : ' + str(Pot_GD)

    # Feature:
    # -> Colocar o cálculo da pertinência triangular aqui, para acontecer logo depois que tiver a violação
