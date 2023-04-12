# coding: utf-8
from Definitions import *
import pandas as pd
import random2

def Adicionar_GDs(Rede2, Pot_GD, Simulation):

    from Definitions import FP, Num_GDs, logger
    from FunctionsSecond import originalSteps

    STEPS = originalSteps(Rede2)
    Shapes = []
    logger.debug("Adicionar_GDs - Num. Steps = " + str(STEPS))

    # A ideia é carregar os loadshapes e criar os geradores de acordo com a demanda de geradores a serem inseridos.
    # No momento existem 6 possíveis geradores, limitação pelo número de curvas de cargas adicionadas na pasta
    # de loadShapes. Para elevar esse número basta adicionar mais curvas

    # A definição do valor de potência é feita pela função HC. A cada tentativa as GDs são redefinidas e o valor de
    # Pot_GD é atualizado
    limitation = 0
    for i in range(Num_GDs):

        # Para tirar esse limitador tem de adicionar mais curvas de cargas para PV
        limitation = random2.choice([j for j in range(6)]) if i > 5 else i

        Shapes.append("New LoadShape._GD_" + str(limitation+1) + " npts=" + str(STEPS) + " minterval=15 "
                               "pmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_"
                               + str(limitation+1) + ".txt) "
                               "qmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_"
                               + str(limitation+1) + ".txt)")

    # Criação das curvas do pv
    Shapes.append("New XYCurve.FatorPvsT npts=4 xarray=[0 25 75 100] yarray=[1.2 1.0 .8 .6]")
    Shapes.append("New XYCurve.Eff npts=4 xarray=[.1 .2 .4 1.0] yarray=[.86 .9 .93 .97]")
    Shapes.append("New TShape.Temp npts=96 minterval=15 "
                           "temp=(File=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Temp.txt)")
    Shapes.append("New LoadShape.irrad npts=96 minterval=15 "
                           "mult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Irrad.txt)")
    #Shapes.append("New XYcurve.vv_curve npts=4 Xarray=(0.5,0.89,0.96,1,1.02,1.1,1.5) "
    Shapes.append("New XYcurve.vv_curve npts=5 Xarray=(0.92, 0.99, 1, 1.01, 1.05) "
                           "Yarray=(1.0, 0, 0, 0, -1.0)")
    #Shapes.append("New XYcurve.vw_curve npts=4 yarray=[1 1 0.90 0.85 0.8] xarray=[0.8 1 1.01 1.05 1.5]")

    #  Fazer um estudo para avaliar o nível de redução da pot ativa
    Shapes.append("New XYcurve.vw_curve npts=4 yarray=(1 1 0.50 0.50) xarray=(0.8 1.03 1.05 2)")

    for shape in Shapes:
        #Rede.dssText.Command = shape
        Rede2.text(shape)
        logger.debug("Adicionar_GDs - Shape was created : " + str(shape))

    if Use_PV:
        # adicionar compilaçãoem paralelo aqui
        [Create_PV(Rede2, 'PV_' + str(i), Pot_GD, FP, 'Irrad', 'Temp', Simulation) for i in range(Num_GDs)]
        #print(DF_PV.head(10))# Printa os dados gerais das GDs ( resumo )
    else:
        # Ainda n foi migrado para nova dll
        [Create_GD(Rede2, 'GD_' + str(i), Pot_GD, 0, '_GD_' + str(i + 1), Simulation) for i in range(Num_GDs)]


def Create_PV(Rede2, Nome, Pmp, FP, Irrad, Temp, Simulation):

    from Definitions import DF_PV, Barras_GDs, Casos, logger, sqrt3
    from FunctionsSecond import ativa_barra, Identify_Phases, Fase2String
    from Monitores import Define_Random_Monior_Test

    index = len(DF_PV)
    STRING = ['A', 'B', 'C', 'N']
    invcontrol = 0

    DF_PV.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
    DF_PV.loc[index, 'Simulation'] = Simulation
    DF_PV.loc[index, 'Name'] = str("PVSystem." + Nome).lower()
    DF_PV.loc[index, 'Bus'] = Barras_GDs[(len(Barras_GDs) - 1) - index]

    ativa_barra(Rede2, str(DF_PV.loc[index, 'Bus']))

    DF_PV.loc[index, 'Pmp'] = Pmp * 1.05
    DF_PV.loc[index, 'kW'] = 0   #Definir função para coletar pot gerada
    DF_PV.loc[index, 'kvar'] = 0
    DF_PV.loc[index, 'kva'] = 0
    DF_PV.loc[index, 'FP'] = FP
    #DF_PV.loc[index, 'Phases'] = Fase2String([STRING[i - 1] for i in Rede.dssBus.Nodes])
    DF_PV.loc[index, 'Phases'] = Fase2String([STRING[i - 1] for i in Rede2.bus_nodes()])
    DF_PV.loc[index, 'Irrad'] = Irrad
    DF_PV.loc[index, 'Temp'] = Temp

    kvbase = 0.220

    #if Rede.dssBus.NumNodes == 2:
    if Rede2.bus_num_nodes() == 2:
        kvbase = kvbase/sqrt3

    Identify_Phases0 =Identify_Phases(DF_PV.loc[index, 'Phases'])[0]
    Identify_Phases1 = Identify_Phases(DF_PV.loc[index, 'Phases'])[1]

    # Pmpp - Potência nominal para 1kw/m^2 ( tem de incrementar essa variável )
    # kva - pot nom inversor - Pot gerada n pode ser maior
    # pot dc = ppmppx x irrad x (1-irrad_tempo) x temp_por_pot
    # pot ac = pot dc x eff

    Command = "New PVSystem." + Nome + " phases=" + \
                           str(Identify_Phases1) + \
                           " bus1=" + str(DF_PV.loc[index, 'Bus']) + \
                           str(Identify_Phases0) + \
                           " Pmpp=" + str(Pmp) +  \
                           " kv=" + str(kvbase) + \
                           " kVA=" + str(Pmp * 1.05) + \
                           " con=wye EffCurve=Eff" + \
                           " %Cutin=0.1 %cutout=0.1 P-TCurve=FactorPVsT" + \
                           " pf=1 VarFollowInverter=true" + \
                           " irradiance=" + str(Const_Irrad) + " temperature=" + str(Const_Temp) + \
                           " daily=irrad Tdaily=Temp wattpriority=yes"

    Command + " debugtrace=yes" if Debug else 0

    logger.debug("Create_PV - " + Command)
    #Rede.dssText.Command = Command
    Rede2.text(Command)
    Rede2.text("set maxcontroliter=2000")
    #Rede.dssText.Command = "set maxcontroliter=2000"



    if (Simulation == 3 or Simulation == 7) and Debug_VV == 1:

        Command ="New InvControl.InvPVCtrl_" + Nome + " DERList=PVSystem." + Nome + \
                           " mode=VOLTVAR voltage_curvex_ref=rated" +\
                           " vvc_curve1=vv_curve " \
                           " varchangetolerance=0.5 voltagechangetolerance=0.01" +\
                           " deltaQ_factor=-1 RefReactivePower=VARAVAL" + \
                           " monVoltageCalc=AVG"# EventLog=yes"
        logger.debug("Create_PV - Define InvControl VV " + Command)
        Rede2.text(Command)
        invcontrol = 1

    if Simulation == 4 and Debug_VV == 1:

        Command ="New InvControl.InvPVCtrl_" + Nome + " DERList=PVSystem." + Nome + \
                              " mode=VOLTWATT voltage_curvex_ref=rated" +\
                              " voltwatt_curve=vw_curve DeltaP_factor=-1" +\
                              " VoltwattYAxis=PAVAILABLEPU " + \
                              " varchangetolerance=0.5 voltagechangetolerance=0.01" + \
                              " monVoltageCalc=AVG"# EventLog=yes"
        logger.debug("Create_PV - Define InvControl VW " + Command)
        Rede2.text(Command)
        invcontrol = 1

    if Simulation == 6 and Debug_VV == 1:

        Command ="New InvControl.InvPVCtrl_" + Nome + " DERList=PVSystem." + Nome + \
                 " Combimode=VV_VW voltage_curvex_ref=rated" \
                 " vvc_curve1=vv_curve" + \
                 " deltaQ_factor=-1 RefReactivePower=VARAVAL" \
                 " voltwatt_curve=vw_curve DeltaP_factor=-1" \
                 " VoltwattYAxis=PAVAILABLEPU " + \
                 " varchangetolerance=0.5 voltagechangetolerance=0.01" + \
                 " monVoltageCalc=AVG"# EventLog=yes"
        logger.debug("Create_PV - Define InvControl VV + VW " + Command)
        Rede2.text(Command)
        invcontrol = 1

    ## deltaQ_factor -> Mudança máxima da pot reativa da solução anterior para a desejada durante
    #                   cada iteração de controle
    ## RefReactivePower -> Limita a saída de pot reativa ao limite dsponível no inversor, caso seja requisitado
    #                       mais que o kva permitido, o kvar vai ser limitado
    ## varchangetolerence -> Diferença entre o pot reativa desejada para a obtida. Um dos parâmetrso que limita
    #                        o número de iterações feita por cada controle
    ## maxcontroliter -> Número máximo de iterações por controle, default é 15. Um número baixo pode não ser
    #                    suficiente e, casos mais complesxo de multiplos GDs

    # Define um monitor para observar as configurações do PV durante o InvControl
    if invcontrol:
        Define_Random_Monior_Test(Rede2, "InvControl", "PVSystem." + Nome, 1, 3)

def Create_GD(Rede, Nome, kW, kvar, LoadShape, Simulation):
    from Definitions import DF_Geradores, Barras_GDs, Casos
    from FunctionsSecond import ativa_barra, Identify_Phases, Fase2String

    # Preparação para armazenamento dos dados
    index = len(DF_Geradores)  # Define a linha para aplicar as alterações
    STRING = ['A', 'B', 'C', 'N']  # Definie a string de fases para o gerador


    # Armazenar e salvar dados
    DF_Geradores.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
    DF_Geradores.loc[index, 'Simulation'] = Simulation
    DF_Geradores.loc[index, 'Name'] = Nome
    DF_Geradores.loc[index, 'Bus'] = Barras_GDs[(len(Barras_GDs) - 1) - index]
    DF_Geradores.loc[index, 'kW'] = kW
    DF_Geradores.loc[index, 'kvar'] = kvar

    ativa_barra(Rede, str(DF_Geradores.loc[index, 'Bus']))
    DF_Geradores.loc[index, 'Phases'] = Fase2String([STRING[i - 1] for i in Rede.dssBus.Nodes])
    DF_Geradores.loc[index, 'LoadShape'] = LoadShape

    # Criação da GD no Opendss
    Rede.dssText.Command = "new generator.GD_" + str(index + 1) + " phases=" + \
                           str(Identify_Phases(DF_Geradores.loc[index, 'Phases'])[1]) + \
                           " bus1=" + str(DF_Geradores.loc[index, 'Bus'] +
                           Identify_Phases(DF_Geradores.loc[index, 'Phases'])[0]) + \
                           " kv=" + str(Rede.dssBus.kVBase) + " kW=" + str(kW) + \
                           " kVAr=" + str(kvar + 0.001) + " model=1" + \
                           " daily=" + str(LoadShape)

def FindBusGD(Rede2, Num_GDs):

    from Definitions import Barras_GDs, Debug_VV, logger
    from FunctionsSecond import GetAllLoadsNames

    if Debug_VV == 3000000000000000:
        #Barras_GDs_list = ['bus_33998182_039']#, 'bus_33998182_011',
            # 'bus_33998182_013', 'bus_33998182_027', 'bus_33998182_022']
        Barras_GDs_list = ['bus_33998182_039', 'bus_33998182_011', 'bus_33998182_013',
                         'bus_33998182_027', 'bus_33998182_022']

        #3f - undervoltage com VV
        Barras_GDs_list = ['bus_33998182_017', 'bus_33998182_011', 'bus_33998182_020',
                           'bus_33998182_021', 'bus_33998182_023']

        #1f - undervoltage com VV
        Barras_GDs_list = ['bus_33998182_015', 'bus_33998182_011', 'bus_33998182_032',
                           'bus_33998182_037', 'bus_33998182_027']

        Barras_GDs_list = ['bus_33998182_015', 'bus_33998182_011', 'bus_33998182_025',
                           'bus_33998182_037', 'bus_33998182_026']

        for i in range(Num_GDs):
            Barras_GDs.append(Barras_GDs_list[i])

        return

    if Thiago == 1:
        Barras_GDs_list = ["bus_33998182_015", "bus_33998182_018", "bus_33998182_022",
                           "bus_33998182_013", "bus_33998182_025", "bus_33998182_030",
                           "bus_33998182_031", "bus_33998182_032", "bus_33998182_033"]

        for i in range(Num_GDs):
            Barras_GDs.append(Barras_GDs_list[i])
        return

    vet_choice = []
    #for load in Rede.dssLoads.AllNames:
    for load in GetAllLoadsNames(Rede2):
        Rede2.loads_write_name(load)
        a = Rede2.cktelement_read_bus_names()
        Bus = str(Rede2.cktelement_read_bus_names()[0]).split('.')[0]
        if not Bus.startswith("bus_xfmr"):
            vet_choice.append(Bus)
        #Rede.dssLoads.Name = load
        #vet_choice.append(str(Rede.dssCktElement.BusNames[0]).split('.')[0])

    # I'll leave it here just in case. Basicly it is comparing the hardcoded list with the one
    # created based on load positions ( just for Rede_03 case )
    vet_choice_2 = list(['bus_33998182_030'
                      ,'bus_33998182_025'
                      ,'bus_33998182_031'
                      ,'bus_33998182_032'
                      ,'bus_33998182_033'
                      ,'bus_33998182_029'
                      ,'bus_33998182_015'
                      ,'bus_33998182_038'
                      ,'bus_33998182_037'
                      ,'bus_33998182_028'
                      ,'bus_33998182_026'
                      ,'bus_33998182_027'
                      ,'bus_33998182_035'
                      ,'bus_33998182_018'
                      ,'bus_33998182_019'
                      ,'bus_33998182_039'
                      ,'bus_33998182_016'
                      ,'bus_33998182_024'
                      ,'bus_33998182_017'
                      ,'bus_33998182_034'
                      ,'bus_33998182_020'
                      ,'bus_33998182_022'
                      ,'bus_33998182_026'
                      ,'bus_33998182_019'
                      ,'bus_33998182_024'
                      ,'bus_33998182_021'
                      ,'bus_33998182_023'])
    test5 = True if vet_choice == vet_choice_2 else False

    logger.info("Position list considered in random PV position choice : " + str(vet_choice))
    for i in range(Num_GDs):
        choice = random2.choice(vet_choice)
        vet_choice.remove(choice) if choice in vet_choice else 0
        Barras_GDs.append(choice)

    return
