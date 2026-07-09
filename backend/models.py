from sqlalchemy import Column, Integer, String
from database import Base

class BookingDB(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    phone = Column(String)
    pet_name = Column(String)
    pet_type = Column(String)
    breed = Column(String)
    service = Column(String)
    date = Column(String)
    time = Column(String)