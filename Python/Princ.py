# coding: utf-8

if __name__ == "__main__":

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    Rede = DSS(Rede_Path + "\Master.dss")
    engine = sqlalchemy()

    Version(Rede), Compila_DSS(Rede), Inicializa(Rede)
    RunSQLDefinitions(engine, Rede)

    if Salva_Dados:
        logger.info("Save Network Data Selected")
        Salvar_Dados_Rede(Rede)

    # Depois desse ponto já pode criar o loop pq não vai deletar os dados das tabelas, só precisa salvar
    # os dados da rede uma vez ( seriam os dados padrôes

    if Calc_HC:
        logger.info("Starting Case_by_Case function")
        Case_by_Case(Rede)  # Chamada da função

    # Definições de store procedures que ajustam dados nas tabelas depois de tudo rodar
    logger.info("Starting Store Procedures function")
    Run_Store_Procedures()
