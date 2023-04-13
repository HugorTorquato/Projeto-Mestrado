import pyodbc
import sqlalchemy as sa
import pandas as pd

class SQLActions:

    # Define defalt variables to connect to database, engine
    def __init__(self, database):
        self.connection_string = \
            "DRIVER={ODBC Driver 17 for SQL Server};" \
            "SERVER={LAPTOP-5R3FI4O0\SQLEXPRESS};" \
            f"DATABASE={database};" \
            "UID=sa;" \
            "PWD=sa123"
        self.connection_url = sa.URL.create("mssql+pyodbc", query={"odbc_connect": self.connection_string})
        self.engine = sa.create_engine(self.connection_url)

    # Method to get table from database an return as pandas dataframe
    def ReturnTableFromSQLasDataframe(self, command):

        # CConnection will start and end inside this with, it will avoid memoryleak
        with self.engine.begin() as conn:
            return(pd.read_sql_query(sa.text(command), conn))





