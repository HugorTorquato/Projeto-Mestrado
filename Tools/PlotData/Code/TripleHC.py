"""
This code aims to aggregate the average HC values into 3 tables and generate a forth one with the comparison
relation between them ( 15->30, 15->50, 30->50 ).
Also it is getting all HC results and adding into a boxplot for each configuration
"""

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd

################################################################################################################
def GetHCDATA(db):
    command = f"""
                SELECT * FROM {db}.dbo.tblGeneral
                """
    df = pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)
    return df[['Simulation', 'Case', 'SimulationCount', 'HC']] \
        .drop("Simulation", axis=1).where((df['SimulationCount'] != 5) & (df['SimulationCount'] != 7)).dropna()

def GetHCStatcDATA(db):
    command = f"""
                SELECT * FROM {db}.dbo.spStatisticalResults
                """
    df = pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)
    return df.drop("id", axis=1).where((df['Simulation'] != 5) & (df['Simulation'] != 7)).dropna()

def Aggregate(DB_GROUP):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetHCStatcDATA(db)
        else:
            db_Result = (db_Result + GetHCStatcDATA(db)) / 2

    return db_Result

def CompareHC(df15_avg, df30_avg, df50_avg):
    Compare_Results = pd.DataFrame({
        'Simulation' : [],
        '15->30'     : [],
        '15->50'     : [],
        '30->50'     : []})

    Compare_Results['Simulation'] = df15_avg['Simulation']
    Compare_Results['15->30'] = 100 * (1 - df15_avg['Average'] / df30_avg['Average'])
    Compare_Results['15->50'] = 100 * (1 - df15_avg['Average'] / df50_avg['Average'])
    Compare_Results['30->50'] = 100 * (1 - df30_avg['Average'] / df50_avg['Average'])

    return Compare_Results

def CreateBoxPlot(DB_GROUP):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetHCDATA(db)
        else:
            db_Result = pd.concat([db_Result, GetHCDATA(db)], axis=0)

    bp = plt.boxplot([db_Result[db_Result['SimulationCount'] == 2]['HC'] * 100,
                 db_Result[db_Result['SimulationCount'] == 3]['HC'] * 100,
                 db_Result[db_Result['SimulationCount'] == 4]['HC'] * 100,
                 db_Result[db_Result['SimulationCount'] == 6]['HC'] * 100],
                showmeans=True, widths=0.7, meanline=True)

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

    plt.xticks([1, 2, 3, 4], ['Without Control', 'VV', 'VW', 'VV+VW'], fontsize=17)
    plt.ylim(0, 100), plt.yticks(fontsize=15), plt.ylabel('HC(%)',  fontsize=17)
    #plt.title('Boxplot of HC simulations', fontsize=14, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.9)
    plt.tick_params(axis='both', labelsize=15)





    # Save as PDF and PNG
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\HC_BOXPLOT_" + str(DB_GROUP) + ".pdf",
                format='pdf', transparent=True)
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\HC_BOXPLOT_" + str(DB_GROUP) + ".png")

    return

################################################################################################################

# Define all tables related to each group
DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]

# Group average results from multiple tables
df15_avg = Aggregate(DB15)
print(' Averag result from DB15', DB15), print(df15_avg)
df30_avg = Aggregate(DB30)
print(' Averag result from DB30', DB30), print(df30_avg)
df50_avg = Aggregate(DB50)
print(' Averag result from DB50', DB50), print(df50_avg)

# Create a third dataframe with the relation betweehn them ( Average and STD )
Compare_HC = CompareHC(df15_avg, df30_avg, df50_avg)
print(' Compared average HC from all configurations '), print(Compare_HC)

# Create all Box Plots
fig_TripleHC_15, ax_15 = plt.subplots()
CreateBoxPlot(DB15)
fig_TripleHC_30, ax_30 = plt.subplots()
CreateBoxPlot(DB30)
fig_TripleHC_50, ax_50 = plt.subplots()
CreateBoxPlot(DB50)
