from pydantic import BaseModel, EmailStr

class FlightResponse(BaseModel):
    flight_number: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: int
    seats_available: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    flight_number: str
    passenger_name: str
    phone: str
    email: EmailStr

class BookingResponse(BaseModel):
    pnr_code: str
    flight_number: str
    airline: str
    passenger_name: str
    phone: str
    email: str
    total_amount: int
    payment_status: str
    payment_url: str

    class Config:
        from_attributes = True