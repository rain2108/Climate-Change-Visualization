import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load and process the data
@st.cache_data
def load_data():
    data = pd.read_csv("Change_in_Mean_Sea_Levels.csv")  # update with your CSV file path
    # Convert Date column to datetime and clean the data
    data['Date'] = data['Date'].str.replace(r'^[^\d]*', '', regex=True)
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Year'] = data['Date'].dt.year
    return data

data = load_data()

st.title("Climate Change Data Visualization: Mean Sea Levels")
st.markdown("""
This indicator gives estimates of the rise of global sea levels, based on measurements from satellite radar altimeters. 
These are produced by measuring the time it takes a radar pulse to make a round-trip from the satellite to the sea surface and back again. 
The graphs below show the data obtained by four satellite altimeters – TOPEX/Poseidon, Jason-1, Jason-2, and Jason-3 – which have monitored the same surfaces since 1992. 
On the right, you’ll see mean sea level changes for each of the world’s main seas and oceans.
""")

# Use the 'Measure' column for selecting the sea
st.subheader("Change in Mean Sea Levels by Satellite")
chart1 = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X('Date:T', title='Year'),
    y=alt.Y('Value:Q', title='Mean Sea Level Change'),
    color=alt.Color('Measure:N', title='Satellite Altimeter')
).properties(
    width=1000,
    height=500,
)
st.altair_chart(chart1, use_container_width=True)

seas = sorted(data['Measure'].unique())
selected_sea = st.selectbox("Select a Sea for Yearly Change Visualization", seas)

# Filter the data based on the selected sea
filtered_data = data[data['Measure'] == selected_sea]

# Aggregate data by year
yearly_data = filtered_data.groupby("Year")['Value'].mean().reset_index()

# Plot the yearly change chart
st.subheader(f"Yearly Change in Mean Sea Levels - {selected_sea}")
yearly_chart = alt.Chart(yearly_data).mark_line(point=True).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Value:Q', title='Mean Sea Level Change (mm)')
).properties(
    width=1000,
    height=500,
)
st.altair_chart(yearly_chart, use_container_width=True)

# --- Graph 2: Trend in Mean Sea Levels ---
st.header("Trend in Mean Sea Levels")

# Calculate the average sea level change per sea (using the whole dataset)
trend_data = data.groupby("Measure")['Value'].mean().reset_index()
trend_data = trend_data.sort_values("Value", ascending=True)

# Create a horizontal bar chart using Plotly Express
fig2 = px.bar(
    trend_data, 
    x="Value", 
    y="Measure", 
    orientation="h",
    title="Average Mean Sea Level Change by Sea",
    labels={"Value": "Mean Sea Level Change (mm)", "Measure": "Sea"}
)
st.plotly_chart(fig2, use_container_width=True)
