import os
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

otp_store = {}

def send_otp(email):
    try:
        email = email.strip().lower()   # ✅ normalize

        otp = str(random.randint(100000, 999999))
        otp_store[email] = otp

        api_key = os.getenv("SENDGRID_API_KEY")
        sender_email = os.getenv("SENDER_EMAIL")

        if not api_key:
            raise Exception("Missing SENDGRID_API_KEY")

        if not sender_email:
            raise Exception("Missing SENDER_EMAIL")

        message = Mail(
            from_email=sender_email,
            to_emails=email,
            subject="Your OTP Code",
            html_content=f"<strong>Your OTP is {otp}</strong>"
        )

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print("SENDGRID STATUS:", response.status_code)
        print(f"Stored OTP for {email}: {otp}")   # ✅ debug

        return True

    except Exception as e:
        print("OTP ERROR:", str(e))
        return False


def verify_otp(email, otp):
    email = email.strip().lower()   # ✅ normalize

    stored = otp_store.get(email)

    print(f"Verifying OTP for {email}")
    print(f"Entered OTP: {otp}")
    print(f"Stored OTP: {stored}")

    if not stored:
        print("No OTP found (maybe server restarted)")
        return False

    return str(stored) == str(otp)
