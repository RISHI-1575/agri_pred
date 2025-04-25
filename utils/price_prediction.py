import streamlit as st
import pandas as pd
from utils.model_utils import train_price_model, predict_price
import plotly.graph_objs as go

def price_prediction_page():
    # Load data
    df = pd.read_csv("data/price_data.csv")
    st.title("📈 Crop Price Prediction")

    # User input
    crop = st.selectbox("Select Crop", df["Crop"].unique())
    city = st.selectbox("Select City", df["City"].unique())

    # Filter data based on user selection
    filtered = df[(df["Crop"] == crop) & (df["City"] == city)]

    # Ensure there is data for the selected crop and city
    if filtered.empty:
        st.error("No data available for the selected crop and city. Please try another combination.")
    else:
        # Train the model
        model = train_price_model(filtered)

        # Get the last row for the most recent date
        last_row = filtered.iloc[-1]

        # Predict prices
        try:
            predictions = predict_price(model, 6, pd.to_datetime(last_row["Date"]).month, pd.to_datetime(last_row["Date"]).year)

            # Ensure predictions are not empty
            if not predictions:
                st.error("Unable to generate predictions. Please try again later.")
            else:
                # Unpack predictions
                months, prices = zip(*predictions)

                # Plot the data
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Modal Price"], name="Historical"))
                fig.add_trace(go.Scatter(x=months, y=prices, name="Predicted"))
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred while generating predictions: {e}")
            st.stop()
