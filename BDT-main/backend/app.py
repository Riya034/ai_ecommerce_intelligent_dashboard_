import os
from dotenv import load_dotenv

load_dotenv()
from passlib.hash import bcrypt
from backend.db import add_user, get_user
from backend.otp import send_otp
from fastapi import FastAPI
import pandas as pd
import joblib

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod me specific domain rakhna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

otp_store = {}

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
import time
import re

def is_valid_email(email: str):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
@app.post("/send-otp")
def send(email: str):
    if not is_valid_email(email):
        return {"error": "Invalid email format"}

    # 🚫 Prevent OTP spam (30 sec cooldown)
    if email in otp_store:
        last_time = otp_store[email]["time"]
        if time.time() - last_time < 30:
            return {"error": "Wait before requesting OTP again"}

    otp = send_otp(email)

    otp_store[email] = {
        "otp": otp,
        "time": time.time(),
        "status": "SENT"
    }

    return {"message": "OTP sent"}


@app.post("/verify-otp")
def verify(email: str, otp: str):
    data = otp_store.get(email)

    if not data:
        return {"error": "OTP not requested"}

    # expire after 120 seconds
    if time.time() - data["time"] > 120:
        otp_store.pop(email, None)
        return {"error": "OTP expired"}

    if data["otp"] == otp:
        otp_store[email]["status"] = "VERIFIED"
        return {"message": "Verified"}

    return {"error": "Invalid OTP"}
@app.post("/register")
def register(email: str, password: str):
    if get_user(email):
        return {"error": "User already exists"}

    if otp_store.get(email, {}).get("status") != "VERIFIED":
        return {"error": "OTP not verified"}

    hashed_password = bcrypt.hash(password)
    add_user(email, hashed_password)

    otp_store.pop(email, None)

    return {"message": "User registered"}


@app.post("/login")
def login(email: str, password: str):
    user = get_user(email)

    if user and bcrypt.verify(password, user[1]):
        return {"message": "Login successful"}

    return {"error": "Invalid credentials"}

