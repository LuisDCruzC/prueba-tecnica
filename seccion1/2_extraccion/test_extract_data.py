import unittest
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from sqlalchemy import create_engine

class TestExtractData(unittest.TestCase):
  
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(Config.DB_URL)
        cls.conn = cls.engine.connect()
    
    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
    
    def test_extract_data(self):
        os.system('python seccion1/2_extraccion/extract_data.py')
        
        output_file = 'seccion1/2_extraccion/extract_data_prueba_tecnica.csv'
        self.assertTrue(os.path.exists(output_file), "El archivo CSV no se ha creado.")
        
        df = pd.read_csv(output_file)
        self.assertGreater(len(df), 0, "El archivo CSV está vacío.")
        
        df_db = pd.read_sql('SELECT * FROM data_prueba_tecnica', self.conn)
        
        df = df.where(pd.notnull(df), None)
        df_db = df_db.where(pd.notnull(df_db), None)
        
        pd.testing.assert_frame_equal(df, df_db, check_like=True)
    
if __name__ == '__main__':
    unittest.main()