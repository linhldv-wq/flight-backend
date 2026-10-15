from sqlalchemy import Column, Integer, String
from database import Base

class FlightModel(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    airline = Column(String, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_time = Column(String)
    arrival_time = Column(String)
    duration = Column(String)
    price = Column(Integer)
    seats_available = Column(Integer)

class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    pnr_code = Column(String, unique=True, index=True)
    flight_number = Column(String)
    airline = Column(String)
    passenger_name = Column(String)
    phone = Column(String)
    email = Column(String)
    total_amount = Column(Integer)
    payment_status = Column(String, default="PENDING")