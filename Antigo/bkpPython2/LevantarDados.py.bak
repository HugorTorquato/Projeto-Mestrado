# coding: utf-8
from Definitions import *
import pandas as pd
import matplotlib.pyplot as plt

Geo_Rede = pd.DataFrame()
Load_Rede = pd.DataFrame()
LoadShape_Rede = pd.DataFrame()
Transformers_Rede = pd.DataFrame()

def Salvar_Dados_Rede(Rede):

    Dados_Geometria_Linha(Rede)
    Dados_Load(Rede)
    Dados_LoadShapes(Rede)
    Dados_Transformers(Rede)

    #ToExcel()

def Dados_Geometria_Linha(Rede):

    Nome = []
    [Nome.append(str(i)) for i in Rede.dssLines.AllNames]

    Bus1 = []
    Bus2 = []
    X0 = []
    X1 =[]
    Xg =[]
    Xmatrix = []
    Yprim =[]
    R0 = []
    R1 = []
    Rg = []
    Rho =[]
    Rmatrix = []
    C0   = []
    C1   = []
    Cmatrix = []
    Count = []
    EmergAmps = []
    Geometry = []
    Length = []
    LineCode = []
    NormAmps = []
    NumCust = []
    Phases = []
    Spacing = []
    TotalCust = []

    for linha in Nome:
        Rede.dssLines.Name = linha
        Rmatrix.append(Rede.dssLines.Rmatrix)


        print Rede.dssLines.Properties
        a = Rede.dssLines.Rmatrix
        print linha
        print "hugo"
        print Rede.dssLines.Name
        print Rmatrix[-1]
        pause()

    for linha in Nome:
        Rede.dssLines.Name = linha
        Bus1.append(Rede.dssLines.Bus1)
        Bus2.append(Rede.dssLines.Bus2)
        Xg.append(Rede.dssLines.Xg)
        Xmatrix.append(Rede.dssLines.Xmatrix)
        Yprim.append(Rede.dssLines.Yprim)
        Rg.append(Rede.dssLines.Rg)
        Rho.append(Rede.dssLines.Rho)
        Rmatrix.append(Rede.dssLines.Rmatrix)
        Cmatrix.append(Rede.dssLines.Cmatrix)
        Count.append(Rede.dssLines.Count)
        EmergAmps.append(Rede.dssLines.EmergAmps)
        Geometry.append(Rede.dssLines.Geometry)
        Length.append(Rede.dssLines.Length)
        LineCode.append(Rede.dssLines.LineCode)
        NormAmps.append(Rede.dssLines.NormAmps)
        NumCust.append(Rede.dssLines.NumCust)
        Phases.append(Rede.dssLines.Phases)
        Spacing.append(Rede.dssLines.Spacing)
        TotalCust.append(Rede.dssLines.TotalCust)

        a = Rede.dssLines.Rmatrix
        print linha
        print a
        print Rede.dssLines.Name
        print Rmatrix[-1]
        pause()

    Geo_Rede.insert(0, 'Nomes', Nome)
    Geo_Rede.insert(1, 'Bus1', Bus1), Geo_Rede.insert(2, 'Bus2', Bus2), Geo_Rede.insert(3, 'X0', X0)
    Geo_Rede.insert(4, 'X1', X1), Geo_Rede.insert(5, 'Xg', Xg), Geo_Rede.insert(6, 'TotalCust', TotalCust)
    Geo_Rede.insert(7, 'Yprim', Yprim)
    Geo_Rede.insert(8, 'Rg', Rg), Geo_Rede.insert(11, 'Rho', Rho), Geo_Rede.insert(9, 'Rmatrix', Rmatrix)
    Geo_Rede.insert(10, 'Cmatrix', Cmatrix), Geo_Rede.insert(11, 'Count', Count),
    Geo_Rede.insert(12, 'EmergAmps', EmergAmps)
    Geo_Rede.insert(13, 'Geometry', Geometry), Geo_Rede.insert(14, 'Length', Length)
    Geo_Rede.insert(15, 'LineCode', LineCode), Geo_Rede.insert(16, 'NormAmps', NormAmps)
    Geo_Rede.insert(17, 'NumCust', NumCust), Geo_Rede.insert(18, 'Phases', Phases)
    Geo_Rede.insert(19, 'Spacing', Spacing), Geo_Rede.insert(20, 'Xmatrix', Xmatrix)

    print Geo_Rede.head()

def Dados_Load(Rede):

    Nome = []
    [Nome.append(str(i)) for i in Rede.dssLoads.AllNames]

    Daily = []
    kV = []
    kva = []
    kvar = []
    kW = []
    kwh = []
    Model = []
    PF = []
    Rneut = []
    Vmaxpu = []
    Vminemerg = []
    Vminnorm= []
    Vminpu = []
    Xneut = []
    Bus1 = []
    Phases = []

    for load in Nome:
        Rede.dssLoads.Name = load
        Daily.append(Rede.dssLoads.Daily)
        kV.append(Rede.dssLoads.kV)
        kva.append(Rede.dssLoads.kva)
        kvar.append(Rede.dssLoads.kvar)
        kW.append(Rede.dssLoads.kW)
        kwh.append(Rede.dssLoads.kwh)
        Model.append(Rede.dssLoads.Model)
        PF.append(Rede.dssLoads.PF)
        Rneut.append(Rede.dssLoads.Rneut)
        Vmaxpu.append(Rede.dssLoads.Vmaxpu)
        Vminemerg.append(Rede.dssLoads.Vminemerg)
        Vminnorm.append(Rede.dssLoads.Vminnorm)
        Vminpu.append(Rede.dssLoads.Vminpu)
        Xneut.append(Rede.dssLoads.Xneut)
        Bus1.append(Rede.dssCktElement.BusNames)
        Phases.append(Rede.dssCktElement.NumPhases)

    Load_Rede.insert(0, 'Nome', Nome), Load_Rede.insert(1, 'Daily', Daily), Load_Rede.insert(2, 'kV', kV)
    Load_Rede.insert(3, 'kva', kva), Load_Rede.insert(4, 'kvar', kvar), Load_Rede.insert(5, 'kW', kW)
    Load_Rede.insert(6, 'kwh', kwh), Load_Rede.insert(7, 'Model', Model), Load_Rede.insert(8, 'PF', PF)
    Load_Rede.insert(9, 'Rneut', Rneut), Load_Rede.insert(10, 'Vmaxpu', Vmaxpu), Load_Rede.insert(11, 'Vminemerg', Vminemerg)
    Load_Rede.insert(12, 'Vminnorm', Vminnorm), Load_Rede.insert(13, 'Vminpu', Vminpu), Load_Rede.insert(14, 'Xneut', Xneut)
    Load_Rede.insert(15, 'Bus', Bus1), Load_Rede.insert(16, 'Phases', Phases)

    print Load_Rede.head()

def Dados_LoadShapes(Rede):

    Nome = []
    [Nome.append(str(i)) for i in Rede.dssLoadShapes.AllNames]

    Npts = []
    Pbase = []
    Pmult = []
    Qbase = []
    Qmult = []
    Sinterval = []
    TimeArray = []
    UseActual = []

    for LoadShape in Nome:
        Rede.dssLoadShapes.Name = LoadShape

        Npts.append(Rede.dssLoadShapes.Npts)
        Pbase.append(Rede.dssLoadShapes.Pbase)
        Pmult.append(Rede.dssLoadShapes.Pmult)
        Qbase.append(Rede.dssLoadShapes.Qbase)
        Qmult.append(Rede.dssLoadShapes.Qmult)
        Sinterval.append(Rede.dssLoadShapes.Sinterval)
        TimeArray.append(Rede.dssLoadShapes.TimeArray)
        UseActual.append(Rede.dssLoadShapes.UseActual)

    LoadShape_Rede.insert(0, 'Nomes', Nome), LoadShape_Rede.insert(1, 'Npts', Npts)
    LoadShape_Rede.insert(2, 'Pbase', Pbase), LoadShape_Rede.insert(3, 'Pmult', Pmult)
    LoadShape_Rede.insert(4, 'Qbase', Qbase), LoadShape_Rede.insert(5, 'Qmult', Qmult)
    LoadShape_Rede.insert(6, 'Sinterval', Sinterval), LoadShape_Rede.insert(7, 'TimeArray', TimeArray)
    LoadShape_Rede.insert(8, 'UseActual', UseActual)

    print LoadShape_Rede.head()

def Dados_Transformers(Rede):

    Nome = []
    [Nome.append(str(i)) for i in Rede.dssTransformers.AllNames]

    CoreType = []
    IsDelta = []
    kV = []
    kva = []
    MaxTap = []
    Tap = []
    MinTap = []
    NumTaps = []
    NumWindings = []
    R = []
    RdcOhms = []
    Rneut = []
    Xhl = []
    Xht = []
    Xlt = []
    Xneut = []

    for Trans in Nome:
        Rede.dssTransformers.Name = Trans

        CoreType.append(Rede.dssTransformers.CoreType)
        IsDelta.append(Rede.dssTransformers.IsDelta)
        kV.append(Rede.dssTransformers.kV)
        kva.append(Rede.dssTransformers.kva)
        MaxTap.append(Rede.dssTransformers.MaxTap)
        Tap.append(Rede.dssTransformers.Tap)
        MinTap.append(Rede.dssTransformers.MinTap)
        NumTaps.append(Rede.dssTransformers.NumTaps)
        NumWindings.append(Rede.dssTransformers.NumWindings)
        R.append(Rede.dssTransformers.R)
        RdcOhms.append(Rede.dssTransformers.RdcOhms)
        Rneut.append(Rede.dssTransformers.Rneut)
        Xhl.append(Rede.dssTransformers.Xhl)
        Xht.append(Rede.dssTransformers.Xht)
        Xlt.append(Rede.dssTransformers.Xlt)
        Xneut.append(Rede.dssTransformers.Xneut)

    Transformers_Rede.insert(0, 'Nome', Nome), Transformers_Rede.insert(1, 'CoreType', CoreType)
    Transformers_Rede.insert(2, 'IsDelta', IsDelta), Transformers_Rede.insert(3, 'kV', kV)
    Transformers_Rede.insert(4, 'kva', kva), Transformers_Rede.insert(5, 'MaxTap', MaxTap)
    Transformers_Rede.insert(6, 'Tap', Tap), Transformers_Rede.insert(7, 'MinTap', MinTap)
    Transformers_Rede.insert(8, 'NumTaps', NumTaps), Transformers_Rede.insert(9, 'NumWindings', NumWindings)
    Transformers_Rede.insert(10, 'R', R), Transformers_Rede.insert(11, 'RdcOhms', RdcOhms)
    Transformers_Rede.insert(12, 'Rneut', Rneut), Transformers_Rede.insert(13, 'Xhl', Xhl)
    Transformers_Rede.insert(14, 'Xht', Xht), Transformers_Rede.insert(15, 'Xlt', Xlt)
    Transformers_Rede.insert(16, 'Xneut', Xneut)

    print Transformers_Rede.head()



def ToExcel():

    Escrever = pd.ExcelWriter("C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\ToExcel.xlsx")

    Geo_Rede.to_excel(Escrever, 'Dados Linha', index=False)
    Load_Rede.to_excel(Escrever, 'Dados Cargas', index=False)
    LoadShape_Rede.to_excel(Escrever, 'Dados LoadShapes', index=False)
    Transformers_Rede.to_excel(Escrever, 'Dados Transformadores', index=False)

    Escrever.save()