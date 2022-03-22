# coding: utf-8
import os

from Definitions import *
import pandas as pd

def Adicionar_Monitores(Rede):

    # Se precisar adicionar algum monitor no circuito, basta replicar a linha seguinte refasendo a atribuição de
    # valor. Lembrar que o comando de criação do monitor necessita do tipo de elemento para determinar o parametro
    # "element" da declaração, mas o nome do monitor não precisa... Basta seguir o padrão :
    #                                                                       <TIPO>.<NOME_ELEMENTO>

    DF_Lista_Monitors.loc[len(DF_Lista_Monitors), "Elemento_com_monitor"] = "line." + str(Rede.dssLines.AllNames[0])
    # ...

    Define_Monitor(Rede, DF_Lista_Monitors["Elemento_com_monitor"].values)

def Define_Monitor(Rede, Lista_Monitores):

    # Atualmente são definidos dois tipos de monitores por elemento:
    # -> modelo 1 -> Medidores de Pot ( Atia e Reativa )
    # -> modelo 2 -> Medidores de V & I (Tensão e corrente )
    #
    # Se adicionar mais algum modelo, lembrar de modificar a função "Export_And_Read_Monitors_Data", ela vai salvar e
    # ler os arquivos depois de cada simulação, e a implementação é baseada nem dois modelos de medidores. Se Adicionar
    # maisum, tem de adicionar lá também.

    logger.debug("Starting Monitors")
    for element in Lista_Monitores:

        Command1 = "New monitor." + str(element.split('.')[1]) + "_power element=" + str(element) + \
                   " terminal=1 mode=1 ppolar=no"
        Command2 = "New monitor." + str(element.split('.')[1]) + "_voltage element=" + str(element) \
                   + " terminal=1 mode=0"

        logger.debug("Starting Monitor 1  - " + Command1)
        logger.debug("Starting Monitor 2  - " + Command2)
        Rede.dssText.Command = Command1
        Rede.dssText.Command = Command2
        logger.debug("Started Monitor -> monitor." + element)

def Define_Random_Monior_Test(Rede, description, element, terminal, mode):

    Command = "New monitor." + str(description) + "_" + str(element.split('.')[1]) + " element=" \
              + str(element) + " terminal=" + str(terminal) + " mode=" + str(mode)

    logger.debug("Define_Random_Monior_Test - " + Command)
    Rede.dssText.Command = Command
    logger.debug("Define_Random_Monior_Test - Started Random Monitor -> monitor." + description)

def Export_Random_Monitor_Test(Rede, description, element):

    Command = "Export monitors " + str(description) + "_" + str(element.split('.')[1]) + " " \
                "file = " + Debug_Path + "\\" + str(description) + "_" + str(element.split('.')[1])

    logger.debug("Export_Random_Monitor_Test - " + Command)
    Rede.dssText.Command = Command
    logger.debug("Export_Random_Monitor_Test - Exported Random Monitor -> monitor." + description)

def Move_Files():

    import os

    for file in os.listdir(Rede_Path):

        if 'Mon' in file.split("_"):

            os.remove(os.path.join(Debug_Path, file.replace(file.split("_")[0], ""))) \
                if file.replace(file.split("_")[0], "") in os.listdir(Debug_Path) else 0

            os.rename(file, Debug_Path + file.replace(file.split("_")[0], "\\"))

def Export_And_Read_Monitors_Data(Rede, Lista_Monitores, Simulation):

    from Definitions import DF_Monitors_Power_Values, DF_Monitors_Voltage_Values
    from FunctionsSecond import Limpar_DF, originalSteps


    Lista_Monitores = Lista_Monitores["Elemento_com_monitor"].values

    for element in Lista_Monitores:

        logger.debug("Export_And_Read_Monitors_Data - "
                     "Exporting Monitor -> monitor." + str(element.split('.')[1]))

        Rede.dssText.Command = "Export monitors " + str(element.split('.')[1]) + "_power"
        Rede.dssText.Command = "Export monitors " + str(element.split('.')[1]) + "_voltage"

        logger.debug("Export_And_Read_Monitors_Data - "
                     "Exported Monitor -> monitor." + str(element.split('.')[1]))

        Move_Files()

        [Limpar_DF(DF) for DF in [DF_Monitors_Power_Values, DF_Monitors_Voltage_Values, DF_Monitors_Data]]

        DF_Monitors_Power_Values = pd.read_csv(
            Debug_Path + "\_Mon_" + str(element.split('.')[1]) + "_power_1.csv")

        DF_Monitors_Voltage_Values = pd.read_csv(
            Debug_Path + "\_Mon_" + str(element.split('.')[1]) + "_voltage_1.csv")

        Columns_Power_Names = DF_Monitors_Power_Values.columns.values[2:]
        Columns_Voltage_Names = DF_Monitors_Voltage_Values.columns.values[2:]

        Columns = []
        [Columns.append(Col) for Col in Columns_Power_Names]
        [Columns.append(Col) for Col in Columns_Voltage_Names]

        for Meas in Columns:
            index = len(DF_Monitors_Data)
            DF_Monitors_Data.loc[index, 'Simulation'] = Simulation
            DF_Monitors_Data.loc[index, 'Elemento'] = str(element.split('.')[1])
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

            else:
                print("Medição não presente nos arquivos - Export_And_Read_Monitors_Data()")
                logger.info("Export_And_Read_Monitors_Data - Medição não presente nos arquivos"
                            " - Export_And_Read_Monitors_Data()")

        logger.debug("Export_And_Read_Monitors_Data - completed")


def Debug_Loads(Rede, Simulation):

    #if os.path.isfile(Debug_Path + "/Debug_Load.txt") is True and Simulation == 1:
    #    os.remove(Debug_Path + "/Debug_Load.txt")

    file = open(Debug_Path + "/Debug_Load.txt", 'a')

    for load in Rede.dssLoads.AllNames:
        Rede.dssLoads.Name = load
        file.write(str(Simulation) + ", " + str(Rede.dssLoads.Name) + ", " + str(Rede.dssLoads.Model) + "\n")

    # não muda a definição do modelo, pode ser que mude internamente... mas a definição não