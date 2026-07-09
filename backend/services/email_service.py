import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_booking_email(to_email, booking):

    subject = "Paw Spa & Nest - Booking Confirmation"

    body = f"""
Hello,

Your booking has been received.

Owner: {booking.name}
Pet: {booking.pet_name}
Service: {booking.service}
Date: {booking.date}
Time: {booking.time}

Thank you for choosing Paw Spa & Nest.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)