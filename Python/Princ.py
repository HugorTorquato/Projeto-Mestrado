# coding: utf-8
import py_dss_interface

if __name__ == "__main__":

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    Rede = DSS(Rede_Path + "\Master.dss")
    Rede2 = py_dss_interface.DSSDLL() # Opendss object
    Rede2.text("compile " + Rede_Path + "\Master.dss")

    #Version(Rede2)
    #Compila_DSS_old(Rede)
    #Inicializa(Rede)

    engine = sqlalchemy()

    Version(Rede2), Compila_DSS(Rede2), Inicializa(Rede2)
    RunSQLDefinitions(engine, Rede2)

    if Salva_Dados:
        logger.info("Save Network Data Selected")
        Salvar_Dados_Rede(Rede) # Tenho de refazer essa parte depois

    # Depois desse ponto já pode criar o loop pq não vai deletar os dados das tabelas, só precisa salvar
    # os dados da rede uma vez ( seriam os dados padrôes

    if Calc_HC:
        logger.info("Starting Case_by_Case function")
        Case_by_Case(Rede2)  # Chamada da função

    # Definições de store procedures que ajustam dados nas tabelas depois de tudo rodar
    logger.info("Starting Store Procedures function")
    Run_Store_Procedures()
