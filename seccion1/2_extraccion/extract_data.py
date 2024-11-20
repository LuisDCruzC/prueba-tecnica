import pandas as pd
from sqlalchemy import create_engine
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

current_dir = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(Config.DB_URL)
conn = engine.connect()

df = pd.read_sql('SELECT * FROM data_prueba_tecnica', conn)

output_file = os.path.join(current_dir, Config.EXTRACT_CSV_FILE)
df.to_csv(output_file, index=False)

print(f'Datos extraídos y guardados en {output_file}')

conn.close()