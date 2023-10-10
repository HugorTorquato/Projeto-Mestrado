import matplotlib.pyplot as plt
import numpy as np
import pythonsql
import scipy.stats as stats
import pandas as pd

################################################################################################################

DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]

################################################################################################################

def GetHCPowerAVGData(db, tbl):
    command = f"""
                WITH 
                    GroupResults AS (
                        SELECT
                            [Case],
                            MAX(PV_Power)/45 AS HC_PV,
                            MAX(Total_Power)/45  AS HC_PV_BESS
                        FROM {db}.dbo.{tbl}
                        GROUP BY [Case]
                    )
                
                    SELECT 
                        AVG(HC_PV) AS AVG_HV_PV,
                        STDEV(HC_PV) AS STDEV_HV_PV,
                        AVG(HC_PV_BESS) AS AVG_HC_PV_BESS,
                        STDEV(HC_PV_BESS) AS STDEV_HC_PV_BESS
                    FROM GroupResults
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)


def GetHCPowerAVGDataByTimeStep(db, tbl):
    command = f"""
                SELECT 
                    TimeStep
                    , AVG(PV_Power) AS AVG_PV_Power_By_TimeStep
                    , AVG(BESS_Power) AS AVG_BESS_Power_By_TimeStep
                    , AVG(Total_Power) AS AVG_Total_Power_By_TimeStep
                FROM {db}.dbo.{tbl}
                GROUP BY TimeStep
                ORDER BY TimeStep
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command).set_index('TimeStep')


def Aggregate(DB_GROUP, table):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetHCPowerAVGData(db, table)
        else:
            db_Result = (db_Result + GetHCPowerAVGData(db, table)) / 2

    return db_Result

def AggregateByTimeStep(DB_GROUP, table):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetHCPowerAVGDataByTimeStep(db, table)
        else:
            db_Result = (db_Result + GetHCPowerAVGDataByTimeStep(db, table)) / 2

    return db_Result

def PlotDailyCurves(DATA1, DATA2, i):

    # Data
    time = np.linspace(0, 24, 96)  # Assuming one data point per hour

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

    # Plot the irradiance-like curves
    ax.plot(time, DATA1, color='blue', linewidth=2.5)
    ax.plot(time, DATA2, color='red', linewidth=2.5)

    # Fill the area below the curves with colors
    ax.fill_between(time, DATA1, color='blue', alpha=0.3, label='PV')
    ax.fill_between(time, DATA1, DATA2, color='red', alpha=0.3, label='PV and BESS')

    # Add labels and title
    ax.set_xlabel('Time (hours)', fontsize=17)
    ax.set_ylabel('Power Measurement (kW)', fontsize=17)



    # Customize x-axis tick labels to display hour values with a 2-hour interval
    interval = 8
    ax.set_xticks(time[::interval])
    ax.set_xticklabels([f'{int(t):02d}:00' for t in time[::interval]], rotation=45, ha='right', fontsize=15)
    plt.yticks(fontsize=15)


    # Set x-axis limits
    start_sample = 20
    end_sample = 76
    ax.set_xlim(time[start_sample], time[end_sample])

    # Set y-axis limits
    ax.set_ylim(0, 27)

    # Add grid
    ax.grid(True, linestyle='--',  alpha=0.9)

    # Add legend
    ax.legend(fontsize=15, loc='upper right')

    # Show the plot
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\HCC" + str(i) + ".png", dpi=300, bbox_inches='tight')
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\HCC" + str(i) + ".pdf", dpi=300, bbox_inches='tight')


################################################################################################################









df15_avg_ByTime_4 = AggregateByTimeStep(DB15, "vwGetPowerToHCCalculation4")
df30_avg_ByTime_4 = AggregateByTimeStep(DB30, "vwGetPowerToHCCalculation4")
df50_avg_ByTime_4 = AggregateByTimeStep(DB50, "vwGetPowerToHCCalculation4")

df15_avg_ByTime_6 = AggregateByTimeStep(DB15, "vwGetPowerToHCCalculation6")
df30_avg_ByTime_6 = AggregateByTimeStep(DB30, "vwGetPowerToHCCalculation6")
df50_avg_ByTime_6 = AggregateByTimeStep(DB50, "vwGetPowerToHCCalculation6")


PlotDailyCurves(df15_avg_ByTime_4['AVG_PV_Power_By_TimeStep'].values, df15_avg_ByTime_4['AVG_Total_Power_By_TimeStep'].values, 1)
PlotDailyCurves(df30_avg_ByTime_4['AVG_PV_Power_By_TimeStep'].values, df30_avg_ByTime_4['AVG_Total_Power_By_TimeStep'].values, 3)
PlotDailyCurves(df50_avg_ByTime_4['AVG_PV_Power_By_TimeStep'].values, df50_avg_ByTime_4['AVG_Total_Power_By_TimeStep'].values, 5)

PlotDailyCurves(df15_avg_ByTime_6['AVG_PV_Power_By_TimeStep'].values, df15_avg_ByTime_6['AVG_Total_Power_By_TimeStep'].values, 2)
PlotDailyCurves(df30_avg_ByTime_6['AVG_PV_Power_By_TimeStep'].values, df30_avg_ByTime_6['AVG_Total_Power_By_TimeStep'].values, 4)
PlotDailyCurves(df50_avg_ByTime_6['AVG_PV_Power_By_TimeStep'].values, df50_avg_ByTime_6['AVG_Total_Power_By_TimeStep'].values ,6)



plt.show()














# Group average results from multiple tables
df15_avg_4 = Aggregate(DB15, "vwGetPowerToHCCalculation4")
print(' -------------------------------- Averag result from DB15', DB15), print(df15_avg_4)
df30_avg_4 = Aggregate(DB30, "vwGetPowerToHCCalculation4")
print(' -------------------------------- Averag result from DB30', DB30), print(df30_avg_4)
df50_avg_4 = Aggregate(DB50, "vwGetPowerToHCCalculation4")
print(' -------------------------------- Averag result from DB50', DB50), print(df50_avg_4)

print("------------------------------------------------------------------------------------------------")
# Group average results from multiple tables
df15_avg_4 = Aggregate(DB15, "vwGetPowerToHCCalculation6")
print(' -------------------------------- Averag result from DB15', DB15), print(df15_avg_4)
df30_avg_4 = Aggregate(DB30, "vwGetPowerToHCCalculation6")
print(' -------------------------------- Averag result from DB30', DB30), print(df30_avg_4)
df50_avg_4 = Aggregate(DB50, "vwGetPowerToHCCalculation6")
print(' -------------------------------- Averag result from DB50', DB50), print(df50_avg_4)

print("------------------------------------------------------------------------------------------------")










print()

