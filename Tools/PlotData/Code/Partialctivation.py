"""

"""

import pythonsql
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.max_rows', None)  # Display all rows

################################################################################################################

def GetActivationOcurrency(db):
    command = f"""
                SELECT 
                    COUNT(*)
                FROM {db}.dbo.vwPartialVVActivation
                """
    return pythonsql.SQLActions(db).returnTableFromSQLasDataframe(command)

def Aggregate(DB_GROUP):
    db_Result = pd.DataFrame()

    for db in DB_GROUP:
        if db_Result.empty:
            db_Result = GetActivationOcurrency(db)
        else:
            db_Result = db_Result + GetActivationOcurrency(db)

    return db_Result

################################################################################################################

# Define all tables related to each group
DB15 = ["DB_Rede_3_50_2706_15", "DB_Rede_3_50_2806_15", "DB_Rede_3_50_3006_15"]
DB30 = ["DB_Rede_3_50_0107_30", "DB_Rede_3_50_0107_2_30", "DB_Rede_3_50_0107_3_30"]
DB50 = ["DB_Rede_3_50_0107_50", "DB_Rede_3_50_1207_50", "DB_Rede_3_50_0307_2_50"]

db15_count = Aggregate(DB15)
print("_---------------------------- Count artial Ocurrency db15_count : ", db15_count)
db30_count = Aggregate(DB30)
print("_---------------------------- Count artial Ocurrency db30_count : ", db30_count)
db50_count = Aggregate(DB50)
print("_---------------------------- Count artial Ocurrency db50_count : ", db50_count)




