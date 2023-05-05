"""
This Plot aims to demonstrate the reduction of active power loss between the VW and VV+VW control.
Each line represents a VW reduction (15, 30 or 50%)
Inside each subplot exists a zoom plot to represent the biggest difference between both simulations, and also
display the percentage reduction between them.

The plot happens automatically, it identifies the biggest difference in power 3F in each simulation
(15, 30 or 50%) in VW control and plot the same point but with VV + VW control to compare the differences.

But we can see the reduction in the graphic as well, the area bellow the curve


is it better to also plot the biggest diference for this equipment in the same Case? or plot the same
point in time? or another plot?
"""

import numpy as np
import pythonsql
import matplotlib.pyplot as plt


# Find a way to get the max power diference from each VW rate

DB15 = "DB_Rede_3_50_1403"
DB30 = "DB_Rede_3_50_3103_30"
DB50 = "DB_Rede_3_50_1904_50"

def GetPowerDataTable(db):
    command = f"""
                SELECT 
                    *
                FROM {db}.dbo.vwCreateSUMProcessedPVPowerDataDiffTable
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)


def GetFuncPowerDataFilteredTable(db, DF):
    command = f"""
                SELECT 
                    *
                FROM {db}.dbo.fnGetPotDataBasedOnElement ( \'{DF['Elemento']}\',  \'{DF['Case']}\')
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)


dfDB15 = GetPowerDataTable(DB15)
dfDB30 = GetPowerDataTable(DB30)
dfDB50 = GetPowerDataTable(DB50)

D15 = 15
D30 = 30
D50 = 50

dfFiltered15 = dfDB15.loc[( (dfDB15['Sum_Pot_5'] - dfDB15['Sum_Pot_4'])/dfDB15['Sum_Pot_5'] > (D15-0.5)/100 )
                      & ( (dfDB15['Sum_Pot_5'] - dfDB15['Sum_Pot_4'])/dfDB15['Sum_Pot_5'] <= D15/100 )].iloc[0]
dfFiltered30 = dfDB30.loc[( (dfDB30['Sum_Pot_5'] - dfDB30['Sum_Pot_4'])/dfDB30['Sum_Pot_5'] > (D30-1)/100 )
                      & ( (dfDB30['Sum_Pot_5'] - dfDB30['Sum_Pot_4'])/dfDB30['Sum_Pot_5'] <= D30/100 )].iloc[0]
dfFiltered50 = dfDB50.loc[( (dfDB50['Sum_Pot_5'] - dfDB50['Sum_Pot_4'])/dfDB50['Sum_Pot_5'] > (D50-1.5)/100 )
                      & ( (dfDB50['Sum_Pot_5'] - dfDB50['Sum_Pot_4'])/dfDB50['Sum_Pot_5'] <= D50/100 )].iloc[0]

df2_DB15 = GetFuncPowerDataFilteredTable(DB15, dfFiltered15)
df2_DB30 = GetFuncPowerDataFilteredTable(DB30, dfFiltered30)
df2_DB50 = GetFuncPowerDataFilteredTable(DB50, dfFiltered50)

x_ax = df2_DB15["TimeStep"]


fig3 = plt.figure(3)

#######################################################################################################################
ax1 = fig3.add_subplot(3, 2, 1)
x1, y1 = dfFiltered15['TimeStep'], dfFiltered15['Sum_Pot_5']
x2, y2 = dfFiltered15['TimeStep'], dfFiltered15['Sum_Pot_4']
ax1.plot(x_ax, df2_DB15["Sum_Pot_5"], label='Pot Without VW')
ax1.plot(x_ax, df2_DB15["Sum_Pot_4"], label='Pot With VW')
ax1.set_xlim(18, 96)
ax1.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax1.add_patch(square)
# Zoom in on the square
axins1 = ax1.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins1.plot(x_ax, df2_DB15["Sum_Pot_5"])
axins1.plot(x_ax, df2_DB15["Sum_Pot_4"])
axins1.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins1.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins1.annotate('', xy=(x1, y1), xytext=(x2, y2),
               arrowprops=dict(arrowstyle='<->', linewidth=3))

axins1.annotate(
    f"{round((100*(df2_DB15['Sum_Pot_5'].iloc[x1]-df2_DB15['Sum_Pot_4'].iloc[x1]))/df2_DB15['Sum_Pot_5'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins1.grid()

#######################################################################################################################
ax2 = fig3.add_subplot(3, 2, 2)
x1, y1 = dfFiltered15['TimeStep'], dfFiltered15['Sum_Pot_7']
x2, y2 = dfFiltered15['TimeStep'], dfFiltered15['Sum_Pot_6']
ax2.plot(x_ax, df2_DB15["Sum_Pot_7"], label='Pot Without VW')
ax2.plot(x_ax, df2_DB15["Sum_Pot_6"], label='Pot With VW')
ax2.set_xlim(18, 96)
ax2.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax2.add_patch(square)
# Zoom in on the square
axins2 = ax2.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins2.plot(x_ax, df2_DB15["Sum_Pot_7"])
axins2.plot(x_ax, df2_DB15["Sum_Pot_6"])
axins2.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins2.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins2.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', linewidth=3))

axins2.annotate(
    f"{round((100*(df2_DB15['Sum_Pot_7'].iloc[x1]-df2_DB15['Sum_Pot_6'].iloc[x1]))/df2_DB15['Sum_Pot_7'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins2.grid()







#######################################################################################################################
ax1 = fig3.add_subplot(3, 2, 3)
x1, y1 = dfFiltered30['TimeStep'], dfFiltered30['Sum_Pot_5']
x2, y2 = dfFiltered30['TimeStep'], dfFiltered30['Sum_Pot_4']
ax1.plot(x_ax, df2_DB30["Sum_Pot_5"], label='Pot Without VW')
ax1.plot(x_ax, df2_DB30["Sum_Pot_4"], label='Pot With VW')
ax1.set_xlim(18, 96)
ax1.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax1.add_patch(square)
# Zoom in on the square
axins1 = ax1.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins1.plot(x_ax, df2_DB30["Sum_Pot_5"])
axins1.plot(x_ax, df2_DB30["Sum_Pot_4"])
axins1.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins1.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins1.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', linewidth=3))

axins1.annotate(
    f"{round((100*(df2_DB30['Sum_Pot_5'].iloc[x1]-df2_DB30['Sum_Pot_4'].iloc[x1]))/df2_DB30['Sum_Pot_5'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins1.grid()

#######################################################################################################################
ax2 = fig3.add_subplot(3, 2, 4)
x1, y1 = dfFiltered30['TimeStep'], dfFiltered30['Sum_Pot_7']
x2, y2 = dfFiltered30['TimeStep'], dfFiltered30['Sum_Pot_6']
ax2.plot(x_ax, df2_DB30["Sum_Pot_7"], label='Pot Without VW')
ax2.plot(x_ax, df2_DB30["Sum_Pot_6"], label='Pot With VW')
ax2.set_xlim(18, 96)
ax2.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax2.add_patch(square)
# Zoom in on the square
axins2 = ax2.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins2.plot(x_ax, df2_DB30["Sum_Pot_7"])
axins2.plot(x_ax, df2_DB30["Sum_Pot_6"])
axins2.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins2.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins2.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', linewidth=3))

axins2.annotate(
    f"{round((100*(df2_DB30['Sum_Pot_7'].iloc[x1]-df2_DB30['Sum_Pot_6'].iloc[x1]))/df2_DB30['Sum_Pot_7'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins2.grid()







#######################################################################################################################
ax1 = fig3.add_subplot(3, 2, 5)
x1, y1 = dfFiltered50['TimeStep'], dfFiltered50['Sum_Pot_5']
x2, y2 = dfFiltered50['TimeStep'], dfFiltered50['Sum_Pot_4']
ax1.plot(x_ax, df2_DB50["Sum_Pot_5"], label='Pot Without VW')
ax1.plot(x_ax, df2_DB50["Sum_Pot_4"], label='Pot With VW')
ax1.set_xlim(18, 96)
ax1.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax1.add_patch(square)
# Zoom in on the square
axins1 = ax1.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins1.plot(x_ax, df2_DB50["Sum_Pot_5"])
axins1.plot(x_ax, df2_DB50["Sum_Pot_4"])
axins1.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins1.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins1.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', linewidth=3))

axins1.annotate(
    f"{round((100*(df2_DB50['Sum_Pot_5'].iloc[x1]-df2_DB50['Sum_Pot_4'].iloc[x1]))/df2_DB50['Sum_Pot_5'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins1.grid()

#######################################################################################################################
ax2 = fig3.add_subplot(3, 2, 6)
x1, y1 = dfFiltered50['TimeStep'], dfFiltered50['Sum_Pot_7']
x2, y2 = dfFiltered50['TimeStep'], dfFiltered50['Sum_Pot_6']
ax2.plot(x_ax, df2_DB50["Sum_Pot_7"], label='Pot Without VW')
ax2.plot(x_ax, df2_DB50["Sum_Pot_6"], label='Pot With VW')
ax2.set_xlim(18, 96)
ax2.legend()

# Draw the square
square = plt.Rectangle((x2 - x2 * 0.1, y2 - y2 * 0.025), x2 * 0.2, 2 * (y1-y2),
                       facecolor='none', edgecolor='red', linewidth=2)
ax2.add_patch(square)
# Zoom in on the square
axins2 = ax2.inset_axes([0.3, 0.06, 0.6, 0.6])  # Position and size of the zoomed-in plot
axins2.plot(x_ax, df2_DB50["Sum_Pot_7"])
axins2.plot(x_ax, df2_DB50["Sum_Pot_6"])
axins2.set_xlim((x2 - x2 * 0.1), ((x2 - x2 * 0.1) + x2 * 0.2))     # Adjust the x limits to move the square down
axins2.set_ylim((y2 - y2 * 0.025), ((y2 - y2 * 0.025) + 2 * (y1-y2)))  # Adjust the y limits to zoom in on the square

axins2.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', linewidth=3))

axins2.annotate(
    f"{round((100*(df2_DB50['Sum_Pot_7'].iloc[x1]-df2_DB50['Sum_Pot_6'].iloc[x1]))/df2_DB50['Sum_Pot_7'].iloc[x1], 2)} %",
    xy=(x1 + .5, (y1 + y2)/2), xytext=(x1 + .5, (y1 + y2)/2))
axins2.grid()












plt.show()



print()