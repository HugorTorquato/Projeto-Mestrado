# coding: utf-8
from Geradores import *

def Inicializa(Rede):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA,\
        DF_PVPowerData, DF_kW_PV, DF_kvar_PV, DF_irradNow_PV, Num_GDs
    from FunctionsSecond import originalSteps

    # Essa função é responsável por inicializar alguns os dataframes utilizados ( Acho quenão preciso )

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

    [DF_PVPowerData.insert(i + 4, "Time_" + str(i), 0) for i in range(originalSteps(Rede))]

    PVs = ["PV_" + str(i) for i in range(Num_GDs)]

    DF_kW_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kW_PV.insert(i + 1, str(i), 'TBD') for i in range(originalSteps(Rede))]

    DF_kvar_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kvar_PV.insert(i + 1, str(i), 'TBD') for i in range(originalSteps(Rede))]

    DF_irradNow_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_irradNow_PV.insert(i + 1, str(i), 'TBD') for i in range(originalSteps(Rede))]


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

    from FunctionsSecond import Tensao_Barras, originalSteps, Correntes_elementos, Data_PV

    for itera in range(0, originalSteps(Rede)):
        Rede.dssSolution.SolveSnap()

        Tensao_Barras(Rede, itera)
        Correntes_elementos(Rede, itera)
        Data_PV(Rede, itera)

        Rede.dssSolution.FinishTimeStep()

        # Adicionar uma função para salvar o DF e depois zerar ele para a próxima simulação

    # print DF_Tensao_A['0'], DF_Tensao_B['0'], DF_Tensao_C['0']

def HC(Rede):

    # Essa função é o pulmão do código, aqui que é feito o cálculo do HC
    from FunctionsSecond import Colunas_DF_Horas, Limpar_DF, Check, Power_measurement_PV, \
        Adicionar_EnergyMeter
    from Definitions import Num_GDs, DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_Tensao_A, DF_PV,\
        DF_PVPowerData
    from DB_Rede import Save_General_Data, Save_Data, Process_Data

    coll = Colunas_DF_Horas(Rede)

    # [1,2,3,4,5] [[b1,b2,b3], [b1,b2,b3], [b1,b2,b3]]

    # Fazer a combinação e avaliar por zona
    #Barras_GDs = list(combinations(DF_Tensao_A.Barras.values, 3))

    for Simulation in range(1, Num_Simulations + 1):

        Nummero_Simulacoes = 0
        Pot_GD = 0

        Compila_DSS(Rede)

        [Limpar_DF(DF) for DF in [DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV, DF_PVPowerData]]

        # Define em quais barras as GDs vão ser inseridas para obtenção do HC nessa simulação
        FindBusGD(Num_GDs)

        while Nummero_Simulacoes == 0 or Check() == True:

            # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
            # valores para fazer o código funcionar
            if Criar_GD and Nummero_Simulacoes > 0:
                Compila_DSS(Rede)
                [Limpar_DF(DF) for DF in [DF_Geradores, DF_Elements, DF_PV]]

            # ----------------------------------------------------------------------------------------------------------
            # A função Compila DSS lê os arquivos .dss e deixa o circuito da forma que que está lá.
            # Para adicionar novos elementos ( Geradores, PVSystem, Medidores... ) tem de ser feito aqui,
            # Essa definição vai ser incluida na definição dos arquivos .dss e computada durante o solve
            # que tem dentro da função "Solve_Hora_por_Hora".
            # OBS: Se definir um DF, lembrar de limpar o mesmo na seção anterior

            Adicionar_GDs(Rede, Pot_GD, Simulation)
            Adicionar_EnergyMeter(Rede)

            # ----------------------------------------------------------------------------------------------------------

            Solve_Hora_por_Hora(Rede, Simulation)  # Chamada da função que levanta o perfil diário

            Nummero_Simulacoes += 1
            Pot_GD += Incremento_gd
            print('-----------------------------------------------------')
            print(max(DF_Tensao_A.set_index('Barras').max().values))
            print(min(DF_Tensao_A.set_index('Barras').min().values))
            print('-----------------------------------------------------')

        Power_measurement_PV(Rede, Simulation)
        Process_Data(Rede, Simulation)
        Save_General_Data(Simulation)
        Save_Data(Simulation)
        print('Número da Simulação : ' + str(Simulation) + ' Pot GDs : ' + str(Pot_GD - Incremento_gd))

    # Feature:
    # -> Colocar o cálculo da pertinência triangular aqui, para acontecer logo depois que tiver a violação
