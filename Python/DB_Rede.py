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