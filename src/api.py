from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
from typing import List

app = FastAPI(title="Fraud Detection API")

# load trained model and scaler
model = joblib.load("models/randomforest_fraud_model.pkl")
scaler = joblib.load("models/scaler.pkl")


@app.get("/")
def home():
    return {"message": "Fraud Detection API running"}


@app.post("/predict")
def predict(transaction: List[float]):

    # validate feature count
    if len(transaction) != 30:
        raise HTTPException(
            status_code=400,
            detail="Transaction must contain exactly 30 features"
        )

    # convert to numpy
    data = np.array(transaction).reshape(1, -1)

    # scale features
    data_scaled = scaler.transform(data)

    # prediction
    prediction = model.predict(data_scaled)[0]
    probability = model.predict_proba(data_scaled)[0][1]

    return {
        "fraud_prediction": int(prediction),
        "fraud_probability": float(probability)
    }