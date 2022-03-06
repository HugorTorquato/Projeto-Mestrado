# coding: utf-8

if __name__ == "__main__":

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    Rede = DSS(Rede_Path + "\Master.dss")
    engine = sqlalchemy()

    Version(Rede), Compila_DSS(Rede), Inicializa(Rede), Refresh_Or_Create_Tables(Rede, engine), \
    Refresh_Or_Create_Views(Rede, engine), Refresh_Or_Create_StoreProcedures(Rede, engine)

    if Salva_Dados:
        Salvar_Dados_Rede(Rede)

    # Depois desse ponto já pode criar o loop pq não vai deletar os dados das tabelas, só precisa salvar
    # os dados da rede uma vez ( seriam os dados padrôes

    if Calc_HC:
        Case_by_Case(Rede)  # Chamada da função

    # Definições de store procedures que ajustam dados nas tabelas depois de tudo rodar
    Run_Store_Procedures()
