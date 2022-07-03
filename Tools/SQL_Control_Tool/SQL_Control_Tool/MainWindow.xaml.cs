using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using SQL_Control_Tool.Conect_to_SQL;

namespace SQL_Control_Tool
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        DatabaseInteraction DI = new DatabaseInteraction(@"LAPTOP-5R3FI4O0\SQLEXPRESS", "DB_Rede_3", "sa", "sa123");

        public MainWindow()
        {
            InitializeComponent();
            
        }

        private void Create_Con_SQL(object sender, RoutedEventArgs e)
        {
            DI.DefineDatabase();
        }
    }
}
