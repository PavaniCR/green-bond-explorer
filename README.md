# 🌱 Green Bond Explorer

**Green Bond Explorer** is an interactive web dashboard built with Streamlit to explore global trends in green, social, and sustainability bond issuances. This app was developed as part of my Financial Analytics coursework at Virginia Commonwealth University (VCU).

## 🚀 Live Demo

👉 [Launch the app](https://green-bond-explorer-b7gxquysp3zlffuq5iiyuw.streamlit.app/)

---

## 📊 What Does This App Do?

- Lets users filter and visualize bond issuance data by **year, country, and bond type** (green, social, sustainability)
- Provides **dynamic charts:** bar chart (by country), pie chart (by bond type), line chart (trends), and a global map of issuance
- Allows users to **download filtered datasets** for further analysis
- Shows summary metrics for current filters

---

## 🗂️ Data Source

- **Dataset:** [Green Bonds Issued - Climate Bonds Initiative (Cleaned)](https://www.kaggle.com/datasets/sayanroy729/green-bonds-issued)
- **Source:** Kaggle (aggregated from Climate Bonds Initiative and Refinitiv)
- **Fields:** Year, Country, Bond_Type, Type_of_Issuer, Use_of_Proceed, Principal_Currency, Value

---

## 🛠️ Technologies Used

- Python, Streamlit, Pandas, Plotly Express
- Hosted via Streamlit Community Cloud
- GitHub for version control

---

## 📝 How to Use

1. **Clone or download this repo.**
2. Ensure you have Python 3.8+ installed.
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Place the included `green_bonds.csv` in the project folder.
5. Run the app:
    ```bash
    streamlit run app.py
    ```
6. Or try it live at the [app link above](https://green-bond-explorer-b7gxquysp3zlffuq5iiyuw.streamlit.app/).

---

## 🎯 Features

- Sidebar filters for Year, Country, Bond Type (multi-level)
- Data table view of filtered results
- Download filtered data as CSV
- Bar chart: Issuance by country
- Pie chart: Share by bond type
- Line chart: Issuance trends over the years
- Choropleth map: Global issuance visualization
- Responsive warning/info messages for users

---

## 📢 About This Project

This project was created to provide an accessible, open-source tool for exploring sustainable finance data. It demonstrates hands-on data analytics, visualization, and web deployment skills relevant to the financial sector.



