import streamlit as st
import pandas as pd
from utils.model_utils import train_price_model, predict_price
import plotly.graph_objs as go

df = pd.read_csv("data/price_data.csv")
st.title("📈 Crop Price Prediction")

crop = st.selectbox("Select Crop", df["Crop"].unique())
city = st.selectbox("Select City", df["City"].unique())

filtered = df[(df["Crop"] == crop) & (df["City"] == city)]
model = train_price_model(filtered)

last_row = filtered.iloc[-1]
predictions = predict_price(model, 6, pd.to_datetime(last_row["Date"]).month, pd.to_datetime(last_row["Date"]).year)

months, prices = zip(*predictions)
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Modal Price"], name="Historical"))
fig.add_trace(go.Scatter(x=months, y=prices, name="Predicted"))
st.plotly_chart(fig, use_container_width=True)