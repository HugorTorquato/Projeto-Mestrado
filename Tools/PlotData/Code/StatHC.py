import matplotlib.pyplot as plt
import numpy as np
import pythonsql
import scipy.stats as stats
import pandas as pd


def GetHCTableBySimulation(db, simulation):
    x = pythonsql.SQLActions(db)
    command = f"""
                SELECT * FROM {db}.dbo.spStatisticalResults WHERE Simulation = {simulation}
                """
    df = x.returnTableFromSQLasDataframe(command)
    return df.drop("id", axis=1).where((df['Simulation'] != 5) & (df['Simulation'] != 7)).dropna()


def GetHCDATABySimulation(db, simulation):
    x = pythonsql.SQLActions(db)
    command = f"""
                SELECT * FROM {db}.dbo.tblGeneral where simulationCount = {simulation}
                """
    df = x.returnTableFromSQLasDataframe(command)
    return df[['Case', 'HC']].dropna()


def GetHCDATA(db):
    x = pythonsql.SQLActions(db)
    command = f"""
                SELECT * FROM {db}.dbo.tblGeneral
                """
    df = x.returnTableFromSQLasDataframe(command)
    return df[['Simulation', 'Case', 'SimulationCount', 'HC']] \
        .drop("Simulation", axis=1).where((df['SimulationCount'] != 5) & (df['SimulationCount'] != 7)).dropna()


"""
NOT IN USE - I'm not using this Normal distribution in Results

# Test for normality using the Shapiro-Wilk test
def Normality_Test(data):
    print('Normality Test (Shapiro-Wilk):')
    stat, p = stats.shapiro(data)
    alpha = 0.05
    print(f"Data1 (Normal Distribution): stat={stat:.4f}, p-value={p:.4f}")
    if p > alpha:
        print("The null hypothesis cannot be rejected. Data1 may follow a normal distribution.\n")
    else:
        print("The null hypothesis can be rejected. Data1 may not follow a normal distribution.\n")


def PlotBoxPlot(data, mean, std):
    
    # Test created to validate if Normal distribution was applied ( NOT IN USE )
    Normality_Test(data)

    # Calculate X and Y values for the normal distribution  ( Função Densidade de Probabilidade )
    x = np.linspace(mean - 3*std, mean + 3*std, 100)   
    y = 1/(std * np.sqrt(2 * np.pi)) * np.exp(-(x - mean)**2 / (2 * std**2))

    # Create the plot
    fig, ax = plt.subplots()
    stats.probplot(data, dist="norm", plot=plt)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.hist(data, density=True, alpha=0.5)  # Add a histogram of the data
    ax.set_xlabel('x')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram and normal distribution for $x$')


# Sample data
data = [1.2, 2.1, 0.5, 1.8, 2.5, 0.9, 1.6, 1.3, 0.7, 1.1]

# Calculate mean and standard deviation
mu, sigma = np.mean(data), np.std(data)
PlotBoxPlot(data, mu, sigma)

DB15 = "DB_Rede_3_50_2403"

Simulations_to_Plot = [2, 3, 4, 6]
for Sim in Simulations_to_Plot:

    dfTable15 = GetHCTableBySimulation(DB15, Sim)
    dfDATA15 = GetHCDATABySimulation(DB15, Sim)
    PlotBoxPlot(dfDATA15['HC'].values*100, dfTable15['Average'].values*100, dfTable15['StandardDeviation'].values*100)


"""

DB = "DB_Rede_3_50_2403"

##########################
fig2, ax = plt.subplots()
df = GetHCDATA(DB)
# generate a boxplot based on the new grouping
plt.boxplot([df[df['SimulationCount'] == 2]['HC'] * 100,
             df[df['SimulationCount'] == 3]['HC'] * 100,
             df[df['SimulationCount'] == 4]['HC'] * 100,
             df[df['SimulationCount'] == 6]['HC'] * 100],
            showmeans=True, idths=0.7, meanline=True)

plt.xticks([1, 2, 3, 4], ['C/PV', 'VV', 'VW', 'VV+VW'])
plt.ylabel('HC(%)')
plt.title('Boxplot of HC simulations with and without controls')

# Save as PDF and PNG
plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Figs\Artigo2" +
            "\BOXPLOT_HC_DB_" + str(DB) + ".pdf",
            format='pdf', transparent=True)
plt.savefig(r"C:\Users\hugo1\Desktop\Projeto_Rede_Fornecida\Figs\Artigo2" + "\BOXPLOT_HC_DB_" + str(DB))
plt.show()
