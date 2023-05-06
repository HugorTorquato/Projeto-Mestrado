import unittest
import sys
sys.path.append('../Code')
import pythonsql

class SQLActionsTestCase(unittest.TestCase):

    # Adicionar test para quando for nome de banco errado
    my_obj = pythonsql.SQLActions("DB_Rede_3")

    def test_returnTableFromSQLasDataframe_SimpleQuery(self):

        command = """
                        SELECT 1
                    """

        self.assertEqual(self.my_obj.returnTableFromSQLasDataframe(command).values, 1)

    def test_returnTableFromSQLasDataframe_SimpleCountQuery(self):

        command = """
                        SELECT TOP 10 COUNT(*) FROM tblMonitoresData WHIT (NOLOCK)
                    """

        self.assertGreater(self.my_obj.returnTableFromSQLasDataframe(command).values, 1)

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
