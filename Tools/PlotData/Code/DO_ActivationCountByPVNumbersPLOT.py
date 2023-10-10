""""
This code aims to aggregate the average HC values into 3 tables and generate a forth one with the comparison
relation between them ( 15->30, 15->50, 30->50 ).
Also it is getting all HC results and adding into a boxplot for each configuration
    """

################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data1
data1 = {
    'Controls': ['0', '1', '2', '3', '4', '5', '6'],
    'VV': [4.6, 0.0, 0.6, 2.6, 12.6, 31.3, 48.0],
    'VW': [6.0, 9.3, 26.0, 32.6, 18.0, 7.3, 0.6],
    'VV&VW': [9.3, 10.6, 34.0, 28.0, 14.0, 4.0, 0.0]
}

df1 = pd.DataFrame(data1)
df1.set_index('Controls', inplace=True)

# Data2
data2 = {
    'Controls': ['0', '1', '2', '3', '4', '5', '6'],
    'VV': [0.0, 0.0, 0.0, 3.3, 14.0, 28.6, 54.0],
    'VW': [1.3, 10.6, 33.3, 32.0, 18.6, 4.0, 0.0],
    'VV&VW': [3.3, 16.0, 38.0, 34.60, 6.0, 2.0, 0.0]
}

df2 = pd.DataFrame(data2)
df2.set_index('Controls', inplace=True)

# Data3
data3 = {
    'Controls': ['0', '1', '2', '3', '4', '5', '6'],
    'VV': [0.0, 0.0, 0.0, 2.6, 10.0, 37.3, 50.0],
    'VW': [0.0, 5.3, 26.0, 29.3, 31.3, 8.0, 0.0],
    'VV&VW': [3.3, 18.0, 32.0, 32.60, 11.3, 2.6, 0.0]
}

df3 = pd.DataFrame(data3)
df3.set_index('Controls', inplace=True)

# Set the width of the bars
bar_width = 0.2

# Set the positions of the bars on the x-axis
r1 = np.arange(len(df1.index))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Plot the stacked bars for df1
plt.bar(r1, df1['VV'], width=bar_width, label='VV - df1')
plt.bar(r1, df1['VW'], width=bar_width, bottom=df1['VV'], label='VW - df1')
plt.bar(r1, df1['VV&VW'], width=bar_width, bottom=df1['VV']+df1['VW'], label='VV&VW - df1')

# Create custom legend handles and labels for df1
legend_handles_df1 = [plt.Rectangle((0, 0), 1, 1, color='blue', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='orange', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='green', alpha=0.7)]
legend_labels_df1 = ['VV - df1', 'VW - df1', 'VV&VW - df1']
plt.legend(legend_handles_df1, legend_labels_df1, title='df1', loc='upper left')

# Plot the stacked bars for df2
plt.bar(r2, df2['VV'], width=bar_width, label='VV - df2')
plt.bar(r2, df2['VW'], width=bar_width, bottom=df2['VV'], label='VW - df2')
plt.bar(r2, df2['VV&VW'], width=bar_width, bottom=df2['VV']+df2['VW'], label='VV&VW - df2')

# Create custom legend handles and labels for df2
legend_handles_df2 = [plt.Rectangle((0, 0), 1, 1, color='blue', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='orange', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='green', alpha=0.7)]
legend_labels_df2 = ['VV - df2', 'VW - df2', 'VV&VW - df2']
plt.legend(legend_handles_df2, legend_labels_df2, title='df2', loc='upper center')

# Plot the stacked bars for df3
plt.bar(r3, df3['VV'], width=bar_width, label='VV - df3')
plt.bar(r3, df3['VW'], width=bar_width, bottom=df3['VV'], label='VW - df3')
plt.bar(r3, df3['VV&VW'], width=bar_width, bottom=df3['VV']+df3['VW'], label='VV&VW - df3')

# Create custom legend handles and labels for df3
legend_handles_df3 = [plt.Rectangle((0, 0), 1, 1, color='blue', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='orange', alpha=0.7),
                      plt.Rectangle((0, 0), 1, 1, color='green', alpha=0.7)]
legend_labels_df3 = ['VV - df3', 'VW - df3', 'VV&VW - df3']
plt.legend(legend_handles_df3, legend_labels_df3, title='df3', loc='upper right')

# Set the x-axis labels
plt.xticks([r + bar_width for r in range(len(df1.index))], df1.index)

# Set the y-axis label
plt.ylabel('Count')

# Set the title
plt.title('Stacked Bar Plot')

# Show the plot
plt.show()











################################################################################################################
