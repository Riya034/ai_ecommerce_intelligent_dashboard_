import os
from fastapi import FastAPI
import pandas as pd
import joblib
import re

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("model.pkl")

# Load data
df = pd.read_csv(
    "https://drive.google.com/uc?id=14PhCD4ABT5uWrQqdL5OpX2LsrVfZwJ6s",
    encoding="ISO-8859-1",
    low_memory=False
)

df.columns = df.columns.str.lower().str.strip()
df["total"] = df["price"] * df["quantity"]

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/predict")
def predict(price: float, quantity: int):
    pred = model.predict([[price, quantity, price]])
    return {"revenue": float(pred[0])}

@app.get("/summary")
def summary():
    return {
        "revenue": float(df["total"].sum()),
        "orders": int(len(df))
    }

# ---------------- AUTH (DEMO MODE) ----------------

def is_valid_email(email: str):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.post("/send-otp")
def send(email: str):
    if not is_valid_email(email):
        return {"error": "Invalid email format"}

    return {"message": "OTP sent (demo mode)"}


@app.post("/login-otp")
def login_with_otp(email: str, otp: str):
    if not is_valid_email(email):
        return {"error": "Invalid email"}
    return {"message": "Login successful"}


