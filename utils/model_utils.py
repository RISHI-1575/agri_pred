from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def train_price_model(data):
    model = LinearRegression()
    data["Month"] = pd.to_datetime(data["Date"]).dt.month
    model.fit(data[["Month"]], data["Modal Price"])
    return model

def predict_price(model, months_ahead, start_month, start_year):
    months = [(start_year, start_month + i) for i in range(months_ahead)]
    predicted_prices = model.predict(np.array([m[1] for m in months]).reshape(-1, 1))
    return months, predicted_prices
