import streamlit as st
import pandas as pd

df = pd.read_csv("data/recommendation_data.csv")
st.title("🌾 Crop Recommendation")

location = st.selectbox("Select Your Region", df["Location"].unique())

st.subheader("Recommended Crops")
filtered = df[df["Location"] == location].sort_values(by="Profit_Percent", ascending=False)
st.dataframe(filtered[["Crop", "Growth_Time", "Avg_Price", "Profit_Percent"]])