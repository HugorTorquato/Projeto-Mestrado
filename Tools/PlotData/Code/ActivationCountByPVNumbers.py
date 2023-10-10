"""

"""

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.max_rows', None)  # Display all rows

################################################################################################################

def GetActivationOcurrency(db, table):
    command = f"""
            WITH GETOCURRENCYNUMBER AS (
            SELECT 
                DISTINCT([Case]),
                (SELECT COUNT(*) FROM {db}.dbo.{table} TEMP WHERE TEMP.[Case] = viewRes.[Case]) AS Ocurrency
            FROM {db}.dbo.{table} viewRes
            )
            
            SELECT
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 1) AS '1_PV_Ocurrency',
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 2) AS '2_PV_Ocurrency',
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 3) AS '3_PV_Ocurrency',
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 4) AS '4_PV_Ocurrency',
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 5) AS '5_PV_Ocurrency',
                (SELECT COUNT(*) FROM GETOCURRENCYNUMBER WHERE Ocurrency = 6) AS '6_PV_Ocurrency'
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def Aggregate(DB_GROUP, table):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetActivationOcurrency(db, table)
        else:
            db_Result = db_Result + GetActivationOcurrency(db, table)

    return db_Result

################################################################################################################

# Define all tables related to each group
DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]

table = "vwGetVVControlActivation"
db15_count = Aggregate(DB15, table)
print("_---------------------------- Count Ocurrency db15_count: ", db15_count, table)
db30_count = Aggregate(DB30, table)
print("_---------------------------- Count Ocurrency db30_count : ", db30_count, table)
db50_count = Aggregate(DB50, table)
print("_---------------------------- Count Ocurrency db50_count : ", db50_count, table)

print()
table = "vwGetVWControlActivation"
db15_count = Aggregate(DB15, table)
print("_---------------------------- Count Ocurrency db15_count: ", db15_count, table)
db30_count = Aggregate(DB30, table)
print("_---------------------------- Count Ocurrency db30_count : ", db30_count, table)
db50_count = Aggregate(DB50, table)
print("_---------------------------- Count Ocurrency db50_count : ", db50_count, table)

print()
table = "vwGetVVVWControlActivation"
db15_count = Aggregate(DB15, table)
print("_---------------------------- Count Ocurrency db15_count: ", db15_count, table)
db30_count = Aggregate(DB30, table)
print("_---------------------------- Count Ocurrency db30_count : ", db30_count, table)
db50_count = Aggregate(DB50, table)
print("_---------------------------- Count Ocurrency db50_count : ", db50_count, table)




