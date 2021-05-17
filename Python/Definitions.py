# coding: utf-8
import win32com.client
import pandas as pd
from Princ import *

# Nível de tensão
DF_Tensao_A = pd.DataFrame()
DF_Tensao_B = pd.DataFrame()
DF_Tensao_C = pd.DataFrame()

# GDs
DF_Geradores = pd.DataFrame({'Simulation': [],
                             'Name'      : [],
                             'Bus'       : [],
                             'kW'        : [],
                             'kvar'      : [],
                             'Phases'    : '',
                             'LoadShape' : ''})

DF_General = pd.DataFrame({'Voltage_Max': [],
                           'Voltage_Min': [],
                           'GD_Config'  : ''})


DF_TESTE = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [4, 3, 2, 1],
    "C": [2, 1, 4, 3]})

# Valores e Arrays auxiliares
Barras_GDs = []

##Switches

Salva_Dados = 0  # Aciona o script que faz o levantamento dos dados da rede
Criar_GD = 1     # Aciona a inserção de GDs na rede
Num_GDs = 2      # Definição do número de GDs que serão adicionadas
Calc_HC = 1      # Aciona o cálculo do HC

Num_Simulations = 2 # Deifnie o número de simulações que serão realizadas


class DSS():

    def __init__(self, Modelo_Barras):

        # Armazena o caminho para o circuito .dss para ser aberto
        self.Modelo_Barras = Modelo_Barras

        # Criar a conexão entre Python e OpenDSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Iniciar o Objeto DSS
        if self.dssObj.Start(0) == False:
            print("Problemas em iniciar o OpenDSS")
        else:
            # Criar variáveis paras as principais interfaces
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssCapacitores = self.dssCircuit.Capacitors
            self.dssRegControls = self.dssCircuit.RegControls
            self.dssLoadShapes = self.dssCircuit.LoadShapes
            self.dssLoads = self.dssCircuit.Loads
            self.dssLines = self.dssCircuit.Lines
            self.dssSwtControls = self.dssCircuit.SwtControls
            self.dssGenerators = self.dssCircuit.Generators
            self.dssMonitors = self.dssCircuit.Monitors
            self.dssActiveClass = self.dssCircuit.ActiveClass
            self.dssPDElements = self.dssCircuit.PDElements
            self.dssTransformers = self.dssCircuit.Transformers