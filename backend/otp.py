import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import os

# Get environment variables from Render
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def send_otp(email):
    # Check if env variables exist
    if not SENDGRID_API_KEY or not SENDER_EMAIL:
        print("⚠️ Missing SendGrid configuration")
        return None

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
