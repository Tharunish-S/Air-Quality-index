import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Air Quality EDA Dashboard",
    layout="wide"
)

st.title("🌍 Air Quality Index (AQI) – Advanced Interactive EDA Dashboard")

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
st.sidebar.header("📂 Upload AQI Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload AQI CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👆 Please upload the AQI dataset to begin analysis.")
    st.stop()

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip()

# 🔥 IMPORTANT FIX: clean categorical columns
df["Country"] = df["Country"].astype(str).str.strip()
df["City"] = df["City"].astype(str).str.strip()

# -------------------------------------------------
# REQUIRED COLUMNS CHECK
# -------------------------------------------------
required_columns = [
    "Country", "City", "AQI Value", "AQI Category",
    "CO AQI Value", "Ozone AQI Value",
    "NO2 AQI Value", "PM2.5 AQI Value",
    "lat", "lng"
]

missing = [col for col in required_columns if col not in df.columns]
if missing:
    st.error("❌ Dataset is missing required columns:")
    st.write(missing)
    st.stop()

# -------------------------------------------------
# DATA PREVIEW
# -------------------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# -------------------------------------------------
# SIDEBAR FILTERS (FIXED)
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].dropna().unique().tolist())
)

city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(df["City"].dropna().unique().tolist())
)

filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if city != "All":
    filtered_df = filtered_df[filtered_df["City"] == city]

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------
st.subheader("📊 Key AQI Indicators")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Locations", len(filtered_df))
k2.metric("Average AQI", round(filtered_df["AQI Value"].mean(), 1))
k3.metric("Max AQI", int(filtered_df["AQI Value"].max()))
k4.metric("Dominant Category", filtered_df["AQI Category"].mode()[0])

# -------------------------------------------------
# AQI CATEGORY COLORS
# -------------------------------------------------
aqi_colors = {

    "Good": "#00FF6A",                       
    "Moderate": "#FFE600",                   
    "Unhealthy for Sensitive Groups": "#FF9F1C",  
    "Unhealthy": "#FF3B3B",                  
    "Very Unhealthy": "#B5179E",             
    "Hazardous": "#7A0000"                   
}

# -------------------------------------------------
# AQI DISTRIBUTION
# -------------------------------------------------
st.subheader("📈 AQI Distribution by Category")

fig1 = px.histogram(
    filtered_df,
    x="AQI Value",
    color="AQI Category",
    nbins=40,
    barmode="relative",
    opacity=0.75,
    color_discrete_map=aqi_colors,
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# POLLUTANT COMPARISON (ADVANCED)
# -------------------------------------------------
st.subheader("🧪 Pollutant-wise Distribution")

pollutant = st.selectbox(
    "Select Pollutant",
    ["CO AQI Value", "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"]
)

fig3 = px.violin(
    filtered_df,
    x="AQI Category",
    y=pollutant,
    color="AQI Category",
    color_discrete_map=aqi_colors,
    box=True,
    points="all",
    template="plotly_dark"
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# GLOBAL AQI MAP
# -------------------------------------------------
st.subheader("🗺️ Global AQI Map")

fig4 = px.scatter_geo(
    filtered_df,
    lat="lat",
    lon="lng",
    size="AQI Value",
    color="AQI Category",
    color_discrete_map=aqi_colors,
    hover_name="City",
    hover_data=["Country", "AQI Value"],
    projection="natural earth",
    template="plotly_dark"
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# TOP 10 MOST POLLUTED CITIES
# -------------------------------------------------
st.subheader("🚨 Top 10 Most Polluted Cities")

top10 = filtered_df.sort_values("AQI Value", ascending=False).head(10)

fig5 = px.bar(
    top10,
    x="AQI Value",
    y="City",
    orientation="h",
    color="AQI Category",
    color_discrete_map=aqi_colors,
    template="plotly_dark"
)

fig5.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig5, use_container_width=True)

# -------------------------------------------------
# DOWNLOAD DATA
# -------------------------------------------------
st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_air_quality_data.csv")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.write("✅ Advanced Air Quality EDA using **Streamlit + Plotly**")

