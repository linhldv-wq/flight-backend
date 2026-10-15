from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import airportsdata

app = FastAPI(title="Flight Booking API - Global", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tải toàn bộ dữ liệu sân bay thế giới theo chuẩn IATA
airports = airportsdata.load("IATA")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to Flight Booking API!"}

@app.get("/api/airports")
def get_airports(q: str = Query(None, description="Tìm kiếm theo tên hoặc mã sân bay")):
    result = []
    for code, data in airports.items():
        if data.get("city") and data.get("country"):
            item = {
                "code": code,
                "city": data["city"],
                "name": data["name"],
                "country": data["country"]
            }
            # Nếu người dùng có nhập từ khóa tìm kiếm
            if q:
                q_lower = q.lower()
                if q_lower in code.lower() or q_lower in data["city"].lower() or q_lower in data["name"].lower():
                    result.append(item)
            else:
                result.append(item)
                
    # Nếu không tìm kiếm gì, trả về tối đa 500 sân bay phổ biến thay vì giới hạn 100 như trước
    return result[:500]

@app.get("/api/flights")
def search_flights(
    origin: str = Query(..., description="Mã sân bay đi"),
    destination: str = Query(..., description="Mã sân bay đến"),
    date: str = Query(..., description="Ngày đi YYYY-MM-DD")
):
    sample_flights = [
        {
            "id": "FL001",
            "airline": "Vietnam Airlines",
            "flight_number": "VN 210",
            "origin": origin.upper(),
            "destination": destination.upper(),
            "departure_time": "08:00",
            "arrival_time": "10:05",
            "duration": "2g 05m",
            "price": 1850000,
            "seats_left": 30
        },
        {
            "id": "FL002",
            "airline": "VietJet Air",
            "flight_number": "VJ 152",
            "origin": origin.upper(),
            "destination": destination.upper(),
            "departure_time": "13:30",
            "arrival_time": "15:35",
            "duration": "2g 05m",
            "price": 1290000,
            "seats_left": 25
        }
    ]
    return {"flights": sample_flights}
