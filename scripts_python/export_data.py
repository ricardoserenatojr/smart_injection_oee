import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:admin_password@localhost:5432/factory_db")

tables = ['production_log', 'downtime_log', 'daily_oee_stats']

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    # This saves each table to a CSV file in your project folder
    df.to_csv(f"{table}_export.csv", index=False)
    print(f"✅ {table} exported to {table}_export.csv")