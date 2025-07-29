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

st.set_page_config(page_title="Green Bond Explorer", layout="wide")

st.title("Green Bond Explorer 🌱")
st.write("Explore global trends in green, social, and sustainability bond issuance by country, year, and bond type.")

# Sidebar About section and data source link
st.sidebar.markdown("#### About")
st.sidebar.info(
    "This app lets you explore global green, social, and sustainability bond issuances. "
    "Select filters and view dynamic charts! Data source: Kaggle (Climate Bonds Initiative)."
)
st.sidebar.markdown(
    "[Kaggle Data Source](https://www.kaggle.com/datasets/sayanroy729/green-bonds-issued)"
)

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
    filtered = filtered[filtered["Bond_Type"].str.title() == selected_bond_type]

st.write(f"### Bonds issued in {selected_year}")
st.write(f"Total records for selected filters: {len(filtered)}")
st.dataframe(filtered)

# Download filtered data button
if not filtered.empty:
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered.to_csv(index=False),
        file_name="filtered_green_bonds.csv",
        mime="text/csv"
    )

# Summary card / key stat
if not filtered.empty:
    total_issuance = filtered["Bond_Amount_USD"].sum()
    st.metric(label="Total Issuance (USD Billion)", value=round(total_issuance, 2))

# Bar chart: Issuance by country
if not filtered.empty:
    country_data = filtered.groupby("Country")["Bond_Amount_USD"].sum().reset_index()
    fig = px.bar(country_data, x="Country", y="Bond_Amount_USD", title="Total Issuance by Country (USD Billion)")
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart: Share by Bond Type
    pie_df = filtered.groupby("Bond_Type")["Bond_Amount_USD"].sum().reset_index()
    pie_df = pie_df[pie_df["Bond_Amount_USD"] > 0]
    if not pie_df.empty and len(pie_df) > 1:
        fig_pie = px.pie(pie_df, values="Bond_Amount_USD", names="Bond_Type",
                         title="Share by Bond Type (Selected Year & Country)")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Map visualization: Global issuance map
    map_df = filtered.groupby("Country")["Bond_Amount_USD"].sum().reset_index()
    if not map_df.empty and len(map_df) > 1:
        fig_map = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color="Bond_Amount_USD",
            hover_name="Country",
            color_continuous_scale="Greens",
            title="Global Issuance Map (USD Billion)"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # Time trend chart: Issuance over years for the chosen country/type (if filtered)
    if selected_country != "All" or selected_bond_type != "All":
        trend_df = df.copy()
        if selected_country != "All":
            trend_df = trend_df[trend_df["Country"] == selected_country]
        if selected_bond_type != "All":
            trend_df = trend_df[trend_df["Bond_Type"].str.title() == selected_bond_type]

        time_trend = trend_df.groupby("Year")["Bond_Amount_USD"].sum().reset_index()
        fig_trend = px.line(time_trend, x="Year", y="Bond_Amount_USD",
                            title="Bond Issuance Trend Over Years", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.warning("No bond issuances found for the selected filters. Try different options!")
