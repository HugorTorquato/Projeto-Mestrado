# coding: utf-8

if __name__ == "__main__":

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    Rede = DSS(Rede_Path + "\Master.dss")

    Version(Rede), Compila_DSS(Rede), Inicializa(Rede), Refresh_Or_Create_Tables(Rede), Refresh_Or_Create_Views(Rede),
    Refresh_Or_Create_StoreProcedures(Rede)

    if Salva_Dados:
        Salvar_Dados_Rede(Rede)

    if Calc_HC:
        HC(Rede)  # Chamada da função

    # Definições de store procedures que ajustam dados nas tabelas depois de tudo rodar
    Run_Store_Procedures()
