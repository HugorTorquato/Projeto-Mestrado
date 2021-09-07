# coding: utf-8
import win32com.client
import pandas as pd
from Princ import *
import numpy as np

Rede_Path = "C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\TCC\Rede" # IEEE13
Rede_Path = "C:\\Users\hugo1\Desktop\Rede_03\_trafo3"                       #Rede_03
Debug_Path = "C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\Debug"

# Nível de Tensão
DF_Tensao_A = pd.DataFrame()
DF_Tensao_B = pd.DataFrame()
DF_Tensao_C = pd.DataFrame()

# Deseq Tensão
DF_Desq_IEC  = pd.DataFrame()
DF_Desq_IEEE = pd.DataFrame()
DF_Desq_NEMA = pd.DataFrame()

# Corrente Elementos
DF_Corrente_itera = pd.DataFrame()
DF_Corrente_A = pd.DataFrame()
DF_Corrente_B = pd.DataFrame()
DF_Corrente_C = pd.DataFrame()

# Valores e Arrays auxiliares
Barras_GDs = []

DF_kW_PV = pd.DataFrame()
DF_kvar_PV = pd.DataFrame()
DF_irradNow_PV = pd.DataFrame()

# Salva dados locais relacionados aos monitores
DF_Lista_Monitors = pd.DataFrame()
DF_Monitors_Power_Values = pd.DataFrame()
DF_Monitors_Voltage_Values = pd.DataFrame()

DF_Geradores = pd.DataFrame({'Simulation': [],
                             'Name'      : [],
                             'Bus'       : [],
                             'kW'        : [],
                             'kvar'      : [],
                             'Phases'    : '',
                             'LoadShape' : ''})

DF_PVPowerData = pd.DataFrame({'Simulation' : [],
                               'Name'       : [],
                               'Bus'        : [],
                               'Measurement': ''})

DF_PV = pd.DataFrame({'Simulation': [],
                      'Name'      : [],
                      'Bus'       : [],
                      'Pmp'       : [],
                      'kW'        : [],
                      'kvar'      : [],
                      'FP'        : [],
                      'Phases'    : '',
                      'Irrad'     : '',
                      'Temp'      : ''})

DF_General = pd.DataFrame({'Voltage_Max': [],
                           'Voltage_Min': [],
                           'GD_Config'  : ''})

DF_Barras = pd.DataFrame({'Simulation'     : [],
                          'Name'           : [],
                          'V_pu_max_a'     : [],
                          'V_pu_max_b'     : [],
                          'V_pu_max_c'     : [],
                          'V_pu_min_a'     : [],
                          'V_pu_min_b'     : [],
                          'V_pu_min_c'     : [],
                          'Deseq_IEC'      : [],
                          'Deseq_IEEE'     : [],
                          'Deseq_NEMA'     : []})

DF_Elements = pd.DataFrame({'Simulation'     : [],
                            'Elemento'       : [],
                            'I_pu_max_a'     : [],
                            'I_pu_max_b'     : [],
                            'I_pu_max_c'     : [],
                            'I_pu_min_a'     : [],
                            'I_pu_min_b'     : [],
                            'I_pu_min_c'     : []})

# Lembrar de alterar essa tabela sempre que tiver alteração no número de monitores
# Adicionar os novos campos
DF_Monitors_Data = pd.DataFrame({'Simulation'     : [],
                                 'Elemento'       : [],
                                 'Measurement'    : []})

DF_Voltage_Data = pd.DataFrame({'Simulation'     : [],
                                 'Barras'        : [],
                                 'Fase'          : []})

DF_Current_Data = pd.DataFrame({'Simulation'     : [],
                                'Elementos'       : [],
                                'Fase'           : []})

DF_TESTE = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [4, 3, 2, 1],
    "C": [2, 1, 4, 3]})

##Switches

Salva_Dados = 0     # Aciona o script que faz o levantamento dos dados da rede
Criar_GD = 1        # Aciona a inserção de GDs na rede
Num_GDs = 4         # Definição do número de GDs que serão adicionadas
Calc_HC = 1         # Aciona o cálculo do HC
All_GDs = 1
Use_PV = 1          # 1- Usa o PVSystem  0 - Usa geradore
Norma = 1           #  # 0 - PRODIST # 1 - IEEE
Num_Simulations = 2 # Deifnie o número de simulações que serão realizadas

# PVSystem
FP_1 = 1
Const_Irrad = .705
Const_Temp = 25
FP = 1
Incremento_gd = 100

#Constants
sqrt3 = np.sqrt(3)
alfa = complex(-0.5, 0.866025403784)
inv_alfa = complex(-0.5, -0.866025403784)

if Norma == 1:
    limite_superior = 1.1
    limite_inferior = 0.9
    limite_Deseq = 2.5

if Norma == 0:
    limite_superior = 1.05
    limite_inferior = 0.92
    limite_Deseq = 2

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
            self.dssSensor = self.dssCircuit.Sensors
            self.dssPVSystems = self.dssCircuit.PVSystems
