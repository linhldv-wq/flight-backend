from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import FlightModel
from schemas import FlightResponse

router = APIRouter(prefix="/api/flights", tags=["Flights"])

@router.get("/", response_model=List[FlightResponse])
def get_flights(origin: str, destination: str, db: Session = Depends(get_db)):
    flights = db.query(FlightModel).filter(
        FlightModel.origin == origin.upper(),
        FlightModel.destination == destination.upper()
    ).all()
    return flights