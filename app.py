import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Material Dataset Explorer", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

st.title("🌍 Material Dataset Explorer")
st.write("Explore and visualize material trends interactively.")

# --- Sidebar filters ---
st.sidebar.header("Filter Options")
materials = st.sidebar.multiselect("Select Material(s):", df["Material"].unique())
scenarios = st.sidebar.multiselect("Select Scenario(s):", df["Scenario"].unique())
regions = st.sidebar.multiselect("Select Region(s):", df["Region"].unique())

filtered_df = df.copy()
if materials:
    filtered_df = filtered_df[filtered_df["Material"].isin(materials)]
if scenarios:
    filtered_df = filtered_df[filtered_df["Scenario"].isin(scenarios)]
if regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

st.write("### Filtered Data")
st.dataframe(filtered_df.head())

# --- Visualization ---
st.write("### Material Demand Over Time")
year_columns = [c for c in filtered_df.columns if c.isdigit()]

if not filtered_df.empty:
    melted = filtered_df.melt(
        id_vars=["Material", "Scenario", "Region"],
        value_vars=year_columns,
        var_name="Year",
        value_name="Demand"
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=melted, x="Year", y="Demand", hue="Material", ax=ax)
    plt.title("Material Demand Trends")
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

