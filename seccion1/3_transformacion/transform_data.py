import pandas as pd
from sqlalchemy import create_engine, text
from psycopg2.extras import execute_values
import time
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

start_time = time.time()

engine = create_engine(Config.DB_URL)
conn = engine.connect()

csv_file  = Config.CSV_FILE
df        = pd.read_csv(csv_file)

# Renombrar columnas
df.rename(columns={
    'name': 'company_name',
    'paid_at': 'updated_at'
}, inplace=True)

# Convertir tipos de datos
df['id'] = df['id'].astype(str).str.slice(0, 24)
df['company_name'] = df['company_name'].astype(str)
df['company_id'] = df['company_id'].astype(str).str.slice(0, 24)
df['amount'] = df['amount'].astype(float).round(2)
df['status'] = df['status'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
df['updated_at'] = pd.to_datetime(df['updated_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')

df = df.replace({pd.NaT: None})
df['created_at'] = df['created_at'].fillna(pd.Timestamp.now()).infer_objects(copy=False)

# Validar valores de 'amount'
max_amount = 10**14 - 0.01 
df['amount'] = df['amount'].apply(lambda x: min(x, max_amount))

table_name = 'cargo'
create_table = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id VARCHAR(24) NOT NULL,
    company_name VARCHAR(130) NULL,
    company_id VARCHAR(24) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);
"""
conn.execute(text(create_table))
conn.commit()

# Función para insertar datos
def bulk_insert_to_postgres(dataframe, table, engine):
    tuples = [tuple(x) for x in dataframe.to_numpy()]
    cols = ','.join(list(dataframe.columns))
    
    query = f"INSERT INTO {table} ({cols}) VALUES %s"
    
    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cur:
            execute_values(cur, query, tuples)
        raw_conn.commit()
    finally:
        raw_conn.close()

bulk_insert_to_postgres(df, table_name, engine)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Datos transformados y guardados en la nueva tabla {table_name} en PostgreSQL")
print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")

conn.close()