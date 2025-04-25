import streamlit as st
import pandas as pd

st.title("🌾 Crop Recommendation System")

soil_type = st.selectbox("Select Soil Type", ["Loamy", "Sandy", "Clay"])
region = st.selectbox("Select Region", ["North Karnataka", "South Karnataka"])
land_size = st.number_input("Enter Land Size (in acres)", min_value=1.0)

if st.button("Get Recommendations"):
    # Dummy logic for recommendation
    recommendations = [
        {"Crop": "Tomato", "Expected Return (₹)": 50000, "Demand Score": 85},
        {"Crop": "Onion", "Expected Return (₹)": 45000, "Demand Score": 80},
    ]
    df = pd.DataFrame(recommendations)
    st.table(df)
