using System;
using System.Collections.Generic;
using System.Text;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Globalization;

namespace export_SQL_2_CSV.Entities
{
    class DatabaseDetail
    {
        private static SqlConnection _connection;

        public string DBName { get; set; }
        public string UserName { get; }
        public string Password { get; }
        public List<string> Tables { get; set; }

        public DatabaseDetail(string dBName)
        {
            DBName = dBName;
            UserName = "sa";
            Password = "sa123";

            CreateConection();
            Tables = GetTableNames();
        }

        public bool CreateConection()
        {
            _connection?.Close();

            string conectionstring =
                $"Data Source=LAPTOP-5R3FI4O0\\SQLEXPRESS;" +
                $"Initial Catalog={DBName};" +
                $"User ID={UserName}; Password={Password}";

            _connection = new SqlConnection(conectionstring);
            _connection.Open();            

            return true;
        }

        // Listar todas as tabelas do banco
        public List<string> GetTableNames()
        {
            List<string> Tables = new List<string>();

            string cmd = 
                "SELECT INFO.TABLE_NAME " +
                "FROM INFORMATION_SCHEMA.TABLES AS INFO " +
                "WHERE INFO.TABLE_CATALOG = 'DB_Rede_3'";

            using (var command = new SqlCommand(cmd, _connection))
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    Tables.Add(reader["TABLE_NAME"].ToString());
                }
                
                reader.Close();
            }

            return Tables;
        }
        
        public void SaveTableData()
        {
            string saveFile = string.Empty;

            foreach (string table in Tables)
            {
                Console.WriteLine(" Saving table : " + table);

                saveFile = Path.Combine(
                    "C:\\Users\\hugo1\\Desktop\\Projeto_Rede_Fornecida\\Tools\\export_SQL_2_CSV\\Data", table + ".csv");

                string cmd =
                    $"SELECT * " +
                    $"FROM {table} AS t ";

                using (var command = new SqlCommand(cmd, _connection))
                using (var reader = command.ExecuteReader())
                using(var writer = new StreamWriter(saveFile))
                {
                    List<string> columns = new List<string>();

                    foreach(var Colum in reader.GetColumnSchema())
                    {
                        columns.Add(Colum.ColumnName);
                        writer.Write(Colum.ColumnName + ",");
                    }

                    writer.WriteLine();      

                    while (reader.Read())
                    {
                        string txt = string.Empty;

                        foreach (var col in columns)
                        {
                            var value = reader[col];
                            var A = value.GetType();

                            if (double.TryParse(value.ToString(), out double number))
                            {
                                value = reader[col].ToString().Replace(',','.');
                            }

                            txt += value + ",";
                        }

                        writer.WriteLine(txt);
                      
                    }
                    reader.Close();
                }
            }
        }

        public override string ToString()
        {
            return DBName + " " + UserName + " " + Password; 
        }
    }
}
