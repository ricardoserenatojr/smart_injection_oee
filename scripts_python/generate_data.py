import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine("postgresql://admin:admin_password@localhost:5432/factory_db")

machines = ['INJ_01', 'INJ_02']
molds = ['MOLD_A_PANEL', 'MOLD_B_TRIM']
reasons = ['Material Shortage', 'Mechanical Failure', 'Quality Adjustment']
days_to_generate = 30

prod_entries = []
down_entries = []

for i in range(days_to_generate):
    # Calculate date (going backwards from today)
    current_date = datetime.now() - timedelta(days=i)
    
    for machine in machines:
        # Scenario: Each machine runs 2 molds per shift (4 hours each)
        for idx, mold in enumerate(molds):
            # 1. Add a 'Mold Change' downtime BEFORE starting production for that mold
            # (Except maybe for the very first mold of the day, but usually a setup occurs)
            down_entries.append({
                'machine_id': machine,
                'mold_id': mold,
                'reason': 'Mold Change',
                'duration_min': np.random.randint(30, 60), # Setup takes 30-60 mins
                'created_at': current_date - timedelta(minutes=480 - (idx * 240))
            })

            # 2. Production Data
            good_parts = np.random.randint(400, 600)
            rejected = np.random.randint(2, 20)
            
            prod_entries.append({
                'machine_id': machine,
                'mold_id': mold,
                'good_parts': good_parts,
                'rejected_parts': rejected,
                'created_at': current_date - timedelta(minutes=240 - (idx * 240))
            })

            # 3. Random unplanned downtime during this specific mold's run
            if np.random.random() < 0.4:
                down_entries.append({
                    'machine_id': machine,
                    'mold_id': mold,
                    'reason': np.random.choice(reasons),
                    'duration_min': np.random.randint(10, 30),
                    'created_at': current_date - timedelta(minutes=120 - (idx * 120))
                })

# Upload to Postgres
pd.DataFrame(prod_entries).to_sql('production_log', engine, if_exists='append', index=False)
pd.DataFrame(down_entries).to_sql('downtime_log', engine, if_exists='append', index=False)

print("✅ Logic-based factory history inserted. Mold Changes are now correctly attributed!")