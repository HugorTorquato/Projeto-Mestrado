# coding: utf-8
import win32com.client
import pandas as pd
from Princ import *
import numpy as np
import logging
logging.basicConfig(
    level=logging.DEBUG,
    #format='%(asctime)s:%(levelname)s:%(funcname)s:%(message)s', # funcname não funcionava
    format='%(asctime)s:%(levelname)s:%(message)s',
    filename='LOG.log'#filename='/Debug/LOG.log'
)


#Rede_Path = "C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\TCC\Rede" # IEEE13
Rede_Path = "C:\\Users\hugo1\Desktop\Rede_03\_trafo3"                       #Rede_03
Debug_Path = "C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\Debug"

#############################################################################
###################### Logging Configuration ################################
#############################################################################

# DEBUG: Detailed information, intresting onçy for investigations

# INFO: Just confirmations that things are working

# WARNING: Something unexpected happened and may cause problems in he feature

# ERROR: Relate problems, software not able to peform funcitons
    #.exception inclui dados do traceback no log

# CRITICAL: Serious error, program cannot continue

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_Handler = logging.FileHandler(Debug_Path + '\Log' + '\Overal.log')
file_Handler.setFormatter(formatter)
logger.addHandler(file_Handler)
logger.debug("Log Initialized")

#############################################################################
#############################################################################


unbalance_chk = []


# Nível de Tensão (barras)
DF_Tensao_A = pd.DataFrame()
DF_Tensao_B = pd.DataFrame()
DF_Tensao_C = pd.DataFrame()
DF_Tensao_Ang_A = pd.DataFrame()
DF_Tensao_Ang_B = pd.DataFrame()
DF_Tensao_Ang_C = pd.DataFrame()

# Deseq Tensão
DF_Desq_IEC  = pd.DataFrame()
DF_Desq_IEEE = pd.DataFrame()
DF_Desq_NEMA = pd.DataFrame()

# Corrente Elementos
DF_Corrente_itera = pd.DataFrame()
DF_Corrente_A = pd.DataFrame()
DF_Corrente_B = pd.DataFrame()
DF_Corrente_C = pd.DataFrame()
DF_Corrente_Ang_A = pd.DataFrame()
DF_Corrente_Ang_B = pd.DataFrame()
DF_Corrente_Ang_C = pd.DataFrame()

# Pot elementos
DF_Pot_itera = pd.DataFrame()
DF_Pot_P_A = pd.DataFrame()
DF_Pot_P_B = pd.DataFrame()
DF_Pot_P_C = pd.DataFrame()
DF_Pot_Q_A = pd.DataFrame()
DF_Pot_Q_B = pd.DataFrame()
DF_Pot_Q_C = pd.DataFrame()

# Tensão elementos
DF_Voltage_itera = pd.DataFrame()
DF_Voltage_A = pd.DataFrame()
DF_Voltage_B = pd.DataFrame()
DF_Voltage_C = pd.DataFrame()
DF_Voltage_Ang_A = pd.DataFrame()
DF_Voltage_Ang_B = pd.DataFrame()
DF_Voltage_Ang_C = pd.DataFrame()


DF_Corrente_Limite = pd.DataFrame()

# Valores e Arrays auxiliares
Barras_GDs = []


###############################################################################################
# Achar forma melhor de definir uma variável global que pode ser alterada durante o loop interno
Casos = [] # Usado para obter o último caso e salvar o valor no banco de dados,
###############################################################################################

DF_kW_PV = pd.DataFrame()
DF_kvar_PV = pd.DataFrame()
DF_irradNow_PV = pd.DataFrame()

# Salva dados locais relacionados aos monitores
DF_Lista_Monitors = pd.DataFrame()
DF_Monitors_Power_Values = pd.DataFrame()
DF_Monitors_Voltage_Values = pd.DataFrame()

DF_Geradores = pd.DataFrame({'Case'      : [],
                             'Simulation': [],
                             'Name'      : [],
                             'Bus'       : [],
                             'kW'        : [],
                             'kvar'      : [],
                             'Phases'    : '',
                             'LoadShape' : ''})

DF_PVPowerData = pd.DataFrame({'Case'       : [],
                               'Simulation' : [],
                               'Name'       : [],
                               'Bus'        : [],
                               'Measurement': ''})

DF_PV = pd.DataFrame({'Case'      : [],
                      'Simulation': [],
                      'Name'      : [],
                      'Bus'       : [],
                      'Pmp'       : [],
                      'kW'        : [],
                      'kvar'      : [],
                      'FP'        : [],
                      'Phases'    : '',
                      'Irrad'     : '',
                      'Temp'      : ''})

DF_General = pd.DataFrame({'Case'       : [],
                           'Voltage_Max': [],
                           'Voltage_Min': [],
                           'GD_Config'  : ''})

DF_Barras = pd.DataFrame({'Case'           : [],
                          'Simulation'     : [],
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

DF_Elements = pd.DataFrame({'Case'           : [],
                            'Simulation'     : [],
                            'Elemento'       : [],
                            'I_pu_max_a'     : [],
                            'I_pu_max_b'     : [],
                            'I_pu_max_c'     : [],
                            'I_pu_min_a'     : [],
                            'I_pu_min_b'     : [],
                            'I_pu_min_c'     : []})

# Lembrar de alterar essa tabela sempre que tiver alteração no número de monitores
# Adicionar os novos campos
DF_Monitors_Data = pd.DataFrame({'Case'           : [],
                                 'Simulation'     : [],
                                 'Elemento'       : [],
                                 'Measurement'    : []})

DF_Voltage_Data = pd.DataFrame({'Case'          : [],
                                'Simulation'    : [],
                                'Barras'        : [],
                                'Fase'          : [],
                                'TimeMaxPU'     : [],
                                'ValueMaxPU'    : [],
                                'TimeMinPU'     : [],
                                'ValueMinPU'    : []})

DF_Current_Data = pd.DataFrame({'Case'           : [],
                                'Simulation'     : [],
                                'Elementos'      : [],
                                'Fase'           : []})

DF_Check_Report = pd.DataFrame({'Case'           : [],
                                'Simulation'     : [],
                                'overvoltage'    : [],
                                'undervoltage'   : [],
                                'overcurrent'    : [],
                                'unbalance'      : []})

DF_Current_Elemt_Data_Ang = pd.DataFrame({'Case'           : [],
                                          'Simulation'     : [],
                                          'Elementos'      : [],
                                          'Fase'           : []})

DF_Power_P_Elemt_Data = pd.DataFrame({'Case'           : [],
                                      'Simulation'     : [],
                                      'Elementos'      : [],
                                      'Fase'           : []})

DF_Power_Q_Elemt_Data = pd.DataFrame({'Case'           : [],
                                      'Simulation'     : [],
                                      'Elementos'      : [],
                                      'Fase'           : []})

DF_Voltage_Elemt_Data = pd.DataFrame({'Case'           : [],
                                      'Simulation'     : [],
                                      'Elementos'      : [],
                                      'Fase'           : []})

DF_Voltage_Elemt_Data_Ang = pd.DataFrame({'Case'           : [],
                                          'Simulation'     : [],
                                          'Elementos'      : [],
                                          'Fase'           : []})


DF_TESTE = pd.DataFrame({
    "N": ['N', 'M', 'P', 'Q'],
    "A": [1, 2, 3.5, 4],
    "B": [4.5, 3.1, 2, 1],
    "C": [4.6, 1, 2, 3]})

##Switches

Salva_Dados = 0         # Aciona o script que faz o levantamento dos dados da rede
Savar_Dados_Elem = 1    # Habilita que os dados de pot e tensão dos elementos sejam salvos
Criar_GD = 1            # Aciona a inserção de GDs na rede
Num_GDs = 3             # Definição do número de GDs que serão adicionadas
Calc_HC = 1             # Aciona o cálculo do HC
All_GDs = 1

Use_PV = 1              # 1- Usa o PVSystem  0 - Usa geradore
Norma = 1               #  # 0 - PRODIST # 1 - IEEE
Num_Simulations = 2     # Deifnie o número de simulações que serão realizadas

Num_Estudos_de_Caso = 4 # Define o estudo de caso em questão (configuração das GDs)

Debug_VV = 1            # Modo Debug para mensurar e comparar o comportamento do VV no sistema ( 1 - liga 0 - desliga)

# PVSystem
FP_1 = 1
Const_Irrad = .705
Const_Temp = 25
FP = 1
Incremento_gd = 100#0.5  # Valores em porcentagem (%) da pot do trafo de entrada

Steps_wtout_unbalance = 10

#Constants
sqrt3 = np.sqrt(3)
alfa = complex(-0.5, 0.866025403784)
inv_alfa = complex(-0.5, -0.866025403784)

#############################################################################
###################### Definir Tempo de Simulação ###########################
#############################################################################

## Entre com a hora sem o ":", por exemplo: 13:00 -> 1300

# Simulação com intervalo limitado
Inicio_Sim = 1000
Fim_Sim = 1500

# Simulação completa
#Inicio_Sim = 0000
#Fim_Sim = 2400

# Adicionar Log aqui

#############################################################################
#############################################################################

if Norma == 1:
    limite_superior = 1.05
    limite_inferior = 0.92
    limite_Deseq = 3#2.5

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
