# coding: utf-8
from Definitions import *
import pandas as pd
import random2

print DF_Geradores.head()

def Adicionar_GDs(Rede):

    # Definição dos loadshapes para cada GD
    STEPS = 96
    Rede.dssText.Command = "New LoadShape._GD_1 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_1.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_1.txt)"
    Rede.dssText.Command = "New LoadShape._GD_2 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_2.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_2.txt)"
    Rede.dssText.Command = "New LoadShape._GD_3 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_3.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_3.txt)"
    Rede.dssText.Command = "New LoadShape._GD_4 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_4.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_4.txt)"
    Rede.dssText.Command = "New LoadShape._GD_5 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_5.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_5.txt)"
    Rede.dssText.Command = "New LoadShape._GD_6 npts=" + str(STEPS) + " sinterval=1 " \
                                      "pmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\P_GD_6.txt) " \
                                      "qmult=(file=C:\Users\hugo1\Desktop\Rede_03\LoadShapeGeradores\Q_GD_6.txt)"

    Create_GD(Rede, 'Hugo', 50, 0, '_GD_1')
    Create_GD(Rede, 'Hugo2', 50, 0, '_GD_2')

def Create_GD(Rede, Nome, kW, kvar, LoadShape):

    # Preparação para armazenamento dos dados
    index = len(DF_Geradores)                                  # Define a linha para aplicar as alterações
    STRING = ['A', 'B', 'C', 'N']                              # Definie a string de fases para o gerador
    from FunctionsSecond import ativa_barra, Identify_Phases   # Importa a função para ativação da barra

    # Armazenar e salvar dados
    DF_Geradores.loc[index, 'Nome' ] = Nome
    DF_Geradores.loc[index, 'Barra'] = random2.choice(DF_Tensao_A.Barras.values)
    DF_Geradores.loc[index, 'kW'   ] = kW
    DF_Geradores.loc[index, 'kvar' ] = kvar

    ativa_barra(Rede, str(DF_Geradores.loc[index, 'Barra']))
    DF_Geradores.loc[index, 'Fases'] = Fase2String([STRING[i - 1] for i in Rede.dssBus.Nodes])
    DF_Geradores.loc[index, 'LoadShape'] = LoadShape

    print Identify_Phases(DF_Geradores.loc[index, 'Fases'])
    # Criação da GD no Opendss
    Rede.dssText.Command = "new generator.GD_" + str(index + 1) + " phases=" + \
                           str(len(Identify_Phases(DF_Geradores.loc[index, 'Fases']))) +\
                           " bus1=" +  str(DF_Geradores.loc[index, 'Barra']) + \
                           str(Identify_Phases(DF_Geradores.loc[index, 'Fases'])) +\
                           " kv=" + str(Rede.dssBus.kVBase) + " kW=" + str(kW) +\
                           " kVAr=" + str(kvar + 0.001) + " model=1" +\
                           " daily=" + str(LoadShape)

    # Salvar dados

    # como serão as fases dos geradores? Adicionar o neutro ou não?

    # Colocar o loop para fazer o cálculo do HC

    print DF_Geradores.head()

def Fase2String(STRING):

    a = ''
    for i in STRING:
        a += str(i)
    return a
