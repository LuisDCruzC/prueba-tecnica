import unittest
import pandas as pd
from sqlalchemy import create_engine, text
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
class TestLoadData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(Config.DB_URL)
        cls.conn = cls.engine.connect()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_table_creation(self):
        result = self.conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'data_prueba_tecnica');"))
        exists = result.scalar()
        self.assertTrue(exists, "La tabla no se ha creado en la base de datos")

    def test_data_insertion(self):
        df = pd.read_sql('SELECT * FROM data_prueba_tecnica', self.conn)
        self.assertGreater(len(df), 0, "No se han insertado datos en la tabla")

if __name__ == '__main__':
    unittest.main()