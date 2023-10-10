"""
This code aims to aggregate the average HC values into 3 tables and generate a forth one with the comparison
relation between them ( 15->30, 15->50, 30->50 ).
Also it is getting all HC results and adding into a boxplot for each configuration
"""

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.max_rows', None)  # Display all rows


################################################################################################################

def GetPowerDataStatTable(db):
    command = f"""
                SELECT 
                    AVG(AVG_MAX_Pot_Diff_5_4)       AS AVG_MAX_Pot_Diff_5_4,
                    STDEV(AVG_MAX_Pot_Diff_5_4)     AS STDEV_AVG_MAX_Pot_Diff_5_4,
                    AVG(AVG_MAX_Pot_Diff_7_6)       AS AVG_MAX_Pot_Diff_7_6,
                    STDEV(AVG_MAX_Pot_Diff_7_6)     AS STDEV_AVG_MAX_Pot_Diff_7_6,
                    AVG(ADJ_Battery_Capacity_5_4)   AS ADJ_Battery_Capacity_5_4,
                    STDEV(ADJ_Battery_Capacity_5_4) AS STDEV_ADJ_Battery_Capacity_5_4,
                    AVG(ADJ_Battery_Capacity_7_6)   AS ADJ_Battery_Capacity_7_6,
                    STDEV(ADJ_Battery_Capacity_7_6) AS STDEV_ADJ_Battery_Capacity_7_6
                FROM vwBESSAVGResults
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def Aggregate(DB_GROUP):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetPowerDataStatTable(db)
        else:
            db_Result = (db_Result + GetPowerDataStatTable(db)) / 2

    return db_Result

def CompareBESS(df15_avg, df30_avg, df50_avg, field):

    Compare_BESS = pd.DataFrame({
        'Config': str(field),
        '15->30': 100 * (1 - df15_avg[field].values / df30_avg[field].values),
        '15->50': 100 * (1 - df15_avg[field].values / df50_avg[field].values),
        '30->50': 100 * (1 - df30_avg[field].values / df50_avg[field].values)
    })

    return Compare_BESS

def GetPowerDataTable(db):
    command = f"""
                SELECT *
                FROM {db}.dbo.vwBESSAVGResults
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)
    #dfDB = pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)
    #return dfDB[
    #    dfDB['AVG_MAX_Pot_Diff_5_4'] < 10000 &
    #    dfDB['AVG_MAX_Pot_Diff_7_6'] < 10000 &
    #    dfDB['ADJ_Battery_Capacity_5_4'] < 10000 &
    #    dfDB['ADJ_Battery_Capacity_7_6'] < 10000]

def CreateBoxPlot(DB_GROUP):

    fig_TripleBESS, axs = plt.subplots(figsize=(7, 6))


    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetPowerDataTable(db)
        else:
            db_Result = pd.concat([db_Result, GetPowerDataTable(db)], axis=0)

    tick_labels = ["VW Control", "VW and VV Controls"]

    bp = axs.boxplot(
        [
            db_Result['AVG_MAX_Pot_Diff_5_4'],
            db_Result['AVG_MAX_Pot_Diff_7_6']
        ],
        positions=[1, 2], showmeans=True, widths=0.5, meanline=True)

    # Customize box border linewidth (change 2 to your desired value)
    for box in bp['boxes']:
        box.set_linewidth(2)

    # Customize whisker and cap (quartile limit) linewidth (change 2 to your desired value)
    for whisker, cap in zip(bp['whiskers'], bp['caps']):
        whisker.set_linewidth(2)
        cap.set_linewidth(2)

    # Set the linewidth for the median and mean lines
    for median_line, mean_line in zip(bp['medians'], bp['means']):
        median_line.set_linewidth(2)  # Adjust the linewidth for the median line
        mean_line.set_linewidth(2)    # Adjust the linewidth for the mean line

    # Add a legend for median and mean
    legend_labels = ['Median', 'Mean']
    legend_handles = [plt.Line2D([0], [0], color='orange', lw=2),
                      plt.Line2D([0], [0], linestyle='--', color='green', lw=2)]
    plt.legend(legend_handles, legend_labels, loc='upper right', fontsize=15)


    axs.set_ylabel('Power(W)', fontsize=17)
    axs.tick_params(axis='both', labelsize=15)
    axs.grid(True, linestyle='--', alpha=0.9)
    axs.set_xticklabels(tick_labels, fontsize=15)

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\BESS_CreateBoxPlot_Power_" + str(DB_GROUP) + ".pdf",
                format='pdf', transparent=True)
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\BESS_CreateBoxPlot_Power_" + str(DB_GROUP) + ".png")

    fig_TripleBESS2, axs2 = plt.subplots(figsize=(7, 6))
    bp = axs2.boxplot(
        [
            db_Result['ADJ_Battery_Capacity_5_4'],
            db_Result['ADJ_Battery_Capacity_7_6']
        ],
        positions=[3, 4], showmeans=True, widths=0.5, meanline=True)

    #axs2.set_ylabel('Energy (Wh)', fontsize=12)
    #axs.set_title('(A) Maximum Battery Power', fontsize=12, weight='bold')
    #axs2.set_title('(B) Battery Adjusted Energy', fontsize=12, weight='bold')



    # Customize box border linewidth (change 2 to your desired value)
    for box in bp['boxes']:
        box.set_linewidth(2)

    # Customize whisker and cap (quartile limit) linewidth (change 2 to your desired value)
    for whisker, cap in zip(bp['whiskers'], bp['caps']):
        whisker.set_linewidth(2)
        cap.set_linewidth(2)

    # Set the linewidth for the median and mean lines
    for median_line, mean_line in zip(bp['medians'], bp['means']):
        median_line.set_linewidth(2)  # Adjust the linewidth for the median line
        mean_line.set_linewidth(2)    # Adjust the linewidth for the mean line

    # Add a legend for median and mean
    legend_labels = ['Median', 'Mean']
    legend_handles = [plt.Line2D([0], [0], color='orange', lw=2),
                      plt.Line2D([0], [0], linestyle='--', color='green', lw=2)]
    plt.legend(legend_handles, legend_labels, loc='upper right', fontsize=15)


    axs2.set_ylabel('Energy (Wh)', fontsize=17)
    axs2.tick_params(axis='both', labelsize=15)
    axs2.grid(True, linestyle='--', alpha=0.9)
    axs2.set_xticklabels(tick_labels, fontsize=15)





    #axs2.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.25)
    #axs2.set_xticklabels(tick_labels, fontsize=12)

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\BESS_CreateBoxPlot_Energy_" + str(DB_GROUP) + ".pdf",
                format='pdf', transparent=True)
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\BESS_CreateBoxPlot_Energy_" + str(DB_GROUP) + ".png")

    #fig_TripleBESS.suptitle('Battery Sizing Metrics', fontsize=16, weight='bold')

    return

def GetAVGBessKPIData(db, table):
    command = f"""
                SELECT 
                    AVG(EnergByPot)       AS AVG_EnergyByPot,
                    STDEV(EnergByPot)     AS STDEV_AVG_EnergyByPot,
                    AVG(MaxPotByPVSize)       AS AVG_MaxPotByPVSize,
                    STDEV(MaxPotByPVSize)     AS STDEV_MaxPotByPVSize
                FROM {db}.dbo.{table}
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def AggregateKPI(DB_GROUP, table):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetAVGBessKPIData(db, table)
        else:
            db_Result = (db_Result + GetAVGBessKPIData(db, table)) / 2

    return db_Result

def GetBessKPIData(db, table):
    command = f"""
                SELECT *
                FROM {db}.dbo.{table}
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def CreateBoxPlotKPI(DB_GROUP):

    fig_TripleBESS, axs = plt.subplots(figsize=(9, 5))
    fig_TripleBESS2, axs2 = plt.subplots(figsize=(9, 5))
    db_Result1 = pd.DataFrame()
    db_Result2 = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result1.empty:
            db_Result1 = GetBessKPIData(db, "vwCompareBatSizingWithPV54")
        else:
            db_Result1 = pd.concat([db_Result1, GetBessKPIData(db, "vwCompareBatSizingWithPV54")], axis=0)

    for db in DB_GROUP:
        if db_Result2.empty:
            db_Result2 = GetBessKPIData(db, "vwCompareBatSizingWithPV76")
        else:
            db_Result2 = pd.concat([db_Result2, GetBessKPIData(db, "vwCompareBatSizingWithPV76")], axis=0)

    tick_labels = ["VW Control", "VW and VV Controls"]

    axs.boxplot(
        [
            db_Result1['EnergByPot'],
            db_Result1['MaxPotByPVSize']
        ],
        positions=[1, 2], showmeans=True, widths=0.5, meanline=True)

    axs2.boxplot(
        [
            db_Result2['EnergByPot'],
            db_Result2['MaxPotByPVSize']
        ],
        positions=[3, 4], showmeans=True, widths=0.5, meanline=True)

    axs.set_ylabel('Power(W)', fontsize=12), axs2.set_ylabel('Energy (Wh)', fontsize=12)
    #axs.set_title('(A) AVG_EnergyByPot', fontsize=12, weight='bold')
    #axs.set_title('(B) AVG_MaxPotByPVSize', fontsize=12, weight='bold')
    axs.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.25)
    axs2.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.25)
    axs.set_xticklabels(tick_labels, fontsize=12), axs2.set_xticklabels(tick_labels, fontsize=12)

    #fig_TripleBESS.suptitle('Battery Sizing Metrics', fontsize=16, weight='bold')

    return

################################################################################################################

# Define all tables related to each group
DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]



# Group average results from multiple tables
df15_avg = Aggregate(DB15)
print(' -------------------------------- Averag result from DB15', DB15), print(df15_avg)
df30_avg = Aggregate(DB30)
print(' -------------------------------- Averag result from DB30', DB30), print(df30_avg)
df50_avg = Aggregate(DB50)
print(' -------------------------------- Averag result from DB50', DB50), print(df50_avg)

# Create a fourth dataframe with the relation between them ( Average and STD )
Compare = pd.DataFrame()

Compare = pd.concat([Compare, CompareBESS(df15_avg, df30_avg, df50_avg, "AVG_MAX_Pot_Diff_5_4")]
                    , ignore_index=True)
Compare = pd.concat([Compare, CompareBESS(df15_avg, df30_avg, df50_avg, 'AVG_MAX_Pot_Diff_7_6')]
                    , ignore_index=True)
Compare = pd.concat([Compare, CompareBESS(df15_avg, df30_avg, df50_avg, 'ADJ_Battery_Capacity_5_4')]
                    , ignore_index=True)
Compare = pd.concat([Compare, CompareBESS(df15_avg, df30_avg, df50_avg, 'ADJ_Battery_Capacity_7_6')]
                    , ignore_index=True)

print(' Compared average BESS  from all configurations '), print(Compare)

#### Create a fifth dataframe with the relation between them ( Average and STD )

# Basicamente vão ser duas discuções aqui, uma para cada KPI....
df15_kpi_BatSiz = AggregateKPI(DB15, "vwCompareBatSizingWithPV54")
print(' -------------------------------- Averag result from df15_kpi_BatSiz ', DB15), print(df15_kpi_BatSiz)
df30_kpi_BatSiz = AggregateKPI(DB30, "vwCompareBatSizingWithPV54")
print(' -------------------------------- Averag result from df30_kpi_BatSiz ', DB30), print(df30_kpi_BatSiz)
df50_kpi_BatSiz = AggregateKPI(DB50, "vwCompareBatSizingWithPV54")
print(' -------------------------------- Averag result from df50_kpi_BatSiz ', DB50), print(df50_kpi_BatSiz)

df15_kpi_wPV = AggregateKPI(DB15, "vwCompareBatSizingWithPV76")
print(' -------------------------------- Averag result from df15_kpi_wPV ', DB15), print(df15_kpi_wPV)
df30_kpi_wPV = AggregateKPI(DB30, "vwCompareBatSizingWithPV76")
print(' -------------------------------- Averag result from df30_kpi_wPV ', DB30), print(df30_kpi_wPV)
df50_kpi_wPV = AggregateKPI(DB50, "vwCompareBatSizingWithPV76")
print(' -------------------------------- Averag result from df50_kpi_wPV ', DB50), print(df50_kpi_wPV)

# Comparar os resutlados médios

Compare_BatSiz = pd.DataFrame()
Compare_wPV = pd.DataFrame()

Compare_BatSiz = pd.concat([Compare_BatSiz, CompareBESS(df15_kpi_BatSiz, df30_kpi_BatSiz, df50_kpi_BatSiz, "AVG_EnergyByPot")]
                    , ignore_index=True)
Compare_BatSiz = pd.concat([Compare_BatSiz, CompareBESS(df15_kpi_BatSiz, df30_kpi_BatSiz, df50_kpi_BatSiz, 'AVG_MaxPotByPVSize')]
                    , ignore_index=True)
Compare_wPV = pd.concat([Compare_wPV, CompareBESS(df15_kpi_wPV, df30_kpi_wPV, df50_kpi_wPV, 'AVG_EnergyByPot')]
                    , ignore_index=True)
Compare_wPV = pd.concat([Compare_wPV, CompareBESS(df15_kpi_wPV, df30_kpi_wPV, df50_kpi_wPV, 'AVG_MaxPotByPVSize')]
                    , ignore_index=True)


# Create all Box Plots

CreateBoxPlot(DB15)
CreateBoxPlot(DB30)
CreateBoxPlot(DB50)

# Vou ter de fazer outro box plot para ti ( mudar y range e titulos )
#CreateBoxPlotKPI(DB15)
#CreateBoxPlotKPI(DB30)
#CreateBoxPlotKPI(DB50)

print()




