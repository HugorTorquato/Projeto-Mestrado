using System;
using export_SQL_2_CSV.Entities;

namespace export_SQL_2_CSV
{
    class Program
    {
        static void Main(string[] args)
        {
            DatabaseDetail DB = new DatabaseDetail("DB_Rede_3");


            DB.SaveTableData();

            Console.WriteLine(DB);

        }
    }
}
