# coding: utf-8
from Definitions import *
import pandas as pd
import random2

def Adicionar_GDs(Rede, Pot_GD, Simulation):

    from Definitions import DF_Geradores, DF_PV, Num_GDs
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
    # Rede.dssText.Command = "New XYCurve.vv_curve npts=4 Yarray=(1.0,1.0,-1.0,-1.0) " \
    #                       "XArray = (0.5,0.95,1.05,1.5)"

    # Rede.dssText.Command = "New InvControl.InvPVCtrl mode=VOLTVAR voltage_curvex_ref=rated vvc_curve1=vv_curve EventLog=yes"

    if Use_PV:
        [Create_PV(Rede, 'PV_' + str(i), Pot_GD, FP, 'Irrad', 'Temp', Simulation) for i in range(Num_GDs)]
        print(DF_PV.head())
    else:
        [Create_GD(Rede, 'GD_' + str(i), Pot_GD, 0, '_GD_' + str(i + 1), Simulation) for i in range(Num_GDs)]


def Create_PV(Rede, Nome, Pmp, FP, Irrad, Temp, Simulation):
    from Definitions import DF_PV, Barras_GDs
    from FunctionsSecond import ativa_barra, Identify_Phases

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

    A = Identify_Phases(DF_PV.loc[index, 'Phases'])[1]
    B = DF_PV.loc[index, 'Bus']

    Rede.dssText.Command = "New PVSystem." + Nome + " phases=" + \
                           str(Identify_Phases(DF_PV.loc[index, 'Phases'])[1]) + \
                           " bus1=" + \
                           str(DF_PV.loc[index, 'Bus']) + \
                           str(Identify_Phases(DF_PV.loc[index, 'Phases'])[0]) + \
                           " Pmpp=" + str(Pmp) + \
                           " kv=" + str(Rede.dssBus.kVBase) + \
                           " kVA=" + str(Pmp * 1.15) + \
                           " kvarMax=" + str(Pmp * 1.2) + \
                           " con=wye" \
                           " %Cutin=0 %cutout=0 EffCurve=Eff P-TCurve=FactorPVsT" \
                           " pf=1 VarFollowInverter=false" \
                           " irradiance=" + str(Const_Irrad) + " temperature=" + str(Const_Temp) + \
                           " daily=irrad Tdaily=Temp"  # debugtrace=yes"


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
        a += str(i)
    return a

def FindBusGD(Num_GDs):
    from Definitions import DF_Tensao_A, Barras_GDs

    [Barras_GDs.append(random2.choice(DF_Tensao_A.Barras.values)) for i in range(Num_GDs)]
    # [Barras_GDs.append(list(combinations(DF_Tensao_A.Barras.values, 2))) for i in range(Num_GDs)]
    # print(Barras_GDs)
    # Colocar um debug level aqui
    return
