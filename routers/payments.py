from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BookingModel

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.get("/pay")
def simulate_payment_gateway(pnr: str, amount: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.pnr_code == pnr.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Giao dịch không tồn tại")
    
    booking.payment_status = "PAID"
    db.commit()
    
    return {
        "status": "success",
        "message": f"Thanh toán thành công {amount} VNĐ cho mã đặt chỗ {pnr}",
        "pnr_code": pnr,
        "payment_status": "PAID"
    }