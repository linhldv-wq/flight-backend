from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import random
import string
from database import get_db
from models import FlightModel, BookingModel
from schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, request: Request, db: Session = Depends(get_db)):
    flight = db.query(FlightModel).filter(FlightModel.flight_number == booking.flight_number).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay")
    
    if flight.seats_available <= 0:
        raise HTTPException(status_code=400, detail="Chuyến bay đã hết chỗ")
    
    flight.seats_available -= 1
    
    pnr = "SKY" + "".join(random.choices(string.digits, k=4))
    
    new_booking = BookingModel(
        pnr_code=pnr,
        flight_number=flight.flight_number,
        airline=flight.airline,
        passenger_name=booking.passenger_name.upper(),
        phone=booking.phone,
        email=booking.email,
        total_amount=flight.price,
        payment_status="PENDING"
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # Lấy base URL động từ request để link thanh toán tự động khớp với domain thực tế trên Cloud
    base_url = str(request.base_url).rstrip("/")
    payment_gateway_url = f"{base_url}/api/payments/pay?pnr={pnr}&amount={flight.price}"
    
    return BookingResponse(
        pnr_code=new_booking.pnr_code,
        flight_number=new_booking.flight_number,
        airline=new_booking.airline,
        passenger_name=new_booking.passenger_name,
        phone=new_booking.phone,
        email=new_booking.email,
        total_amount=new_booking.total_amount,
        payment_status=new_booking.payment_status,
        payment_url=payment_gateway_url
    )

@router.get("/{pnr_code}", response_model=BookingResponse)
def get_booking_by_pnr(pnr_code: str, request: Request, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.pnr_code == pnr_code.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Mã đặt chỗ không tồn tại")
    
    base_url = str(request.base_url).rstrip("/")
    payment_gateway_url = f"{base_url}/api/payments/pay?pnr={booking.pnr_code}&amount={booking.total_amount}"
    
    return BookingResponse(
        pnr_code=booking.pnr_code,
        flight_number=booking.flight_number,
        airline=booking.airline,
        passenger_name=booking.passenger_name,
        phone=booking.phone,
        email=booking.email,
        total_amount=booking.total_amount,
        payment_status=booking.payment_status,
        payment_url=payment_gateway_url
    )