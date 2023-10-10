""""
This code aims to aggregate the average HC values into 3 tables and generate a forth one with the comparison
relation between them ( 15->30, 15->50, 30->50 ).
Also it is getting all HC results and adding into a boxplot for each configuration
    """

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd

################################################################################################################

def GetActivationOcurrency(db):
    command = f"""
            SELECT 
                *
            FROM {db}.dbo.vwFindBusMostCommonActivations
            """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def Aggregate(DB_GROUP):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetActivationOcurrency(db)
        else:
            db_Result = pd.concat([db_Result, GetActivationOcurrency(db)], ignore_index=True)

    return db_Result

def plotbars(db, DB_GROUP):

    db.index = db.index.str.replace('bus_33998182', 'Bus')
    top_10_data = db.sort_values('Bus', ascending=False).head(10)

    fig1, ax = plt.subplots(figsize=(9, 8))

    min_value = top_10_data['Bus'].min()
    max_value = top_10_data['Bus'].max()
    norm = plt.Normalize(min_value, max_value)
    cmap = plt.cm.RdBu_r

    bars = ax.bar(top_10_data .index.values, top_10_data ['Bus'].values, color=cmap(norm(top_10_data ['Bus'].values)))
    ax.set_xticklabels(top_10_data.index.values, rotation=45, fontsize=14)
    ax.set_ylabel('Number of Occurrences', fontsize=14)
    ax.set_ylim(10, 35)

    # Create a colorbar for the color division
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Set an empty array to map the colors
    cbar = plt.colorbar(sm)
    cbar.set_label('Occurrences', fontsize=14)

    # Save as PDF and PNG
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\VVVW_Violation_Ocurrency_" + str(DB_GROUP) + ".pdf",
                format='pdf', transparent=True)
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\VVVW_Violation_Ocurrency_" + str(DB_GROUP) + ".png")


################################################################################################################

# Define all tables related to each group
DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]

db15_count = pd.DataFrame(Aggregate(DB15)['Bus'].value_counts())
db30_count = pd.DataFrame(Aggregate(DB30)['Bus'].value_counts())
db50_count = pd.DataFrame(Aggregate(DB50)['Bus'].value_counts())

################################################################################################################

plotbars(db15_count, DB15)
plotbars(db30_count, DB30)
plotbars(db50_count, DB50)


plt.show()

print()
