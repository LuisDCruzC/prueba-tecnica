from sqlalchemy import create_engine, text
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
# Conectar a la base de datos usando SQLAlchemy
engine = create_engine(Config.DB_URL)
conn = engine.connect()

# Crear la vista para mostrar el monto total transaccionado por día para las diferentes compañías
create_view_query = """
CREATE OR REPLACE VIEW daily_transactions AS
SELECT 
    c.company_id,
    COALESCE(cp.company_name, 'Unknown') AS company_name,
    DATE(c.created_at) AS transaction_date,
    SUM(c.amount) AS total_amount
FROM 
    charges c
LEFT JOIN 
    companies cp ON c.company_id = cp.company_id
GROUP BY 
    c.company_id, cp.company_name, DATE(c.created_at)
ORDER BY 
    transaction_date, company_name;
"""

# Ejecutar la consulta para crear la vista
conn.execute(text(create_view_query))

# Consultar y imprimir los resultados de la vista
result = conn.execute(text("SELECT * FROM daily_transactions"))
for row in result:
    print(row)

conn.close()