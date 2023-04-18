import pandas
import pythonsql
import matplotlib.pyplot as plt

command = """
    SELECT TOP (1000) [id]
      ,[Simulation]
      ,[Average]
      ,[StandardDeviation]
    FROM [DB_Rede_3_50_2403].[dbo].[spStatisticalResults]
    """

# Create the plot class and init all properties realted to it
x = pythonsql.SQLActions("DB_Rede_3_50_2403")

Firstdata = x.returnTableFromSQLasDataframe(command)

Firstdata.plot()



