import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:admin_password@localhost:5432/factory_db")

def calculate_oee():
    # 1. Load Data
    df_prod = pd.read_sql("SELECT * FROM production_log", engine)
    df_down = pd.read_sql("SELECT * FROM downtime_log", engine)

    # Date normalization
    df_prod['date'] = pd.to_datetime(df_prod['created_at']).dt.date
    df_down['date'] = pd.to_datetime(df_down['created_at']).dt.date

    # 2. Grouping
    daily_prod = df_prod.groupby(['date', 'machine_id', 'mold_id']).agg({
        'good_parts': 'sum',
        'rejected_parts': 'sum'
    }).reset_index()

    daily_down = df_down.groupby(['date', 'machine_id', 'mold_id']).agg({
        'duration_min': 'sum'
    }).reset_index()

    # 3. Merge
    df = pd.merge(daily_prod, daily_down, on=['date', 'machine_id', 'mold_id'], how='left').fillna(0)

    # --- THE MATH (NUMPY) ---
    # Total Shift = 480. We split it by the number of unique molds run on that machine that day.
    # This handles your "Random Use" logic.
    molds_per_day = df.groupby(['date', 'machine_id'])['mold_id'].transform('count')
    df['allocated_time'] = 480 / molds_per_day 
    
    # Ideal Cycle Time: 0.33 mins (20 seconds)
    ideal_cycle = 0.33

    # A - Availability: (Allocated Time - Downtime) / Allocated Time
    df['availability'] = np.where(df['allocated_time'] > 0, 
                                 (df['allocated_time'] - df['duration_min']) / df['allocated_time'], 0)

    # P - Performance: (Total Parts * Ideal Cycle) / (Allocated Time - Downtime)
    total_parts = df['good_parts'] + df['rejected_parts']
    actual_run_time = df['allocated_time'] - df['duration_min']
    df['performance'] = np.where(actual_run_time > 0, 
                                (total_parts * ideal_cycle) / actual_run_time, 0)
    
    # Cap performance at 100% (to handle outliers in random data)
    df['performance'] = df['performance'].clip(upper=1.0)

    # Q - Quality: Good / Total
    df['quality'] = np.where(total_parts > 0, df['good_parts'] / total_parts, 0)

    # OEE
    df['oee'] = df['availability'] * df['performance'] * df['quality']

    # 4. Save to Gold Table
    df.to_sql('daily_oee_stats', engine, if_exists='replace', index=False)
    print("🚀 Gold Table 'daily_oee_stats' is ready with dynamic time allocation!")

if __name__ == "__main__":
    calculate_oee()