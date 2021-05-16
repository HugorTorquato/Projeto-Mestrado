import sqlalchemy as sql
import pandas as pd


def sqlalchemyVersion():

    engine = sql.create_engine('mssql+pymssql://sa:sa123@localhost:3306/DB_Rede_3', echo=True)
    print(engine)
    df = pd.read_sql('SELECT TOP (1000) [Nome] ,[idade] FROM [DB_Rede3].[dbo].[Table_1]', engine)
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


