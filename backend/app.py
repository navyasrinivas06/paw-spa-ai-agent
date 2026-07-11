from bookings.booking import Booking, bookings
from fastapi import FastAPI
from pydantic import BaseModel

from chatbot import ask_ai

from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from database import SessionLocal
from models import BookingDB
from sqlalchemy.orm import Session

from services.email_service import send_booking_email 

app = FastAPI(
    title="Paw Spa & Nest AI Agent",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://paw-spa-ai-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def home():
    return {
        "message": "🐾 Welcome to Paw Spa & Nest AI Agent!"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    reply = ask_ai(request.session_id, request.message)
    return {
        "reply": reply
    }

@app.post("/book")
def create_booking(booking: Booking):

    db = SessionLocal()

    new_booking = BookingDB(
        name=booking.name,
        phone=booking.phone,
        pet_name=booking.pet_name,
        pet_type=booking.pet_type,
        breed=booking.breed,
        service=booking.service,
        date=booking.date,
        time=booking.time
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    db.close()

# Send email after booking is saved
    send_booking_email(
        "pawspaandnest@gmail.com",
        booking
    )
    return {
        "message": "Booking created successfully!"
    }


@app.get("/bookings")
def get_bookings():

    db = SessionLocal()

    all_bookings = db.query(BookingDB).all()

    db.close()

    return all_bookings

@app.delete("/book/{booking_id}")
def delete_booking(booking_id: int):

    db = SessionLocal()

    booking = db.query(BookingDB).filter(
        BookingDB.id == booking_id
    ).first()

    if booking is None:
        db.close()
        return {"message": "Booking not found"}

    db.delete(booking)
    db.commit()
    db.close()

    return {"message": "Booking deleted successfully!"}

# from chatbot import ask_ai
"""
@app.post("/chat")
def chat(request: ChatRequest):
    reply = ask_ai(request.session_id, request.message)
    return {
        "reply": reply
    }
"""