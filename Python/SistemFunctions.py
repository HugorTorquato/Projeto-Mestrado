# coding: utf-8
import time
import py_dss_interface

from Geradores import *
import time
from multiprocessing import Process

def Inicializa(Rede2):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA,\
        DF_kW_PV, DF_kvar_PV, DF_irradNow_PV, Num_GDs, DF_Tensao_Ang_A, DF_Tensao_Ang_B, \
        DF_Tensao_Ang_C, logger
    from FunctionsSecond import originalSteps

    t1 = time.time()

    # Essa função é responsável por inicializar alguns os dataframes utilizados ( Acho quenão preciso )

    # Dataframe de tensão
    DF_Tensao_A.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_A.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Tensao_B.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_B.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Tensao_C.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_C.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Tensao_Ang_A.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_Ang_A.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Tensao_Ang_B.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_Ang_B.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Tensao_Ang_C.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Tensao_Ang_C.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    # Dataframe de desq de tensão
    DF_Desq_IEC.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Desq_IEC.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Desq_IEEE.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Desq_IEEE.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_Desq_NEMA.insert(0, 'Barras', Nome_Barras(Rede2), allow_duplicates=True)
    [DF_Desq_NEMA.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    PVs = ["PV_" + str(i) for i in range(Num_GDs)]

    DF_kW_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kW_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_kvar_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_kvar_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    DF_irradNow_PV.insert(0, 'PVs', PVs, allow_duplicates=True)
    [DF_irradNow_PV.insert(i + 1, str(i), 0) for i in range(originalSteps(Rede2))]

    logger.debug("Inicializa took {" + str(time.time() - t1) + " sec} to execulte")

def Version(Rede2):
    #print(Rede.dssObj.Version)
    print(Rede2.dss_version())


def Compila_DSS_old(Rede):

    from Definitions import logger
    t1 = time.time()

    Rede.dssObj.ClearALL()
    Rede.dssText.Command = "compile " + Rede.Modelo_Barras
    Rede.dssText.Command = "set mode=daily"
    Rede.dssText.Command = "set stepsize = 15m"
    Rede.dssText.Command = "set number = 96"
    Rede.dssText.Command = "Set voltagebases=[0.22 11.9 0.3811 0.127]"
    Rede.dssText.Command = "Calcvoltagebases"

    Rede.dssSolution.Solve()

    logger.debug('Solve Informations :  Mode=Daily Stepsize=15m Number=96')
    logger.debug("Compila_DSS took {" + str(time.time() - t1) + " sec} to execulte ")

def Compila_DSS(Rede2):

    from Definitions import logger
    t1 = time.time()

    Rede2.dss_clear_all()
    Rede2.text("compile " + Rede_Path + "\Master.dss")
    Rede2.text("set mode=daily")
    Rede2.text("set stepsize = 15m")
    Rede2.text("set number = 96")
    Rede2.text("Set voltagebases=[0.22 11.9 0.3811 0.127]")
    Rede2.text("Calcvoltagebases")
    Rede2.solution_solve()

    logger.debug('Solve Informations2 :  Mode=Daily Stepsize=15m Number=96')
    logger.debug("Compila_DSS took {" + str(time.time() - t1) + " sec} to execulte ")

def Compila_DSS2(Rede2):

    from Definitions import logger
    t1 = time.time()


    Rede2.text("compile " + Rede_Path + "\Master.dss")
    Rede2.text("set mode=daily")
    Rede2.text("set stepsize = 15m")
    Rede2.text("set number = 96")
    Rede2.text("Set voltagebases=[0.22 11.9 0.3811 0.127]")
    Rede2.text("Calcvoltagebases")

    logger.debug('Solve Informations2 :  Mode=Daily Stepsize=15m Number=96')
    logger.debug("Compila_DSS took {" + str(time.time() - t1) + " sec} to execulte ")

def Nome_Barras(Rede2):

   return Rede2.circuit_all_bus_names()
    # Rede.dssText.Command = "Show power kva elements"
    # Rede.dssText.Command = 'Buscoords BusCoords.csv'
    # Rede.dssText.Command = 'Set NodeWidth=4'
    # Rede.dssText.Command = 'plot circuit Power Max=20 dots=y labels=n subs=n C1=$00FF0000'
    # Rede.dssText.Command = 'Plot type=circuit quantity=1 Max=.001  dots=no  labels=no Object=BusCoords.CSV'

def barrr():
    a = 0
    for i in range(100):
        a += 1
        print(a)
        time.sleep(1)

def Solve_Hora_por_Hora(Rede2, Simulation, Pot_GD):
    # Essa função é o coração do código, aqui que são feitos todos os comandos e designações para os calculos durante
    # a simulação diária

    from Definitions import DF_Tensao_A, Savar_Dados_Elem, logger
    from Monitores import Adicionar_Monitores, Export_Random_Monitor_Test, Debug_Loads
    from FunctionsSecond import Adicionar_EnergyMeter, Converter_Intervalo_de_Simulacao

    # Feature:
    # -> Limitar a simulação diária somente ao pico de geração fotovoltaica ( algumas horas ) = sim. mais rápida
    # -> Salvar no banco os valores obtidos
    #       -> Função para salvar os dados em cada iteração ( Salvar_Dados_Tensao )

    #Rede.dssSolution.Number = 1
    #Rede.dssSolution.Number = 1
    Rede2.solution_write_number(1)

    # ----------------------------------------------------------------------------------------------------------
    # A função Compila DSS lê os arquivos .dss e deixa o circuito da forma que que está lá.
    # Para adicionar novos elementos ( Geradores, PVSystem, Medidores... ) tem de ser feito aqui,
    # Essa definição vai ser incluida na definição dos arquivos .dss e computada durante o solve
    # que tem dentro da função "Solve_Hora_por_Hora".
    # OBS: Se definir um DF, lembrar de limpar o mesmo na seção anterior

    Adicionar_GDs(Rede2, Pot_GD, Simulation)
    Adicionar_Monitores(Rede2)

    # ----------------------------------------------------------------------------------------------------------

    from FunctionsSecond import Tensao_Barras, originalSteps, Correntes_elementos, Data_PV


    for itera in range(0, originalSteps(Rede2)):

        # Se acahr uma forma de não precisar fazer o solve das horas fora do intervalo seria lega

        t1 = time.time()
        timekill = 10


        a = Rede2.solution_read_step_size()
        b = Rede2.solution_step_size_min()
        c = Rede2.solution_read_mode()
        d = Rede2.solution_read_number()
        e = Rede2.solution_mode_id()

        aa = Rede2.circuit_all_bus_vmag_pu()[45]
        Rede2.solution_solve()
        aaa = Rede2.circuit_all_bus_vmag_pu()[45]

        f = Rede2.solution_read_step_size()
        g = Rede2.solution_step_size_min()
        h = Rede2.solution_read_mode()
        i = Rede2.solution_read_number()
        j = Rede2.solution_mode_id()

        Rede2.solution_finish_time_step()

        #Rede.dssSolution.Solve()

        #if time.time() - t1 >= timekill - 0.5:
        #    Rede.dssSolution.FinishTimeStep()
        #    logger.info("Deu ruim na iteração timekill =" + str(itera))

        #logger.debug("SolveSnap took {" + str(time.time() - t1) + " sec} to execulte "
        #                                                        "in iteration: " + str(itera))

        #if Converter_Intervalo_de_Simulacao(Rede, Inicio_Sim) <= itera\
        #        <= Converter_Intervalo_de_Simulacao(Rede, Fim_Sim):
        #
        #   # All functions added her will generate a huge impact on performance. Limit this section just for those
        #   # functions related to violation check. Everything else can be measured using monitors.
        #   Tensao_Barras(Rede, itera)
        #   Correntes_elementos(Rede, itera)
        #   Rede.dssText.Command = "Export EventLog"
        #
            # Medição já está sendo feita pelos monitores ( pode remover )
            # Data_PV(Rede, itera)
            # Creio que esses dados já estão sendo salvos pelos monitores, não precisa mais
        #else:
        #    logger.debug("Atuação do limite de simulação")
        #Rede.dssSolution.FinishTimeStep()

def Solve_Daily(Rede2, Simulation, Pot_GD):

    from Definitions import logger
    from FunctionsSecond import CreateFakeLoads
    from Monitores import Adicionar_Monitores

    logger.debug("Starting Solve_Daily")
    t1 = time.time()

    Compila_DSS2(Rede2)
    Adicionar_GDs(Rede2, Pot_GD, Simulation)
    CreateFakeLoads(Rede2)
    Adicionar_Monitores(Rede2)

    #a = Rede2.circuit_all_bus_vmag_pu()
    #aa = Rede2.circuit_all_bus_vmag_pu()
    #bb = Rede2.solution_read_load_mult()
    Rede2.solution_solve()
    #aaa = Rede2.circuit_all_bus_vmag_pu()
    #bbb = Rede2.solution_read_load_mult()
    #ccc = Rede2.loadshapes_read_p_mult()
    #ddd = Rede2.loadshapes_read_time_array()
    #eee = Rede2.loadshapes_read_name()
    #fff = Rede2.loadshapes_all_names()

    teste(Rede2)

    logger.debug("Solve_Daily took {" + str(time.time() - t1) + " sec} to execulte")
    #print()

def teste(Rede2): #00000

    Rede2.loads_first()
    pos = 1
    while pos:
        logger.info(str(Rede2.loads_read_name()) + " khw:" + str(Rede2.loads_read_kwh()))

        pos = Rede2.loads_next()

def HC(Rede2):

    # Essa função é o pulmão do código, aqui que é feito o cálculo do HC
    from FunctionsSecond import Limpar_DF, Check2, GetAllTransfNames, Identify_Overcurrent_Limits
    from Definitions import DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV,\
        DF_Lista_Monitors, Incremento_gd, DF_Monitors_Data_2, Casos, logger, DF_Violations_Data, \
        DF_Corrente_Limite


    # Define o primeiro transformador como o ponto de PCC e o incremento de pot em cada verificação do HC é
    # definido em termos de % frente a pot do trafo de entrada

    #Rede.dssTransformers.Name = Rede.dssTransformers.AllNames[0]
    [Limpar_DF(DF) for DF in [DF_Corrente_Limite]]
    Rede2.transformers_write_name(GetAllTransfNames(Rede2)[0])
    Identify_Overcurrent_Limits(Rede2)
    #a = Rede2.transformers_read_name()
    try:
        #Incremento_Pot_gd = float(Incremento_gd)/100 * Rede.dssTransformers.kva
        Incremento_Pot_gd = float(Incremento_gd)/100 * Rede2.transformers_read_kva()
    except:
        Incremento_Pot_gd = 0.025

    Sem_GD = 0
    rest = 0

    for Simulation in range(1, Num_Simulations + 1):

        Nummero_Simulacoes = 0

        # This will make sure the default condition, without PV, will be execulted only once.
        # There is no need to run this condition for each case of study because the result is the same

        # Por algum motivo deu erro de convergência nos inversores se plar o primeiro caso
        # mas também mudei o delta da simulação.... mais um teste para ver
        #if (len(Casos) if Casos != [] else 0) != 1 and Simulation == 1:
        #    logger.info("Default Case already tested - First simulation")
        #    continue

        if Simulation == 5 or Simulation == 7:
            # Save the last Pot reference value to run the simulation again without VW
            Pot_GD -= 2*Incremento_Pot_gd if Criar_GD else 0
        else:
            Pot_GD = 0 if Sem_GD == 0 else 1

        Compila_DSS(Rede2)

        [Limpar_DF(DF) for DF in [DF_Geradores, DF_Barras, DF_General, DF_Elements, DF_PV,
                                  DF_Lista_Monitors, DF_Monitors_Data_2, DF_Violations_Data]]
        Verify = True

        while Nummero_Simulacoes == 0 or Verify is True:

            logger.info("Starting Case " + str(len(Casos) if Casos != [] else 0) +
                        " simulation " + str(Simulation) + " Iteração " + str(Nummero_Simulacoes))
            #print("Starting Case " + str(len(Casos) if Casos != [] else 0) +
            #      " simulation " + str(Simulation) + " Iteração " + str(Nummero_Simulacoes))

            # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
            # valores para fazer o código funcionar
            if Criar_GD and Nummero_Simulacoes > 0:
                Compila_DSS(Rede2)
                [Limpar_DF(DF) for DF in [DF_Geradores, DF_Elements, DF_PV, DF_Lista_Monitors]]

            # trocar .insert por .concat ( primeiro tem performance ruim )
            Solve_Daily(Rede2, Simulation, Pot_GD)
            #Solve_Hora_por_Hora(Rede2, Simulation, Pot_GD)  # Chamada da função que levanta o perfil diário


            Nummero_Simulacoes += 1
            rest += 1
            Verify = Check2(Rede2, Simulation)
            #Verify = Check(Rede, Simulation)

            if Nummero_Simulacoes < 4:
                Pot_GD += 3*Incremento_Pot_gd if Criar_GD and Nummero_Simulacoes > 0 else 0
            else:
                Pot_GD += Incremento_Pot_gd if Criar_GD and Nummero_Simulacoes > 0 else 0

            if Simulation in [1, 5, 7]:
                Sem_GD = 1
                break

            # Creio que n preciso disso aqui, redundante
            if Simulation == 1:
                Sem_GD = 1
                break

            if Nummero_Simulacoes > 30:
                Verify = False
                break

        # Step Back
        Reduction = Incremento_Pot_gd if Criar_GD and Nummero_Simulacoes > 0 else 0
        Pot_GD -= Reduction
        logger.info("Redução de : " + str(Reduction))
        logger.info("Starting Step Back " + str(len(Casos) if Casos != [] else 0) +
                    " simulation " + str(Simulation) + " Iteração " + str(Nummero_Simulacoes))
        #print("Starting Case " + str(len(Casos) if Casos != [] else 0) +
        #      " simulation " + str(Simulation) + " Iteração " + str(Nummero_Simulacoes))

        # Confere se a definição para adicionar GHD está ativa e se não for a primeira simulação, reseta os devidos
        # valores para fazer o código funcionar
        if Criar_GD and Nummero_Simulacoes > 0:
            Compila_DSS2(Rede2)
            [Limpar_DF(DF) for DF in [DF_Geradores, DF_Elements, DF_PV, DF_Lista_Monitors]]

        # trocar .insert por .concat ( primeiro tem performance ruim )
        #Solve_Hora_por_Hora(Rede, Simulation, Pot_GD)  # Chamada da função que levanta o perfil diário
        Solve_Daily(Rede2, Simulation, Pot_GD)

        from Monitores import Export_And_Read_Monitors_Data2
        from DB_Rede import Save_General_Data, Save_Data

        DF_Monitors_Data_2 = Export_And_Read_Monitors_Data2(Rede2, Simulation)
        #DF_Monitors_Data_2 = Export_And_Read_Monitors_Data(Rede, Simulation)

        Save_General_Data(Simulation)
        #Process_Data(Simulation, DF_Monitors_Data_2)
        Save_Data(DF_Monitors_Data_2)

        print('Caso=' + str(len(Casos) if Casos != [] else 0) + ' Número da Simulação : ' +
              str(Simulation) + " Número de iterações : " + str(Nummero_Simulacoes) +
              ' Pot GDs : ' + str(Pot_GD - Incremento_Pot_gd))

def Case_by_Case(Rede2):

    # Essa função é responsável por definir cada estudo de caso que será feito. A variável "Num_Estudos_de_Caso"
    # controla a quantidade de estudos de caso que serão performados ( configurações de GDs ). Para cada caso, podem
    # ser configuradas 4 tipos de simulações ( controladas pela variável Num_Simulações ), sendo:
    # 1 - Sem PV
    # 2 - Com PV FP=1
    # 3 - Com PV + VV
    # 4 - Com PV + VW
    # 5 - Com PV
    # 6 - Com PV + VV + VW
    # 7 - Com PV + VV
    #

    from Definitions import Num_GDs, Casos
    from Geradores import FindBusGD

    for Caso in range(Num_Estudos_de_Caso):
        Casos.append(Caso + 1)
        FindBusGD(Rede2, Num_GDs)
        HC(Rede2)
