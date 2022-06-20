# coding: utf-8
import numpy as np

from Definitions import *
from Definitions import logger
import pandas as pd
import cmath
import time

def Correntes_elementos(Rede, itera):
    # A função poderia ser melhor em termos de performance. No momento ela está salvando um arquivo .csv
    # com as correntes de todos os elementos, lendo esses valores para um DF temp e deste DF tempo os valores
    # são salvos em outros 3 DF ( um para cada fase no formato para fazer as análises de maneira semelhante aos
    # valores obtidos na tensão ).

    from Definitions import DF_Corrente_itera, DF_Corrente_A, DF_Corrente_B, DF_Corrente_C

    t1 = time.time()
    Rede.dssText.Command = "Export Currents file = " + Debug_Path + "\EXP_PVMETERS.CSV"

    Limpar_DF(DF_Corrente_itera)
    DF_Corrente_itera = pd.read_csv(Debug_Path + "\EXP_PVMETERS.CSV")

    # Melhorar isso para identificar o caminho correto, se pa criar um header fixo na definição da rede

    count = 0

    A = DF_Corrente_itera.columns[1]
    B = DF_Corrente_itera.columns[3]
    C = DF_Corrente_itera.columns[5]
    AA = DF_Corrente_itera.columns[2]
    BA = DF_Corrente_itera.columns[4]
    CA = DF_Corrente_itera.columns[6]

    if not 'Elementos' in DF_Corrente_A:
        DF_Corrente_A.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)
        DF_Corrente_B.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)
        DF_Corrente_C.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)
        DF_Corrente_Ang_A.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)
        DF_Corrente_Ang_B.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)
        DF_Corrente_Ang_C.insert(0, 'Elementos', DF_Corrente_itera['Element'].values, allow_duplicates=True)

    for element in DF_Corrente_itera['Element'].values:
        DF_Corrente_A.loc[DF_Corrente_A.index == count, str(itera)] = DF_Corrente_itera[A].values[count]
        DF_Corrente_B.loc[DF_Corrente_B.index == count, str(itera)] = DF_Corrente_itera[B].values[count]
        DF_Corrente_C.loc[DF_Corrente_C.index == count, str(itera)] = DF_Corrente_itera[C].values[count]
        DF_Corrente_Ang_A.loc[DF_Corrente_Ang_A.index == count, str(itera)] = DF_Corrente_itera[AA].values[count]
        DF_Corrente_Ang_B.loc[DF_Corrente_Ang_B.index == count, str(itera)] = DF_Corrente_itera[BA].values[count]
        DF_Corrente_Ang_C.loc[DF_Corrente_Ang_C.index == count, str(itera)] = DF_Corrente_itera[CA].values[count]

        count += 1

    logger.debug("Correntes_elementos took {" + str(time.time() - t1) + " sec} to execulte "
                                                                        "in iteration: " + str(itera))

# Não é usada, pode remover

def Dados_Elements2(Rede, itera):
    # Essa função é separada da coleta das correntes pq pode ser ou não habilitada, depende do "Savar_Dados_Elem"

    from Definitions import DF_Pot_itera, DF_Voltage_itera

    t1 = time.time()

    # Exportar os dados e prapara o dataframe

    Rede.dssText.Command = "Export ElemPowers file = " + Debug_Path + "\EXP_ELEMPOWERS.CSV"
    Rede.dssText.Command = "Export ElemVoltages file = " + Debug_Path + "\EXP_ELEMVOLTAGES.CSV"

    Limpar_DF(DF_Pot_itera), Limpar_DF(DF_Voltage_itera)

    # O número de colunas definidas no arquivo não é constante, por isso tempos de fazer a definição das colunas e a
    # verificação se existe algum valor "nan" -> condição de a coluna não ser definida para determinado elemento

    col_names = ["Element", "Nterminals", "Nconductors", "P_1", "Q_1", "P_2", "Q_2", "P_3", "Q_3", "P_4", "Q_4",
                 "P_5", "Q_5", "P_6", "Q_6", "P_7", "Q_7", "P_8", "Q_8"]
    DF_Pot_itera = pd.read_csv(Debug_Path + "\EXP_ELEMPOWERS.CSV", sep=',', names=col_names, skiprows=1)

    col_names = ["Element", "Nterminals", "Nconductors", "V_1", "Ang_1", "V_2", "Ang_2", "V_3", "Ang_3", "V_4", "Ang_4",
                 "V_5", "Ang_5", "V_6", "Ang_6", "V_7", "Ang_7", "V_8", "Ang_8"]
    DF_Voltage_itera = pd.read_csv(Debug_Path + "\EXP_ELEMVOLTAGES.CSV", sep=',', names=col_names, skiprows=1)

    DF_Pot_itera.fillna(0, inplace=True), DF_Voltage_itera.fillna(0, inplace=True)

    # Segregação dos resultados e criação do dataframe

    AP = DF_Pot_itera.columns[3]
    BP = DF_Pot_itera.columns[5]
    CP = DF_Pot_itera.columns[7]
    APQ = DF_Pot_itera.columns[4]
    BPQ = DF_Pot_itera.columns[6]
    CPQ = DF_Pot_itera.columns[8]

    AV = DF_Voltage_itera.columns[3]
    BV = DF_Voltage_itera.columns[5]
    CV = DF_Voltage_itera.columns[7]
    AVA = DF_Voltage_itera.columns[4]
    BVA = DF_Voltage_itera.columns[6]
    CVA = DF_Voltage_itera.columns[8]

    if not 'Elementos' in DF_Pot_P_A:
        DF_Pot_P_A.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)
        DF_Pot_P_B.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)
        DF_Pot_P_C.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)
        DF_Pot_Q_A.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)
        DF_Pot_Q_B.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)
        DF_Pot_Q_C.insert(0, 'Elementos', DF_Pot_itera['Element'].values, allow_duplicates=True)

    if not 'Elementos' in DF_Voltage_A:
        DF_Voltage_A.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)
        DF_Voltage_B.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)
        DF_Voltage_C.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)
        DF_Voltage_Ang_A.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)
        DF_Voltage_Ang_B.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)
        DF_Voltage_Ang_C.insert(0, 'Elementos', DF_Voltage_itera['Element'].values, allow_duplicates=True)

    count = 0
    for element in DF_Pot_itera['Element'].values:
        DF_Pot_P_A.loc[DF_Pot_P_A.index == count, str(itera)] = DF_Pot_itera[AP].values[count]
        DF_Pot_P_B.loc[DF_Pot_P_B.index == count, str(itera)] = DF_Pot_itera[BP].values[count]
        DF_Pot_P_C.loc[DF_Pot_P_C.index == count, str(itera)] = DF_Pot_itera[CP].values[count]
        DF_Pot_Q_A.loc[DF_Pot_Q_A.index == count, str(itera)] = DF_Pot_itera[APQ].values[count]
        DF_Pot_Q_B.loc[DF_Pot_Q_B.index == count, str(itera)] = DF_Pot_itera[BPQ].values[count]
        DF_Pot_Q_C.loc[DF_Pot_Q_C.index == count, str(itera)] = DF_Pot_itera[CPQ].values[count]
        count += 1

    count = 0
    for element in DF_Voltage_itera['Element'].values:
        DF_Voltage_A.loc[DF_Voltage_A.index == count, str(itera)] = DF_Voltage_itera[AV].values[count]
        DF_Voltage_B.loc[DF_Voltage_B.index == count, str(itera)] = DF_Voltage_itera[BV].values[count]
        DF_Voltage_C.loc[DF_Voltage_C.index == count, str(itera)] = DF_Voltage_itera[CV].values[count]
        DF_Voltage_Ang_A.loc[DF_Voltage_Ang_A.index == count, str(itera)] = DF_Voltage_itera[AVA].values[count]
        DF_Voltage_Ang_B.loc[DF_Voltage_Ang_B.index == count, str(itera)] = DF_Voltage_itera[BVA].values[count]
        DF_Voltage_Ang_C.loc[DF_Voltage_Ang_C.index == count, str(itera)] = DF_Voltage_itera[CVA].values[count]

        count += 1

    logger.debug("Dados_Elements took {" + str(time.time() - t1) + " sec} to execulte "
                                                                   "in iteration: " + str(itera))


def get_resultados_potencia(self):
    # self.dssText.Command = "Show power kva elements"
    # self.dssText.Command = "Show Voltages LN Nodes"
    # self.dssText.Command = "Show Taps"
    self.dssText.Command = "Show Currents"


def Identify_Position(Fase, Nodes):
    if Fase == 1:
        Voltage = 0
        Angle = 1
        return Voltage, Angle

    if Fase == 2 and 1 not in Nodes:
        Voltage = 0
        Angle = 1
        return Voltage, Angle
    elif Fase == 2:
        Voltage = 2
        Angle = 3
        return Voltage, Angle

    if Fase == 3 and 1 not in Nodes:
        if 2 not in Nodes:
            Voltage = 0
            Angle = 1
            return Voltage, Angle
        else:
            Voltage = 2
            Angle = 3
            return Voltage, Angle
    elif 2 not in Nodes:
        Voltage = 2
        Angle = 3
        return Voltage, Angle
    else:
        Voltage = 4
        Angle = 5
        return Voltage, Angle


def Tensao_Barras(Rede, itera):
    t1 = time.time()

    puVmag_Buses = []
    angle_Buses = []
    Bus_Names = DF_Tensao_A.Barras.values

    count = 0

    tensao1 = 0
    tensao2 = 0
    tensao3 = 0
    angle1 = 0
    angle2 = 0
    angle3 = 0
    vmedio = 0

    for Barra in Bus_Names:
        # Feature:
        # -> Não parece estar salvando corretamente a respectiva fase de cada barra, pode ser melhorado

        # puVmag = []
        angle = []
        Rede.dssCircuit.SetActiveBus(Barra)
        ativa_barra(Rede, Barra)  # Ativa a barra
        VmagAngle = puVmagAngle(Rede)
        Nodes = Rede.dssBus.Nodes

        DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[
            Identify_Position(1, Nodes)[0]] if 1 in Nodes else 0
        tensao1 = VmagAngle[Identify_Position(1, Nodes)[0]] if 1 in Nodes else 0

        DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[
            Identify_Position(2, Nodes)[0]] if 2 in Nodes else 0
        tensao2 = VmagAngle[Identify_Position(2, Nodes)[0]] if 2 in Nodes else 0

        DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = VmagAngle[
            Identify_Position(3, Nodes)[0]] if 3 in Nodes else 0
        tensao3 = VmagAngle[Identify_Position(3, Nodes)[0]] if 3 in Nodes else 0

        Vmedio = (tensao1 + tensao2 + tensao3) / 3

        DF_Tensao_Ang_A.loc[DF_Tensao_Ang_A.index == count, str(itera)] = VmagAngle[
            Identify_Position(1, Nodes)[1]] if 1 in Nodes else 0
        angle1 = VmagAngle[Identify_Position(1, Nodes)[1]] if 1 in Nodes else 0

        DF_Tensao_Ang_B.loc[DF_Tensao_Ang_B.index == count, str(itera)] = VmagAngle[
            Identify_Position(2, Nodes)[1]] if 2 in Nodes else 0
        angle2 = VmagAngle[Identify_Position(2, Nodes)[1]] if 2 in Nodes else 0

        DF_Tensao_Ang_C.loc[DF_Tensao_Ang_C.index == count, str(itera)] = VmagAngle[
            Identify_Position(3, Nodes)[1]] if 3 in Nodes else 0
        angle3 = VmagAngle[Identify_Position(3, Nodes)[1]] if 3 in Nodes else 0

        #
        #        if len(VmagAngle) == 6 or len(VmagAngle) == 8:
        #            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
        #            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[2]  # puVmag.append(VmagAngle[0])
        #            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = VmagAngle[4]  # puVmag.append(VmagAngle[0])
        #            tensao1 = VmagAngle[0]# * sqrt3
        #            tensao2 = VmagAngle[2]# * sqrt3
        #            tensao3 = VmagAngle[4]# * sqrt3
        #            Vmedio = (tensao1 + tensao2 + tensao3) / 3
        #        elif len(VmagAngle) == 4:
        #            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
        #            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[2]  # puVmag.append(VmagAngle[0])
        #            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)
        #            tensao1 = VmagAngle[0]# * sqrt3
        #            tensao2 = VmagAngle[2]# * sqrt3
        #            tensao3 = 0
        #            vmedio = (tensao1 + tensao2) / 2
        #        elif len(VmagAngle) == 2:
        #            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
        #            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = 0  # puVmag.append(0)
        #            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)
        #            tensao1 = VmagAngle[0]# * sqrt3
        #            tensao2 = 0
        #            tensao3 = 0
        #            Vmedio = tensao1
        #
        #        if len(VmagAngle) == 6 or len(VmagAngle) == 8:
        #            DF_Tensao_Ang_A.loc[DF_Tensao_Ang_A.index == count, str(itera)] = VmagAngle[1]
        #            DF_Tensao_Ang_B.loc[DF_Tensao_Ang_B.index == count, str(itera)] = VmagAngle[3]
        #            DF_Tensao_Ang_C.loc[DF_Tensao_Ang_C.index == count, str(itera)] = VmagAngle[5]
        #            angle1 = VmagAngle[1]# + int(30)
        #            angle2 = VmagAngle[3]# + int(30)
        #            angle3 = VmagAngle[5]# + int(30)
        #        elif len(VmagAngle) == 4:
        #            DF_Tensao_Ang_A.loc[DF_Tensao_Ang_A.index == count, str(itera)] = VmagAngle[1]
        #            DF_Tensao_Ang_B.loc[DF_Tensao_Ang_B.index == count, str(itera)] = VmagAngle[3]
        #            DF_Tensao_Ang_C.loc[DF_Tensao_Ang_C.index == count, str(itera)] = 0
        #            angle1 = VmagAngle[1]# + int(30)
        #            angle2 = VmagAngle[3]# + int(30)
        #            angle3 = 0
        #        elif len(VmagAngle) == 2:
        #            DF_Tensao_Ang_A.loc[DF_Tensao_Ang_A.index == count, str(itera)] = VmagAngle[1]
        #            DF_Tensao_Ang_B.loc[DF_Tensao_Ang_B.index == count, str(itera)] = 0
        #            DF_Tensao_Ang_C.loc[DF_Tensao_Ang_C.index == count, str(itera)] = 0
        #            angle1 = VmagAngle[1]# + int(30)
        #            angle2 = 0
        #            angle3 = 0

        #
        #        if len(VmagAngle) == 6:
        #            angle.append(VmagAngle[1])
        #            angle.append(VmagAngle[3])
        #            angle.append(VmagAngle[5])
        #            angle1 = VmagAngle[1] + int(30)
        #            angle2 = VmagAngle[3] + int(30)
        #            angle3 = VmagAngle[5] + int(30)
        #        elif len(VmagAngle) == 4:
        #            angle.append(VmagAngle[1])
        #            angle.append(VmagAngle[3])
        #            angle.append(0)
        #            angle1 = VmagAngle[1] + int(30)
        #            angle2 = VmagAngle[3] + int(30)
        #            angle3 = 0
        #        elif len(VmagAngle) == 2:
        #            angle.append(VmagAngle[1])
        #            angle.append(0)
        #            angle.append(0)
        #            angle1 = VmagAngle[1] + int(30)
        #            angle2 = 0
        #            angle3 = 0

        # max_IEEE, min_IEEE = Max_Min(tensao1 / sqrt3, tensao2 / sqrt3, tensao3 / sqrt3)
        max_IEEE, min_IEEE = Max_Min(tensao1, tensao2, tensao3)
        max_NEMA, min_NEMA = Max_Min(tensao1, tensao2, tensao3)

        # Se precisar usar as demais normas masta descomentar o código
        DF_Desq_IEC.loc[DF_Tensao_A.index == count, str(itera)] = \
            IEC(tensao1, tensao2, tensao3, angle1, angle2, angle3)
        # IEC(tensao1 / sqrt3, tensao2 / sqrt3, tensao3 / sqrt3, angle1, angle2, angle3)
        DF_Desq_IEEE.loc[DF_Tensao_A.index == count, str(itera)] = \
            IEEE(tensao1, tensao2, tensao3, max_IEEE, min_IEEE)
        DF_Desq_NEMA.loc[DF_Tensao_A.index == count, str(itera)] = \
            NEMA(vmedio, max_NEMA)

        count += 1
        # puVmag_Buses.append(puVmag)
        # angle_Buses.append(angle)
    # print(DF_Tensao_A.head())
    logger.debug("Tensao_Barras took {" + str(time.time() - t1) + " sec} to execulte "
                                                                  "in iteration: " + str(itera))


def Max_Min(Tensao1, Tensao2, Tensao3):
    Vet_Max_Min = [Tensao1, Tensao2, Tensao3]

    Tensao1 = 0 if Tensao1 < 0.3 else Tensao1
    Tensao2 = 0 if Tensao2 < 0.3 else Tensao2
    Tensao3 = 0 if Tensao3 < 0.3 else Tensao3

    if Tensao1 != 0 and Tensao2 != 0 and Tensao3 != 0:
        max_Tensao = max(Vet_Max_Min)
        min_Tensao = min(Vet_Max_Min)
        return max_Tensao, min_Tensao

    elif Tensao1 == 0 and Tensao2 != 0 and Tensao3 != 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao2 > Tensao3:
            min_Tensao = Tensao3
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao2
            return max_Tensao, min_Tensao

    elif Tensao1 != 0 and Tensao2 == 0 and Tensao3 != 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao1 > Tensao3:
            min_Tensao = Tensao3
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao1
            return max_Tensao, min_Tensao

    elif Tensao1 != 0 and Tensao2 != 0 and Tensao3 == 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao1 > Tensao2:
            min_Tensao = Tensao2
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao1
            return max_Tensao, min_Tensao

    else:
        max_Tensao = max(Vet_Max_Min)
        min_Tensao = max_Tensao
        return max_Tensao, min_Tensao


def IEC(Tensao1, Tensao2, Tensao3, Angle1, Angle2, Angle3):  # Limite de 3%

    Tensao1 = 0 if Tensao1 < 0.3 else Tensao1
    Tensao2 = 0 if Tensao2 < 0.3 else Tensao2
    Tensao3 = 0 if Tensao3 < 0.3 else Tensao3

    if Tensao1 != 0 and Tensao2 != 0 and Tensao3 != 0:
        Positiva = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(Angle1))) +
                               (alfa * cmath.rect(Tensao2, np.deg2rad(Angle2))) +
                               (inv_alfa * cmath.rect(Tensao3, np.deg2rad(Angle3))))
        Negativa = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(Angle1))) +
                               (inv_alfa * cmath.rect(Tensao2, np.deg2rad(Angle2))) +
                               (alfa * cmath.rect(Tensao3, np.deg2rad(Angle3))))
        return (abs(Negativa) / abs(Positiva)) * 100
    else:
        return 0


def IEEE(Tensao1, Tensao2, Tensao3, max, min):  # limite de 2.5%

    # Utiliza tensões de fase
    Tensao1 = 0 if Tensao1 < 0.3 else Tensao1
    Tensao2 = 0 if Tensao2 < 0.3 else Tensao2
    Tensao3 = 0 if Tensao3 < 0.3 else Tensao3

    return (3 * 100 * (max - min)) / (Tensao1 + Tensao2 + Tensao3)


def NEMA(Vmedio, Vmax):
    # return ((Vmax - Vmedio) / Vmedio) * 100 if Vmedio != 0 else 0
    return ((Vmax - Vmedio) / Vmedio) if Vmedio != 0 else 0


def ativa_barra(Rede, nome_barra):
    Rede.dssCircuit.SetActiveBus(nome_barra)


def puVmagAngle(Rede):
    return Rede.dssBus.puVmagAngle


def originalSteps(Rede):
    Rede.dssLoadShapes.Name = Rede.dssLoadShapes.AllNames[1]
    # print len(Rede.dssLoadShapes.pmult)
    return len(Rede.dssLoadShapes.pmult)


def Colunas_DF_Horas(Rede):
    coll = []
    [coll.append(str(i)) for i in range(originalSteps(Rede))]


def Check(Rede, Simulation):

    # --------------------------------------------------------------------------------------------------------
    # Requirements

    # Fazer um check report para identificar quando cada uma das violações acontecerem

    # Mais de uma violação pode acontecer ao mesmo tempo, computar TODAS

    # Tem de entender o que está rolando com o desq de tensão

    # --------------------------------------------------------------------------------------------------------

    t1 = time.time()

    overvoltage = 0
    undervoltage = 0
    overcurrent = 0
    unbalance = 0

    overvoltage = 0 if Check_Overvoltage_Range(Rede, DF_Tensao_A, DF_Tensao_B, DF_Tensao_C) is False \
        else 1
    undervoltage = 0 if Check_Undervoltage_Range(Rede, DF_Tensao_A, DF_Tensao_B, DF_Tensao_C) is False \
        else 1
    overcurrent = 0 if Check_overcurrent() == 0 \
        else 1
    unbalance = 0 if Check_Desq_Range(Rede, DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA) is False \
        else 1

    Ress = True if overvoltage == 0 and undervoltage == 0 and overcurrent == 0 and unbalance == 0 \
        else Salva_Check_Report(Simulation, overvoltage, undervoltage, overcurrent, unbalance)

    logger.debug("Continue? " + str(Ress) + ": "
            " overvoltage = " + str(overvoltage) +
            " undervoltage = " + str(undervoltage) +
            " overcurrent = " + str(overcurrent) +
            " unbalance = " + str(unbalance))

    logger.debug("Check took {" + str(time.time() - t1) + " sec} to execulte "
                                                          "in simulation: " + str(Simulation))
    return Ress


def Check_overcurrent():

    # Daria para observar violações consecultivas, mas isso aumenta a complexidade e tempo. Em tese... essa violações
    # já ocorrem de forma concentrada

    t1 = time.time()
    Violacao = 0

    for DF_Cur in [DF_Corrente_A, DF_Corrente_B, DF_Corrente_C]:

        df_temp_curr = DF_Corrente_Limite.copy(deep=True)
        t_df = DF_Cur[DF_Cur.Elementos.str.contains("Line", regex=False)].set_index('Elementos')

        df_temp_curr.insert(df_temp_curr.ndim + 1, 'Max_Curr',
                            t_df.max(axis=1).values, allow_duplicates=True)

        Violations = []
        for ind in range(t_df.index.size):
            try:
                Violations.append(
                    t_df.iloc[ind].where(
                        t_df.iloc[ind] >
                        df_temp_curr.set_index('Elementos')['Current_Limits'][ind]).count())
            except:
                logger.debug("Deu Ruim Check_overcurrent()")


        df_temp_curr.insert(df_temp_curr.ndim + 2, 'Num_Violations',
                            Violations, allow_duplicates=True)

        for line in df_temp_curr['Num_Violations']:
            if line > Steps_wtout_overcurrent:
                Violacao = 1
                break

        if Violacao == 1:
            break

    logger.debug("Check_overcurrent took {" + str(time.time() - t1) + " sec} to execulte")

    return Violacao

def Check_Violations_Single_Limit(DF, limit, interval_limit, smaller = 0):

    t1 = time.time()
    DF2 = DF.set_index('Barras')
    count = 0

    if smaller == 0:
        for barra in DF2[DF2 > limit].count(axis=1).values:
            count += 1 if barra >= interval_limit else 0
    else:
        for barra in DF2[(DF2 > 0.7) & (DF2 < limit)].count(axis=1).values:
            count += 1 if barra >= interval_limit else 0

    logger.debug("Check_Violations_Single_Limit took {" + str(time.time() - t1) + " sec} to execulte")
    return count

def Check_Overvoltage_Range(Rede, A, B, C):

    t1 = time.time()
    from Definitions import limite_superior

    interval_limit = np.floor(originalSteps(Rede) * float(Steps_wtout_unbalance / 100))

    A = Check_Violations_Single_Limit(A, limite_superior, interval_limit)
    B = Check_Violations_Single_Limit(B, limite_superior, interval_limit)
    C = Check_Violations_Single_Limit(C, limite_superior, interval_limit)

    logger.debug("Check_Overvoltage_Range took {" + str(time.time() - t1) + " sec} to execulte")
    return False if (A + B + C) == 0 else True

def Check_Undervoltage_Range(Rede, A, B, C):

    t1 = time.time()
    from Definitions import limite_inferior

    interval_limit = np.floor(originalSteps(Rede) * float(Steps_wtout_unbalance / 100))

    # Esse 1 no final vai falar que é para fazer comparação meor que
    A = Check_Violations_Single_Limit(A, limite_inferior, interval_limit, 1)
    B = Check_Violations_Single_Limit(B, limite_inferior, interval_limit, 1)
    C = Check_Violations_Single_Limit(C, limite_inferior, interval_limit, 1)

    logger.debug("Check_Undervoltage_Range took {" + str(time.time() - t1) + " sec} to execulte")
    return False if (A + B + C) == 0 else True

def Check_Desq_Range(Rede, IEC, IEEE, NEMA):

    t1 = time.time()
    from Definitions import limite_Deseq

    interval_limit = np.floor(originalSteps(Rede) * float(Steps_wtout_unbalance / 100))
    DF = IEC if Norma == 1 else IEEE if Norma == 0 else NEMA

    logger.debug("Check_Desq_Range took {" + str(time.time() - t1) + " sec} to execulte")
    return \
        False if Check_Violations_Single_Limit(DF, limite_Deseq, interval_limit) == 0\
            else True

def Salva_Check_Report(Simulation_Data, overvoltage, undervoltage, overcurrent, unbalance):
    t1 = time.time()
    Limpar_DF(DF_Check_Report)

    index = len(DF_Check_Report.index)

    DF_Check_Report.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
    DF_Check_Report.loc[index, 'Simulation'] = Simulation_Data
    DF_Check_Report.loc[index, 'overvoltage'] = overvoltage
    DF_Check_Report.loc[index, 'undervoltage'] = undervoltage
    DF_Check_Report.loc[index, 'overcurrent'] = overcurrent
    DF_Check_Report.loc[index, 'unbalance'] = unbalance

    logger.debug("Salva_Check_Report took {" + str(time.time() - t1) + " sec} to execulte")
    return False


def Salvar_Dados_Tensao():
    t1 = time.time()
    Escrever = pd.ExcelWriter(Debug_Path + "\Debug.xlsx")

    DF_Tensao_A.to_excel(Escrever, 'DF_Tensao_A', index=False)
    DF_Tensao_B.to_excel(Escrever, 'DF_Tensao_B', index=False)
    DF_Tensao_C.to_excel(Escrever, 'DF_Tensao_C', index=False)

    Escrever.save()
    logger.debug("Salvar_Dados_Tensao took {" + str(time.time() - t1) + " sec} to execulte")


def Identify_Phases(Phases):
    Num_Phases = ""
    count = 0
    Aa = Phases

    for Phase in Phases:
        if Phase == "A":
            Num_Phases = Num_Phases + ".1"
            count += 1
        elif Phase == "B":
            Num_Phases = Num_Phases + ".2"
            count += 1
        elif Phase == "C":
            Num_Phases = Num_Phases + ".3"
            count += 1
    return Num_Phases, count


def Limpar_DF(DF):
    DF.drop([i for i in range(len(DF))], inplace=True)


def Max_and_Min_Voltage_DF(A, B, C):
    return max(max(A.set_index('Barras').max().values),
               max(B.set_index('Barras').max().values),
               max(C.set_index('Barras').max().values)), \
           min(min(Min_2(A.set_index('Barras').min().values)),
               min(Min_2(B.set_index('Barras').min().values)),
               min(Min_2(C.set_index('Barras').min().values)))


def Data_PV(Rede, itera):
    t1 = time.time()
    PVs = Rede.dssPVSystems.AllNames

    for PV in range(len(Rede.dssPVSystems.AllNames)):
        Rede.dssPVSystems.Name = str(PVs[PV])

        DF_kW_PV.loc[DF_kW_PV.index == PV, str(itera)] = Rede.dssPVSystems.kW
        DF_kvar_PV.loc[DF_kvar_PV.index == PV, str(itera)] = Rede.dssPVSystems.kvar
        DF_irradNow_PV.loc[DF_irradNow_PV.index == PV, str(itera)] = Rede.dssPVSystems.IrradianceNow

    logger.debug("Data_PV took {" + str(time.time() - t1) + " sec} to execulte "
                                                            "in iteration: " + str(itera))


def Power_measurement_PV(Rede, Simulation):
    from Definitions import DF_PVPowerData, DF_PV

    t1 = time.time()
    Measur = ['kW', 'kvar', 'irradNow']
    PVs = Rede.dssPVSystems.AllNames

    for PV in range(len(Rede.dssPVSystems.AllNames)):
        for Meas in range(len(Measur)):
            index = len(DF_PVPowerData)
            DF_PVPowerData.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
            DF_PVPowerData.loc[index, 'Simulation'] = Simulation
            DF_PVPowerData.loc[index, 'Name'] = PVs[PV]
            DF_PVPowerData.loc[index, 'Bus'] = \
                DF_PV.query('Name == "' + str(PVs[PV]).upper() + '"')['Bus'].values
            DF_PVPowerData.loc[index, 'Measurement'] = Measur[Meas]

            if Meas == 0:
                for i in range(originalSteps(Rede)):
                    DF_PVPowerData.loc[index, 'Time_' + str(i)] = DF_kW_PV.loc[PV, str(i)]
            elif Meas == 1:
                for i in range(originalSteps(Rede)):
                    DF_PVPowerData.loc[index, 'Time_' + str(i)] = DF_kvar_PV.loc[PV, str(i)]
            elif Meas == 2:
                for i in range(originalSteps(Rede)):
                    DF_PVPowerData.loc[index, 'Time_' + str(i)] = DF_irradNow_PV.loc[PV, str(i)]

    logger.debug("Power_measurement_PV took {" + str(time.time() - t1) + " sec} to execulte "
                                                                         "in simulation: " + str(Simulation))


def Adicionar_EnergyMeter(Rede):
    # Definir o elemento correto ( barra sourcebus ou a primeira linha? fazer de forma iterativa )
    TE = Rede.dssCircuit.Name

    # Rede.dssText.Command = "New energymeter.EM element=circuit." + str(Rede.dssCircuit.Name) + " terminal=1"

    # Como coletar os resultados?

    return


def Adjust_Colum_Name(DF):
    # Faz o ajuste dos nomes das colunas ( 0 -> Time_0 ) caso não esteja de acordo com a formatação da tabela

    new_Col = []

    for column in DF.columns:
        new_Col.append('Time_' + str(column)) if column.isnumeric() is True else new_Col.append(column)

    return new_Col


def Identify_Overcurrent_Limits(Rede):

    NormAmps = []
    Line_Names = []
    Wire_Geometry = []

    for Line in Rede.dssLines.AllNames:
        Rede.dssLines.Name = Line
        Line_Names.append("Line." + str(Line).upper())
        NormAmps.append(float(Rede.dssLines.NormAmps))
        Wire_Geometry.append(Rede.dssLines.Geometry)

        # Acharo nome dos cabos pelo opendss
        #Rede.dssCktElement.Name = Line
        #a = Rede.dssCktElement.Name
        #b = Rede.dssCktElement.Properties("geometry").val
        #c = Rede.dssCktElement.Properties("wires").val
        #d = Rede.dssCktElement.Properties("cncables").val
        #d = Rede.dssCktElement.Properties("tscables").val

    DF_Corrente_Limite.insert(0, 'Elementos', Line_Names, allow_duplicates=True)
    DF_Corrente_Limite.insert(1, 'Wire_Geometry', Wire_Geometry, allow_duplicates=True)
    DF_Corrente_Limite.insert(2, 'Current_Limits', NormAmps, allow_duplicates=True)

def Converter_Intervalo_de_Simulacao(Rede, Hora):
    # Converte a hora passada para o respectivo instante em steps da curva de carga

    Pontos_por_Hora = originalSteps(Rede) / 24

    H = Hora // 100 % 100

    return H * Pontos_por_Hora


def Min_2(Vet):
    for value in range(len(Vet)):
        if Vet[value] < 0.2:
            Vet[value] = 1
    return Vet


def Return_Time_String_Colum(Rede):
    # Essa função retorna uma string com o número correto de colunas para ser usada nas buscas
    # pelas tabelas do SQL

    Ary = ''
    MaxLen = originalSteps(Rede)

    for i in range(MaxLen):
        Ary += '(Time_' + str(i) + ')' if i == MaxLen - 1 else '(Time_' + str(i) + '),'

    return Ary


def Return_Time_String_Colum_Case_Options(Rede):
    # Essa função retorna uma string com os casos para o store procedure 'Update_Voltage_Data_Table_Max_Min_Time_Value'
    # Vai variar de acordo com o tamanho da amostragem desejada para o dia

    commandMax = ''
    commandMin = ''

    for i in range(originalSteps(Rede)):
        commandMax += ' WHEN ValueMaxPU = Time_' + str(i) + ' AND Time_' + str(i) + ' <> 0 THEN \'Time_' + str(i) + '\''

    for i in range(originalSteps(Rede)):
        commandMin += ' WHEN ValueMinPU = Time_' + str(i) + ' AND Time_' + str(i) + ' <> 0 THEN \'Time_' + str(i) + '\''

    return commandMax, commandMin
