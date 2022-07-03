using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;
using System.Configuration;

namespace SQL_Control_Tool.Conect_to_SQL
{
    class DatabaseInteraction
    {
        public string Server { get; set; }
        public string Database { get; set; }
        public string User { get; set; }
        public string Password { get; set; }
        public string ConString { get; set; }

        public DatabaseInteraction(string server, string database, string user, string password)
        {
            Server = server;
            Database = database;
            User = user;
            Password = password;

        }

        // Definir os metodos que podem gerar ações no banco

        private string GetConnectionString(string connString)
        {
            // This function will return the correct connection string from app.config definition
            return ConfigurationManager.ConnectionStrings[connString].ConnectionString;
        }

        // COnectar ao sql e definir o banco se não existir ainda

        public void DefineDatabase()
        {
            ConString = GetConnectionString("RedeMaster");

            using (SqlConnection connection = new SqlConnection(ConString))
            {
                connection.Open();

                //Provide the command to execute
                using (SqlCommand cmd = new SqlCommand())
                {
                    cmd.Connection = connection;
                    cmd.CommandText = "SELECT @@VERSION as a";

                    // STORE THE RESULT
                    SqlDataReader dr = cmd.ExecuteReader();

                    while (dr.Read())
                    {
                        string data = dr["a"].ToString();
                        Console.WriteLine($"{data}");
                    }
                    dr.Close();
                }

                
            }
        }


        // Rodar uma query existente ( arquivo .sql )
            // Definir tabelas

            // Definir Store procedures

            // Definir views

        // Execultar store procedure sql
    }
}
