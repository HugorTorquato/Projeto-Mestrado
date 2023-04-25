"""
THis plot aims to create an average comparison between all simulations ( control cases ) based in average HC%
values. And aso present the average power loss with VW control and the proposed battery sizing (Wh and W)
to that specific control simulation
"""

import numpy as np
import pythonsql
import matplotlib.pyplot as plt

DB15 = "DB_Rede_3_50_1403"
DB30 = "DB_Rede_3_50_3103_30"
DB50 = "DB_Rede_3_50_1904_50"


def GetHCTable(db):
    x = pythonsql.SQLActions(db)
    command = f"""
                SELECT * FROM {db}.dbo.spStatisticalResults
                """
    df = x.returnTableFromSQLasDataframe(command)
    return df.drop("id", axis=1).where((df['Simulation'] != 5) & (df['Simulation'] != 7)).dropna()


def GetBatTable(db):
    x = pythonsql.SQLActions(db)
    command = f"""
                SELECT * FROM {db}.dbo.vwExtractBatteryAVGData
                """
    df = x.returnTableFromSQLasDataframe(command)
    return df


dfTable15 = GetHCTable(DB15)
dfTable30 = GetHCTable(DB30)
dfTable50 = GetHCTable(DB50)
dfBatTable15 = GetBatTable(DB15)
dfBatTable30 = GetBatTable(DB30)
dfBatTable50 = GetBatTable(DB50)

n = dfTable15.index.size
r = np.arange(n)
width = 0.25

fig2, ax = plt.subplots()

ax.bar(r - width, dfTable15['Average'] * 100, width=width, yerr=dfTable15['StandardDeviation'] * 100)
ax.bar(r,         dfTable30['Average'] * 100, width=width, yerr=dfTable15['StandardDeviation'] * 100)
ax.bar(r + width, dfTable50['Average'] * 100, width=width, yerr=dfTable15['StandardDeviation'] * 100)

plt.xticks(r, ['PV', 'PV+VV', '<PV+VW', 'PV+VV+VW'])

plt.ylabel("HC%")
plt.yticks(np.arange(0, 110, 10))
plt.legend([f"VW-15% : PV+VW    -> Energy Loss :{dfBatTable15['Avg_Energy_Loss_5_4'].values}, Baterry(Wh) :{dfBatTable15['Avg_Cap_Loss_5_4'].values}, Baterry(W) :{dfBatTable15['Avg_Pot_Loss_5_4'].values}\n" +
            f"         PV+VV+VW -> Energy Loss :{dfBatTable15['Avg_Energy_Loss_7_6'].values}, Baterry(Wh) :{dfBatTable15['Avg_Cap_Loss_7_6'].values}, Baterry(W) :{dfBatTable15['Avg_Pot_Loss_7_6'].values}",
            f"VW-30% : PV+VW    -> Energy Loss :{dfBatTable30['Avg_Energy_Loss_5_4'].values}, Baterry(Wh) :{dfBatTable30['Avg_Cap_Loss_5_4'].values}, Baterry(W) :{dfBatTable30['Avg_Pot_Loss_5_4'].values}\n" +
            f"         PV+VV+VW -> Energy Loss :{dfBatTable30['Avg_Energy_Loss_7_6'].values}, Baterry(Wh) :{dfBatTable30['Avg_Cap_Loss_7_6'].values}, Baterry(W) :{dfBatTable30['Avg_Pot_Loss_7_6'].values}",
            f"VW-50% : PV+VW    -> Energy Loss :{dfBatTable50['Avg_Energy_Loss_5_4'].values}, Baterry(Wh) :{dfBatTable50['Avg_Cap_Loss_5_4'].values}, Baterry(W) :{dfBatTable50['Avg_Pot_Loss_5_4'].values}\n" +
            f"         PV+VV+VW -> Energy Loss :{dfBatTable50['Avg_Energy_Loss_7_6'].values}, Baterry(Wh) :{dfBatTable50['Avg_Cap_Loss_7_6'].values}, Baterry(W) :{dfBatTable50['Avg_Pot_Loss_7_6'].values}"],
           loc='upper left')
plt.grid()

print(dfTable15)
print(dfTable30)
print(dfTable50)
