"""


"""

import pythonsql
import matplotlib.pyplot as plt

DB = "DB_Rede_3_50_2706_15"

def GetPowerDataTable(db):
    # Fazer verificação se a vw está definida?
    command = f"""
                SELECT 
                    *
                FROM {db}.dbo.vwBESSAVGResults
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)


dfDB = GetPowerDataTable(DB)

fig7, axs = plt.subplots(1, 2, figsize=(9, 5))
tick_labels = ["VW Control", "VW and VV Controls"]

axs[0].boxplot(
    [
        dfDB[dfDB['AVG_MAX_Pot_Diff_5_4'] < 10000]['AVG_MAX_Pot_Diff_5_4'],
        dfDB[dfDB['AVG_MAX_Pot_Diff_7_6'] < 10000]['AVG_MAX_Pot_Diff_7_6']
    ],
    positions=[1, 2], showmeans=True, widths=0.5, meanline=True)

axs[1].boxplot(
    [
        dfDB[dfDB['ADJ_Battery_Capacity_5_4'] < 10000]['ADJ_Battery_Capacity_5_4'],
        dfDB[dfDB['ADJ_Battery_Capacity_7_6'] < 10000]['ADJ_Battery_Capacity_7_6']
    ],
    positions=[3, 4], showmeans=True, widths=0.5, meanline=True)

axs[0].set_ylabel('Power(W)', fontsize=12), axs[1].set_ylabel('Energy (Wh)', fontsize=12)
axs[0].set_title('(A) Maximum Battery Power', fontsize=12, weight='bold')
axs[1].set_title('(B) Battery Adjusted Energy', fontsize=12, weight='bold')
axs[0].grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.25)
axs[1].grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.25)
axs[0].set_xticklabels(tick_labels, fontsize=12), axs[1].set_xticklabels(tick_labels, fontsize=12)

fig7.suptitle('Battery Sizing Metrics', fontsize=16, weight='bold')

plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Figs\Artigo2" +
            "\BOXPLOT_Bat_Sizing_DB_" + str(DB) + ".pdf",
            format='pdf', transparent=True)
plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Figs\Artigo2" + "\BOXPLOT_Bat_Sizing_DB_" + str(DB))




print()

