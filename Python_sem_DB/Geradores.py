# coding: utf-8
from Definitions import *
from DB_Rede import *

import pandas as pd
import random2
import time

def Adicionar_GDs(Rede, Pot_GD, Simulation):

    # Definição dos loadshapes para cada GD
    STEPS = 96
    FindBusGD(Num_GDs)

    # A ideia é carregar os loadshapes e criar os geradores de acordo com a demanda de geradores a serem inseridos.
    # No momento existem 6 possíveis geradores, limitação pelo número de curvas de cargas adicionadas na pasta
    # de loadShapes. Para elevar esse número basta adicionar mais curvas

    # A definição do valor de potência é feita pela função HC. A cada tentativa as GDs são redefinidas e o valor de
    # Pot_GD é atualizado

    for i in range(Num_GDs):
        Rede.dssText.Command = "New LoadShape._GD_" + str(i + 1) + " npts=" + str(STEPS) + " sinterval=1 " \
              "pmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_" + str(i + 1) + ".txt) " \
              "qmult=(file=C:\\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_" + str(i + 1) + ".txt)"

    [Create_GD(Rede, 'Hugo_' + str(i), Pot_GD, 0, '_GD_' + str(i + 1), Simulation) for i in range(Num_GDs)]
    print(DF_Geradores.head())

def Create_GD(Rede, Nome, kW, kvar, LoadShape, Simulation):

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
                           str(Identify_Phases(DF_Geradores.loc[index, 'Phases'])[1]) +\
                           " bus1=" + str(DF_Geradores.loc[index, 'Bus'] +
                                          Identify_Phases(DF_Geradores.loc[index, 'Phases'])[0] ) +\
                           " kv=" + str(Rede.dssBus.kVBase) + " kW=" + str(kW) +\
                           " kVAr=" + str(kvar + 0.001) + " model=1" +\
                           " daily=" + str(LoadShape)

def Fase2String(STRING):

    a = ''
    for i in STRING:
        a += str(i)
    return a

def FindBusGD(Num_GDs):

    [Barras_GDs.append(random2.choice(DF_Tensao_A.Barras.values)) for i in range(Num_GDs)]
    #print(Barras_GDs)
    # Colocar um debug level aqui