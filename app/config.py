from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LOCATION_API_KEY: str
    WEATHER_API_KEY: str
    REDIS_URL: str
    REDIS_CACHE_TTL: int = 600
    RATE_LIMIT_REQUESTS: int = 5
    RATE_LIMIT_WINDOW: int = 60

    class Config:
        env_file = ".env"

settings = Settings() 