import pandas as pd
import sqlalchemy as sql
from Definitions import *

def sqlalchemy():

    engine = sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server').connect()

    return engine

def Refresh_Or_Create_Tables(Rede):

    metadata = sql.MetaData()
    engine = sqlalchemy()

    # To do:
    #   1- Colocar tabela com todos os valores de tensão ()

    # Definição da tabela PVSystems
    DB = 'Voltage_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        print('Create Table :' + str(DB))
        Barras = sql.Table(str(DB), metadata,
                           sql.Column('Nome_ID', sql.Integer, primary_key=True),
                           sql.Column('Simulation', None, sql.ForeignKey('General.Simulation')),
                           sql.Column('Barras', sql.String),
                           sql.Column('Fase', sql.String)
                           )

    else:
        engine.execute('DBCC CHECKIDENT(\'' + DB + '\', RESEED, 0)') # Redefine a PK para começar do zero novamente
        engine.execute('DELETE FROM ' + str(DB))

    # Definição da tabela PVSystems
    DB = 'Current_Data'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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
        print('Create Table :' + str(DB))
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

def Adjust_tables_to_timestemp(engine, Rede):

    from FunctionsSecond import originalSteps

    # Case queira salvar dados em todos os intervalos de simulação, tem de adicionar o nome da tabela destino
    # o seguinte vetor. A ideia dessa função consiste em adicionar N colunas com que irá possíbilitar salvar
    # todos os valores presentes em um dia

    DB = ['PVPowerData', 'MonitoresData', 'Current_Data', 'Voltage_Data']

    for table in DB:
        if pd.read_sql('SELECT COUNT(COLUMN_NAME) AS resultado FROM INFORMATION_SCHEMA.COLUMNS '
                       'WHERE TABLE_NAME = \'' + str(table) + '\' AND  COLUMN_NAME = \'Time_1\'', engine).values == 0:

            for i in range(originalSteps(Rede)):
                engine.execute("ALTER TABLE " + table + " ADD Time_" + str(i) + " float(53)")

def Save_Data(Simulation, DF_Voltage_Data, DF_Corrente_Data):

    from Definitions import DF_Geradores, DF_General, DF_Barras, DF_Elements, DF_PV, DF_PVPowerData, DF_Monitors_Data

    DF_General.to_sql('General', sqlalchemy(), if_exists='append', index=False)
    DF_Geradores.to_sql('GD', sqlalchemy(), if_exists='append', index=False)
    DF_PV.to_sql('PVSystems', sqlalchemy(), if_exists='append', index=False)
    DF_PVPowerData.to_sql('PVPowerData', sqlalchemy(), if_exists='append', index=False)
    DF_Monitors_Data.to_sql('MonitoresData', sqlalchemy(), if_exists='append', index=False)
    DF_Barras.to_sql('Barras', sqlalchemy(), if_exists='append', index=False)
    DF_Elements.to_sql('Grid_Elements', sqlalchemy(), if_exists='append', index=False)

    # Corrigir essa ref -> Por algum motivo não está sendo armazenada a global
    DF_Voltage_Data.to_sql('Voltage_Data', sqlalchemy(), if_exists='append', index=False)
    DF_Corrente_Data.to_sql('Current_Data', sqlalchemy(), if_exists='append', index=False)

def Save_General_Data(Simulation):

    from FunctionsSecond import Max_and_Min_Voltage_DF
    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Geradores, DF_General

    DF_General.loc[0, 'Voltage_Max'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]
    DF_General.loc[0, 'Voltage_Min'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]
    DF_General.loc[0, 'GD_Config'] = str(DF_Geradores.set_index('Name').values)

def Process_Data(Rede, Simulation):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Barras, DF_Desq_IEC, DF_Desq_IEEE,\
        DF_Desq_NEMA, DF_Corrente_A, DF_Corrente_B, DF_Corrente_C, DF_Elements, DF_Voltage_Data, DF_Current_Data
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

    return DF_Voltage_Data, DF_Corrente_Data
