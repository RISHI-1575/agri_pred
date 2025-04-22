import pandas as pd
from sklearn.linear_model import LinearRegression

def train_price_model(df):
    df["Month"] = pd.to_datetime(df["Date"]).dt.month
    df["Year"] = pd.to_datetime(df["Date"]).dt.year
    X = df[["Month", "Year"]]
    y = df["Modal Price"]
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_price(model, months_ahead, last_month, last_year):
    preds = []
    for i in range(months_ahead):
        m = (last_month + i) % 12 or 12
        y = last_year + (last_month + i - 1) // 12
        pred = model.predict([[m, y]])[0]
        preds.append((f"{m}-{y}", pred))
    return preds