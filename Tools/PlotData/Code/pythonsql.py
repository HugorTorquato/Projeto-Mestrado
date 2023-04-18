import pyodbc
import sqlalchemy as sa
import pandas as pd


class SQLActions:

    # Define default variables to connect to database, engine
    def __init__(self, database):
        self.servername = "LAPTOP-5R3FI4O0\SQLEXPRESS"
        self.username = "sa"
        self.password = "sa123"
        url = f"mssql+pyodbc://{self.username}:{self.password}@{self.servername}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

        self.engine = sa.create_engine(url)

    # Method to get table from database an return as pandas dataframe
    def returnTableFromSQLasDataframe(self, command):
        # CConnection will start and end inside this with, it will avoid memoryleak
        with self.engine.begin() as conn:
            return pd.read_sql_query(sa.text(command), conn)
