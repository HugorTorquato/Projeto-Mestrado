# coding: utf-8
from Geradores import *

def Inicializa(Rede):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA,\
        DF_PVPowerData, DF_kW_PV, DF_kvar_PV, DF_irradNow_PV, Num_GDs
    from FunctionsSecond import originalSteps

    # Essa função é responsável por inicializar alguns os dataframes utilizados ( Acho quenão preciso )

    # Dataframe de tensão
    DF_Tensao_A.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_A.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_B.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_B.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    DF_Tensao_C.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Tensao_C.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    # Dataframe de desq de tensão
    DF_Desq_IEC.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_IEC.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    DF_Desq_IEEE.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_IEEE.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    DF_Desq_NEMA.insert(0, 'Barras', Nome_Barras(Rede), allow_duplicates=True)
    [DF_Desq_NEMA.insert(i + 1, str(i), 0) for i in range(Tamanho_pmult(Rede))]

    [DF_PVPowerData.insert(i + 4, "Time_" + str(i), 0) for i in range(originalSteps(Rede))]

    PVs = ["PV_" + str(i) for i in range(Num_GDs)]

    DF_kW_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kW_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede))]

    DF_kvar_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kvar_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede))]

    DF_irradNow_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_irradNow_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede))]

    # Defnição das barras em que os geradores vão estar inseridos no sistema
    # FindBusGD(Num_GDs)

def Version(Rede):
    print(Rede.dssObj.Version)

def Compila_DSS(Rede):
    Rede.dssObj.ClearALL()
    Rede.dssText.Command = "compile " + Rede.Modelo_Barras
    Rede.dssText.Command = "set mode=daily"
    Rede.dssText.Command = "set stepsize = 15m"
    Rede.dssText.Command = "set number = 96"

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

def Solve_Hora_por_Hora(Rede, Simulation, Pot_GD):
    # Essa função é o coração do código, aqui que são feitos todos os comandos e designações para os calculos durante
    # a simulação diária

    from Monitores import Adicionar_Monitores
    from FunctionsSecond import Adicionar_EnergyMeter, Converter_Intervalo_de_Simulacao

    # Feature:
    # -> Limitar a simulação diária somente ao pico de geração fotovoltaica ( algumas horas ) = sim. mais rápida
    # -> Salvar no banco os valores obtidos
    #       -> Função para salvar os dados em cada iteração ( Salvar_Dados_Tensao )

    Rede.dssSolution.Number = 1

    # ----------------------------------------------------------------------------------------------------------
    # A função Compila DSS lê os arquivos .dss e deixa o circuito da forma que que está lá.
    # Para adicionar novos elementos ( Geradores, PVSystem, Medidores... ) tem de ser feito aqui,
    # Essa definição vai ser incluida na definição dos arquivos .dss e computada durante o solve
    # que tem dentro da função "Solve_Hora_por_Hora".
    # OBS: Se definir um DF, lembrar de limpar o mesmo na seção anterior

    Adicionar_GDs(Rede, Pot_GD, Simulation)
    Adicionar_EnergyMeter(Rede)
    Adicionar_Monitores(Rede)

    # ----------------------------------------------------------------------------------------------------------

    from FunctionsSecond import Tensao_Barras, originalSteps, Correntes_elementos, Data_PV

    for itera in range(0, originalSteps(Rede)):

        # Se acahr uma forma de não precisar fazer o solve das horas fora do intervalo seria lega

        Rede.dssSolution.SolveSnap()

        if Converter_Intervalo_de_Simulacao(Rede, Inicio_Sim) <= itera\
                <= Converter_Intervalo_de_Simulacao(Rede, Fim_Sim):

            Tensao_Barras(Rede, itera)
            Correntes_elementos(Rede, itera)
            Data_PV(Rede, itera)

        Rede.dssSolution.FinishTimeStep()

    print(DF_Tensao_A.head())

def HC(Rede):

    # Adicionar uma simulação padrão apra salvar os valores sem interferência das GDs

    # Essa função é o pulmão do código, aqui que é feito o cálculo do HC
    from FunctionsSecond import Limpar_DF, Check, Identify_Overcurrent_Limits, \
        Max_and_Min_Voltage_DF
    from Definitions import Num_GDs, DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV,\
        DF_PVPowerData, DF_Lista_Monitors, DF_Tensao_A, DF_Tensao_B, DF_Tensao_C
    from Geradores import FindBusGD

    # Define o primeiro transformador como o ponto de PCC e o incremento de pot em cada verificação do HC é
    # definido em termos de % frente a pot do trafo de entrada

    Rede.dssTransformers.Name = Rede.dssTransformers.AllNames[0]
    Incremento_Pot_gd = float(Incremento_gd)/100 * Rede.dssTransformers.kva

    Identify_Overcurrent_Limits(Rede)

    Sem_GD = 0

    for Simulation in range(1, Num_Simulations + 1):

        Nummero_Simulacoes = 0
        Pot_GD = 0 if Sem_GD == 0 else 1

        Compila_DSS(Rede)

        [Limpar_DF(DF) for DF in [DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV, DF_PVPowerData,
                                  DF_Lista_Monitors, DF_PVPowerData]]

        FindBusGD(Num_GDs) # Define em quais barras as GDs vão ser inseridas para obtenção do HC nessa simulação

        while Nummero_Simulacoes == 0 or Check(Rede, Simulation) is True:

            # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
            # valores para fazer o código funcionar
            if Criar_GD and Nummero_Simulacoes > 0:
                Compila_DSS(Rede)
                [Limpar_DF(DF) for DF in [DF_Geradores, DF_Elements, DF_PV, DF_Lista_Monitors, DF_PVPowerData]]

            Solve_Hora_por_Hora(Rede, Simulation, Pot_GD)  # Chamada da função que levanta o perfil diário

            Nummero_Simulacoes += 1
            Pot_GD += Incremento_Pot_gd if Criar_GD and Nummero_Simulacoes > 0 else 0

            print('-----------------------------------------------------')
            #print(DF_Tensao_A.head())
            print(float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]))
            print(float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]))
            print('-----------------------------------------------------')

            if Sem_GD == 0:
                print('--------------------- S/ GD -------------------------')
                print('-----------------------------------------------------')
                Sem_GD = 1
                break

        from Monitores import Export_And_Read_Monitors_Data
        from FunctionsSecond import Power_measurement_PV
        from DB_Rede import Save_General_Data, Save_Data, Process_Data
        from Definitions import DF_Lista_Monitors

        Export_And_Read_Monitors_Data(Rede, DF_Lista_Monitors, Simulation)
        Power_measurement_PV(Rede, Simulation)
        DF_Voltage_Data, DF_Corrente_Data = Process_Data(Rede, Simulation)
        Save_General_Data(Simulation)
        Save_Data(Simulation, DF_Voltage_Data, DF_Corrente_Data)

        # Olhar isso aqui direito... parece que n está computando o valor limite certinho
        # Apresenta o valor de pot já com a violação
        #Pot_GD = Incremento_Pot_gd if Pot_GD == 0 else Pot_GD

        print('Número da Simulação : ' + str(Simulation) + ' Pot GDs : ' + str(Pot_GD - Incremento_Pot_gd))

        # Feature:
        # -> Colocar o cálculo da pertinência triangular aqui, para acontecer logo depois que tiver a violação
