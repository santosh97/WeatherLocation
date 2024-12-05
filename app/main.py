from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.location_service import LocationService
from app.services.weather_service import WeatherService
from app.services.cache_service import CacheService
from app.utils.rate_limiter import RateLimiter
from app.utils.validators import validate_ip
from app.config import settings

app = FastAPI(title="Weather By IP API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Initialize services
location_service = LocationService()
weather_service = WeatherService()
cache_service = CacheService()
rate_limiter = RateLimiter()

@app.get("/weather-by-ip")
async def get_weather_by_ip(request: Request, ip: str = None):
    # Get client IP if not provided
    client_ip = ip or request.client.host
    
    # Validate IP
    if not validate_ip(client_ip):
        raise HTTPException(status_code=400, detail="Invalid IP address")
    
    # Check rate limit
    if not await rate_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Check cache
    cached_result = await cache_service.get(client_ip)
    if cached_result:
        return cached_result
    
    # Get location data
    location_data = await location_service.get_location(client_ip)
    if not location_data:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Get weather data
    weather_data = await weather_service.get_weather(
        location_data["city"],
        location_data["country"]
    )
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    # Prepare response
    response = {
        "ip": client_ip,
        "location": location_data,
        "weather": weather_data
    }
    
    # Cache the result
    await cache_service.set(client_ip, response)
    
    return response 