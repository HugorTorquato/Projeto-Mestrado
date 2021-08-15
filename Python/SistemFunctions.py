# coding: utf-8
import numpy as np
from Geradores import *
from DB_Rede import *


def Inicializa(Rede):
    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C
    # Essa função é responsável por inicializar alguns os dataframes utilizados ( Acho quenão preciso )

    # Features:
    # Daria para colocar uma coluna para diferênciar a simulação diária ( primeira, segunda....)( ID da simulação)

    # Dataframe de tensão
    DF_Tensao_A.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_A.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_B.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_B.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_C.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_C.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    # Dataframe de desq de tensão
    DF_Desq_IEC.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_IEC.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Desq_IEEE.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_IEEE.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    DF_Desq_NEMA.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_NEMA.insert(i + 1, str(i), 'TBD') for i in range(Tamanho_pmult(Rede))]

    # Defnição das barras em que os geradores vão estar inseridos no sistema
    # FindBusGD(Num_GDs)


def Version(Rede):
    print(Rede.dssObj.Version)


def Compila_DSS(Rede):
    Rede.dssObj.ClearALL()
    Rede.dssText.Command = "compile " + Rede.Modelo_Barras

    Rede.dssSolution.Solve()


def Nome_Barras(Rede):
    return Rede.dssCircuit.AllBusNames
    # Rede.dssText.Command = "Show power kva elements"
    # Rede.dssText.Command = 'Buscoords BusCoords.csv'
    # Rede.dssText.Command = 'Set NodeWidth=4'
    # Rede.dssText.Command = 'plot circuit Power Max=20 dots=y labels=n subs=n C1=$00FF0000'
    # Rede.dssText.Command = 'Plot type=circuit quantity=1 Max=.001  dots=no  labels=no Object=BusCoords.CSV'


def Tamanho_pmult(Rede):
    Rede.dssLoadShapes.Name = Rede.dssLoadShapes.AllNames[1]
    return len(Rede.dssLoadShapes.pmult)


def Solve_Hora_por_Hora(Rede, Simulation):
    # Essa função é o coração do código, aqui que são feitos todos os comandos e designações para os calculos durante
    # a simulação diária

    # Feature:
    # -> Limitar a simulação diária somente ao pico de geração fotovoltaica ( algumas horas ) = sim. mais rápida
    # -> Salvar no banco os valores obtidos
    #       -> Função para salvar os dados em cada iteração ( Salvar_Dados_Tensao )

    Rede.dssSolution.Number = 1

    # print 'originalsteps : ' + str(originalSteps)
    from FunctionsSecond import Tensao_Barras, originalSteps, Correntes_elementos

    for itera in range(0, originalSteps(Rede)):
        Rede.dssSolution.SolveSnap()

        Tensao_Barras(Rede, itera)
        Correntes_elementos(Rede, itera)

        teste(Rede)

        Rede.dssSolution.FinishTimeStep()

        # Adicionar uma função para salvar o DF e depois zerar ele para a próxima simulação

    # print DF_Tensao_A['0'], DF_Tensao_B['0'], DF_Tensao_C['0']

def teste(Rede):

    a = Rede.dssPVSystems.AllNames
    b = Rede.dssLoadShapes.AllNames
    from FunctionsSecond import ativa_barra
    Rede.dssPVSystems.Name = str(a[1])
    Rede.dssLoadShapes.Name = str(b[7])
    irrad.append(Rede.dssLoadShapes.pmult)
    Pot_PV.append(Rede.dssPVSystems.RegisterValues)
    Pot_PV1.append(Rede.dssPVSystems.kW)
    Pot_PV2.append(Rede.dssPVSystems.kVArated)
    Pot_PV3.append(Rede.dssPVSystems.IrradianceNow)
    Pot_PV4.append(Rede.dssPVSystems.kvar)


def HC(Rede):
    # Essa função é o pulmão do código, aqui que é feito o cálculo do HC
    from FunctionsSecond import Colunas_DF_Horas, Limpar_DF, Check
    from Definitions import Num_GDs, DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_Tensao_A, DF_PV
    from DB_Rede import Save_General_Data, Save_Data, Process_Data

    coll = Colunas_DF_Horas(Rede)

    # [1,2,3,4,5] [[b1,b2,b3], [b1,b2,b3], [b1,b2,b3]]

    # Fazer a combinação e avaliar por zona
    #Barras_GDs = list(combinations(DF_Tensao_A.Barras.values, 3))

    for Simulation in range(1, Num_Simulations + 1):
        print(Num_GDs)

        Nummero_Simulacoes = 0
        Pot_GD = 0

        Compila_DSS(Rede)

        [Limpar_DF(DF) for DF in [DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV]]

        # Define em quais barras as GDs vão ser inseridas para obtenção do HC nessa simulação
        FindBusGD(Num_GDs)

        while Nummero_Simulacoes == 0 or Check() == True:
            # desq
            # corrente

            # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
            # valores para fazer o código funcionar
            if Criar_GD and Nummero_Simulacoes > 0:
                Compila_DSS(Rede), [Limpar_DF(DF) for DF in [DF_Geradores, DF_Elements, DF_PV]]

            Adicionar_GDs(Rede, Pot_GD, Simulation)

            Solve_Hora_por_Hora(Rede, Simulation)  # Chamada da função que levanta o perfil diário

            Nummero_Simulacoes += 1
            Pot_GD += Incremento_gd
            print('-----------------------------------------------------')
            print(max(DF_Tensao_A.set_index('Barras').max().values))
            print(min(DF_Tensao_A.set_index('Barras').min().values))
            print('-----------------------------------------------------')

        Process_Data(Rede, Simulation)
        Save_General_Data(Simulation)
        Save_Data(Simulation)
        print('Número da Simulação : ' + str(Simulation) + ' Pot GDs : ' + str(Pot_GD - Incremento_gd))

    # Feature:
    # -> Colocar o cálculo da pertinência triangular aqui, para acontecer logo depois que tiver a violação
