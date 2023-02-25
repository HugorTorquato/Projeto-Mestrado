# coding: utf-8
import os

import numpy as np

from Definitions import *
import pandas as pd
import time

def Adicionar_Monitores(Rede2):

    # Se precisar adicionar algum monitor no circuito, basta replicar a linha seguinte refasendo a atribuição de
    # valor. Lembrar que o comando de criação do monitor necessita do tipo de elemento para determinar o parametro
    # "element" da declaração, mas o nome do monitor não precisa... Basta seguir o padrão :
    #                                                                       <TIPO>.<NOME_ELEMENTO>

    from FunctionsSecond import Limpar_DF, GetAllElemtfNames

    Limpar_DF(DF_Lista_Monitors)

    #DF_Lista_Monitors.loc[len(DF_Lista_Monitors), "Elemento_com_monitor"] = "line." + str(Rede.dssLines.AllNames[0])
    for element in GetAllElemtfNames(Rede2):
        if element.split('.')[0] != 'Monitor':
            DF_Lista_Monitors.loc[len(DF_Lista_Monitors), "Elemento_com_monitor"] = element
    # ...

    Define_Monitor(Rede2, DF_Lista_Monitors["Elemento_com_monitor"].values)

    #Define_Monitor(Rede, Rede.dssCircuit.AllElementNames)

def Define_Monitor(Rede2, Lista_Monitores):

    # Atualmente são definidos3 tipos de monitores por elemento:
    # -> modelo 1 -> Medidores de Pot ( Atia e Reativa )
    # -> modelo 2 -> Medidores de V & I (Tensão e corrente )
    # -> modelo 3 -> Medidores de loss (Perdas por elemento )
    #
    # Se adicionar mais algum modelo, lembrar de modificar a função "Export_And_Read_Monitors_Data", ela vai salvar e
    # ler os arquivos depois de cada simulação, e a implementação é baseada nem dois modelos de medidores. Se Adicionar
    # mais um, tem de adicionar lá também.

    logger.debug("Starting Monitors")
    for element in Lista_Monitores:
        Command = []

        if element.split('.')[1].startswith("fakeload"):
            Command.append("New monitor." + str(element.replace('.', '_')) + "_voltage element=" + str(element) \
                       + " terminal=1 mode=0 enabled=Yes")
        elif element.split('.')[0] != 'Monitor':
            Command.append("New monitor." + str(element.replace('.', '_')) + "_power element=" + str(element) \
                       + " terminal=1 mode=1 ppolar=no enabled=Yes")
            Command.append("New monitor." + str(element.replace('.', '_')) + "_voltage element=" + str(element) \
                       + " terminal=1 mode=0 enabled=Yes")
            Command.append("New monitor." + str(element.replace('.', '_')) + "_loss element=" + str(element) \
                       + " terminal=1 mode=9 enabled=Yes")

            #logger.debug("Starting Monitor 1  - " + Command1)
            #logger.debug("Starting Monitor 2  - " + Command2)
            #logger.debug("Starting Monitor 3  - " + Command3)
            #Rede.dssText.Command = Command1
            #Rede.dssText.Command = Command2
            #Rede.dssText.Command = Command3
        [Rede2.text(Cmd) for Cmd in Command]

def Define_Random_Monior_Test(Rede2, description, element, terminal, mode):

    Command = "New monitor." + str(description) + "_" + str(element.split('.')[1]) + " element=" \
              + str(element) + " terminal=" + str(terminal) + " mode=" + str(mode) + " enabled=Yes"

    logger.debug("Define_Random_Monior_Test - " + Command)
    Rede2.text(Command)

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


def Export_And_Read_Monitors_Data2(Rede2, Simulation):

    t1 = time.time()
    from Definitions import DF_Monitors_Data_2
    from FunctionsSecond import IEC, ativa_barra
    from DB_Rede import Save_Data
    import sqlalchemy as sql

    No_Monitor = Rede2.monitors_first()
    header_after_filtering = Remove_Measurament

    while No_Monitor != 0:
        Name = Rede2.monitors_read_name()
        Element = Rede2.monitors_read_element()

        if Element.split('.')[0].startswith("reactor"):
            No_Monitor = Rede2.monitors_next()
            continue

        header = Rede2.monitors_header()

        V1  = []
        V1A = []
        V2  = []
        V2A = []
        V3  = []
        V3A = []

        for channel in range(len(header)):
            if header[channel] not in header_after_filtering:
                try:
                    Data = Rede2.monitors_channel(header.index(header[channel]) + 1) if header[channel] in header else []

                    if Element.split('.')[1].startswith("fakeload"):
                        V1  = Data if ' V1' == header[channel] else V1
                        V1A = Data if ' VAngle1' == header[channel] else V1A
                        V2  = Data if ' V2' == header[channel] else V2
                        V2A = Data if ' VAngle2' == header[channel] else V2A
                        V3  = Data if ' V3' == header[channel] else V3
                        V3A = Data if ' VAngle3' == header[channel] else V3A

                except:
                    logger.info("Export_And_Read_Monitors_Data DEU RUIM - " + Name + " : " +
                                Element + " " + str(header) + " ")

                temp_df = pd.DataFrame({'Case'           : len(Casos) if Casos != [] else 0,
                                        'Simulation'     : Simulation,
                                        'Monitor'        : Name,
                                        'Elemento'       : Element,
                                        'TimeStep'       : range(0, len(Data)),
                                        'Measurement'    : str(header[channel]),
                                        'Value'          : Data})
                try:
                    DF_Monitors_Data_2 = pd.concat([DF_Monitors_Data_2, temp_df], ignore_index=True)
                except:
                    logger.info("Export_And_Read_Monitors_Data DEU RUIM 2 - ")
                    logger.info(DF_Monitors_Data_2.head())
                    logger.info(temp_df.head())

        if Element.split('.')[1].startswith("fakeload"):

            # Calcular desequilibrio
            bus = Element.replace("load_fakeload_", "").replace("_voltage", "")
            ativa_barra(Rede2, bus)
            kvbase = Rede2.bus_kv_base()

            Data = IEC(V1, V2, V3, V1A, V2A, V3A, Rede2, kvbase * 1000)
            Element = Name.replace("load_fakeload_", "").replace("_voltage", "")
            Measurement = UnbalanceType.IEC.name

            temp_df = pd.DataFrame({'Case'           : len(Casos) if Casos != [] else 0,
                                    'Simulation'     : Simulation,
                                    'Monitor'        : Name,
                                    'Elemento'       : Element,
                                    'TimeStep'       : range(0, len(Data)),
                                    'Measurement'    : Measurement,
                                    'Value'          : Data})

            try:
                DF_Monitors_Data_2 = pd.concat([DF_Monitors_Data_2, temp_df], ignore_index=True)
            except:
                logger.info("Export_And_Read_Monitors_Data DEU RUIM 3 - ")
                logger.info(DF_Monitors_Data_2.head())
                logger.info(temp_df.head())

        logger.debug("Evaluating monitor : " + str(Name))
        No_Monitor = Rede2.monitors_next()

    logger.debug("Export_And_Read_Monitors_Data2 took {" + str(time.time() - t1) + " sec} to execulte")

    return DF_Monitors_Data_2


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
        header_after_filtering = Remove_Measurament

        for channel in range(len(header)):
            if header[channel] not in header_after_filtering:
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
