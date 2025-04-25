import streamlit as st
import pandas as pd
import pickle
import numpy as np

def crop_recommendation_page():
    st.title("🌾 Crop Recommendation System")

    # Load pre-trained ML model
    try:
        with open("utils/crop_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        st.error("The ML model file (crop_model.pkl) is missing. Please train the model and place it in the 'utils' directory.")
        return

    # Input Fields
    soil_type = st.selectbox("Select Soil Type", ["Loamy", "Sandy", "Clay"])
    region = st.selectbox("Select Region", ["North Karnataka", "South Karnataka"])
    land_size = st.number_input("Enter Land Size (in acres)", min_value=1.0)

    # Convert categorical inputs to numerical values
    soil_mapping = {"Loamy": 0, "Sandy": 1, "Clay": 2}
    region_mapping = {"North Karnataka": 0, "South Karnataka": 1}

    if st.button("Get Recommendations"):
        # Prepare input data for the model
        input_data = np.array([
            soil_mapping[soil_type],
            region_mapping[region],
            land_size
        ]).reshape(1, -1)

        # Predict crop recommendations using the ML model
        predictions = model.predict(input_data)
        predicted_crops = model.predict_proba(input_data)

        # Example realistic data table for crop details
        # This data should ideally come from your dataset or database
        crop_details = {
            "Tomato": {"Expected Return per Acre (₹)": 50000, "Expense per Acre (₹)": 20000, "Star Rating": "⭐⭐⭐⭐", "Demand Score": 85},
            "Onion": {"Expected Return per Acre (₹)": 45000, "Expense per Acre (₹)": 18000, "Star Rating": "⭐⭐⭐", "Demand Score": 80},
            "Chili": {"Expected Return per Acre (₹)": 60000, "Expense per Acre (₹)": 25000, "Star Rating": "⭐⭐⭐⭐⭐", "Demand Score": 90},
        }

        # Generate recommendations
        recommendations = []
        for crop, prob in zip(predictions[0], predicted_crops[0]):
            crop_info = crop_details.get(crop, {})
            if crop_info:
                crop_info["Crop"] = crop
                crop_info["Probability (%)"] = round(prob * 100, 2)
                crop_info["Total Expected Return (₹)"] = crop_info["Expected Return per Acre (₹)"] * land_size
                crop_info["Total Expense (₹)"] = crop_info["Expense per Acre (₹)"] * land_size
                crop_info["Profitability (₹)"] = crop_info["Total Expected Return (₹)"] - crop_info["Total Expense (₹)"]
                recommendations.append(crop_info)

        # Convert to DataFrame
        df = pd.DataFrame(recommendations)

        # Display the table
        st.subheader("Crop Recommendations")
        st.table(df)

        # Additional Insights
        st.subheader("Insights")
        most_profitable = df.loc[df["Profitability (₹)"].idxmax()]
        st.success(f"The most profitable crop for your selection is **{most_profitable['Crop']}** with an estimated profitability of **₹{most_profitable['Profitability (₹)']:,.2f}**.")
