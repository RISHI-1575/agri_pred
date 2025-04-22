import streamlit as st
import pandas as pd

df = pd.read_csv("data/marketplace_data.csv")
st.title("🛒 Crop Marketplace")

if st.session_state.role == "company":
    with st.expander("📢 Post Crop Requirement"):
        crop = st.text_input("Crop Name")
        qty = st.number_input("Quantity (kg)", 0)
        price = st.number_input("Price Offered", 0)
        contact = st.text_input("Contact")
        deadline = st.date_input("Deadline")
        if st.button("Post Requirement"):
            st.success("Posted successfully! (Simulated)")

st.subheader("📋 All Open Requirements")
st.dataframe(df)