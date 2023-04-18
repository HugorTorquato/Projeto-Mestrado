import pandas
import pandas as pd

import pythonsql
import matplotlib.pyplot as plt

command1 = """
SELECT 
	 (SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 <  50) AS ADJ_Capacity_50
	,(SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 < 100 AND ADJ_Battery_Capacity_5_4 >  50) AS ADJ_Capacity_100
	,(SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 < 150 AND ADJ_Battery_Capacity_5_4 > 100) AS ADJ_Capacity_150
	,(SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 < 200 AND ADJ_Battery_Capacity_5_4 > 150) AS ADJ_Capacity_200
	,(SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 < 250 AND ADJ_Battery_Capacity_5_4 > 200) AS ADJ_Capacity_250
	,(SELECT COUNT(ADJ_Battery_Capacity_5_4) FROM spBatterySummary WHERE ADJ_Battery_Capacity_5_4 > 250) AS ADJ_Capacity_B_250
    """

command2 = """
SELECT 
	 (SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 <  50) AS ADJ_Capacity_50
	,(SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 < 100 AND ADJ_Battery_Capacity_7_6 >  50) AS ADJ_Capacity_100
	,(SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 < 150 AND ADJ_Battery_Capacity_7_6 > 100) AS ADJ_Capacity_150
	,(SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 < 200 AND ADJ_Battery_Capacity_7_6 > 150) AS ADJ_Capacity_200
	,(SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 < 250 AND ADJ_Battery_Capacity_7_6 > 200) AS ADJ_Capacity_250
	,(SELECT COUNT(ADJ_Battery_Capacity_7_6) FROM spBatterySummary WHERE ADJ_Battery_Capacity_7_6 > 250) AS ADJ_Capacity_B_250
    """

# Create the plot class and init all properties realted to it
x15 = pythonsql.SQLActions("DB_Rede_3_50_2303")
x30 = pythonsql.SQLActions("DB_Rede_3_50_2303")
x50 = pythonsql.SQLActions("DB_Rede_3_50_2303")

command1Value = x15.returnTableFromSQLasDataframe(command1).melt()["value"]
command2Value = x15.returnTableFromSQLasDataframe(command2).melt()["value"]

labels = ['<50', '<100', '<150', '<200', '<250', '>250']

dfTable15 = pd.concat([command1Value, command2Value, 100 * (command2Value - command1Value) / command1Value], axis=1)
dfTable15.columns = ["Values_5_4", "Values_7_6", "Diff(%)"]
dfTable15.index = labels






fig = plt.figure(1)

ax1 = fig.add_subplot(1, 2, 1)
ax1.pie(dfTable15["Values_5_4"], autopct='%1.1f%%')
ax1.set_title("VW Control enabled")

ax2 = fig.add_subplot(1, 2, 2)
ax2.pie(dfTable15["Values_7_6"], autopct='%1.1f%%')
ax2.set_title("VW and VV Control enabled")

fig.legend(labels, loc='upper left')
fig.suptitle("BATTERY DIVIDED BY SIZE")

'''
This table and pie chart represents the diference between only VW and VW + VV controls.
The amount of storages < 50Wh increased 27% and te rst reduced... here is a result from 1 database
Values_5_4  Values_7_6     Diff(%
<50          184         235  27.717391
<100          44          38 -13.636364
<150          45          13 -71.111111
<200          15           9 -40.000000
<250          10           3 -70.000000
>250           2           2   0.000000
'''

print(dfTable15)




