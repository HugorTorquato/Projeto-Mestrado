# coding: utf-8
from Definitions import *
import pandas as pd
import random2

def Adicionar_GDs(Rede, Pot_GD, Simulation):

    from Definitions import DF_PV, Num_GDs
    from FunctionsSecond import originalSteps

    STEPS = originalSteps(Rede)

    # A ideia é carregar os loadshapes e criar os geradores de acordo com a demanda de geradores a serem inseridos.
    # No momento existem 6 possíveis geradores, limitação pelo número de curvas de cargas adicionadas na pasta
    # de loadShapes. Para elevar esse número basta adicionar mais curvas

    # A definição do valor de potência é feita pela função HC. A cada tentativa as GDs são redefinidas e o valor de
    # Pot_GD é atualizado

    for i in range(Num_GDs):
        Rede.dssText.Command = "New LoadShape._GD_" + str(i + 1) + " npts=" + str(STEPS) + " minterval=15 " \
                               "pmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_" \
                               + str(i + 1) + ".txt) " \
                               "qmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_" \
                               + str(i + 1) + ".txt)"

    # Criação das curvas do pv
    Rede.dssText.Command = "New XYCurve.FatorPvsT npts=4 xarray=[0 25 75 100] yarray=[1.2 1.0 .8 .6]"
    Rede.dssText.Command = "New XYCurve.Eff npts=4 xarray=[.1 .2 .4 1.0] yarray=[.86 .9 .93 .97]"
    Rede.dssText.Command = "New TShape.Temp npts=96 minterval=15 " \
                           "temp=(File=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Temp.txt)"
    Rede.dssText.Command = "New LoadShape.irrad npts=96 minterval=15 " \
                           "mult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Irrad.txt)"
    Rede.dssText.Command = "New XYcurve.generic npts=4 Xarray=(0.5,0.89,0.92,0.95,1,1.02,1.05,1.1,1.5) " \
                           "Yarray=(1.0,1.0,1,0,0,0,1,-1.0,-1.0)"
    Rede.dssText.Command = "New XYCurve.vv_curve npts=7 Yarray=[1 1 0 0 0 -1 -1] " \
                           "XArray = [0.5 0.87 0.92 1 1.05 1.01 1.5]"

    if Use_PV:
        [Create_PV(Rede, 'PV_' + str(i), Pot_GD, FP, 'Irrad', 'Temp', Simulation) for i in range(Num_GDs)]
        print(DF_PV.head(10)) # Printa os dados gerais das GDs ( resumo )
    else:
        [Create_GD(Rede, 'GD_' + str(i), Pot_GD, 0, '_GD_' + str(i + 1), Simulation) for i in range(Num_GDs)]


def Create_PV(Rede, Nome, Pmp, FP, Irrad, Temp, Simulation):

    from Definitions import DF_PV, Barras_GDs
    from FunctionsSecond import ativa_barra, Identify_Phases
    from Monitores import Define_Random_Monior_Test

    index = len(DF_PV)
    STRING = ['A', 'B', 'C', 'N']

    DF_PV.loc[index, 'Simulation'] = Simulation
    DF_PV.loc[index, 'Name'] = Nome
    DF_PV.loc[index, 'Bus'] = Barras_GDs[(len(Barras_GDs) - 1) - index]

    ativa_barra(Rede, str(DF_PV.loc[index, 'Bus']))

    DF_PV.loc[index, 'Pmp'] = Pmp
    DF_PV.loc[index, 'kW'] = 0   #Definir função para coletar pot gerada
    DF_PV.loc[index, 'kvar'] = 0
    DF_PV.loc[index, 'FP'] = FP
    DF_PV.loc[index, 'Phases'] = Fase2String([STRING[i - 1] for i in Rede.dssBus.Nodes])
    DF_PV.loc[index, 'Irrad'] = Irrad
    DF_PV.loc[index, 'Temp'] = Temp

    # Pmpp - Ponto de máx pot
    # kva - pot nom inversor - Pot gerada n pode ser maior
    # pot dc = ppmppx x irrad x (1-irrad_tempo) x temp_por_pot
    # pot ac = pot dc x eff

    Rede.dssText.Command = "New PVSystem." + Nome + " phases=" + \
                           str(Identify_Phases(DF_PV.loc[index, 'Phases'])[1]) + \
                           " bus1=" + str(DF_PV.loc[index, 'Bus']) + \
                           str(Identify_Phases(DF_PV.loc[index, 'Phases'])[0]) + \
                           " Pmpp=" + str(Pmp) + \
                           " kv=" + str(Rede.dssBus.kVBase) + \
                           " kVA=" + str(Pmp * 1.15) + \
                           " kvarMax=" + str(Pmp * 1.2) + \
                           " con=wye" \
                           " %Cutin=0.1 %cutout=0.1 EffCurve=Eff P-TCurve=FactorPVsT" \
                           " pf=1 VarFollowInverter=true " \
                           " irradiance=" + str(Const_Irrad) + " temperature=" + str(Const_Temp) + \
                           " daily=irrad Tdaily=Temp wattpriority=yes debugtrace=yes"
    if Simulation > 2 and Debug_VV == 1:
        Rede.dssText.Command = "set maxcontroliter=2000"

        Rede.dssText.Command ="New InvControl.InvPVCtrl_" + Nome + " DERList=PVSystem." + Nome + \
                              " pvsystemlist=pv_0 mode=VOLTVAR voltage_curvex_ref=rated " \
                           "vvc_curve1=generic monVoltageCalc=" + str(Identify_Phases(DF_PV.loc[index, 'Phases'])[0])+\
                           " deltaQ_factor=0.2 RefReactivePower=VARAVAL varchangetolerance=0.025"# EventLog=yes "

    ## deltaQ_factor -> Mudança máxima da pot reativa da solução anterior para a desejada durante
    #                   cada iteração de controle
    ## RefReactivePower -> Limita a saída de pot reativa ao limite dsponível no inversor, caso seja requisitado
    #                       mais que o kva permitido, o kvar vai ser limitado
    ## varchangetolerence -> Diferença entre o pot reativa desejada para a obtida. Um dos parâmetrso que limita
    #                        o número de iterações feita por cada controle
    ## maxcontroliter -> Número máximo de iterações por controle, default é 15. Um número baixo pode não ser
    #                    suficiente e, casos mais complesxo de multiplos GDs


    # Define um monitor para observar as configurações do PV durante o InvControl
    Define_Random_Monior_Test(Rede, "InvControl", "PVSystem." + Nome, 1, 3)

    print("New PVSystem." + Nome + " phases=" + \
          str(Identify_Phases(DF_PV.loc[index, 'Phases'])[1]) + \
          " bus1=" + \
          str(DF_PV.loc[index, 'Bus']) + \
          str(Identify_Phases(DF_PV.loc[index, 'Phases'])[0]) + \
          " Pmpp=" + str(Pmp) + \
          " kv=" + str(Rede.dssBus.kVBase) + \
          " kVA=" + str(Pmp * 1.15) + \
          " kvarMax=" + str(Pmp * 1.2) + \
          " con=wye" \
          " %Cutin=0.1 %cutout=0.1 EffCurve=Eff P-TCurve=FactorPVsT" \
          " pf=1 VarFollowInverter=true " \
          " irradiance=" + str(Const_Irrad) + " temperature=" + str(Const_Temp) + \
          " daily=irrad Tdaily=Temp wattpriority=yes" ) # debugtrace=yes")

def Create_GD(Rede, Nome, kW, kvar, LoadShape, Simulation):
    from Definitions import DF_Geradores, Barras_GDs

    # Preparação para armazenamento dos dados
    index = len(DF_Geradores)  # Define a linha para aplicar as alterações
    STRING = ['A', 'B', 'C', 'N']  # Definie a string de fases para o gerador
    from FunctionsSecond import ativa_barra, Identify_Phases  # Importa a função para ativação da barra

    # Armazenar e salvar dados
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

def Fase2String(STRING):
    a = ''
    for i in STRING:
        #if i != 'N':
       a += str(i)
    return a

def FindBusGD(Num_GDs):
    from Definitions import DF_Tensao_A, Barras_GDs, Debug_VV

    if Debug_VV == 1:
        Barras_GDs_list = ['bus_33998182_039']#, 'bus_33998182_011',
            # 'bus_33998182_013', 'bus_33998182_027', 'bus_33998182_022']
        #Barras_GDs_list = ['bus_33998182_039', 'bus_33998182_011',
        #                 'bus_33998182_013', 'bus_33998182_027', 'bus_33998182_022']

        for i in range(Num_GDs):
            Barras_GDs.append(Barras_GDs_list[i])

        return

    vet_choice = list(DF_Tensao_A.Barras.values)
    for i in range(Num_GDs):
        choice = random2.choice(vet_choice)
        vet_choice.remove(choice) if choice in vet_choice else 0
        Barras_GDs.append(choice)


    # [Barras_GDs.append(list(combinations(DF_Tensao_A.Barras.values, 2))) for i in range(Num_GDs)]
    # print(Barras_GDs)
    # Colocar um debug level aqui
    return
