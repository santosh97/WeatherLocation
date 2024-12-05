import httpx
from app.config import settings
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import ipaddress

logger = logging.getLogger(__name__)

class LocationService:
    def __init__(self):
        self.base_url = "http://ip-api.com/json"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_location(self, ip: str) -> dict:
        """Get location data for an IP address with retry logic"""
        try:
            # Validate IP address first
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                logger.error(f"Invalid IP address provided: {ip}")
                raise ValueError("Invalid IP address")
                
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{ip}",
                    params={"fields": "status,message,city,country,query"}
                )
                response.raise_for_status()
                data = response.json()
                
                logger.debug(f"Location API Response for IP {ip}: {data}")
                
                if data.get("status") != "success":
                    logger.error(f"API Error for IP {ip}: {data.get('message')}")
                    return None
                
                location_data = {
                    "city": data.get("city"),
                    "country": data.get("country")
                }
                
                if not location_data["city"] or not location_data["country"]:
                    logger.warning(f"Incomplete location data for IP {ip}: {location_data}")
                
                return location_data
        except Exception as e:
            logger.error(f"Error fetching location data for IP {ip}: {str(e)}")
            return None 