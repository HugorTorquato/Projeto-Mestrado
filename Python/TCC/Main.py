# coding: utf-8
#

import pandas as pd
import matplotlib as pd


if __name__ == "__main__":
    print("TESTE")

    from Def import *
    from SystemFunctions import *

    Rede = DSS("C:\\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Python\TCC\Rede\Master.dss")

    Version(Rede)

    Compila_DSS(Rede)

    print(Nome_Barras(Rede))

    HC(Rede)
