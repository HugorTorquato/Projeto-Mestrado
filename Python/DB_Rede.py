import concurrent.futures

import pandas as pd
import sqlalchemy as sql
from Definitions import *

def sqlalchemy():

    engine = sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server').connect()

    logger.debug("Engine created")
    return engine

def Refresh_Or_Create_Tables(Rede):

    metadata = sql.MetaData()
    engine = sqlalchemy()

    # To do:
    #   1-

    # Definição da tabela Voltage_Data
    DB = 'Unbalance_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Barras', sql.String),
                           sql.Column('Descr', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Voltage_Elemt_Data
    DB = 'Voltage_Elemt_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Voltage_Elemt_Data_Ang
    DB = 'Voltage_Elemt_Data_Ang'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Power_Q_Elemt_Data
    DB = 'Power_Q_Elemt_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Power_P_Elemt_Data
    DB = 'Power_P_Elemt_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Check_Report
    DB = 'Check_Report'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('overvoltage', sql.Integer),
                           sql.Column('undervoltage', sql.Integer),
                           sql.Column('overcurrent', sql.Integer),
                           sql.Column('unbalance', sql.Integer)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Voltage_Data
    DB = 'Voltage_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Barras', sql.String),
                           sql.Column('Fase', sql.String),
                           sql.Column('TimeMaxPU', sql.String),
                           sql.Column('ValueMaxPU', sql.Float),
                           sql.Column('TimeMinPU', sql.String),
                           sql.Column('ValueMinPU', sql.Float)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Voltage_Data_Ang
    DB = 'Voltage_Data_Ang'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Barras', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Current_Data
    DB = 'Current_Elemt_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Current_Elemt_Data_Ang
    DB = 'Current_Elemt_Data_Ang'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elementos', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela PVSystems
    DB = 'MonitoresData'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elemento', sql.String),
                           sql.Column('Measurement', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela PVSystems
    DB = 'PVPowerData'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Name', sql.String),
                           sql.Column('Bus', sql.String),
                           sql.Column('Measurement', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela PVSystems
    DB = 'PVSystems'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Name', sql.String),
                           sql.Column('Bus', sql.String),
                           sql.Column('Pmp', sql.Float),
                           sql.Column('kW', sql.Float),
                           sql.Column('kvar', sql.Float),
                           sql.Column('FP', sql.Float),
                           sql.Column('Phases', sql.String),
                           sql.Column('Irrad', sql.String),
                           sql.Column('Temp', sql.String)
                           )
    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Elements
    DB = 'Grid_Elements'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Elemento', sql.String),
                           sql.Column('I_pu_max_a', sql.Float),
                           sql.Column('I_pu_max_b', sql.Float),
                           sql.Column('I_pu_max_c', sql.Float),
                           sql.Column('I_pu_min_a', sql.Float),
                           sql.Column('I_pu_min_b', sql.Float),
                           sql.Column('I_pu_min_c', sql.Float)
                           )
    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela Barras
    DB = 'Barras'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Name', sql.String),
                           sql.Column('V_pu_max_a', sql.Float),
                           sql.Column('V_pu_max_b', sql.Float),
                           sql.Column('V_pu_max_c', sql.Float),
                           sql.Column('V_pu_min_a', sql.Float),
                           sql.Column('V_pu_min_b', sql.Float),
                           sql.Column('V_pu_min_c', sql.Float),
                           sql.Column('Deseq_IEC',  sql.Float),
                           sql.Column('Deseq_IEEE', sql.Float),
                           sql.Column('Deseq_NEMA', sql.Float)
                           )
    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela GD
    DB = 'GD'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        GD = sql.Table(str(DB), metadata,
                       sql.Column('Nome_ID', sql.Integer, primary_key=True),
                       sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                       sql.Column('Name', sql.String),
                       sql.Column('Bus', sql.String),
                       sql.Column('kW', sql.Float),#sql.DECIMAL(12, 6)
                       sql.Column('kvar', sql.Float),
                       sql.Column('Phases', sql.String),
                       sql.Column('LoadShape', sql.String) #sql.ForeignKey('LoadShape.Name')
                        )
    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela General
    DB = 'General'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        logger.info('Create Table :' + str(DB))
        General = sql.Table(str(DB), metadata,
                            sql.Column('Simulation', sql.Integer, primary_key=True),
                            sql.Column('Voltage_Max', sql.Float),
                            sql.Column('Voltage_Min', sql.Float),
                            sql.Column('GD_Config', sql.String),
                            )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    metadata.create_all(engine)
    Adjust_tables_to_timestemp(engine, Rede)

def Refresh_Or_Create_Views(Rede):

    # 1- Colocar isso para criar somente quando precisar....
    # 2- Condição de log para quando já estiver criado

    metadata = sql.MetaData()
    engine = sqlalchemy()

    # Definição da view : vw_HC_VIOLATION_REPORT

    view = 'vw_HC_VIOLATION_REPORT'

    Definition = 'CREATE VIEW [dbo].[' + view + '] ' \
                 'AS ' \
                 '	SELECT ' \
                 '		overvoltage_count' \
                 '		,undervoltage_count' \
                 '		,overcurrent_count' \
                 '		,unbalance_count' \
                 '		,(SELECT overvoltage_count + undervoltage_count + overcurrent_count + unbalance_count) as total_count' \
                 '	FROM ' \
                 '(' \
                 '	SELECT TOP(1) ' \
                 '		(select ISNULL(sum(CR.overvoltage), 0) from Check_Report CR where CR.overvoltage = 1) as overvoltage_count' \
                 '		,(select ISNULL(sum(CR.undervoltage), 0) from Check_Report CR where CR.undervoltage = 1) as undervoltage_count' \
                 '		,(select ISNULL(sum(CR.overcurrent), 0) from Check_Report CR where CR.overcurrent = 1) as overcurrent_count' \
                 '		,(select ISNULL(sum(CR.unbalance), 0) from Check_Report CR where CR.unbalance = 1) as unbalance_count' \
                 '	) AS counts '

    DropView(engine, view)
    engine.execute(Definition)
    logger.info('Create View :' + str(view))

def Refresh_Or_Create_StoreProcedures(Rede):

    from FunctionsSecond import Return_Time_String_Colum

    engine = sqlalchemy()

    storeProcedure = 'Update_Voltage_Data_Table_Max_Min'
    Ary = Return_Time_String_Colum(Rede)

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
                     '                          FROM Voltage_Data VD2 WHERE VD.Nome_ID = VD2.Nome_ID),' \
                     '      VD.ValueMinPU = (SELECT (select ISNULL(MIN(Barra), 0) from (VALUES ' + str(Ary) + ')' \
                     '                               as Menor(Barra)' \
                     '                               where Barra > 0.5) as Menor' \
                     '                          FROM Voltage_Data VD3 WHERE VD.Nome_ID = VD3.Nome_ID) ' \
                     '  FROM Voltage_Data AS VD'

        t1 = time.perf_counter()
        engine.execute(Definition)
        logger.info('Create StoreProcedure :' + str(storeProcedure))
    else:
        logger.info('StoreProcedure already exists :' + str(storeProcedure))

def DropView(engine, view):

    engine.execute('DROP VIEW IF EXISTS ' + view)

def Adjust_tables_to_timestemp(engine, Rede):

    from FunctionsSecond import originalSteps

    # Case queira salvar dados em todos os intervalos de simulação, tem de adicionar o nome da tabela destino
    # o seguinte vetor. A ideia dessa função consiste em adicionar N colunas com que irá possíbilitar salvar
    # todos os valores presentes em um dia

    DB = ['PVPowerData', 'MonitoresData', 'Current_Elemt_Data', 'Current_Elemt_Data_Ang', 'Voltage_Data',
          'Voltage_Data_Ang', 'Voltage_Elemt_Data', 'Voltage_Elemt_Data_Ang', 'Power_P_Elemt_Data',
          'Power_Q_Elemt_Data', 'Unbalance_Data']

    for table in DB:
        if pd.read_sql('SELECT COUNT(COLUMN_NAME) AS resultado FROM INFORMATION_SCHEMA.COLUMNS '
                       'WHERE TABLE_NAME = \'' + str(table) + '\' AND  COLUMN_NAME = \'Time_1\'', engine).values == 0:

            for i in range(originalSteps(Rede)):
                engine.execute("ALTER TABLE " + table + " ADD Time_" + str(i) + " float(53)")

def Save_Data(Simulation, DF_Voltage_Data, DF_Tensao_Data_Ang, DF_Corrente_Data, DF_Current_Elemt_Data_Ang,
              DF_Unbalance_Data):

    from Definitions import DF_Geradores, DF_General, DF_Barras, DF_Elements, DF_PV, DF_PVPowerData,\
        DF_Monitors_Data, DF_Check_Report

    DF_General.to_sql('General', sqlalchemy(), if_exists='append', index=False)
    DF_Geradores.to_sql('GD', sqlalchemy(), if_exists='append', index=False)
    DF_PV.to_sql('PVSystems', sqlalchemy(), if_exists='append', index=False)
    DF_PVPowerData.to_sql('PVPowerData', sqlalchemy(), if_exists='append', index=False)
    DF_Monitors_Data.to_sql('MonitoresData', sqlalchemy(), if_exists='append', index=False)
    DF_Barras.to_sql('Barras', sqlalchemy(), if_exists='append', index=False)
    DF_Elements.to_sql('Grid_Elements', sqlalchemy(), if_exists='append', index=False)
    DF_Check_Report.to_sql('Check_Report', sqlalchemy(), if_exists='append', index=False)

    # Corrigir essa ref -> Por algum motivo não está sendo armazenada a global
    DF_Voltage_Data.to_sql('Voltage_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Tensao_Data_Ang.to_sql('Voltage_Data_Ang', sqlalchemy(), if_exists='append', index=False)
    DF_Corrente_Data.to_sql('Current_Elemt_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Current_Elemt_Data_Ang.to_sql('Current_Elemt_Data_Ang', sqlalchemy(), if_exists='append', index=False)
    DF_Unbalance_Data.to_sql('Unbalance_Data', sqlalchemy(), if_exists='append', index=False)

def Save_Data_Secondary(DF_Power_P_Elemt_Data, DF_Power_Q_Elemt_Data, DF_Voltage_Elemt_Data,
                        DF_Voltage_Elemt_Data_Ang):

    DF_Power_P_Elemt_Data.to_sql('Power_P_Elemt_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Power_Q_Elemt_Data.to_sql('Power_Q_Elemt_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Voltage_Elemt_Data.to_sql('Voltage_Elemt_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Voltage_Elemt_Data_Ang.to_sql('Voltage_Elemt_Data_Ang', sqlalchemy(), if_exists='append', index=False)

def Save_General_Data(Simulation):

    from FunctionsSecond import Max_and_Min_Voltage_DF
    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Geradores, DF_General

    DF_General.loc[0, 'Voltage_Max'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]
    DF_General.loc[0, 'Voltage_Min'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]
    DF_General.loc[0, 'GD_Config'] = str(DF_Geradores.set_index('Name').values)

def Run_Store_Procedures():

    # Run all store procedures frim the list by the end of the Simulation

    SPs = ['Update_Voltage_Data_Table_Max_Min']

    [sqlalchemy().execute(SP) for SP in SPs]

def Process_Data(Rede, Simulation):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Barras, DF_Desq_IEC, DF_Desq_IEEE,\
        DF_Desq_NEMA, DF_Corrente_A, DF_Corrente_B, DF_Corrente_C, DF_Elements, DF_Voltage_Data, DF_Current_Data,\
        DF_Tensao_Ang_A, DF_Tensao_Ang_B, DF_Tensao_Ang_C, DF_Corrente_Ang_A, DF_Corrente_Ang_B, DF_Corrente_Ang_C,\
        Savar_Dados_Elem
    from FunctionsSecond import Adjust_Colum_Name

    # Process Bus
    index = len(DF_Barras.index)

    for Barra in DF_Tensao_A.Barras.values:
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

    DF_Voltage_Data.insert(loc=0, column='Simulation', value=Simulation)
    # Exemplo de como adicionar elementos nulos em uma coluna nula
    DF_Voltage_Data.insert(loc=3, column='TimeMaxPU', value='')
    DF_Voltage_Data.insert(loc=4, column='ValueMaxPU', value=0)
    DF_Voltage_Data.insert(loc=5, column='TimeMinPU', value='')
    DF_Voltage_Data.insert(loc=6, column='ValueMinPU', value=0)

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

    DF_Tensao_Data_Ang.insert(loc=0, column='Simulation', value=Simulation)

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
    DF_Unbalance_Data.insert(loc=0, column='Simulation', value=Simulation)

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

    DF_Corrente_Data.insert(loc=0, column='Simulation', value=Simulation)

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

    DF_Current_Elemt_Data_Ang.insert(loc=0, column='Simulation', value=Simulation)

    Save_Data(Simulation, DF_Voltage_Data, DF_Tensao_Data_Ang, DF_Corrente_Data, DF_Current_Elemt_Data_Ang,
              DF_Unbalance_Data)

    if Savar_Dados_Elem == 1:
        Process_Data_Secondary(Rede, Simulation)

def Process_Data_Secondary(Rede, Simulation):


    from FunctionsSecond import Adjust_Colum_Name

    # Process Element Voltage in each simulation
    global DF_Voltage_Elemt_Data
    DF_Voltage_A_Temp = DF_Voltage_A.copy(deep=True)
    DF_Voltage_B_Temp = DF_Voltage_B.copy(deep=True)
    DF_Voltage_C_Temp = DF_Voltage_C.copy(deep=True)

    DF_Voltage_A_Temp.columns = Adjust_Colum_Name(DF_Voltage_A_Temp)
    DF_Voltage_B_Temp.columns = Adjust_Colum_Name(DF_Voltage_B_Temp)
    DF_Voltage_C_Temp.columns = Adjust_Colum_Name(DF_Voltage_C_Temp)

    DF_Voltage_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Voltage_A_Temp else 0
    DF_Voltage_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Voltage_B_Temp else 0
    DF_Voltage_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Voltage_C_Temp else 0

    DF_Voltage_Elemt_Data = pd.concat([DF_Voltage_A_Temp, DF_Voltage_B_Temp, DF_Voltage_C_Temp])

    DF_Voltage_Elemt_Data.insert(loc=0, column='Simulation', value=Simulation)

    # Process Element Voltage Angle in each simulation
    global DF_Voltage_Elemt_Data_Ang
    DF_Voltage_Ang_A_Temp = DF_Voltage_Ang_A.copy(deep=True)
    DF_Voltage_Ang_B_Temp = DF_Voltage_Ang_B.copy(deep=True)
    DF_Voltage_Ang_C_Temp = DF_Voltage_Ang_C.copy(deep=True)

    DF_Voltage_Ang_A_Temp.columns = Adjust_Colum_Name(DF_Voltage_Ang_A_Temp)
    DF_Voltage_Ang_B_Temp.columns = Adjust_Colum_Name(DF_Voltage_Ang_B_Temp)
    DF_Voltage_Ang_C_Temp.columns = Adjust_Colum_Name(DF_Voltage_Ang_C_Temp)

    DF_Voltage_Ang_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Voltage_Ang_A_Temp else 0
    DF_Voltage_Ang_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Voltage_Ang_B_Temp else 0
    DF_Voltage_Ang_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Voltage_Ang_C_Temp else 0

    DF_Voltage_Elemt_Data_Ang = pd.concat([DF_Voltage_Ang_A_Temp, DF_Voltage_Ang_B_Temp, DF_Voltage_Ang_C_Temp])

    DF_Voltage_Elemt_Data_Ang.insert(loc=0, column='Simulation', value=Simulation)

    # Process Element Active Power in each simulation
    global DF_Power_P_Elemt_Data
    DF_Pot_P_A_Temp = DF_Pot_P_A.copy(deep=True)
    DF_Pot_P_B_Temp = DF_Pot_P_B.copy(deep=True)
    DF_Pot_P_C_Temp = DF_Pot_P_C.copy(deep=True)

    DF_Pot_P_A_Temp.columns = Adjust_Colum_Name(DF_Pot_P_A_Temp)
    DF_Pot_P_B_Temp.columns = Adjust_Colum_Name(DF_Pot_P_B_Temp)
    DF_Pot_P_C_Temp.columns = Adjust_Colum_Name(DF_Pot_P_C_Temp)

    DF_Pot_P_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Pot_P_A_Temp else 0
    DF_Pot_P_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Pot_P_B_Temp else 0
    DF_Pot_P_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Pot_P_C_Temp else 0

    DF_Power_P_Elemt_Data = pd.concat([DF_Pot_P_A_Temp, DF_Pot_P_B_Temp, DF_Pot_P_C_Temp])

    DF_Power_P_Elemt_Data.insert(loc=0, column='Simulation', value=Simulation)

    # Process Element Reactive Power in each simulation
    global DF_Power_Q_Elemt_Data
    DF_Pot_Q_A_Temp = DF_Pot_Q_A.copy(deep=True)
    DF_Pot_Q_B_Temp = DF_Pot_Q_B.copy(deep=True)
    DF_Pot_Q_C_Temp = DF_Pot_Q_C.copy(deep=True)

    DF_Pot_Q_A_Temp.columns = Adjust_Colum_Name(DF_Pot_Q_A_Temp)
    DF_Pot_Q_B_Temp.columns = Adjust_Colum_Name(DF_Pot_Q_B_Temp)
    DF_Pot_Q_C_Temp.columns = Adjust_Colum_Name(DF_Pot_Q_C_Temp)

    DF_Pot_Q_A_Temp.insert(loc=1, column='Fase', value='A') \
        if 'Fase' not in DF_Pot_Q_A_Temp else 0
    DF_Pot_Q_B_Temp.insert(loc=1, column='Fase', value='B') \
        if 'Fase' not in DF_Pot_Q_B_Temp else 0
    DF_Pot_Q_C_Temp.insert(loc=1, column='Fase', value='C') \
        if 'Fase' not in DF_Pot_Q_C_Temp else 0

    DF_Power_Q_Elemt_Data = pd.concat([DF_Pot_Q_A_Temp, DF_Pot_Q_B_Temp, DF_Pot_Q_C_Temp])

    DF_Power_Q_Elemt_Data.insert(loc=0, column='Simulation', value=Simulation)

    #return DF_Voltage_Elemt_Data, DF_Voltage_Elemt_Data_Ang, DF_Power_P_Elemt_Data, DF_Power_Q_Elemt_Data
    Save_Data_Secondary(DF_Power_P_Elemt_Data, DF_Power_Q_Elemt_Data, DF_Voltage_Elemt_Data,
                        DF_Voltage_Elemt_Data_Ang)
