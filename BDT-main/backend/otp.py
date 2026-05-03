import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import os
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def send_otp(email):
    otp = str(random.randint(100000, 999999))

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=email,
        subject="Your OTP Code",
        html_content=f"<strong>Your OTP is: {otp}</strong>",
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return otp
    except Exception as e:
        print("Email error:", e)
        return None