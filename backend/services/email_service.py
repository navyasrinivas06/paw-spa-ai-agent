import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_booking_email(to_email, booking):

    print("Email sending disabled.")
    return
    body = f"""
Hello,

Your booking has been received successfully.

Owner Name : {booking.name}
Phone       : {booking.phone}
Pet Name    : {booking.pet_name}
Pet Type    : {booking.pet_type}
Breed       : {booking.breed}
Service     : {booking.service}
Date        : {booking.date}
Time        : {booking.time}

Thank you for choosing Paw Spa & Nest!
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("Booking email sent successfully.")

    except Exception as e:
        print(f"Email sending failed: {e}")