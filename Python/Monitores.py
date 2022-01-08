# coding: utf-8
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

    for element in Lista_Monitores:
        Rede.dssText.Command = "New monitor." + str(element.split('.')[1]) + "_power element=" + str(element) + \
                               " terminal=1 mode=1 ppolar=no"
        Rede.dssText.Command = "New monitor." + str(element.split('.')[1]) + "_voltage element=" + str(element) \
                               + " terminal=1 mode=0"

def Define_Random_Monior_Test(Rede, description, element, terminal, mode):
    print(description)
    Rede.dssText.Command = "New monitor." + str(description) + "_" + str(element.split('.')[1]) + " element=" \
                           + str(element) + " terminal=" + str(terminal) + " mode=" + str(mode)

def Export_Random_Monitor_Test(Rede, description, element):
    print(description + "2")
    Rede.dssText.Command = "Export monitors " + str(description) + "_" + str(element.split('.')[1]) + " " \
                          "file = " + Debug_Path + "\\" + str(description) + "_" + str(element.split('.')[1])

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
        Rede.dssText.Command = "Export monitors " + str(element.split('.')[1]) + "_power"
        Rede.dssText.Command = "Export monitors " + str(element.split('.')[1]) + "_voltage"

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
