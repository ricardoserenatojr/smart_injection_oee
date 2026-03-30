import pandas as pd
from sqlalchemy import create_engine

# Database connection string
# postgresql://user:password@host:port/database
conn_string = "postgresql://admin:admin_password@localhost:5432/factory_db"
engine = create_engine(conn_string)

print("--- Production Log ---")
df_prod = pd.read_sql("SELECT * FROM production_log", engine)
print(df_prod)

print("\n--- Downtime Log ---")
df_down = pd.read_sql("SELECT * FROM downtime_log", engine)
print(df_down)