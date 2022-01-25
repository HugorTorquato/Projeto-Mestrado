# coding: utf-8

if __name__ == "__main__":

    from Definitions import *
    from SistemFunctions import *
    from LevantarDados import *
    from Geradores import *
    from DB_Rede import *

    Rede = DSS(Rede_Path + "\Master.dss")

    Version(Rede), Compila_DSS(Rede), Inicializa(Rede), Refresh_Or_Create_Tables(Rede), Refresh_Or_Create_Views(Rede)

    if Salva_Dados:
        Salvar_Dados_Rede(Rede)

    # Depois desse ponto já pode criar o loop pq não vai deletar os dados das tabelas, só precisa salvar
    # os dados da rede uma vez ( seriam os dados padrôes

    if Calc_HC:
        Case_by_Case(Rede)  # Chamada da função

    #else:
        #Solve_Hora_por_Hora(Rede)

    # print DF_Tensao_A.head()
    # from FunctionsSecond import Colunas_DF_Horas

    # print DF_Tensao_A.set_index('Barras').head()

    # plt.figure(1)
    # [DF_Tensao_A.set_index('Barras')[coll].plot(figsize=(16, 8), kind='bar', color='black') for coll in ['48']]
    # plt.xticks(rotation=45), plt.ylim([0.9, 1.05]), plt.grid()

    # plt.figure(2)
    # print 'hugo'
    # print DF_Tensao_A.set_index('Barras').iloc[3:5]
    # DF_Tensao_A.set_index('Barras').iloc[4].plot(figsize=(16, 8), linewidth=4)
    # plt.ylim([0.9, 1.05]), plt.grid()

    # plt.show()
