
# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print (u"Autor: Hugo Torquato \nData: 24/01/2020 \nE-mail: hugortorquato@gmail.com \n")

hugo = pd.DataFrame()

hugo.insert(0, 'teste', [9,8,7,6,5,4,3,2,1])

print (hugo.head())