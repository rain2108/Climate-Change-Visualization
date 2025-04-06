import streamlit as st
import pandas as pd
import altair as alt

# Title and description
st.title("Atmospheric Carbon Dioxide Concentrations Dashboard")
st.markdown("""
This indicator presents the monthly atmospheric carbon dioxide concentrations (in the unit provided)
dating back to 1958. Use the slider below to select a time period and explore the rate of year-on-year growth.
Data source: NOAA Global Monitoring Laboratory via FAOSTAT.
""")

# Load the dataset (ensure the CSV filename is correct)
data = pd.read_csv("Atmospheric_CO%E2%82%82_Concentrations.csv")

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%YM%m')

# Determine the minimum and maximum dates in the dataset
min_date = pd.to_datetime(data['Date'].min()).to_pydatetime()
max_date = pd.to_datetime(data['Date'].max()).to_pydatetime()

start_date, end_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)
# Filter the data based on the selected date range
filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)].copy()

# ---------------------------
# Graph 1: Monthly CO2 Concentrations
# ---------------------------
st.subheader("Monthly Atmospheric Carbon Dioxide Concentrations")
chart1 = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('Value:Q', title='CO₂ Concentration'),
    tooltip=['Date:T', 'Value:Q']
).properties(width=1000, height=500)
st.altair_chart(chart1, use_container_width=True)

# ---------------------------
# Calculate Year-on-Year Growth Rate
# ---------------------------
# Sort data by date to ensure correct calculation
filtered_data = filtered_data.sort_values('Date')

# Compute the percentage change with a lag of 12 months
filtered_data['YoY_Growth'] = filtered_data['Value'].pct_change(periods=12) * 100

# Remove rows where growth rate is NaN (e.g., the first 12 months)
growth_data = filtered_data.dropna(subset=['YoY_Growth'])

# ---------------------------
# Graph 2: Year on Year Growth Rate
# ---------------------------
st.subheader("Monthly CO₂ Concentrations Year on Year Growth Rate")
chart2 = alt.Chart(growth_data).mark_line(point=True).encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('YoY_Growth:Q', title='Year-on-Year Growth Rate (%)'),
    tooltip=['Date:T', alt.Tooltip('YoY_Growth:Q', format=".2f")]
).properties(width=1000, height=500)
st.altair_chart(chart2, use_container_width=True)
