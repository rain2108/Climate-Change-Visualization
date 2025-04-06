import streamlit as st
import pandas as pd
import altair as alt

# Load and process the disaster dataset
@st.cache_data
def load_disaster_data():
    df = pd.read_csv("Climate-related_Disasters_Frequency.csv")

    # Extract disaster type from the 'Indicator' column
    df['Disaster Type'] = df['Indicator'].str.extract(r'Disasters: (.+)$')

    # Keep only desired disaster types
    allowed_disasters = ['Landslide', 'Extreme temperature', 'Wildfire', 'Storm', 'Flood', 'Drought']
    df = df[df['Disaster Type'].str.lower().isin([d.lower() for d in allowed_disasters])]

    # Melt the year columns into a long format
    year_columns = [col for col in df.columns if col.startswith('F')]
    df_melted = df.melt(id_vars=['Country', 'Disaster Type'], value_vars=year_columns,
                        var_name='Year', value_name='Disaster Count')

    # Clean and convert 'F1980' -> 1980
    df_melted['Year'] = df_melted['Year'].str.extract(r'F(\d+)').astype(int)
    df_melted['Disaster Count'] = df_melted['Disaster Count'].fillna(0)

    return df_melted

# Load the data
data = load_disaster_data()

st.title("Climate-Related Natural Disasters Over Time")

# Dropdown for selecting country
country_list = sorted(data['Country'].dropna().unique())
selected_country = st.selectbox("Select a Country", country_list)

# Filter data by selected country
filtered_data = data[data['Country'] == selected_country]

# Plot stacked column chart
chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Disaster Count:Q', stack='zero', title='Number of Disasters'),
    color=alt.Color('Disaster Type:N', title='Disaster Type'),
    tooltip=['Year', 'Disaster Type', 'Disaster Count']
).properties(
    width=1000,
    height=500,
    title=f"Climate-Related Disasters in {selected_country} (1980–2022)"
)

st.altair_chart(chart, use_container_width=True)
