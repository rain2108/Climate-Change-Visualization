import streamlit as st
import pandas as pd
import altair as alt

# Set the title and description of your dashboard
st.title("Annual Surface Temperature Change")
st.markdown("""
This indicator presents the mean surface temperature change during the period 1961-2021,
using the 1951-1980 period as a baseline. Select a country from the drop-down below to view
its annual temperature change.
""")

# Load the CSV file (ensure the file path is correct)
data = pd.read_csv("Annual_Surface_Temperature_Change.csv")

# Create a list of unique countries for the dropdown menu
countries = sorted(data['Country'].unique())
selected_country = st.selectbox("Select a Country", countries)

# Filter the data for the selected country (assuming one row per country)
country_row = data[data['Country'] == selected_country].iloc[0]

# Identify columns corresponding to annual data (they start with 'F')
year_columns = [col for col in data.columns if col.startswith('F')]

# Convert the wide-format data into a long format using pandas
df_long = pd.DataFrame({
    'Year': [col.replace('F', '') for col in year_columns],
    'Temperature_Change': country_row[year_columns].values
})
df_long['Year'] = df_long['Year'].astype(int)
df_long = df_long.sort_values('Year')

# Display the filtered data (optional)
st.subheader(f"Temperature Change for {selected_country}")
st.write(df_long.head())

# Plot a simple line chart using Streamlit's built-in chart function
# st.line_chart(df_long.set_index('Year'))

# Alternatively, build a more customizable chart with Altair
chart = alt.Chart(df_long).mark_line(point=True).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Temperature_Change:Q', title='Temperature Change (°C)'),
    tooltip=['Year', 'Temperature_Change']
).properties(width=700, height=400)
st.altair_chart(chart, use_container_width=True)
