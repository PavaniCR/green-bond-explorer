import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data
df = pd.read_csv("green_bonds.csv")

# Standardize Bond_Type values: lowercase, strip spaces, and group all variations
df["Bond_Type"] = df["Bond_Type"].astype(str).str.strip().str.lower()
df["Bond_Type"] = df["Bond_Type"].replace({
    "green bond": "green bonds",
    "green bonds": "green bonds",
    "social bond": "social bonds",
    "social bonds": "social bonds",
    "sustainability bond": "sustainability bonds",
    "sustainability bonds": "sustainability bonds",
    "not applicable": "",
    "nan": ""
})

# For display, use title case and remove empty values
years = sorted(df["Year"].unique())
countries = sorted([c for c in df["Country"].dropna().unique() if c.lower() != "not applicable" and c.strip() != ""])
bond_types_raw = [b for b in df["Bond_Type"].dropna().unique() if b != ""]
bond_types = sorted([b.title() for b in bond_types_raw])

st.title("Green Bond Explorer 🌱")
st.write("Explore global trends in green, social, and sustainability bond issuance by country, year, and bond type.")

# Add a user tip
st.info(
    "Tip: Not all countries have bonds in every year and bond type. "
    "If you see 'No data available,' try changing your selection."
)

# Sidebar filters
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)
selected_bond_type = st.sidebar.selectbox("Select Bond Type", ["All"] + bond_types)

# Filter the data based on user selection
filtered = df[df["Year"] == selected_year]

if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]
if selected_bond_type != "All":
    # Compare in title case for display
    filtered = filtered[filtered["Bond_Type"].str.title() == selected_bond_type]

st.write(f"### Bonds issued in {selected_year}")
st.dataframe(filtered)

if not filtered.empty:
    country_data = filtered.groupby("Country")["Bond_Amount_USD"].sum().reset_index()
    fig = px.bar(country_data, x="Country", y="Bond_Amount_USD", title="Total Issuance by Country (USD Billion)")
    st.plotly_chart(fig)
else:
    st.warning("No bond issuances found for the selected filters. Try different options!")
