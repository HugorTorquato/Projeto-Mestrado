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


def IEC(V1, V2, V3, VAngle1, VAngle2, VAngle3, Rede2, kvbase):  # Limite de 3%

    List_Desq_IEC = []

    for i in range(originalSteps(Rede2)):

        # Add other unbalances calculations here, and also add to dataframe to be sent to database

        Tensao1 = V1[i] if len(V1) > 1 * kvbase and V1[i] > 0.3 * kvbase else 0
        Tensao2 = V2[i] if len(V2) > 1 * kvbase and V2[i] > 0.3 * kvbase else 0
        Tensao3 = V3[i] if len(V3) > 1 * kvbase and V3[i] > 0.3 * kvbase else 0

        if Tensao1 != 0 and Tensao2 != 0 and Tensao3 != 0:
            Positiva = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(VAngle1[i]))) +
                                   (alfa * cmath.rect(Tensao2, np.deg2rad(VAngle2[i]))) +
                                   (inv_alfa * cmath.rect(Tensao3, np.deg2rad(VAngle3[i]))))
            Negativa = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(VAngle1[i]))) +
                                   (inv_alfa * cmath.rect(Tensao2, np.deg2rad(VAngle2[i]))) +
                                   (alfa * cmath.rect(Tensao3, np.deg2rad(VAngle3[i]))))
            List_Desq_IEC.append((abs(Negativa) / abs(Positiva)) * 100)
        else:
            List_Desq_IEC.append(0)

    return List_Desq_IEC


def IEEE(Tensao1, Tensao2, Tensao3, max, min):  # limite de 2.5%

    # Utiliza tensões de fase
    Tensao1 = 0 if Tensao1 < 0.3 else Tensao1
    Tensao2 = 0 if Tensao2 < 0.3 else Tensao2
    Tensao3 = 0 if Tensao3 < 0.3 else Tensao3

    return (3 * 100 * (max - min)) / (Tensao1 + Tensao2 + Tensao3)


def NEMA(Vmedio, Vmax):
    # return ((Vmax - Vmedio) / Vmedio) * 100 if Vmedio != 0 else 0
    return ((Vmax - Vmedio) / Vmedio) if Vmedio != 0 else 0


def ativa_barra(Rede2, nome_barra):
    #Rede.dssCircuit.SetActiveBus(nome_barra)
    Rede2.circuit_set_active_bus(nome_barra)


def puVmagAngle(Rede):
    return Rede.dssBus.puVmagAngle


def originalSteps(Rede2):
    #Rede.dssLoadShapes.Name = Rede.dssLoadShapes.AllNames[1]
    # print len(Rede.dssLoadShapes.pmult)
    #return len(Rede.dssLoadShapes.pmult)

    Rede2.loadshapes_write_name(Rede2.loadshapes_all_names()[1])
    return Rede2.loadshapes_read_npts()


def Colunas_DF_Horas(Rede):
    coll = []
    [coll.append(str(i)) for i in range(originalSteps(Rede))]

def Check2(Rede2, Simulation):

    from Definitions import limite_superior, limite_inferior, limite_Deseq

    t1 = time.time()

    Check_Voltages(Rede2, Simulation)
    Check_Current(Rede2, Simulation)

    # Processas DF_Violation_Data para saber se teve violação. Seguir as regras
        # > Steps_wtout_overcurrent
        # > interval_limit = np.floor(originalSteps(Rede) * float(Steps_wtout_unbalance / 100))

    overvoltage = 1 if DF_Violations_Data["ViolationType"][DF_Violations_Data["ViolationType"] ==
                                                           ViolationType.overvoltage.value].count() > 0 \
        else 0
    undervoltage = 1 if DF_Violations_Data["ViolationType"][DF_Violations_Data["ViolationType"] ==
                                                            ViolationType.undervoltage.value].count() > 0 \
        else 0
    unbalance = 1 if DF_Violations_Data["ViolationType"][DF_Violations_Data["ViolationType"] ==
                                                         ViolationType.unbalance.value].count() > 0 \
        else 0
    overcurrent = 1 if DF_Violations_Data["ViolationType"][DF_Violations_Data["ViolationType"] ==
                                                           ViolationType.overcurrent.value].count() > 0 \
        else 0

    Ress = True if overvoltage == 0 and undervoltage == 0 and overcurrent == 0 and unbalance == 0 \
        else Salva_Check_Report(Simulation, overvoltage, undervoltage, overcurrent, unbalance)

    logger.debug("Continue? " + str(Ress) + ": "
                                            " overvoltage = " + str(overvoltage) +
                 " undervoltage = " + str(undervoltage) +
                 " overcurrent = " + str(overcurrent) +
                 " unbalance = " + str(unbalance))

    logger.debug("Check2 took {" + str(time.time() - t1) + " sec} to execulte in simulation: " + str(Simulation))
    return Ress

def Populate_DF_Violations_Data(Simulation, bus, fase, type, i , data):

    t1 = time.time()

    index = len(DF_Violations_Data.index)
    DF_Violations_Data.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
    DF_Violations_Data.loc[index, 'Simulation'] = Simulation
    DF_Violations_Data.loc[index, 'Element'] = bus
    DF_Violations_Data.loc[index, 'Fase'] = fase
    DF_Violations_Data.loc[index, 'ViolationType'] = type
    DF_Violations_Data.loc[index, 'TimeStep'] = i
    DF_Violations_Data.loc[index, 'Value'] = data

    logger.debug("Populate_DF_Violations_Data took {" + str(time.time() - t1) + " sec} to execulte in simulation: " + str(Simulation))

def Check_Current(Rede2, Simulation):

    t1 = time.time()

    LinesMonNames = []
    [LinesMonNames.append(mon) if mon.startswith("line") and mon.endswith("_voltage") else ""
         for mon in Rede2.monitors_all_names()]

    # Overcurrent
    df_temp_curr = DF_Corrente_Limite.copy(deep=True)
    for line in LinesMonNames:

        Rede2.monitors_write_name(line)
        line_name_df = line.replace("line_", "").replace("_voltage", "").upper()
        header = Rede2.monitors_header()

        I1 = Rede2.monitors_channel(header.index(' I1') + 1) if ' I1' in header else []
        I2 = Rede2.monitors_channel(header.index(' I2') + 1) if ' I2' in header else []
        I3 = Rede2.monitors_channel(header.index(' I3') + 1) if ' I3' in header else []
        #A1A = Rede2.monitors_channel(header.index(' IAngle1') + 1) if ' IAngle1' in header else []
        #A2A = Rede2.monitors_channel(header.index(' IAngle2') + 1) if ' IAngle2' in header else []
        #A3A = Rede2.monitors_channel(header.index(' IAngle3') + 1) if ' IAngle3' in header else []
        #I2 = [5000, 5000, 5000, 5000, 5.383053212426603e-05, 5000, 5000, 5000, 4000, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05, 5.383053212426603e-05]

        Nom_Element_Curr = DF_Corrente_Limite["Current_Limits"][
            DF_Corrente_Limite["Elementos"] == "Line." + line_name_df].values
        logger.debug("Overcurrent check : Line name : " + line_name_df + " Current Limit : " + str(Nom_Element_Curr))

        phase = 1
        for data in [I1, I2, I3]:
            try:
                #if np.any(data) > 0 and np.max(data) > Nom_Element_Curr:
                if np.any(data) > 0:
                    if np.max(data) > Nom_Element_Curr:
                        count = 0
                        for i in range(len(data)):
                            if data[i] > Nom_Element_Curr:
                                count += 1
                                if count > 1e10:
                                    logger.debug("Valor errado, avaliar o que aconteceu")
                                    logger.error("Valor: " + str(data[i]) + " Simulation: " + str(Simulation) + ""
                                                " line_name_df:" + str(line_name_df) + " Phase:" + str(phase) + " Voltage Type Violation:" +
                                                ViolationType.overvoltage.value)
                                if count >= Steps_wtout_overcurrent:
                                    count = 0
                                    Populate_DF_Violations_Data(Simulation, line_name_df, phase,
                                                                ViolationType.overcurrent.value, i, data[i])
            except:
                print()
            phase = phase + 1
    logger.debug("Check_Current took {" + str(time.time() - t1) + " sec} to execulte in simulation: " + str(Simulation))

def Check_Voltages(Rede2, Simulation):

    t1 = time.time()

    FakeLoadsMonNames = []
    [FakeLoadsMonNames.append(mon) if mon.startswith("load_fakeload") else ""
     for mon in Rede2.monitors_all_names()]

    for mon in FakeLoadsMonNames:

        # Get bus base voltage
        bus = mon.replace("load_fakeload_", "").replace("_voltage", "")
        ativa_barra(Rede2, bus)
        kvbase = Rede2.bus_kv_base()

        Rede2.monitors_write_name(mon)
        header = Rede2.monitors_header()

        pross_inf_limit = limite_inferior * 1000 * kvbase
        pross_sup_limit = limite_superior * 1000 * kvbase

        V1  = Rede2.monitors_channel(header.index(' V1') + 1) if ' V1' in header else []
        V1A = Rede2.monitors_channel(header.index(' VAngle1') + 1) if ' VAngle1' in header else []
        V2  = Rede2.monitors_channel(header.index(' V2') + 1) if ' V2' in header else []
        V2A = Rede2.monitors_channel(header.index(' VAngle2') + 1) if ' VAngle2' in header else []
        V3  = Rede2.monitors_channel(header.index(' V3') + 1) if ' V3' in header else []
        V3A = Rede2.monitors_channel(header.index(' VAngle3') + 1) if ' VAngle3' in header else []

        #V1 = [70.46826171875, 2270.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 16870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875, 6870.46826171875]
        # Calcular desequilibrio

        List_Desq_IEC = IEC(V1, V2, V3, V1A, V2A, V3A, Rede2, kvbase * 1000)

        # Overvoltage and undervoltage
        phase = 1
        for data in [V1, V2, V3]:
            if len(data) > 1 and max(data) > pross_sup_limit:
                count = 0
                for i in range(len(data)):
                    if (data[i]> pross_sup_limit):
                        count += 1
                        if count > 1e10:
                            logger.debug("Valor errado, avaliar o que aconteceu")
                            logger.error("Valor: " + str(data[i]) + " Simulation: " + str(Simulation) + ""
                                        " Bus:" + str(bus) + " Phase:" + str(phase) + " Voltage Type Violation:" +
                                         ViolationType.overvoltage.value)
                        if count >= Steps_wtout_overcurrent:
                            count = 0
                            Populate_DF_Violations_Data(Simulation, bus, phase,
                                                        ViolationType.overvoltage.value, i, data[i])
            if len(data) > 1 and min(data) < pross_inf_limit:
                count = 0
                for i in range(len(data)):
                    if (data[i] < pross_inf_limit and data[i] > 0.3 * kvbase * 1000):
                        count += 1
                        if count >= Steps_wtout_overcurrent:
                            count = 0
                            Populate_DF_Violations_Data(Simulation, bus, phase,
                                                        ViolationType.undervoltage.value, i, data[i])

            phase = phase + 1

        # Unbalance
        if max(List_Desq_IEC) > limite_Deseq:
            count = 0
            for i in range(len(List_Desq_IEC)):
                if len(List_Desq_IEC) > 1 and (List_Desq_IEC[i] > limite_Deseq):
                    count += 1
                    if count > 1e10:
                        logger.debug("Valor errado, avaliar o que aconteceu")
                        logger.error("Valor: " + str(data[i]) + " Simulation: " + str(Simulation) + ""
                                     " Bus:" + str(bus) + " Phase:" + str(phase) + " Voltage Type Violation:" +
                                     ViolationType.overvoltage.value)
                    if count >= Steps_wtout_overcurrent:
                        count = 0
                        Populate_DF_Violations_Data(Simulation, bus, 0,
                                                    ViolationType.unbalance.value, i, List_Desq_IEC[i])

    logger.debug("Check_Voltages took {" + str(time.time() - t1) + " sec} to execulte in simulation: " + str(Simulation))

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
            except Exception as e:
                logger.info("Deu Ruim Check_overcurrent()")
                logger.info("Deu Ruim Check_overcurrent() com erro : " + str(e))


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

def Fase2String(STRING):
    a = ''
    for i in STRING:
        #if i != 'N':
        a += str(i)
    return a

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

def Identify_Overcurrent_Limits(Rede2):

    from Definitions import DF_Corrente_Limite

    NormAmps = []
    Line_Names = []
    Wire_Geometry = []

    for Line in GetAllLinesfNames(Rede2):
        Rede2.lines_write_name(Line)
        Line_Names.append("Line." + str(Line).upper())
        NormAmps.append(float(Rede2.lines_read_norm_amps()))
        Wire_Geometry.append(Rede2.lines_read_geometry())

    try:
        if not DF_Corrente_Limite.empty:
            # Make sure the DF is empty before adding more stuffs in there
            [Limpar_DF(DF) for DF in [DF_Corrente_Limite]]

        DF_Corrente_Limite['Elementos'] = Line_Names
        DF_Corrente_Limite['Wire_Geometry'] = Wire_Geometry
        DF_Corrente_Limite['Current_Limits'] = NormAmps

    except Exception as e:
        logger.error("Deu Ruim Identify_Overcurrent_Limits()")
        logger.error("Deu Ruim Identify_Overcurrent_Limits() com erro : " + str(e))

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


def Return_Time_String_Colum(Rede2):
    # Essa função retorna uma string com o número correto de colunas para ser usada nas buscas
    # pelas tabelas do SQL

    Ary = ''
    MaxLen = originalSteps(Rede2)

    for i in range(MaxLen):
        Ary += '(Time_' + str(i) + ')' if i == MaxLen - 1 else '(Time_' + str(i) + '),'
    return Ary

def Return_Time_String_Colum_Case_Options(Rede2):
    # Essa função retorna uma string com os casos para o store procedure 'Update_Voltage_Data_Table_Max_Min_Time_Value'
    # Vai variar de acordo com o tamanho da amostragem desejada para o dia

    commandMax = ''
    commandMin = ''

    for i in range(originalSteps(Rede2)):
        commandMax += ' WHEN ValueMaxPU = Time_' + str(i) + ' AND Time_' + str(i) + ' <> 0 THEN \'Time_' + str(i) + '\''

    for i in range(originalSteps(Rede2)):
        commandMin += ' WHEN ValueMinPU = Time_' + str(i) + ' AND Time_' + str(i) + ' <> 0 THEN \'Time_' + str(i) + '\''

    return commandMax, commandMin

def OrderFiles(listOfFiles):
    # This function aims to order files with a numeric value in place. The norma procedure considers
    # 10 after 1 instead of 2 after 1. This function will fix it

    B = []
    for item in listOfFiles:
        B.append([item, item.split(' ')[0], item.split(' ')[1].split('.')[0]])

    return sorted(B, key=lambda B: int(B[1]))

def GetAllBusNames(Rede2):
    return Rede2.circuit_all_bus_names()

def GetAllLoadsNames(Rede2):
    return Rede2.loads_all_names()

def GetAllTransfNames(Rede2):
    return Rede2.transformers_all_Names()

def GetAllElemtfNames(Rede2):
    return Rede2.circuit_all_element_names()

def GetAllLinesfNames(Rede2):
    return Rede2.lines_all_names()

def CreateFakeLoads(Rede2):

    #This method aims to create a fake load on each bus to alow us to create monitors in there
    #Rede2.text("New LoadShape.Fakeloadshape Npts=96"
    #           " pMult=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)"
    #           " Hour=(0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75, 14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75, 16.0, 16.25, 16.5, 16.75, 17.0, 17.25, 17.5, 17.75, 18.0, 18.25, 18.5, 18.75, 19.0, 19.25, 19.5, 19.75, 20.0, 20.25, 20.5, 20.75, 21.0, 21.25, 21.5, 21.75, 22.0, 22.25, 22.5, 22.75, 23.0, 23.25, 23.5, 23.75)"
    #           )

    for bus in GetAllBusNames(Rede2):
        ativa_barra(Rede2, bus)
        bus_nodes = bus
        count = 0
        for i in Rede2.bus_nodes():
            bus_nodes = bus_nodes + "." + str(i)
            count += sum([1 if i < 4 else 0])

        Command = "New Load.FakeLoad_" + bus + " Bus1=" + bus_nodes + \
          " model=6 kV=" + str(Rede2.bus_kv_base()) + " Phases=" + str(count) + " kW=0 kvar=0"

        logger.debug("Create_FakeLoad - " + Command)
        Rede2.text(Command)
