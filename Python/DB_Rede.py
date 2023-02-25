import os
import sys

import pandas as pd
import sqlalchemy as sql
from Definitions import *
import time
from sqlalchemy import MetaData

from Definitions import logger


def sqlalchemy():

    engine = sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server').connect()

    return engine

def sqlalchemyengine():
    # I need to start changing this to use with to open and close conetions ( It is best practices )
    # In this case i'm duplicating this method to migrate it slowly

    return sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server')

def RunSQLDefinitions(engine, Rede2):

    t = time.time()
    t1 = time.time()
    TableFolder = SQL_Path + "\\Tables"
    ViewsFolder = SQL_Path + "\\Views"

    from FunctionsSecond import OrderFiles

    for filefromfolder in OrderFiles(os.listdir(TableFolder)):
        if (filefromfolder[2].startswith("sp") or filefromfolder[2].startswith("tbl"))\
                and filefromfolder[2] != "tblGeneral":
            try:
                if len(pd.read_sql(
                        'SELECT TABLE_NAME '
                        'FROM INFORMATION_SCHEMA.TABLES '
                        'WHERE TABLE_NAME = \'' + str(filefromfolder[2]) + '\'', engine)) != 0:
                    engine.execute('DBCC CHECKIDENT(\'' + str(filefromfolder[2]) + '\', RESEED, 0)')
                    engine.execute('DELETE FROM ' + str(filefromfolder[2]))
                    logger.info('Deleted Table :' + str(filefromfolder[0]))
            except Exception as e:
                print("!!!!!!!Deu ruim deletando a tabela : " + filefromfolder[0] + " >>>>>> CONFERIR LOGS ")
                logger.error("!!!!!!!Deu ruim deletando a tabela : " + filefromfolder[0] +
                             " com a seguinte mensagem de erro: " + str(e.args))
                logger.error("Mensagem detalhada do erro: \n" + str(e))
                sys.exit()

    try:
        if len(pd.read_sql(
                'SELECT TABLE_NAME '
                'FROM INFORMATION_SCHEMA.TABLES '
                'WHERE TABLE_NAME = \'tblGeneral\'', engine)) != 0:
            engine.execute('DBCC CHECKIDENT(\'tblGeneral\', RESEED, 0)')
            engine.execute('DELETE FROM tblGeneral')
            logger.info('Deleted Table :' + str("tblGeneral"))
    except Exception as e:
        print("!!!!!!!Deu ruim deletando a tabela : " + "tblGeneral" + " >>>>>> CONFERIR LOGS ")
        logger.error("!!!!!!!Deu ruim deletando a tabela : " + "tblGeneral" +
                     " com a seguinte mensagem de erro: " + str(e.args))
        logger.error("Mensagem detalhada do erro: \n" + str(e))
        sys.exit()

    for filefromfolder in OrderFiles(os.listdir(TableFolder)):
        with open(TableFolder + "\\" + filefromfolder[0]) as file:
            try:
                query = file.read()
                engine.execute(query)
                logger.info('Create Table :' + str(filefromfolder[0]))
                logger.debug("Create Table :" + str(filefromfolder[0] + " took {" + str(time.time() - t1) +
                                                    " sec} to execulte"))
            except Exception as e:
                print("!!!!!!!Deu ruim na tabela : " + filefromfolder[0] + " >>>>>> CONFERIR LOGS ")
                logger.error("!!!!!!!Deu ruim na tabela : " + filefromfolder[0] +
                             " com a seguinte mensagem de erro: " + str(e.args))
                logger.error("Mensagem detalhada do erro: \n" + str(e))
                sys.exit()

    logger.info("Finish creating tables")
    logger.debug("RunTablesDefinitions took {" + str(time.time() - t1) + " sec} to execulte")

    t1 = time.time()

    for filefromfolder in os.listdir(ViewsFolder):
        with open(ViewsFolder + "\\" + filefromfolder) as file:
            try:
                query = sql.text(file.read())
                engine.execute(query)
                logger.info('Create Views :' + str(filefromfolder))
                logger.debug("Create Views :" + str(filefromfolder + " took {" + str(time.time() - t1) +
                                                    " sec} to execulte"))
            except Exception as e:
                print("!!!!!!!Deu ruim na Views : " + filefromfolder + " >>>>>> CONFERIR LOGS ")
                logger.error("!!!!!!!Deu ruim na Views : " + filefromfolder +
                             " com a seguinte mensagem de erro: " + str(e.args))
                logger.error("Mensagem detalhada do erro: \n" + str(e))
                sys.exit()

    logger.info("Finish creating Views")
    logger.debug("RunViewsDefinitions took {" + str(time.time() - t1) + " sec} to execulte")

    t1 = time.time()
    Folder = SQL_Path + "\\StoredProcedures"
    for filefromfolder in os.listdir(Folder):
        with open(Folder + "\\" + filefromfolder) as file:
            try:
                query = sql.text(file.read())
                engine.execute(query)
                logger.info('Create StoredProcedures :' + str(filefromfolder))
                logger.debug("Create StoredProcedures :" + str(filefromfolder + " took {" + str(time.time() - t1) +
                                                               " sec} to execulte"))
            except Exception as e:
                print("!!!!!!!Deu ruim na StoredProcedures : " + filefromfolder + " >>>>>> CONFERIR LOGS ")
                logger.error("!!!!!!!Deu ruim na StoredProcedures : " + filefromfolder +
                             " com a seguinte mensagem de erro: " + str(e.args))
                logger.error("Mensagem detalhada do erro: \n" + str(e))
                sys.exit()

    # I'll have to leave it here because this definition is dynamic, depends on originalSteps(Rede)
    Adjust_tables_to_timestemp(engine, Rede2)
    Refresh_Or_Create_StoreProcedures(engine, Rede2)
    logger.debug("RunStoredProceduresDefinitions took {" + str(time.time() - t1) + " sec} to execulte")

    logger.debug("RunSQLDefinitions took {" + str(time.time() - t) + " sec} to execulte")
    print("SQL Definitions completed")

def Refresh_Or_Create_StoreProcedures(engine, Rede2):

    from FunctionsSecond import Return_Time_String_Colum, Return_Time_String_Colum_Case_Options

    # Lembrar de adicionar os SP da pasta ###############################################################

    storeProcedure = 'spUpdate_Voltage_Data_Table_Max_Min'
    Ary = Return_Time_String_Colum(Rede2)

    if len(pd.read_sql(
        'SELECT * '
        'FROM sys.objects '
        'where [type] = \'P\' and [name]  = \'' + storeProcedure + '\'', engine)) == 0:

        Definition = 'CREATE PROCEDURE ' + storeProcedure + \
                     ' AS ' \
                     '  UPDATE VD ' \
                     '  SET ' \
                     '      VD.ValueMaxPU = (SELECT (select MAX(Barra) from (VALUES ' + str(Ary) + ') as Maior(Barra))'\
                     '                          as Maior' \
                     '                          FROM tblVoltage_Data VD2 WHERE VD.Nome_ID = VD2.Nome_ID),' \
                     '      VD.ValueMinPU = (SELECT (select ISNULL(MIN(Barra), 0) from (VALUES ' + str(Ary) + ')' \
                     '                               as Menor(Barra)' \
                     '                               where Barra > 0.5) as Menor' \
                     '                          FROM tblVoltage_Data VD3 WHERE VD.Nome_ID = VD3.Nome_ID) ' \
                     '  FROM tblVoltage_Data AS VD'

        engine.execute(Definition)
        logger.info('Create StoreProcedure :' + str(storeProcedure))
    else:
        logger.info('StoreProcedure already exists :' + str(storeProcedure))

    storeProcedure = 'spUpdate_Voltage_Data_Table_Max_Min_Time_Value'
    AryMax = Return_Time_String_Colum_Case_Options(Rede2)[0]
    AryMin = Return_Time_String_Colum_Case_Options(Rede2)[1]

    if len(pd.read_sql(
            'SELECT * '
            'FROM sys.objects '
            'where [type] = \'P\' and [name]  = \'' + storeProcedure + '\'', engine)) == 0:

        Definition = 'CREATE PROCEDURE ' + storeProcedure + \
                     ' AS ' \
                     '  UPDATE VD ' \
                     '  SET ' \
                     '  VD.TimeMaxPU = CASE ' + AryMax + ' ELSE \'TBD\' END,' \
                     '  VD.TimeMinPU = CASE ' + AryMin + ' ELSE \'TBD\' END' \
                     ' FROM tblVoltage_Data VD'


        engine.execute(Definition)
        logger.info('Create StoreProcedure :' + str(storeProcedure))
    else:
        logger.info('StoreProcedure already exists :' + str(storeProcedure))

def Adjust_tables_to_timestemp(engine, Rede2):

    from FunctionsSecond import originalSteps

    # Case queira salvar dados em todos os intervalos de simulação, tem de adicionar o nome da tabela destino
    # o seguinte vetor. A ideia dessa função consiste em adicionar N colunas com que irá possíbilitar salvar
    # todos os valores presentes em um dia

    DB = ['tblCurrent_Elemt_Data', 'tblCurrent_Elemt_Data_Ang', 'tblVoltage_Data',
          'tblVoltage_Data_Ang', 'tblUnbalance_Data']

    for table in DB:
        if pd.read_sql('SELECT COUNT(COLUMN_NAME) AS resultado FROM INFORMATION_SCHEMA.COLUMNS '
                       'WHERE TABLE_NAME = \'' + str(table) + '\' AND  COLUMN_NAME = \'Time_1\'', engine).values == 0:

            for i in range(originalSteps(Rede2)):
                engine.execute("ALTER TABLE " + table + " ADD Time_" + str(i) + " float(53)")

def Save_Data(DF_Monitors_Data_2):

    # Before improvements
    #2022-04-10 17:33:10,722:Definitions:DEBUG:Save_Data took {207.72897791862488 sec} to execulte
    # After improvements
    #

    from Definitions import DF_Geradores, DF_General, DF_Barras, DF_Elements, DF_PV,\
        DF_Check_Report, DF_Current_Data, DF_Violations_Data

    t1 = time.time()
    
    DF_General.to_sql('tblGeneral', sqlalchemy(), if_exists='append', index=False)
    DF_PV.to_sql('tblPVSystems', sqlalchemy(), if_exists='append', index=False)
    #DF_Geradores.to_sql('tblGD', sqlalchemy(), if_exists='append', index=False)

    #DF_Barras.to_sql('tblBarras', sqlalchemy(), if_exists='append', index=False)
    #DF_Elements.to_sql('tblGrid_Elements', sqlalchemy(), if_exists='append', index=False)
    DF_Check_Report.to_sql('tblCheck_Report', sqlalchemy(), if_exists='append', index=False)
    DF_Violations_Data.to_sql('tblViolations_Data', sqlalchemy(), if_exists='append', index=False)

    # Corrigir essa ref -> Por algum motivo não está sendo armazenada a global

    #DF_Voltage_Data.to_sql('tblVoltage_Data', sqlalchemy(), if_exists='append', index=False)
    #DF_Tensao_Data_Ang.to_sql('tblVoltage_Data_Ang', sqlalchemy(), if_exists='append', index=False)
    #DF_Unbalance_Data.to_sql('tblUnbalance_Data', sqlalchemy(), if_exists='append', index=False)
    #DF_Current_Data.to_sql('tblCurrent_Elemt_Data', sqlalchemy(), if_exists='append', index=False)
    #DF_Current_Elemt_Data_Ang.to_sql('tblCurrent_Elemt_Data_Ang', sqlalchemy(), if_exists='append', index=False)

    DF_Monitors_Data_2.to_sql('tblMonitoresData', sqlalchemy(), if_exists='append', index=False)

    logger.debug("Save_Data took {" + str(time.time() - t1) + " sec} to execulte")

def Save_General_Data(Simulation):

    from FunctionsSecond import Max_and_Min_Voltage_DF
    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Geradores, DF_General, Casos

    t1 = time.time()

    DF_General.loc[0, 'Case'] = len(Casos) if Casos != [] else 0
    DF_General.loc[0, 'SimulationCount'] = Simulation
    DF_General.loc[0, 'Voltage_Max'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]
    DF_General.loc[0, 'Voltage_Min'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]
    DF_General.loc[0, 'GD_Config'] = str(DF_Geradores.set_index('Name').values)

    logger.debug("Save_General_Data took {" + str(time.time() - t1) + " sec} to execulte")

def Run_Store_Procedures():

    # Run all store procedures frim the list by the end of the Simulation

    t1 = time.time()
    SPs = ['spUpdate_Voltage_Data_Table_Max_Min', 'spUpdate_Voltage_Data_Table_Max_Min_Time_Value']

    for SP in SPs:
        t2 = time.time()
        sqlalchemy().execute(SP)
        logger.debug("Store Procedure " + SP + " took {" + str(time.time() - t1) + " sec} to execulte")

    logger.debug("Save_General_Data took {" + str(time.time() - t1) + " sec} to execulte")

def Process_Data(Simulation, DF_Monitors_Data_2):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Barras, DF_Desq_IEC, DF_Desq_IEEE,\
        DF_Desq_NEMA, DF_Corrente_A, DF_Corrente_B, DF_Corrente_C, DF_Elements, DF_Voltage_Data, DF_Current_Data,\
        DF_Tensao_Ang_A, DF_Tensao_Ang_B, DF_Tensao_Ang_C, DF_Corrente_Ang_A, DF_Corrente_Ang_B, DF_Corrente_Ang_C,\
        Savar_Dados_Elem, Casos
    from FunctionsSecond import Adjust_Colum_Name

    t1 = time.time()

    # Process Bus
    index = len(DF_Barras.index)

    for Barra in DF_Tensao_A.Barras.values:
        DF_Barras.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
        DF_Barras.loc[index, 'Simulation'] = Simulation
        DF_Barras.loc[index, 'Name'] = Barra
        DF_Barras.loc[index, 'V_pu_max_a'] = max(DF_Tensao_A.set_index('Barras').loc[[str(Barra)]].max())
        DF_Barras.loc[index, 'V_pu_max_b'] = max(DF_Tensao_B.set_index('Barras').loc[[str(Barra)]].max())
        DF_Barras.loc[index, 'V_pu_max_c'] = max(DF_Tensao_C.set_index('Barras').loc[[str(Barra)]].max())
        DF_Barras.loc[index, 'V_pu_min_a'] = min(DF_Tensao_A.set_index('Barras').loc[[str(Barra)]].min())
        DF_Barras.loc[index, 'V_pu_min_b'] = min(DF_Tensao_B.set_index('Barras').loc[[str(Barra)]].min())
        DF_Barras.loc[index, 'V_pu_min_c'] = min(DF_Tensao_C.set_index('Barras').loc[[str(Barra)]].min())
        DF_Barras.loc[index, 'Deseq_IEC' ] = max(DF_Desq_IEC.set_index('Barras').loc[[str(Barra)]].min())
        DF_Barras.loc[index, 'Deseq_IEEE'] = max(DF_Desq_IEEE.set_index('Barras').loc[[str(Barra)]].min())
        DF_Barras.loc[index, 'Deseq_NEMA'] = max(DF_Desq_NEMA.set_index('Barras').loc[[str(Barra)]].min())

        index += 1

    # Process Elements
    index = len(DF_Elements.index)

    for Elem in DF_Corrente_A.Elementos.values:
        DF_Elements.loc[index, 'Case'] = len(Casos) if Casos != [] else 0
        DF_Elements.loc[index, 'Simulation'] = Simulation
        DF_Elements.loc[index, 'Elemento'] = Elem
        DF_Elements.loc[index, 'I_pu_max_a'] = max(DF_Corrente_A.set_index('Elementos').loc[[str(Elem)]].max())
        DF_Elements.loc[index, 'I_pu_max_b'] = max(DF_Corrente_B.set_index('Elementos').loc[[str(Elem)]].max())
        DF_Elements.loc[index, 'I_pu_max_c'] = max(DF_Corrente_C.set_index('Elementos').loc[[str(Elem)]].max())
        DF_Elements.loc[index, 'I_pu_min_a'] = min(DF_Corrente_A.set_index('Elementos').loc[[str(Elem)]].min())
        DF_Elements.loc[index, 'I_pu_min_b'] = min(DF_Corrente_B.set_index('Elementos').loc[[str(Elem)]].min())
        DF_Elements.loc[index, 'I_pu_min_c'] = min(DF_Corrente_C.set_index('Elementos').loc[[str(Elem)]].min())

        index += 1

    # Process Bus Voltages in each simulation
    global DF_Voltage_Data
    DF_Tensao_A_Temp = DF_Tensao_A.copy(deep=True)
    DF_Tensao_B_Temp = DF_Tensao_B.copy(deep=True)
    DF_Tensao_C_Temp = DF_Tensao_C.copy(deep=True)

    DF_Tensao_A_Temp.columns = Adjust_Colum_Name(DF_Tensao_A_Temp)
    DF_Tensao_B_Temp.columns = Adjust_Colum_Name(DF_Tensao_B_Temp)
    DF_Tensao_C_Temp.columns = Adjust_Colum_Name(DF_Tensao_C_Temp)

    DF_Tensao_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Tensao_A_Temp else 0
    DF_Tensao_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Tensao_B_Temp else 0
    DF_Tensao_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Tensao_C_Temp else 0

    DF_Voltage_Data = pd.concat([DF_Tensao_A_Temp, DF_Tensao_B_Temp, DF_Tensao_C_Temp])

    DF_Voltage_Data.insert(loc=0, column='Case', value=len(Casos) if Casos != [] else 0)
    DF_Voltage_Data.insert(loc=1, column='Simulation', value=Simulation)
    # Exemplo de como adicionar elementos nulos em uma coluna nula
    DF_Voltage_Data.insert(loc=4, column='TimeMaxPU', value='')
    DF_Voltage_Data.insert(loc=5, column='ValueMaxPU', value=0)
    DF_Voltage_Data.insert(loc=6, column='TimeMinPU', value='')
    DF_Voltage_Data.insert(loc=7, column='ValueMinPU', value=0)

    # Process Element Currents Angle in each simulation
    global DF_Voltage_Data_Ang
    DF_Tensao_Ang_A_Temp = DF_Tensao_Ang_A.copy(deep=True)
    DF_Tensao_Ang_B_Temp = DF_Tensao_Ang_B.copy(deep=True)
    DF_Tensao_Ang_C_Temp = DF_Tensao_Ang_C.copy(deep=True)

    DF_Tensao_Ang_A_Temp.columns = Adjust_Colum_Name(DF_Tensao_Ang_A_Temp)
    DF_Tensao_Ang_B_Temp.columns = Adjust_Colum_Name(DF_Tensao_Ang_B_Temp)
    DF_Tensao_Ang_C_Temp.columns = Adjust_Colum_Name(DF_Tensao_Ang_C_Temp)

    DF_Tensao_Ang_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Tensao_Ang_A_Temp else 0
    DF_Tensao_Ang_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Tensao_Ang_B_Temp else 0
    DF_Tensao_Ang_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Tensao_Ang_C_Temp else 0

    DF_Tensao_Data_Ang = pd.concat([DF_Tensao_Ang_A_Temp, DF_Tensao_Ang_B_Temp, DF_Tensao_Ang_C_Temp])

    DF_Tensao_Data_Ang.insert(loc=0, column='Case', value=len(Casos) if Casos != [] else 0)
    DF_Tensao_Data_Ang.insert(loc=1, column='Simulation', value=Simulation)

    # Process Bus Unbalance in each simulation
    global DF_Unbalance_Data
    DF_Desq_IEC_Temp = DF_Desq_IEC.copy(deep=True)
    DF_Desq_IEEE_Temp = DF_Desq_IEEE.copy(deep=True)
    DF_Desq_NEMA_Temp = DF_Desq_NEMA.copy(deep=True)

    DF_Desq_IEC_Temp.columns = Adjust_Colum_Name(DF_Desq_IEC_Temp)
    DF_Desq_IEEE_Temp.columns = Adjust_Colum_Name(DF_Desq_IEEE_Temp)
    DF_Desq_NEMA_Temp.columns = Adjust_Colum_Name(DF_Desq_NEMA_Temp)

    DF_Desq_IEC_Temp.insert(loc=1, column='Descr', value='IEC') \
        if 'Descr' not in DF_Desq_IEC_Temp else 0
    DF_Desq_IEEE_Temp.insert(loc=1, column='Descr', value='IEEE') \
        if 'Descr' not in DF_Desq_IEEE_Temp else 0
    DF_Desq_NEMA_Temp.insert(loc=1, column='Descr', value='NEMA') \
        if 'Descr' not in DF_Desq_NEMA_Temp else 0

    DF_Unbalance_Data = pd.concat([DF_Desq_IEC_Temp, DF_Desq_IEEE_Temp, DF_Desq_NEMA_Temp])
    DF_Unbalance_Data.insert(loc=0, column='Case', value=len(Casos) if Casos != [] else 0)
    DF_Unbalance_Data.insert(loc=1, column='Simulation', value=Simulation)

    if Remove == 0:
        # Process Element Currents in each simulation
        global DF_Current_Data
        DF_Corrente_A_Temp = DF_Corrente_A.copy(deep=True)
        DF_Corrente_B_Temp = DF_Corrente_B.copy(deep=True)
        DF_Corrente_C_Temp = DF_Corrente_C.copy(deep=True)

        DF_Corrente_A_Temp.columns = Adjust_Colum_Name(DF_Corrente_A_Temp)
        DF_Corrente_B_Temp.columns = Adjust_Colum_Name(DF_Corrente_B_Temp)
        DF_Corrente_C_Temp.columns = Adjust_Colum_Name(DF_Corrente_C_Temp)

        DF_Corrente_A_Temp.insert(loc=1, column='Fase', value='A') \
            if 'Fase' not in DF_Corrente_A_Temp else 0
        DF_Corrente_B_Temp.insert(loc=1, column='Fase', value='B') \
            if 'Fase' not in DF_Corrente_B_Temp else 0
        DF_Corrente_C_Temp.insert(loc=1, column='Fase', value='C') \
            if 'Fase' not in DF_Corrente_C_Temp else 0

        DF_Corrente_Data = pd.concat([DF_Corrente_A_Temp, DF_Corrente_B_Temp, DF_Corrente_C_Temp])

        DF_Corrente_Data.insert(loc=0, column='Case', value=len(Casos) if Casos != [] else 0)
        DF_Corrente_Data.insert(loc=1, column='Simulation', value=Simulation)

    if Remove == 0:
        # Process Element Currents Angle in each simulation
        global DF_Current_Elemt_Data_Ang
        DF_Corrente_Ang_A_Temp = DF_Corrente_Ang_A.copy(deep=True)
        DF_Corrente_Ang_B_Temp = DF_Corrente_Ang_B.copy(deep=True)
        DF_Corrente_Ang_C_Temp = DF_Corrente_Ang_C.copy(deep=True)

        DF_Corrente_Ang_A_Temp.columns = Adjust_Colum_Name(DF_Corrente_Ang_A_Temp)
        DF_Corrente_Ang_B_Temp.columns = Adjust_Colum_Name(DF_Corrente_Ang_B_Temp)
        DF_Corrente_Ang_C_Temp.columns = Adjust_Colum_Name(DF_Corrente_Ang_C_Temp)

        DF_Corrente_Ang_A_Temp.insert(loc=1, column='Fase', value='A') \
            if 'Fase' not in DF_Corrente_Ang_A_Temp else 0
        DF_Corrente_Ang_B_Temp.insert(loc=1, column='Fase', value='B') \
            if 'Fase' not in DF_Corrente_Ang_B_Temp else 0
        DF_Corrente_Ang_C_Temp.insert(loc=1, column='Fase', value='C') \
            if 'Fase' not in DF_Corrente_Ang_C_Temp else 0

        DF_Current_Elemt_Data_Ang = pd.concat([DF_Corrente_Ang_A_Temp, DF_Corrente_Ang_B_Temp, DF_Corrente_Ang_C_Temp])

        DF_Current_Elemt_Data_Ang.insert(loc=0, column='Case', value=len(Casos) if Casos != [] else 0)
        DF_Current_Elemt_Data_Ang.insert(loc=1, column='Simulation', value=Simulation)

    Save_Data(DF_Voltage_Data, DF_Tensao_Data_Ang,
              DF_Unbalance_Data, DF_Monitors_Data_2)

    logger.debug("Process_Data took {" + str(time.time() - t1) + " sec} to execulte")


def Save_Element_Data():
    """
    All element's data will be stored before the beginning of the simulation using this function
    """
    t1 = time.time()

    from Definitions import DF_Elements_Data

    DF_Elements_Data.to_sql('tblElements_Data', sqlalchemy(), if_exists='append', index=False)

    logger.debug("Save_Element_Data took {" + str(time.time() - t1) + " sec} to execulte")
