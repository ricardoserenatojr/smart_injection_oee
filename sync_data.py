    import pandas as pd
from sqlalchemy import create_engine

# Trocando o ponto por [at] e forçando o user_id no final
URL = "postgresql://postgres.xpcekhdvztyaodwrhmfi:Vaitomanocu@aws-0-us-east-1.pooler.supabase.com:5432/postgres?options=-c%20user_id%3Dxpcekhdvztyaodwrhmfi"

try:
    engine = create_engine(URL)
    print("⏳ Tentando conexão final com os EUA...")

    # Envia os 3 arquivos (Certifique-se de que eles estão na mesma pasta do script)
    pd.read_csv('production_log_export.csv').to_sql('production_log', engine, if_exists='replace', index=False)
    pd.read_csv('downtime_log_export.csv').to_sql('downtime_log', engine, if_exists='replace', index=False)
    pd.read_csv('daily_oee_stats_export.csv').to_sql('daily_oee_stats', engine, if_exists='replace', index=False)

    print("✅ FINALMENTE! Dados carregados com sucesso no Supabase.")
except Exception as e:
    print(f"❌ Erro: {e}")