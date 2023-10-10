""""

    """

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

################################################################################################################



def GetLoadNames(db):
    command = f"""
            SELECT 
                DISTINCT(Elemento)
            FROM {db}.dbo.tblMonitoresData 
            WHERE 
                Elemento like 'load.c%'
                AND Measurement like ' P%'
                AND [Case] = 1 AND Simulation = 1
            """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def GetActivationOcurrency(db, load, PQ, phase):
    command = f"""
            SELECT 
                * 
            FROM {db}.dbo.tblMonitoresData 
            WHERE 
                Elemento = '{load[0]}'
                AND Measurement like ' {PQ}{phase}%'
                AND [Case] = 1 AND Simulation = 1
            """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def Plot(db):

    loadNames = GetLoadNames(db)

    #plt.figure(1)
    db_Result = pd.DataFrame()
    data = pd.DataFrame()

    steps = np.arange(96)
    hours = np.arange(0, 24, 0.25)
    time_labels = [f"{int(h):02d}:{int((h%1)*60):02d}" for h in hours]

    fig10, axs = plt.subplots(figsize=(6, 4), dpi=300)

    for load in loadNames.values:
        for phase in ['1', '2', '3']:

            data = GetActivationOcurrency(db, load, 'P', phase)['Value']

            if db_Result.empty:
                db_Result = data
                axs.plot(data.values, linewidth=1)
            elif not data.empty and abs(data.values[0]) > 0.05:
                db_Result = (db_Result + data) / 2
                axs.plot(data.values, linewidth=1)

    axs.plot(db_Result.values, color='Black', label='Average Active Load Demand', linewidth=6)
    axs.grid(True, linestyle='--', alpha=0.9)
    axs.set_xticks(steps[::8])  # Show every 4th step
    axs.set_xticklabels(time_labels[::8], rotation=45, fontsize=15)
    axs.tick_params(axis='both', labelsize=15)
    axs.set_ylabel('Power (kW)', fontsize=17)
    axs.set_xlabel('Time (Hour)', fontsize=17)
    fig10.legend(fontsize=11, loc='upper right')

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_LoadPowerShapeP.pdf",
                format='pdf', transparent=True, dpi=300, bbox_inches='tight')
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
            "\Plot_LoadPowerShapeP.png", dpi=300, bbox_inches='tight')


    fig11, axs = plt.subplots(figsize=(6, 4), dpi=300)
    db_Result = pd.DataFrame()

    for load in loadNames.values:
        for phase in ['1', '2', '3']:

            data = GetActivationOcurrency(db, load, 'Q', phase)['Value']

            if db_Result.empty:
                db_Result = data
                axs.plot(data.values, linewidth=2)
            elif not data.empty and abs(data.values[0]) > 0.05:
                db_Result = (db_Result + data) / 2
                axs.plot(data.values, linewidth=2)

    axs.plot(db_Result.values, color='Black', label='Average Reactive Load Demand', linewidth=6)
    axs.grid(True, linestyle='--', alpha=0.9)
    axs.set_xticks(steps[::8])  # Show every 4th step
    axs.set_xticklabels(time_labels[::8], rotation=45, fontsize=15)
    axs.tick_params(axis='both', labelsize=15)
    axs.set_ylabel('Power (kVAr)', fontsize=17)
    axs.set_xlabel('Time (Hour)', fontsize=17)
    fig11.legend(fontsize=11, loc='upper right')

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_LoadPowerShapeQ.pdf",
                format='pdf', transparent=True, dpi=300, bbox_inches='tight')
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_LoadPowerShapeQ.png", dpi=300, bbox_inches='tight')

    print()



################################################################################################################


DB = "DB_Rede_3_50_2706_15"

data = Plot(DB)

print()

