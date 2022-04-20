# coding: utf-8
import os

import numpy as np

from Definitions import *
import pandas as pd
import time

def Adicionar_Monitores(Rede):

    # Se precisar adicionar algum monitor no circuito, basta replicar a linha seguinte refasendo a atribuição de
    # valor. Lembrar que o comando de criação do monitor necessita do tipo de elemento para determinar o parametro
    # "element" da declaração, mas o nome do monitor não precisa... Basta seguir o padrão :
    #                                                                       <TIPO>.<NOME_ELEMENTO>

    from FunctionsSecond import Limpar_DF
    Limpar_DF(DF_Lista_Monitors)

    #DF_Lista_Monitors.loc[len(DF_Lista_Monitors), "Elemento_com_monitor"] = "line." + str(Rede.dssLines.AllNames[0])
    for element in Rede.dssCircuit.AllElementNames:
        if element.split('.')[0] != 'Monitor':
            DF_Lista_Monitors.loc[len(DF_Lista_Monitors), "Elemento_com_monitor"] = element
    # ...

    Define_Monitor(Rede, DF_Lista_Monitors["Elemento_com_monitor"].values)

    #Define_Monitor(Rede, Rede.dssCircuit.AllElementNames)

def Define_Monitor(Rede, Lista_Monitores):

    # Atualmente são definidos dois tipos de monitores por elemento:
    # -> modelo 1 -> Medidores de Pot ( Atia e Reativa )
    # -> modelo 2 -> Medidores de V & I (Tensão e corrente )
    #
    # Se adicionar mais algum modelo, lembrar de modificar a função "Export_And_Read_Monitors_Data", ela vai salvar e
    # ler os arquivos depois de cada simulação, e a implementação é baseada nem dois modelos de medidores. Se Adicionar
    # mais um, tem de adicionar lá também.

    logger.debug("Starting Monitors")
    for element in Lista_Monitores:
        if element.split('.')[0] != 'Monitor':

            # Medição de corrente?

            Command1 = "New monitor." + str(element.replace('.', '_')) + "_power element=" + str(element) \
                       + " terminal=1 mode=1 ppolar=no enabled=Yes"
            Command2 = "New monitor." + str(element.replace('.', '_')) + "_voltage element=" + str(element) \
                       + " terminal=1 mode=0 enabled=Yes"
            Command3 = "New monitor." + str(element.replace('.', '_')) + "_loss element=" + str(element) \
                       + " terminal=1 mode=9 enabled=Yes"

            #logger.debug("Starting Monitor 1  - " + Command1)
            #logger.debug("Starting Monitor 2  - " + Command2)
            #logger.debug("Starting Monitor 3  - " + Command3)
            Rede.dssText.Command = Command1
            Rede.dssText.Command = Command2
            Rede.dssText.Command = Command3

def Define_Random_Monior_Test(Rede, description, element, terminal, mode):

    Command = "New monitor." + str(description) + "_" + str(element.split('.')[1]) + " element=" \
              + str(element) + " terminal=" + str(terminal) + " mode=" + str(mode) + " enabled=Yes"

    logger.debug("Define_Random_Monior_Test - " + Command)
    Rede.dssText.Command = Command

def Export_Random_Monitor_Test(Rede, description, element):

    Command = "Export monitors " + str(description) + "_" + str(element.split('.')[1]) + " " \
                "file = " + Debug_Path + "\\" + str(description) + "_" + str(element.split('.')[1])

    logger.debug("Export_Random_Monitor_Test - " + Command)
    Rede.dssText.Command = Command

def Move_Files():

    import os

    for file in os.listdir(Rede_Path):

        if 'Mon' in file.split("_"):

            os.remove(os.path.join(Debug_Path, file.replace(file.split("_")[0], ""))) \
                if file.replace(file.split("_")[0], "") in os.listdir(Debug_Path) else 0

            os.rename(file, Debug_Path + file.replace(file.split("_")[0], "\\"))


def Export_And_Read_Monitors_Data(Rede, Simulation):

    # 2022-04-10 16:11:52,858:Definitions:DEBUG: New = 11.477030754089355 Old = 80.24969696998596

    from Definitions import DF_Monitors_Data_2

    t1 = time.time()
    No_Monitor = Rede.dssMonitors.First

    while No_Monitor != 0:

        Name = Rede.dssMonitors.Name
        Element = Rede.dssMonitors.Element
        Rede.dssText.Command = "Export monitors " + str(Name)
        header = Rede.dssMonitors.Header

        for channel in range(len(header)):

            try:
                Data = Rede.dssMonitors.Channel(channel+1)
            except:
                Data = 'TBD'
                logger.info("Export_And_Read_Monitors_Data DEU RUIM - " + Name + " : " +
                            Element + " " + str(header) + " ")

            temp_df = pd.DataFrame({'Case'           : len(Casos) if Casos != [] else 0,
                                    'Simulation'     : Simulation,
                                    'Monitor'        : Name,
                                    'Elemento'       : Element,
                                    'TimeStep'       : range(0, len(Data)),
                                    'Measurement'    : header[channel],
                                    'Value'          : Data})

            DF_Monitors_Data_2 = pd.concat([DF_Monitors_Data_2, temp_df], ignore_index=True)

        logger.debug("Evaluating monitor : " + str(Name))
        No_Monitor = Rede.dssMonitors.Next

    logger.debug("Export_And_Read_Monitors_Data took {" + str(time.time() - t1) + " sec} to execulte")

    # REMOVER ESSE RETURN
    return DF_Monitors_Data_2

def AtivarMonitor(Rede, mon):

    Rede.dssCktElement.Name = str(mon)



def Export_And_Read_Monitors_Data_Old(Rede, Lista_Monitores, Simulation):

    # Fazer isso sem exportar para arquivos
    t1 = time.time()

    from Definitions import DF_Monitors_Power_Values, DF_Monitors_Voltage_Values
    from FunctionsSecond import Limpar_DF, originalSteps


    Lista_Monitores = Lista_Monitores["Elemento_com_monitor"].values # erro aquu
    # solução com pandas

    Lista = []
    count = 0

    for elem in Lista_Monitores:
        if elem.split('.')[0] != 'Monitor':
            Lista.append(elem)

    Limpar_DF(DF_Monitors_Data)


    for element in Lista:

        Export(Rede, element)
        Move_Files()

        [Limpar_DF(DF) for DF in [DF_Monitors_Power_Values, DF_Monitors_Voltage_Values]]



        # Medição de corrente?

        DF_Monitors_Power_Values = pd.read_csv(
            Debug_Path + "\_Mon_" + str(element.replace('.', '_')) + "_power_1.csv")

        DF_Monitors_Voltage_Values = pd.read_csv(
            Debug_Path + "\_Mon_" + str(element.replace('.', '_')) + "_voltage_1.csv")

        DF_Monitors_loss_Values = pd.read_csv(
            Debug_Path + "\_Mon_" + str(element.replace('.', '_')) + "_loss_1.csv")

        Columns_Power_Names = DF_Monitors_Power_Values.columns.values[2:]
        Columns_Voltage_Names = DF_Monitors_Voltage_Values.columns.values[2:]
        Columns_loss_Names = DF_Monitors_loss_Values.columns.values[2:]

        Columns = []
        [Columns.append(Col) for Col in Columns_Power_Names]
        [Columns.append(Col) for Col in Columns_Voltage_Names]
        [Columns.append(Col) for Col in Columns_loss_Names]

        for Meas in Columns:
            index = len(DF_Monitors_Data)
            DF_Monitors_Data.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
            DF_Monitors_Data.loc[index, 'Simulation'] = Simulation
            DF_Monitors_Data.loc[index, 'Elemento'] = str(element.replace('.', '_'))
            DF_Monitors_Data.loc[index, 'Measurement'] = Meas

            if Meas in Columns_Power_Names:

                for i in range(originalSteps(Rede)):
                    val = float(DF_Monitors_Power_Values.loc[i, Meas])
                    if type(val) == str:
                        print(val)
                    if val < -1.51756E035:
                    #if type(val) == str or val < -1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = -1.51756E035
                    elif val > 1.51756E035:
                    #elif type(val) == str or val > 1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = 1.51756E035
                    else:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = val

            elif Meas in Columns_Voltage_Names:

                for i in range(originalSteps(Rede)):
                    val = float(DF_Monitors_Voltage_Values.loc[i, Meas])
                    if type(val) == str:
                        print(val)
                    if val < -1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = -1.51756E035
                    elif val > 1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = 1.51756E035
                    else:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = val

            elif Meas in Columns_loss_Names:

                for i in range(originalSteps(Rede)):
                    val = float(DF_Monitors_loss_Values.loc[i, Meas])
                    if type(val) == str:
                        print(val)
                    if val < -1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = -1.51756E035
                    elif val > 1.51756E035:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = 1.51756E035
                    else:
                        DF_Monitors_Data.loc[index, 'Time_' + str(i)] = val
            else:
                print("Medição não presente nos arquivos - Export_And_Read_Monitors_Data()")
                logger.info("Export_And_Read_Monitors_Data - Medição não presente nos arquivos"
                            " - Export_And_Read_Monitors_Data()")

        count += 1

    logger.debug("Export_And_Read_Monitors_Data2 took {" + str(time.time() - t1) + " sec} to execulte")

def Export(Rede, element):

    logger.debug("Export_And_Read_Monitors_Data - "
                 "Exporting Monitor -> monitor." + str(element.replace('.', '_')))

    Rede.dssText.Command = "Export monitors " + str(element.replace('.', '_')) + "_power"
    Rede.dssText.Command = "Export monitors " + str(element.replace('.', '_')) + "_voltage"
    Rede.dssText.Command = "Export monitors " + str(element.replace('.', '_')) + "_loss"


    logger.debug("Export_And_Read_Monitors_Data - "
                 "Exported Monitor -> monitor." + str(element.replace('.', '_')))

def Debug_Loads(Rede, Simulation):

    #if os.path.isfile(Debug_Path + "/Debug_Load.txt") is True and Simulation == 1:
    #    os.remove(Debug_Path + "/Debug_Load.txt")

    file = open(Debug_Path + "/Debug_Load.txt", 'a')

    for load in Rede.dssLoads.AllNames:
        Rede.dssLoads.Name = load
        file.write(str(Simulation) + ", " + str(Rede.dssLoads.Name) + ", " + str(Rede.dssLoads.Model) + "\n")

    # não muda a definição do modelo, pode ser que mude internamente... mas a definição não