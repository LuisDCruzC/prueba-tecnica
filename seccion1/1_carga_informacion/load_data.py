import pandas as pd
from sqlalchemy import create_engine, text
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

csv_file  = Config.CSV_FILE
df        = pd.read_csv(csv_file)

engine = create_engine(Config.DB_URL)
conn = engine.connect()

def structure_sql(pandas_dtype):
    if pd.api.types.is_integer_dtype(pandas_dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(pandas_dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(pandas_dtype):
        return 'BOOLEAN'
    else:
        return 'TEXT'

table_name  = 'data'
columns     = [
    f"{col} {structure_sql(dtype)}" for col, dtype in zip(df.columns, df.dtypes)
]
create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"

conn.execute(text(create_table))

insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join([':' + col for col in df.columns])})"
for _, row in df.iterrows():
    conn.execute(text(insert_query), row.to_dict())

df.to_sql('data_prueba_tecnica', engine, if_exists='replace', index=False)

print('Tabla con datos creada exitosamente')

conn.close()