import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# 1. Database Connection
engine = create_engine("postgresql://admin:admin_password@localhost:5432/factory_db")

# Page Config
st.set_page_config(page_title="Smart Injection OEE Dashboard", layout="wide")
st.title("Smart Injection - OEE Production Analysis")

# 2. Load the "Gold Table"
@st.cache_data(ttl=60) # Refresh every minute
def load_data():
    # Load Gold Table for OEE and Raw Downtime for Pareto
    df_stats = pd.read_sql("SELECT * FROM daily_oee_stats ORDER BY date DESC", engine)
    return df_stats

df = load_data()
# Ensure date types match for filtering
df['date'] = pd.to_datetime(df['date']).dt.date

# 3. Sidebar Filters
st.sidebar.header("Filters")
selected_machine = st.sidebar.multiselect("Select Machine", options=df['machine_id'].unique(), default=df['machine_id'].unique())
selected_mold = st.sidebar.multiselect("Select Mold", options=df['mold_id'].unique(), default=df['mold_id'].unique())
selected_date = st.sidebar.multiselect("Select Date", options=sorted(df['date'].unique(), reverse=True), default=df['date'].unique())

filtered_df = df[(df['machine_id'].isin(selected_machine)) & (df['mold_id'].isin(selected_mold) & (df['date'].isin(selected_date)))]

# 4. Top Level KPI Cards
st.subheader("Current Performance Metrics - OEE Goal: 85%")
col1, col2, col3, col4 = st.columns(4)

st.subheader("Total Production & Capacity Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Calculate averages for the filtered selection
avg_oee = filtered_df['oee'].mean() * 100
avg_avail = filtered_df['availability'].mean() * 100
avg_perf = filtered_df['performance'].mean() * 100
avg_qual = filtered_df['quality'].mean() * 100

total_good = filtered_df['good_parts'].sum()
total_defects = filtered_df['rejected_parts'].sum()
total_units = total_good + total_defects

col1.metric("Avg OEE", f"{avg_oee:.1f}%", delta=f"{avg_oee-85:.1f}% vs Goal")
col2.metric("Availability", f"{avg_avail:.1f}%")
col3.metric("Performance", f"{avg_perf:.1f}%")
col4.metric("Quality", f"{avg_qual:.1f}%")

kpi1.metric("Total Good Parts", total_good)
kpi2.metric("Total Defects", total_defects)
kpi3.metric("Total Units", total_units)
kpi4.metric(" Scrap Rate", f"{(total_defects/total_units)*100:.1f}%" if total_units > 0 else "0.0%")


st.divider()

# Updated Tab Structure
tab1, tab2, tab3 = st.tabs([
    "OEE & Mold Usage", 
    "Time & Quality Analysis", 
    "Raw Data"
])

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

# streamlit run dashboard/dashboard.py