
import numpy as np
import pandas as pd

import pythonsql
import matplotlib.pyplot as plt

DB = 'DB_Rede_3_50_2403'
CASE = 37
SIMULATION = 6


# CASO 1 DO BANCO 'DB_Rede_3_50_2403' SIMULAÇÃO 6 É LEGAL
# CASO 2 DO BANCO 'DB_Rede_3_50_2403' SIMULAÇÃO 6 É LEGAL
# CASO 5 DO BANCO 'DB_Rede_3_50_2403' SIMULAÇÃO 6 É LEGAL
# CASO 20 DO BANCO 'DB_Rede_3_50_2403' SIMULAÇÃO 6 É LEGAL

# Creio que foi PV em barra do trafo de entrada
# CASO 17 DO BANCO 'DB_Rede_3_50_1403' SIMULAÇÃO 6 É LEGAL
# CASO 20 DO BANCO 'DB_Rede_3_50_1403' SIMULAÇÃO 6 É LEGAL


def Query_to_Collect_Control_DATA(db, monitorElement, case, simulation):
    command = f"""
                SELECT 
                    *
                FROM {db}.dbo.spSummary_InvControlData
                WHERE id_Summary = 
                (   
                    SELECT id FROM {db}.dbo.spSummary_InvControl 
                    WHERE Monitor = '{monitorElement}'
                        AND [Case] = {case}
                        AND Simulation = {simulation}
                )
            """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)


# Collect trigger actions data from invcontrol

InvControl_Monitors_Name = pythonsql.SQLActions(DB).returnTableFromSQLasDataframe(
    f"""
        SELECT 
            distinct(Monitor) 
        FROM spSummary_InvControl 
        WHERE Monitor like '%invcontrol%'
    """
)

# Popular um dataframe com os resultados.... agora como...
# Vai vir um grandão com tudo...

ControlValues = pd.DataFrame()

for MON in InvControl_Monitors_Name.values:
    SQLDATA = Query_to_Collect_Control_DATA(DB, MON[0], CASE, SIMULATION)
    data = {
        'Element'  : MON[0],
        'Vreg'     : SQLDATA[SQLDATA['Measurement'] == 'Vreg'].Value.values,
        'volt-var' : SQLDATA[SQLDATA['Measurement'] == 'volt-var'].Value.values,
        'volt-watt': SQLDATA[SQLDATA['Measurement'] == 'volt-watt'].Value.values
    }
    ControlValues = pd.concat([ControlValues, pd.DataFrame(data)])


# Collect power data from power monitors

Power_Monitors_Name = pythonsql.SQLActions(DB).returnTableFromSQLasDataframe(
    f"""
        SELECT 
            distinct(Monitor) 
        FROM spSummary_InvControl 
        WHERE Monitor like '%power%'
    """
)

# Collect overall power o phase by phase?
PowerValues = pd.DataFrame()

for MON in Power_Monitors_Name.values:
    SQLDATA = Query_to_Collect_Control_DATA(DB, MON[0], CASE, SIMULATION)
    SQLDATA['Measurement'] = SQLDATA['Measurement'].str.replace('\x00', '')

    data = {'Element': MON[0]}
    measurements = [' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)']

    for measurement in measurements:
        if measurement in SQLDATA['Measurement'].values:
            data[measurement] = SQLDATA[SQLDATA['Measurement'] == measurement].Value.values
        else:
            # A good test is to use NONE instead of 0. And compare SQLDATA for monitors without phases
            # data[measurement] = "NONE"
            data[measurement] = 0

    PowerValues = pd.DataFrame(data) if PowerValues.empty else pd.concat([PowerValues, pd.DataFrame(data)])


countplot = 1
numRows = 2
numColm = ControlValues['Element'].unique().size



def Plot_Contro_Power(CombTemp, monitor):


    steps = np.arange(96)
    hours = np.arange(0, 24, 0.25)
    time_labels = [f"{int(h):02d}:{int((h%1)*60):02d}" for h in hours]


    fig10, axs = plt.subplots(figsize=(6, 4), dpi=300)
    axs.plot(CombTemp['Vreg'], linewidth=2.5, label='V Reference')
    axs.axhline(y=1.01, color='black', linestyle='--', linewidth=2.5)
    axs.axhline(y=0.99, color='black', linestyle='--', linewidth=2.5)
    axs.axhline(y=1.03, color='black', linestyle='-', linewidth=2.5)

    ax2 = axs.twinx()

    ax2.plot(CombTemp['volt-var'], color='blue', label='Volt-Var', linewidth=2.5) \
        if CombTemp['volt-var'].max() <= 1 else 0
    ax2.plot(CombTemp['volt-watt'], color='green', label='Volt-Watt', linewidth=2.5) \
        if CombTemp['volt-watt'].max() <= 1 else 0

    #axs.set_title('(A) Voltage control strategies references', fontsize=16, weight='bold')
    axs.set_ylim(0.93, 1.07), ax2.set_ylim(-1.1, 1.1)
    fig10.legend(fontsize=11, bbox_to_anchor=(0.9, 0.9))
    ax2.tick_params(axis='both', labelsize=15)
    ax2.set_ylabel('Control Operation', fontsize=17, rotation=270, labelpad=15)
    axs.grid(True, linestyle='--', alpha=0.9)
    axs.tick_params(axis='both', labelsize=15)
    axs.set_ylabel('Voltage Reference (pu)', fontsize=17)
    axs.set_xlabel('Time (Hour)', fontsize=17)
    #axs[0].set_xlabel('Time', fontsize=12)
    axs.set_xticks(steps[::8])  # Show every 4th step
    axs.set_xticklabels(time_labels[::8], rotation=45, fontsize=15)

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_Contro_Power_Activation_" + str(monitor) + ".pdf",
                format='pdf', transparent=True, dpi=300, bbox_inches='tight')
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_Contro_Power_Activation_" + str(monitor) + ".png", dpi=300, bbox_inches='tight')

    fig11, axs2 = plt.subplots(figsize=(6, 4), dpi=300)
    axs2.plot(CombTemp[' P1 (kW)'], label='P1(kW)', linewidth=2.5)
    axs2.plot(CombTemp[' P2 (kW)'], label='P2(kW)', linewidth=2.5)
    axs2.plot(CombTemp[' P3 (kW)'], label='P2(kW)', linewidth=2.5)
    axs2.plot(CombTemp[' Q1 (kvar)'], label='Q1(kVAr)', linewidth=2.5)
    axs2.plot(CombTemp[' Q2 (kvar)'], label='Q2(kVAr)', linewidth=2.5)
    axs2.plot(CombTemp[' Q3 (kvar)'], label='Q3(kVAr)', linewidth=2.5)



    #axs2.set_title('(B) Voltage control strategies results', fontsize=16, weight='bold')
    axs2.legend(fontsize=11, loc='upper right')
    axs2.grid(True, linestyle='--', alpha=0.9)
    axs2.tick_params(axis='both', labelsize=15)
    axs2.set_ylabel('Power Reference', fontsize=17)
    axs2.set_xlabel('Time (Hour)', fontsize=17)
    #axs[1].set_xlabel('Time', fontsize=12)
    axs2.set_xticks(steps[::8])  # Show every 4th step
    axs2.set_xticklabels(time_labels[::8], rotation=45, fontsize=15)

    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_Contro_Power_Power_" + str(monitor) + ".pdf",
                format='pdf', transparent=True, dpi=300, bbox_inches='tight')
    plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Dissertação\Figs" +
                "\Plot_Contro_Power_Power_" + str(monitor) + ".png", dpi=300, bbox_inches='tight')

    #fig10.suptitle('Voltage Control Strategies Response', fontsize=18, weight='bold')
    #fig10.subplots_adjust(top=0.92)



for monitor in ControlValues['Element'].unique():

    TempControlValues = ControlValues[ControlValues['Element'] == monitor]
    TempPowerValues = \
        PowerValues[PowerValues['Element'].str.replace('pvsystem_', '').str.replace('_power', '') ==
                    monitor.replace('invcontrol_', '')]

    TempControlValues['Element'] = TempControlValues['Element'].str.replace('invcontrol_', '')
    TempPowerValues['Element'] = TempPowerValues['Element'].str.replace('pvsystem_', '').str.replace('_power', '')


    CombTemp = pd.concat([TempControlValues, TempPowerValues], axis=1)

    Plot_Contro_Power(CombTemp, monitor)



print()