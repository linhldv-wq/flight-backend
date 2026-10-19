import httpx
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import airportsdata

app = FastAPI(title="Waltme Live Flight API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

airports = airportsdata.load("IATA")
DUFFEL_ACCESS_TOKEN = "duffel_test_2iInettznX-PiY9qmpZMSrqeZBngaIMwX8upRdtEq9t"

@app.get("/api/airports")
def get_airports(q: str = Query(None)):
    result = []
    for code, data in airports.items():
        if data.get("city") and data.get("country"):
            item = {"code": code, "city": data["city"], "name": data["name"], "country": data["country"]}
            if q:
                if q.lower() in code.lower() or q.lower() in data["city"].lower():
                    result.append(item)
            else:
                result.append(item)
    return result[:500]

@app.get("/api/flights")
async def search_real_flights(
    origin: str = Query(...),
    destination: str = Query(...),
    date: str = Query(...)
):
    async with httpx.AsyncClient() as client:
        try:
            # Tạo yêu cầu tìm kiếm chuyến bay thực tế qua Duffel API
            response = await client.post(
                "https://api.duffel.com/air/offer_requests",
                headers={
                    "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
                    "Duffel-Version": "v1",
                    "Content-Type": "application/json"
                },
                json={
                    "data": {
                        "slices": [{"origin": origin, "destination": destination, "departure_date": date}],
                        "passengers": [{"type": "adult"}],
                        "cabin_class": "economy"
                    }
                },
                timeout=15.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            data = response.json()
            offers = data.get("data", {}).get("offers", [])
            
            # Định dạng lại dữ liệu trả về cho Frontend hiển thị
            formatted_flights = []
            for offer in offers[:10]: # Lấy top 10 chuyến bay tốt nhất
                owner = offer.get("owner", {})
                total_amount = float(offer.get("total_amount", 0))
                currency = offer.get("total_currency", "VND")
                
                # Lấy thông tin chặng bay
                slices = offer.get("slices", [])
                duration = "N/A"
                departure_time = "N/A"
                arrival_time = "N/A"
                flight_number = "N/A"
                
                if slices and slices[0].get("segments"):
                    seg = slices[0]["segments"][0]
                    duration = slices[0].get("duration", "N/A")
                    departure_time = seg.get("departing_at", "").split("T")[1][:5] if "T" in seg.get("departing_at", "") else ""
                    arrival_time = seg.get("arriving_at", "").split("T")[1][:5] if "T" in seg.get("arriving_at", "") else ""
                    flight_number = seg.get("marketing_flight_number", "N/A")

                formatted_flights.append({
                    "id": offer.get("id"),
                    "airline": owner.get("name", "Hãng hàng không quốc tế"),
                    "flight_number": flight_number,
                    "origin": origin,
                    "destination": destination,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "duration": duration,
                    "price": total_amount,
                    "currency": currency,
                    "seats_left": 9
                })

            return {"flights": formatted_flights}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
