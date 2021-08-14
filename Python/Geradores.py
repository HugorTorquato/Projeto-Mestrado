# coding: utf-8
from Definitions import *
import pandas as pd
import random2
from itertools import *

def Adicionar_GDs(Rede, Pot_GD, Simulation):
    from Definitions import DF_Geradores, Num_GDs

    # Definição dos loadshapes para cada GD
    STEPS = 96

    #FindBusGD(Num_GDs) - Se deixar essa definição aqui ela vai trocar a posição das GDs a cada alteração de Pot

    # A ideia é carregar os loadshapes e criar os geradores de acordo com a demanda de geradores a serem inseridos.
    # No momento existem 6 possíveis geradores, limitação pelo número de curvas de cargas adicionadas na pasta
    # de loadShapes. Para elevar esse número basta adicionar mais curvas

    # A definição do valor de potência é feita pela função HC. A cada tentativa as GDs são redefinidas e o valor de
    # Pot_GD é atualizado

    for i in range(Num_GDs):
        Rede.dssText.Command = "New LoadShape._GD_" + str(i + 1) + " npts=" + str(STEPS) + " sinterval=1 " \
              "pmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_" + str(i + 1) + ".txt) " \
              "qmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_" + str(i + 1) + ".txt)"

    # Criação das curvas do pv
    Rede.dssText.Command = "New XYCurve.FatorPvsT npts=4 xarray=[0 25 75 100] yarray=[1.2 1.0 .8 .6]"
    Rede.dssText.Command = "New XYCurve.Eff npts=4 xarray=[.1 .2 .4 1.0] yarray=[.86 .9 .93 .97]"
    Rede.dssText.Command = "New TShape.Temp npts=96 interval= 1 " \
                           "temp=(File=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Temp.txt)"
    Rede.dssText.Command = "New LoadShape.Irrad npts=96 interval=1 " \
                           "mult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Temp.txt"


    #if Geradores:
    #[Create_GD(Rede, 'GD_' + str(i), Pot_GD, 0, '_GD_' + str(i + 1), Simulation) for i in range(Num_GDs)]

    [Create_PV(Rede, 'PV_' + str(i), Pot_GD, 0, Simulation) for i in range(1)]
    print(DF_Geradores.head())

def Create_PV(Rede, Nome, kW, kvar, Simulation):

    Rede.dssText.Command = "New PVSystem.PV phases=3 bus1=650 Pmpp=100 kv=13.8 kVA=1200 con=wye " \
                           "%Cutin=10 %cutout=10 EffCurve=Eff P-TCurve=FactorPVsT " \
                           "pf=0.9 kvarMax=1200 VarFollowInverter=false " \
                           "irradiance=0.98 daily=Irrad Tdaily=Temp"

    Rede.dssText.Command = "New XYCurve.vv_curve npts=4 Yarray=(1.0,1.0,-1.0,-1.0) " \
                           "XArray = (0.5,0.95,1.05,1.5)"

    Rede.dssText.Command = "New InvControl.InvPVCtrl mode=VOLTVAR voltage_curvex_ref=rated " \
                           "vvc_curve1=vv_curve EventLog=yes"




    return


def Create_GD(Rede, Nome, kW, kvar, LoadShape, Simulation):

    from Definitions import DF_Geradores

    # FEATURES : Adicionar lógica para salvar os dados

    # Preparação para armazenamento dos dados
    index = len(DF_Geradores)                                  # Define a linha para aplicar as alterações
    STRING = ['A', 'B', 'C', 'N']                              # Definie a string de fases para o gerador
    from FunctionsSecond import ativa_barra, Identify_Phases   # Importa a função para ativação da barra

    # Armazenar e salvar dados
    DF_Geradores.loc[index, 'Simulation'] = Simulation
    DF_Geradores.loc[index, 'Name' ] = Nome
    DF_Geradores.loc[index, 'Bus'] = Barras_GDs[(len(Barras_GDs)-1) - index]
    DF_Geradores.loc[index, 'kW'   ] = kW
    DF_Geradores.loc[index, 'kvar' ] = kvar

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

    from Definitions import DF_Tensao_A

    [Barras_GDs.append(random2.choice(DF_Tensao_A.Barras.values)) for i in range(Num_GDs)]
    #[Barras_GDs.append(list(combinations(DF_Tensao_A.Barras.values, 2))) for i in range(Num_GDs)]
    #print(Barras_GDs)
    # Colocar um debug level aqui
    return