import os
import random
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from backend.db import save_otp, get_otp, delete_otp

OTP_EXPIRY = 5  # minutes


def send_otp(email):
    try:
        email = email.lower().strip()
        otp = str(random.randint(100000, 999999))

        expires_at = (datetime.utcnow() + timedelta(minutes=OTP_EXPIRY)).isoformat()

        # ✅ Save in DB
        save_otp(email, otp, expires_at)

        api_key = os.getenv("SENDGRID_API_KEY")
        sender_email = os.getenv("SENDER_EMAIL")

        message = Mail(
            from_email=sender_email,
            to_emails=email,
            subject="Your OTP Code",
            html_content=f"<strong>Your OTP is {otp}</strong>"
        )

        sg = SendGridAPIClient(api_key)
        sg.send(message)

        print("OTP SENT:", otp)

        return True

    except Exception as e:
        print("OTP ERROR:", str(e))
        return False


def verify_otp(email, otp):
    email = email.lower().strip()

    record = get_otp(email)

    if not record:
        return False

    stored_otp, expires_at = record

    # convert string → datetime
    expires_at = datetime.fromisoformat(expires_at)

    if datetime.utcnow() > expires_at:
        delete_otp(email)
        return False

    if stored_otp == otp:
        delete_otp(email)  # ✅ one-time use
        return True

    return False
