# coding:utf-8



def Version(Rede):
    print(Rede.dssObj.Version)

def Compila_DSS(Rede):

    Rede.dssObj.ClearAll()
    Rede.dssText.Command = "compile " + Rede.Modelo_Barras
    Rede.dssSolution.Solve()

def Nome_Barras(Rede):
    return Rede.dssCircuit.AllBusNames

def HC(Rede):

    # Definição inicial

    # loop local e configuração de gds

        # loop HC

            # loop daily




    Pot_GD = 0

    for i in range(2): #HC

        Rede.dssSolution.Number = 1

        from SecondFunctions import originalSteps

        for itera in range(originalSteps(Rede)):

            Rede.dssSolution.SolveSnap()

            # Coleta de dados

            Rede.dssSolution.FinishTimeStep()
