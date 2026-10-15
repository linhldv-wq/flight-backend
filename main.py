import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import FlightModel
from routers import flights, bookings, payments

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    if db.query(FlightModel).count() == 0:
        sample_flights = [
            FlightModel(flight_number="VN 210", airline="Vietnam Airlines", origin="SGN", destination="HAN", departure_time="08:00", arrival_time="10:05", duration="2g 05m", price=1850000, seats_available=30),
            FlightModel(flight_number="VJ 152", airline="VietJet Air", origin="SGN", destination="HAN", departure_time="13:30", arrival_time="15:35", duration="2g 05m", price=1290000, seats_available=25),
        ]
        db.add_all(sample_flights)
        db.commit()
    db.close()

seed_data()

app = FastAPI(title="Flight Booking REST API", version="2.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(payments.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)