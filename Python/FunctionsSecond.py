# coding: utf-8
from Definitions import *
import pandas as pd
import cmath

def Adiciona_Sensor(Rede):

    a = Rede.dssSensor.AllNames
    Elementos = Rede.dssLines.AllNames + Rede.dssTransformers.AllNames
    Barras_Elementos = []

    #for linha in Rede.dssLines.AllNames:
    #    Barras_Elementos.append(linha[0:3])
    ## WDG Currents

    # Precisa do kvbase? o opendss já deve pegar
    for elemento in Rede.dssLines.AllNames:
        Rede.dssText.Command = "New Sensor." + elemento + " Element=" + elemento + " enabled=yes" + \
                               " kvbase=2.4 clear=yes"

    for elemento in Rede.dssTransformers.AllNames:
        Rede.dssText.Command = "New Sensor." + elemento + " Element=" + elemento + " enabled=yes"

def Correntes_elementos(Rede):

    nome = []
    corrente = []
    teste = []

    for elemento in Rede.dssSensor.AllNames:

        Rede.dssCircuit.SetActiveElement(elemento)
        teste.append(Rede.dssCktElement.Powers)
        Rede.dssSensor.Name = elemento

        nome.append(Rede.dssSensor.Name)
        corrente.append(Rede.dssSensor.kWS)
        #corrente.append(Rede.dssTransformers.WdgCurrents)


    return

def get_resultados_potencia(self):

    #self.dssText.Command = "Show power kva elements"
    #self.dssText.Command = "Show Voltages LN Nodes"
    #self.dssText.Command = "Show Taps"
    self.dssText.Command = "Show Currents"

def Tensao_Barras(Rede, itera):
    puVmag_Buses = []
    angle_Buses = []
    Bus_Names = DF_Tensao_A.Barras.values

    count = 0

    tensao1 = 0
    tensao2 = 0
    tensao3 = 0
    angle1 = 0
    angle2 = 0
    angle3 = 0
    vmedio = 0

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
            tensao1 = VmagAngle[0] * sqrt3
            tensao2 = VmagAngle[2] * sqrt3
            tensao3 = VmagAngle[4] * sqrt3
            Vmedio = (tensao1 + tensao2 + tensao3) / 3
        elif len(VmagAngle) == 4:
            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = VmagAngle[2]  # puVmag.append(VmagAngle[0])
            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)
            tensao1 = VmagAngle[0] * sqrt3
            tensao2 = VmagAngle[2] * sqrt3
            tensao3 = 0
            vmedio = (tensao1 + tensao2)/2
        elif len(VmagAngle) == 2:
            DF_Tensao_A.loc[DF_Tensao_A.index == count, str(itera)] = VmagAngle[0]  # puVmag.append(VmagAngle[0])
            DF_Tensao_B.loc[DF_Tensao_B.index == count, str(itera)] = 0  # puVmag.append(0)
            DF_Tensao_C.loc[DF_Tensao_C.index == count, str(itera)] = 0  # puVmag.append(0)
            tensao1 = VmagAngle[0] * sqrt3
            tensao2 = 0
            tensao3 = 0
            Vmedio = tensao1

        if len(VmagAngle) == 6:
            angle.append(VmagAngle[1])
            angle.append(VmagAngle[3])
            angle.append(VmagAngle[5])
            angle1 = VmagAngle[1] + int(30)
            angle2 = VmagAngle[3] + int(30)
            angle3 = VmagAngle[5] + int(30)
        elif len(VmagAngle) == 4:
            angle.append(VmagAngle[1])
            angle.append(VmagAngle[3])
            angle.append(0)
            angle1 = VmagAngle[1] + int(30)
            angle2 = VmagAngle[3] + int(30)
            angle3 = 0
        elif len(VmagAngle) == 2:
            angle.append(VmagAngle[1])
            angle.append(0)
            angle.append(0)
            angle1 = VmagAngle[1] + int(30)
            angle2 = 0
            angle3 = 0

        max_IEEE, min_IEEE = Max_Min(tensao1/sqrt3, tensao2/sqrt3, tensao3/sqrt3)
        max_NEMA, min_NEMA = Max_Min(tensao1, tensao2, tensao3)

        # Se precisar usar as demais normas masta descomentar o código
        DF_Desq_IEC.loc[DF_Tensao_A.index == count, str(itera)] = \
            IEC(tensao1/sqrt3, tensao2/sqrt3, tensao3/sqrt3, angle1, angle2, angle3)
        DF_Desq_IEEE.loc[DF_Tensao_A.index == count, str(itera)] = \
            IEEE(tensao1, tensao2, tensao3, max_IEEE, min_IEEE)
        DF_Desq_NEMA.loc[DF_Tensao_A.index == count, str(itera)] =\
            NEMA(vmedio, max_NEMA)

        count += 1
        # puVmag_Buses.append(puVmag)
        angle_Buses.append(angle)
    # print(DF_Tensao_A.head())

def Max_Min(Tensao1, Tensao2, Tensao3):

    Vet_Max_Min = [Tensao1, Tensao2, Tensao3]

    if Tensao1 != 0 and Tensao2 != 0 and Tensao3 != 0:
        max_Tensao = max(Vet_Max_Min)
        min_Tensao = min(Vet_Max_Min)
        return max_Tensao, min_Tensao

    elif Tensao1 == 0 and Tensao2 != 0 and Tensao3 != 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao2 > Tensao3:
            min_Tensao = Tensao3
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao2
            return max_Tensao, min_Tensao

    elif Tensao1 != 0 and Tensao2 == 0 and Tensao3 != 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao1 > Tensao3:
            min_Tensao = Tensao3
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao1
            return max_Tensao, min_Tensao

    elif Tensao1 != 0 and Tensao2 != 0 and Tensao3 == 0:

        max_Tensao = max(Vet_Max_Min)
        if Tensao1 > Tensao2:
            min_Tensao = Tensao2
            return max_Tensao, min_Tensao
        else:
            min_Tensao = Tensao1
            return max_Tensao, min_Tensao

    else:
        max_Tensao = max(Vet_Max_Min)
        min_Tensao = max_Tensao
        return max_Tensao, min_Tensao

def IEC(Tensao1, Tensao2, Tensao3, Angle1, Angle2, Angle3):   # Limite de 2%

    if Tensao1 != 0 and Tensao2 != 0 and Tensao3 != 0:
        Positiva = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(Angle1))) +
                               (alfa * cmath.rect(Tensao2, np.deg2rad(Angle2))) +
                               (inv_alfa * cmath.rect(Tensao3, np.deg2rad(Angle3))))
        Negativa = 0.333333 * ((cmath.rect(Tensao1, np.deg2rad(Angle1))) +
                               (inv_alfa * cmath.rect(Tensao2, np.deg2rad(Angle2))) +
                               (alfa * cmath.rect(Tensao3, np.deg2rad(Angle3))))
        return (abs(Negativa)/abs(Positiva))*100
    else:
        return 0

def IEEE(Tensao1, Tensao2, Tensao3, max, min): # limite de 2.5%

    # Utiliza tensões de fase
    return (3*100*(max - min))/(Tensao1 + Tensao2 + Tensao3)

def NEMA(Vmedio, Vmax):

    return ((Vmax - Vmedio)/Vmedio)*100 if Vmedio != 0 else 0

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
    #print(DF_Desq_IEC)
    #print(Check_Desq(DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA))
    if float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[0]) <= limite_superior and \
       float(Max_and_Min_Voltage_DF(DF_Tensao_A, DF_Tensao_B, DF_Tensao_C)[1]) >= limite_inferior:# and \
       #float(Check_Desq(DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA)) <= limite_Deseq:
        #print(Check_Desq(DF_Desq_IEC, DF_Desq_IEEE, DF_Desq_NEMA))
        return True
    else:
        return False

def Check_Desq(IEC, IEEE, NEMA):

    DF = IEC if Norma == 0 else IEEE if Norma == 1 else NEMA

    return max(DF.set_index('Barras').max().values)



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
