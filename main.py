from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import airportsdata

app = FastAPI(title="Flight Booking API - Global", version="1.0.0")

# Cấu hình CORS cho phép Frontend từ Hostinger kết nối vào
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
    return {
        "status": "online",
        "message": "Welcome to Flight Booking API!",
        "endpoints": {
            "get_airports": "/api/airports",
            "search_flights": "/api/flights?origin=SGN&destination=HAN&date=2026-10-15"
        }
    }

@app.get("/api/airports")
def get_airports(q: str = Query(None, description="Tìm kiếm theo tên hoặc mã sân bay")):
    result = []
    for code, data in airports.items():
        # Lọc các sân bay thương mại có đầy đủ thông tin thành phố và quốc gia
        if data.get("city") and data.get("country"):
            item = {
                "code": code,
                "city": data["city"],
                "name": data["name"],
                "country": data["country"]
            }
            if q:
                if q.lower() in code.lower() or q.lower() in data["city"].lower() or q.lower() in data["name"].lower():
                    result.append(item)
            else:
                result.append(item)
    # Giới hạn trả về tối đa 100 kết quả để giao diện tải mượt mà
    return result[:100]

@app.get("/api/flights")
def search_flights(
    origin: str = Query(..., description="Mã sân bay đi"),
    destination: str = Query(..., description="Mã sân bay đến"),
    date: str = Query(..., description="Ngày đi YYYY-MM-DD")
):
    # Dữ liệu mẫu chuyến bay trả về dựa trên chặng bay bạn chọn
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
