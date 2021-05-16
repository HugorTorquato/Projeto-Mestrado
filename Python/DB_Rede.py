import sqlalchemy as sql
import pandas as pd


def sqlalchemyVersion():

    #engine = sql.create_engine('mssql+pymssql://sa:sa123@localhost:1433/DB_Rede_3', echo=True)
    engine = sql.create_engine(
        'mssql+pyodbc://LAPTOP-5R3FI4O0\SQLEXPRESS/DB_Rede_3?driver=ODBC Driver 17 for SQL Server').connect()
    print(engine)

    #DF_TESTE = pd.DataFrame({
    #    "A": [1, 2, 3, 4],
    #    "B": [4, 3, 2, 1],
    #    "C": [2, 1, 4, 3]})
    #DF_TESTE.to_sql(
    #    name='TESTE',
    #    con= engine
    #)
    df = pd.read_sql('SELECT * FROM TESTE', engine)
    print(df)
    #Create_Tables(engine)


def Create_Tables(engine):

    metadata = sql.MetaData()
    users = sql.Table('addresses', metadata,
                   sql.Column('id', sql.Integer, primary_key=True),
                   sql.Column('user_id', None, sql.ForeignKey('users.id')),
                   sql.Column('email_address', sql.String, nullable=False))
    metadata.create_all(engine)

    print('hugo')


## Criar chart com a dinamica do banco e as possiveis conexoes que podem ser feitas entra as tabelas
## Criar as tabelas


