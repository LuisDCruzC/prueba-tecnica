import pandas as pd
from sqlalchemy import create_engine, text
from psycopg2.extras import execute_values
import time
import uuid
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

start_time = time.time()
engine = create_engine(Config.DB_URL)
conn = engine.connect()

csv_file = Config.CSV_FILE
df = pd.read_csv(csv_file)

df.rename(columns={
    'name': 'company_name',
    'paid_at': 'updated_at'
}, inplace=True)

df['id'] = df['id'].astype(str).str.slice(0, 24)
df['company_name'] = df['company_name'].astype(str).str.strip()
df['company_id'] = df['company_id'].astype(str).str.slice(0, 24).replace(['*******', 'nan'], None)
df['amount'] = df['amount'].astype(float).round(2)
df['status'] = df['status'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
df['updated_at'] = pd.to_datetime(df['updated_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')

df = df.replace({pd.NaT: None})
df['created_at'] = df['created_at'].fillna(pd.Timestamp.now()).infer_objects(copy=False)

max_amount = 10**14 - 0.01
df['amount'] = df['amount'].apply(lambda x: min(x, max_amount))

valid_company_ids = df[df['company_id'].notna()][['company_name', 'company_id']].drop_duplicates()
company_map = dict(zip(valid_company_ids['company_name'], valid_company_ids['company_id']))

def replace_company_name_and_id(row):
    if row['company_name'] in ['MiP0xFFFF', 'MiPas0xFFFF']:
        row['company_name'] = 'MiPasajefy'
    if pd.isna(row['company_id']) and row['company_name'] in company_map:
        row['company_id'] = company_map[row['company_name']]
    if pd.isna(row['id']) or row['id'] == 'nan':
        row['id'] = str(uuid.uuid4()).replace('-', '')[:24]
    return row

df = df.apply(replace_company_name_and_id, axis=1)

df = df[df['company_id'].notna()]

# Crear tablas en la base de datos
conn.execute(text("DROP TABLE IF EXISTS charges CASCADE"))
conn.execute(text("DROP TABLE IF EXISTS companies CASCADE"))

create_companies_table = """
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(24) NOT NULL PRIMARY KEY,
    company_name VARCHAR(130) NULL
);
"""

create_charges_table = """
CREATE TABLE IF NOT EXISTS charges (
    id VARCHAR(24) NOT NULL PRIMARY KEY,
    company_id VARCHAR(24) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);
"""

conn.execute(text(create_companies_table))
conn.execute(text(create_charges_table))
conn.commit()

# Insertar datos en la tabla 'companies'
companies_df = df[['company_id', 'company_name']].drop_duplicates(subset=['company_id'])
companies_tuples = [tuple(x) for x in companies_df.to_numpy()]
companies_query = """
INSERT INTO companies (company_id, company_name) VALUES %s
"""

raw_conn = engine.raw_connection()
try:
    with raw_conn.cursor() as cur:
        execute_values(cur, companies_query, companies_tuples)
    raw_conn.commit()
finally:
    raw_conn.close()

# Insertar datos en la tabla 'charges'
charges_df = df[['id', 'company_id', 'amount', 'status', 'created_at', 'updated_at']].drop_duplicates(subset=['id'])
charges_tuples = [tuple(x) for x in charges_df.to_numpy()]
charges_query = """
INSERT INTO charges (id, company_id, amount, status, created_at, updated_at) VALUES %s
"""

raw_conn = engine.raw_connection()
try:
    with raw_conn.cursor() as cur:
        execute_values(cur, charges_query, charges_tuples)
    raw_conn.commit()
finally:
    raw_conn.close()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Datos transformados y guardados en las tablas 'companies' y 'charges' en PostgreSQL")
print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")

conn.close()