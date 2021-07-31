# coding: utf-8
from Definitions import *
import pandas as pd


def Tensao_Barras(Rede, itera):
    puVmag_Buses = []
    angle_Buses = []
    Bus_Names = DF_Tensao_A.Barras.values
    count = 0


    for Barra in Bus_Names:
        # Feature:
        # -> Criar e adicionar a atribuição do DF para o angulo da tensão tbm

        # puVmag = []
        angle = []
        Rede.dssCircuit.SetActiveBus(Barra)
        ativa_barra(Rede, Barra)  # Ativa a barra
        VmagAngle = puVmagAngle(Rede)

        if len(VmagAngle) == 6 or len(VmagAngle) == 8:
            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[2]  # puVmag.append(VmagAngle[0])
            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = VmagAngle[4]  # puVmag.append(VmagAngle[0])
        elif len(VmagAngle) == 4:
            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[2]  # puVmag.append(VmagAngle[0])
            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)
        elif len(VmagAngle) == 2:
            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = 0  # puVmag.append(0)
            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)

        if len(VmagAngle) == 6:
            angle.append(VmagAngle[1])
            angle.append(VmagAngle[3])
            angle.append(VmagAngle[5])
        elif len(VmagAngle) == 4:
            angle.append(VmagAngle[1])
            angle.append(VmagAngle[3])
            angle.append(0)
        elif len(VmagAngle) == 2:
            angle.append(VmagAngle[1])
            angle.append(0)
            angle.append(0)

        count += 1
        # puVmag_Buses.append(puVmag)
        angle_Buses.append(angle)
    # print(DF_Tensao_A.head())


def ativa_barra(Rede, nome_barra):
    Rede.dssCircuit.SetActiveBus(nome_barra)


def puVmagAngle(Rede):
    return Rede.dssBus.puVmagAngle


def originalSteps(Rede):
    Rede.dssLoadShapes.Name = Rede.dssLoadShapes.AllNames[1]
    # print len(Rede.dssLoadShapes.pmult)
    return len(Rede.dssLoadShapes.pmult)


def Colunas_DF_Horas(Rede):
    coll = []
    [coll.append(str(i)) for i in range(originalSteps(Rede))]


def Check():

    # Adicionar condições de vioçação aqui:

    if (float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]) <= 1.05 and
            float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]) >= 0.92):
        return True
    else:
        return False


def Salvar_Dados_Tensao():
    Escrever = pd.ExcelWriter("C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\Debug\Debug.xlsx")

    DF_Tensao_A.to_excel(Escrever, 'DF_Tensao_A', index=False)
    DF_Tensao_B.to_excel(Escrever, 'DF_Tensao_B', index=False)
    DF_Tensao_C.to_excel(Escrever, 'DF_Tensao_C', index=False)

    Escrever.save()


def Identify_Phases(Phases):
    Num_Phases = ""
    count = 0
    for Phase in Phases:
        if Phase == "A":
            Num_Phases = Num_Phases + ".1"
            count += 1
        elif Phase == "B":
            Num_Phases = Num_Phases + ".2"
            count += 1
        elif Phase == "C":
            Num_Phases = Num_Phases + ".3"
            count += 1
    return Num_Phases, count


def Limpar_DF(DF):
    DF.drop([i for i in range(len(DF))], inplace=True)


def Max_and_Min_Voltage_DF(A, B, C):
    return max(max(A.set_index('Barras').max().values),
               max(B.set_index('Barras').max().values),
               max(C.set_index('Barras').max().values)), \
           min(min(A.set_index('Barras')[A.set_index('Barras') > .2].min().values),
               min(B.set_index('Barras')[B.set_index('Barras') > .2].min().values),
               min(C.set_index('Barras')[C.set_index('Barras') > .1].min().values))
