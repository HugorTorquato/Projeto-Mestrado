import sqlalchemy as sql


def sqlalchemyVersion():

    engine = sql.create_engine('mssql+pymssql://sa:sa123@localhost:3306/DB_Rede3')
    print(engine)


## Criar engine com o SQL Server -> engine = create_engine('sqlite:///:memory:', echo=True)
## Criar chart com a dinamica do banco e as possiveis conexoes que podem ser feitas entra as tabelas
## Criar as tabelas


