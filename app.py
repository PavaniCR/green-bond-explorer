import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data
df = pd.read_csv("green_bonds.csv")

st.title("Green Bond Explorer 🌱")
st.write("Explore global trends in green, social, and sustainability bond issuance by country, year, and bond type.")

# Sidebar filters
years = sorted(df["Year"].unique())
countries = sorted(df["Country"].unique())
bond_types = sorted([str(x) for x in df["Bond_Type"].dropna().unique()])

selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)
selected_bond_type = st.sidebar.selectbox("Select Bond Type", ["All"] + bond_types)

# Filter the data based on user selection
filtered = df[df["Year"] == selected_year]

if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]
if selected_bond_type != "All":
    filtered = filtered[filtered["Bond_Type"] == selected_bond_type]

st.write(f"### Bonds issued in {selected_year}")
st.dataframe(filtered)

# Plot total issuance by country for selected year and bond type
if not filtered.empty:
    country_data = filtered.groupby("Country")["Bond_Amount_USD"].sum().reset_index()
    fig = px.bar(country_data, x="Country", y="Bond_Amount_USD", title="Total Issuance by Country (USD Billion)")
    st.plotly_chart(fig)
else:
    st.write("No data available for selected filters.")
