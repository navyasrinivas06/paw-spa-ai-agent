from pydantic import BaseModel
from typing import Optional

bookings = []

class Booking(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    pet_name: Optional[str] = None
    pet_type: Optional[str] = None
    breed: Optional[str] = None
    service: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None