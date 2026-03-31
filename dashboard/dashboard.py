import pandas as pd
import plotly.express as px
import streamlit as st
from supabase import create_client

# 1. Page Configuration
st.set_page_config(page_title="Smart Injection OEE Dashboard", layout="wide")

# 2. Data Loading Logic via API (Port 443 - Bypass network blocks)
@st.cache_data(ttl=60)
def load_data():
    try:
        # 1. Connection (Direct from Secrets)
        supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        
        # 2. Fetch and Convert to DataFrame
        response = supabase.table("daily_oee_stats").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if df.empty:
            return df

        # 3. Quick Clean: Columns to lowercase
        df.columns = df.columns.str.lower()
        
        # 4. Smart Conversion: Dates and Numbers in one go
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        cols = ['oee', 'availability', 'performance', 'quality', 'good_parts', 'rejected_parts', 'allocated_time', 'duration_min']
        # Convert only the columns that exist, forcing numeric and filling NaN with 0
        df[df.columns.intersection(cols)] = df[df.columns.intersection(cols)].apply(pd.to_numeric, errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"API Error: {e}")
        return pd.DataFrame()

# Data loading and verification
df = load_data()

if df.empty:
    st.warning("No records found. Check your Supabase table.")
    if st.button("Retry"):
        st.cache_data.clear()
        st.rerun()
    st.stop()

st.title("Smart Injection - OEE Production Analysis")

# 5. Sidebar Filters
st.sidebar.header("Analysis Filters")
selected_machine = st.sidebar.multiselect("Machine ID", options=df['machine_id'].unique(), default=df['machine_id'].unique())
selected_mold = st.sidebar.multiselect("Mold ID", options=df['mold_id'].unique(), default=df['mold_id'].unique())
all_dates = sorted(df['date'].unique(), reverse=True)
selected_date = st.sidebar.multiselect("Select Dates", options=all_dates, default=all_dates)

# Filtering Engine
filtered_df = df[
    (df['machine_id'].isin(selected_machine)) & 
    (df['mold_id'].isin(selected_mold)) & 
    (df['date'].isin(selected_date))
]

# 6. Main KPI Dashboard
st.subheader("Performance Indicators (OEE Target: 85%)")
kpi_oee, kpi_avail, kpi_perf, kpi_qual = st.columns(4)

def format_pct(val):
    return val * 100 if val <= 1.0 and val > 0 else val

avg_oee = format_pct(filtered_df['oee'].mean())
avg_avail = format_pct(filtered_df['availability'].mean())
avg_perf = format_pct(filtered_df['performance'].mean())
avg_qual = format_pct(filtered_df['quality'].mean())

kpi_oee.metric("Avg. OEE", f"{avg_oee:.1f}%", delta=f"{avg_oee-85:.1f}% vs Target")
kpi_avail.metric("Availability", f"{avg_avail:.1f}%")
kpi_perf.metric("Performance", f"{avg_perf:.1f}%")
kpi_qual.metric("Quality", f"{avg_qual:.1f}%")

# Secondary KPIs
st.subheader("Production Volume & Scrap Analysis")
m1, m2, m3, m4 = st.columns(4)

total_good = filtered_df['good_parts'].sum()
total_rejected = filtered_df['rejected_parts'].sum()
total_produced = total_good + total_rejected
scrap_rate = (total_rejected / total_produced * 100) if total_produced > 0 else 0

m1.metric("Good Parts", f"{total_good:,.0f}")
m2.metric("Scrap/Rejected", f"{total_rejected:,.0f}")
m3.metric("Total Produced", f"{total_produced:,.0f}")
m4.metric("Scrap Rate", f"{scrap_rate:.1f}%")

st.divider()
# 7. Visualization Tabs
tab1, tab2, tab3 = st.tabs(["OEE & Mold Usage", "Time & Quality Analysis", "Raw Data"])

# --- TAB 1: OEE & MOLD USAGE ---
with tab1:
    st.subheader("General Performance")
    c1, c2 = st.columns(2)

    with c1:
        st.write("### OEE Trend per Machine")
        fig_line = px.line(filtered_df, x='date', y='oee', color='machine_id', markers=True,
                           labels={'oee': 'OEE %', 'date': 'Date'})
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.write("### Total Good Parts by Mold")
        fig_bar = px.bar(filtered_df.groupby('mold_id')['good_parts'].sum().reset_index(), 
                         x='mold_id', y='good_parts', color='mold_id', text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: TIME & QUALITY ANALYSIS ---
with tab2:
    # Time Analysis Section
    st.subheader("Time Allocation Analysis (Minutes)")
    time_df = filtered_df.groupby(['date', 'machine_id']).agg({
        'allocated_time': 'first',
        'duration_min': 'sum'
    }).reset_index()
    time_df['Actual Run Time'] = time_df['allocated_time'] - time_df['duration_min']
    time_df = time_df.rename(columns={'duration_min': 'Downtime'})

    fig_time = px.bar(time_df, x='date', y=['Actual Run Time', 'Downtime'], 
                      color_discrete_map={'Actual Run Time': '#27ae60', 'Downtime': '#e74c3c'},
                      barmode='stack', title="Daily Production Time vs. Losses")
    st.plotly_chart(fig_time, use_container_width=True)

    st.divider()

    # Quality Section
    st.subheader("Quality Analysis (Scrap Rate)")
    fig_scatter = px.scatter(filtered_df, x='good_parts', y='rejected_parts', 
                             color='mold_id', size='oee', hover_data=['date', 'machine_id'])
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 3: RAW DATA ---
with tab3:
    st.subheader("Detailed Data Log")
    st.dataframe(filtered_df, use_container_width=True)