import sqlalchemy as sql
import pandas as pd
from Definitions import *


def sqlalchemy():

    engine = sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server').connect()

    return engine

def Refresh_Or_Create_Tables():

    metadata = sql.MetaData()
    engine = sqlalchemy()

    # Definição da tabela Barras
    DB = 'Barras'
    if len(pd.read_sql(
            'SELECT TABLE_NAME '
            'FROM INFORMATION_SCHEMA.TABLES '
            'WHERE TABLE_NAME = \'' + DB + '\'', engine)) == 0:
        print('Create')
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
                           sql.Column('Deseq', sql.Float)
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
        print('Create')
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
        print('Create')
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

## Criar chart com a dinamica do banco e as possiveis conexoes que podem ser feitas entra as tabelas
## Criar as tabelas


def Save_Data(Simulation):

    DF_General.to_sql('General', sqlalchemy(), if_exists='append', index=False)
    DF_Geradores.to_sql('GD', sqlalchemy(), if_exists='append', index=False)
    DF_Barras.to_sql('Barras', sqlalchemy(), if_exists='append', index=False)

def Save_General_Data(Simulation):

    from FunctionsSecond import Limpar_DF, Max_and_Min_Voltage_DF
    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Geradores, DF_General


    DF_General.loc[0, 'Voltage_Max'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]
    DF_General.loc[0, 'Voltage_Min'] = Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]
    DF_General.loc[0, 'GD_Config'] = str(DF_Geradores.set_index('Name').values)

def Save_Barras_Data(Rede, Simulation):

    from Definitions import DF_Tensao_A, DF_Tensao_B, DF_Tensao_C, DF_Barras
    from FunctionsSecond import originalSteps

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
        DF_Barras.loc[index, 'Deseq'] = 0

        index += 1


